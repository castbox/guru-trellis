from __future__ import annotations

import argparse
import copy
import hashlib
import json
import stat
import subprocess
import sys
from pathlib import Path

from runtime.io import CommandError
from runtime.schema import validate_json


RETIRED_EXITS = {"passed", "continuity_passed", "blocked"}


def parse(parser, argv):
    parser.add_argument("--json", action="store_true")
    try:
        return parser.parse_args(argv)
    except SystemExit as exc:
        raise CommandError(
            "invalid_arguments", "arguments", "Use exact command help."
        ) from exc


def root(package_root, value=None):
    repo = Path(value or ".").resolve()
    if not repo.is_dir() or not (repo / ".git").exists():
        raise CommandError("unsafe_path", "root", "Use a Git repository root.")
    return repo


def _lstat_below(boundary: Path, target: Path, field: str, final_kind: str) -> None:
    boundary = boundary.resolve()
    try:
        relative = target.relative_to(boundary)
    except ValueError as exc:
        raise CommandError(
            "unsafe_path", field, "Use the exact owner-private path."
        ) from exc
    current = boundary
    parts = relative.parts
    for index, part in enumerate(parts):
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            raise CommandError(
                "stale_identity", field, "Rerecord the current Branch Review gate.", 3
            )
        if stat.S_ISLNK(metadata.st_mode):
            raise CommandError(
                "unsafe_path", field, "Owner-private paths must not contain symlinks."
            )
        expected = final_kind if index == len(parts) - 1 else "directory"
        if expected == "directory" and not stat.S_ISDIR(metadata.st_mode):
            raise CommandError(
                "unsafe_path", field, "Owner-private ancestors must be directories."
            )
        if expected == "file" and not stat.S_ISREG(metadata.st_mode):
            raise CommandError(
                "unsafe_path", field, "The Branch Review checkpoint must be a regular file."
            )


def load(repo, package_root, value, field):
    if value == "-":
        raw = sys.stdin.read()
    else:
        candidate = Path(str(value or ""))
        choices = [candidate] if candidate.is_absolute() else [repo / candidate, package_root / candidate]
        source = next(
            (path for path in choices if path.is_file() and not path.is_symlink()), None
        )
        if source is None:
            raise CommandError("unsafe_path", field, "Use a regular JSON file.")
        raw = source.read_text()
    try:
        value = json.loads(raw)
    except Exception as exc:
        raise CommandError(
            "invalid_json", field, "Provide one JSON object."
        ) from exc
    if not isinstance(value, dict):
        raise CommandError("invalid_json", field, "Provide one JSON object.")
    return value


def task(repo: Path, value: str | None) -> Path:
    raw = str(value or "")
    if not raw:
        current = repo / ".trellis/.runtime/current-task"
        if current.is_file() and not current.is_symlink():
            raw = current.read_text().strip()
    if raw.startswith(".trellis/tasks/"):
        relative = Path(raw)
        if relative.as_posix() != raw or ".." in relative.parts or "." in relative.parts:
            raise CommandError(
                "unsafe_path", "task", "Use one normalized task path below .trellis/tasks."
            )
        candidate = repo / relative
    else:
        if not raw or "/" in raw or raw in {".", ".."}:
            raise CommandError(
                "unsafe_path", "task", "Use one current task below .trellis/tasks."
            )
        tasks_root = repo / ".trellis/tasks"
        found = list(tasks_root.glob(f"**/{raw}")) if tasks_root.is_dir() else []
        candidate = found[0] if len(found) == 1 else None
    if candidate is None:
        raise CommandError(
            "unsafe_path", "task", "Use one current task below .trellis/tasks."
        )
    _lstat_below(repo, candidate, "task", "directory")
    tasks_root = repo / ".trellis/tasks"
    if not candidate.resolve().is_relative_to(tasks_root.resolve()):
        raise CommandError(
            "unsafe_path", "task", "Use one current task below .trellis/tasks."
        )
    return candidate


def rel(repo: Path, path: Path) -> str:
    return path.resolve().relative_to(repo.resolve()).as_posix()


