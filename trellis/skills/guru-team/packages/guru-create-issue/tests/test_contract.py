from __future__ import annotations

import importlib.util
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("guru_create_issue_candidate", PACKAGE / "runtime/invoke.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CreateIssueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.draft = {
            "repo_ref": "castbox/guru-trellis", "title": "Reviewed new task",
            "body": "Exact scope and acceptance.", "labels": ["enhancement"],
            "duplicate_disposition": "create_new",
        }
        self.request = {
            "profile": "issue_creation", "action": "create_issue",
            "ready_target_kind": "proposed_draft",
            "reviewed_at": "2026-09-26T12:00:00Z",
            "reviewed_target": {
                "kind": "proposed_draft", "repo": "castbox/guru-trellis",
                "draft_id": "draft-reviewed-new-task",
                "source_request_sha256": "7663f130297dd509ea18cbf17dd9132bb168eb72c4ae8b6831a732ee22dfd519",
                "title_sha256": "c23bb4ea8415a95f1ee33d83208f2fdc9884cd1946476034f291724266c036c3",
                "body_sha256": "2300f289b59828872df896801965134fce77583b411711ab284c0cd0ec73ef4b",
                "identity_sha256": "20f7bc7e724fac50c2879df50cb8faad40583a302a7d672e152d2c0bff6078c6",
                "content_sha256": "4fbe4dfb113dd20b0e7ed107d8094c44311c18b44fdafdaedffb4f1e49b9d570",
            },
            "draft": self.draft,
        }
        self.issue = {
            "number": 654, "url": "https://github.com/castbox/guru-trellis/issues/654",
            "title": self.draft["title"], "body": MODULE._created_body(
                self.request, datetime(2026, 9, 26, 12, 0, tzinfo=timezone.utc)),
            "labels": [{"name": "enhancement"}], "state": "OPEN", "createdAt": "2026-09-26T12:00:01Z",
        }
        now = patch.object(MODULE, "_utc_now", return_value=datetime(2026, 9, 26, 12, 0, 1, tzinfo=timezone.utc))
        now.start()
        self.addCleanup(now.stop)

    def test_creation_rereads_live_identity_and_recovery_is_read_only(self) -> None:
        calls = []

        def gh(*args):
            calls.append(args)
            if args[:2] == ("issue", "create"):
                return self.issue["url"]
            if args[:2] == ("issue", "list"):
                return json.dumps([{"number": 654}])
            return json.dumps(self.issue)

        with patch.object(MODULE, "_gh", side_effect=gh):
            result = MODULE.invoke(self.request)
            self.assertEqual(result, {"exit_id": "created", "repo_ref": self.draft["repo_ref"],
                                      "number": 654, "url": self.issue["url"]})
            recovered = MODULE.invoke({**self.request, "action": "recover_created_issue_result"})
        self.assertEqual(result, recovered)
        self.assertEqual(sum(args[:2] == ("issue", "create") for args in calls), 1)
        create = next(args for args in calls if args[:2] == ("issue", "create"))
        self.assertEqual(create[create.index("--body") + 1], self.issue["body"])

    def test_recovery_rejects_ambiguous_or_changed_issue(self) -> None:
        with patch.object(MODULE, "_gh", side_effect=[
            json.dumps([{"number": 654}, {"number": 655}]),
            json.dumps(self.issue), json.dumps({**self.issue, "number": 655}),
        ]):
            result = MODULE.invoke({**self.request, "action": "recover_created_issue_result"})
        self.assertEqual(result, {"exit_id": "blocked", "reason_code": "created_issue_result_not_unique"})
        with patch.object(MODULE, "_gh", side_effect=[self.issue["url"], json.dumps({**self.issue, "body": "stale"})]):
            self.assertEqual(MODULE.invoke(self.request)["exit_id"], "blocked")

    def test_recovery_ignores_identical_issue_from_before_review(self) -> None:
        old = {**self.issue, "number": 123, "url": "https://github.com/castbox/guru-trellis/issues/123",
               "createdAt": "2026-09-25T12:00:00Z"}
        with patch.object(MODULE, "_gh", side_effect=[json.dumps([{"number": 123}]), json.dumps(old)]):
            self.assertEqual(MODULE.invoke({**self.request, "action": "recover_created_issue_result"}),
                             {"exit_id": "blocked", "reason_code": "created_issue_result_not_unique"})
        with patch.object(MODULE, "_gh", side_effect=[json.dumps([{"number": 123}, {"number": 654}]),
                                                    json.dumps(old), json.dumps(self.issue)]):
            self.assertEqual(MODULE.invoke({**self.request, "action": "recover_created_issue_result"}),
                             {"exit_id": "created", "repo_ref": self.draft["repo_ref"],
                              "number": 654, "url": self.issue["url"]})

    def test_subsecond_review_waits_for_next_second_before_creation(self) -> None:
        request = {**self.request, "reviewed_at": "2026-09-26T12:00:00.500Z"}
        issue = {**self.issue, "body": MODULE._created_body(
            request, datetime(2026, 9, 26, 12, 0, 0, 500000, tzinfo=timezone.utc))}
        clock = iter([datetime(2026, 9, 26, 12, 0, 0, 500000, tzinfo=timezone.utc),
                      datetime(2026, 9, 26, 12, 0, 1, tzinfo=timezone.utc)])
        with patch.object(MODULE, "_utc_now", side_effect=lambda: next(clock)), \
             patch.object(MODULE.time, "sleep") as sleep, \
             patch.object(MODULE, "_gh", side_effect=[issue["url"], json.dumps(issue)]) as gh:
            self.assertEqual(MODULE.invoke(request)["exit_id"], "created")
        sleep.assert_called_once_with(0.5)
        self.assertEqual(gh.call_count, 2)

    def test_subsecond_review_recovery_excludes_same_second_old_issue(self) -> None:
        request = {**self.request, "action": "recover_created_issue_result",
                   "reviewed_at": "2026-09-26T12:00:00.500Z"}
        old = {**self.issue, "number": 123, "createdAt": "2026-09-26T12:00:00Z"}
        new = {**self.issue, "body": MODULE._created_body(
            request, datetime(2026, 9, 26, 12, 0, 0, 500000, tzinfo=timezone.utc))}
        with patch.object(MODULE, "_gh", side_effect=[json.dumps([{"number": 123}, {"number": 654}]),
                                                    json.dumps(old), json.dumps(new)]):
            self.assertEqual(MODULE.invoke(request)["number"], 654)
        with patch.object(MODULE, "_gh", side_effect=[json.dumps([{"number": 123}]), json.dumps(old)]):
            self.assertEqual(MODULE.invoke(request)["exit_id"], "blocked")

    def test_future_review_time_refreshes_without_creating_issue(self) -> None:
        request = {**self.request, "reviewed_at": "2999-09-26T12:00:00Z"}
        with patch.object(MODULE, "_gh") as gh:
            self.assertEqual(MODULE.invoke(request),
                             {"exit_id": "refresh_review", "reason_code": "reviewed_time_not_current"})
        gh.assert_not_called()

    def test_stale_review_time_refreshes_without_creating_issue(self) -> None:
        request = {**self.request, "reviewed_at": "2026-09-26T11:58:00Z"}
        with patch.object(MODULE, "_gh") as gh:
            self.assertEqual(MODULE.invoke(request),
                             {"exit_id": "refresh_review", "reason_code": "reviewed_time_not_current"})
        gh.assert_not_called()

    def test_stale_review_still_allows_read_only_recovery(self) -> None:
        request = {**self.request, "action": "recover_created_issue_result",
                   "reviewed_at": "2026-09-26T11:58:00Z"}
        issue = {**self.issue, "body": MODULE._created_body(
            request, datetime(2026, 9, 26, 11, 58, tzinfo=timezone.utc))}
        with patch.object(MODULE, "_gh", side_effect=[json.dumps([{"number": 654}]), json.dumps(issue)]):
            self.assertEqual(MODULE.invoke(request)["exit_id"], "created")

    def test_recovery_never_claims_later_identical_issue_from_other_attempt(self) -> None:
        other = {**self.issue, "body": self.draft["body"], "createdAt": "2026-09-26T12:04:00Z"}
        with patch.object(MODULE, "_gh", side_effect=[json.dumps([{"number": 654}]), json.dumps(other)]):
            self.assertEqual(MODULE.invoke({**self.request, "action": "recover_created_issue_result"}),
                             {"exit_id": "blocked", "reason_code": "created_issue_result_not_unique"})
        other["body"] = self.issue["body"].replace("guru-create-issue:", "guru-create-issue:other-")
        with patch.object(MODULE, "_gh", side_effect=[json.dumps([{"number": 654}]), json.dumps(other)]):
            self.assertEqual(MODULE.invoke({**self.request, "action": "recover_created_issue_result"})["exit_id"],
                             "blocked")

    def test_created_issue_accepts_canonical_label_case(self) -> None:
        draft = {**self.draft, "labels": ["Enhancement"]}
        issue = {**self.issue, "labels": [{"name": "enhancement"}]}
        with patch.object(MODULE, "_gh", side_effect=[issue["url"], json.dumps(issue)]):
            self.assertEqual(MODULE.invoke({**self.request, "draft": draft})["exit_id"], "created")

    def test_changed_reviewed_draft_refreshes_before_any_provider_call(self) -> None:
        changed = {**self.request, "draft": {**self.draft, "body": "Changed after review."}}
        with patch.object(MODULE, "_gh") as gh:
            result = MODULE.invoke(changed)
        self.assertEqual(result, {"exit_id": "refresh_review", "reason_code": "reviewed_draft_stale"})
        gh.assert_not_called()


if __name__ == "__main__":
    unittest.main()
