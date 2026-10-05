"""Scientific contracts for the shared research run, not scientific truth scores."""

from __future__ import annotations

import hashlib
import json

from arisctl.validators import ValidationError


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def mechanism_digest(mechanism):
    from copy import deepcopy
    technical = deepcopy(mechanism)
    for derivation in technical.get("derivations", []):
        derivation.pop("status", None)
        derivation.pop("check_ids", None)
    return digest(technical)


def obj(value, label):
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    return value


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be non-empty text")
    return value


def texts(value, label, *, empty=False):
    if not isinstance(value, list) or (not empty and not value):
        raise ValidationError(f"{label} must be a list" + ("" if empty else " with entries"))
    for item in value:
        text(item, label)
    if len(value) != len(set(value)):
        raise ValidationError(f"{label} contains duplicate entries")
    return value


def rows(value, label, *, empty=False):
    if not isinstance(value, list) or (not empty and not value):
        raise ValidationError(f"{label} must be a list of objects")
    return [obj(item, label) for item in value]


def fields(value, names, label):
    obj(value, label)
    for name in names:
        text(value.get(name), f"{label}.{name}")


def choice(value, options, label):
    if value not in options:
        raise ValidationError(f"{label} must be one of {sorted(options)}")
    return value


def evidence(value, known, label, *, empty=False):
    ids = texts(value, label, empty=empty)
    if set(ids) - set(known):
        raise ValidationError(f"{label} refers to unregistered/currently unavailable Evidence")
    return ids


def validate_frame(frame):
    fields(frame, ("core_application", "key_research_question", "target_domain", "operating_envelope"), "frame")
    texts(frame.get("success_criteria"), "frame.success_criteria")
    texts(frame.get("constraints"), "frame.constraints")
    return frame


def validate_priors(priors, known, *, empty=True):
    for prior in rows(priors, "prior_assessments", empty=empty):
        fields(prior, ("source_domain", "domain_rationale", "coverage_rationale", "strongest_argument",
                       "assumptions", "failure_boundaries", "remaining_pain"), "prior")
        evidence(prior.get("evidence_ids"), known, "prior.evidence_ids")
        choice(prior.get("domain_identity"), {"IN_FIELD", "CROSS_FIELD", "UNCERTAIN"}, "prior.domain_identity")
        choice(prior.get("coverage"), {"SUBSTANTIAL", "PARTIAL", "RELATED", "UNKNOWN"}, "prior.coverage")
        choice(prior.get("covers"), {"PROBLEM", "CONTRIBUTION"}, "prior.covers")
    return priors


def strong_prior(priors):
    return any(p["domain_identity"] == "IN_FIELD" and p["coverage"] == "SUBSTANTIAL" for p in priors)


def validate_feedback(responses, pending, known):
    seen = set()
    for response in rows(responses, "feedback_responses", empty=True):
        fields(response, ("feedback_id", "response", "changed_elements"), "feedback response")
        evidence(response.get("evidence_ids"), known, "feedback evidence", empty=True)
        if response["feedback_id"] not in pending or response["feedback_id"] in seen:
            raise ValidationError("feedback response must identify one pending feedback item exactly once")
        seen.add(response["feedback_id"])
    if seen != set(pending):
        raise ValidationError("all pending feedback must be consumed with a reasoned response")


