"""Record actual public CLI results without manufacturing gate receipts."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import harness
from arisctl.project_setup import verify_formal_native_subagent_runtime
from harness.scientific_validators import validate_frame, validate_problems

HERE = Path(__file__).resolve().parent
RUN = "impedance-control-landscape-e2e"


def main():
    assert not (HERE / "RUN_ATTEMPT.json").exists(), "preserve the first actual CLI attempt"
    frame = json.loads((HERE / "frame.json").read_text(encoding="utf-8"))
    packet = json.loads((HERE / "problems.first.json").read_text(encoding="utf-8"))
    state_path = ROOT / f".aris/runs/{RUN}.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    known = {k.split(":", 1)[1]: r for k, r in state["research_lit"]["accepted_artifacts"].items() if k.startswith("evidence:")}
    validate_frame(frame)
    validate_problems(packet, frame, known, [])
    records = []
    commands = [
        ("before_status", ["lit", "status", RUN]),
        ("before_actions", ["lit", "allowed-actions", RUN]),
        ("accepted_handoff_attempt", ["literature-handoff", RUN]),
        ("science_begin_attempt", ["science", "begin", RUN, str(HERE / "frame.json")]),
        ("after_status", ["lit", "status", RUN]),
        ("science_handoff_attempt", ["science", "handoff", RUN]),
    ]
    for label, args in commands:
        result = subprocess.run([sys.executable, "-X", "utf8", "-m", "harness", *args],
                                cwd=ROOT, capture_output=True)
        for stream in ("stdout", "stderr"):
            (HERE / f"{label}.{stream}.txt").write_bytes(getattr(result, stream))
        records.append({"label": label, "argv": [sys.executable, "-X", "utf8", "-m", "harness", *args],
                        "exit_code": result.returncode,
                        "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
                        "stderr_sha256": hashlib.sha256(result.stderr).hexdigest()})
        if label not in {"before_status", "after_status"}:
            print(label, result.returncode, result.stdout.decode("utf-8")[:250])
    native = verify_formal_native_subagent_runtime(ROOT, "scientific_reviewer")
    manifest = json.loads((ROOT / ".codex/ARIS_CONTROLLER_LAYER.json").read_text(encoding="utf-8"))
    result = {"at": datetime.now(timezone.utc).isoformat(), "root": str(ROOT), "run": RUN,
              "commands": records, "candidate_schema_check": "PASS_ONLY_NOT_SCIENTIFIC_REVIEW",
              "native_structural_preflight": native, "managed_layer": manifest,
              "module_paths": {"ScientificController": str(ROOT / "harness/scientific_controller.py"),
                               "Validator": str(ROOT / "harness/scientific_validators.py")},
              "actual_runtime": {"source_skill_read": "skills/research-cycle/SKILL.md",
                  "installed_skill_read": ".agents/skills/research-cycle/SKILL.md",
                  "configured_role": ".codex/agents/scientific_reviewer.toml",
                  "formal_reviewer_dispatched": False, "natural_completion_hook_observed": False,
                  "new_review_receipt": None, "human_selection": None, "method_design_started": False,
                  "reason": "Public landscape handoff and science begin failed current landscape audit before a scientific request could be issued; structural preflight is not role/Hook lifecycle evidence"},
              "state_unchanged_by_attempt": state_path.read_bytes() == (HERE / "IMPORTED_STATE.json").read_bytes()}
    (HERE / "RUN_ATTEMPT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert result["state_unchanged_by_attempt"]
    print("No problem submission, reviewer, human selection or method-design command executed.")


if __name__ == "__main__":
    main()
