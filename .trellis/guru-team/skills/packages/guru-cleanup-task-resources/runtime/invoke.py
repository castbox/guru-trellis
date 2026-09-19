from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


RESOURCE_ORDER = {
    "worktree": 0,
    "branch": 1,
    "remote_branch": 2,
    "remote_tracking": 3,
    "runtime": 4,
}


def load(root: Path, package_root: Path, value: str, field: str) -> dict:
    path = Path(value)
    choices = [path] if path.is_absolute() else [root / path, package_root / path]
    source = next(
        (candidate for candidate in choices if candidate.is_file() and not candidate.is_symlink()),
        None,
    )
    if source is None:
        raise CommandError("invalid_json", field, "Provide one regular JSON file.")
    try:
        payload = json.loads(source.read_text())
    except json.JSONDecodeError as exc:
        raise CommandError("invalid_json", field, "Provide valid JSON.") from exc
    if not isinstance(payload, dict):
        raise CommandError("invalid_json", field, "Provide one object.")
    return payload


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if check and proc.returncode:
        raise CommandError(
            "stale_identity",
            "owned_resources",
            proc.stderr.strip() or "Refresh the reviewed task resources.",
            3,
        )
    return proc


def registered_worktrees(root: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    current: dict[str, str] = {}
    for line in git(root, "worktree", "list", "--porcelain").stdout.splitlines() + [""]:
        if not line:
            if "worktree" in current:
                rows[str(Path(current["worktree"]).resolve())] = current
            current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    return rows


def finish_receipt_path(root: Path, finish_ref: str) -> Path:
    return root / ".trellis/.runtime/guru-team/finish" / (finish_ref.rsplit(":", 1)[-1] + ".json")


def cleanup_receipt_path(root: Path, finish_ref: str) -> Path:
    return root / ".trellis/.runtime/guru-team/cleanup" / (finish_ref.rsplit(":", 1)[-1] + ".json")


def continuation(public: dict) -> dict:
    return {
        "exit_id": "remaining_resources",
        "task_ref": public["task_ref"],
        "archive_ref": public["archive_ref"],
        "finish_ref": public["finish_ref"],
    }


def read_finish_receipt(root: Path, package_root: Path, public: dict) -> tuple[Path, dict]:
    path = finish_receipt_path(root, public["finish_ref"])
    if not path.is_file() or path.is_symlink():
        raise CommandError(
            "stale_identity",
            "finish_ref",
            "Current Finish success receipt is missing or stale.",
            3,
        )
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError(
            "stale_identity",
            "finish_ref",
            "Current Finish success receipt is unreadable.",
            3,
        ) from exc
    validate_json(
        value,
        package_root.parent / "guru-finish-task/schemas/finish-transaction.schema.json",
        "finish_receipt",
    )
    expected = {
        "stage": "success",
        "task_ref": public["task_ref"],
        "archive_ref": public["archive_ref"],
        "finish_ref": public["finish_ref"],
    }
    if any(value.get(key) != expected_value for key, expected_value in expected.items()):
        raise CommandError(
            "stale_identity",
            "finish_ref",
            "Finish receipt is not the current terminal transaction for this cleanup call.",
            3,
        )
    return path, value


def archive_generation(root: Path, public: dict) -> int:
    path = root / public["archive_ref"] / "task.json"
    if not path.is_file() or path.is_symlink():
        raise CommandError("stale_identity", "archive_ref", "The terminal archive generation is missing.", 3)
    try:
        generation = json.loads(path.read_text()).get("lifecycle_generation", 0)
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("stale_identity", "archive_ref.task.json.lifecycle_generation", "The terminal archive generation is invalid.", 3) from exc
    if not isinstance(generation, int) or generation < 0:
        raise CommandError("stale_identity", "archive_ref.task.json.lifecycle_generation", "The terminal archive generation is invalid.", 3)
    return generation


def read_cleanup_receipt(root: Path, package_root: Path, public: dict, resources: list[dict], lifecycle_generation: int) -> Path | None:
    path = cleanup_receipt_path(root, public["finish_ref"])
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise CommandError("stale_identity", "cleanup_receipt", "Cleanup recovery receipt is unsafe.", 3)
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError("stale_identity", "cleanup_receipt", "Cleanup recovery receipt is invalid.", 3) from exc
    validate_json(value, package_root / "schemas/cleanup-transaction.schema.json", "cleanup_receipt")
    expected = {
        "stage": "cleaned",
        "task_ref": public["task_ref"],
        "archive_ref": public["archive_ref"],
        "finish_ref": public["finish_ref"],
        "lifecycle_generation": lifecycle_generation,
        "owned_resources": resources,
    }
    if any(value.get(key) != expected_value for key, expected_value in expected.items()):
        raise CommandError(
            "stale_identity",
            "cleanup_receipt",
            "Cleanup recovery receipt belongs to another reviewed cleanup call.",
            3,
        )
    archive = root / public["archive_ref"]
    active = root / public["task_ref"]
    if not archive.is_dir() or active.exists():
        raise CommandError(
            "stale_identity",
            "cleanup_receipt",
            "The finished task identity is no longer terminal; rediscover current lifecycle state.",
            3,
        )
    return path


def write_cleanup_receipt(root: Path, package_root: Path, public: dict, resources: list[dict], lifecycle_generation: int) -> Path:
    path = cleanup_receipt_path(root, public["finish_ref"])
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise CommandError("stale_identity", "cleanup_receipt", "Cleanup recovery receipt is unsafe.", 3)
    value = {
        "schema_version": "1.0",
        "stage": "cleaned",
        "task_ref": public["task_ref"],
        "archive_ref": public["archive_ref"],
        "finish_ref": public["finish_ref"],
        "lifecycle_generation": lifecycle_generation,
        "owned_resources": resources,
    }
    validate_json(value, package_root / "schemas/cleanup-transaction.schema.json", "cleanup_receipt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return path


def validate_runtime_resource(root: Path, path: Path, public: dict, finish_receipt: Path) -> bool:
    runtime_root = (root / ".trellis/.runtime/guru-team").resolve()
    if not str(path).startswith(str(runtime_root) + "/"):
        raise CommandError(
            "stale_identity",
            "owned_resources",
            "Runtime cleanup is outside the task runtime root.",
            3,
        )
    if path == finish_receipt.resolve():
        return path.is_file() and not path.is_symlink()
    if not path.exists():
        return False
    if not path.is_file() or path.is_symlink():
        raise CommandError(
            "stale_identity",
            "owned_resources",
            "Cleanup accepts only current task-bound runtime files.",
            3,
        )
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError(
            "stale_identity",
            "owned_resources",
            "Runtime resource is not current task-bound JSON.",
            3,
        ) from exc
    if not isinstance(value, dict) or public["task_ref"] not in {
        value.get("task_ref"),
        value.get("task_artifact_dir"),
    }:
        raise CommandError(
            "stale_identity",
            "owned_resources",
            "Runtime resource does not belong to the current task.",
            3,
        )
    return True


def remote_head(root: Path, branch: str) -> str | None:
    proc = git(root, "ls-remote", "--heads", "origin", f"refs/heads/{branch}", check=False)
    if proc.returncode:
        raise CommandError(
            "stale_identity",
            "owned_resources",
            proc.stderr.strip() or "Refresh the Finish-owned remote branch.",
            3,
        )
    rows = [line.split() for line in proc.stdout.splitlines() if line.strip()]
    if not rows:
        return None
    if len(rows) != 1 or len(rows[0]) != 2 or rows[0][1] != f"refs/heads/{branch}":
        raise CommandError("stale_identity", "owned_resources", "Remote branch identity is ambiguous.", 3)
    return rows[0][0]


def validate_resources(
    root: Path,
    public: dict,
    resources: list[dict],
    receipt: dict,
    finish_receipt: Path,
) -> set[tuple[str, str]]:
    worktree_rows = registered_worktrees(root)
    head_branch = receipt["head_branch"]
    head_ref = "refs/heads/" + head_branch
    expected_commit = receipt["commit"]
    expected_remote = "origin/" + head_branch
    expected_tracking = "refs/remotes/origin/" + head_branch
    present: set[tuple[str, str]] = set()
    seen: set[tuple[str, str]] = set()
    for item in resources:
        identity = (item["kind"], item["locator"])
        if identity in seen:
            raise CommandError("stale_identity", "owned_resources", "Cleanup resources must be unique.", 3)
        seen.add(identity)
        kind, locator = identity
        if kind == "branch":
            if locator != head_branch or locator in {receipt["base_branch"], "main", "master"} or locator.startswith("refs/"):
                raise CommandError(
                    "stale_identity",
                    "owned_resources",
                    "Branch cleanup must target the exact Finish head branch.",
                    3,
                )
            branch = git(root, "show-ref", "--verify", "--quiet", head_ref, check=False)
            if branch.returncode == 0:
                if git(root, "rev-parse", head_ref).stdout.strip() != expected_commit:
                    raise CommandError("stale_identity", "owned_resources", "Finish head branch moved.", 3)
                if git(
                    root,
                    "merge-base",
                    "--is-ancestor",
                    head_ref,
                    f"refs/remotes/origin/{receipt['base_branch']}",
                    check=False,
                ).returncode:
                    raise CommandError(
                        "stale_identity",
                        "owned_resources",
                        "Finish head branch is not contained in the verified target baseline.",
                        3,
                    )
                present.add(identity)
        elif kind == "worktree":
            path = Path(locator)
            if not path.is_absolute():
                raise CommandError(
                    "stale_identity",
                    "owned_resources",
                    "Worktree cleanup requires one exact absolute path.",
                    3,
                )
            resolved = path.resolve()
            if resolved == root:
                raise CommandError(
                    "stale_identity",
                    "owned_resources",
                    "Cleanup cannot remove the checkout executing the command.",
                    3,
                )
            row = worktree_rows.get(str(resolved))
            if row is not None:
                if row.get("branch") != head_ref or git(resolved, "rev-parse", "HEAD").stdout.strip() != expected_commit:
                    raise CommandError(
                        "stale_identity",
                        "owned_resources",
                        "Worktree is not registered to the exact Finish head branch and commit.",
                        3,
                    )
                if git(resolved, "status", "--porcelain=v1", "--untracked-files=all").stdout:
                    raise CommandError(
                        "stale_identity",
                        "owned_resources",
                        "Finish worktree is not clean and cannot be removed.",
                        3,
                    )
                present.add(identity)
            elif resolved.exists():
                raise CommandError(
                    "stale_identity",
                    "owned_resources",
                    "Existing worktree path is not registered to the Finish branch.",
                    3,
                )
        elif kind == "remote_branch":
            if locator != expected_remote:
                raise CommandError(
                    "stale_identity",
                    "owned_resources",
                    "Remote cleanup must target origin and the exact Finish head branch.",
                    3,
                )
            live_remote_head = remote_head(root, head_branch)
            if live_remote_head is not None:
                if live_remote_head != expected_commit:
                    raise CommandError("stale_identity", "owned_resources", "Finish remote branch moved.", 3)
                present.add(identity)
        elif kind == "remote_tracking":
            if locator != expected_tracking:
                raise CommandError(
                    "stale_identity",
                    "owned_resources",
                    "Remote-tracking cleanup must target the exact origin Finish ref.",
                    3,
                )
            tracking = git(root, "show-ref", "--verify", "--quiet", expected_tracking, check=False)
            if tracking.returncode == 0:
                if git(root, "rev-parse", expected_tracking).stdout.strip() != expected_commit:
                    raise CommandError("stale_identity", "owned_resources", "Finish remote-tracking ref moved.", 3)
                present.add(identity)
        else:
            path = (root / locator).resolve()
            if validate_runtime_resource(root, path, public, finish_receipt):
                present.add(identity)
    return present


def remove_resource(root: Path, item: dict, receipt: dict, finish_receipt: Path) -> bool:
    kind, locator = item["kind"], item["locator"]
    if kind == "runtime":
        path = (root / locator).resolve()
        if path.exists() and path != finish_receipt.resolve():
            try:
                path.unlink()
            except OSError:
                return False
        return True
    if kind == "worktree":
        path = Path(locator).resolve()
        if not path.exists():
            return True
        return git(root, "worktree", "remove", str(path), check=False).returncode == 0
    if kind == "branch":
        ref = f"refs/heads/{locator}"
        if git(root, "show-ref", "--verify", "--quiet", ref, check=False).returncode != 0:
            return True
        return git(root, "branch", "-d", locator, check=False).returncode == 0
    if kind == "remote_branch":
        branch = receipt["head_branch"]
        if remote_head(root, branch) is None:
            return True
        return git(root, "push", "origin", "--delete", branch, check=False).returncode == 0
    ref = f"refs/remotes/origin/{receipt['head_branch']}"
    if git(root, "show-ref", "--verify", "--quiet", ref, check=False).returncode != 0:
        return True
    return git(root, "update-ref", "-d", ref, receipt["commit"], check=False).returncode == 0


def run(package_root: Path, command: dict, argv: list[str]) -> dict:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-result", required=True)
    parser.add_argument("--confirmed-cleanup", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError("invalid_arguments", "arguments", "Use the cleanup command contract.") from exc

    root = Path(args.root or ".").resolve()
    public = load(root, package_root, args.input, "input")
    semantic = load(root, package_root, args.semantic_result, "semantic_result")
    validate_json(public, package_root / "schemas/public-input.schema.json", "input")
    validate_json(semantic, package_root / "schemas/semantic-result.schema.json", "semantic_result")
    if public["profile"] != semantic["profile"] or public["mode"] != semantic["mode"]:
        raise CommandError("stale_identity", "semantic_result", "Cleanup identity differs from Finish.", 3)

    route = semantic["route"]
    resources = semantic["owned_resources"]
    if public.get("resources") is not None and public["resources"] != resources:
        raise CommandError(
            "stale_identity",
            "owned_resources",
            "Cleanup resource discovery changed after review.",
            3,
        )

    if route["typed_exit"] == "remaining_resources":
        out = continuation(public)
        validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
        return out
    if route["typed_exit"] == "blocked":
        out = {"exit_id": "blocked"}
        validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
        return out

    finish_path = finish_receipt_path(root, public["finish_ref"])
    if finish_path.is_file() and not finish_path.is_symlink():
        finish_receipt, receipt = read_finish_receipt(root, package_root, public)
        lifecycle_generation = receipt["lifecycle_generation"]
    else:
        lifecycle_generation = archive_generation(root, public)
        recovered = read_cleanup_receipt(root, package_root, public, resources, lifecycle_generation)
        if recovered is not None:
            out = {"exit_id": "cleaned"}
            validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
            return out
        finish_receipt, receipt = read_finish_receipt(root, package_root, public)
    present = validate_resources(root, public, resources, receipt, finish_receipt)
    if present and not args.confirmed_cleanup:
        out = continuation(public)
        validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
        return out

    remaining = [
        item["locator"]
        for item in sorted(resources, key=lambda value: RESOURCE_ORDER[value["kind"]])
        if (item["kind"], item["locator"]) in present
        and not remove_resource(root, item, receipt, finish_receipt)
    ]
    if remaining:
        out = continuation(public)
        validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
        return out

    write_cleanup_receipt(root, package_root, public, resources, lifecycle_generation)
    finish_receipt.unlink(missing_ok=True)
    out = {"exit_id": "cleaned"}
    validate_json(out, package_root / "schemas/public-output.schema.json", "stdout")
    return out


if __name__ == "__main__":
    try:
        print(json.dumps(run(Path(__file__).parents[1], {}, sys.argv[1:]), ensure_ascii=False))
    except CommandError as exc:
        print(
            json.dumps(
                {"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise SystemExit(exc.exit_status)
