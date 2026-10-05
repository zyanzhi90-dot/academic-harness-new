"""One-time, pinned state mapping for this real case; no scientific gate replay."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import harness
from arisctl.controller import ARISController
from arisctl.gateways import append_jsonl
from arisctl.project_setup import install_project_codex_layer
from arisctl.validators import sha256_file
from arisctl.workflow import literature_workflow_path
from tools import run_state
from tools.literature_coverage_audit import audit_landscape

HERE = Path(__file__).resolve().parent
RUN = "impedance-control-landscape-e2e"


def main():
    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    archive = HERE / "source-8fff5f3.zip"
    assert sha256_file(archive) == manifest["archive_sha256"]
    target = run_state._run_path(str(ROOT), RUN)
    assert not target.exists(), "never overwrite an existing live run"
    z = zipfile.ZipFile(archive)
    source = json.loads(z.read(f".aris/runs/{RUN}.json"))
    assert source["research_lit"]["current_stage"] == "LANDSCAPE_ACCEPTED"
    accepted = source["research_lit"]["accepted_artifacts"]
    approval = accepted["source_admission_policy"]
    assert any(a["decision"] == "approve" and a["approval_request_id"] == approval["approval_request_id"]
               for a in source["research_lit"]["approvals"])
    restored = {}
    missing = []
    for row in manifest["accepted_binding_audit"]:
        if row["reconstruction"] == "MISSING_IN_PINNED_GIT_TREE":
            # This superseded old-phase plan is not a landscape input. Keep the
            # exact old record in import history, not as a live existing file.
            assert row["name"] == "incremental-query-plan-problem_generation"
            missing.append({"name": row["name"], "record": accepted[row["name"]]})
            continue
        data = z.read(row["path"])
        if row["reconstruction"] == "LF_TO_CRLF":
            data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        assert hashlib.sha256(data).hexdigest() == row["recorded_sha256"], row["path"]
        restored[row["path"]] = data
    for path in ("idea-stage/EVIDENCE_REGISTRY.jsonl", "idea-stage/LITERATURE_CORPUS.jsonl", "idea-stage/SEARCH_LEDGER.jsonl"):
        restored[path] = z.read(path).replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    for relative, data in restored.items():
        path = ROOT / relative
        assert path.resolve().is_relative_to(ROOT)
        assert not path.exists() or path.read_bytes() == data, f"changed artifact: {relative}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    corpus = ROOT / "idea-stage/LITERATURE_CORPUS.jsonl"
    original_rows = [json.loads(line) for line in z.read("idea-stage/LITERATURE_CORPUS.jsonl").decode("utf-8").splitlines() if line.strip()]
    latest = {row["source_id"]: row for row in original_rows}
    mapped_decisions = []
    for paper_id, original in latest.items():
        # The old initial survey stored decisions at top level; its subsequent
        # supplements used phase-scoped decisions. Reuse the recorded decision,
        # without screening again or inventing a landscape-era approval.
        recorded = original if original.get("screening_status") else next(
            (d for d in reversed(original.get("context_decisions", [])) if d.get("screening_status")), {})
        assert recorded.get("screening_status") in {"IN_SCOPE", "OUT_OF_SCOPE", "DUPLICATE"}, paper_id
        fields = ("admission_status", "admission_exception", "screening_in_scope", "screening_status",
                  "screening_basis", "screening_reason", "reading_priority", "fulltext_selected",
                  "fulltext_selection_reason", "screened_at", "decided_at", "decision_id", "duplicate")
        decision = {k: deepcopy(recorded[k]) for k in fields if k in recorded}
        decision["context"] = {"phase": "landscape", "origin": "legacy_case_import",
                               "source_commit": manifest["source_commit"],
                               "original_record_sha256": original["record_sha256"],
                               "original_context": deepcopy(recorded.get("context")),
                               "semantics": "existing screening reused in unified evidence corpus; not a new reading/screening/approval"}
        mapped = deepcopy(original)
        mapped.pop("record_sha256", None)
        mapped.pop("previous_record_sha256", None)
        mapped["context_decisions"] = [*mapped.get("context_decisions", []), decision]
        append_jsonl(corpus, mapped)
        mapped_decisions.append({"paper_id": paper_id, "original_record_sha256": original["record_sha256"],
                                 "mapped_decision": decision})
    (HERE / "SCREENING_MAPPING.json").write_text(json.dumps(mapped_decisions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    controller = ARISController(ROOT, RUN, literature_workflow_path())
    state = deepcopy(source)
    state["workflow"] = deepcopy(controller.workflow)
    state["workflow_sha256"] = controller.workflow_sha256
    # Keep all real literature events and decisions, including historical model
    # identities and approval timestamps. Do not re-label them as new work.
    for row in missing:
        del state["research_lit"]["accepted_artifacts"][row["name"]]
    state["phases"] = [deepcopy(next(p for p in source["phases"] if p["phase"] == "landscape"))]
    state["scientific_core"] = {"status": "NOT_IMPLEMENTED", "current_phase": None}
    state["legacy_imports"] = [{
        "source_commit": manifest["source_commit"], "source_archive_sha256": manifest["archive_sha256"],
        "source_state_git_sha256": hashlib.sha256(z.read(f".aris/runs/{RUN}.json")).hexdigest(),
        "from_workflow_sha256": source["workflow_sha256"], "to_workflow_sha256": controller.workflow_sha256,
        "reason": "User-authorized adoption of accepted literature only; old problem approval is historical scope evidence, not a new selection",
        "missing_historical_artifacts": missing,
        "historical_problem_versions": source["scientific_core"]["problem_versions"],
        "historical_scope_approval": [a for a in source["research_lit"]["approvals"] if a["gate"] == "scope_human_approval"],
        "line_endings": "Pinned Git LF blobs restored to exact approved CRLF SHA256; no content/hash substitution",
    }]
    audit = audit_landscape(ROOT, controller.workflow, state=state)
    audit_path = HERE / ("IMPORT_AUDIT.json" if not (HERE / "IMPORT_AUDIT.json").exists() else "MAPPED_IMPORT_AUDIT.json")
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "PROPOSED_IMPORT_STATE.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert audit["ok"], {"error_count": len(audit["errors"]), "first_errors": audit["errors"][:5]}
    for name, record in state["research_lit"]["accepted_artifacts"].items():
        controller._assert_artifact_current(state["research_lit"], name)
    install_project_codex_layer(ROOT, literature_only=True)
    with run_state._lock(str(ROOT), RUN):
        run_state._save(str(ROOT), RUN, state)
    # Initial import state is an immutable run record even though live .aris is
    # ignored by Git. Subsequent Controller output is saved separately.
    (HERE / "IMPORTED_STATE.json").write_bytes(target.read_bytes())
    print(json.dumps({"run": RUN, "stage": state["research_lit"]["current_stage"],
                      "accepted_inputs": len(state["research_lit"]["accepted_artifacts"]), "audit": audit}))


if __name__ == "__main__":
    main()
