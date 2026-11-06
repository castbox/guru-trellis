"""Public carrier admission with real Draft planning, gates and transactions.

Only the external GitHub/Git effects use the original stateful fixture ports.
"""
from contextlib import chdir
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("publication_carrier_fixture", PACKAGE / "tests/test_early_draft.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
owner = fixture.owner


class SingleRead(io.StringIO):
    def __init__(self, content):
        super().__init__(content)
        self.reads = 0

    def read(self, *args, **kwargs):
        self.reads += 1
        if self.reads > 1:
            raise AssertionError("A public stdin carrier was consumed more than once.")
        return super().read(*args, **kwargs)


class PublicationCarrierTests(unittest.TestCase):
    setUp = fixture.EarlyDraftPublication.setUp
    github = fixture.EarlyDraftPublication.github
    mutate = fixture.EarlyDraftPublication.mutate
    public = fixture.EarlyDraftPublication.public

    def entry(self, module, command, argv, stdin=None):
        spec = importlib.util.spec_from_file_location("publication_carrier_" + module, PACKAGE / "runtime" / (module + ".py"))
        entry = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(entry)
        stream = SingleRead(stdin) if stdin is not None else io.StringIO("")
        with patch.object(sys, "stdin", stream):
            result = entry.run(PACKAGE, {"id": command}, ["--root", str(self.f.repo), *argv])
        if stdin is not None:
            self.assertEqual(stream.reads, 1)
        return result

    def review(self):
        return {"schema_version": "1.0", "skill_id": PACKAGE.name,
                "review": {"status": "passed", "summary": "Reviewed this exact early Draft and its remaining evidence."},
                "route": {"typed_exit": "draft_published"}}

    def test_draft_preview_carriers_match_and_preserve_old_file_forms(self):
        public = self.public()
        encoded = json.dumps(public)
        path = Path(self.f.write("publication-carrier.json", public))
        link = self.f.repo / "publication-carrier-link.json"
        link.symlink_to(path)
        with chdir(self.f.repo):
            contexts = [self.entry("check", "preview-task-delivery-publication", ["--input", carrier], stdin)
                        for carrier, stdin in [(encoded, None), (str(path), None), (os.path.relpath(path, self.f.repo), None), (str(link), None), ("-", encoded)]]
        self.assertTrue(all(context == contexts[0] for context in contexts))
        self.assertEqual(contexts[0]["typed_exit"], "preview")
        self.assertEqual(owner.preview(self.f.repo, str(path)), contexts[0])
        self.assertEqual(self.effects, [])
        self.assertIsNone(self.f.projection.resolve(self.f.key)["publication_result"])

    def test_public_stdin_pipeline_uses_original_private_state_readers(self):
        public = self.public()
        encoded = json.dumps(public)
        review = json.dumps(self.review())
        private_reader = owner.read_json
        with patch.object(owner, "read_json", wraps=private_reader) as reads:
            recorded = self.entry("record", "record-task-delivery-publication-gate", ["--input", "-", "--review-input", review], encoded)
            gate = recorded["gate"]
            checked = self.entry("check", "check-task-delivery-publication-gate", ["--input", "-", "--gate", gate], encoded)
            published = self.entry("execute", "execute-task-delivery-publication", ["--input", "-", "--gate", gate], encoded)
        self.assertEqual(checked["status"], "passed")
        self.assertEqual(published["exit_id"], "draft_published")
        self.assertEqual(self.effects, ["push", "create"])
        self.assertTrue(self.pr["isDraft"])
        self.assertIsNone(self.f.projection.resolve(self.f.key)["publication_result"])
        locators = [str(call.args[0]) for call in reads.call_args_list]
        self.assertTrue(any(value.endswith("task.json") for value in locators))
        self.assertTrue(any(value.endswith(".gate.json") for value in locators))
        self.assertTrue(any("/guru-publish-task-delivery/" in value and not value.endswith(".gate.json") for value in locators))
        self.assertFalse(set(locators) & {encoded, review, "-"})
        # The private file reader does not acquire public carrier semantics.
        with self.assertRaises(owner.WorkflowError) as error:
            private_reader('{"private_state":"inline is not a locator"}')
        self.assertEqual(error.exception.code, "invalid_json")

    def test_formal_selector_consumes_input_once_and_review_stdin_recovers_same_draft(self):
        public = self.public()
        encoded = json.dumps(public)
        context = self.entry("check", "preview-task-delivery-publication", ["--input", encoded])
        review_path = self.f.write("carrier-review.json", self.review())
        published = self.entry("invoke", "invoke-guru-publish-task-delivery", ["--input", "-", "--review-input", review_path, "--confirmed-preview-sha256", context["confirmation_identity"]], encoded)
        recovered = self.entry("invoke", "invoke-guru-publish-task-delivery", ["--input", encoded, "--review-input", "-"], json.dumps(self.review()))
        self.assertEqual(published["exit_id"], "draft_published")
        self.assertEqual(published, recovered)
        self.assertEqual(self.effects, ["push", "create"])

    def test_invalid_public_carriers_keep_parameter_diagnostics(self):
        from runtime.io import CommandError
        with self.assertRaises(CommandError) as empty_input_error:
            self.entry("invoke", "invoke-guru-publish-task-delivery", ["--input", "", "--review-input", "{}"])
        self.assertEqual((empty_input_error.exception.code, empty_input_error.exception.field_path), ("invalid_json", "input"))
        with self.assertRaises(CommandError) as input_error:
            self.entry("check", "preview-task-delivery-publication", ["--input", "{" ])
        self.assertEqual((input_error.exception.code, input_error.exception.field_path), ("invalid_json", "input"))
        with self.assertRaises(CommandError) as review_error:
            self.entry("record", "record-task-delivery-publication-gate", ["--input", json.dumps(self.public()), "--review-input", "-"], "{")
        self.assertEqual((review_error.exception.code, review_error.exception.field_path), ("invalid_json", "review_input"))

    def test_legacy_formal_selector_passes_the_same_single_stdin_object(self):
        public = {"profile": "legacy_history_verification", "root": str(self.f.repo),
                  "key": {"task_id": "flow-task", "lifecycle_generation": 0}, "task_ref": self.f.task_ref,
                  "fact_refs": [{"repo_ref": "example/repo", "pr_number": 41, "reviewed_head": self.f.head,
                                 "target_branch": "main", "head_branch": "feat/flow"}]}
        with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 1, "", "Unavailable")):
            result = self.entry("invoke", "invoke-guru-publish-task-delivery", ["--input", "-"], json.dumps(public))
        self.assertEqual(result["exit_id"], "unverified_legacy_history")
        self.assertEqual(self.effects, [])


if __name__ == "__main__":
    unittest.main()
