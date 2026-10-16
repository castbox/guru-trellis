"""Bounded Plan2 committed-plan source bridge owned by TaskCommit.

No public state or gate is created. The reviewed write set proves that missing
HEAD paths are relocations of actual committed blobs, not new business work.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
from pathlib import Path

from common import git, load, parse, root
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle import LifecycleContractError

NAMES = ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl")


def source_path(repo, key):
    return repo / ".trellis/.runtime/guru-team/task-commit-sources" / key["delivery_id"] / "source.json"


def committed_file(repo, commit, path):
    blob = subprocess.run(["git", "show", commit + ":" + path], cwd=repo, capture_output=True)
    entry = git(repo, "ls-tree", commit, "--", path, check=False).stdout.strip().split()
    if blob.returncode or len(entry) < 3 or entry[0] not in {"100644", "100755"}:
        raise CommandError("stale_identity", "planning_sources", "Read each actual regular committed planning blob.", 3)
    return blob.stdout, int(entry[0], 8) & 0o777


def project_planning_links(repo, source, target, content):
    """Rebase the reviewed, bounded inline Markdown destinations only.

    This is byte-preserving outside destinations, not a Markdown normalizer.
    Unsupported relative syntax returns to the migration semantic owner.
    """
    if not source.endswith(".md"):
        return content
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CommandError("stale_identity", "planning_projection", "Review UTF-8 planning before projecting links.", 3) from exc
    source_dir = (repo / source).parent
    target_dir = target.parent

    def rebase(value):
        if not value or value.startswith(("#", "/")) or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
            return value
        if re.search(r"[\s\\()]", value):
            raise CommandError("stale_identity", "planning_projection", "Return unsupported relative link syntax to the original planning migration owner.", 3)
        parts = re.split(r"([?#].*)", value, maxsplit=1)
        original = (source_dir / parts[0]).resolve()
        if not original.is_file():
            raise CommandError("stale_identity", "planning_projection", "Restore or review the actual original relative link target before migration.", 3)
        projected = Path(os.path.relpath(original, target_dir)).as_posix() + "".join(parts[1:])
        return projected

    # Supported ordinary inline links/images, with optional angle brackets/title.
    links = re.compile(r'!?\[[^\]\n]*\]\((?:<(?P<angled>[^>\n]*)>|(?P<plain>[^\s()]*))(?:[ \t]+(?:"[^"\n]*"|\'[^\'\n]*\'))?\)')
    output = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            output.append(line)
            continue
        if fence is not None:
            output.append(line)
            continue
        if re.match(r"^[ \t]{0,3}\[[^\]]+\]:", line):
            raise CommandError("stale_identity", "planning_projection", "Review reference-definition links through the original planning migration owner.", 3)
        def prose(fragment):
            def replace(match):
                field = "angled" if match.group("angled") is not None else "plain"
                projected = rebase(match.group(field))
                start, end = match.span(field)
                return match.string[match.start():start] + projected + match.string[end:match.end()]
            spans = [match.span() for match in links.finditer(fragment)]
            if any(not any(start <= marker.start() < end for start, end in spans)
                   for marker in re.finditer(r"\]\(", fragment)):
                raise CommandError("stale_identity", "planning_projection", "Return unsupported inline link syntax to the original planning migration owner.", 3)
            return links.sub(replace, fragment)

        # Preserve each complete inline code span including its delimiters.
        cursor = 0
        for code in re.finditer(r"(?P<ticks>`+).*?(?P=ticks)", line):
            output.append(prose(line[cursor:code.start()]))
            output.append(code.group(0))
            cursor = code.end()
        output.append(prose(line[cursor:]))
    return "".join(output).encode("utf-8")


def expected_committed(repo, commit, source, path, planning_projection=None):
    content, mode = committed_file(repo, commit, source)
    if planning_projection == "markdown_relative_links_v1":
        content = project_planning_links(repo, source, path, content)
    return content, mode


def matches_committed(repo, commit, source, path, planning_projection=None):
    content, mode = expected_committed(repo, commit, source, path, planning_projection)
    return path.is_file() and not path.is_symlink() and path.read_bytes() == content and (path.stat().st_mode & 0o111) == (mode & 0o111)


def read_source(package, repo, key):
    path = source_path(repo, key)
    if not path.is_file():
        return None
    value = load(repo, package, str(path), "planning_source")
    validate_json(value, package / "schemas/delivery-planning-source-1.0.schema.json", "planning_source")
    if value["delivery_key"] != key or git(repo, "merge-base", "--is-ancestor", value["source_commit"], "HEAD", check=False).returncode:
        raise CommandError("stale_identity", "planning_source", "Restore the reviewed original committed source association.", 3)
    return value


def _run(package, command, argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--input", required=True)
    parser.add_argument("--owner-result", required=True)
    parser.add_argument("--preview", action="store_true")
    args = parse(parser, argv)
    repo = root(package, args.root)
    public = load(repo, package, args.input, "input")
    review = load(repo, package, args.owner_result, "owner_result")
    validate_json(public, package / "schemas/delivery-source-migration-input-1.0.schema.json", "input")
    validate_json(review, package / "schemas/delivery-commit-review-1.0.schema.json", "owner_result")
    if review["status"] != "passed":
        raise CommandError("stale_identity", "owner_result", "The original TaskCommit owner must review the exact Plan2 source mapping.", 3)
    projection = DeliveryProjection(repo, public["task_ref"])
    try:
        delivery = projection.resolve(public["delivery_key"])
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    plan = load(repo, package, public["plan_file"], "plan_file")
    rows = [row for row in plan.get("tasks", []) if row.get("workspace") == public["workspace"] and row.get("task_ref") == public["task_ref"]]
    if plan.get("schema_version") != "2.0" or len(rows) != 1 or rows[0].get("disposition") not in {"convert_active", "convert_archive"}:
        raise CommandError("stale_identity", "plan_file", "Use the actual reviewed Plan2 conversion of this Task.", 3)
    projected = projection._call(projection.api.delivery_schema.parse_task_v2, rows[0]["record"])
    projection._call(projection.api.delivery_operations.get_gate_applicability, projected, public["delivery_key"])
    planned_delivery = next(row for row in projected["deliveries"] if row["id"] == public["delivery_key"]["delivery_id"])
    if planned_delivery["planning_root"] != delivery["planning_root"] or projected["accepted_scope"] != projection.read_record()["accepted_scope"]:
        raise CommandError("stale_identity", "plan_file.record", "Review the same scope and Delivery planning mapping.", 3)
    if git(repo, "merge-base", "--is-ancestor", public["source_commit"], "HEAD", check=False).returncode:
        raise CommandError("stale_identity", "source_commit", "Use the original committed candidate ancestor.", 3)
    missing = False
    for name in NAMES:
        target = projection.planning_directory(public["delivery_key"]) / name
        relative = target.relative_to(repo).as_posix()
        source = public["planning_sources"][name]
        content, mode = expected_committed(repo, public["source_commit"], source, target, public.get("planning_projection"))
        writes = [row for row in plan.get("files", []) if row.get("target") == {"kind": "project", "workspace": public["workspace"], "path": relative}]
        if (len(writes) != 1 or writes[0].get("owner") != "artifact" or writes[0].get("action") != "write"
                or base64.b64decode(writes[0].get("target_content_base64", "")) != content
                or (writes[0].get("target_mode", 0) & 0o111) != (mode & 0o111)
                or not matches_committed(repo, public["source_commit"], source, target, public.get("planning_projection"))):
            raise CommandError("stale_identity", "plan_file.files", "Match all five actual Plan2 writes to committed source bytes/modes.", 3)
        missing |= git(repo, "cat-file", "-e", "HEAD:" + relative, check=False).returncode != 0
    value = {"schema_version": "1.0", "delivery_key": public["delivery_key"], "source_commit": public["source_commit"], "planning_sources": public["planning_sources"]}
    if "planning_projection" in public:
        value["planning_projection"] = public["planning_projection"]
    path = source_path(repo, public["delivery_key"])
    if args.preview:
        return {"status": "preview", "write_paths": [path.relative_to(repo).as_posix()] if missing else []}
    if missing:
        existing = read_source(package, repo, public["delivery_key"])
        if existing is not None and existing != value:
            raise CommandError("stale_identity", "planning_source", "Recover the original same-plan source association.", 3)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    return {"status": "source_bound" if missing else "direct_committed", "source_binding": path.relative_to(repo).as_posix() if missing else None}


def run(package, command, argv):
    try:
        return _run(package, command, argv)
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
