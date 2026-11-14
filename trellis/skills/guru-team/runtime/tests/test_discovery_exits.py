"""Public exit discovery against actual source contracts and routing consumers."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path


RUNTIME = Path(__file__).resolve().parents[1]
REPOSITORY = RUNTIME.parents[3]
sys.path.insert(0, str(RUNTIME.parent))
from runtime.schema import validate_json  # noqa: E402
from runtime.discovery import select_authoring_profile  # noqa: E402


class ExitDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.directory = tempfile.TemporaryDirectory()
        cls.root = Path(cls.directory.name)
        shutil.copytree(REPOSITORY / "trellis", cls.root / "trellis", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        cls.wrapper = cls.root / "trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh"
        cls.routing = cls.root / "trellis/workflows/guru-team/references/routing.md"
        bootstrap = subprocess.run(
            [sys.executable, str(cls.root / "trellis/skills/guru-team/runtime/bootstrap.py"), "--repo", str(cls.root),
             "--runtime-assets", str(cls.root / "trellis/skills/guru-team/runtime"), "--python", sys.executable, "--json"],
            text=True, capture_output=True, check=False,
        )
        if bootstrap.returncode:
            raise AssertionError(bootstrap)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.directory.cleanup()

    def query(self, skill: str, *exits: str) -> subprocess.CompletedProcess[str]:
        argv = [str(self.wrapper), "--root", str(self.root), "--mode", "source", "--skill", skill, "--json"]
        for exit_id in exits:
            argv.extend(("--exit", exit_id))
        return subprocess.run(argv, text=True, capture_output=True, check=False)

    def successful(self, skill: str, exit_id: str) -> dict:
        result = self.query(skill, exit_id)
        self.assertEqual(result.returncode, 0, result)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    @contextmanager
    def changed(self, path: Path):
        original = path.read_bytes()
        try:
            yield
        finally:
            path.write_bytes(original)

    def test_skill_consumer_exposes_target_preconditions_and_usable_producer_schema(self) -> None:
        result = self.successful("guru-review-change-request", "supplement_context")
        self.assertEqual(result["consumer"], {"kind": "skill", "id": "guru-discover-change-context"})
        self.assertTrue(result["entry"]["locator"].endswith("guru-discover-change-context/SKILL.md"))
        self.assertTrue(result["entry"]["entry_preconditions"])
        self.assertEqual(result["entry"]["input"]["kind"], "structured_json")
        package = self.root / result["contract_root"]
        output = result["output_contract"]
        example = json.loads((package / output["example"]["path"]).read_text())
        validate_json(example, package / output["schema"]["path"], "output")
        self.assertEqual(result["projection"]["operation"], "rename")
        selected = select_authoring_profile(result["consumer_input"]["contract"], example)
        self.assertEqual(selected["profile_id"], "issue_readiness_supplement")
        self.assertEqual(set(selected["authoring_fields"]), {"profile"})
        self.assertNotIn("private_artifacts", result)

    def test_conditional_router_is_returned_without_choosing_a_branch(self) -> None:
        result = self.successful("guru-review-contract-wording", "pass")
        self.assertEqual(result["consumer"]["id"], "guru-contract-wording-pass-router")
        self.assertIn("change_request", result["entry"]["body"])
        self.assertIn("delivery_planning_artifacts", result["entry"]["body"])
        self.assertNotIn("## Mandatory Skills", result["entry"]["body"])

    def test_stop_consumer_keeps_its_own_behavior(self) -> None:
        result = self.successful("guru-author-task-plan", "blocked")
        self.assertEqual(result["consumer"], {"kind": "stop", "id": "task-plan-author-blocked"})
        self.assertIn("task-plan-author-blocked", result["entry"]["locator"])
        self.assertTrue(result["entry"]["body"])

    def test_consumer_schema_locator_resolves_package_and_shared_roots(self) -> None:
        for skill, exit_id, shared in (
            ("guru-author-task-plan", "plan_ready", False),
            ("guru-upgrade-tools", "tools_upgraded", True),
            ("guru-bind-task-session", "session_resumed", False),
        ):
            with self.subTest(skill=skill):
                result = self.successful(skill, exit_id)
                package = self.root / result["contract_root"]
                interface = json.loads((package / "interface.json").read_text())
                declared = next(row for row in interface["public_contracts"]["consumer_inputs"] if row["id"] == result["consumer_input"]["id"])
                self.assertEqual(result["consumer_input"], declared)
                schema_root = self.root / "trellis/skills/guru-team" if shared else package
                schema_path = schema_root / declared["contract"]["path"]
                self.assertEqual(self.root / result["consumer_schema_locator"], schema_path)
                output = result["output_contract"]
                example = json.loads((package / output["example"]["path"]).read_text())
                validate_json(example, schema_path, "actual_consumer")

    def test_instruction_only_exit_keeps_conversation_contract(self) -> None:
        result = self.successful("guru-orchestrate-issue-sequence", "chain_completed")
        self.assertEqual(result["consumer"]["kind"], "stop")
        self.assertEqual(result["entry"]["body"], result["output_contract"]["contract"])
        self.assertNotIn("projection", result)
        self.assertNotIn("consumer_input", result)

    def test_unknown_and_multiple_exit_arguments_stop(self) -> None:
        for exits, code in ((["not_an_exit"], "unknown_exit"), (["blocked", "plan_ready"], "multiple_exits")):
            with self.subTest(exits=exits):
                result = self.query("guru-author-task-plan", *exits)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertEqual(json.loads(result.stderr)["code"], code)

    def test_normal_missing_and_duplicate_graph_declarations_stop(self) -> None:
        original = self.routing.read_text()
        marker = next(line for line in original.splitlines() if '"skill":"guru-author-task-plan","exit":"plan_ready"' in line)
        for text in (original.replace(marker, ""), original + "\n" + marker + "\n"):
            with self.subTest(duplicate=text.endswith(marker + "\n")), self.changed(self.routing):
                self.routing.write_text(text)
                result = self.query("guru-author-task-plan", "plan_ready")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertEqual(json.loads(result.stderr)["code"], "workflow_graph_invalid")

    def test_missing_reference_does_not_fall_back_to_inline(self) -> None:
        workflow = self.root / "trellis/workflows/guru-team/workflow.md"
        with self.changed(workflow):
            workflow.write_text("# Old inline workflow\n" + self.routing.read_text())
            result = self.query("guru-author-task-plan", "plan_ready")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stderr)["code"], "workflow_graph_invalid")

    def test_legal_target_evolution_updates_the_same_public_query(self) -> None:
        interface_path = self.root / "trellis/skills/guru-team/packages/guru-author-task-plan/interface.json"
        schema_path = interface_path.parent / "consumers/workflow/plan-ready-2.0.schema.json"
        new_schema_path = schema_path.with_name("plan-ready-current.schema.json")
        old = "guru-task-plan-ready-router"
        new = "guru-task-plan-ready-current-router"
        with self.changed(interface_path), self.changed(self.routing), self.changed(schema_path):
            schema_path.rename(new_schema_path)
            try:
                interface = json.loads(interface_path.read_text())
                for item in interface["external_exits"]:
                    if item["id"] == "plan_ready":
                        item["consumer"]["id"] = new
                for item in interface["public_contracts"]["consumer_inputs"]:
                    if item["id"] == "plan_ready":
                        item["consumer"]["id"] = new
                        item["contract"]["path"] = new_schema_path.relative_to(interface_path.parent).as_posix()
                interface_path.write_text(json.dumps(interface))
                self.routing.write_text(self.routing.read_text().replace(old, new))
                result = self.successful("guru-author-task-plan", "plan_ready")
                self.assertEqual(result["consumer"]["id"], new)
                self.assertTrue(result["entry"]["locator"].endswith("#" + new))
                self.assertEqual(self.root / result["consumer_schema_locator"], new_schema_path)
            finally:
                new_schema_path.unlink(missing_ok=True)

    def test_output_projection_update_omission_stops_the_query(self) -> None:
        interface_path = self.root / "trellis/skills/guru-team/packages/guru-author-task-plan/interface.json"
        with self.changed(interface_path):
            interface = json.loads(interface_path.read_text())
            output = next(item for item in interface["public_contracts"]["outputs"] if item["exit_id"] == "plan_ready")
            output["consumer_use_ids"] = ["missing_projection"]
            interface_path.write_text(json.dumps(interface))
            result = self.query("guru-author-task-plan", "plan_ready")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertEqual(json.loads(result.stderr)["code"], "unmapped_exit")

    def test_plain_skill_contract_discovery_keeps_all_original_contracts(self) -> None:
        result = self.query("guru-sync-base")
        self.assertEqual(result.returncode, 0, result)
        payload = json.loads(result.stdout)
        self.assertIn("private_artifacts", payload)
        self.assertNotIn("consumer", payload)


class InstalledExitDiscoveryTests(unittest.TestCase):
    def test_actual_installed_shared_consumer_schema_is_readable(self) -> None:
        root = Path(os.environ.get("GURU_TEST_INSTALLED_ROOT", str(REPOSITORY))).resolve()
        result = subprocess.run(
            [str(root / ".trellis/guru-team/scripts/bash/discover-skill-contract.sh"), "--root", str(root),
             "--mode", "installed", "--skill", "guru-upgrade-tools", "--exit", "tools_upgraded", "--json"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result)
        payload = json.loads(result.stdout)
        schema = root / payload["consumer_schema_locator"]
        self.assertTrue(payload["consumer_schema_locator"].startswith(".trellis/guru-team/skills/consumers/stop/"))
        package = root / payload["contract_root"]
        output = payload["output_contract"]
        example = json.loads((package / output["example"]["path"]).read_text())
        validate_json(example, schema, "actual_installed_consumer")

    def test_actual_matching_installed_query_uses_installed_reference(self) -> None:
        root = Path(os.environ.get("GURU_TEST_INSTALLED_ROOT", str(REPOSITORY))).resolve()
        result = subprocess.run(
            [str(root / ".trellis/guru-team/scripts/bash/discover-skill-contract.sh"), "--root", str(root),
             "--mode", "installed", "--skill", "guru-author-task-plan", "--exit", "plan_ready", "--json"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["consumer"]["id"], "guru-task-plan-ready-router")
        self.assertTrue(payload["entry"]["locator"].startswith(".trellis/guru-team/references/routing.md#"))


if __name__ == "__main__":
    unittest.main()