def validate_problems(packet, frame, known, pending):
    obj(packet, "problem packet")
    validate_feedback(packet.get("feedback_responses", []), pending, known)
    candidates = rows(packet.get("candidates"), "candidates")
    ids = []
    for candidate in candidates:
        fields(candidate, ("id", "core_application", "key_research_question", "pain_point", "significance",
                           "current_solution_extent", "scope_change_rationale"), "candidate")
        if candidate["core_application"] != frame["core_application"]:
            raise ValidationError("candidate must retain the core application")
        route = choice(candidate.get("discovery_path"), {"COMMUNITY_RECOGNIZED", "COMMON_FAILURE"}, "discovery_path")
        choice(candidate.get("failure_origin"), {"AUTHOR_REPORTED", "INFERENCE", "HYPOTHESIS"}, "failure_origin")
        ids.append(candidate["id"])
        refs = evidence(candidate.get("evidence_ids"), known, "candidate.evidence_ids")
        interrogation = obj(candidate.get("interrogation"), "interrogation")
        text(interrogation.get("strongest_argument"), "interrogation.strongest_argument")
        for key in ("premises", "counterexamples", "alternative_explanations", "literature_conflicts"):
            texts(interrogation.get(key), f"interrogation.{key}", empty=key == "literature_conflicts")
        if route == "COMMON_FAILURE":
            text(interrogation.get("first_principles"), "interrogation.first_principles")
            if len(refs) < 2:
                raise ValidationError("COMMON_FAILURE requires evidence from multiple papers")
        validate_priors(candidate.get("prior_assessments"), known, empty=False)
        texts(candidate.get("unverified_claims"), "candidate.unverified_claims", empty=True)
    if len(ids) != len(set(ids)):
        raise ValidationError("candidate IDs must be unique")
    return packet


def validate_binding(binding, selected):
    expected = {key: selected[key] for key in ("problem_id", "version", "sha256")}
    if binding != expected:
        raise ValidationError("problem binding does not match the human-selected version")


