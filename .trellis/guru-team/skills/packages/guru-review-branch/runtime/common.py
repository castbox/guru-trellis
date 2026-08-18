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
from runtime.reviewed_content import (
    REVIEWED_CONTENT_ALGORITHM,
    ReviewedContentError,
    reviewed_content_metadata_path,
    reviewed_content_identity,
)
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


def dirty_paths(repo, _task_ref):
    process = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise CommandError(
            "stale_identity",
            "repository",
            process.stderr.decode("utf-8", "replace").strip()
            or "Repair Git state.",
            3,
        )

    fields = process.stdout.split(b"\0")
    rows = []
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if not field:
            continue
        if len(field) < 4:
            raise CommandError(
                "stale_identity",
                "worktree",
                "Git returned an invalid porcelain status record.",
                3,
            )
        try:
            status_text = field[:2].decode("ascii", "strict")
            path = field[3:].decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            raise CommandError(
                "stale_identity",
                "worktree",
                "Dirty paths must be valid UTF-8.",
                3,
            ) from exc

        related_path = None
        relation_kinds = {item for item in status_text if item in {"R", "C"}}
        if len(relation_kinds) > 1 or (
            relation_kinds and (index >= len(fields) or not fields[index])
        ):
            raise CommandError(
                "stale_identity",
                "worktree",
                "Git returned an invalid rename/copy status record.",
                3,
            )
        if relation_kinds:
            try:
                related_path = fields[index].decode("utf-8", "strict")
            except UnicodeDecodeError as exc:
                raise CommandError(
                    "stale_identity",
                    "worktree",
                    "Dirty paths must be valid UTF-8.",
                    3,
                ) from exc
            index += 1

        included_paths = [path]
        if relation_kinds == {"R"} and related_path is not None:
            included_paths.append(related_path)
        rows.extend(
            candidate
            for candidate in included_paths
            if not reviewed_content_metadata_path(candidate)
        )
    return rows


def content_identity(repo, commit):
    try:
        return reviewed_content_identity(repo, commit, include_worktree=False)["sha256"]
    except ReviewedContentError as exc:
        raise CommandError(
            "stale_identity",
            "reviewed_content_sha256",
            str(exc),
            3,
        ) from exc


def validate_gate(package_root, repo, value, expected_exit=None):
    if (
        value.get("schema_version") != "6.0"
        or value.get("reviewed_content_algorithm") != REVIEWED_CONTENT_ALGORITHM
    ):
        raise CommandError(
            "stale_identity",
            "checkpoint",
            "Run a fresh Branch Review for the current reviewed-content contract.",
            3,
        )
    validate_json(value, package_root / "schemas/review-gate-6.0.schema.json", "gate")
    classifications = value.get("candidate_classifications")
    refs = [
        item.get("candidate_ref")
        for item in classifications
        if isinstance(item, dict)
    ] if isinstance(classifications, list) else []
    if not refs or len(refs) != len(classifications) or len(set(refs)) != len(refs):
        raise CommandError(
            "schema_mismatch",
            "candidate_classifications",
            "Record one complete non-empty classification for every unique current candidate.",
        )
    known = set(refs)
    linked = []
    for key in (
        "qualified_findings",
        "scope_proposals",
        "observations",
        "followup_candidates",
        "rejected_candidates",
    ):
        linked.extend(
            item.get("candidate_ref")
            for item in value["semantic_review"].get(key, [])
            if isinstance(item, dict)
        )
    if any(not ref or ref not in known for ref in linked):
        raise CommandError(
            "schema_mismatch",
            "candidate_classifications",
            "Every Branch Review candidate disposition must bind one current classified candidate.",
        )
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
        content_identity(repo, current)
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
