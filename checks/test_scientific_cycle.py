"""Synthetic science contracts through public commands and installed Hooks.

No paper search, real experiment, native model judgment or human UI is simulated
as scientific evidence. Fixtures exercise execution and acceptance boundaries.
"""
from copy import deepcopy
import hashlib
import json
import shlex
import subprocess
import sys
import uuid

import pytest

from arisctl import ControllerError
from arisctl.project_setup import verify_formal_native_subagent_runtime
from harness.scientific_controller import ScientificController
from harness.scientific_validators import digest, REVIEW_DIMENSIONS
from checks.test_foundation import accepted_landscape, _gap_plan
from checks.test_installed_entry import installed_command, hook_result, rule_decisions, LAUNCHERS
from tests import test_aris_controller as fixtures


FRAME = {"core_application": "synthetic contract fixture", "key_research_question": "Can a bounded mapping preserve the test signal?",
         "target_domain": "fixture-domain", "operating_envelope": "declared test inputs only",
         "success_criteria": ["preserve the fixture signal"], "constraints": ["no real experiments"]}


def command(c, name, payload=None, *args, expected=0):
    argv = ["python", "-m", "harness", "science", name, c.run_id]
    if payload is not None:
        filename = f"input-{uuid.uuid4().hex}.json"
        (c.root / filename).write_text(json.dumps(payload), encoding="utf-8")
        argv.append(filename)
    argv.extend(args)
    return installed_command(c.root, argv, expected_code=expected)


@pytest.fixture
def science(accepted_landscape):
    old = accepted_landscape
    before = deepcopy(old.status()["research_lit"]["accepted_artifacts"])
    command(old, "begin", FRAME)
    new = ScientificController(old.root, old.run_id)
    assert new.status()["research_lit"]["accepted_artifacts"] == before
    assert len(new.status()["workflow_adoptions"]) == 1
    return new


def core(c):
    return c.status()["scientific_core"]


def responses(c, target):
    return [{"feedback_id": f["id"], "response": "Evidence changes the reasoning in this synthetic revision",
             "changed_elements": "question framing or mechanism boundary", "evidence_ids": ["P1"]}
            for f in core(c)["feedback"] if f["target"] == target and not f["consumed_by"]]


def prior(identity="IN_FIELD", coverage="PARTIAL"):
    return {"evidence_ids": ["P1"], "source_domain": "fixture source", "domain_identity": identity,
            "domain_rationale": "identity assessed independently of coverage", "coverage": coverage,
            "covers": "CONTRIBUTION", "coverage_rationale": "fixture coverage assessment",
            "strongest_argument": "source solves its declared task", "assumptions": "bounded inputs",
            "failure_boundaries": "unsupported input regime", "remaining_pain": "important unresolved signal boundary"}


def problems(c, path="COMMUNITY_RECOGNIZED"):
    return {"candidates": [{"id": "candidate-1", "core_application": FRAME["core_application"],
        "key_research_question": FRAME["key_research_question"], "pain_point": "fixture loses signal in a declared regime",
        "significance": "tests useful scientific contract", "current_solution_extent": "source supports only part of the envelope",
        "scope_change_rationale": "retains the application and key question", "discovery_path": path,
        "failure_origin": "INFERENCE", "evidence_ids": ["P1"] if path == "COMMUNITY_RECOGNIZED" else ["P1", "P2"],
        "interrogation": {"strongest_argument": "existing source works under its own premise", "premises": ["input bounded"],
            "counterexamples": ["signal absent outside envelope"], "alternative_explanations": ["measurement error"],
            "literature_conflicts": [], "first_principles": "information absent from inputs cannot be recovered"},
        "prior_assessments": [prior()], "unverified_claims": ["common cause remains inferred"]}],
        "feedback_responses": responses(c, "PROBLEM_DISCOVERY")}


