import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def load_runtime():
    candidates = []
    for ancestor in [PACKAGE_ROOT, *PACKAGE_ROOT.parents]:
        candidates.extend([
            ancestor / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
            ancestor / ".trellis/guru-team/scripts/python/guru_team_trellis.py",
        ])
    runtime_path = next((path for path in candidates if path.is_file()), None)
    if runtime_path is None:
        raise RuntimeError("Compatible Guru Team runtime not found for package tests.")
    spec = importlib.util.spec_from_file_location("contract_wording_package_runtime", runtime_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Compatible Guru Team runtime could not be loaded.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


class ContractWordingPackageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(
            ["git", "init", "-q", "-b", "main", str(self.root)],
            check=True,
        )
        self.task = self.root / ".trellis/tasks/wording-review"
        self.task.mkdir(parents=True)
        for name in GTT.CONTRACT_WORDING_PLANNING_SCOPE:
            (self.task / name).write_text(
                f"# {name}\n\nThis file defines one exact contract.\n",
                encoding="utf-8",
            )
        self.explicit = self.root / "docs/review.md"
        self.explicit.parent.mkdir(parents=True)
        self.explicit.write_text("# Review\n\n建议绑定一个确定值。\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def result(
        self,
        scope: dict[str, object],
        scan: dict[str, object],
        *,
        classification: str | None = "term_definition",
        typed_exit: str = "pass",
        revisions: list[dict[str, object]] | None = None,
    ) -> dict[str, object]:
        classifications = [] if classification is None else [
            {
                "hit_id": hit["hit_id"],
                "classification": classification,
                "reason": "The retained occurrence has an explicit reviewed meaning.",
            }
            for hit in scan["hits"]
        ]
        passed = typed_exit != "blocked"
        return GTT.contract_wording_derive_result(
            str(scope["identity"]).split(":", 1)[0],
            "workflow" if str(scope["identity"]).startswith("planning_artifacts:") else "standalone",
            scope,
            scan,
            {
                "generated_at": "2026-01-01T00:00:00Z",
                "semantic_review": {
                    "revisions": revisions or [],
                    "classifications": classifications,
                    "ai_review_gate": {
                        "status": "passed" if passed else "blocked",
                        "reviewer": "package-test-reviewer",
                        "summary": "The complete current scope and scan were reviewed.",
                        "reviewed_scan_sha256": scan["scan_sha256"],
                        "checked_dimensions": {
                            name: passed for name in GTT.CONTRACT_WORDING_REVIEW_DIMENSIONS
                        },
                    },
                },
                "human_confirmation": {
                    "status": "not_required" if passed else "refused",
                    "confirmed_by": None,
                    "confirmed_at": None,
                    "reason": "The package test records the reviewed confirmation state.",
                },
                "typed_exit": typed_exit,
            },
        )

    def test_interface_declares_semantic_closed_loop_and_fixed_exits(self) -> None:
        interface = json.loads((PACKAGE_ROOT / "interface.json").read_text(encoding="utf-8"))
        self.assertEqual(interface["schema_version"], "1.2")
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertEqual(
            interface["ordered_stages"],
            [
                "forward_behavior",
                "ai_review_gate",
                "conditional_human_confirmation",
                "recorder_validator",
                "typed_exit",
            ],
        )
        self.assertEqual(interface["modes"]["workflow"]["entry_precondition_ids"], interface["modes"]["standalone"]["entry_precondition_ids"])
        self.assertEqual([item["id"] for item in interface["external_exits"]], ["pass", "content_changed", "blocked"])

    def test_contract_is_the_human_readable_vocabulary_owner(self) -> None:
        contract = (PACKAGE_ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        for token in ("contract-wording-v2", "contract-wording-classifications-v1", "change_request", "planning_artifacts", "explicit_paths"):
            self.assertIn(token, contract)
        for classification in ("contract_violation", "deterministic_threshold", "deterministic_default", "deterministic_option", "deterministic_reference"):
            self.assertIn(classification, contract)

    def test_schema_and_example_are_closed_versioned_json(self) -> None:
        schema = json.loads((PACKAGE_ROOT / "schemas" / "contract-wording-review.schema.json").read_text(encoding="utf-8"))
        example = json.loads((PACKAGE_ROOT / "examples" / "contract-wording-review.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(example["schema_version"], "1.0")
        self.assertEqual(example["skill_id"], "guru-review-contract-wording")

    def test_wrappers_resolve_the_managed_dispatcher_from_every_install_root(self) -> None:
        for name in ("record-contract-wording-review.sh", "check-contract-wording-review.sh"):
            wrapper = (PACKAGE_ROOT / "scripts" / name).read_text(encoding="utf-8")
            self.assertIn('DISPATCHER="$REPO_ROOT/.trellis/guru-team/scripts/bash/run-skill-command.sh"', wrapper)
            for root in (".trellis/guru-team/skills/packages", ".agents/skills", ".codex/skills", ".cursor/skills", ".claude/skills"):
                self.assertIn(f"*/{root}/guru-review-contract-wording", wrapper)
            self.assertNotIn("../../../../../workflows/guru-team", wrapper)

    def test_all_three_profiles_build_their_complete_scope(self) -> None:
        planning, _ = GTT.contract_wording_build_scope(
            self.root, "planning_artifacts", "workflow", task_dir=self.task
        )
        self.assertEqual(
            [item["path"] for item in planning["items"]],
            [f".trellis/tasks/wording-review/{name}" for name in GTT.CONTRACT_WORDING_PLANNING_SCOPE],
        )

        second = self.root / "docs/second.md"
        second.write_text("# Second\n", encoding="utf-8")
        explicit, _ = GTT.contract_wording_build_scope(
            self.root,
            "explicit_paths",
            "standalone",
            explicit_paths=["docs/second.md", "docs/review.md"],
        )
        self.assertEqual(
            [item["path"] for item in explicit["items"]],
            ["docs/review.md", "docs/second.md"],
        )

        draft_input = self.root / "draft.json"
        draft_input.write_text(json.dumps({
            "kind": "draft",
            "draft_id": "draft-1",
            "title": "Exact change title",
            "body": "Exact change body",
            "selected_comments": [{
                "id": "comment-1",
                "author": "reviewer",
                "updated_at": "2026-01-01T00:00:00Z",
                "selection_reason": "This comment is authoritative.",
                "body": "Exact authoritative comment.",
            }],
        }), encoding="utf-8")
        change, _ = GTT.contract_wording_build_scope(
            self.root,
            "change_request",
            "standalone",
            change_request_input="draft.json",
        )
        self.assertEqual(
            [item["field"] for item in change["items"]],
            ["title", "body", "comment"],
        )
        change_scan = GTT.scan_contract_wording(change, {
            "change:title": "Exact change title",
            "change:body": "Exact change body",
            "comment:comment-1": "Exact authoritative comment.",
        })
        change_result = self.result(change, change_scan)
        change_result["scope"]["items"][2]["author"] = None
        change_result["facts_sha256"] = GTT.context_digest({
            key: value for key, value in change_result.items() if key != "facts_sha256"
        })
        self.assertIn(
            "contract_wording_schema_validation_failed",
            GTT.contract_wording_structural_errors(self.root, change_result, change, change_scan),
        )

    def test_change_request_selected_comments_require_author_and_updated_at(self) -> None:
        for missing in ("author", "updated_at"):
            with self.subTest(missing=missing):
                row = {
                    "id": "comment-1",
                    "author": "reviewer",
                    "updated_at": "2026-01-01T00:00:00Z",
                    "selection_reason": "This comment is authoritative.",
                    "body": "Exact authoritative comment.",
                }
                row[missing] = None
                draft_input = self.root / f"draft-missing-{missing}.json"
                draft_input.write_text(json.dumps({
                    "kind": "draft",
                    "draft_id": f"draft-missing-{missing}",
                    "title": "Exact change title",
                    "body": "Exact change body",
                    "selected_comments": [row],
                }), encoding="utf-8")
                with self.assertRaises(GTT.WorkflowError):
                    GTT.contract_wording_build_scope(
                        self.root,
                        "change_request",
                        "standalone",
                        change_request_input=draft_input.name,
                    )

        issue_input = self.root / "issue.json"
        issue_input.write_text(json.dumps({
            "kind": "issue",
            "repo": "castbox/guru-trellis",
            "number": 114,
            "selected_comments": [{
                "id": "comment-1",
                "selection_reason": "This comment is authoritative.",
            }],
        }), encoding="utf-8")
        live = {
            "title": "Exact change title",
            "body": "Exact change body",
            "url": "https://github.com/castbox/guru-trellis/issues/114",
            "updatedAt": "2026-07-17T00:00:00Z",
            "comments": [{
                "id": "comment-1",
                "author": None,
                "updatedAt": "2026-07-17T00:00:00Z",
                "body": "Exact authoritative comment.",
            }],
        }
        with mock.patch.object(GTT, "require_gh_auth"), mock.patch.object(GTT, "issue_view", return_value=live):
            with self.assertRaises(GTT.WorkflowError):
                GTT.contract_wording_build_scope(
                    self.root,
                    "change_request",
                    "standalone",
                    change_request_input=issue_input.name,
                )

    def test_workflow_profiles_cannot_be_narrowed_or_replaced(self) -> None:
        with self.assertRaises(GTT.WorkflowError):
            GTT.contract_wording_build_scope(
                self.root,
                "planning_artifacts",
                "workflow",
                task_dir=self.task,
                explicit_paths=["docs/review.md"],
            )
        with self.assertRaises(GTT.WorkflowError):
            GTT.contract_wording_build_scope(
                self.root,
                "explicit_paths",
                "workflow",
                explicit_paths=["docs/review.md"],
            )
        with self.assertRaises(GTT.WorkflowError):
            GTT.contract_wording_build_scope(
                self.root,
                "change_request",
                "standalone",
                explicit_paths=["docs/review.md"],
                change_request_input="draft.json",
            )

    def test_explicit_paths_reject_unsafe_or_non_markdown_selectors(self) -> None:
        text_path = self.root / "docs/not-markdown.txt"
        text_path.write_text("not markdown\n", encoding="utf-8")
        symlink = self.root / "docs/link.md"
        symlink.symlink_to(self.explicit)
        for value in (
            str(self.explicit.resolve()),
            "../outside.md",
            "docs/not-markdown.txt",
            "docs/link.md",
        ):
            with self.subTest(value=value), self.assertRaises(GTT.WorkflowError):
                GTT.contract_wording_build_scope(
                    self.root,
                    "explicit_paths",
                    "standalone",
                    explicit_paths=[value],
                )

    def test_scanner_covers_the_complete_v2_vocabulary(self) -> None:
        self.explicit.write_text(
            "# Vocabulary\n\n" + " | ".join(GTT.CONTRACT_WORDING_VOCABULARY_V2) + "\n",
            encoding="utf-8",
        )
        scope, contents = GTT.contract_wording_build_scope(
            self.root, "explicit_paths", "standalone", explicit_paths=["docs/review.md"]
        )
        scan = GTT.scan_contract_wording(scope, contents)
        self.assertEqual(
            {hit["term"] for hit in scan["hits"]},
            set(GTT.CONTRACT_WORDING_VOCABULARY_V2),
        )

    def test_all_classifications_and_blocking_projection(self) -> None:
        scope, contents = GTT.contract_wording_build_scope(
            self.root, "explicit_paths", "standalone", explicit_paths=["docs/review.md"]
        )
        scan = GTT.scan_contract_wording(scope, contents)
        for classification in GTT.CONTRACT_WORDING_CLASSIFICATIONS_V1:
            with self.subTest(classification=classification):
                typed_exit = "blocked" if classification == "contract_violation" else "pass"
                payload = self.result(
                    scope,
                    scan,
                    classification=classification,
                    typed_exit=typed_exit,
                )
                self.assertEqual(
                    GTT.contract_wording_structural_errors(self.root, payload, scope, scan),
                    [],
                )
                self.assertEqual(
                    bool(payload["semantic_review"]["unchecked_normative_hits"]),
                    classification == "contract_violation",
                )

    def test_missing_unknown_empty_and_duplicate_classifications_fail_closed(self) -> None:
        scope, contents = GTT.contract_wording_build_scope(
            self.root, "explicit_paths", "standalone", explicit_paths=["docs/review.md"]
        )
        scan = GTT.scan_contract_wording(scope, contents)

        missing = self.result(scope, scan, classification=None)
        self.assertIn(
            "contract_wording_hit_classification_incomplete",
            GTT.contract_wording_structural_errors(self.root, missing, scope, scan),
        )

        unknown = self.result(scope, scan)
        unknown["semantic_review"]["classifications"][0]["classification"] = "unknown"
        unknown["facts_sha256"] = GTT.context_digest({
            key: value for key, value in unknown.items() if key != "facts_sha256"
        })
        self.assertIn(
            "unknown_contract_wording_classification",
            GTT.contract_wording_structural_errors(self.root, unknown, scope, scan),
        )

        empty = self.result(scope, scan)
        empty["semantic_review"]["classifications"][0]["reason"] = ""
        empty["facts_sha256"] = GTT.context_digest({
            key: value for key, value in empty.items() if key != "facts_sha256"
        })
        self.assertIn(
            "empty_contract_wording_classification_reason",
            GTT.contract_wording_structural_errors(self.root, empty, scope, scan),
        )

        duplicate = self.result(scope, scan)
        duplicate["semantic_review"]["classifications"].append(
            dict(duplicate["semantic_review"]["classifications"][0])
        )
        duplicate["facts_sha256"] = GTT.context_digest({
            key: value for key, value in duplicate.items() if key != "facts_sha256"
        })
        self.assertIn(
            "duplicate_contract_wording_classification",
            GTT.contract_wording_structural_errors(self.root, duplicate, scope, scan),
        )

    def test_content_hash_change_invalidates_prior_scope_scan_and_gate(self) -> None:
        scope, contents = GTT.contract_wording_build_scope(
            self.root, "explicit_paths", "standalone", explicit_paths=["docs/review.md"]
        )
        scan = GTT.scan_contract_wording(scope, contents)
        payload = self.result(scope, scan)
        self.explicit.write_text("# Review\n\nThe contract now has one exact value.\n", encoding="utf-8")
        current_scope, current_contents = GTT.contract_wording_build_scope(
            self.root, "explicit_paths", "standalone", explicit_paths=["docs/review.md"]
        )
        current_scan = GTT.scan_contract_wording(current_scope, current_contents)
        errors = GTT.contract_wording_structural_errors(
            self.root, payload, current_scope, current_scan
        )
        self.assertIn("contract_wording_scope_stale", errors)
        self.assertIn("contract_wording_scan_stale", errors)

    def test_three_exit_invariants_and_unique_routes(self) -> None:
        interface = json.loads((PACKAGE_ROOT / "interface.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {item["id"]: item["consumer"] for item in interface["external_exits"]},
            {
                "pass": {"kind": "workflow", "id": "guru-contract-wording-pass-router"},
                "content_changed": {"kind": "workflow", "id": "guru-contract-wording-change-router"},
                "blocked": {"kind": "stop", "id": "contract-wording-blocked"},
            },
        )
        scope, contents = GTT.contract_wording_build_scope(
            self.root, "explicit_paths", "standalone", explicit_paths=["docs/review.md"]
        )
        scan = GTT.scan_contract_wording(scope, contents)
        current_hash = scope["items"][0]["content_sha256"]
        revision = {
            "revision_id": "revision-1",
            "locator": "docs/review.md",
            "before_sha256": "0" * 64,
            "after_sha256": current_hash,
            "reason": "The wording was rewritten to one exact contract.",
            "mutation_authority": "standalone user-authorized file edit",
            "rescan_sha256": scan["scan_sha256"],
        }
        changed = self.result(
            scope,
            scan,
            typed_exit="content_changed",
            revisions=[revision],
        )
        self.assertEqual(
            GTT.contract_wording_structural_errors(self.root, changed, scope, scan),
            [],
        )
        wrong_pass = self.result(scope, scan, revisions=[revision])
        self.assertIn(
            "contract_wording_pass_has_unconsumed_revision",
            GTT.contract_wording_structural_errors(self.root, wrong_pass, scope, scan),
        )
        wrong_changed = self.result(scope, scan, typed_exit="content_changed")
        self.assertIn(
            "contract_wording_content_changed_requires_revision",
            GTT.contract_wording_structural_errors(self.root, wrong_changed, scope, scan),
        )

    def test_live_issue_mutation_binds_confirmed_payload_preimage_and_reread_result(self) -> None:
        issue_input = self.root / "issue-mutation.json"
        issue_input.write_text(json.dumps({
            "kind": "issue",
            "repo": "castbox/guru-trellis",
            "number": 114,
            "selected_comments": [],
        }), encoding="utf-8")
        live = {
            "title": "Exact change title",
            "body": "Exact rewritten body",
            "url": "https://github.com/castbox/guru-trellis/issues/114",
            "updatedAt": "2026-07-17T08:00:00Z",
            "comments": [],
        }
        with mock.patch.object(GTT, "require_gh_auth"), mock.patch.object(GTT, "issue_view", return_value=live):
            scope, contents = GTT.contract_wording_build_scope(
                self.root,
                "change_request",
                "standalone",
                change_request_input=issue_input.name,
            )
        scan = GTT.scan_contract_wording(scope, contents)
        body_item = next(item for item in scope["items"] if item["field"] == "body")
        revision = {
            "revision_id": "revision-1",
            "locator": body_item["id"],
            "before_sha256": "0" * 64,
            "after_sha256": body_item["content_sha256"],
            "reason": "The issue body was rewritten to one exact contract.",
            "mutation_authority": "The user confirmed the exact issue body payload.",
            "rescan_sha256": scan["scan_sha256"],
            "change_request_mutation": {
                "source_identity": body_item["source_identity"],
                "locator": body_item["id"],
                "field": "body",
                "preimage_sha256": "0" * 64,
                "confirmed_content_sha256": body_item["content_sha256"],
                "reread_content_sha256": body_item["content_sha256"],
                "source_updated_at": body_item["updated_at"],
            },
        }
        payload_digest = GTT.context_digest([GTT.context_digest({
            "source_identity": body_item["source_identity"],
            "locator": body_item["id"],
            "field": "body",
            "preimage_sha256": "0" * 64,
            "content_sha256": body_item["content_sha256"],
        })])
        result = GTT.contract_wording_derive_result(
            "change_request",
            "standalone",
            scope,
            scan,
            {
                "generated_at": "2026-07-17T08:01:00Z",
                "semantic_review": {
                    "revisions": [revision],
                    "classifications": [],
                    "ai_review_gate": {
                        "status": "passed",
                        "reviewer": "package-test-reviewer",
                        "summary": "The exact confirmed payload and live reread result were reviewed.",
                        "reviewed_scan_sha256": scan["scan_sha256"],
                        "checked_dimensions": {
                            name: True for name in GTT.CONTRACT_WORDING_REVIEW_DIMENSIONS
                        },
                    },
                },
                "human_confirmation": {
                    "status": "confirmed",
                    "confirmed_by": "user",
                    "confirmed_at": "2026-07-17T07:59:00Z",
                    "reason": "The user confirmed the exact issue body payload.",
                    "confirmed_payload_sha256": payload_digest,
                },
                "typed_exit": "content_changed",
            },
        )
        self.assertEqual(GTT.contract_wording_structural_errors(self.root, result, scope, scan), [])

        missing = json.loads(json.dumps(result))
        del missing["semantic_review"]["revisions"][0]["change_request_mutation"]
        missing["facts_sha256"] = GTT.context_digest({
            key: value for key, value in missing.items() if key != "facts_sha256"
        })
        self.assertIn(
            "change_request_live_mutation_evidence_missing",
            GTT.contract_wording_structural_errors(self.root, missing, scope, scan),
        )

        stale_result = json.loads(json.dumps(result))
        stale_result["semantic_review"]["revisions"][0]["change_request_mutation"]["source_updated_at"] = "2026-07-17T07:00:00Z"
        stale_result["facts_sha256"] = GTT.context_digest({
            key: value for key, value in stale_result.items() if key != "facts_sha256"
        })
        self.assertIn(
            "change_request_mutation_result_binding_mismatch",
            GTT.contract_wording_structural_errors(self.root, stale_result, scope, scan),
        )


if __name__ == "__main__":
    unittest.main()
