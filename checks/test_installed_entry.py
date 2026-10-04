"""Installed command/Hook interactions; all human decisions are synthetic fixtures."""

from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import shlex
import shutil
import subprocess
import sys

import pytest
import yaml

from harness.__main__ import main
from arisctl import ARISController
from arisctl.project_setup import verify_formal_native_subagent_runtime
from arisctl.workflow import literature_workflow_path
from tests import test_aris_controller as fixtures


LAUNCHERS = (["python", "-m", "harness"], ["python3", "-m", "harness"],
             ["py", "-m", "harness"], ["academic-harness"])
HUMAN_COMMANDS = ("human-approve", "request-source-policy-revision")


def installed_rules(root: Path) -> list[dict]:
    rules = []
    runpy.run_path(str(root / ".codex/rules/aris.rules"),
                   init_globals={"prefix_rule": lambda **rule: rules.append(rule)})
    return rules


def rule_decisions(root: Path, argv: list[str]) -> list[str]:
    # Evaluate this project's prefix-only rules, including token alternatives.
    return [rule["decision"] for rule in installed_rules(root)
            if len(argv) >= len(rule["pattern"]) and all(
                token in expected if isinstance(expected, list) else token == expected
                for token, expected in zip(argv, rule["pattern"]))]


def hook_result(root: Path, command: str, *, input_key: str = "command") -> str:
    config = json.loads((root / ".codex/hooks.json").read_text(encoding="utf-8"))
    entry = config["hooks"]["PreToolUse"][0]["hooks"][0]
    configured = shlex.split(entry["commandWindows"] if os.name == "nt" else entry["command"])
    env = {**os.environ, "PATH": str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]}
    executable = shutil.which(configured[0], path=env["PATH"])
    assert executable, configured[0]
    result = subprocess.run([executable, *configured[1:]], cwd=root, env=env,
                            input=json.dumps({"hook_event_name": "PreToolUse", "cwd": str(root),
                                              "tool_name": "Bash", "tool_input": {input_key: command}}),
                            text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr
    return result.stdout


def installed_command(root: Path, argv: list[str], *, expected_code: int = 0) -> dict | str:
    """Run only after Hook passage; fixture runner stands in for the human terminal.

    This proves process/rule compatibility, not Codex UI confirmation or trust.
    """
    assert hook_result(root, shlex.join(argv)) == ""
    env = {**os.environ, "PATH": str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]}
    executable = shutil.which(argv[0], path=env["PATH"])
    assert executable, argv[0]
    result = subprocess.run([executable, *argv[1:]], cwd=root, env=env, text=True, capture_output=True, check=False)
    assert result.returncode == expected_code, result.stdout + result.stderr
    return json.loads(result.stdout) if expected_code == 0 else result.stdout + result.stderr


@pytest.fixture
def installed_project(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["lit", "start", "run-1", "--executor", "fixture-executor"]) == 0
    capsys.readouterr()
    return tmp_path


@pytest.mark.parametrize("launcher", LAUNCHERS)
@pytest.mark.parametrize("command", HUMAN_COMMANDS)
@pytest.mark.parametrize("input_key", ["command", "cmd"])
def test_installed_human_prefixes_pass_hook_and_require_prompt(installed_project, launcher, command, input_key):
    argv = [*launcher, "lit", command, "run-1"]
    if command == "human-approve":
        argv += ["source_policy_approval", "--decision", "approve"]
    assert hook_result(installed_project, shlex.join(argv), input_key=input_key) == ""
    assert rule_decisions(installed_project, argv) == ["prompt"]


