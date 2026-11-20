"""Check the Issue snapshot supplied by a read-only review owner."""

from __future__ import annotations

import subprocess

from .io import CommandError, decode_json


_FIELDS = "number,url,state,title,body,updatedAt,comments"
_FIELD_PATH = "owner_context.issue_snapshot"


def check_issue_snapshot(issue: dict, reviewed: dict) -> None:
    repo = issue["repo_ref"]
    number = issue["number"]
    url = f"https://github.com/{repo}/issues/{number}"
    if reviewed["number"] != number or reviewed["url"].casefold() != url.casefold():
        raise CommandError(
            "stale_identity", _FIELD_PATH,
            "Read the Issue selected by public_input.issue and review its current contents.", 3,
        )
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(number), "--repo", repo, "--json", _FIELDS],
            text=True, capture_output=True, check=False,
        )
    except FileNotFoundError as exc:
        raise CommandError(
            "stale_identity", _FIELD_PATH,
            "GitHub CLI is unavailable. Restore gh before reading and reviewing the selected Issue.", 3,
        ) from exc
    if result.returncode:
        raise CommandError(
            "stale_identity", _FIELD_PATH,
            f"gh issue view exited {result.returncode}. Check GitHub CLI authentication and "
            "repository access, then read and review the selected Issue.", 3,
        )
    live = decode_json(
        result.stdout, _FIELD_PATH,
        syntax_remediation="gh issue view returned invalid JSON. Read the selected Issue again.",
    )
    if live != reviewed:
        raise CommandError(
            "stale_identity", _FIELD_PATH,
            "The Issue snapshot changed. Reread the Issue and discussion, reassess affected "
            "conclusions, and invoke the same standalone review again.", 3,
        )
