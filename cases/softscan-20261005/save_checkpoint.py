"""Archive the actual review checkpoint and check byte-preserved evidence.

The isolated negative audit is an engineering check, never scientific evidence.
This script does not mutate the live Controller state or mint review receipts.
"""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
import harness
import harness.scientific_controller as scientific_controller
import harness.scientific_validators as scientific_validators
from arisctl.project_setup import verify_formal_native_subagent_runtime
from tools.literature_coverage_audit import audit_landscape

RUN = "impedance-control-landscape-e2e"
digest = lambda data: hashlib.sha256(data).hexdigest()
def save(name, value):
    target = HERE / name
    assert not target.exists(), f"preserve original {name}"
    target.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

state_path = ROOT / f".aris/runs/{RUN}.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
core = state["scientific_core"]
assert core["current_phase"] == "PROBLEM_REVIEW"
assert core["active_problem_version"] is None and core["active_route"] is None
assert not core["approvals"] and not core["problem_versions"] and not core["route_versions"]
handoff = json.loads((HERE / "generic_review_handoff.stdout.txt").read_text(encoding="utf-8"))
task = handoff["task"].encode("utf-8")
task_path = HERE / "review-task.exact.txt"
if task_path.exists():
    assert task_path.read_bytes() == task
else:
    task_path.write_bytes(task)
bindings = core["review_request"]["artifact_bindings"]
assert handoff["artifact_bindings"] == bindings
for path, expected in bindings.items():
    assert digest((ROOT / path).read_bytes()) == expected, path
    assert handoff["task_binding"]["original_artifacts"][path].encode("utf-8") == (ROOT / path).read_bytes()
assert json.loads((ROOT / core["accepted_artifacts"]["problems"]["path"]).read_text(encoding="utf-8"))["content"] == json.loads((HERE / "problems.first.json").read_text(encoding="utf-8"))

source_manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
source_archive = HERE / "source-8fff5f3.zip"
assert digest(source_archive.read_bytes()) == source_manifest["archive_sha256"]
with zipfile.ZipFile(source_archive) as source:
    for record in source_manifest["files"]:
        assert digest(source.read(record["path"])) == record["git_bytes_sha256"]
    source_state = json.loads(source.read(f".aris/runs/{RUN}.json"))
    inherited = {}
    for path in ("idea-stage/LITERATURE_CORPUS.jsonl", "idea-stage/EVIDENCE_REGISTRY.jsonl", "idea-stage/SEARCH_LEDGER.jsonl"):
        original = source.read(path).replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        current = (ROOT / path).read_bytes()
        assert current.startswith(original)
        if not path.endswith("LITERATURE_CORPUS.jsonl"):
            assert current == original
        inherited[path] = {"original_bytes": len(original), "original_sha256": digest(original),
                           "original_prefix_preserved": True, "current_bytes": len(current), "current_sha256": digest(current)}
    historical_versions = source_state["scientific_core"]["problem_versions"]
    assert historical_versions[-1]["acceptance"]["confirmed_in"] == "explicit_human_command"

baseline = audit_landscape(ROOT, state["workflow"], state=state)
assert baseline["ok"], baseline
with tempfile.TemporaryDirectory(prefix="softscan-audit-") as directory:
    isolated = Path(directory)
    paths = set(state["workflow"]["artifact_manifest"].values())
    paths.update(record["path"] for record in state["research_lit"]["accepted_artifacts"].values())
    for path in paths:
        origin = ROOT / path
        if origin.is_file():
            target = isolated / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origin, target)
    registry = isolated / state["workflow"]["artifact_manifest"]["evidence_registry"]
    rows = registry.read_bytes().splitlines(keepends=True)
    registry.write_bytes(b"".join(row for row in rows if json.loads(row)["source_id"] != "j4KJ1EdUyYAJ"))
    negative = audit_landscape(isolated, deepcopy(state["workflow"]), state=deepcopy(state))
    expected = "full-text-selected candidate j4KJ1EdUyYAJ has no accepted Evidence Card"
    assert not negative["ok"] and expected in negative["errors"], negative