def attest(c, payload):
    # Execute the hook installed in the actual research directory, not its source.
    result = subprocess.run([sys.executable, str(c.root / ".codex/hooks/subagent_attestation.py")], cwd=c.root,
        input=json.dumps({"hook_event_name": "SubagentStop", "cwd": str(c.root), "turn_id": "fixture-turn",
            "agent_id": "fixture-independent", "agent_type": "scientific_reviewer",
            "last_assistant_message": json.dumps(payload)}), text=True, capture_output=True)
    assert result.returncode == 0 and result.stdout == "", result.stderr


def review(c, decision=None, issues=None, priors=None, gaps=None):
    request = command(c, "review-handoff")
    decision = decision or ("PROBLEMS_READY" if request["kind"] == "PROBLEMS" else "METHOD_READY")
    return {"run_id": c.run_id, "review_request_id": request["id"], "reviewer": "fixture-independent-model",
            "verdict_id": uuid.uuid4().hex, "rationale": "synthetic reviewer protocol check",
            "reviewed_artifact_hashes": request["artifact_bindings"], "decision": decision,
            "assessments": {d: {"status": "PASS" if decision.endswith("READY") else "GAP", "rationale": "fixture rationale"}
                            for d in REVIEW_DIMENSIONS[request["kind"]]},
            "issues": issues or [], "prior_assessments": priors or [], "gaps": gaps or []}


def accept_review(c):
    payload = review(c)
    attest(c, payload)
    command(c, "submit-review", payload)


def select(c):
    command(c, "submit-problems", problems(c))
    accept_review(c)
    request = core(c)["approval_request"]["id"]
    command(c, "human-select-problem", None, "candidate-1", "--request-id", request)


def method(c):
    selected = core(c)["active_problem_version"]
    return {"problem_binding": {k: selected[k] for k in ("problem_id", "version", "sha256")},
        "route_id": "route-1", "change_reason": "initial concrete route", "scientific_delta": "preserve a target-task signal",
        "expected_benefit": "testable reduction in fixture signal loss", "design_mode": "DIRECT_REUSE",
        "mechanism": {"model": "y = x", "applicability": "bounded fixture inputs", "variables": [{"name": "x", "meaning": "test signal", "units": "dimensionless"}],
            "inputs": ["x"], "outputs": ["y"], "algorithm": [{"id": "step-1", "operation": "copy x to y", "inputs": ["x"], "outputs": ["y"]}],
            "derivations": [{"id": "derivation-1", "expression": "y - x = 0", "rationale": "identity model", "assumptions": ["exact copy"], "status": "INFERENCE"}],
            "components": [{"id": "copy", "purpose": "preserve signal", "input": "x", "output": "y", "why_needed": "output must retain signal",
                            "isolation_test": "remove copying and compare signal", "assumptions": ["copy exact"]}], "assumptions": ["input available"]},
        "mature_method_search": {"queries": [{"query_id": next(iter(c.status()["research_lit"]["query_events"])),
            "terms": next(iter(c.status()["research_lit"]["query_events"].values()))["query"], "domain": "fixture source domain", "outcome": "P1 mechanism investigated"}],
            "sources": [{"evidence_ids": ["P1"], "domain_identity": "CROSS_FIELD", "domain_rationale": "resource outside target task",
                "mechanism": "identity mapping", "input_output_match": "signal-to-signal interface", "assumption_match": "bounded exact copy",
                "reuse_mode": "DIRECT_REUSE", "changes": "none required", "attribution": "fixture P1", "coverage": "SUBSTANTIAL",
                "coverage_rationale": "resource solves its source task; target contribution separately tested"}]},
        "prior_assessments": [prior()], "claims": [{"id": "claim-1", "statement": "target-task signal is preserved",
            "kind": "EMPIRICAL", "evidence_status": "HYPOTHESIS", "evidence_ids": [], "check_ids": [], "limitations": "unverified test fixture"}],
        "checks": [{"check_id": name, "kind": kind, "claim_ids": ["claim-1"], "comparison": "identity versus signal removal",
                    "controls": "same resource budget", "metric": "signal loss", "setting": "fixture units",
                    "expected_observation": "less loss", "falsifying_result": "no reduction", "execution_authorization": "synthetic tests only",
                    "derivation_ids": ["derivation-1"] if kind == "THEORY" else []}
                   for name, kind in (("selection", "DESIGN_SELECTION"), ("independent", "INDEPENDENT_VALIDATION"), ("theory", "THEORY"))],
        "alternatives": ["signal removal baseline"], "feedback_responses": responses(c, "METHOD_DESIGN")}


