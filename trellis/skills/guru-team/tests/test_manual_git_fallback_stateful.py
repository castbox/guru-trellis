"""T408-06/07 test-only command effects, not AI or live GitHub evidence.

Tests explicitly select each operation. There is no approval function, routing,
Guru runtime invocation, or recovery artifact. Native Agent exercises own the
dialogue/confirmation evidence; fake provider results cannot prove remote GitHub
permissions, checks, automatic closure, or release-contract compliance.
"""

from __future__ import annotations

import copy
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class UnknownRemoteFact(RuntimeError):
    """A failed read differs from a successful read of an absent resource."""


class FakeGitHub:
    """Closed, in-memory provider: records effects only, never chooses a route."""

    def __init__(self) -> None:
        self.state = {
            "prs": {}, "issues": {408: "OPEN", 409: "OPEN"}, "releases": {},
        }
        self.effects = []
        self.unavailable = set()

    def read(self, resource: str, identity: object):
        if resource in self.unavailable:
            raise UnknownRemoteFact(f"fake GitHub {resource}: read unavailable")
        return copy.deepcopy(self.state[resource].get(identity))

    def create_pr(self, number: int, payload: dict) -> None:
        self.state["prs"][number] = copy.deepcopy(payload)
        self.effects.append(("pr.create", number, copy.deepcopy(payload)))

    def update_pr(self, number: int, payload: dict) -> None:
        self.state["prs"][number].update(copy.deepcopy(payload))
        self.effects.append(("pr.update", number, copy.deepcopy(payload)))

    def record_merge(self, number: int, sha: str) -> None:
        # Caller supplies a merge actually created in the temporary Git remote.
        self.state["prs"][number].update(state="MERGED", mergeCommit=sha)
        self.effects.append(("pr.merge", number, sha))

    def close_issue(self, number: int) -> None:
        self.state["issues"][number] = "CLOSED"
        self.effects.append(("issue.close", number))

    def create_release(self, tag: str, payload: dict) -> None:
        self.state["releases"][tag] = copy.deepcopy(payload)
        self.effects.append(("release.create", tag, copy.deepcopy(payload)))


class ManualGitFallbackStatefulTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="manual-git-408-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "checkout"
        self.remote = self.root / "remote.git"
        # Isolate real Git commands from the developer's identity, hooks and env.
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_TERMINAL_PROMPT="0", GIT_ALLOW_PROTOCOL="file",
                        GIT_AUTHOR_NAME="Manual Fixture",
                        GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Manual Fixture",
                        GIT_COMMITTER_EMAIL="fixture@example.invalid")
        self.commands = []
        self.git(self.root, "init", "--bare", "-q", "-b", "main", str(self.remote))
        self.git(self.root, "init", "-q", "-b", "main", str(self.repo))
        self.write(".gitignore", ".trellis/.runtime/\n")
        self.write("base.txt", "base\n")
        self.write(".trellis/tasks/manual/task.json", '{"status":"in_progress"}\n')
        self.write(".trellis/tasks/archive/old/finish-summary.json", '{"old":true}\n')
        self.write(".trellis/.runtime/guru-team/workspace.json", '{"stale":true}\n')
        self.write(".trellis/.runtime/guru-team/finalizer/state.json", '{"pending":true}\n')
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-qm", "fixture base")
        self.base = self.git(self.repo, "rev-parse", "HEAD")
        self.git(self.repo, "remote", "add", "origin", str(self.remote))
        self.git(self.repo, "push", "-q", "origin", "main:main")
        self.git(self.repo, "switch", "-qc", "task")
        self.write("change.txt", "selected change\n")
        self.write("unrelated.txt", "leave untracked\n")
        self.cleanup_target = self.root / "selected-scratch"
        self.cleanup_target.mkdir()
        (self.cleanup_target / "note").write_bytes(b"temporary output\n")
        self.sibling = self.root / "keep-scratch"
        self.sibling.mkdir()
        (self.sibling / "note").write_bytes(b"unselected output\n")
        self.github = FakeGitHub()
        self.residue = self.files(self.repo / ".trellis")

    def write(self, name: str, text: str) -> None:
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def git(self, cwd: Path, *args: str) -> str:
        argv = ["git", "-c", "core.hooksPath=/dev/null",
                "-c", "commit.gpgSign=false", "-c", "tag.gpgSign=false", *args]
        result = subprocess.run(argv, cwd=cwd, env=self.env, text=True,
                                capture_output=True, check=False)
        self.commands.append((str(cwd), tuple(args), result.returncode))
        result.check_returncode()
        return result.stdout.strip()

    @staticmethod
    def files(root: Path) -> dict:
        return {str(path.relative_to(root)): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file() and ".git" not in path.relative_to(root).parts}

    def refs(self, repo: Path) -> dict:
        output = self.git(repo, "for-each-ref", "--format=%(refname) %(objectname)")
        return dict(line.split() for line in output.splitlines())

    def snapshot(self) -> dict:
        return {
            "local_refs": self.refs(self.repo), "remote_refs": self.refs(self.remote),
            "head": self.git(self.repo, "rev-parse", "HEAD"),
            "branch": self.git(self.repo, "symbolic-ref", "HEAD"),
            "status": self.git(self.repo, "status", "--porcelain=v1", "--untracked-files=all"),
            "index": self.git(self.repo, "ls-files", "--stage"),
            "files": self.files(self.repo), "github": copy.deepcopy(self.github.state),
            "scratch": self.files(self.cleanup_target),
            "scratch_exists": self.cleanup_target.exists(),
            "sibling": self.files(self.sibling),
        }

    def assert_only(self, before: dict, **changes) -> None:
        expected = copy.deepcopy(before)
        expected.update(changes)
        self.assertEqual(self.snapshot(), expected)
        self.assertEqual(self.files(self.repo / ".trellis"), self.residue)

    def commit_change(self) -> str:
        self.git(self.repo, "add", "--", "change.txt")
        self.git(self.repo, "commit", "-qm", "manual selected change")
        return self.git(self.repo, "rev-parse", "HEAD")

    def push_change(self) -> str:
        head = self.commit_change()
        self.git(self.repo, "push", "-q", "origin", "task:task")
        return head

    def pr_payload(self, head: str) -> dict:
        return {"repo": "fixture/guru", "base": "main", "head": "task",
                "headOid": head, "title": "\u624b\u52a8\u53d8\u66f4",
                "body": "Refs #408", "isDraft": True, "state": "OPEN"}

    def seed_pr(self) -> str:
        head = self.push_change()
        self.github.create_pr(1, self.pr_payload(head))
        self.github.effects.clear()
        return head

    def test_commit_changes_only_selected_commit_and_index(self) -> None:
        before = self.snapshot()
        head = self.commit_change()
        self.assertEqual(self.git(self.repo, "show", "-s", "--format=%P%n%B", head),
                         f"{self.base}\nmanual selected change")
        self.assertEqual(self.git(self.repo, "diff-tree", "--no-commit-id", "--name-only",
                                  "-r", head), "change.txt")
        blob = self.git(self.repo, "rev-parse", f"{head}:change.txt")
        index = sorted(before["index"].splitlines() + [f"100644 {blob} 0\tchange.txt"],
                       key=lambda entry: entry.split("\t", 1)[1])
        self.assertEqual(self.git(self.repo, "rev-parse", f"{head}^{{tree}}"),
                         self.git(self.repo, "write-tree"))
        self.assert_only(before, head=head,
                         local_refs={**before["local_refs"], "refs/heads/task": head},
                         index="\n".join(index), status="?? unrelated.txt")
        self.assertEqual(self.github.effects, [])

    def test_push_changes_only_named_remote_branch_and_tracking_ref(self) -> None:
        head = self.commit_change()
        before = self.snapshot()
        self.git(self.repo, "push", "-q", "origin", "task:task")
        self.assertEqual(self.git(self.repo, "ls-remote", "origin", "refs/heads/task"),
                         f"{head}\trefs/heads/task")
        self.assert_only(before,
                         remote_refs={**before["remote_refs"], "refs/heads/task": head},
                         local_refs={**before["local_refs"], "refs/remotes/origin/task": head})
        self.assertEqual(self.github.effects, [])

    def test_pr_create_changes_only_new_draft_pr(self) -> None:
        head = self.push_change()
        before = self.snapshot()
        payload = self.pr_payload(head)
        self.github.create_pr(1, payload)
        expected = copy.deepcopy(before["github"])
        expected["prs"][1] = payload
        self.assertEqual(self.github.read("prs", 1), payload)
        self.assert_only(before, github=expected)
        self.assertEqual(self.github.effects, [("pr.create", 1, payload)])

    def test_pr_update_preserves_draft_and_does_not_merge(self) -> None:
        self.seed_pr()
        before = self.snapshot()
        payload = {"title": "\u66f4\u65b0\u624b\u52a8\u53d8\u66f4", "body": "Refs #408\nUpdated notes"}
        self.github.update_pr(1, payload)
        expected = copy.deepcopy(before["github"])
        expected["prs"][1].update(payload)
        self.assertEqual(self.github.read("prs", 1), expected["prs"][1])
        self.assert_only(before, github=expected)
        self.assertEqual(self.github.effects, [("pr.update", 1, payload)])

    def test_merge_updates_base_and_pr_without_closure_or_cleanup(self) -> None:
        head = self.seed_pr()
        # A separate clone represents the server performing the merge.
        server = self.root / "merge-server"
        self.git(self.root, "clone", "-q", str(self.remote), str(server))
        before = self.snapshot()
        self.assertEqual(self.github.read("prs", 1)["headOid"], head)
        self.git(server, "merge", "--no-ff", "-m", "manual merge", head)
        merged = self.git(server, "rev-parse", "HEAD")
        self.git(server, "push", "-q", "origin", "main:main")
        self.github.record_merge(1, merged)
        self.assertEqual(self.git(self.remote, "show", "-s", "--format=%P", merged),
                         f"{self.base} {head}")
        self.assertEqual(self.git(self.remote, "rev-parse", f"{merged}^{{tree}}"),
                         self.git(self.repo, "rev-parse", f"{head}^{{tree}}"))
        expected = copy.deepcopy(before["github"])
        expected["prs"][1].update(state="MERGED", mergeCommit=merged)
        self.assertEqual(self.github.read("prs", 1), expected["prs"][1])
        self.assert_only(before, github=expected,
                         remote_refs={**before["remote_refs"], "refs/heads/main": merged})
        self.assertEqual(self.github.effects, [("pr.merge", 1, merged)])

    def test_issue_closure_changes_only_named_issue(self) -> None:
        self.seed_pr()
        before = self.snapshot()
        self.assertEqual(self.github.read("issues", 408), "OPEN")
        self.github.close_issue(408)
        expected = copy.deepcopy(before["github"])
        expected["issues"][408] = "CLOSED"
        self.assertEqual(self.github.read("issues", 408), "CLOSED")
        self.assert_only(before, github=expected)
        self.assertEqual(self.github.effects, [("issue.close", 408)])

    def test_tag_does_not_publish_release_and_release_does_not_close_issue(self) -> None:
        head = self.push_change()
        before = self.snapshot()
        tag = "fixture-guru-candidate"
        self.git(self.repo, "tag", tag, head)
        self.git(self.repo, "push", "-q", "origin", f"refs/tags/{tag}:refs/tags/{tag}")
        self.assertEqual(self.git(self.repo, "ls-remote", "origin", f"refs/tags/{tag}"),
                         f"{head}\trefs/tags/{tag}")
        self.assert_only(before,
                         local_refs={**before["local_refs"], f"refs/tags/{tag}": head},
                         remote_refs={**before["remote_refs"], f"refs/tags/{tag}": head})
        self.assertEqual(self.github.effects, [])
        before_release = self.snapshot()
        payload = {"repo": "fixture/guru", "target": head, "notes": "Fixture notes",
                   "isDraft": False}
        self.github.create_release(tag, payload)
        expected = copy.deepcopy(before_release["github"])
        expected["releases"][tag] = payload
        self.assertEqual(self.github.read("releases", tag), payload)
        self.assert_only(before_release, github=expected)
        self.assertEqual(self.github.effects, [("release.create", tag, payload)])

    def test_cleanup_deletes_only_explicit_temporary_resource(self) -> None:
        self.seed_pr()
        before = self.snapshot()
        (self.cleanup_target / "note").unlink()
        self.cleanup_target.rmdir()
        self.assert_only(before, scratch={}, scratch_exists=False)
        self.assertEqual(self.github.effects, [])

    def test_unknown_remote_reads_are_not_known_absence_or_success(self) -> None:
        before = self.snapshot()
        self.assertIsNone(self.github.read("prs", 1))
        self.assertEqual(self.git(self.repo, "ls-remote", "origin", "refs/heads/task"), "")
        self.github.unavailable.update(("prs", "issues", "releases"))
        for resource, identity in (("prs", 1), ("issues", 408), ("releases", "candidate")):
            with self.subTest(resource=resource):
                with self.assertRaisesRegex(UnknownRemoteFact, "read unavailable"):
                    self.github.read(resource, identity)
        with self.assertRaises(subprocess.CalledProcessError) as error:
            self.git(self.repo, "ls-remote", str(self.root / "unavailable.git"), "refs/heads/main")
        self.assertNotEqual(error.exception.returncode, 0)
        self.assert_only(before)
        self.assertEqual(self.github.effects, [])


if __name__ == "__main__":
    unittest.main()
