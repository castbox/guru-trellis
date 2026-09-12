from __future__ import annotations

import copy
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
from test_discovery_stdin_integration import file_snapshot, run_preset_install

SOURCE = Path(__file__).resolve().parents[5]


class WordingStdinIntegrationTests(unittest.TestCase):
    def test_installed_stdin_chain_and_reapply(self):
        with tempfile.TemporaryDirectory(prefix="guru-388-installed-") as tmp:
            work = Path(tmp)
            installed = work / "installed"
            (installed / ".trellis").mkdir(parents=True)
            shutil.copy2(SOURCE / "trellis/workflows/guru-team/workflow.md", installed / ".trellis/workflow.md")
            shutil.copytree(SOURCE / ".trellis/scripts", installed / ".trellis/scripts", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            for phase in ("initial", "reapply"):
                with self.subTest(phase=phase):
                    applied = run_preset_install(installed, all_platforms=True)
                    self.assertEqual(applied.returncode, 0, applied.stdout[-2500:] + applied.stderr)
                    self.assertEqual(list(installed.rglob("*.new")) + list(installed.rglob("*.bak")), [])
                    self.chain(installed, work / phase)

    def chain(self, installed, chain):
        root, env = transcript.stage_transcript_owner_repo(installed, chain)
        sync, _ = transcript.invoke_public(root, env, "guru-sync-base", {
            "schema_version": "1.0", "public_input": {"source_exit": "start", "mode": "workflow", "repo_root": ".", "base_branch": "main", "route": "repo_change"},
        }, "synced")
        public, _ = transcript.project_installed_output(root, "guru-sync-base", "synced", sync)
        owner, _, public = transcript.checked_context_owner_for_issue(root, env, public, sync["transition"])
        discovery, _ = transcript.invoke_public(root, env, "guru-discover-change-context", {
            "schema_version": "1.0", "public_input": public, "transition": sync["transition"], "owner_context": {}, "owner_result": owner,
        }, "context_ready")
        owner, _ = transcript.clarification_owner_for_issue(root, env, discovery["transition"], discovery["duplicate_snapshot"])
        clarity, _ = transcript.invoke_public(root, env, "guru-clarify-requirements", {
            "schema_version": "1.0", "public_input": {"profile": "initial_change_request", "source_exit": "context_ready", "mode": "workflow", "target_locator": discovery["transition"]["target_locator"], "continuation_id": discovery["transition"]["continuation_id"], "duplicate_snapshot": discovery["duplicate_snapshot"]},
            "transition": discovery["transition"], "owner_context": {}, "owner_result": owner,
        }, "clear")
        issue = transcript.live_issue(root, env)
        envelope = {"profile": "change_request", "mode": "workflow", "change_request": transcript.wording_change_request_source(issue), "owner_result": {}}
        before = file_snapshot(root)
        paths = {str(p.relative_to(chain)) for p in chain.rglob("*")}
        scanned = self.call(root, env, "record-contract-wording-review.sh", envelope, "--scan-only")
        self.assertEqual(scanned["scan"]["hits"], [])
        # English fixture has no controlled terms; the independent semantic
        # fixture still supplies every gate dimension before recording.
        envelope["owner_result"] = {"generated_at": "2026-09-09T00:00:00Z", "revisions": [], "classifications": [], "typed_exit": "pass", "ai_review_gate": {
            "status": "passed", "reviewer": "integration-fixture", "summary": "The complete fixture title and body define one fixed transition contract.", "reviewed_scan_sha256": scanned["scan"]["scan_sha256"],
            "checked_dimensions": {key: True for key in ("complete_profile_scope", "all_hits_classified", "zero_unchecked_hits", "product_semantics_preserved", "retained_reasons_sufficient", "zero_hits_not_requirement_review")},
        }}
        envelope["owner_result"] = self.call(root, env, "record-contract-wording-review.sh", envelope)
        checked = self.call(root, env, "check-contract-wording-review.sh", envelope)
        counts = transcript.operation_counts(env)
        result, _ = transcript.invoke_public(root, env, "guru-review-contract-wording", {
            "schema_version": "1.0", "public_input": {"profile": "change_request", "source_exit": "clear", "mode": "workflow", "target_locator": clarity["transition"]["target_locator"], "continuation_id": clarity["transition"]["continuation_id"]},
            "transition": clarity["transition"], "owner_context": {}, "owner_result": envelope["owner_result"], "validation_receipt": checked["validation_receipt"],
        }, "pass")
        self.assertEqual(result["transition"]["stage"], "wording_current")
        self.assertEqual(transcript.operation_delta(counts, transcript.operation_counts(env)), {})
        self.assertEqual(file_snapshot(root), before)
        self.assertEqual({str(p.relative_to(chain)) for p in chain.rglob("*")}, paths)
        for field in ("title", "body"):
            authority = chain / f"issue-{field}.txt"
            original = authority.read_text()
            try:
                authority.write_text(original + " changed")
                self.call(root, env, "check-contract-wording-review.sh", envelope, expected=3)
            finally:
                authority.write_text(original)
        missing = copy.deepcopy(envelope)
        missing.pop("change_request")
        self.call(root, env, "record-contract-wording-review.sh", missing, expected=2)
        self.assertEqual(file_snapshot(root), before)
        transcript.assert_forbidden_runtime_absent(root)

    def call(self, root, env, name, envelope, *args, expected=0):
        wrapper = root / ".trellis/guru-team/skills/packages/guru-review-contract-wording/scripts" / name
        result = transcript.run([wrapper, "--root", root, "--invocation", "-", *args], cwd=root, env=env, stdin=envelope, check=False)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        value = json.loads(result.stdout)
        if expected == 3:
            self.assertEqual(value["code"], "stale_identity")
        return value


if __name__ == "__main__":
    unittest.main()
