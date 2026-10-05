"""Public scientific commands; the literature commands keep their original API."""

import json
from pathlib import Path

from .scientific_controller import ScientificController


def add_science_parser(sub):
    parser = sub.add_parser("science", help="problem discovery and concrete method research cycle")
    commands = parser.add_subparsers(dest="scientific_command", required=True)
    start = commands.add_parser("start")
    start.add_argument("run_id")
    start.add_argument("--executor", required=True)
    for name in ("begin", "submit-problems", "submit-method", "submit-review", "submit-check", "submit-prior-assessment", "request-literature-update"):
        command = commands.add_parser(name)
        command.add_argument("run_id")
        command.add_argument("json_file")
    for name in ("status", "allowed-actions", "allowed-agents", "handoff"):
        commands.add_parser(name).add_argument("run_id")
    review = commands.add_parser("review-handoff")
    review.add_argument("run_id")
    review.add_argument("--dispatch-mode", choices=("configured_role", "native_generic_compat"), default="configured_role")
    select = commands.add_parser("human-select-problem")
    select.add_argument("run_id")
    select.add_argument("candidate_id")
    select.add_argument("--request-id", required=True)
    select.add_argument("--accept-scope-change", action="store_true")
    confirm = commands.add_parser("human-confirm-method")
    confirm.add_argument("run_id")
    confirm.add_argument("--request-id", required=True)
    reopen = commands.add_parser("reopen-problem")
    reopen.add_argument("run_id")
    reopen.add_argument("--reason", required=True)
    reopen.add_argument("--evidence-id", action="append", required=True)


def execute_science(args):
    name = args.scientific_command
    if name == "start":
        return ScientificController.start(args.root, args.run_id, executor=args.executor).status()
    if name == "begin":
        from .scientific_validators import validate_frame
        validate_frame(json.loads(Path(args.json_file).read_text(encoding="utf-8")))
        controller = ScientificController.attach(args.root, args.run_id)
    else:
        controller = ScientificController(args.root, args.run_id)
    if hasattr(args, "json_file"):
        payload = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    if name == "human-select-problem":
        return controller.human_select_problem(args.candidate_id, args.request_id, accept_scope_change=args.accept_scope_change)
    if name == "human-confirm-method":
        return controller.human_confirm_method(args.request_id)
    if name == "reopen-problem":
        return controller.reopen_problem(args.reason, args.evidence_id)
    if name == "request-literature-update":
        return controller.request_literature_update(payload["gaps"], requested_by=payload["requested_by"], context=payload.get("context"))
    if name == "review-handoff":
        return controller.review_handoff(dispatch_mode=args.dispatch_mode)
    method = {"submit-problems": "submit_problems", "submit-method": "submit_method", "submit-review": "submit_review",
              "submit-check": "submit_check", "submit-prior-assessment": "submit_prior_assessment", "begin": "begin"}.get(name)
    if method:
        return getattr(controller, method)(payload)
    return getattr(controller, name.replace("-", "_"))()


def existing_controller(root, run_id):
    from arisctl import ARISController
    from arisctl.workflow import literature_workflow_path
    from tools import run_state
    path = Path(run_state._run_path(str(root), run_id))
    if path.is_file() and json.loads(path.read_text(encoding="utf-8"))["workflow"].get("mode") == "research_cycle":
        return ScientificController(root, run_id)
    return ARISController(root, run_id, literature_workflow_path())
