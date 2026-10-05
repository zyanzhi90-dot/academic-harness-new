"""Capture the specified case's Git objects without touching its worktree."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

COMMIT = "8fff5f3cbb1d47405f54888c0e92c61d08e31ced"
RUN = "impedance-control-landscape-e2e"
HERE = Path(__file__).resolve().parent


def capture(source):
    git = ["git", "-c", f"safe.directory={source}", "-C", str(source)]
    def read(*args):
        return subprocess.check_output(git + list(args))
    assert read("rev-parse", COMMIT).decode().strip() == COMMIT
    tree = read("ls-tree", "-rz", COMMIT).decode("utf-8").split("\0")
    selected = {}
    for row in tree:
        if not row:
            continue
        info, path = row.split("\t")
        # State, accepted originals, failed/revised history and source records;
        # no credentials, runtime configuration or publisher PDFs are copied.
        if path.startswith((".aris/", "idea-stage/")) or (
            "/" not in path and Path(path).suffix in {".md", ".txt", ".json", ".yaml"}
            and path not in {"AGENTS.md", "status-utf8-smoke.json"}
        ):
            selected[path] = (info.split()[2], read("cat-file", "blob", info.split()[2]))
    archive = HERE / "source-8fff5f3.zip"
    assert not archive.exists(), "preserve the first source snapshot"
    records = []
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path, (oid, data) in sorted(selected.items()):
            entry = zipfile.ZipInfo(path, (2026, 10, 5, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(entry, data)
            records.append({"path": path, "git_blob": oid, "bytes": len(data),
                            "git_bytes_sha256": hashlib.sha256(data).hexdigest()})
    state = json.loads(selected[f".aris/runs/{RUN}.json"][1])
    bindings = []
    for name, record in state["research_lit"]["accepted_artifacts"].items():
        path = record["path"].replace("\\", "/")
        row = {"name": name, "path": path, "recorded_sha256": record["sha256"]}
        if path not in selected:
            row["reconstruction"] = "MISSING_IN_PINNED_GIT_TREE"
        else:
            data = selected[path][1]
            variants = {"git_bytes": data, "LF_TO_CRLF": data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")}
            row["git_bytes_sha256"] = hashlib.sha256(data).hexdigest()
            row["reconstruction"] = next((k for k, b in variants.items()
                                          if hashlib.sha256(b).hexdigest() == record["sha256"]), "UNRESOLVED")
        bindings.append(row)
    manifest = {"source_repository": "zyanzhi90-dot/e2e", "source_commit": COMMIT,
                "local_object_source": str(source), "source_worktree_head": read("rev-parse", "HEAD").decode().strip(),
                "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                "files": records, "accepted_binding_audit": bindings}
    (HERE / "SOURCE_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files": len(records), "archive_bytes": archive.stat().st_size,
                      "binding_results": {k: sum(x["reconstruction"] == k for x in bindings)
                                          for k in {x["reconstruction"] for x in bindings}}}))


if __name__ == "__main__":
    capture(Path(sys.argv[1]).resolve())