def checkpoint(repo: Path, task_dir: Path) -> Path:
    return (
        repo
        / ".trellis/.runtime/guru-team/owner-checkpoints"
        / task_dir.name
        / "review-gate.json"
    )


def _prepare_checkpoint_parent(repo: Path, target: Path) -> None:
    boundary = repo.resolve()
    current = boundary
    for part in target.parent.relative_to(boundary).parts:
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            current.mkdir()
            metadata = current.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise CommandError(
                "unsafe_path",
                "checkpoint",
                "Owner-private checkpoint ancestors must be regular directories.",
            )
    if target.exists() or target.is_symlink():
        _lstat_below(repo, target, "checkpoint", "file")


def store_checkpoint(repo: Path, task_dir: Path, value: dict) -> tuple[Path, bool]:
    target = checkpoint(repo, task_dir)
    _prepare_checkpoint_parent(repo, target)
    duplicate = False
    if target.is_file() and not target.is_symlink():
        try:
            existing = json.loads(target.read_text())
        except Exception as exc:
            raise CommandError(
                "invalid_json", "checkpoint", "Remove the invalid checkpoint and rerecord."
            ) from exc
        duplicate = isinstance(existing, dict) and {
            key: copy.deepcopy(item)
            for key, item in existing.items()
            if key != "generated_at"
        } == {
            key: copy.deepcopy(item)
            for key, item in value.items()
            if key != "generated_at"
        }
    if not duplicate:
        target.write_text(
            json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        )
    return target, duplicate


def load_checkpoint(repo: Path, task_dir: Path) -> tuple[Path, dict]:
    target = checkpoint(repo, task_dir)
    _lstat_below(repo, target, "checkpoint", "file")
    try:
        value = json.loads(target.read_text())
    except Exception as exc:
        raise CommandError(
            "invalid_json", "checkpoint", "Rerecord one valid Branch Review gate."
        ) from exc
    if not isinstance(value, dict):
        raise CommandError(
            "invalid_json", "checkpoint", "Rerecord one valid Branch Review gate."
        )
    return target, value


def retire_checkpoint(repo: Path, task_dir: Path) -> None:
    target, _ = load_checkpoint(repo, task_dir)
    target.unlink()
    for parent in (target.parent, target.parent.parent):
        try:
            parent.rmdir()
        except OSError:
            break


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def git(repo, *args, check=True):
    process = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and process.returncode:
        raise CommandError(
            "stale_identity",
            "repository",
            process.stderr.strip() or "Repair Git state.",
            3,
        )
    return process.stdout.strip()


def ancestor(repo, ancestor_ref, descendant_ref):
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor_ref, descendant_ref],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).returncode
        == 0
    )


def dirty_paths(repo, task_ref):
    rows = []
    for line in git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all").split("\0"):
        if not line:
            continue
        path = line[3:].split(" -> ")[-1]
        if path.startswith(task_ref + "/") and Path(path).name in {
            "review.md",
            "review-gate.json",
        }:
            continue
        rows.append(path)
    return rows


def content_identity(repo, base_commit, commit, task_ref):
    rows = []
    for line in git(repo, "ls-tree", "-rz", commit).split("\0"):
        if not line:
            continue
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        if path.startswith(task_ref + "/") and Path(path).name in {
            "review.md",
            "review-gate.json",
        }:
            continue
        rows.append({"path": path, "mode": mode, "kind": kind, "oid": oid})
    return digest(
        {
            "algorithm": "guru-reviewed-content-1.0",
            "base_commit": base_commit,
            "entries": sorted(rows, key=lambda item: item["path"].encode()),
        }
    )