def update_finish(c, cycle=1):
    gap = c.status()["research_lit"]["literature_update_requests"][-1]["gaps"][0]
    query = f"synthetic gap cycle {cycle}"
    c.submit_query_plan(_gap_plan(gap, query))
    c.execute_query(query, "fixture-search", lambda _: [fixtures.metadata("P2")], plan_item_id="gap-p2",
                    query_options={"year_from": 2000, "year_to": 2026, "exact_title": False, "page": 1})
    c.decide_admission("P2", screening_in_scope=True, screening_basis="TITLE_ABSTRACT", screening_reason="test gap source", reading_priority="TARGETED_GAP_FOLLOWUP")
    c.decide_admission("P1", screening_in_scope=True, screening_basis="FULL_TEXT", screening_reason="retain accepted source", reading_priority="HIGH_CITATION_BACKBONE",
                       fulltext_selected=False, fulltext_selection_reason="accepted Evidence already exists")
    c.select_reading_subset(["P2"], rationale="gap-only reading")
    c.finish_retrieval()
    if "evidence:P2" not in c.status()["research_lit"]["accepted_artifacts"]:
        read = c.read_full_text("P2", "fixture-reader", lambda _: "synthetic P2 full paper")
        c.submit_evidence_card("P2", fixtures.card(read, "P2"))
    c.finish_reading()
    field_map = fixtures.field_map()
    field_map["family_development_traces"][0]["evidence_ids"] = ["P1", "P2"]
    field_map["assumption_effectiveness_failure_matrix"][0]["source_ids"] = ["P1", "P2"]
    field_map["consensus"] = [f"gap test cycle {cycle}"]
    c.submit_field_map(field_map)
    request = c.status()["research_lit"]["coverage_review_request"]
    payload = fixtures.coverage_review(request["artifact_sha256"], request["id"], bindings=request["artifact_bindings"])
    fixtures.attest(c, "coverage_reviewer", payload)
    # The completion and callback use the public lit entry on the same new profile.
    filename = c.root / "coverage.json"
    filename.write_text(json.dumps(payload), encoding="utf-8")
    installed_command(c.root, ["python", "-m", "harness", "lit", "submit-coverage-review", c.run_id, str(filename)])


