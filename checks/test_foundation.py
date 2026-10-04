from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from harness.__main__ import main, literature_handoff
from arisctl import ARISController, ControllerError
from arisctl.workflow import literature_workflow_path
from tests import test_aris_controller as fixtures


@pytest.fixture
def accepted_landscape(tmp_path: Path, monkeypatch, capsys) -> ARISController:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ARIS_REVIEW_ATTESTATION_ROOT", str(tmp_path / "attestations"))
    fixtures.write_policy(tmp_path)
    assert main(["--root", str(tmp_path), "lit", "start", "run-1", "--executor", "fixture-executor"]) == 0
    state = json.loads(capsys.readouterr().out)
    assert [item["phase"] for item in state["phases"]] == ["landscape"]
    controller = ARISController(tmp_path, "run-1", literature_workflow_path())
    fixtures.approve(controller, "source_policy_approval")
    controller.submit_query_plan({
        "coverage_gaps": ["anchor"],
        "queries": [{"query": "test field", "purpose": "close explicit gap"}],
    })
    digest, request_id = fixtures.reach_coverage(controller)
    review = fixtures.coverage_review(digest, request_id)
    fixtures.attest(controller, "coverage_reviewer", review)
    controller.submit_coverage_review(review)
    return controller


def test_public_entry_finishes_at_map_and_exports_traceable_evidence(accepted_landscape, capsys):
    controller = accepted_landscape
    state = controller.status()
    assert state["scientific_core"]["status"] == "NOT_IMPLEMENTED"
    assert controller.current_stage() == "LANDSCAPE_ACCEPTED"
    assert state["research_lit"]["approval_request"] is None
    assert main(["--root", str(controller.root), "literature-handoff", controller.run_id]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["evidence"]["evidence:P1"]["sha256"]
    assert result["artifacts"]["active_field_map"]["sha256"]
    assert set(result["artifacts"]) >= {"evidence_registry", "literature_corpus", "search_log", "coverage_review", "query_plan"}
    assert "source_repo" in (controller.root / ".codex/ARIS_CONTROLLER_LAYER.json").read_text(encoding="utf-8")
    assert "scientific_core" not in state["workflow"]


def _gap_plan(gap: str, query: str) -> dict:
    return {
        "schema_version": 2,
        "search_strategy": {
            "priority_order": ["RECENT_AUTHORITATIVE_REVIEWS", "HIGH_CITATION_BACKBONE", "RECENT_ELITE_FRONTIER", "TARGETED_GAP_FOLLOWUP"],
            "discovery_sources": ["Google Scholar"],
            "time_range": {"year_from": 2000, "year_to": 2026},
            "screening_requirement": "TITLE_ABSTRACT_FOR_ALL_RETRIEVED_CANDIDATES",
            "saturation_criteria": ["the specific boundary is resolved or reframed"],
        },
        "coverage_gaps": [gap],
        "queries": [{
            "plan_item_id": "gap-p2", "query": query,
            "purpose": "test the missing failure boundary", "coverage_gaps": [gap],
            "priority_tier": "TARGETED_GAP_FOLLOWUP", "year_from": 2000,
            "year_to": 2026, "page": 1, "exact_title": False,
            "target_venues": ["Test Elite Venue"],
            "expected_close_condition": "evidence discriminates the boundary",
        }],
    }


def test_gap_update_reuses_registry_revises_map_and_can_repeat(accepted_landscape):
    controller = accepted_landscape
    before = deepcopy(controller.status()["research_lit"]["accepted_artifacts"]["evidence:P1"])
    gap = "The strongest method's failure boundary needs investigation."
    context = {"core_application": "synthetic fixture", "selected_problem": "P-selected", "problem_version": 2, "route_revision": "R1"}
    for cycle in (1, 2):
        query = f"boundary mechanism cycle {cycle}"
        controller.request_literature_update([gap], requested_by="method_design", context=context)
        with pytest.raises(ControllerError, match="LANDSCAPE_ACCEPTED"):
            literature_handoff(controller)
        with pytest.raises(ControllerError, match="required coverage gap"):
            controller.submit_query_plan(_gap_plan("unrelated gap", query))
        controller.submit_query_plan(_gap_plan(gap, query))
        controller.execute_query(query, "fixture-search", lambda _: [fixtures.metadata("P2")],
                                 plan_item_id="gap-p2", query_options={"year_from": 2000, "year_to": 2026, "exact_title": False, "page": 1})
        controller.decide_admission("P2", screening_in_scope=True, screening_basis="TITLE_ABSTRACT",
                                    screening_reason="addresses the requested failure boundary", reading_priority="TARGETED_GAP_FOLLOWUP")
        controller.decide_admission("P1", screening_in_scope=True, screening_basis="FULL_TEXT",
                                    screening_reason="retains the foundational evidence", reading_priority="HIGH_CITATION_BACKBONE",
                                    fulltext_selected=False, fulltext_selection_reason="accepted full-text Evidence already exists")
        controller.select_reading_subset(["P2"], rationale="read only the gap source")
        controller.finish_retrieval()
        if cycle == 1:
            read = controller.read_full_text("P2", "fixture-reader", lambda _: "synthetic full paper P2")
            controller.submit_evidence_card("P2", fixtures.card(read, "P2"))
        controller.finish_reading()
        field_map = fixtures.field_map()
        field_map["family_development_traces"][0]["evidence_ids"] = ["P1", "P2"]
        field_map["assumption_effectiveness_failure_matrix"][0]["source_ids"] = ["P1", "P2"]
        field_map["consensus"] = [f"Evidence revised the boundary in cycle {cycle}."]
        controller.submit_field_map(field_map)
        request = controller.status()["research_lit"]["coverage_review_request"]
        review = fixtures.coverage_review(request["artifact_sha256"], request["id"], bindings=request["artifact_bindings"])
        fixtures.attest(controller, "coverage_reviewer", review)
        controller.submit_coverage_review(review)
        assert controller.current_stage() == "LANDSCAPE_ACCEPTED"
        assert controller.status()["research_lit"]["accepted_artifacts"]["evidence:P1"] == before
        assert "evidence:P2" in literature_handoff(controller)["evidence"]
    state = controller.status()
    assert len(state["research_lit"]["literature_update_requests"]) == 2
    assert state["research_lit"]["literature_update_requests"][-1]["context"] == context
    assert len(state["research_lit"]["field_map_history"]) >= 3
    assert [item["phase"] for item in state["phases"]] == ["landscape"]


def test_installed_hook_imports_new_runtime_without_old_installation(accepted_landscape):
    controller = accepted_landscape
    payload = {"hook_event_name": "Stop", "cwd": str(controller.root)}
    hook = controller.root / ".codex/hooks/subagent_attestation.py"
    result = subprocess.run(
        [sys.executable, "-I", "-S", "-c",
         "import runpy,sys,types; sys.modules['yaml']=types.ModuleType('yaml'); runpy.run_path(sys.argv[1],run_name='__main__')", str(hook)],
        input=json.dumps(payload), text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr


def test_public_entry_does_not_expose_old_method_workflow():
    with pytest.raises(SystemExit) as exc:
        main(["lit", "start-phase", "unused"])
    assert exc.value.code == 2


def test_standalone_recovery_uses_new_entry_and_preserves_accepted_map(accepted_landscape, tmp_path):
    from arisctl.recovery import save_recovery_snapshot

    controller = accepted_landscape
    destination = tmp_path.parent / (tmp_path.name + "-recovery")
    save_recovery_snapshot(controller.root, controller.run_id, destination)
    manifest = json.loads((destination / "ARIS_RECOVERY.json").read_text(encoding="utf-8"))
    assert manifest["resume"]["status_command"] == "python -m harness lit status run-1"
    restored = ARISController(destination, controller.run_id, literature_workflow_path())
    assert literature_handoff(restored)["artifacts"]["active_field_map"]["sha256"] == (
        literature_handoff(controller)["artifacts"]["active_field_map"]["sha256"]
    )
