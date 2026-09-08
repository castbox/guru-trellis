from __future__ import annotations

from common import build_result, invocation, validate_owner


def run(package_root, command, argv):
    envelope, target, prerequisites = invocation(package_root, argv)
    return validate_owner(package_root, build_result(envelope["owner_result"], target, prerequisites))
