"""Read-only pre-cutover closure for the #434 package candidate."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


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
        old_ids = set(RETIRED) | {"check-workspace-boundary", "prepare-task.sh", "start-task.sh", "finish-work.sh"}
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
