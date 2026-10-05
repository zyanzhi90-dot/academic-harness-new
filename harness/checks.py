"""Offline checks of the migrated source and runtime resources."""

from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path
import re

from . import REPOSITORY_ROOT, VENDOR_ROOT
from arisctl.project_setup import MANAGED_FILES
from arisctl.workflow import load_workflow, literature_workflow_path, research_workflow_path


def check_foundation() -> dict:
    errors: list[str] = []
    manifest = json.loads((REPOSITORY_ROOT / "docs/REUSE_MANIFEST.json").read_text(encoding="utf-8"))
    records = list(manifest["files"])
    records.extend({"destination": item["path"], "destination_sha256": item["sha256"]}
                   for item in manifest["generated_profiles"])
    records.extend({"destination": item["path"], "destination_sha256": item["sha256"]}
                   for item in manifest.get("generated_scientific_files", []))
    records.extend({"destination": path, "destination_sha256": digest}
                   for path, digest in manifest["basis_sha256"].items())
    for record in records:
        path = REPOSITORY_ROOT / record["destination"]
        if not path.is_file():
            errors.append(f"missing reused file: {record['destination']}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != record["destination_sha256"]:
            errors.append(f"reuse hash mismatch: {record['destination']}")
    modules = [f"arisctl.{path.stem}" for path in (VENDOR_ROOT / "arisctl").glob("*.py") if path.stem != "__init__"]
    modules += ["tools.run_state", "tools.provenance", "tools.literature_coverage_audit"]
    for name in modules:
        module = importlib.import_module(name)
        if not Path(module.__file__).resolve().is_relative_to(VENDOR_ROOT):
            errors.append(f"module resolved outside migrated runtime: {name}")
    for source, _ in MANAGED_FILES:
        if not (VENDOR_ROOT / source).is_file():
            errors.append(f"missing project runtime resource: {source}")
    markdown = [VENDOR_ROOT / item["source"] for item in manifest["files"] if item["destination"].startswith("vendor/") and item["source"].endswith(".md")]
    markdown.append(REPOSITORY_ROOT / "skills/research-lit/SKILL.md")
    markdown.extend((REPOSITORY_ROOT / "skills/research-cycle").rglob("*.md"))
    for path in markdown:
        for link in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"^(?:https?://|#|mailto:|app:|sandbox:)", link):
                continue
            target = path.parent / link.split("#")[0]
            if not target.exists():
                errors.append(f"missing linked resource: {path.relative_to(REPOSITORY_ROOT)} -> {link}")
    workflow = load_workflow(literature_workflow_path())
    mirror = VENDOR_ROOT / "skills/skills-codex/shared-references/literature-workflow.yaml"
    if mirror.read_bytes() != literature_workflow_path().read_bytes():
        errors.append("literature workflow mirror differs")
    research = load_workflow(research_workflow_path())
    if (VENDOR_ROOT / "skills/skills-codex/shared-references/research-workflow.yaml").read_bytes() != research_workflow_path().read_bytes():
        errors.append("research workflow mirror differs")
    return {
        "ok": not errors,
        "reused_files": len(manifest["files"]),
        "runtime_modules": len(modules),
        "workflow_id": workflow["workflow_id"],
        "research_workflow_id": research["workflow_id"],
        "phases": [phase["phase"] for phase in workflow["phases"]],
        "errors": errors,
        "scope": "offline source, import and resource checks; no live research executed",
    }
