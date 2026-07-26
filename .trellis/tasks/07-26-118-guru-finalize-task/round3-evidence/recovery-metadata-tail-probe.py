#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


REPO = Path(__file__).resolve().parents[4]
RUNTIME = REPO / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"


def load_runtime():
    spec = importlib.util.spec_from_file_location("gtt_round3_repro", RUNTIME)
    if spec is None or spec.loader is None:
        raise RuntimeError("runtime import spec is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    runtime = load_runtime()
    reviewed_head = "a" * 40
    evidence_head = "b" * 40
    plan_ref = "closeout-plan:" + "c" * 64
    results: dict[str, object] = {}

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        task_dir = root / ".trellis/tasks/07-26-normal-recovery"
        task_dir.mkdir(parents=True)
        task_ref = task_dir.relative_to(root).as_posix()
        artifact = task_dir / runtime.MARKETPLACE_VERIFICATION_ARTIFACT
        payload = {
            "public_input": {
                "mode": "workflow",
                "task_ref": task_ref,
                "plan_ref": plan_ref,
                "reviewed_head": reviewed_head,
            },
            "typed_exit": "verified",
            "mode": "workflow",
            "identity": {
                "verification_ref": "extension-verification:current",
            },
            "repository": {
                "task_worktree_sha256": "worktree-current",
                "remote": "origin",
                "ref": "refs/heads/feat/118",
                "remote_head": reviewed_head,
            },
        }
        runtime.write_json(artifact, payload)

        for label, current in (
            ("reviewed_content_head_control", reviewed_head),
            ("normal_evidence_metadata_tail", evidence_head),
        ):
            remote_proc = SimpleNamespace(
                returncode=0,
                stdout=f"{reviewed_head}\trefs/heads/feat/118\n",
                stderr="",
            )
            with (
                mock.patch.object(runtime, "load_config", return_value={}),
                mock.patch.object(
                    runtime,
                    "extension_verification_payload_errors",
                    return_value=[],
                ),
                mock.patch.object(
                    runtime,
                    "extension_verification_task_identity",
                    return_value=task_dir,
                ),
                mock.patch.object(
                    runtime,
                    "extension_verification_task_worktree_sha256",
                    return_value="worktree-current",
                ),
                mock.patch.object(runtime, "run", return_value=remote_proc),
                mock.patch.object(runtime, "current_head", return_value=current),
            ):
                diagnostics = {
                    "patched_current_head": runtime.current_head(root),
                    "owner_reviewed_head": payload["public_input"]["reviewed_head"],
                    "resolved_remote_head": runtime.extension_verification_resolved_remote_head(
                        remote_proc,
                        "refs/heads/feat/118",
                    ),
                }
                try:
                    checked = runtime.finalization_current_verification_owner_result(
                        root,
                        task_dir,
                        task_ref=task_ref,
                        plan_ref=plan_ref,
                        reviewed_head=reviewed_head,
                    )
                except runtime.WorkflowError as exc:
                    results[label] = {
                        **diagnostics,
                        "status": "blocked",
                        "message": str(exc),
                        "errors": exc.payload.get("errors", []),
                    }
                else:
                    results[label] = {
                        **diagnostics,
                        "status": "passed",
                        "typed_exit": checked[1]["typed_exit"] if checked else None,
                    }

    print(json.dumps(results, indent=2, sort_keys=True))
    if results["reviewed_content_head_control"]["status"] != "passed":
        return 2
    if results["normal_evidence_metadata_tail"]["status"] != "blocked":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
