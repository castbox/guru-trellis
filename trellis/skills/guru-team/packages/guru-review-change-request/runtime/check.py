from __future__ import annotations

from common import check_result, invocation, live_issue_source, validation_receipt


def run(package_root, command, argv):
    envelope, target, prerequisites = invocation(package_root, argv)
    value = envelope["owner_result"]
    check_result(package_root, value, target, prerequisites)
    live_issue_source(envelope["owner_context"]["change_request"])
    return {"status": "passed", "skill_id": "guru-review-change-request",
            "typed_exit": value["typed_exit"], "target_identity_sha256": target["identity_sha256"],
            "target_content_sha256": target["content_sha256"],
            "linkage_sha256": value["evidence_linkage"]["linkage_sha256"],
            "facts_sha256": value["facts_sha256"], "validation_receipt": validation_receipt(value, envelope["transition"])}
