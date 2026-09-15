from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SPEC = Path(".trellis/spec/workflow/semantic-retrieval.md")
CANONICAL_SPEC = Path("trellis/presets/guru-team/spec/workflow/semantic-retrieval.md")
CANONICAL_SKILL_PACKAGE_CONTRACT = Path(
    "trellis/presets/guru-team/spec/workflow/skill-package-contract.md"
)
GURU_OWNERS = (
    "guru-discover-change-context",
    "guru-clarify-requirements",
    "guru-check-task",
    "guru-review-branch",
)
SEMANTIC_FIXTURES = {
    "guru-discover-change-context": "evals/files/eval-context-ready-facts.json",
    "guru-clarify-requirements": "evals/files/eval-clear-facts.json",
    "guru-check-task": "evals/files/passed-initial-facts.json",
    "guru-review-branch": "evals/files/workflow-passed-facts.json",
}
NON_OWNERS = (
    "guru-review-change-request",
    "guru-review-contract-wording",
    "guru-create-task-commit",
    "guru-review-task-publication",
    "guru-finalize-task",
    "guru-reconcile-task-base",
)
UPSTREAM_EVIDENCE_PATHS = (
    ".trellis/agents/implement.md",
    ".trellis/agents/check.md",
    ".agents/skills/trellis-check/SKILL.md",
    ".agents/skills/trellis-session-insight/SKILL.md",
    ".claude/agents/trellis-research.md",
    ".claude/agents/trellis-implement.md",
    ".claude/agents/trellis-check.md",
    ".codex/agents/trellis-research.toml",
    ".codex/agents/trellis-implement.toml",
    ".codex/agents/trellis-check.toml",
    ".cursor/agents/trellis-research.md",
    ".cursor/agents/trellis-implement.md",
    ".cursor/agents/trellis-check.md",
)
OWNERSHIP_INVENTORY = Path(
    "trellis/presets/guru-team/ownership/upstream-ownership.json"
)


