"""Integration checks use real Git checkouts and native unittest subprocesses."""
import json
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest
from unittest import mock

from runtime_diagnostic import WrapperObserver

import targeted_ci as ci


class DriverIntegrationTest(unittest.TestCase):
    def git(self, root, *args):
        return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.STDOUT).decode().strip()

    def test_independent_commits_continue_and_preserve_raw_results(self):
        with tempfile.TemporaryDirectory(prefix="Guru CI space ") as temporary:
            root = Path(temporary)
            repo = root / "source"
            repo.mkdir()
            self.git(repo, "init")
            self.git(repo, "config", "user.email", "ci@example.invalid")
            self.git(repo, "config", "user.name", "CI fixture")
            tests = repo / ci.TEST_ROOT
            tests.mkdir(parents=True)
            lock = repo / "trellis/skills/guru-team/runtime/requirements.lock"
            lock.parent.mkdir(parents=True)
            lock.write_text("", encoding="utf-8")
            test = tests / "test_behavior.py"
            test.write_text("import unittest\nclass Behavior(unittest.TestCase):\n def test_value(self):\n  self.assertEqual(1, 2, 'baseline value')\n", encoding="utf-8")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-m", "baseline")
            baseline = self.git(repo, "rev-parse", "HEAD")
            test.write_text(test.read_text().replace("assertEqual(1, 2", "assertEqual(2, 2"), encoding="utf-8")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-m", "candidate")
            candidate = self.git(repo, "rev-parse", "HEAD")
            output = root / "diagnostics"
            output.mkdir()
            report = {"driver_sha": "integration-driver", "targets": []}
            # This fixture proves tests/continuation only. Missing Bash explicitly
            # leaves installation incomplete; it must never become a passing job.
            ci.execute_targets(report, str(repo), [("baseline", baseline), ("candidate", candidate)],
                               root / "work", output, ["test_behavior.py"], None)
            first, second = report["targets"]
            self.assertEqual([row["sha"] for row in report["targets"]], [baseline, candidate])
            self.assertNotEqual(first["workspace"], second["workspace"])
            self.assertEqual(first["tests"]["failures"], 1)
            self.assertEqual(second["tests"]["failures"], 0)
            self.assertEqual(first["tests"]["outcomes"][0]["id"], "test_behavior.Behavior.test_value")
            codes = [next(step["returncode"] for step in row["steps"] if step["stage"] == "tests")
                     for row in report["targets"]]
            self.assertEqual(codes, [1, 0])
            summary = ci.summarize(report, "test_behavior.Behavior.test_value", "1 != 2 : baseline value")
            self.assertEqual(report["returncode"], 1)
            self.assertFalse(report["comparison"]["baseline_matched"])
            self.assertIn(candidate, summary)
            saved = json.loads((output / "candidate/result.json").read_text())
            self.assertEqual(saved["tests"]["tests_run"], 1)
            self.assertIn("Bash unavailable", saved["execution_error"])
            self.assertEqual(self.git(repo, "rev-parse", "HEAD"), candidate)
            # A collector error must not prevent the independent installation
            # attempt, and installation failures cannot match expected tests.
            with mock.patch.object(ci, "smoke") as smoke:
                def installation_failure(steps, target, workspace, python, bash, sha):
                    steps.call("smoke-preset", [python, "-c", "raise SystemExit(7)"],
                               target, "installation")
                smoke.side_effect = installation_failure
                report = {"driver_sha": "integration-driver", "targets": []}
                ci.execute_targets(report, str(repo), [("baseline", baseline), ("candidate", candidate)],
                                   root / "work-install", root / "diagnostics-install",
                                   ["test_behavior.py"], ci.find_bash())
            self.assertEqual(smoke.call_count, 2)
            for row in report["targets"]:
                self.assertEqual(row["runtime_diagnostic"]["collector_status"], "failed")
                self.assertEqual(row["runtime_diagnostic"]["fixture_status"], "not_executed")
                self.assertEqual(row["status"], "failed")
                self.assertEqual(row["steps"][-1]["stage"], "smoke-preset")
                self.assertEqual(row["steps"][-1]["returncode"], 7)
            ci.summarize(report, "test_behavior.Behavior.test_value", "1 != 2 : baseline value")
            self.assertEqual(report["returncode"], 1)
            self.assertFalse(report["comparison"]["baseline_matched"])

    def test_nested_package_script_resolves_target_local_pnpm(self):
        lock = json.loads((ci.HERE.parent / "trellis/presets/guru-team/source/trellis-source.json").read_text())
        with tempfile.TemporaryDirectory(prefix="Guru local pnpm space ") as temporary:
            root = Path(temporary)
            tools = root / "tools"
            installed = ci.run([shutil.which("npm") or "npm", "install", "--prefix", tools,
                                "--no-audit", "--no-fund", lock["package_manager"]], root)
            self.assertEqual(installed.returncode, 0, installed.stdout.decode("utf-8", "replace"))
            package = root / "package"
            package.mkdir()
            (package / "package.json").write_text(json.dumps({"name": "nested-pnpm-fixture",
                "private": True, "scripts": {"outer": "pnpm run inner", "inner": "node probe.cjs"}}))
            (package / "probe.cjs").write_text(
                'require("node:fs").writeFileSync("resolved.json", JSON.stringify({execpath: process.env.npm_execpath}));\n')
            diagnostics = root / "diagnostics"
            diagnostics.mkdir()
            result = {"role": "fixture", "steps": []}
            steps = ci.Steps(diagnostics, result)
            pnpm = tools / "node_modules/pnpm/bin/pnpm.cjs"
            ok, output = steps.call("nested-pnpm", ["node", pnpm, "run", "outer"], package,
                                    path_prepend=tools / "node_modules/.bin")
            self.assertTrue(ok, output)
            resolved = json.loads((package / "resolved.json").read_text())
            self.assertEqual(Path(resolved["execpath"]).resolve(), pnpm.resolve())
            self.assertEqual(result["steps"][0]["returncode"], 0)

    def test_only_exact_assertion_can_exempt_baseline(self):
        baseline = {"role": "baseline", "status": "failed", "steps": [
            {"stage": "tests", "category": "tests", "returncode": 1, "log": "tests.log"}],
            "tests": {"tests_run": 1, "outcomes": [
                {"id": "case.test", "kind": "failure", "message": "specific assertion"}]}}
        candidate = {"role": "candidate", "status": "passed", "steps": []}
        report = {"driver_sha": "driver", "targets": [baseline, candidate]}
        ci.summarize(report, "case.test", "specific assertion")
        self.assertTrue(report["comparison"]["established"])
        self.assertEqual(report["returncode"], 0)
        baseline["tests"]["outcomes"][0]["kind"] = "error"
        ci.summarize(report, "case.test", "specific assertion")
        self.assertFalse(report["comparison"]["established"])
        self.assertEqual(report["returncode"], 1)
        baseline["tests"]["outcomes"][0]["kind"] = "failure"
        candidate["status"] = "failed"
        ci.summarize(report, "case.test", "specific assertion")
        self.assertFalse(report["comparison"]["established"])
        self.assertEqual(report["returncode"], 1)


