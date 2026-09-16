from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from referencing import Registry, Resource
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import eval_support, native_adapter
from adapters.eval.intake_authoring import FACTS_PATH, INTAKE_SKILLS, validate_intake_trace

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]


class IntakeProjectionTests(unittest.TestCase):
    def test_actual_model_projection_and_closed_reads(self):
        # Exercise the real projection/context/helper. Only installed fixture setup
        # is replaced; this test performs no preset apply, Git write or native call.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            execution = root / "execution"
            workdir = execution / "workdir"
            workdir.mkdir(parents=True)
            package = SKILLS / "packages" / INTAKE_SKILLS[-1]
            fixture = json.loads((package / "evals/files/standard-intake-source.json").read_text())
            (workdir / "source.json").write_text(json.dumps(fixture))
            owner = root / "owner"
            required = list(fixture["repository_files"]) + [".trellis/spec/workflow/semantic-retrieval.md"]
            for relative, content in fixture["repository_files"].items():
                path = owner / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            spec = owner / required[-1]
            spec.parent.mkdir(parents=True)
            spec.write_bytes((REPO / required[-1]).read_bytes())
            facts = owner / FACTS_PATH
            facts.parent.mkdir(parents=True, exist_ok=True)
            facts.write_text(json.dumps({"source": fixture["source"], "required_reads": required}))
            for relative in ("docs/unrelated.md", ".trellis/guru-team/skills/consumers/example.json"):
                path = owner / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("not declared")
            target = owner / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
            interface = json.loads((package / "interface.json").read_text())
            request = {"schema_version": "1.0", "skill_id": INTAKE_SKILLS[-1],
                "case_id": "projection-test",
                "prompt": "Review the supplied source request.", "files": ["source.json"],
                "native_execution_mode": "semantic_authoring", "native_authoring_flow": "standard_intake",
                "native_execution_adapter": "codex", "model_id": "gpt-5.6-sol",
                "package_root": str(package), "workdir": str(workdir),
                "runtime_target": str(REPO / ".trellis/guru-team/scripts/bash/run-skill-command.sh"),
                "interface": {"public_invocation": interface["public_contracts"]["invocation"]}}
            model = root / "model"
            model.mkdir()
            with mock.patch.object(native_adapter, "stage_owner_execution", return_value=(package, target, {})), \
                    mock.patch.object(native_adapter.tempfile, "mkdtemp", return_value=str(model)):
                result = native_adapter.build_context(request, "codex")
            context, _, _, _, protocol_path, _, _, _, thread, stop, _ = result
            try:
                protocol = json.loads(protocol_path.read_text())
                inventory = protocol["intake_read_paths"]
                projection = Path(protocol["projection_root"])
                repository = Path(protocol["repository_projection_root"])
                materialized = {str(p) for base in (projection, repository, model / "evidence/case")
                                for p in base.rglob("*") if p.is_file()}
                self.assertEqual(materialized, {p for paths in inventory.values() for p in paths})
                self.assertEqual({p.relative_to(repository).as_posix() for p in repository.rglob("*") if p.is_file()},
                                 {FACTS_PATH, *required})
                self.assertNotIn("needed schemas/examples", context)
                self.assertNotIn("expected_exit", context)
                self.assertNotIn("legacy assets, not additional", context)
                for path in materialized:
                    self.assertFalse(set(Path(path).parts) & {"examples", "evals", ".runtime"})
                for skill in INTAKE_SKILLS:
                    projected = projection if skill == INTAKE_SKILLS[-1] else projection / "flow-packages" / skill
                    for name in ("SKILL.md", "references/contract.md", "interface.json"):
                        self.assertEqual((projected / name).read_bytes(), (SKILLS / "packages" / skill / name).read_bytes())
                    self.assertFalse((projected / "examples").exists())
                    self.assertFalse((projected / "schemas/public-input.schema.json").exists())
                self.assertFalse((projection / "schemas/public-ready-output.schema.json").exists())
                self.assertFalse((projection / "schemas/public-proposed-draft-input.schema.json").exists())
                for skill in INTAKE_SKILLS[-2:]:
                    projected = projection if skill == INTAKE_SKILLS[-1] else projection / "flow-packages" / skill
                    self.assertIn(str(projected / "schemas/review-invocation.schema.json"), inventory["skill_contract"])
                wording_schema = json.loads((projection / "flow-packages" / INTAKE_SKILLS[3] /
                                             "schemas/review-invocation.schema.json").read_text())
                Draft202012Validator(wording_schema).validate({
                    "profile": "change_request", "mode": "workflow", "owner_result": {},
                    "change_request": {"source_kind": "issue", "identity": fixture["source"]["url"],
                                       "title": fixture["source"]["title"], "body": fixture["source"]["body"],
                                       "updated_at": fixture["source"]["updated_at"]},
                })
                args = [sys.executable, "-B", protocol["helper_path"]]
                for flag, field in (("trace", "trace_path"), ("request-sha256", "request_sha256"),
                        ("projection-root", "projection_root"), ("repository-root", "repository_projection_root"),
                        ("sandbox-root", "model_root"), ("request-fifo", "request_fifo"),
                        ("response-fifo", "response_fifo"), ("skill-sha256", "skill_sha256"),
                        ("wrapper-sha256", "wrapper_sha256")):
                    args.extend(["--" + flag, protocol[field]])
                args.extend(["--flow", "standard_intake", "read"])
                for kind, paths in inventory.items():
                    for path in paths:
                        read = subprocess.run([*args, "--kind", kind, "--path", path], capture_output=True, timeout=10)
                        self.assertEqual(read.returncode, 0, read.stderr)
                        self.assertEqual(read.stdout, Path(path).read_bytes())
                # Ordinary linked-example/extra-file reads remain denied even if
                # a file is present. Existence cannot grant helper or trace access.
                denied = [("skill_contract", projection / "examples/public-ready-output.json"),
                          ("skill_contract", projection / "schemas/unused.schema.json"),
                          ("owner_file", repository / "docs/unrelated.md"),
                          ("case_file", model / "native-context.txt"),
                          ("skill_contract", projection / "evals/evals.json"),
                          ("owner_file", repository / ".trellis/.runtime/private.json")]
                for kind, path in denied:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("must not be read")
                    read = subprocess.run([*args, "--kind", kind, "--path", str(path)], capture_output=True, timeout=10)
                    self.assertNotEqual(read.returncode, 0)
                    self.assertEqual(read.stdout, b"")
                    without_flow = args[:-3] + ["read"]
                    read = subprocess.run([*without_flow, "--kind", kind, "--path", str(path)],
                                          capture_output=True, timeout=10)
                    self.assertNotEqual(read.returncode, 0)
                    self.assertEqual(read.stdout, b"")
                    Path(protocol["intake_receipts_path"]).write_text('[{}]')
                    event = {"kind": "read", "target_kind": kind, "path": str(path),
                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                             "request_sha256": protocol["request_sha256"]}
                    payload = {"request_sha256": protocol["request_sha256"], "events": [event, {"kind": "command"}]}
                    with self.assertRaisesRegex(ValueError, "outside public projection"):
                        validate_intake_trace(payload, protocol, "")
            finally:
                stop.set()
                thread.join(timeout=3)

    def test_other_projection_modes_keep_existing_examples(self):
        for skill in (INTAKE_SKILLS[-1], "guru-maintain-architecture-baseline", "guru-check-task"):
            interface = json.loads((SKILLS / "packages" / skill / "interface.json").read_text())
            self.assertTrue(any(path.parts[0] == "examples" for path in eval_support.public_projection_assets(interface)))
        source = eval_support.qualification_trace_helper_source()
        self.assertIn("INTAKE_READ_PATHS = {}", source)

    def test_selected_schema_references_are_self_contained(self):
        def references(value):
            if isinstance(value, dict):
                if "$ref" in value:
                    yield value["$ref"]
                for child in value.values():
                    yield from references(child)
            elif isinstance(value, list):
                for child in value:
                    yield from references(child)

        for skill in INTAKE_SKILLS:
            package = SKILLS / "packages" / skill
            interface = json.loads((package / "interface.json").read_text())
            assets = eval_support.intake_projection_assets(interface) | eval_support.public_projection_shared_assets(interface)
            for path in assets:
                if path.suffix == ".json" and path != Path("interface.json"):
                    with self.subTest(skill=skill, schema=str(path)):
                        source = (SKILLS if path.parts[0] == "consumers" else package) / path
                        schema = json.loads(source.read_text())
                        resource = Resource.from_contents(schema)
                        resolver = Registry().with_resource(schema["$id"], resource).resolver(schema["$id"])
                        for ref in references(schema):
                            self.assertTrue(ref.startswith("#"), f"Unprojected schema dependency: {ref}")
                            resolver.lookup(ref)


if __name__ == "__main__":
    unittest.main()