class SemanticRetrievalContractTest(unittest.TestCase):
    def test_single_spec_defines_required_contract(self) -> None:
        matches = list((ROOT / ".trellis/spec").rglob("semantic-retrieval.md"))
        self.assertEqual(matches, [ROOT / SPEC])
        self.assertEqual((ROOT / SPEC).read_bytes(), (ROOT / CANONICAL_SPEC).read_bytes())
        text = matches[0].read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Semantic Retrieval Contract 1.0",
            "must include every applicable category",
            "in one language cannot independently support",
            "OBJECT_ACCESS_DENIED",
            "reviewed_content_sha256",
            "workspace_ref",
            "can only execute queries supplied by the AI",
            "The Guru semantic retrieval owners are "
            "`guru-discover-change-context`, `guru-clarify-requirements`, "
            "`guru-check-task`, and `guru-review-branch`.",
            "Upstream workers and providers may supply evidence, but they do not own or "
            "consume this Guru SSOT.",
            "The Guru caller remains responsible for the applicable concept family, "
            "combined evidence coverage, and conclusion sufficiency",
            "Do not persist a raw search report",
        ):
            self.assertIn(required, normalized)

    def test_guru_owners_reference_without_expanding_non_owners(self) -> None:
        package_root = ROOT / "trellis/skills/guru-team/packages"
        for skill_id in GURU_OWNERS:
            with self.subTest(owner=skill_id):
                package = package_root / skill_id
                self.assertIn(SPEC.as_posix(), (package / "SKILL.md").read_text(encoding="utf-8"))
                self.assertIn(SPEC.as_posix(), (package / "references/contract.md").read_text(encoding="utf-8"))
                evals = json.loads((package / "evals/evals.json").read_text(encoding="utf-8"))
                semantic = [
                    assertion
                    for case in evals["evals"]
                    for assertion in case.get("assertions", {}).get("semantic", [])
                ]
                self.assertGreaterEqual(len(semantic), 2)
                self.assertTrue(all(item["evidence_selector"] != "output" for item in semantic))
                fixture = json.loads(
                    (package / SEMANTIC_FIXTURES[skill_id]).read_text(encoding="utf-8")
                )["semantic_retrieval_fixture"]
                self.assertGreaterEqual(len(fixture["concept_family"]), 3)
                self.assertGreaterEqual(len(fixture["evidence"]), 2)
                self.assertIn("zero results", fixture["rejected_conclusion"])
                self.assertTrue(fixture["expected_disposition"])
        for skill_id in NON_OWNERS:
            with self.subTest(non_owner=skill_id):
                text = (package_root / skill_id / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn(SPEC.as_posix(), text)
        reconcile_contract = (
            package_root / "guru-reconcile-task-base/references/contract.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn(SPEC.as_posix(), reconcile_contract)

        shared_contract = (ROOT / CANONICAL_SKILL_PACKAGE_CONTRACT).read_text(
            encoding="utf-8"
        )
        reconcile_section = shared_contract.split(
            "## Task Base Reconciliation Owner", maxsplit=1
        )[1].split("\n## ", maxsplit=1)[0]
        self.assertNotIn(SPEC.as_posix(), reconcile_section)
        self.assertIn(
            "one exact\ncaller-supplied active-task/base-evolution pair",
            reconcile_section,
        )
        self.assertIn(
            "It does\nnot own or consume the broad semantic retrieval SSOT",
            reconcile_section,
        )

    def test_semantic_eval_runner_requires_complete_external_grading(self) -> None:
        runner = ROOT / "trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh"
        base_argv = [
            str(runner), "--root", str(ROOT), "--mode", "source",
            "--skill", "guru-discover-change-context", "--adapter", "shared",
            "--case", "context-ready-route",
        ]
        env = {**os.environ, "PATH": f"/usr/local/bin:{os.environ.get('PATH', '')}"}
        with tempfile.TemporaryDirectory(prefix="guru-semantic-eval-") as temporary:
            work_root = Path(temporary)
            missing = subprocess.run(
                [*base_argv, "--run-root", str(work_root / "missing"), "--json"],
                cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(missing.returncode, 0, missing.stderr)
            missing_result = json.loads(missing.stdout)
            self.assertEqual(missing_result["status"], "evaluation_failed")
            self.assertEqual(
                {row["detail"] for row in missing_result["cases"][0]["semantic_results"]},
                {"external semantic grading missing"},
            )

            grading = {
                "schema_version": "1.0",
                "results": [
                    {
                        "case_id": "context-ready-route",
                        "comparison_side": "current",
                        "assertion_id": assertion_id,
                        "passed": True,
                        "summary": "The transcript satisfies the semantic retrieval criterion.",
                    }
                    for assertion_id in (
                        "bilingual-current-evidence",
                        "exact-literal-preserved",
                    )
                ],
            }
            grading_path = work_root / "grading.json"
            grading_path.write_text(json.dumps(grading), encoding="utf-8")
            complete = subprocess.run(
                [
                    *base_argv, "--run-root", str(work_root / "complete"),
                    "--semantic-grading", str(grading_path), "--json",
                ],
                cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(complete.returncode, 0, complete.stderr)
            complete_result = json.loads(complete.stdout)
            self.assertEqual(complete_result["status"], "passed")
            self.assertTrue(
                all(row["passed"] for row in complete_result["cases"][0]["semantic_results"])
            )

            grading["results"][0].update({
                "passed": False,
                "summary": "The candidate relies on a single-language zero result.",
            })
            rejected_grading_path = work_root / "rejected-grading.json"
            rejected_grading_path.write_text(json.dumps(grading), encoding="utf-8")
            rejected = subprocess.run(
                [
                    *base_argv, "--run-root", str(work_root / "rejected"),
                    "--semantic-grading", str(rejected_grading_path), "--json",
                ],
                cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(rejected.returncode, 0, rejected.stderr)
            rejected_result = json.loads(rejected.stdout)
            self.assertEqual(rejected_result["status"], "evaluation_failed")
            self.assertFalse(rejected_result["cases"][0]["semantic_results"][0]["passed"])

    def test_upstream_evidence_paths_do_not_consume_or_claim_guru_spec(self) -> None:
        inventory = json.loads((ROOT / OWNERSHIP_INVENTORY).read_text(encoding="utf-8"))
        exact_inventory_entries = {
            item["pattern"] for item in inventory["guru_owned_rules"]
        } | {
            item["path"] for item in inventory["managed_path_claims"]
        }
        for relative in UPSTREAM_EVIDENCE_PATHS:
            with self.subTest(upstream_path=relative):
                self.assertNotIn(
                    SPEC.as_posix(),
                    (ROOT / relative).read_text(encoding="utf-8"),
                )
                self.assertNotIn(relative, exact_inventory_entries)


if __name__ == "__main__":
    unittest.main()
