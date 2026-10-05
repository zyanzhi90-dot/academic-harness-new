"""Persist the historical mapping, then let the public science gate judge it.

This records an unusable historical LANDSCAPE_ACCEPTED snapshot; it does not
certify acceptance under the current audit or bypass science begin's checks.
"""

from copy import deepcopy
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import harness
from arisctl.controller import ARISController
from arisctl.project_setup import install_project_codex_layer
from arisctl.workflow import literature_workflow_path
from tools import run_state
from tools.literature_coverage_audit import audit_landscape

HERE = Path(__file__).resolve().parent
RUN = "impedance-control-landscape-e2e"


def main():
    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    z = zipfile.ZipFile(HERE / "source-8fff5f3.zip")
    source = json.loads(z.read(f".aris/runs/{RUN}.json"))
    state = deepcopy(source)
    controller = ARISController(ROOT, RUN, literature_workflow_path())
    state["workflow"] = deepcopy(controller.workflow)
    state["workflow_sha256"] = controller.workflow_sha256
    missing = "incremental-query-plan-problem_generation"
    missing_record = state["research_lit"]["accepted_artifacts"].pop(missing)
    state["phases"] = [deepcopy(next(p for p in source["phases"] if p["phase"] == "landscape"))]
    state["scientific_core"] = {"status": "NOT_IMPLEMENTED", "current_phase": None}
    state["legacy_imports"] = [{
        "source_commit": manifest["source_commit"], "source_archive_sha256": manifest["archive_sha256"],
        "from_workflow_sha256": source["workflow_sha256"], "to_workflow_sha256": controller.workflow_sha256,
        "historical_problem_versions": source["scientific_core"]["problem_versions"],
        "historical_scope_approval": [a for a in source["research_lit"]["approvals"] if a["gate"] == "scope_human_approval"],
        "missing_historical_artifacts": [{"name": missing, "record": missing_record}],
        "reason": "User-authorized legacy evidence/state mapping; no new approval, selection, reading or review",
        "screening_mapping": "cases/softscan-20261005/SCREENING_MAPPING.json",
        "line_endings": "Git LF restored to exact historical approved CRLF hashes",
        "current_acceptance": "BLOCKED_BY_CURRENT_LANDSCAPE_AUDIT",
    }]
    for name in state["research_lit"]["accepted_artifacts"]:
        controller._assert_artifact_current(state["research_lit"], name)
    audit = audit_landscape(ROOT, controller.workflow, state=state)
    state["legacy_imports"][0]["current_audit"] = audit
    state["research_lit"]["validator_results"].append({"artifact": "legacy_import_landscape",
        "result": "PASS" if audit["ok"] else "FAIL", "errors": audit["errors"],
        "origin": "actual 2026-10-05 import attempt; does not replace historical coverage review"})
    target = run_state._run_path(str(ROOT), RUN)
    assert not target.exists(), "preserve existing run"
    install_project_codex_layer(ROOT, literature_only=True)
    with run_state._lock(str(ROOT), RUN):
        run_state._save(str(ROOT), RUN, state)
    (HERE / "IMPORTED_STATE.json").write_bytes(target.read_bytes())
    print(json.dumps({"run": RUN, "legacy_stage": state["research_lit"]["current_stage"],
                      "current_audit_ok": audit["ok"], "current_audit_error_count": len(audit["errors"]),
                      "accepted_original_hash_checks": len(state["research_lit"]["accepted_artifacts"])}))


if __name__ == "__main__":
    main()