def validate_gate(package_root, repo, value, expected_exit=None):
    validate_json(value, package_root / "schemas/review-gate-4.0.schema.json", "gate")
    unsigned = {
        key: copy.deepcopy(item)
        for key, item in value.items()
        if key not in {"generated_at", "facts_sha256"}
    }
    if value["facts_sha256"] != digest(unsigned):
        raise CommandError(
            "stale_identity", "facts_sha256", "Rerecord current review facts.", 3
        )
    if expected_exit and value["typed_exit"] != expected_exit:
        raise CommandError(
            "stale_identity", "typed_exit", "Use current typed exit.", 3
        )
    current = git(repo, "rev-parse", "HEAD")
    if value["profile"] == "branch_review" and (
        git(repo, "rev-parse", value["base_ref"]) != value["base_head"]
    ):
        raise CommandError(
            "stale_identity", "base_ref", "Run a fresh review for the current base.", 3
        )
    if not ancestor(repo, value["base_head"], value["review_commit"]):
        raise CommandError(
            "stale_identity",
            "base_head",
            "Recorded base must precede reviewed task content.",
            3,
        )
    pair = value.get("integration_pair")
    if pair is not None:
        if not ancestor(repo, pair["old_base_head"], pair["new_base_head"]):
            raise CommandError(
                "stale_identity",
                "integration_pair",
                "Base continuity requires an ancestor delta.",
                3,
            )
        if pair["task_head"] != value["review_commit"]:
            raise CommandError(
                "stale_identity",
                "integration_pair.task_head",
                "Bind continuity to reviewed task content.",
                3,
            )
    if dirty_paths(repo, value["task_dir"]):
        raise CommandError(
            "stale_identity",
            "worktree",
            "Commit or remove all non-review overlays before branch review.",
            3,
        )
    if not ancestor(repo, value["review_commit"], current):
        raise CommandError(
            "stale_identity",
            "review_commit",
            "Review commit is not current history.",
            3,
        )
    if (
        content_identity(repo, value["base_head"], current, value["task_dir"])
        != value["reviewed_content_sha256"]
    ):
        raise CommandError(
            "stale_identity",
            "reviewed_content_sha256",
            "Run a fresh review for current task content.",
            3,
        )
    for finding in value["semantic_review"]["qualified_findings"]:
        if not ancestor(repo, finding["introduced_head"], value["review_commit"]):
            raise CommandError(
                "schema_mismatch",
                "qualified_findings",
                "Finding introduction must precede reviewed content.",
            )
        if finding["status"] == "resolved" and (
            not ancestor(repo, finding["introduced_head"], finding["fix_head"])
            or not ancestor(repo, finding["fix_head"], finding["closure_head"])
            or not ancestor(repo, finding["closure_head"], value["review_commit"])
        ):
            raise CommandError(
                "schema_mismatch",
                "qualified_findings",
                "Bind introduced, fix, closure, and review ancestry.",
            )
    return value


def validate_public_binding(package_root, repo, public, gate):
    profile = public.get("profile")
    schema = {
        "branch_review": "public-branch-review-input.schema.json",
        "base_continuity": "public-base-continuity-input.schema.json",
    }.get(profile)
    if schema is None:
        raise CommandError(
            "schema_mismatch", "input.profile", "Use one declared Branch Review profile."
        )
    validate_json(public, package_root / "schemas" / schema, "input")
    expected = {
        "task_dir": public["task_ref"],
        "mode": public["mode"],
        "profile": profile,
        "review_intent": public["review_intent"],
        "review_commit": public["branch_review_commit"],
    }
    for field, value in expected.items():
        if gate.get(field) != value:
            raise CommandError(
                "stale_identity", field, "Use the exact public input for this checkpoint.", 3
            )
    base_ref = public["new_base_head"] if profile == "base_continuity" else public["base_ref"]
    base_head = git(
        repo,
        "rev-parse",
        public["old_base_head"] if profile == "base_continuity" else base_ref,
    )
    if gate.get("base_ref") != base_ref or gate.get("base_head") != base_head:
        raise CommandError(
            "stale_identity", "base_ref", "Use the exact reviewed base identity.", 3
        )
    if profile == "base_continuity":
        expected_pair = {
            key: public[key]
            for key in (
                "task_head",
                "old_base_head",
                "new_base_head",
                "candidate_tree_sha256",
                "relevant_paths",
                "resume_target",
            )
        }
        if gate.get("integration_pair") != expected_pair:
            raise CommandError(
                "stale_identity",
                "integration_pair",
                "Use the exact reviewed base-continuity identity.",
                3,
            )
    return gate
