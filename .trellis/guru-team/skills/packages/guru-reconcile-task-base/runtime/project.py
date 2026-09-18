from __future__ import annotations

import argparse
import copy
from pathlib import Path

from common import parse, read_json, repo_root, resolve_commit, validate_json
from runtime.io import CommandError


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--authoring", required=True)
    args = parse(parser, argv)
    repo = repo_root(args.root)
    public = read_json(repo, package_root, args.input, "input")
    result = read_json(repo, package_root, args.result, "result")
    authoring = read_json(repo, package_root, args.authoring, "authoring")
    validate_json(public, package_root / "schemas/public-resolved-candidate-input.schema.json", "input")
    validate_json(result, package_root / "schemas/resolved-reconciliation-result.schema.json", "result")
    validate_json(authoring, package_root / "schemas/resolved-full-review-authoring.schema.json", "authoring")
    expected = {
        "task_ref": public["task_ref"],
        "branch": public["branch"],
        "phase2_commit_anchor": public["phase2_commit_anchor"],
        "old_base_head": public["old_base_head"],
        "new_base_head": public["new_base_head"],
        "merge_head": public["merge_head"],
        "stage0_tree": public["stage0_tree"],
        "index_tree_sha256": public["index_tree_sha256"],
        "parent_order": public["parent_order"],
        "commit_message": public["commit_message"],
    }
    if (
        any(result[key] != value for key, value in expected.items())
        or resolve_commit(repo, "HEAD", "HEAD") != result["reconciled_task_head"]
        or authoring["mode"] != public["mode"]
        or authoring["base_ref"] != public["selected_base_ref"]
    ):
        raise CommandError("stale_identity", "result", "Use the exact current resolved reconciliation result and Branch Review authoring.", 3)
    output = {
        **copy.deepcopy(authoring),
        "task_ref": public["task_ref"],
        "branch_review_commit": result["reconciled_task_head"],
    }
    target = package_root.parent / "guru-review-branch/schemas/public-branch-review-input.schema.json"
    validate_json(output, target, "stdout")
    return output