@pytest.mark.parametrize("command", [
    'python -c "controller.human_approve(\'source_policy_approval\', \'approve\')"',
    'python -c "controller.request_source_policy_revision()"',
    'python -m unrelated human-approve run-1',
    'python -m harness lit status human-approve',
    'python -m harness lit revise-problem run-1',
    'python -m harness --root . lit human-approve run-1 source_policy_approval --decision approve',
    'academic-harness --root . lit request-source-policy-revision run-1',
])
def test_installed_hook_does_not_treat_alternate_calls_as_human_decisions(installed_project, command):
    before = ARISController(installed_project, "run-1", literature_workflow_path()).status()
    result = json.loads(hook_result(installed_project, command))
    assert result["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert ARISController(installed_project, "run-1", literature_workflow_path()).status() == before


@pytest.mark.parametrize("launcher", [LAUNCHERS[0], LAUNCHERS[-1]])
def test_installed_commands_validate_revise_and_approve_exact_candidate(installed_project, launcher):
    root = installed_project
    controller = ARISController(root, "run-1", literature_workflow_path())
    candidate = root / "candidate.yaml"
    policy = fixtures.policy_payload()
    candidate.write_text(yaml.safe_dump(policy), encoding="utf-8")
    submitted = installed_command(root, [*launcher, "lit", "submit-source-policy", "run-1", "candidate.yaml"])
    waiting = submitted["research_lit"]
    assert waiting["current_stage"] == "WAITING_FOR_HUMAN"
    assert waiting["approvals"] == []
    assert "source_admission_policy" not in waiting["accepted_artifacts"]
    request = waiting["approval_request"]
    assert installed_command(root, [*launcher, "lit", "status", "run-1"])["research_lit"] == waiting
    revised = installed_command(root, [*launcher, "lit", "request-source-policy-revision", "run-1"])
    research = revised["research_lit"]
    assert research["current_stage"] == "SOURCE_POLICY_DRAFTING"
    assert research["approval_request"] is None
    assert research["pending_source_policy"] is None
    assert research["approvals"][-1]["decision"] == "request_revision"
    assert research["approvals"][-1]["approval_request_id"] == request["id"]
    assert "source_admission_policy" not in research["accepted_artifacts"]
    policy["notes"] = "Synthetic human requested this revised candidate."
    candidate.write_text(yaml.safe_dump(policy), encoding="utf-8")
    waiting = installed_command(root, [*launcher, "lit", "submit-source-policy", "run-1", "candidate.yaml"])["research_lit"]
    assert waiting["approval_request"]["id"] != request["id"]
    argv = [*launcher, "lit", "human-approve", "run-1", "source_policy_approval", "--decision", "approve"]
    assert rule_decisions(root, argv) == ["prompt"]
    approved = installed_command(root, argv)["research_lit"]
    assert approved["current_stage"] == "QUERY_PLANNING"
    record = approved["accepted_artifacts"]["source_admission_policy"]
    assert record["approved_by"] == "human"
    assert record["sha256"] == waiting["approval_request"]["artifact_sha256"]
    assert record["approval_request_id"] == waiting["approval_request"]["id"]
    assert approved["approvals"][-1]["confirmed_in"] == "explicit_human_command"
    assert controller.status()["scientific_core"]["status"] == "NOT_IMPLEMENTED"
    instructions = (root / "AGENTS.md").read_text(encoding="utf-8")
    assert "no --root before lit" in instructions
    assert "Never approve on the AI's own judgment" in instructions


def test_installed_approval_still_rejects_changed_candidate(installed_project):
    root = installed_project
    candidate = root / "candidate.yaml"
    candidate.write_text(yaml.safe_dump(fixtures.policy_payload()), encoding="utf-8")
    installed_command(root, ["python", "-m", "harness", "lit", "submit-source-policy", "run-1", "candidate.yaml"])
    controller = ARISController(root, "run-1", literature_workflow_path())
    pending = controller.status()["research_lit"]["pending_source_policy"]
    path = root / pending["path"]
    path.write_text(path.read_text(encoding="utf-8") + "\n# fixture changed after validation\n", encoding="utf-8")
    result = installed_command(root, ["python", "-m", "harness", "lit", "human-approve", "run-1",
                                     "source_policy_approval", "--decision", "approve"], expected_code=1)
    assert "changed" in result
    assert controller.current_stage() == "WAITING_FOR_HUMAN"
    assert controller.status()["research_lit"]["approvals"] == []


def test_reinstall_refreshes_old_hook_without_resetting_run_or_user_instructions(installed_project):
    root = installed_project
    controller = ARISController(root, "run-1", literature_workflow_path())
    before = controller.status()
    for relative in ("hooks/pre_tool_use_policy.py", "rules/aris.rules"):
        (root / ".codex" / relative).write_text("# stale installed file", encoding="utf-8")
    agents = root / "AGENTS.md"
    agents.write_text("# Existing user instructions\n", encoding="utf-8")
    assert main(["lit", "start", "run-1", "--executor", "fixture-executor"]) == 0
    assert controller.status() == before
    assert agents.read_text(encoding="utf-8") == "# Existing user instructions\n"
    verify_formal_native_subagent_runtime(root, "paper_reader", runtime_project_root=root)
    argv = ["python", "-m", "harness", "lit", "request-source-policy-revision", "run-1"]
    assert hook_result(root, shlex.join(argv)) == ""
    assert rule_decisions(root, argv) == ["prompt"]
