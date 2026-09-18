from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parents[1]))
spec = importlib.util.spec_from_file_location(
    "merge_delivery_history", PACKAGE / "runtime/history.py"
)
assert spec and spec.loader
HISTORY = importlib.util.module_from_spec(spec)
spec.loader.exec_module(HISTORY)


class DeliveryHistoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Guru Test")
        self.git("config", "user.email", "guru@example.test")
        (self.root / "state.txt").write_text("base\n", encoding="utf-8")
        self.git("add", "state.txt")
        self.git("commit", "-m", "base")
        self.task_identity = "435-active-task-delivery-loop"
        self.deliveries: list[dict[str, str | int]] = []
        self.add_delivery("delivery-a", 101, "A")
        self.add_delivery("delivery-b", 102, "B")
        self.add_bookkeeping_merge()
        self.base_head = self.git("rev-parse", "main")
        self.git("switch", "-c", "reactivated-binding")
        self.query = {
            "schema_version": "1.0",
            "task_identity": self.task_identity,
            "repo_ref": "example/repo",
            "base_ref": "main",
        }

    def git(self, *args: str) -> str:
        proc = subprocess.run(
            ["git", *args],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return proc.stdout.strip()

    def add_delivery(self, branch: str, pr_number: int, marker: str) -> None:
        self.git("switch", "-c", branch, "main")
        with (self.root / "state.txt").open("a", encoding="utf-8") as stream:
            stream.write(marker + "\n")
        self.git("add", "state.txt")
        self.git("commit", "-m", f"delivery {marker}")
        reviewed_head = self.git("rev-parse", "HEAD")
        self.git("switch", "main")
        message = (
            f"merge {marker}\n\n"
            f"Guru-Task-Identity: {self.task_identity}\n"
            "Guru-Delivery-Schema: 1\n"
            f"Guru-Delivery-Head: {reviewed_head}"
        )
        self.git("merge", "--no-ff", branch, "-m", message)
        merge_sha = self.git("rev-parse", "HEAD")
        self.git("branch", "-D", branch)
        self.deliveries.append({
            "reviewed_head": reviewed_head,
            "merge_commit_sha": merge_sha,
            "pr_number": pr_number,
        })

    def add_bookkeeping_merge(self) -> None:
        self.git("switch", "-c", "finish-bookkeeping", "main")
        (self.root / "bookkeeping.txt").write_text("finish\n", encoding="utf-8")
        self.git("add", "bookkeeping.txt")
        self.git("commit", "-m", "finish bookkeeping")
        self.git("switch", "main")
        self.git(
            "merge", "--no-ff", "finish-bookkeeping", "-m", "finish bookkeeping"
        )
        self.git("branch", "-D", "finish-bookkeeping")

    def github_value(self, _root: Path, args: list[str], _operation: str):
        endpoint = args[-1]
        if endpoint == "repos/example/repo":
            return {"full_name": "example/repo"}
        if endpoint == "repos/example/repo/git/ref/heads/main":
            return {"object": {"sha": self.base_head}}
        for delivery in self.deliveries:
            if endpoint == (
                f"repos/example/repo/commits/{delivery['merge_commit_sha']}/pulls"
            ):
                return [{
                    "number": delivery["pr_number"],
                    "state": "closed",
                    "merged_at": "2026-09-18T01:00:00Z",
                    "merge_commit_sha": delivery["merge_commit_sha"],
                    "body": "mutated after merge and intentionally ignored",
                    "base": {
                        "ref": "main",
                        "repo": {"full_name": "example/repo"},
                    },
                    "head": {
                        "sha": delivery["reviewed_head"],
                        "ref": "deleted-old-branch",
                        "repo": {"full_name": "example/repo"},
                    },
                }]
        raise AssertionError(endpoint)

    def discover(self) -> dict:
        with mock.patch.object(HISTORY, "require_gh"), mock.patch.object(
            HISTORY, "gh_value", side_effect=self.github_value
        ) as github:
            result = HISTORY.discover(self.root, PACKAGE, self.query)
        self.assertTrue(
            all(call.args[1][0] == "api" for call in github.call_args_list)
        )
        return result

    def test_two_cross_branch_deliveries_are_reconstructed_and_bookkeeping_is_excluded(self) -> None:
        result = self.discover()
        self.assertEqual(len(result["deliveries"]), 2)
        self.assertEqual(
            [item["pr_number"] for item in result["deliveries"]],
            [101, 102],
        )
        self.assertEqual(
            [item["reviewed_head"] for item in result["deliveries"]],
            [item["reviewed_head"] for item in self.deliveries],
        )
        self.assertEqual(self.git("branch", "--show-current"), "reactivated-binding")

    def test_pr_body_and_deleted_head_branch_do_not_define_identity(self) -> None:
        result = self.discover()
        self.assertEqual(
            [item["merge_commit_sha"] for item in result["deliveries"]],
            [item["merge_commit_sha"] for item in self.deliveries],
        )

    def test_pr_head_drift_fails_closed(self) -> None:
        original = self.github_value

        def drifted(root: Path, args: list[str], operation: str):
            value = original(root, args, operation)
            if isinstance(value, list) and value:
                value = json.loads(json.dumps(value))
                value[0]["head"]["sha"] = "f" * 40
            return value

        with mock.patch.object(HISTORY, "require_gh"), mock.patch.object(
            HISTORY, "gh_value", side_effect=drifted
        ), self.assertRaises(HISTORY.CommandError):
            HISTORY.discover(self.root, PACKAGE, self.query)

    def test_trailer_head_that_is_not_parent_two_fails_closed(self) -> None:
        self.git("switch", "main")
        self.git("switch", "-c", "bad-delivery")
        (self.root / "bad.txt").write_text("bad\n", encoding="utf-8")
        self.git("add", "bad.txt")
        self.git("commit", "-m", "bad delivery")
        self.git("switch", "main")
        message = (
            "bad merge\n\n"
            f"Guru-Task-Identity: {self.task_identity}\n"
            "Guru-Delivery-Schema: 1\n"
            f"Guru-Delivery-Head: {'f' * 40}"
        )
        self.git("merge", "--no-ff", "bad-delivery", "-m", message)
        self.git("branch", "-D", "bad-delivery")
        self.base_head = self.git("rev-parse", "main")
        with mock.patch.object(HISTORY, "require_gh"), mock.patch.object(
            HISTORY, "gh_value", side_effect=self.github_value
        ), self.assertRaises(HISTORY.CommandError):
            HISTORY.discover(self.root, PACKAGE, self.query)

    def test_base_or_repository_drift_fails_closed(self) -> None:
        for endpoint, replacement in (
            ("repos/example/repo", {"full_name": "other/repo"}),
            (
                "repos/example/repo/git/ref/heads/main",
                {"object": {"sha": "f" * 40}},
            ),
        ):
            def drifted(
                root: Path,
                args: list[str],
                operation: str,
                *,
                selected=endpoint,
                value=replacement,
            ):
                if args[-1] == selected:
                    return value
                return self.github_value(root, args, operation)

            with self.subTest(endpoint=endpoint), mock.patch.object(
                HISTORY, "require_gh"
            ), mock.patch.object(
                HISTORY, "gh_value", side_effect=drifted
            ), self.assertRaises(HISTORY.CommandError):
                HISTORY.discover(self.root, PACKAGE, self.query)


if __name__ == "__main__":
    unittest.main()
