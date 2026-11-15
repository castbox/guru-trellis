"""Validate a bounded read-only review; the Agent owns every conclusion."""
from __future__ import annotations

import json
import subprocess

from runtime.io import CommandError
from runtime.schema import validate_json


def execute(package, envelope):
    validate_json(envelope, package.parents[1] / "consumers/workflow/stage0/invocations/semantic-owner-3.0.schema.json", "invocation")
    public, owner = envelope["public_input"], envelope["owner_result"]
    validate_json(public, package / "schemas/public-standalone-wording-review-input-1.0.schema.json", "public_input")
    validate_json(owner, package / "schemas/wording-review-owner-1.0.schema.json", "owner_result")
    if owner["typed_exit"] == "blocked":
        return {"exit_id": "blocked"}
    target = public["target"]
    if target["kind"] == "issue":
        source = envelope["owner_context"].get("change_request")
        result = subprocess.run(
            ["gh", "issue", "view", str(target["number"]), "--repo", target["repo_ref"],
             "--json", "number,title,body,updatedAt"],
            text=True, capture_output=True, check=False,
        )
        if result.returncode:
            raise CommandError("stale_identity", "owner_context.change_request", "Read the selected Issue before completing its bounded review.", 3)
        try:
            live = json.loads(result.stdout)
        except ValueError as exc:
            raise CommandError("invalid_json", "owner_context.change_request", "Reread the selected Issue.") from exc
        if not isinstance(source, dict) or source.get("repo") != target["repo_ref"] or any(
            source.get(key) != live.get(remote) for key, remote in
            (("number", "number"), ("title", "title"), ("body", "body"), ("updated_at", "updatedAt"))
        ):
            raise CommandError("stale_identity", "owner_context.change_request", "Reread the current selected Issue and reassess affected wording.", 3)
    output = {"exit_id": "reviewed", "conclusion": owner["conclusion"], "findings": owner["findings"]}
    validate_json(output, package / "schemas/public-reviewed-output-1.0.schema.json", "stdout")
    return output