save("ADAPTATION_CHECK.json", {"scope": "Engineering checks only, not research effects or scientific approval",
     "current_real_case_audit": baseline, "isolated_missing_selected_evidence": {
         "expected_rejection_observed": expected, "audit": negative},
     "source_archive_all_file_hashes_match": len(source_manifest["files"]),
     "current_bound_original_hashes_match": len(bindings), "inherited_jsonl": inherited})

runtime_paths = [".agents/skills/research-cycle/SKILL.md", ".agents/skills/research-lit/SKILL.md",
                 "harness/scientific_controller.py", "harness/scientific_validators.py",
                 "vendor/aris/skills/shared-references/research-workflow.yaml",
                 ".codex/config.toml", ".codex/agents/scientific_reviewer.toml", ".codex/hooks.json",
                 ".codex/hooks/pre_tool_use_policy.py", ".codex/hooks/subagent_attestation.py"]
save("RUNTIME_EXECUTION.json", {"at": datetime.now(timezone.utc).isoformat(), "run_id": RUN,
     "current_phase": core["current_phase"], "review_request_id": core["review_request"]["id"],
     "loaded_by_main": [".agents/skills/research-cycle/SKILL.md", ".agents/skills/research-lit/SKILL.md"],
     "actual_controller_module": scientific_controller.__file__, "actual_validator_module": scientific_validators.__file__,
     "runtime_file_sha256": {path: digest((ROOT / path).read_bytes()) for path in runtime_paths},
     "native_structural_preflight": verify_formal_native_subagent_runtime(ROOT, "scientific_reviewer"),
     "configured_reviewer_role": ".codex/agents/scientific_reviewer.toml", "actual_reviewer_session": None,
     "reviewer_dispatched": False, "reviewer_verdict": None, "natural_completion_hook_observed": False,
     "hook_trust_confirmed_in_this_run": False, "scientific_review_receipt": None,
     "hook_paths": {"PreToolUse": ".codex/hooks/pre_tool_use_policy.py", "SubagentStop": ".codex/hooks/subagent_attestation.py", "Stop": ".codex/hooks/subagent_attestation.py"},
     "runtime_boundary": "Installed configuration/preflight is not proof that configured roles or natural Hooks executed",
     "dispatch_capability": "This session's collaboration.spawn_agent schema cannot select a configured role; exact native_generic_compat handoff required",
     "dispatch_blocker": "The full task cannot be carried unchanged through the current model-to-child invocation; task was not truncated, split, replaced with a file reference or dispatched",
     "task": {"path": "review-task.exact.txt", "characters": len(handoff["task"]), "utf8_bytes": len(task),
              "sha256": digest(task), "bound_originals": len(bindings)},
     "pending_platform_prerequisite": "Project Hook trust and natural native child-completion path are not verified in this run",
     "human_selection": None, "method_design_started": False,
     "scientific_effect_acceptance": "UNDETERMINED: first candidate exists; independent review and PROBLEM_SELECTION not reached"})

snapshot_paths = {state_path}
snapshot_paths.update(ROOT / path for path in bindings)
snapshot_paths.update(ROOT / path for path in state["workflow"]["artifact_manifest"].values() if (ROOT / path).is_file())
snapshot = HERE / "CURRENT_RUN_SNAPSHOT.zip"
assert not snapshot.exists()
entries = []
with zipfile.ZipFile(snapshot, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(snapshot_paths):
        data = path.read_bytes()
        relative = path.relative_to(ROOT).as_posix()
        entry = zipfile.ZipInfo(relative, (2026, 10, 5, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(entry, data)
        entries.append({"path": relative, "bytes": len(data), "sha256": digest(data)})
save("CURRENT_RUN_SNAPSHOT.json", {"run_id": RUN, "stage": "PROBLEM_REVIEW", "archive_sha256": digest(snapshot.read_bytes()),
     "reason": "Exact current run/evidence bytes retained; .aris remains an ignored live runtime", "files": entries})
print(json.dumps({"phase": core["current_phase"], "task_characters": len(handoff["task"]),
                  "task_utf8_bytes": len(task), "bindings": len(bindings), "snapshot_files": len(entries),
                  "negative_selected_evidence_guard": "PASS"}))