class SelectionTest(unittest.TestCase):
    def run_selection(self, root, selection):
        output = root / "outcome.json"
        proc = subprocess.run([sys.executable, ci.HERE / "unittest_report.py",
                               "--root", root, "--output", output, selection],
                              cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc.returncode, json.loads(output.read_text(encoding="utf-8"))

    def test_file_selector_loads_only_selected_case_and_retains_id(self):
        with tempfile.TemporaryDirectory(prefix="Guru selector space ") as temporary:
            root = Path(temporary)
            package = root / "outside package"
            package.mkdir()
            test = package / "test_contract.py"
            test.write_text("import unittest\nclass Contract(unittest.TestCase):\n"
                            " def test_selected(self): pass\n"
                            " def test_unselected(self): self.fail('unselected failure')\n", encoding="utf-8")
            code, report = self.run_selection(root, str(test) + "::Contract.test_selected")
            self.assertEqual((code, report["tests_run"], report["errors"], report["failures"]), (0, 1, 0, 0))
            code, report = self.run_selection(root, str(test) + "::Contract.test_unselected")
            self.assertEqual(code, 1)
            self.assertEqual(report["outcomes"], [{"id": "test_contract.Contract.test_unselected",
                "kind": "failure", "message": "unselected failure"}])
            for missing in ("Contract.missing", "Missing.test_selected"):
                code, report = self.run_selection(root, str(test) + "::" + missing)
                self.assertEqual((code, report["errors"]), (1, 1))
            code, report = self.run_selection(root, str(package / "missing.py") + "::Contract.test_selected")
            self.assertEqual((code, report["errors"]), (1, 1))
            test.write_text("import absent_ci_fixture_dependency\n", encoding="utf-8")
            code, report = self.run_selection(root, str(test) + "::Contract.test_selected")
            self.assertEqual((code, report["errors"]), (1, 1))
            self.assertIn("absent_ci_fixture_dependency", report["outcomes"][0]["message"])

    def test_legacy_file_and_module_selection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            test = root / "test_legacy.py"
            test.write_text("import unittest\nclass Legacy(unittest.TestCase):\n def test_ok(self): pass\n", encoding="utf-8")
            for selection in (str(test), "test_legacy.Legacy.test_ok"):
                with self.subTest(selection=selection):
                    code, report = self.run_selection(root, selection)
                    self.assertEqual((code, report["tests_run"]), (0, 1))


class ObserverTest(unittest.TestCase):
    cases = [{"arguments": ["--valid"], "expected_returncode": 0, "expected_output": {"ok": True}},
             {"arguments": ["--invalid"], "expected_returncode": 2, "expected_output": {"code": "schema_mismatch"}}]

    def test_success_keeps_original_results_and_arguments_without_extra_calls(self):
        calls = []
        results = [subprocess.CompletedProcess([], 0, '{"ok":true}', ''),
                   subprocess.CompletedProcess([], 2, '{"code":"schema_mismatch"}', '')]
        run = mock.Mock(side_effect=results)
        observer = WrapperObserver(run, self.cases, calls)
        kwargs = {"cwd": Path("fixture"), "env": {"fixture": "only"}, "text": True,
                  "stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "check": False}
        for index, case in enumerate(self.cases):
            command = ["bash", "/fixture/invoke.sh", *case["arguments"]]
            self.assertIs(observer(command, **kwargs), results[index])
            self.assertEqual(run.call_args, mock.call(command, **kwargs))
        self.assertEqual(run.call_count, 2)
        self.assertEqual([row["supplemental"] for row in calls], [False, False])

    def test_first_failure_records_supplemental_and_retains_original_exception(self):
        for primary in (subprocess.CompletedProcess([], 1, 'original output', 'original stderr'),
                        OSError("original launch failure")):
            with self.subTest(primary=primary):
                calls = []
                second = subprocess.CompletedProcess([], 2, '{"code":"schema_mismatch"}', '')
                run = mock.Mock(side_effect=[primary, second])
                observer = WrapperObserver(run, self.cases, calls)
                command = ["bash", "/fixture/invoke.sh", "--valid"]
                kwargs = {"text": True, "cwd": "original-view"}
                if isinstance(primary, Exception):
                    with self.assertRaises(OSError) as caught:
                        observer(command, **kwargs)
                    self.assertIs(caught.exception, primary)
                    self.assertEqual(calls[0]["exception"]["message"], str(primary))
                else:
                    self.assertIs(observer(command, **kwargs), primary)
                    self.assertEqual(calls[0]["stdout"], "original output")
                    self.assertEqual(calls[0]["stderr"], "original stderr")
                self.assertEqual(run.call_args_list, [mock.call(command, **kwargs),
                    mock.call(["bash", "/fixture/invoke.sh", "--invalid"], **kwargs)])
                self.assertEqual([row["supplemental"] for row in calls], [False, True])
                self.assertEqual(calls[1]["returncode"], 2)


if __name__ == "__main__":
    unittest.main()
