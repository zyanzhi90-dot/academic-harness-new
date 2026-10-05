"""Preserve public review requests; do not dispatch or emulate a reviewer."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = "impedance-control-landscape-e2e"

assert not (HERE / "REVIEW_HANDOFF_ATTEMPT.json").exists()
records = []
for label, args in [
    ("science_status_after_submission", ["science", "status", RUN]),
    ("science_actions_after_submission", ["science", "allowed-actions", RUN]),
    ("configured_review_handoff", ["science", "review-handoff", RUN]),
    ("generic_review_handoff", ["science", "review-handoff", RUN, "--dispatch-mode", "native_generic_compat"]),
]:
    result = subprocess.run([sys.executable, "-X", "utf8", "-m", "harness", *args], cwd=ROOT, capture_output=True)
    for stream in ("stdout", "stderr"):
        (HERE / f"{label}.{stream}.txt").write_bytes(getattr(result, stream))
    records.append({"label": label, "argv": args, "exit_code": result.returncode,
                    "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
                    "stderr_sha256": hashlib.sha256(result.stderr).hexdigest()})
    print(label, result.returncode, len(result.stdout))
(HERE / "REVIEW_HANDOFF_ATTEMPT.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
handoff = json.loads((HERE / "generic_review_handoff.stdout.txt").read_text(encoding="utf-8"))
print("keys", list(handoff))
print("string lengths", [(k, len(v)) for k, v in handoff.items() if isinstance(v, str)])
