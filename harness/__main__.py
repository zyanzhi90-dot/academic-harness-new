"""Public literature entry; scientific problem/method modules follow later."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from arisctl.__main__ import main as literature_main, _emit_json, _emit
from arisctl.controller import ARISController, ControllerError
from arisctl.validators import sha256_file
from arisctl.workflow import literature_workflow_path
from tools.literature_coverage_audit import audit_landscape


LITERATURE_COMMANDS = (
    "start", "status", "allowed-actions", "allowed-agents", "save-recovery",
    "submit-source-policy", "request-source-policy-revision", "human-approve",
    "submit-query-plan", "query", "enrich-candidate", "enrich-candidates",
    "retry-candidate-enrichment", "recover-interrupted-query",
    "reconcile-query-plan-events", "extend-literature-budget",
    "submit-human-search-results", "submit-human-fulltext-batch", "defer-fulltext-batch",
    "promote-user-source", "repair-literature-corpus-hash-chain", "admit", "admit-batch",
    "select-reading-subset", "select-formal-primary-subset", "withdraw-admission",
    "reverify-admission", "register-user-source", "read-text", "fetch-fulltext",
    "read-user-fulltext", "materialize-completed-read-event", "submit-evidence",
    "preflight-native-subagent", "finish-retrieval", "finish-reading",
    "submit-field-map", "submit-coverage-review", "attest-review-transcript",
    "submit-coverage-review-transcript",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="harness")
    parser.add_argument("--root", default=".", help="research project directory")
    sub = parser.add_subparsers(dest="entry", required=True)
    lit = sub.add_parser("lit", help="retained literature lifecycle")
    lit.add_argument("command", choices=LITERATURE_COMMANDS)
    lit.add_argument("arguments", nargs=argparse.REMAINDER)
    update = sub.add_parser("update-literature", help="reopen the same map for concrete gaps")
    update.add_argument("run_id")
    update.add_argument("--gap", action="append", required=True)
    update.add_argument("--requested-by", choices=("field_cognition", "problem_discovery", "method_design"), required=True)
    update.add_argument("--context", help="JSON object recording application/problem/route context")
    handoff = sub.add_parser("literature-handoff", help="current accepted map and evidence references")
    handoff.add_argument("run_id")
    sub.add_parser("check", help="check reuse hashes and local runtime dependencies")
    return parser


def literature_handoff(controller: ARISController) -> dict:
    state = controller.status()
    research = state["research_lit"]
    if research["current_stage"] != "LANDSCAPE_ACCEPTED":
        raise ControllerError("literature handoff requires LANDSCAPE_ACCEPTED")
    for name in ("source_admission_policy", "active_field_map", "coverage_review"):
        controller._assert_artifact_current(research, name)
    audit = audit_landscape(controller.root, state["workflow"], state=state)
    if not audit["ok"] or audit["coverage_status"] != "SUFFICIENT":
        raise ControllerError("literature handoff audit failed: " + "; ".join(audit["errors"]))
    return {
        "run_id": controller.run_id,
        "project_root": str(controller.root),
        "workflow_sha256": controller.workflow_sha256,
        "stage": research["current_stage"],
        "artifacts": {
            **{
                name: {"path": str(path.relative_to(controller.root)), "sha256": sha256_file(path)}
                for name, path in controller._paths().items()
            },
            **{
                name: {"path": research["accepted_artifacts"][name]["path"],
                       "sha256": research["accepted_artifacts"][name]["sha256"]}
                for name in ("coverage_review", "query_plan")
            },
        },
        "evidence": {
            key: dict(record) for key, record in research["accepted_artifacts"].items()
            if key.startswith("evidence:")
        },
        "update_requests": research.get("literature_update_requests", []),
        "next_modules": "problem discovery and method design: not implemented",
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.entry == "lit":
            return literature_main(
                ["--root", args.root, args.command, *args.arguments],
                workflow_path=literature_workflow_path(),
            )
        if args.entry == "check":
            from .checks import check_foundation
            result = check_foundation()
            _emit_json(result)
            return 0 if result["ok"] else 1
        controller = ARISController(args.root, args.run_id, literature_workflow_path())
        if args.entry == "update-literature":
            context = json.loads(Path(args.context).read_text(encoding="utf-8")) if args.context else None
            result = controller.request_literature_update(args.gap, requested_by=args.requested_by, context=context)
        else:
            result = literature_handoff(controller)
        _emit_json(result)
        return 0
    except (ControllerError, OSError, ValueError) as exc:
        _emit(f"error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