def result(c, check_id="independent", action="REVISE_METHOD", units=None, content=None):
    route = core(c)["active_route"]
    packet = c._read(route)
    plan = next(p for p in packet["checks"] if p["check_id"] == check_id)
    path = c.root / f"result-{check_id}.txt"
    path.write_text(content or f"synthetic result {check_id}", encoding="utf-8")
    return {"route_binding": {k: route[k] for k in ("route_id", "version", "sha256")}, "plan_sha256": digest(plan),
            "check_id": check_id, "kind": plan["kind"], "claim_ids": plan["claim_ids"], "derivation_ids": plan["derivation_ids"], "outcome": "PASS",
            "finding": "synthetic observation", "design_consequence": "retain mechanism, update evidence boundary",
            "independence_rationale": "disjoint fixture units", "execution_authorization": "unit tests only",
            "evaluation_units": units or [check_id], "artifacts": [{"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "origin": "synthetic fixture"}],
            "action": action, "gaps": ["fixture needs stronger premise"]}


def test_complete_public_loop_without_principle_chain_and_installed_skills(science):
    c = science
    verify_formal_native_subagent_runtime(c.root, "scientific_reviewer")
    for name in ("research-cycle", "research-lit"):
        assert (c.root / ".agents/skills" / name / "SKILL.md").is_file()
    select(c)
    command(c, "submit-method", method(c))
    assert core(c)["current_phase"] == "METHOD_REVIEW"
    accept_review(c)
    installed_command(c.root, ["academic-harness", "science", "human-confirm-method", c.run_id,
                              "--request-id", core(c)["approval_request"]["id"]])
    handoff = command(c, "handoff")
    assert handoff["stage"] == "METHOD_CONFIRMED" and handoff["claims"][0]["evidence_status"] == "HYPOTHESIS"
    assert not handoff["checks"]
    assert not c.status()["workflow"].get("scientific_core")


@pytest.mark.parametrize("launcher", LAUNCHERS)
@pytest.mark.parametrize("name", ["human-select-problem", "human-confirm-method"])
def test_installed_science_human_aliases(science, launcher, name):
    argv = [*launcher, "science", name, science.run_id, "--request-id", "fixture"]
    assert hook_result(science.root, shlex.join(argv)) == ""
    assert rule_decisions(science.root, argv) == ["prompt"]
    wrapped = [*launcher, "--root", ".", *argv[len(launcher):]]
    assert "deny" in hook_result(science.root, shlex.join(wrapped))


def test_human_selection_and_material_scope_change_required(science):
    c = science
    command(c, "submit-method", {}, expected=1)
    payload = problems(c)
    payload["candidates"][0]["key_research_question"] = "materially revised test question"
    command(c, "submit-problems", payload)
    accept_review(c)
    request = core(c)["approval_request"]["id"]
    command(c, "human-select-problem", None, "candidate-1", "--request-id", request, expected=1)
    command(c, "human-select-problem", None, "candidate-1", "--request-id", request, "--accept-scope-change")
    assert core(c)["active_problem_version"]["version"] == 1
    assert core(c)["approvals"][-1]["scope_change_accepted"]


def test_common_failure_multi_paper_and_continuous_problem_updates(science):
    c = science
    command(c, "submit-problems", problems(c, "COMMON_FAILURE"), expected=1)
    old = c.status()["research_lit"]["accepted_artifacts"]["evidence:P1"]
    for cycle in (1, 2):
        command(c, "request-literature-update", {"gaps": ["fixture premise missing"], "requested_by": "problem_discovery"})
        command(c, "submit-problems", problems(c), expected=1)
        update_finish(c, cycle)
        assert core(c)["current_phase"] == "PROBLEM_DISCOVERY"
    command(c, "submit-problems", problems(c, "COMMON_FAILURE"))
    assert c.status()["research_lit"]["accepted_artifacts"]["evidence:P1"] == old
    assert all(f["consumed_by"] for f in core(c)["feedback"])


def test_method_supplement_returns_same_object_and_consumes_feedback(science):
    c = science
    select(c)
    command(c, "submit-method", method(c))
    original = deepcopy(core(c)["active_route"])
    command(c, "request-literature-update", {"gaps": ["fixture mechanism missing"], "requested_by": "method_design"})
    suspended = command(c, "handoff")
    assert suspended["route"] == original and not suspended["landscape_currently_accepted"]
    update_finish(c)
    assert core(c)["current_phase"] == "METHOD_DESIGN" and core(c)["active_route"] == original
    packet = method(c)
    packet["feedback_responses"] = []
    command(c, "submit-method", packet, expected=1)
    command(c, "submit-method", method(c))
    assert core(c)["active_route"]["version"] == 2


@pytest.mark.parametrize("channel", ["method", "prior", "review"])
def test_covering_in_field_prior_updates_then_returns_problem(science, channel):
    c = science
    select(c)
    packet = method(c)
    if channel == "method":
        packet["prior_assessments"] = [prior("IN_FIELD", "SUBSTANTIAL")]
        packet["followup_gaps"] = ["important pain beyond prior"]
        command(c, "submit-method", packet)
    elif channel == "prior":
        command(c, "submit-prior-assessment", {"problem_binding": packet["problem_binding"], "prior_assessments": [prior("IN_FIELD", "SUBSTANTIAL")], "followup_gaps": ["important pain beyond prior"]})
    else:
        command(c, "submit-method", packet)
        payload = review(c, "RETURN_TO_PROBLEM", [{"id": "prior", "target": "PROBLEM_DISCOVERY", "rationale": "covered", "requested_change": "find important pain", "evidence_ids": ["P1"]}],
                         [prior("IN_FIELD", "SUBSTANTIAL")], ["important pain beyond prior"])
        attest(c, payload)
        command(c, "submit-review", payload)
    assert core(c)["current_phase"] == "LITERATURE_UPDATE"
    update_finish(c)
    assert core(c)["current_phase"] == "PROBLEM_DISCOVERY"
    select(c)
    assert len(core(c)["problem_versions"]) == 2 and core(c)["active_route"] is None
    assert core(c)["frame"]["core_application"] == FRAME["core_application"]


def test_independent_feedback_cannot_be_rewritten_and_must_change_route(science):
    c = science
    select(c)
    command(c, "submit-method", method(c))
    payload = review(c, "REVISE_METHOD", [{"id": "component", "target": "METHOD_DESIGN", "rationale": "isolation unresolved", "requested_change": "explain isolation", "evidence_ids": ["P1"]}])
    attest(c, payload)
    changed = deepcopy(payload)
    changed["rationale"] = "main rewrites verdict"
    command(c, "submit-review", changed, expected=1)
    command(c, "submit-review", payload)
    packet = method(c)
    packet["feedback_responses"] = []
    command(c, "submit-method", packet, expected=1)
    packet["feedback_responses"] = responses(c, "METHOD_DESIGN")
    packet["mechanism"]["components"][0]["isolation_test"] = "matched-budget independent component removal"
    command(c, "submit-method", packet)
    assert len(core(c)["route_versions"]) == 2


@pytest.mark.parametrize("mutation", ["claim", "mechanism", "artifact", "design_trial"])
def test_validated_claim_requires_exact_current_independent_results(science, mutation):
    c = science
    select(c)
    command(c, "submit-method", method(c))
    check = result(c, "selection" if mutation == "design_trial" else "independent")
    command(c, "submit-check", check)
    packet = method(c)
    packet["claims"][0].update(evidence_status="VALIDATED", check_ids=[check["check_id"]])
    if mutation == "claim":
        packet["claims"][0]["statement"] = "different unsupported claim"
    elif mutation == "mechanism":
        packet["mechanism"]["model"] = "y = 2x"
    elif mutation == "artifact":
        (c.root / check["artifacts"][0]["path"]).write_text("tampered", encoding="utf-8")
    command(c, "submit-method", packet, expected=1)


def test_actual_result_enables_bounded_claim_and_independence_separation(science):
    c = science
    select(c)
    command(c, "submit-method", method(c))
    command(c, "submit-check", result(c, "selection", units=["design-unit"]))
    command(c, "submit-method", method(c))
    command(c, "submit-check", result(c, units=["design-unit"]), expected=1)
    command(c, "submit-check", result(c))
    packet = method(c)
    packet["claims"][0].update(evidence_status="VALIDATED", check_ids=["independent"])
    command(c, "submit-method", packet)
    assert c._read(core(c)["active_route"])["claims"][0]["evidence_status"] == "VALIDATED"


def test_check_plan_exact_binding_and_negative_result_return(science):
    c = science
    select(c)
    command(c, "submit-method", method(c))
    payload = result(c, action="RETURN_TO_PROBLEM")
    payload["plan_sha256"] = "0" * 64
    command(c, "submit-check", payload, expected=1)
    payload = result(c, action="RETURN_TO_PROBLEM")
    payload["outcome"] = "FAIL"
    command(c, "submit-check", payload)
    update_finish(c)
    assert core(c)["current_phase"] == "PROBLEM_DISCOVERY"


def test_recovery_preserves_scientific_stage_versions_and_entry(science, tmp_path):
    c = science
    select(c)
    command(c, "submit-method", method(c))
    destination = tmp_path.parent / (tmp_path.name + "-science-recovery")
    installed_command(c.root, ["python", "-m", "harness", "lit", "save-recovery", c.run_id, str(destination)])
    recovery = json.loads((destination / "ARIS_RECOVERY.json").read_text(encoding="utf-8"))
    assert "science" in recovery["resume"]["science_status_command"]
    installed_command(destination, ["python", "-m", "harness", "lit", "resume", c.run_id])
    restored = ScientificController(destination, c.run_id)
    assert command(restored, "handoff")["route"] == core(c)["active_route"]


def test_problem_packet_covering_prior_cannot_reach_selection(science):
    c = science
    packet = problems(c)
    packet["candidates"][0]["prior_assessments"] = [prior("IN_FIELD", "SUBSTANTIAL")]
    command(c, "submit-problems", packet, expected=1)
    packet["followup_gaps"] = ["strong source still has important boundary pain"]
    command(c, "submit-problems", packet)
    assert core(c)["current_phase"] == "LITERATURE_UPDATE" and core(c)["approval_request"] is None


def test_theory_check_supports_exact_derivation_and_conditions(science):
    c = science
    select(c)
    command(c, "submit-method", method(c))
    command(c, "submit-check", result(c, "theory"))
    packet = method(c)
    packet["mechanism"]["derivations"][0].update(status="CHECKED", check_ids=["theory"])
    changed = deepcopy(packet)
    changed["checks"][2]["controls"] = "different proof assumptions"
    command(c, "submit-method", changed, expected=1)
    command(c, "submit-method", packet)
    assert core(c)["current_phase"] == "METHOD_REVIEW"


def test_new_profile_starts_through_public_entry_and_preserves_custom_instructions(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    custom = "# Custom instructions\nPreserve this content.\n"
    (tmp_path / "AGENTS.md").write_text(custom, encoding="utf-8")
    from harness.__main__ import main
    assert main(["science", "start", "fresh-run", "--executor", "fixture-model"]) == 0
    c = ScientificController(tmp_path, "fresh-run")
    assert c.status()["workflow"]["mode"] == "research_cycle"
    assert c.allowed_actions() == ["submit_source_admission_policy"]
    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == custom


def test_stale_installed_skill_prevents_review_and_rolls_back_packet(science):
    c = science
    installed = c.root / ".agents/skills/research-cycle/SKILL.md"
    installed.write_text("changed locally", encoding="utf-8")
    before = core(c)
    command(c, "submit-problems", problems(c), expected=1)
    assert core(c) == before


def test_fake_mature_search_terms_do_not_satisfy_executed_search(science):
    c = science
    select(c)
    packet = method(c)
    packet["mature_method_search"]["queries"][0]["terms"] = "unexecuted cross-domain query"
    command(c, "submit-method", packet, expected=1)


@pytest.mark.parametrize("broken", [None, "original", "tool", "parent"])
def test_scientific_native_generic_reuses_bound_role_and_originals(science, broken):
    c = science
    command(c, "submit-problems", problems(c))
    handoff = command(c, "review-handoff", None, "--dispatch-mode", "native_generic_compat")
    payload = review(c)
    binding = deepcopy(handoff["task_binding"])
    if broken == "original":
        key = next(iter(binding["original_artifacts"]))
        binding["original_artifacts"][key] = "incomplete source"
    event = fixtures._native_generic_compat_event(c.root, binding=binding, payload=payload, role="scientific_reviewer",
                                                tool_name="shell" if broken == "tool" else None)
    if broken == "parent":
        path = c.root / "scientific_reviewer-native-generic.jsonl"
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        records[0]["payload"]["thread_source"] = "main"
        path.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")
    checked = subprocess.run([sys.executable, str(c.root / ".codex/hooks/subagent_attestation.py")], cwd=c.root,
                             input=json.dumps(event), text=True, capture_output=True)
    assert checked.returncode == 0
    if broken:
        assert "block" in checked.stdout
        command(c, "submit-review", payload, expected=1)
    else:
        assert checked.stdout == ""
        command(c, "submit-review", payload)
        assert core(c)["current_phase"] == "PROBLEM_SELECTION"


def test_literature_entry_keeps_cycle_profile_with_options_before_run_id(science):
    c = science
    restored = installed_command(c.root, ["python", "-m", "harness", "lit", "start", "--executor", "fixture-executor", c.run_id])
    assert restored["workflow"]["mode"] == "research_cycle" and restored["scientific_core"]["engine"] == "research_cycle_v1"
