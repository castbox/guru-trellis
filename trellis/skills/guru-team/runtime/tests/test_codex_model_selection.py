from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import native_adapter
from runtime import eval_runner as runner

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
SKILL = "guru-review-change-request"


class CodexModelSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.package, self.interface, self.row = runner.package_context(SKILLS, SKILL)
        self.corpus, _ = runner.corpus(SKILLS, self.package, self.interface)
        self.post_owner = next(case for case in self.corpus["evals"]
                               if case.get("native_execution_mode", "post_owner") == "post_owner")

    def args(self, *extra, adapter="codex"):
        return runner.parser().parse_args([
            "run-skill-evals", "--root", str(REPO), "--mode", "source",
            "--skill", SKILL, "--adapter", adapter, "--case", self.post_owner["id"],
            "--run-root", str(self.root / "run"), *extra,
        ])

    def request(self, args, case=None):
        return runner.eval_request(args, self.package, self.interface, self.row,
                                   case or self.post_owner, self.root / "workdir",
                                   "a" * 64, runner.runtime_target(REPO))

    def argv(self, request):
        return native_adapter.native_argv(
            "codex", "codex", request, "unchanged context", self.root / "context.txt",
            self.root / "native-request.json", self.root / "projection",
        )

    def test_cli_to_staged_request_to_native_argv(self):
        observed = []

        def adapter(skills, descriptor, request_path):
            request = json.loads(request_path.read_text())
            observed.append((request, self.argv(request)[0]))
            return runner.adapter_failure(request_path, "unit transport only")

        for extra in ((), ("--codex-model", "gpt-5.6-sol")):
            with self.subTest(extra=extra), mock.patch.object(runner, "call_adapter", side_effect=adapter):
                result = runner.run(REPO, SKILLS, self.args(*extra))
                self.assertEqual(result["status"], "execution_error")
        default_request, default_argv = observed[0]
        selected_request, selected_argv = observed[1]
        self.assertNotIn("model_id", default_request)
        self.assertNotIn("--model", default_argv)
        self.assertEqual(selected_request, {**default_request, "model_id": "gpt-5.6-sol"})
        index = selected_argv.index("--model")
        self.assertEqual(selected_argv[index + 1], "gpt-5.6-sol")
        self.assertEqual(selected_argv[:index] + selected_argv[index + 2:], default_argv)

    def test_pinned_semantic_cases_are_unchanged(self):
        for case in self.corpus["evals"]:
            if case.get("native_execution_mode") != "semantic_authoring":
                continue
            with self.subTest(case=case["id"]):
                original = copy.deepcopy(case)
                default = self.request(self.args(), case)
                explicit = self.request(self.args("--codex-model", "different-unpinned-model"), case)
                self.assertEqual(explicit, default)
                self.assertEqual(case, original)
                self.assertEqual(self.argv(explicit), self.argv(default))
                argv, _ = self.argv(explicit)
                self.assertEqual(argv[argv.index("--model") + 1], case["model_id"])

    def test_rejects_blank_and_non_codex_before_staging(self):
        selections = [("codex", value) for value in ("", " ", "\t\r\n")]
        selections += [(adapter, "gpt-5.6-sol") for adapter in ("shared", "claude", "cursor")]
        for adapter, value in selections:
            with self.subTest(adapter=adapter, value=value), \
                    mock.patch.object(runner, "discover") as discover, \
                    mock.patch.object(runner, "call_adapter") as dispatch:
                with self.assertRaises(runner.CommandError):
                    runner.run(REPO, SKILLS, self.args("--codex-model", value, adapter=adapter))
                discover.assert_not_called()
                dispatch.assert_not_called()
                self.assertFalse((self.root / "run").exists())

    def test_request_schema_in_source_and_installed_layouts(self):
        source = SKILLS / "schemas/skill-eval-adapter-request.schema.json"
        installed = self.root / ".trellis/guru-team/skills/schemas" / source.name
        installed.parent.mkdir(parents=True)
        shutil.copy2(source, installed)
        for schema in (source, installed):
            for adapter in runner.ADAPTERS:
                for mode in (None, "post_owner"):
                    with self.subTest(schema=schema, adapter=adapter, mode=mode):
                        request = self.request(self.args(adapter=adapter))
                        if mode is None:
                            request.pop("native_execution_mode")
                        runner.validate_instance(request, schema, "request")
                        request["model_id"] = "gpt-5.6-sol"
                        if adapter == "codex":
                            runner.validate_instance(request, schema, "request")
                        else:
                            with self.assertRaises(runner.CommandError):
                                runner.validate_instance(request, schema, "request")
            semantic = next(case for case in self.corpus["evals"]
                            if case.get("native_execution_mode") == "semantic_authoring")
            request = self.request(self.args("--codex-model", "other-model"), semantic)
            runner.validate_instance(request, schema, "request")
            for field in ("model_id", "native_execution_adapter"):
                missing = dict(request)
                missing.pop(field)
                with self.assertRaises(runner.CommandError):
                    runner.validate_instance(missing, schema, "request")

    def test_post_owner_still_rejects_authoring_fields(self):
        schema = SKILLS / "schemas/skill-eval-adapter-request.schema.json"
        for field, value in (("native_execution_adapter", "codex"),
                             ("native_authoring_flow", "standard_intake")):
            with self.subTest(field=field):
                request = self.request(self.args("--codex-model", "gpt-5.6-sol"))
                request[field] = value
                with self.assertRaises(runner.CommandError):
                    runner.validate_instance(request, schema, "request")

    def test_qualification_dispatch_accepts_different_explicit_option(self):
        args = self.args("--codex-model", "different-unpinned-model")
        args.skill = runner.QUALIFICATION_SKILL
        package, interface, _ = runner.package_context(SKILLS, args.skill)
        corpus, _ = runner.corpus(SKILLS, package, interface)
        args.case = corpus["evals"][0]["id"]
        with mock.patch.object(runner, "qualification_run", return_value={"status": "unsupported"}) as dispatch:
            self.assertEqual(runner.run(REPO, SKILLS, args), {"status": "unsupported"})
        dispatch.assert_called_once()
        self.assertEqual(dispatch.call_args.args[8]["production_gate"]["model_id"], runner.QUALIFICATION_MODEL)


if __name__ == "__main__":
    unittest.main()
