"""Factual prerequisites for the disposable qualification semantic fixture.

This fixture uses the installed public Task/Scope/Delivery model. Its seeded
branch/resource association is outside the qualifier boundary and is not
Creation, native context or caller-continuation evidence.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.identity import resolve_task_id
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


def stage_delivery(root: Path) -> tuple[str, dict, Path]:
    root = root.resolve()
    script = root / ".trellis/scripts/task.py"
    if not script.is_file():
        raise ValueError("Qualification factual fixture requires the complete installed Task/Delivery provider.")
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith(("TRELLIS_", "CODEX_", "CLAUDE_", "CURSOR_", "GIT_"))}
    def run(args, value=None):
        result = subprocess.run(args, cwd=root, input=value, text=True, capture_output=True, env=environment)
        if result.returncode:
            raise ValueError("Qualification factual fixture command failed: " + result.stdout + result.stderr)
        return result.stdout.strip()
    if subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=root, capture_output=True).returncode:
        run(["git", "add", "."])
        from adapters.eval.fixture_io import commit_qualification_owner_fixture
        commit_qualification_owner_fixture(root)
    base = run(["git", "branch", "--show-current"])
    run(["git", "switch", "-c", "codex/qualification-eval"])
    run([sys.executable, str(script), "create", "Qualification semantic fixture", "--description", "Current identity prerequisite only",
         "--slug", "qualification-eval", "--task-id", "qualification-eval", "--schema-version", "2.0",
         "--source-json", '{"kind":"no_issue"}', "--base-branch", base, "--no-start"])
    artifact = resolve_task_id(root, "qualification-eval")
    ref = artifact.task_ref
    repository = inspect_repository(root)
    task_key = TaskLifecycleKey(artifact.task_id, artifact.lifecycle_generation)
    BranchBindingStore(repository).establish(task_key, "codex/qualification-eval")
    ResourceLedgerStore(repository).establish_current(task_key, binding_revision=0,
        branch_name="codex/qualification-eval", branch_ownership="caller_owned", worktree_ownership="not_applicable")
    task = root / ref
    (task / "prd.md").write_text("# Qualification factual scope\n\nAC01: qualify the current candidate.\n")
    projection = DeliveryProjection(root, ref)
    authority = authority_ref(task / "prd.md", root)
    projection.scope(authority)
    # Stable identity across independent eval repositories preserves the
    # original five-invocation prompt contract. This is a factual public-model
    # fixture, not evidence for Guru Creation or a semantic owner result.
    key = {"task_id": artifact.task_id, "lifecycle_generation": artifact.lifecycle_generation,
           "delivery_id": str(uuid.uuid5(uuid.NAMESPACE_URL, "guru-qualification-semantic-fixture"))}
    projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": key,
                      "owner_role": "creation", "owner_id": projection.declaration()["owners"]["creation"],
                      "scope_ref": {"authority": authority, "anchors": ["AC01"]}, "profile": "pull_request"})
    return ref, key, projection.planning_directory(key)
