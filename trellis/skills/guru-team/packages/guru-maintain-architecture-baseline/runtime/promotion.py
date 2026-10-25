"""Objective candidate and promotion binding; the Architecture owner writes files."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from runtime.io import CommandError
from runtime.reviewed_content import (
    REVIEWED_CONTENT_ALGORITHM,
    ReviewedContentError,
    _blob_oid,
    _tree_entries,
    _validate_gitlinks,
    _worktree_overlays,
    reviewed_content_identity,
    reviewed_content_metadata_path,
)


def _error(field: str, remediation: str) -> None:
    raise CommandError("stale_identity", field, remediation, 3)


def _git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True)
    if result.returncode:
        _error("before_authority", "Reread the available exact Git authority and candidate.")
    return result.stdout


def _path(repo: Path, locator: str) -> Path:
    path = Path(locator)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        _error("promotion_targets", "Use repository-relative target files.")
    target = repo / path
    if target.is_symlink() or (target.exists() and not target.is_file()):
        _error("promotion_targets", "Read the regular target file before continuing.")
    return target


def capture_candidate(repo: Path) -> dict:
    try:
        identity = reviewed_content_identity(repo)
    except ReviewedContentError as exc:
        _error("candidate", str(exc))
    return {"head": _git(repo, "rev-parse", "HEAD").decode().strip(),
            "content_identity": "sha256:" + identity["sha256"]}


def check_before_authority(repo: Path, public: dict) -> None:
    authority = public["before_authority"]
    revision = authority["git_revision"]
    if _git(repo, "rev-parse", revision + "^{commit}").decode().strip() != revision:
        _error("before_authority.git_revision", "Use the exact available authority commit.")
    locators = {authority[field] for field in
                ("baseline_locator", "constitution_locator", "change_contract_locator")}
    absent = set(authority.get("absent_locators", []))
    if not absent <= locators:
        _error("before_authority.absent_locators", "Declare absence only for the three authority locators.")
    for locator in locators:
        _path(repo, locator)
        entries = _git(repo, "ls-tree", "-z", revision, "--", locator).decode().split("\0")
        present = any(row.split("\t", 1)[-1] == Path(locator).as_posix() for row in entries)
        if locator in absent:
            if present:
                _error("before_authority.absent_locators", "Reread actual presence at the fixed before revision.")
        else:
            if not present or _git(repo, "cat-file", "-t", revision + ":" + locator).strip() != b"blob":
                _error("before_authority", "Read each existing before authority file or declare its actual absence.")
            _git(repo, "show", revision + ":" + locator)
    committed_range = public.get("committed_range")
    if committed_range and (revision != committed_range["base_head"]
                            or _git(repo, "rev-parse", "HEAD").decode().strip() != committed_range["review_head"]):
        _error("before_authority", "Bind committed review to its fixed before authority and current HEAD.")


def target_states(repo: Path, targets: list[dict]) -> dict[str, str]:
    """Read the same operation's targets without writing or selecting a route."""
    states = {}
    for target in targets:
        locator = target["locator"]
        if locator in states or reviewed_content_metadata_path(locator):
            _error("promotion_targets", "Declare each reviewed Architecture target once, outside runtime metadata.")
        path = _path(repo, locator)
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == target["content"]:
            states[locator] = "completed"
        elif current == target["before_content"]:
            states[locator] = "pending"
        else:
            states[locator] = "conflict"
    return states


def _before_candidate(repo: Path, targets: list[dict]) -> dict:
    """Reconstruct the reviewed snapshot with shared reviewed-content primitives."""
    try:
        entries = _tree_entries(repo, "HEAD")
        gitlinks = {path: row["oid"] for path, row in entries.items() if row["mode"] == "160000"}
        gitlink_overlays = {}
        for overlay in _worktree_overlays(repo):
            locator = overlay["path"]
            if overlay.get("deleted"):
                entries.pop(locator, None)
            else:
                entries[locator] = {key: overlay[key] for key in ("path", "mode", "oid")}
                if overlay["mode"] == "160000":
                    gitlink_overlays[locator] = overlay
        _validate_gitlinks(repo, entries, gitlinks, gitlink_overlays)
        for target in targets:
            locator, content = target["locator"], target["before_content"]
            if content is None:
                entries.pop(locator, None)
            else:
                # Architecture promotion writes regular text while retaining its mode.
                mode = entries.get(locator, {}).get("mode", "100644")
                entries[locator] = {"path": locator, "mode": mode,
                                    "oid": _blob_oid(repo, content.encode("utf-8"))}
        payload = {"algorithm": REVIEWED_CONTENT_ALGORITHM,
                   "entries": sorted(entries.values(), key=lambda row: row["path"].encode("utf-8"))}
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                           separators=(",", ":")).encode()).hexdigest()
        return {"head": _git(repo, "rev-parse", "HEAD").decode().strip(),
                "content_identity": "sha256:" + digest}
    except ReviewedContentError as exc:
        _error("candidate", str(exc))


def check_current_candidate(repo: Path, public: dict) -> None:
    check_before_authority(repo, public)
    if capture_candidate(repo) != public["candidate"]:
        _error("candidate", "Reassess the actual complete tracked/untracked candidate.")


def check_promotion(repo: Path, public: dict, owner: dict) -> None:
    check_before_authority(repo, public)
    targets = owner.get("promotion_targets", [])
    review = owner.get("review", {})
    if (review.get("status") != "reviewed" or review.get("independent") is not True
            or review.get("candidate") != public["candidate"]
            or review.get("before_authority") != public["before_authority"]):
        _error("owner_result.review", "Use the actual independent candidate and proposed-content assessment.")
    if not targets:
        _error("owner_result.promotion_targets", "Recover the original reviewed target contents before continuing.")
    states = target_states(repo, targets)
    if any(state != "completed" for state in states.values()):
        _error("owner_result.promotion_targets", "Read back this operation's completed, pending and conflicting files; complete only unconflicted pending writes through the original owner.")
    if _before_candidate(repo, targets) != public["candidate"]:
        _error("candidate", "The actual delta exceeds the reviewed candidate or proposed target contents; return to the affected Architecture assessment.")
    baseline = public["baseline"]
    if (public["expected_current_identity"] != baseline["identity"]
            or public["current_identity"] != baseline["identity"]):
        _error("expected_current_identity", "Reread the actual expected-current Architecture authority.")
    if owner.get("baseline_identity") != baseline["identity"]:
        baseline_writes = [target for target in targets
                           if target["locator"] == baseline["locator"]]
        if (len(baseline_writes) != 1
                or baseline_writes[0]["before_content"] is None
                or baseline_writes[0]["content"] is None
                or baseline_writes[0]["before_content"] == baseline_writes[0]["content"]):
            _error("owner_result.baseline_identity", "A changed after identity requires this operation's actual reviewed baseline target write; leaf-only promotion retains its before identity.")
    if owner.get("post_candidate") != capture_candidate(repo):
        _error("owner_result.post_candidate", "Bind the result to the actual complete promoted candidate.")
    if owner.get("postwrite_applicability", {}).get("status") != "applicable":
        _error("owner_result.postwrite_applicability", "The original owner must assess actual postwrite applicability before projection.")