def validate_method(packet, selected, known, pending, checks, query_ids):
    obj(packet, "method packet")
    validate_binding(packet.get("problem_binding"), selected)
    fields(packet, ("route_id", "change_reason", "scientific_delta", "expected_benefit"), "method")
    validate_feedback(packet.get("feedback_responses", []), pending, known)
    mechanism = obj(packet.get("mechanism"), "mechanism")
    fields(mechanism, ("model", "applicability"), "mechanism")
    for key in ("inputs", "outputs"):
        texts(mechanism.get(key), f"mechanism.{key}")
    variables = rows(mechanism.get("variables"), "variables")
    for variable in variables:
        fields(variable, ("name", "meaning", "units"), "variable")
    if len({v["name"] for v in variables}) != len(variables):
        raise ValidationError("variable names must be unique")
    for step in rows(mechanism.get("algorithm"), "algorithm"):
        fields(step, ("id", "operation"), "algorithm step")
        texts(step.get("inputs"), "step.inputs")
        texts(step.get("outputs"), "step.outputs")
    for derivation in rows(mechanism.get("derivations"), "derivations"):
        fields(derivation, ("id", "expression", "rationale"), "derivation")
        texts(derivation.get("assumptions"), "derivation.assumptions")
        choice(derivation.get("status"), {"INFERENCE", "CHECKED"}, "derivation.status")
        if derivation["status"] == "CHECKED":
            refs = texts(derivation.get("check_ids"), "derivation.check_ids")
            _supporting_checks(refs, checks, selected, mechanism, {"THEORY"}, derivation=derivation)
    for component in rows(mechanism.get("components"), "components"):
        fields(component, ("id", "purpose", "input", "output", "why_needed", "isolation_test"), "component")
        texts(component.get("assumptions"), "component.assumptions")
    texts(mechanism.get("assumptions"), "mechanism.assumptions")
    search = obj(packet.get("mature_method_search"), "mature_method_search")
    for query in rows(search.get("queries"), "mature method queries"):
        fields(query, ("query_id", "terms", "domain", "outcome"), "mature method query")
        if query["query_id"] not in query_ids:
            raise ValidationError("mature-method search must bind an actually executed query")
        executed = query_ids[query["query_id"]]
        if executed.get("status") != "complete" or executed.get("query") != query["terms"]:
            raise ValidationError("mature-method search must use the exact completed query terms")
    sources = rows(search.get("sources"), "mature method sources", empty=True)
    for source in sources:
        fields(source, ("domain_rationale", "mechanism", "input_output_match", "assumption_match",
                        "changes", "attribution", "coverage_rationale"), "mature method source")
        evidence(source.get("evidence_ids"), known, "source.evidence_ids")
        choice(source.get("domain_identity"), {"IN_FIELD", "CROSS_FIELD", "UNCERTAIN"}, "source.domain_identity")
        choice(source.get("reuse_mode"), {"DIRECT_REUSE", "TRANSFER", "ADAPT", "FUSE", "NOT_USED"}, "source.reuse_mode")
        choice(source.get("coverage"), {"SUBSTANTIAL", "PARTIAL", "RELATED", "UNKNOWN"}, "source.coverage")
    choice(packet.get("design_mode"), {"DIRECT_REUSE", "TRANSFER", "ADAPT", "FUSE", "ORIGINAL"}, "design_mode")
    if packet["design_mode"] == "ORIGINAL":
        text(packet.get("original_design_rationale"), "original_design_rationale")
    elif not any(source["reuse_mode"] != "NOT_USED" for source in sources):
        raise ValidationError("reuse/transfer must identify the source mechanism being used")
    validate_priors(packet.get("prior_assessments"), known)
    claims = rows(packet.get("claims"), "claims")
    claim_ids = [c.get("id") for c in claims]
    if any(not isinstance(i, str) or not i for i in claim_ids) or len(set(claim_ids)) != len(claim_ids):
        raise ValidationError("claim IDs must be unique non-empty strings")
    for claim in claims:
        fields(claim, ("id", "statement", "limitations"), "claim")
        choice(claim.get("kind"), {"THEORETICAL", "EMPIRICAL"}, "claim.kind")
        choice(claim.get("evidence_status"), {"AUTHOR_REPORTED", "INFERENCE", "HYPOTHESIS", "VALIDATED"}, "claim.evidence_status")
        evidence(claim.get("evidence_ids"), known, "claim.evidence_ids", empty=True)
        refs = texts(claim.get("check_ids", []), "claim.check_ids", empty=True)
        if claim["evidence_status"] == "AUTHOR_REPORTED" and not claim["evidence_ids"]:
            raise ValidationError("author-reported claims require source Evidence")
        if claim["evidence_status"] == "VALIDATED":
            if not refs:
                raise ValidationError("validated claim requires performed supporting checks")
            kinds = {"THEORY"} if claim["kind"] == "THEORETICAL" else {"INDEPENDENT_VALIDATION"}
            _supporting_checks(refs, checks, selected, mechanism, kinds, claim)
    plans = rows(packet.get("checks"), "checks")
    check_ids = []
    derivation_ids = {d["id"] for d in mechanism["derivations"]}
    for plan in plans:
        fields(plan, ("check_id", "comparison", "controls", "metric", "setting", "expected_observation",
                      "falsifying_result", "execution_authorization"), "check plan")
        choice(plan.get("kind"), {"THEORY", "DESIGN_SELECTION", "INDEPENDENT_VALIDATION"}, "check.kind")
        targets = texts(plan.get("claim_ids"), "check.claim_ids")
        if set(targets) - set(claim_ids):
            raise ValidationError("check refers to an unknown claim")
        derivations = texts(plan.get("derivation_ids", []), "check.derivation_ids", empty=True)
        if set(derivations) - derivation_ids or (derivations and plan["kind"] != "THEORY"):
            raise ValidationError("only theory checks can evaluate declared derivations")
        check_ids.append(plan["check_id"])
    if len(check_ids) != len(set(check_ids)):
        raise ValidationError("check IDs must be unique")
    if not any(p["kind"] == "INDEPENDENT_VALIDATION" for p in plans):
        raise ValidationError("method requires an independent contribution validation plan")
    plans_by_id = {p["check_id"]: p for p in plans}
    for claim in claims:
        if claim["evidence_status"] == "VALIDATED":
            _current_plans(claim["check_ids"], checks, plans_by_id)
    for derivation in mechanism["derivations"]:
        if derivation["status"] == "CHECKED":
            _current_plans(derivation["check_ids"], checks, plans_by_id)
    for improvement in rows(packet.get("improvements", []), "improvements", empty=True):
        fields(improvement, ("change", "rationale", "benefit", "cost", "validation"), "improvement")
        evidence(improvement.get("evidence_ids"), known, "improvement.evidence_ids", empty=True)
    texts(packet.get("alternatives"), "alternatives")
    return packet


