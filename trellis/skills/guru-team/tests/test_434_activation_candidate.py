"""Read-only pre-cutover closure for the #434 package candidate."""
from __future__ import annotations

import json
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml


SKILLS = Path(__file__).resolve().parents[1]
ROOT = SKILLS.parents[2]
PACKAGES = SKILLS / "packages"
sys.path.insert(0, str(SKILLS))
from runtime import validate as package_validator  # noqa: E402
from runtime.installed import workflow_facts  # noqa: E402


RETIRED = {
    "guru-create-task-workspace", "guru-review-task-publication", "guru-finalize-task",
    "guru-merge-task-pr", "guru-restore-archived-task",
}
NEW = {
    "guru-create-issue", "guru-create-task", "guru-activate-task",
    "guru-ensure-task-checkout", "guru-establish-task-identity",
    "guru-establish-task-branch-binding", "guru-rebind-task-branch",
}
RETIRED_CONSUMER_SCHEMAS = {
    "guru-stage0-invocation-workspace-mutation-1.0",
    "guru-finalize-task-workflow-published-input-1.0",
    "guru-finalize-task-stop-blocked-input-1.0",
    "guru-production-review-task-publication-workflow-return-to-task-work-input-1.0",
    "guru-production-review-task-publication-stop-blocked-input-1.0",
    "guru-merge-task-pr-workflow-merged-input-1.0",
    "guru-merge-task-pr-stop-merge-blocked-input-1.0",
    "guru-merge-task-pr-stop-closure-mismatch-input-1.0",
}
OLD_GRAPH_HEAD = "bab8cfcd534692735b9240b25dd8bc63e40a5cb4"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def old_blob(path: str) -> str:
    return subprocess.run(
        ["git", "show", f"{OLD_GRAPH_HEAD}:{path}"], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout


def graph_entries(registry: dict, old: bool) -> dict:
    entries = {}
    for row in registry["skills"]:
        if row["state"] != "active":
            continue
        path = f"trellis/skills/guru-team/{row['interface']}"
        interface = json.loads(old_blob(path)) if old else read_json(SKILLS / row["interface"])
        entries[row["id"]] = {**row, "interface_data": interface}
    return entries


class ActivationCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        registry = read_json(SKILLS / "registry.json")
        current = {row["id"] for row in registry["skills"] if row["state"] == "active"}
        self.ids = current - RETIRED | NEW
        self.interfaces = {skill: read_json(PACKAGES / skill / "interface.json") for skill in self.ids}

    def test_installed_finish_graph_executes_current_terminal_cases(self) -> None:
        script = SKILLS / "tests/test_finish_family_integration.py"
        result = subprocess.run(
            [sys.executable, str(script)], cwd=ROOT, capture_output=True, text=True,
            env={**os.environ, "GURU_FINISH_INTEGRATION_MODE": "installed",
                 "GURU_FINISH_INTEGRATION_ROOT": str(ROOT), "PYTHONDONTWRITEBYTECODE": "1"},
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran 6 tests", result.stderr)

    def test_installed_fixed_fork_session_port_supports_task_identity(self) -> None:
        runtime = PACKAGES / "guru-bind-task-session/runtime/invoke.py"
        spec = importlib.util.spec_from_file_location("guru_434_installed_session_probe", runtime)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        port = module.official_port(ROOT)
        for name in ("resolve_context_key", "repository_facts", "resolve_task_identity",
                     "session_path", "record_exists", "read_record", "write_record"):
            self.assertTrue(callable(getattr(port, name, None)), name)

    def test_candidate_projection_binds_exact_fixed_fork_source(self) -> None:
        lock = read_json(ROOT / "trellis/presets/guru-team/source/trellis-source.json")
        self.assertEqual(read_json(ROOT / ".trellis/guru-team/trellis-source.json"), lock)
        contribution = yaml.safe_load(
            (ROOT / "docs/requirements-design-test-contributions/"
             "454-task-lifecycle-gen7-taskid-domain/manifest.yaml")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(contribution["status"], "candidate_pending_review")
        self.assertEqual(contribution["expected_current_version"], "current-main-0.6.17-guru.67")
        for relative in (
            "docs/architecture/contributions/454-task-lifecycle-gen7-taskid-domain.md",
            "docs/requirements-design-test-contributions/454-task-lifecycle-gen7-taskid-domain/design.md",
            "trellis/presets/guru-team/spec/workflow/data-contracts.md",
            ".trellis/spec/workflow/data-contracts.md",
        ):
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn(lock["commit"], text)

    def test_fixed_fork_context_template_matches_installed_script(self) -> None:
        checkout = os.environ.get("GURU_FIXED_TRELLIS_CHECKOUT")
        if not checkout:
            self.skipTest("set GURU_FIXED_TRELLIS_CHECKOUT for exact fixed-Fork source proof")
        lock = read_json(ROOT / "trellis/presets/guru-team/source/trellis-source.json")
        tree = subprocess.run(
            ["git", "-C", checkout, "rev-parse", f"{lock['commit']}^{{tree}}"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        self.assertEqual(tree, lock["tree"])
        source = subprocess.run(
            ["git", "-C", checkout, "show",
             f"{lock['commit']}:packages/cli/src/templates/trellis/scripts/get_context.py"],
            check=True, capture_output=True,
        ).stdout
        self.assertEqual(source, (ROOT / ".trellis/scripts/get_context.py").read_bytes())
        self.assertIn(b'options.mode in {"phase", "continuation"}', source)
        task_store = subprocess.run(
            ["git", "-C", checkout, "show",
             f"{lock['commit']}:packages/cli/src/templates/trellis/scripts/common/task_store.py"],
            check=True, capture_output=True,
        ).stdout
        self.assertEqual(task_store, (ROOT / ".trellis/scripts/common/task_store.py").read_bytes())

    def test_current_test_index_includes_latest_acceptance_cases(self) -> None:
        index = (ROOT / "docs/test/README.md").read_text(encoding="utf-8")
        self.assertIn("`T434-01..39`", index)
        self.assertNotIn("`T434-01..36`", index)

    def test_official_task_id_and_generic_start_guidance_match_guru_activation(self) -> None:
        source = ROOT / ".trellis/scripts/common/task_store.py"
        self.assertIn("TASK_ID_PATTERN.fullmatch(task_id)", source.read_text(encoding="utf-8"))
        self.assertIn("TASK_ID_PATTERN,", source.read_text(encoding="utf-8"))
        utility = ROOT / ".trellis/scripts/common/task_utils.py"
        self.assertIn('TASK_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")', utility.read_text(encoding="utf-8"))
        for platform in (".agents", ".claude", ".cursor"):
            with self.subTest(platform=platform):
                guide = (ROOT / platform / "skills/trellis-meta/references/local-architecture/task-system.md").read_text(encoding="utf-8")
                self.assertIn("Guru Team uses `guru-activate-task` instead", guide)
                commands = guide.split("## Common Commands", 1)[1].split("```bash", 1)[1].split("```", 1)[0]
                self.assertNotIn("task.py start", commands)
        with tempfile.TemporaryDirectory(prefix="guru-434-task-id-") as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".trellis").mkdir()
            (root / ".trellis/scripts").symlink_to(ROOT / ".trellis/scripts")
            for index, task_id in enumerate(("issue.", "issue.lock", "issue..434")):
                slug = f"valid-{index}"
                result = subprocess.run(
                    [sys.executable, str(ROOT / ".trellis/scripts/task.py"), "create", "candidate",
                     "--description", "TaskId fixture", "--slug", slug, "--task-id", task_id,
                     "--creator", "test", "--assignee", "test", "--no-start"],
                    cwd=root, capture_output=True, text=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, check=False,
                )
                self.assertEqual(result.returncode, 0, (task_id, result.stdout, result.stderr))
                task = root / result.stdout.strip() / "task.json"
                self.assertEqual(json.loads(task.read_text(encoding="utf-8"))["id"], task_id)
            before = sorted((root / ".trellis/tasks").glob("*/task.json"))
            for task_id in ("issue 434", "-issue", "issue/name"):
                result = subprocess.run(
                    [sys.executable, str(ROOT / ".trellis/scripts/task.py"), "create", "candidate",
                     "--description", "TaskId fixture", "--slug", "invalid", "--task-id", task_id,
                     "--creator", "test", "--assignee", "test", "--no-start"],
                    cwd=root, capture_output=True, text=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, check=False,
                )
                self.assertNotEqual(result.returncode, 0, (task_id, result.stdout, result.stderr))
                self.assertIn("--task-id", result.stderr)
                self.assertEqual(sorted((root / ".trellis/tasks").glob("*/task.json")), before)

            derived = subprocess.run(
                [sys.executable, str(ROOT / ".trellis/scripts/task.py"), "create", "candidate",
                 "--description", "TaskId fixture", "--slug", "two words",
                 "--creator", "test", "--assignee", "test", "--no-start"],
                cwd=root, capture_output=True, text=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, check=False,
            )
            self.assertNotEqual(derived.returncode, 0, (derived.stdout, derived.stderr))
            self.assertIn("derived task id must match", derived.stderr)
            self.assertEqual(sorted((root / ".trellis/tasks").glob("*/task.json")), before)

    def test_candidate_adr_id_does_not_reuse_accepted_decision(self) -> None:
        seen: dict[str, Path] = {}
        for path in sorted((ROOT / "docs/architecture/adr").glob("[0-9][0-9][0-9]-*.md")):
            match = re.match(r"# (ADR-\d{3}):", path.read_text(encoding="utf-8"))
            self.assertIsNotNone(match, path)
            decision_id = match.group(1)
            self.assertEqual(path.name[:3], decision_id[-3:], path)
            self.assertNotIn(decision_id, seen, (seen.get(decision_id), path))
            seen[decision_id] = path
        self.assertEqual(seen["ADR-016"].name, "016-task-delivery-lifecycle.md")

    def test_candidate_packages_and_unique_skill_consumers(self) -> None:
        self.assertEqual((len(self.ids), sum(len(i["external_exits"]) for i in self.interfaces.values())),
                         (34, 155))
        for skill, interface in self.interfaces.items():
            outputs = interface["public_contracts"]["outputs"]
            projections = interface["public_contracts"]["projections"]
            inputs = interface["public_contracts"]["consumer_inputs"]
            for exit_row in interface["external_exits"]:
                with self.subTest(skill=skill, exit=exit_row["id"]):
                    self.assertEqual(len([row for row in outputs if row["exit_id"] == exit_row["id"]]), 1)
                    matches = [row for row in projections if row["exit_id"] == exit_row["id"]]
                    self.assertEqual(len(matches), 1)
                    consumer = next(row for row in inputs if row["id"] == matches[0]["consumer_input_id"])
                    self.assertEqual(consumer["consumer"], exit_row["consumer"])
                    if exit_row["consumer"]["kind"] == "skill":
                        self.assertIn(exit_row["consumer"]["id"], self.ids)

    def test_candidate_registry_and_packages_pass_source_validator(self) -> None:
        registry = read_json(SKILLS / "registry.json")
        active = {row["id"] for row in registry["skills"] if row["state"] == "active"}
        self.assertEqual(active, self.ids)
        self.assertTrue(NEW <= active)
        self.assertFalse(RETIRED & active)
        result = package_validator.validate(ROOT, "source")
        self.assertEqual((result["status"], result["active_packages"], result["commands"]),
                         ("passed", 34, 104))

    def test_selected_interface_schema_is_installed(self) -> None:
        registry = read_json(SKILLS / "registry.json")
        selected = {row["interface_schema_id"] for row in registry["skills"] if row["state"] == "active"}
        for schema_id in selected:
            filename = f"skill-interface-{schema_id.rsplit('-', 1)[-1]}.schema.json"
            with self.subTest(schema_id=schema_id):
                self.assertTrue((ROOT / ".trellis/guru-team/skills/schemas" / filename).is_file())
                manifest = read_json(ROOT / ".trellis/guru-team/extension.json")
                self.assertIn(
                    f".trellis/guru-team/skills/schemas/{filename}",
                    {row["path"] for row in manifest["skill_packages"]["files"]},
                )
        installed = package_validator.validate(ROOT, "installed")
        self.assertEqual(installed["status"], "passed", installed)

    def test_entry_and_review_handoffs_do_not_use_retired_consumers(self) -> None:
        change = self.interfaces["guru-review-change-request"]
        branch = self.interfaces["guru-review-branch"]
        self.assertEqual(next(row for row in change["external_exits"] if row["id"] == "ready")["consumer"],
                         {"kind": "workflow", "id": "guru-task-intake-router"})
        self.assertEqual(next(row for row in branch["external_exits"] if row["id"] == "passed")["consumer"],
                         {"kind": "skill", "id": "guru-review-task-delivery"})
        self.assertEqual(next(row for row in branch["external_exits"] if row["id"] == "archived_review_passed")["consumer"],
                         {"kind": "stop", "id": "legacy-archived-review-disposition-required"})
        for skill, exit_id in (("guru-review-change-request", "ready"),
                               ("guru-review-branch", "archived_review_passed")):
            interface = self.interfaces[skill]
            output = next(row for row in interface["public_contracts"]["outputs"] if row["exit_id"] == exit_id)
            projection = next(row for row in interface["public_contracts"]["projections"] if row["exit_id"] == exit_id)
            consumer = next(row for row in interface["public_contracts"]["consumer_inputs"]
                            if row["id"] == projection["consumer_input_id"])
            self.assertEqual(projection["operation"], "direct")
            value = read_json(PACKAGES / skill / output["example"]["path"])
            for contract in (output["schema"], consumer["contract"]):
                Draft202012Validator(read_json(PACKAGES / skill / contract["path"])).validate(value)
        passed = read_json(PACKAGES / "guru-review-branch/examples/public-passed-output.json")
        authored = read_json(PACKAGES / "guru-review-branch/examples/public-delivery-review-authoring.json")
        self.assertEqual({key: authored[key] for key in ("task_ref", "branch_review_commit")},
                         {key: passed[key] for key in ("task_ref", "branch_review_commit")})
        Draft202012Validator(read_json(PACKAGES / "guru-review-task-delivery/schemas/public-delivery-review-input.schema.json")).validate(authored)

    def test_publication_qualification_outputs_route_to_delivery_review(self) -> None:
        for skill, prefix in (("guru-qualify-normal-scenario", "normal-scenario"),
                              ("guru-qualify-solution-mechanism", "solution-mechanism")):
            package = PACKAGES / skill
            publication_input = read_json(package / "examples/public-publication-candidate-set-input.json")
            self.assertEqual(publication_input["profile"], "publication_candidate_set")
            self.assertEqual(publication_input["caller"], "guru-review-task-delivery")
            Draft202012Validator(read_json(package / "schemas/public-publication-candidate-set-input.schema.json")).validate(publication_input)
            for exit_id, example, producer_schema, consumer in (
                ("classified", "public-classified-output.json", "public-classified-output.schema.json", f"{prefix}-classified-router.schema.json"),
                ("mechanism_revision_required", "public-mechanism-revision-required-output.json",
                 "public-mechanism-revision-required-output.schema.json", f"{prefix}-mechanism-router.schema.json"),
            ):
                with self.subTest(skill=skill, exit_id=exit_id):
                    output = read_json(package / "examples" / example)
                    output["profile"] = publication_input["profile"]
                    output["resume_target"] = publication_input["caller"]
                    output["candidate_results"][0]["candidate_ref"] = publication_input["candidate_refs"][0]
                    producer = Draft202012Validator(read_json(package / "schemas" / producer_schema))
                    router = Draft202012Validator(read_json(SKILLS / "consumers/workflow/production" / consumer))
                    producer.validate(output)
                    router.validate(output)
                    retired = {**output, "resume_target": "guru-review-task-publication"}
                    self.assertFalse(router.is_valid(retired))

    def test_complete_old_and_new_graphs_pass_but_mixed_graphs_fail(self) -> None:
        old = graph_entries(json.loads(old_blob("trellis/skills/guru-team/registry.json")), True)
        current = graph_entries(read_json(SKILLS / "registry.json"), False)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / "workflow.md"
            for label, text, entries, expected in (
                ("pinned-old", old_blob("trellis/workflows/guru-team/workflow.md"), old, True),
                ("current", (ROOT / "trellis/workflows/guru-team/workflow.md").read_text(encoding="utf-8"), current, True),
                ("old-workflow-new-packages", old_blob("trellis/workflows/guru-team/workflow.md"), current, False),
                ("new-workflow-old-packages", (ROOT / "trellis/workflows/guru-team/workflow.md").read_text(encoding="utf-8"), old, False),
            ):
                with self.subTest(graph=label):
                    workflow.write_text(text, encoding="utf-8")
                    errors: list[str] = []
                    facts = workflow_facts(root, workflow, entries, True, errors)
                    self.assertEqual(not errors, expected, (label, facts, errors[:5]))
                    if expected:
                        self.assertEqual(facts["invoke_markers"], len([
                            row for row in entries.values() if row.get("workflow_integration_state", "integrated") == "integrated"
                        ]))

    def test_current_graph_rejects_retired_or_extra_markers(self) -> None:
        current = graph_entries(read_json(SKILLS / "registry.json"), False)
        text = (ROOT / "trellis/workflows/guru-team/workflow.md").read_text(encoding="utf-8")
        extras = (
            '<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"ready_for_merge","consumer":{"kind":"workflow","id":"old-router"}} -->',
            '<!-- guru-skill-invoke: {"skill":"guru-finalize-task","required":true} -->',
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / "workflow.md"
            for extra in extras:
                with self.subTest(marker=extra):
                    workflow.write_text(text + "\n" + extra + "\n", encoding="utf-8")
                    errors: list[str] = []
                    workflow_facts(root, workflow, current, True, errors)
                    self.assertTrue(any("undeclared" in error for error in errors), errors)

    def test_old_public_ids_have_explicit_dispositions_and_real_replacements(self) -> None:
        old_ids = set(RETIRED) | RETIRED_CONSUMER_SCHEMAS | {
            "check-workspace-boundary", "prepare-task.sh", "start-task.sh", "finish-work.sh",
        }
        for skill in RETIRED:
            old_commands = json.loads(old_blob(f"trellis/skills/guru-team/packages/{skill}/commands.json"))
            old_ids.update(row["id"] for row in old_commands["commands"])
        workspace = json.loads(old_blob("trellis/skills/guru-team/packages/guru-create-task-workspace/interface.json"))

        def visit(value: object) -> None:
            if isinstance(value, dict):
                for key, item in value.items():
                    if key in {"id", "schema_id"} and isinstance(item, str) and "task-workspace" in item:
                        old_ids.add(item)
                    visit(item)
            elif isinstance(value, list):
                for item in value:
                    visit(item)

        visit(workspace)
        migration = (ROOT / "trellis/presets/guru-team/MIGRATION-434.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| `([^`]+)` \| `(replaced\([^)]*\)|retired_without_replacement)`", migration, re.M)
        dispositions = dict(rows)
        self.assertEqual(len(rows), len(dispositions))
        self.assertEqual(set(dispositions), old_ids)
        new_ids = set(self.ids) | {"check-task-checkout-boundary"}
        for skill, interface in self.interfaces.items():
            new_ids.update(row["id"] for row in read_json(PACKAGES / skill / "commands.json")["commands"])
            new_ids.update(row["consumer"]["id"] for row in interface["external_exits"])
        for old_id, disposition in rows:
            if disposition.startswith("replaced("):
                self.assertIn(disposition[len("replaced("):-1], new_ids, old_id)


if __name__ == "__main__":
    unittest.main()
