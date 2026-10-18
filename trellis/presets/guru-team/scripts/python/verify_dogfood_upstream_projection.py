#!/usr/bin/env python3
"""Read-only verification of source-locked official dogfood template bytes.

This complements Guru managed-asset drift checks. It neither installs official
templates nor treats editable platform configuration or Guru workflow/overlays
as upstream template projections.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from guru_platform_inventory import PLATFORM_BY_FLAG
from platform_projection_contract import DOGFOOD_PLATFORM_FLAGS
from verify_trellis_compatibility_matrix import MatrixError, validate_fork_source


# This official module was removed by the selected Fork. Its old template hash
# must not let an obsolete task/history reader survive a projection refresh.
RETIRED_OFFICIAL_PATHS = (".trellis/scripts/common/history_paths.py",)
EDITABLE_PLATFORM_CONFIG_PATHS = frozenset({
    ".claude/settings.json", ".codex/config.toml",
    ".codex/hooks.json", ".cursor/hooks.json",
})

NODE_PROJECTION = r"""
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const [source, repo, idsJson, excludedJson] = process.argv.slice(1);
const base = path.join(source, 'packages/cli/dist');
const load = rel => import(pathToFileURL(path.join(base, rel)).href);
const {getAllScripts, getAllAgents} = await load('templates/trellis/index.js');
const {collectPlatformTemplates} = await load('configurators/index.js');
const {preserveCodexAgentModelKeys} = await load('configurators/codex.js');
const {computeHash} = await load('utils/template-hash.js');
const files = new Map();
for (const [p, content] of getAllScripts()) files.set('.trellis/scripts/' + p, content);
for (const [p, content] of getAllAgents()) files.set('.trellis/agents/' + p, content);
for (const id of JSON.parse(idsJson)) {
  for (const [p, content] of collectPlatformTemplates(id)) files.set(p, content);
}
// This is the same documented user-model preservation used by official update.
preserveCodexAgentModelKeys(repo, files);
const excluded = new Set(JSON.parse(excludedJson));
const rows = [];
for (const [p, content] of files) {
  if (excluded.has(p)) continue;
  const absolute = path.join(repo, p);
  const actual = fs.existsSync(absolute) && fs.statSync(absolute).isFile()
    ? fs.readFileSync(absolute, 'utf8') : null;
  rows.push({path:p, template_hash:computeHash(content),
    installed_hash:actual === null ? null : computeHash(actual)});
}
console.log(JSON.stringify({rows,
  excluded_paths:[...files.keys()].filter(p => excluded.has(p)).sort()}));
"""


class ProjectionError(RuntimeError):
    pass


def load_projection(repo_root: Path, fork_source: Path) -> dict[str, Any]:
    ids = [PLATFORM_BY_FLAG[flag].upstream_id for flag in DOGFOOD_PLATFORM_FLAGS]
    completed = subprocess.run(
        ["node", "--input-type=module", "-e", NODE_PROJECTION,
         str(fork_source), str(repo_root), json.dumps(ids),
         json.dumps(sorted(EDITABLE_PLATFORM_CONFIG_PATHS))],
        cwd=fork_source, text=True, capture_output=True, check=False,
    )
    if completed.returncode:
        raise ProjectionError(
            "official template export failed: " + completed.stderr.strip()
        )
    return json.loads(completed.stdout)


def check_projection(
    repo_root: Path, projection: dict[str, Any], cli_version: str,
) -> dict[str, Any]:
    """Compare only the official export's exact paths; do not scan history."""
    hashes_path = repo_root / ".trellis/.template-hashes.json"
    hashes_document = json.loads(hashes_path.read_text(encoding="utf-8"))
    if not isinstance(hashes_document, dict) or hashes_document.get("__version") != 2 or not isinstance(
        hashes_document.get("hashes"), dict
    ):
        raise ProjectionError("official template hashes must use schema version 2")
    hashes = hashes_document["hashes"]
    errors: list[dict[str, str]] = []
    for row in projection["rows"]:
        relative = row["path"]
        if row["installed_hash"] is None:
            errors.append({"code": "missing_official_file", "path": relative})
        elif row["installed_hash"] != row["template_hash"]:
            errors.append({"code": "official_projection_drift", "path": relative})
        if hashes.get(relative) != row["template_hash"]:
            errors.append({"code": "official_template_hash_drift", "path": relative})
    version_path = repo_root / ".trellis/.version"
    actual_version = (
        version_path.read_text(encoding="utf-8").strip()
        if version_path.is_file() else None
    )
    if actual_version != cli_version:
        errors.append({"code": "official_version_drift", "path": ".trellis/.version"})
    for relative in RETIRED_OFFICIAL_PATHS:
        if (repo_root / relative).exists():
            errors.append({"code": "retired_official_file", "path": relative})
        if relative in hashes:
            errors.append({"code": "retired_official_hash", "path": relative})
    return {
        "status": "error" if errors else "ok",
        "selected_platforms": list(DOGFOOD_PLATFORM_FLAGS),
        "checked_file_count": len(projection["rows"]),
        "excluded_editable_paths": projection["excluded_paths"],
        "errors": errors,
    }


def verify(repo_root: Path, fork_source: Path) -> dict[str, Any]:
    source = validate_fork_source(repo_root, fork_source)
    projection = load_projection(repo_root, fork_source)
    result = check_projection(repo_root, projection, source["cli_version"])
    result["fork_commit"] = source["commit"]
    result["cli_version"] = source["cli_version"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--fork-source", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = verify(args.repo_root.resolve(), args.fork_source.resolve())
    except (MatrixError, ProjectionError, OSError, ValueError) as exc:
        result = {"status": "error", "detail": str(exc)}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    elif result["status"] == "ok":
        print(f"Verified {result['checked_file_count']} official dogfood files")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
