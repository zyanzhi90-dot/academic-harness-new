"""Problem and concrete-method loop on the retained Controller's single State."""

from __future__ import annotations

from copy import deepcopy
import json
import re
from pathlib import Path
import uuid

from arisctl.controller import ARISController, ControllerError
from arisctl.gateways import now
from arisctl.project_setup import install_project_codex_layer, verify_formal_native_subagent_runtime
from arisctl.validators import ValidationError, sha256_file
from arisctl.workflow import literature_workflow_path, research_workflow_path
from tools.literature_coverage_audit import audit_landscape

from . import scientific_validators as v


class ScientificController(ARISController):
    """The scientific extension shares _StateStore, registries, receipts and recovery."""

    def __init__(self, root, run_id, workflow_path=None):
        super().__init__(root, run_id, workflow_path or research_workflow_path())

    @classmethod
    def attach(cls, root, run_id):
        """Adopt an accepted standalone landscape without redoing any research."""
        # Validate the ID through the existing Controller before reading State.
        from tools import run_state
        path = Path(run_state._run_path(str(root), run_id))
        state = json.loads(path.read_text(encoding="utf-8"))
        if state["workflow"].get("mode") == "research_cycle":
            return cls(root, run_id)
        if state["workflow"].get("mode") != "literature_only":
            raise ControllerError("only the accepted public literature profile can be adopted")
        old = ARISController(root, run_id, literature_workflow_path())
        old._require_stage(old.status(), "LANDSCAPE_ACCEPTED")
        for name in ("source_admission_policy", "active_field_map", "coverage_review"):
            old._assert_artifact_current(state["research_lit"], name)
        new = cls(root, run_id)
        install_project_codex_layer(root, literature_only=True)
        with old._store.mutate() as live:
            new._landscape(live)
            live.setdefault("workflow_adoptions", []).append({
                "from_sha256": live["workflow_sha256"], "to_sha256": new.workflow_sha256,
                "reason": "Attach scientific core to the same accepted landscape", "at": now(),
            })
            live["workflow"] = deepcopy(new.workflow)
            live["workflow_sha256"] = new.workflow_sha256
            live["scientific_core"]["status"] = "NOT_STARTED"
        return new

    def _landscape(self, state):
        research = self._require_stage(state, "LANDSCAPE_ACCEPTED")
        for name in ("source_admission_policy", "active_field_map", "coverage_review"):
            self._assert_artifact_current(research, name)
        audit = audit_landscape(self.root, state["workflow"], state=state)
        if not audit["ok"] or audit["coverage_status"] != "SUFFICIENT":
            raise ControllerError("scientific work requires a current accepted landscape")
        return research

    def _core(self, state, *stages):
        self._landscape(state)
        core = state["scientific_core"]
        if core.get("engine") != "research_cycle_v1" or (stages and core.get("current_phase") not in stages):
            raise ControllerError(f"scientific action requires {stages}; current={core.get('current_phase')}")
        return core

    def _evidence(self, state):
        known = {}
        for name in state["research_lit"]["accepted_artifacts"]:
            if name.startswith("evidence:"):
                record = self._assert_artifact_current(state["research_lit"], name)
                known[name.split(":", 1)[1]] = record
        return known

    def _bindings(self, state):
        records = dict(state["research_lit"]["accepted_artifacts"])
        records.update(state["scientific_core"].get("accepted_artifacts", {}))
        return {record["path"]: record["sha256"] for record in records.values()}

    def _assert_bindings(self, bindings):
        for relative, expected in bindings.items():
            path = (self.root / relative).resolve()
            if not path.is_relative_to(self.root) or not path.is_file() or sha256_file(path) != expected:
                raise ControllerError(f"scientific input changed or missing: {relative}")

    def _read(self, record):
        self._assert_bindings({record["path"]: record["sha256"]})
        return json.loads((self.root / record["path"]).read_text(encoding="utf-8"))["content"]

    def _publish(self, state, kind, content):
        path = self._canonical_path(f"science-{kind}-{uuid.uuid4().hex}")
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema_version": 1, "kind": kind, "run_id": self.run_id,
                   "workflow_sha256": self.workflow_sha256, "at": now(),
                   "upstream_bindings": self._bindings(state), "content": deepcopy(content)}
        path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        self._store.recover_on_mutation_failure(lambda: path.unlink(missing_ok=True))
        record = {"path": str(path.relative_to(self.root)), "sha256": sha256_file(path),
                  "validator_result": "PASS", "at": payload["at"], "kind": kind}
        state["scientific_core"]["accepted_artifacts"][kind] = record
        state["scientific_core"]["artifact_history"].append(deepcopy(record))
        return record

    def _transition(self, core, stage, reason):
        before = core["current_phase"]
        core["current_phase"] = stage
        core["status"] = "METHOD_CONFIRMED" if stage == "METHOD_CONFIRMED" else "RESEARCH_ACTIVE"
        core["transition_log"].append({"from": before, "to": stage, "reason": reason, "at": now()})

    def _pending(self, core, stage):
        return {item["id"]: item for item in core["feedback"] if item["target"] == stage and not item.get("consumed_by")}

    def _consume_feedback(self, core, responses, record):
        for response in responses:
            item = next(item for item in core["feedback"] if item["id"] == response["feedback_id"])
            item.update({"response": deepcopy(response), "consumed_by": deepcopy(record)})

    def _feedback(self, core, target, rationale, requested_change, *, evidence_ids=(), source=None):
        item = {"id": uuid.uuid4().hex, "target": target, "rationale": rationale,
                "requested_change": requested_change, "evidence_ids": list(evidence_ids),
                "source": deepcopy(source), "at": now(), "consumed_by": None}
        core["feedback"].append(item)
        return item

    def begin(self, frame):
        v.validate_frame(frame)
        with self._store.mutate() as state:
            self._landscape(state)
            if state["scientific_core"].get("engine"):
                raise ControllerError("scientific core already started; use status or reopen-problem")
            state["scientific_core"] = {
                "engine": "research_cycle_v1", "status": "RESEARCH_ACTIVE", "current_phase": "NOT_STARTED",
                "frame": deepcopy(frame), "accepted_artifacts": {}, "artifact_history": [],
                "problem_versions": [], "active_problem_version": None, "route_versions": [],
                "active_route": None, "checks": {}, "feedback": [], "approvals": [],
                "approval_request": None, "review_request": None, "suspended_work": None,
                "transition_log": [], "return_history": [],
            }
            self._publish(state, "frame", frame)
            self._transition(state["scientific_core"], "PROBLEM_DISCOVERY", "current accepted map and application frame")
            return state

    def allowed_actions(self):
        state = self.status()
        if state["research_lit"]["current_stage"] != "LANDSCAPE_ACCEPTED":
            return self._research_lit_allowed_actions(state["research_lit"])
        stage = state["scientific_core"].get("current_phase") or "NOT_STARTED"
        return list(self.workflow["research_cycle"]["allowed_actions"][stage])

    def allowed_agents(self):
        state = self.status()
        if state["research_lit"]["current_stage"] != "LANDSCAPE_ACCEPTED":
            return super().allowed_agents()
        stage = state["scientific_core"].get("current_phase") or "NOT_STARTED"
        if stage in {"PROBLEM_REVIEW", "METHOD_REVIEW"}:
            return ["scientific_reviewer"]
        if stage in {"PROBLEM_SELECTION", "METHOD_READY", "METHOD_CONFIRMED"}:
            return []
        return ["main_research_agent"]

    def _request_review(self, state, kind):
        verify_formal_native_subagent_runtime(self.root, "scientific_reviewer")
        core = state["scientific_core"]
        verdicts = (["PROBLEMS_READY", "REVISE_PROBLEMS", "UPDATE_LITERATURE"] if kind == "PROBLEMS"
                    else ["METHOD_READY", "REVISE_METHOD", "UPDATE_LITERATURE", "RETURN_TO_PROBLEM"])
        core["review_request"] = {
            "id": uuid.uuid4().hex, "run_id": self.run_id, "kind": kind,
            "required_reviewer_role": "scientific_reviewer", "artifact_bindings": self._bindings(state),
            "accepted_verdicts": verdicts, "at": now(),
        }
        self._transition(core, "PROBLEM_REVIEW" if kind == "PROBLEMS" else "METHOD_REVIEW", "scientific packet submitted")

    def submit_problems(self, packet):
        with self._store.mutate() as state:
            core = self._core(state, "PROBLEM_DISCOVERY")
            v.validate_problems(packet, core["frame"], self._evidence(state), self._pending(core, "PROBLEM_DISCOVERY"))
            priors = [p for candidate in packet["candidates"] for p in candidate["prior_assessments"]]
            if v.strong_prior(priors):
                v.texts(packet.get("followup_gaps"), "covering prior followup_gaps")
            record = self._publish(state, "problems", packet)
            self._consume_feedback(core, packet.get("feedback_responses", []), record)
            if v.strong_prior(priors):
                self._return_for_prior(state, priors, packet["followup_gaps"], record)
            else:
                self._request_review(state, "PROBLEMS")
            return state

    def human_select_problem(self, candidate_id, request_id, *, accept_scope_change=False):
        with self._store.mutate() as state:
            core = self._core(state, "PROBLEM_SELECTION")
            request = core["approval_request"]
            if not request or request_id != request["id"]:
                raise ControllerError("human selection must identify the current approval request")
            self._assert_bindings(request["artifact_bindings"])
            candidate = next((c for c in self._read(core["accepted_artifacts"]["problems"])["candidates"] if c["id"] == candidate_id), None)
            if candidate is None:
                raise ControllerError("human selection must identify a reviewed candidate")
            previous = core.get("active_problem_version")
            original_question = (self._read(previous)["candidate"]["key_research_question"] if previous else core["frame"]["key_research_question"])
            changed = candidate["key_research_question"] != original_question
            if changed and not accept_scope_change:
                raise ControllerError("material question change requires explicit --accept-scope-change and a new human selection")
            record = self._publish(state, "problem", {"candidate": candidate, "frame": core["frame"],
                                  "human_request_id": request_id, "scope_change_accepted": changed,
                                  "scope_change_rationale": candidate["scope_change_rationale"]})
            version = {**record, "problem_id": candidate_id, "version": len(core["problem_versions"]) + 1,
                       "approved_by": "human", "approval_request_id": request_id}
            core["problem_versions"].append(deepcopy(version))
            core["active_problem_version"] = version
            core["active_route"] = None
            core["accepted_artifacts"].pop("method", None)
            core["approval_request"] = None
            core["approvals"].append({"gate": "problem_selection", "selected_id": candidate_id,
                                      "request_id": request_id, "confirmed_in": "explicit_human_command",
                                      "scope_change_accepted": changed, "problem": deepcopy(version), "at": now()})
            self._transition(core, "METHOD_DESIGN", "human selected a reviewed problem version")
            return state

    def _selected(self, core):
        selected = core.get("active_problem_version")
        if not selected:
            raise ControllerError("method work requires a human-selected problem")
        self._read(selected)
        return selected

    def submit_method(self, packet):
        with self._store.mutate() as state:
            core = self._core(state, "METHOD_DESIGN")
            selected = self._selected(core)
            v.validate_method(packet, selected, self._evidence(state), self._pending(core, "METHOD_DESIGN"),
                              core["checks"], state["research_lit"].get("query_events", {}))
            for claim in packet["claims"]:
                if claim["evidence_status"] == "VALIDATED":
                    for check_id in claim["check_ids"]:
                        check = core["checks"][check_id]
                        self._read(check)
                        self._assert_bindings({a["path"]: a["sha256"] for a in check["result"]["artifacts"]})
            for derivation in packet["mechanism"]["derivations"]:
                if derivation["status"] == "CHECKED":
                    for check_id in derivation["check_ids"]:
                        check = core["checks"][check_id]
                        self._read(check)
                        self._assert_bindings({a["path"]: a["sha256"] for a in check["result"]["artifacts"]})
            priors = packet["prior_assessments"] + packet["mature_method_search"]["sources"]
            if v.strong_prior(priors):
                v.texts(packet.get("followup_gaps"), "covering prior followup_gaps")
            record = self._publish(state, "method", packet)
            version = {**record, "route_id": packet["route_id"], "version": len(core["route_versions"]) + 1,
                       "problem_binding": packet["problem_binding"], "mechanism_sha256": v.mechanism_digest(packet["mechanism"])}
            core["route_versions"].append(deepcopy(version))
            core["active_route"] = version
            self._consume_feedback(core, packet.get("feedback_responses", []), record)
            if v.strong_prior(priors):
                self._return_for_prior(state, priors, packet["followup_gaps"], record)
            else:
                self._request_review(state, "METHOD")
            return state

    def submit_prior_assessment(self, packet):
        with self._store.mutate() as state:
            core = self._core(state, "PROBLEM_DISCOVERY", "METHOD_DESIGN", "METHOD_REVIEW", "METHOD_READY")
            priors = v.validate_priors(packet.get("prior_assessments"), self._evidence(state), empty=False)
            if core["active_problem_version"]:
                v.validate_binding(packet.get("problem_binding"), self._selected(core))
            if v.strong_prior(priors):
                v.texts(packet.get("followup_gaps"), "covering prior followup_gaps")
            record = self._publish(state, "prior-assessment", packet)
            if v.strong_prior(priors):
                self._return_for_prior(state, priors, packet["followup_gaps"], record)
            else:
                self._feedback(core, "METHOD_DESIGN" if core["active_problem_version"] else "PROBLEM_DISCOVERY",
                               "Prior identity and actual coverage assessed separately", "Consume the prior assessment; reuse mature cross-field mechanisms when matched",
                               source=record, evidence_ids=[i for p in priors for i in p["evidence_ids"]])
                core["review_request"] = None
                core["approval_request"] = None
                self._transition(core, "METHOD_DESIGN" if core["active_problem_version"] else "PROBLEM_DISCOVERY", "prior assessment updates scientific judgment")
            return state

    def _return_for_prior(self, state, priors, gaps, source):
        core = state["scientific_core"]
        self._feedback(core, "PROBLEM_DISCOVERY", "In-field prior substantially covers the problem or contribution",
                       "Reconstruct its strongest argument, assumptions, failure boundaries and remaining important pain; retain the core application and avoid shrinking increment to evade prior",
                       source=source, evidence_ids=list(dict.fromkeys(i for p in priors for i in p["evidence_ids"])))
        core["return_history"].append({"reason": "COVERING_IN_FIELD_PRIOR", "source": source,
                                        "problem": core.get("active_problem_version"), "route": core.get("active_route"), "at": now()})
        core["return_after_update"] = "PROBLEM_DISCOVERY"
        self._apply_literature_update(state, gaps, "problem_discovery", {"close_conditions": gaps})

    def _on_literature_update(self, state, gaps, requested_by, context):
        core = state["scientific_core"]
        if core.get("engine") != "research_cycle_v1":
            return context
        if core["current_phase"] in {"LITERATURE_UPDATE", "METHOD_CONFIRMED"}:
            raise ControllerError("reopen scientific work before requesting a new update")
        selected = core.get("active_problem_version")
        route = core.get("active_route")
        binding = {"core_application": core["frame"]["core_application"],
                   "selected_problem": selected["problem_id"] if selected else None,
                   "problem_version": selected["version"] if selected else None,
                   "route_id": route["route_id"] if route else None,
                   "route_version": route["version"] if route else None}
        for key in binding:
            if context and key in context and context[key] != binding[key]:
                raise ControllerError("literature update context does not match the current scientific object")
        context = {**deepcopy(context or {}), **binding}
        closures = context.get("close_conditions")
        if closures is None:
            context["close_conditions"] = list(gaps)
        elif len(v.texts(closures, "close_conditions")) != len(gaps):
            raise ControllerError("each requested gap requires a close condition")
        return_stage = core.pop("return_after_update", None) or (
            "PROBLEM_DISCOVERY" if core["current_phase"].startswith("PROBLEM") else "METHOD_DESIGN")
        core["suspended_work"] = {"from": core["current_phase"], "return_to": return_stage,
                                    "problem_binding": deepcopy(selected), "route_binding": deepcopy(route),
                                    "map_before": state["research_lit"]["accepted_artifacts"]["active_field_map"]["sha256"],
                                    "gaps": list(gaps), "context": context}
        core["review_request"] = None
        core["approval_request"] = None
        self._transition(core, "LITERATURE_UPDATE", "concrete scientific gaps temporarily reopen the shared map")
        return context

    def _on_landscape_accepted(self, state):
        core = state["scientific_core"]
        suspended = core.get("suspended_work")
        if not suspended:
            return
        if core.get("active_problem_version") != suspended["problem_binding"] or core.get("active_route") != suspended["route_binding"]:
            raise ControllerError("scientific object changed while literature work was suspended")
        updated = state["research_lit"]["accepted_artifacts"]["active_field_map"]
        self._feedback(core, suspended["return_to"], "Supplementary literature accepted; continue the suspended scientific work",
                       "Assess how new evidence closes or reframes each gap and changes the problem or route",
                       source={"map_before": suspended["map_before"], "map_after": updated,
                               "gaps": suspended["gaps"], "context": suspended["context"]})
        self._transition(core, suspended["return_to"], "coverage accepted; returned to original scientific work")
        core["suspended_work"] = None

    def reopen_problem(self, rationale, evidence_ids):
        with self._store.mutate() as state:
            core = self._core(state, "METHOD_DESIGN", "METHOD_REVIEW", "METHOD_READY", "METHOD_CONFIRMED", "PROBLEM_SELECTION")
            v.text(rationale, "reopen rationale")
            v.evidence(evidence_ids, self._evidence(state), "reopen evidence")
            self._feedback(core, "PROBLEM_DISCOVERY", rationale, "Revise candidate framing with evidence; retain core application and submit material changes for a new human choice", evidence_ids=evidence_ids)
            core["review_request"] = None
            core["approval_request"] = None
            self._transition(core, "PROBLEM_DISCOVERY", "scientific evidence requires reconsidering the problem")
            return state

    def submit_check(self, result):
        with self._store.mutate() as state:
            core = self._core(state, "METHOD_DESIGN", "METHOD_REVIEW", "METHOD_READY")
            route = core.get("active_route")
            if not route:
                raise ControllerError("checks require a concrete submitted route")
            packet = self._read(route)
            expected = {key: route[key] for key in ("route_id", "version", "sha256")}
            if result.get("route_binding") != expected:
                raise ControllerError("check is not bound to the current concrete route")
            v.fields(result, ("check_id", "finding", "design_consequence", "independence_rationale", "execution_authorization"), "check result")
            if result["check_id"] in core["checks"]:
                raise ControllerError("check IDs are immutable and cannot be replayed")
            plan = next((p for p in packet["checks"] if p["check_id"] == result["check_id"]), None)
            if not plan or result.get("kind") != plan["kind"] or result.get("claim_ids") != plan["claim_ids"]:
                raise ControllerError("check result must match the submitted check plan")
            if result.get("plan_sha256") != v.digest(plan):
                raise ControllerError("check result must bind the exact check conditions and comparisons")
            if result.get("derivation_ids", []) != plan.get("derivation_ids", []):
                raise ControllerError("theory result must identify the derivations evaluated by its plan")
            v.choice(result.get("outcome"), {"PASS", "FAIL", "INCONCLUSIVE"}, "outcome")
            v.choice(result.get("action"), {"REVISE_METHOD", "RETURN_TO_PROBLEM", "UPDATE_LITERATURE"}, "check.action")
            units = v.texts(result.get("evaluation_units"), "evaluation_units")
            artifacts = v.rows(result.get("artifacts"), "check.artifacts")
            bindings = {}
            for artifact in artifacts:
                v.fields(artifact, ("path", "sha256", "origin"), "check artifact")
                bindings[artifact["path"]] = artifact["sha256"]
            self._assert_bindings(bindings)
            for previous in core["checks"].values():
                opposite = {previous["result"]["kind"], result["kind"]} == {"DESIGN_SELECTION", "INDEPENDENT_VALIDATION"}
                if opposite and (set(units) & set(previous["result"]["evaluation_units"]) or
                                 set(bindings.values()) & {a["sha256"] for a in previous["result"]["artifacts"]}):
                    raise ControllerError("independent contribution validation must not reuse design-selection units or result artifacts")
            if result["action"] in {"RETURN_TO_PROBLEM", "UPDATE_LITERATURE"}:
                v.texts(result.get("gaps"), "check.gaps")
            record = self._publish(state, "check", result)
            core["checks"][result["check_id"]] = {
                **record, "result": deepcopy(result), "problem_binding": route["problem_binding"],
                "mechanism_sha256": route["mechanism_sha256"],
                "claim_bindings": {c["id"]: v.digest({"statement": c["statement"], "kind": c["kind"]}) for c in packet["claims"]},
            }
            core["review_request"] = None
            core["approval_request"] = None
            target = "PROBLEM_DISCOVERY" if result["action"] == "RETURN_TO_PROBLEM" else "METHOD_DESIGN"
            self._feedback(core, target, result["finding"], result["design_consequence"], source=record)
            if result["action"] in {"RETURN_TO_PROBLEM", "UPDATE_LITERATURE"}:
                core["return_after_update"] = target
                self._apply_literature_update(state, result["gaps"], "method_design", {"close_conditions": result["gaps"]})
            else:
                self._transition(core, "METHOD_DESIGN", "theory/experiment finding must influence the next route packet")
            return state

    def submit_review(self, payload):
        with self._store.mutate() as state:
            core = self._core(state, "PROBLEM_REVIEW", "METHOD_REVIEW")
            request = core["review_request"]
            if not request:
                raise ControllerError("no live scientific review request")
            self._assert_bindings(request["artifact_bindings"])
            v.validate_review(payload, request, self._evidence(state))
            attested = self._attested_reviewer_payload(role="scientific_reviewer", request_id=request["id"],
                reviewer=payload["reviewer"], verdict_id=payload["verdict_id"], decision=payload["decision"], artifact_bindings=request["artifact_bindings"])
            if payload != attested:
                raise ControllerError("review must be the exact independently attested reviewer payload")
            self._consume_review_attestation(role="scientific_reviewer", request_id=request["id"], reviewer=payload["reviewer"],
                verdict_id=payload["verdict_id"], decision=payload["decision"], artifact_bindings=request["artifact_bindings"])
            record = self._publish(state, "review", payload)
            core["review_request"] = None
            for issue in payload["issues"]:
                self._feedback(core, issue["target"], issue["rationale"], issue["requested_change"],
                               evidence_ids=issue["evidence_ids"], source=record)
            decision = payload["decision"]
            if v.strong_prior(payload["prior_assessments"]):
                self._return_for_prior(state, payload["prior_assessments"], payload["gaps"], record)
            elif decision in {"UPDATE_LITERATURE", "RETURN_TO_PROBLEM"}:
                core["return_after_update"] = "PROBLEM_DISCOVERY" if decision == "RETURN_TO_PROBLEM" or request["kind"] == "PROBLEMS" else "METHOD_DESIGN"
                self._apply_literature_update(state, payload["gaps"], "problem_discovery" if request["kind"] == "PROBLEMS" else "method_design", {"close_conditions": payload["gaps"]})
            elif decision in {"PROBLEMS_READY", "METHOD_READY"}:
                stage = "PROBLEM_SELECTION" if decision == "PROBLEMS_READY" else "METHOD_READY"
                self._transition(core, stage, "independent scientific review ready")
                core["approval_request"] = {"id": uuid.uuid4().hex, "kind": stage,
                                             "artifact_bindings": self._bindings(state), "at": now()}
            else:
                self._transition(core, "PROBLEM_DISCOVERY" if request["kind"] == "PROBLEMS" else "METHOD_DESIGN", "independent feedback requires revision")
            return state

    def human_confirm_method(self, request_id):
        with self._store.mutate() as state:
            core = self._core(state, "METHOD_READY")
            request = core["approval_request"]
            if not request or request["id"] != request_id:
                raise ControllerError("human method confirmation must identify the current approval request")
            self._assert_bindings(request["artifact_bindings"])
            core["approvals"].append({"gate": "method_confirmation", "request_id": request_id,
                                      "route": deepcopy(core["active_route"]), "confirmed_in": "explicit_human_command", "at": now()})
            core["approval_request"] = None
            self._transition(core, "METHOD_CONFIRMED", "human confirmed the bounded method; no experiment is auto-started")
            return state

    def handoff(self):
        state = self.status()
        core = state["scientific_core"]
        if core.get("engine") != "research_cycle_v1":
            raise ControllerError("scientific handoff requires a started core")
        updating = core["current_phase"] == "LITERATURE_UPDATE"
        if updating:
            bindings = {r["path"]: r["sha256"] for r in core["accepted_artifacts"].values()}
        else:
            self._core(state)
            bindings = self._bindings(state)
        self._assert_bindings(bindings)
        return {"run_id": self.run_id, "workflow_sha256": self.workflow_sha256,
                "stage": core["current_phase"], "frame": core["frame"],
                "problem": core["active_problem_version"], "route": core["active_route"],
                "artifacts": bindings, "feedback": core["feedback"],
                "literature_stage": state["research_lit"]["current_stage"],
                "landscape_currently_accepted": not updating, "suspended_work": core["suspended_work"],
                "review_request": core["review_request"], "approval_request": core["approval_request"],
                "claims": self._read(core["active_route"])["claims"] if core["active_route"] else [],
                "checks": core["checks"], "actions": self.allowed_actions(),
                "validation_boundary": "Declared plans are not performed validation; real results and science quality require case acceptance."}

    def review_handoff(self, *, dispatch_mode="configured_role"):
        state = self.status()
        core = self._core(state, "PROBLEM_REVIEW", "METHOD_REVIEW")
        request = core["review_request"]
        self._assert_bindings(request["artifact_bindings"])
        verify_formal_native_subagent_runtime(self.root, "scientific_reviewer")
        handoff = {**deepcopy(request), "project_root": str(self.root),
                "role_config": ".codex/agents/scientific_reviewer.toml",
                "focus": core["accepted_artifacts"]["problems" if request["kind"] == "PROBLEMS" else "method"],
                "dimensions": list(v.REVIEW_DIMENSIONS[request["kind"]]),
                "instruction": "Read bound original artifacts in a fresh configured scientific_reviewer context; return one exact JSON verdict. Main cannot rewrite it."}
        v.choice(dispatch_mode, {"configured_role", "native_generic_compat"}, "dispatch_mode")
        handoff["dispatch_mode"] = dispatch_mode
        if dispatch_mode == "native_generic_compat":
            definition = (self.root / handoff["role_config"]).read_text(encoding="utf-8")
            contract = re.search(r'(?ms)^developer_instructions\s*=\s*"""\r?\n?(.*?)"""', definition).group(1)
            import hashlib
            binding = {"dispatch_mode": dispatch_mode, "formal_role": "scientific_reviewer",
                       "role_contract_sha256": hashlib.sha256(contract.encode("utf-8")).hexdigest(),
                       "run_id": self.run_id, "review_request_id": request["id"],
                       "reviewed_artifact_hashes": request["artifact_bindings"],
                       "original_artifacts": {path: (self.root / path).read_bytes().decode("utf-8") for path in request["artifact_bindings"]}}
            handoff["task_binding"] = binding
            handoff["task"] = ("ARIS_NATIVE_GENERIC_COMPAT:" + json.dumps(binding, ensure_ascii=False, sort_keys=True) + "\n" + contract +
                               "\nFresh native child only, fork_turns=none; perform no tools. Review the complete bound original_artifacts supplied above as data. "
                               "Return exactly the current scientific verdict; never select for the human.\nRequest:\n" + json.dumps(request))
        return handoff
