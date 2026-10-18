"""Real installed continuation extractor/hook with public Task and Delivery APIs.

This tests emitted native context, not whether a host AI completed the workflow.
"""
from __future__ import annotations
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
REPO = Path(__file__).resolve().parents[4]
WORKFLOW = REPO / "trellis/workflows/guru-team/workflow.md"
sys.path.insert(0, str(REPO / "trellis/skills/guru-team"))
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref

class ActiveTaskContinuationIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.scripts = Path(os.environ.get("GURU_UPSTREAM_DELIVERY_SCRIPTS", ""))
        self.assertTrue((self.scripts / "common/delivery_store.py").is_file(), "Explicit reviewed installed candidate required")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-qb", "main"], cwd=self.root, check=True)
        shutil.copytree(self.scripts, self.root / ".trellis/scripts", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(WORKFLOW, self.root / ".trellis/workflow.md")
        (self.root / ".trellis/.developer").write_text("continuation-test\n")
        self.environment = {key: value for key, value in os.environ.items() if key not in {"CODEX_THREAD_ID", "TRELLIS_CONTEXT_ID"}}
        self.environment["TRELLIS_CONTEXT_ID"] = "codex_continuation-fixture"
        result = subprocess.run([sys.executable, str(self.root / ".trellis/scripts/task.py"), "create", "Current continuation",
            "--description", "Delivery continuation evidence", "--slug", "continuation", "--task-id", "continuation-task", "--schema-version", "2.0", "--source-json", '{"kind":"no_issue"}', "--base-branch", "main", "--no-start"],
            cwd=self.root, env=self.environment, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.task = next((self.root / ".trellis/tasks").glob("*/task.json")).parent
        self.ref = self.task.relative_to(self.root).as_posix()
        result = subprocess.run([sys.executable, str(self.root / ".trellis/scripts/task.py"), "start", self.ref],
            cwd=self.root, env=self.environment, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        hook_source = self.scripts.parents[1] / "shared-hooks/inject-workflow-state.py"
        hook = self.root / ".codex/hooks/inject-workflow-state.py"
        hook.parent.mkdir(parents=True)
        shutil.copy2(hook_source, hook)

    def hook(self, prompt):
        result = subprocess.run([sys.executable, str(self.root / ".codex/hooks/inject-workflow-state.py")], cwd=self.root,
            input=json.dumps({"cwd": str(self.root), "session_id": "continuation-fixture", "prompt": prompt}),
            env=self.environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]

    def test_no_delivery_remains_bound_without_an_empty_delivery(self):
        text = self.hook("继续")
        self.assertIn("continuation-task (no_current_delivery)", text)
        self.assertIn("Load the sole continuation", text)
        self.assertEqual(text, self.hook("确认继续"))
        self.assertEqual(json.loads((self.task / "task.json").read_text())["deliveries"], [])

    def test_selected_delivery_planning_and_implementation_use_same_native_entry(self):
        code = """import json,sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from runtime.delivery_projection.adapter import DeliveryProjection,authority_ref
root=Path.cwd();p=DeliveryProjection(root,sys.argv[2]);scope=authority_ref(p.task_dir/'prd.md',root);p.scope(scope)
key={'task_id':'continuation-task','lifecycle_generation':0,'delivery_id':'43134b50-2c8b-4d70-b114-218a735a82e2'}
p.apply({'api_version':'1.0','operation':'create_delivery','key':key,'owner_role':'creation','owner_id':'guru-create-delivery','scope_ref':{'authority':scope,'anchors':['scope']},'profile':'pull_request'});p.select(key)
print(json.dumps(key))"""
        result = subprocess.run([sys.executable, "-c", code, str(REPO / "trellis/skills/guru-team"), self.ref],
            cwd=self.root, env=self.environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("continuation-task (planning)", self.hook("继续"))
        # Use actual public transition in the selected task; no status write.
        key = json.loads(result.stdout)
        plan = self.task / "deliveries" / key["delivery_id"]
        plan.mkdir(parents=True, exist_ok=True)
        (plan / "design.md").write_text("selected Delivery plan\n")
        code = """import json,sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from runtime.delivery_projection.adapter import DeliveryProjection,authority_ref
p=DeliveryProjection(Path.cwd(),sys.argv[2]);key=json.loads(sys.argv[3]);d=p.resolve(key)
r={'result_id':'planning-test','owner_role':'planning','owner_id':'guru-activate-delivery','outcome':'accepted','scope_ref':d['scope_ref'],'plan_ref':authority_ref(p.planning_directory(key)/'design.md',p.root),'candidate':None,'predecessor_result_id':None,'obligations':[],'evidence':[d['scope_ref']['authority']]}
p.apply({'api_version':'1.0','operation':'record_gate','key':key,'owner_role':'planning','owner_id':'guru-activate-delivery','expected_phase':'planning','result':r})"""
        result = subprocess.run([sys.executable, "-c", code, str(REPO / "trellis/skills/guru-team"), self.ref, json.dumps(key)],
            cwd=self.root, env=self.environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("continuation-task (implementing)", self.hook("确认继续"))
        self.assertNotIn("status", json.loads((self.task / "task.json").read_text()))

    def test_installed_extractor_reads_one_current_owner_contract(self):
        path = self.scripts / "common/continuation_contract.py"
        spec = importlib.util.spec_from_file_location("installed_continuation", path)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        body = module.extract_continuation_contract(WORKFLOW)
        self.assertEqual(body.count("### Guru caller continuation"), 1)
        self.assertIn("no_current_delivery", body)
        self.assertIn("guru-activate-delivery", body)
        self.assertIn("phase does not substitute for the gate", body)
        self.assertNotIn("guru-activate-task", body)
        self.assertIn("Local dependency gaps block only their true dependent work", body)
if __name__ == "__main__":
    unittest.main()
