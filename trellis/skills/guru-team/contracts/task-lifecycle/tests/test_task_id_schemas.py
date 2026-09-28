import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


CONTRACTS = Path(__file__).resolve().parents[1]
PACKAGES = CONTRACTS.parents[1] / "packages"
TASK_ID_PATTERN = "^[A-Za-z0-9][A-Za-z0-9._-]*$"
TASK_ID_SUFFIX = "[A-Za-z0-9][A-Za-z0-9._-]*$"


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


class TaskIdSchemaTest(unittest.TestCase):
    def test_canonical_task_id_patterns_match_issue_contract(self):
        paths = list(CONTRACTS.rglob("*.schema.json"))
        paths += list(PACKAGES.glob("*/schemas/*.schema.json"))
        paths += list(PACKAGES.glob("*/consumers/**/*.schema.json"))
        matches = 0
        for path in paths:
            schema = json.loads(path.read_text())
            for entry in objects(schema):
                pattern = entry.get("pattern")
                if not isinstance(pattern, str) or not pattern.endswith(TASK_ID_SUFFIX):
                    continue
                if pattern.startswith("^refs/heads/guru-task-lifecycle/"):
                    continue
                with self.subTest(path=path):
                    self.assertEqual(pattern, TASK_ID_PATTERN)
                    validator = Draft202012Validator({"type": "string", "pattern": pattern})
                    for task_id in ("a..b", "a.", "a.lock", "A_0-b"):
                        self.assertTrue(validator.is_valid(task_id), task_id)
                    for task_id in ("", ".a", "-a", "a/b"):
                        self.assertFalse(validator.is_valid(task_id), task_id)
                matches += 1
        self.assertGreater(matches, 0)

    def test_branch_and_receipt_refs_keep_git_constraints(self):
        catalog = json.loads((CONTRACTS / "task-lifecycle-dtos.schema.json").read_text())
        for file_name, definition, prefix in (
            ("task-lifecycle-dtos.schema.json", "branchRef", ""),
            ("task-branch-binding.schema.json", "branchName", ""),
            ("task-branch-rebind-transaction.schema.json", "branchName", ""),
            ("task-resource-ledger.schema.json", "branchRef", "refs/heads/"),
            ("task-resource-cleanup-resolution.schema.json", "branchRef", "refs/heads/"),
        ):
            schema = json.loads((CONTRACTS / file_name).read_text())
            branch = Draft202012Validator(schema["$defs"][definition])
            for value in ("a..b", "a.", "guru-task-lifecycle/a", "guru-task-lifecycle-id/a"):
                with self.subTest(schema=file_name, branch=value):
                    self.assertFalse(branch.is_valid(prefix + value))
            if not prefix:
                self.assertFalse(branch.is_valid("a.lock"))
            self.assertTrue(branch.is_valid(prefix + "guru-task-lifecycle-id-other"))

        receipt = Draft202012Validator(catalog["$defs"]["handoffReceiptRef"])
        self.assertTrue(receipt.is_valid("refs/heads/guru-task-lifecycle/a-b"))
        for task_id in ("a..b", "a.", "a.lock"):
            digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()
            with self.subTest(task_id=task_id):
                self.assertFalse(receipt.is_valid(f"refs/heads/guru-task-lifecycle/{task_id}"))
                self.assertTrue(receipt.is_valid(f"refs/heads/guru-task-lifecycle-id/{digest}"))
        for value in (
            "refs/heads/guru-task-lifecycle-id/abc",
            "refs/heads/guru-task-lifecycle-id/" + "A" * 64,
            "refs/heads/guru-task-lifecycle-id/" + "a" * 64 + "/extra",
        ):
            with self.subTest(receipt=value):
                self.assertFalse(receipt.is_valid(value))

        ledger = json.loads((CONTRACTS / "task-resource-ledger.schema.json").read_text())
        retained = Draft202012Validator(ledger["$defs"]["retainedControlRef"])
        self.assertTrue(retained.is_valid("refs/heads/guru-task-lifecycle/a-b"))
        self.assertTrue(retained.is_valid("refs/heads/guru-task-lifecycle-id/" + "a" * 64))
        self.assertFalse(retained.is_valid("refs/heads/guru-task-lifecycle-id/abc"))

    def test_cleanup_contract_documents_both_retained_control_ref_namespaces(self):
        readme = (CONTRACTS / "README.md").read_text()
        for namespace in (
            "refs/heads/guru-task-lifecycle/*",
            "refs/heads/guru-task-lifecycle-id/*",
        ):
            with self.subTest(namespace=namespace):
                self.assertIn(f"`{namespace}`", readme)


if __name__ == "__main__":
    unittest.main()
