from __future__ import annotations

import copy

from common import build_result, digest, invocation, linkage, validate_owner
from runtime.io import CommandError


def run(package_root, command, argv):
    envelope, target, prerequisites = invocation(package_root, argv)
    authored = copy.deepcopy(envelope["owner_result"])
    semantic = authored.get("semantic_review")
    if (not isinstance(semantic, dict)
            or not isinstance(semantic.get("ai_review_gate"), dict)
            or not isinstance(semantic.get("findings"), list)
            or not isinstance(semantic.get("scope_conclusion"), dict)):
        raise CommandError("schema_mismatch", "semantic_review", "Provide the completed AI gate, findings and scope conclusion.")
    gate = semantic["ai_review_gate"]
    derived = {
        "reviewed_linkage_sha256": linkage(target, prerequisites)["linkage_sha256"],
        "scope_conclusion_sha256": digest(semantic["scope_conclusion"]),
        "findings_count": len(semantic["findings"]),
    }
    for key, value in derived.items():
        if key in gate and (type(gate[key]) is not type(value) or gate[key] != value):
            raise CommandError("schema_mismatch", "semantic_review.ai_review_gate." + key,
                               "Use the current derived binding or omit it for recording.")
        gate[key] = value
    return validate_owner(package_root, build_result(authored, target, prerequisites))
