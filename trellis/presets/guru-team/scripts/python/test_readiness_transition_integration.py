from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import verify_installed_phase0_transcript as transcript
from test_discovery_stdin_integration import run_preset_install


SOURCE = Path(__file__).resolve().parents[5]


def snapshot(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


def producers(installed: Path, chain: Path):
    root, env = transcript.stage_transcript_owner_repo(installed, chain)
    sync, _ = transcript.invoke_public(root, env, "guru-sync-base", {
        "schema_version": "1.0", "public_input": {
            "source_exit": "start", "mode": "workflow", "repo_root": ".",
            "base_branch": "main", "route": "repo_change",
        },
    }, "synced")
    public, _ = transcript.project_installed_output(root, "guru-sync-base", "synced", sync)
    discovery_owner, _, public = transcript.checked_context_owner_for_issue(root, env, public, sync["transition"])
    discovery, _ = transcript.invoke_public(root, env, "guru-discover-change-context", {
        "schema_version": "1.0", "public_input": public, "transition": sync["transition"],
        "owner_context": {}, "owner_result": discovery_owner,
    }, "context_ready")
    clarity_owner, _ = transcript.clarification_owner_for_issue(root, env, discovery["transition"], discovery["duplicate_snapshot"])
    clarity, _ = transcript.invoke_public(root, env, "guru-clarify-requirements", {
        "schema_version": "1.0", "public_input": {
            "profile": "initial_change_request", "source_exit": "context_ready", "mode": "workflow",
            "target_locator": discovery["transition"]["target_locator"],
            "continuation_id": discovery["transition"]["continuation_id"],
            "duplicate_snapshot": discovery["duplicate_snapshot"],
        }, "transition": discovery["transition"], "owner_context": {}, "owner_result": clarity_owner,
    }, "clear")
    issue = transcript.live_issue(root, env)
    source = {
        "kind": "issue", "repo": "example/guru-extension", "number": 145, "url": issue["url"],
        "title": issue["title"], "body": issue["body"], "updated_at": issue["updatedAt"], "selected_comments": [],
    }
    source_path = chain / "source.json"
    source_path.write_text(json.dumps(source), encoding="utf-8")
    wording_path = chain / "wording-source.json"
    wording_path.write_text(json.dumps(transcript.wording_change_request_source(issue)), encoding="utf-8")
    wording_owner, checked = transcript.wording_owner_for_issue(root, env, wording_path)
    wording, _ = transcript.invoke_public(root, env, "guru-review-contract-wording", {
        "schema_version": "1.0", "public_input": {
            "profile": "change_request", "source_exit": "clear", "mode": "workflow",
            "target_locator": clarity["transition"]["target_locator"],
            "continuation_id": clarity["transition"]["continuation_id"],
        }, "transition": clarity["transition"], "owner_context": {"change_request": source},
        "owner_result": wording_owner, "validation_receipt": checked["validation_receipt"],
    }, "pass")
    return root, env, source, source_path, discovery, clarity, wording, clarity_owner, wording_owner


class InstalledReadinessTransitionTests(unittest.TestCase):
    def test_real_producer_chain_initial_install_and_reapply(self):
        with tempfile.TemporaryDirectory(prefix="guru-386-installed-") as temp:
            work = Path(temp)
            installed = work / "installed"
            (installed / ".trellis").mkdir(parents=True)
            shutil.copy2(SOURCE / "trellis/workflows/guru-team/workflow.md", installed / ".trellis/workflow.md")
            shutil.copytree(SOURCE / ".trellis/scripts", installed / ".trellis/scripts", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            for phase in ("initial", "reapply"):
                with self.subTest(phase=phase):
                    applied = run_preset_install(installed, all_platforms=True)
                    self.assertEqual(applied.returncode, 0, applied.stdout[-5000:] + applied.stderr[-2000:])
                    self.assertEqual(list(installed.rglob("*.bak")) + list(installed.rglob("*.new")), [])
                    self.check_chain(installed, work / phase)

    def check_chain(self, installed: Path, chain: Path):
        root, env, source, source_path, discovery, clarity, wording, clarity_owner, wording_owner = producers(installed, chain)
        before = snapshot(root)
        siblings = {str(p.relative_to(chain)) for p in chain.rglob("*")}
        worktrees = transcript.run(["git", "worktree", "list", "--porcelain"], cwd=root).stdout
        transitions = (wording["transition"], clarity["transition"], discovery["transition"])
        exits = ("ready", "review_wording", "clarify_requirements")
        for transition, exit_id in zip(transitions, exits):
            recorded, checked = transcript.checked_readiness_owner_for_issue(root, env, transition, source_path, exit_id)
            envelope = transcript.readiness_invocation(transition, source, recorded)
            envelope["validation_receipt"] = checked["validation_receipt"]
            counts = transcript.operation_counts(env)
            actual, _ = transcript.invoke_public(root, env, "guru-review-change-request", envelope, exit_id)
            self.assertEqual(transcript.operation_delta(counts, transcript.operation_counts(env)), {})
            if exit_id == "ready":
                self.assertEqual(actual["profile"], "execute_reviewed_plan")
                self.assertEqual(actual["transition"]["clarity"], clarity["transition"]["clarity"])
                self.assertEqual(actual["transition"]["target_content_sha256"], wording["transition"]["target_content_sha256"])
                self.assertNotEqual(actual["transition"]["clarity"]["content_sha256"], actual["transition"]["target_content_sha256"])
                self.assertNotIn("payload_sha256", recorded["prerequisites"]["clarity"])
                self.assertNotIn("payload_sha256", recorded["prerequisites"]["wording"])
                ready_envelope = {key: value for key, value in envelope.items() if key != "validation_receipt"}
            else:
                self.assertEqual(actual["transition"], transition)
        self.assertEqual(snapshot(root), before)
        self.assertEqual({str(p.relative_to(chain)) for p in chain.rglob("*")}, siblings)
        self.assertEqual(transcript.run(["git", "worktree", "list", "--porcelain"], cwd=root).stdout, worktrees)
        self.assertFalse((root / ".trellis/tasks").exists())
        self.assertFalse((root / ".trellis/workspace").exists())
        self.assertEqual(list(root.rglob("__pycache__")) + list(root.rglob("*.pyc")), [])
        # The real remote fixture advances content, without altering any prior output.
        for field in ("title", "body"):
            authority_path = chain / f"issue-{field}.txt"
            old = authority_path.read_text()
            authority_path.write_text(old + " changed")
            try:
                result = self.call(root, env, "check-change-request-review.sh", ready_envelope)
                self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)["code"], "stale_identity")
            finally:
                authority_path.write_text(old)
        authored = transcript.readiness_owner_for_issue(root, env, {**wording["transition"], "readiness_source": source})
        legacy = copy.deepcopy(authored)
        legacy["prerequisite_payloads"] = {"clarity": clarity_owner, "wording": wording_owner}
        legacy_envelope = transcript.readiness_invocation(wording["transition"], source, legacy)
        rejected = self.call(root, env, "record-change-request-review.sh", legacy_envelope)
        self.assertEqual(rejected.returncode, 2, rejected.stdout + rejected.stderr)
        self.assertEqual(json.loads(rejected.stdout)["code"], "schema_mismatch")
        for missing in ("transition", "public_input", "owner_result"):
            invalid = copy.deepcopy(ready_envelope)
            invalid.pop(missing)
            rejected = self.call(root, env, "check-change-request-review.sh", invalid)
            self.assertEqual(rejected.returncode, 2, rejected.stdout + rejected.stderr)
            self.assertEqual(json.loads(rejected.stdout)["code"], "schema_mismatch")
        transcript.assert_forbidden_runtime_absent(root)
        self.assertEqual(snapshot(root), before)

    def call(self, root, env, command, envelope):
        wrapper = root / ".trellis/guru-team/skills/packages/guru-review-change-request/scripts" / command
        return transcript.run([wrapper, "--invocation", "-"], cwd=root, env=env, stdin=envelope, check=False)


if __name__ == "__main__":
    unittest.main()
