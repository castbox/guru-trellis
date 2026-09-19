import json
import unittest
from pathlib import Path

class ContractTest(unittest.TestCase):
    def test_interface_declares_unique_routes_and_no_duplicate_binding_store(self):
        p = Path(__file__).resolve().parents[1]
        interface = json.loads((p / "interface.json").read_text())
        exits = [x["id"] for x in interface["external_exits"]]
        self.assertEqual(len(exits), len(set(exits)))
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertEqual(interface["public_contracts"]["input"]["profiles"][-1]["example"]["path"], "examples/public-manual-recovery-input.json")
        self.assertEqual(interface.get("private_artifacts", []), [])

    def test_switch_contract_exposes_explicit_source_and_target_fields(self):
        p = Path(__file__).resolve().parents[1]
        for name in ("public-input.schema.json", "semantic-result.schema.json"):
            schema = json.loads((p / "schemas" / name).read_text())
            self.assertIn("current_task_ref", schema["properties"])
            self.assertIn("target_task_ref", schema["properties"])


class ProfileContractTest(unittest.TestCase):
    def test_each_profile_example_validates_and_matches_discriminator(self):
        from jsonschema import Draft202012Validator
        package = Path(__file__).resolve().parents[1]
        interface = json.loads((package / 'interface.json').read_text())
        paths = set()
        for profile in interface['public_contracts']['input']['profiles']:
            with self.subTest(profile=profile['id']):
                example = json.loads((package / profile['example']['path']).read_text())
                schema = json.loads((package / profile['schema']['path']).read_text())
                Draft202012Validator(schema).validate(example)
                self.assertEqual(example[profile['discriminator']['field']], profile['discriminator']['value'])
                paths.add(profile['example']['path'])
                if profile['id'] == 'switch_task':
                    self.assertNotEqual(example['current_task_ref'], example['target_task_ref'])
        self.assertEqual(len(paths), 5)

    def test_schema_accepts_only_the_five_profile_route_pairs(self):
        from jsonschema import Draft202012Validator
        package = Path(__file__).resolve().parents[1]
        validator = Draft202012Validator(json.loads((package / 'schemas/semantic-result.schema.json').read_text()))
        value = json.loads((package / 'examples/semantic-result.json').read_text())
        routes = {'resume_current_task': 'resume', 'rebind_missing_session': 'rebind', 'switch_task': 'switch', 'reactivate_rebind': 'reactivate', 'manual_recovery': 'manual_recovery'}
        for profile, expected in routes.items():
            for route in routes.values():
                with self.subTest(profile=profile, route=route):
                    self.assertEqual(validator.is_valid({**value, 'profile': profile, 'route': route}), route == expected)


class PublicOutputContractTest(unittest.TestCase):
    def test_public_output_excludes_runtime_binding_identity(self):
        package = Path(__file__).resolve().parents[1]
        schema = json.loads((package / 'schemas/public-output.schema.json').read_text())
        route = json.loads((package / 'consumers/workflow/production/session-binding-route.schema.json').read_text())
        for value in (schema, route):
            self.assertNotIn('session_id', value.get('properties', {}))
            self.assertNotIn('binding_id', value.get('properties', {}))
            self.assertNotIn('session_id', value.get('required', []))
            self.assertNotIn('binding_id', value.get('required', []))
