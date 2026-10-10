from pathlib import Path
import json
import unittest
from jsonschema import Draft202012Validator

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]

class RootContractTest(unittest.TestCase):
    def test_all_examples_match_selected_schemas(self):
        interface=json.loads((PACKAGE/"interface.json").read_text())
        for row in interface["public_contracts"]["input"]["profiles"] + interface["public_contracts"]["outputs"]:
            example=json.loads((PACKAGE/row["example"]["path"]).read_text())
            schema=json.loads((PACKAGE/row["schema"]["path"]).read_text())
            Draft202012Validator(schema).validate(example)
        Draft202012Validator(json.loads((PACKAGE/"schemas/semantic-result.schema.json").read_text())).validate(json.loads((PACKAGE/"examples/semantic-result.json").read_text()))

    def test_projections_use_independent_consumer_schemas(self):
        interface=json.loads((PACKAGE/"interface.json").read_text())
        for projection in interface["public_contracts"]["projections"]:
            output=next(row for row in interface["public_contracts"]["outputs"] if row["exit_id"]==projection["exit_id"])
            consumer=next(row for row in interface["public_contracts"]["consumer_inputs"] if row["id"]==projection["consumer_input_id"])
            self.assertEqual("direct",projection["operation"])
            Draft202012Validator(json.loads((SKILLS/consumer["contract"]["path"]).read_text())).validate(json.loads((PACKAGE/output["example"]["path"]).read_text()))

if __name__=="__main__": unittest.main()