def _current_plans(ids, checks, plans):
    for check_id in ids:
        if check_id not in plans or checks[check_id]["result"]["plan_sha256"] != digest(plans[check_id]):
            raise ValidationError("performed check cannot support changed validation conditions")


def _supporting_checks(ids, checks, selected, mechanism, kinds, claim=None, derivation=None):
    for check_id in ids:
        record = checks.get(check_id)
        if not record or record["result"]["outcome"] != "PASS" or record["result"]["kind"] not in kinds:
            raise ValidationError("supporting check is missing, failed, or not independent for this claim")
        if record["problem_binding"] != {key: selected[key] for key in ("problem_id", "version", "sha256")}:
            raise ValidationError("supporting check belongs to another problem version")
        if record["mechanism_sha256"] != mechanism_digest(mechanism):
            raise ValidationError("supporting check belongs to a changed mechanism")
        if claim is not None:
            if claim["id"] not in record["result"]["claim_ids"] or record["claim_bindings"].get(claim["id"]) != digest({"statement": claim["statement"], "kind": claim["kind"]}):
                raise ValidationError("supporting check did not evaluate this exact claim")
        if derivation is not None and derivation["id"] not in record["result"].get("derivation_ids", []):
            raise ValidationError("theory check did not evaluate this derivation")


REVIEW_DIMENSIONS = {
    "PROBLEMS": ("problem_reality", "question_value", "scope_fidelity", "prior_classification"),
    "METHOD": ("mechanism_completeness", "reuse_fit", "contribution_boundary", "validation_logic", "engineering_conditions"),
}


def validate_review(payload, request, known):
    fields(payload, ("run_id", "review_request_id", "reviewer", "verdict_id", "rationale"), "review")
    if payload["run_id"] != request["run_id"] or payload["review_request_id"] != request["id"]:
        raise ValidationError("review does not match live request")
    if payload.get("reviewed_artifact_hashes") != request["artifact_bindings"]:
        raise ValidationError("review artifact bindings are stale or incomplete")
    decision = choice(payload.get("decision"), set(request["accepted_verdicts"]), "review.decision")
    assessments = obj(payload.get("assessments"), "review.assessments")
    if set(assessments) != set(REVIEW_DIMENSIONS[request["kind"]]):
        raise ValidationError("review must assess exactly the requested scientific dimensions")
    for dimension in REVIEW_DIMENSIONS[request["kind"]]:
        assessment = obj(assessments.get(dimension), dimension)
        text(assessment.get("rationale"), f"{dimension}.rationale")
        choice(assessment.get("status"), {"PASS", "GAP"}, f"{dimension}.status")
    issues = rows(payload.get("issues"), "review.issues", empty=True)
    for issue in issues:
        fields(issue, ("id", "rationale", "requested_change"), "issue")
        choice(issue.get("target"), {"PROBLEM_DISCOVERY", "METHOD_DESIGN"}, "issue.target")
        evidence(issue.get("evidence_ids"), known, "issue.evidence_ids", empty=True)
        expected_target = "PROBLEM_DISCOVERY" if request["kind"] == "PROBLEMS" or decision == "RETURN_TO_PROBLEM" or strong_prior(payload.get("prior_assessments", [])) else "METHOD_DESIGN"
        if issue["target"] != expected_target:
            raise ValidationError("review feedback must target the stage to which work returns")
    validate_priors(payload.get("prior_assessments"), known)
    if decision in {"PROBLEMS_READY", "METHOD_READY"}:
        if any(a["status"] != "PASS" for a in assessments.values()) or issues or strong_prior(payload["prior_assessments"]):
            raise ValidationError("ready verdict cannot carry unresolved issues, assessment gaps, or covering in-field prior")
    elif not issues:
        raise ValidationError("non-ready review requires actionable feedback")
    if strong_prior(payload["prior_assessments"]):
        texts(payload.get("gaps"), "covering prior followup gaps")
    if decision in {"UPDATE_LITERATURE", "RETURN_TO_PROBLEM"}:
        texts(payload.get("gaps"), "review.gaps")
    return payload
