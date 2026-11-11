"""Current public wrappers: a real exact candidate before independent committed Review."""
import importlib.util
import json
from pathlib import Path
import unittest

SKILLS = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("draft_delivery_flow", SKILLS / "packages/guru-check-task/tests/test_delivery_flow.py")
flow_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flow_module)


class EarlyDraftCommit(unittest.TestCase):
    def setUp(self):
        self.flow = flow_module.DeliveryFlow()
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        from runtime.delivery_projection.adapter import authority_ref
        from runtime.delivery_projection.gates import rework
        rework(self.flow.projection, self.flow.key, "check", "implementation",
               authority_ref(self.flow.repo / "requirements.md", self.flow.repo), ["check", "full_review", "readiness"])
        self.base = self.flow.git("rev-parse", "main").strip()

    def test_clean_draft_profile_cannot_prepare_a_dirty_commit(self):
        f=self.flow
        (f.repo/"app.txt").write_text("pending dirty increment\n")
        before=f.git("rev-parse","HEAD")
        public={"profile":"delivery_pre_review_committed_reentry","mode":"workflow","task_ref":f.task_ref,"delivery_key":f.key,"base_ref":self.base}
        result=f.wrapper("guru-create-task-commit","prepare-task-commit.sh","--input",f.write("clean-prepare.json",public),"--candidate-json",f.write("clean-prepare-owner.json",{}),success=False)
        self.assertEqual("invalid_arguments",result["code"])
        self.assertEqual(before,f.git("rev-parse","HEAD"))
        self.assertFalse((f.repo/".trellis/.runtime/guru-team/task-commit-plans").exists())
        self.assertEqual("pending dirty increment\n",(f.repo/"app.txt").read_text())

    def test_real_no_check_commit_stdout_loss_and_clean_reentry(self):
        f = self.flow
        (f.repo / "app.txt").write_text("early draft increment\n")
        (f.repo / "unrelated.txt").write_text("parallel work\n")
        public = {"profile":"delivery_pre_review_commit", "mode":"workflow", "task_ref":f.task_ref, "delivery_key":f.key, "base_ref":self.base}
        package = SKILLS / "packages/guru-create-task-commit"
        message = json.loads((package / "examples/task-commit-candidate.json").read_text())["message"]
        authoring = {"message":message, "ai_review":{"status":"passed","summary":"Bounded scope and sensitive-content review; final Check remains pending.","evidence":["Exact proposed diff and minimum self-checks."]},
            "path_classifications":[{"path":path,"category":"task-reviewed" if path=="app.txt" else "unrelated-preserved","reason":"Reviewed implementation." if path=="app.txt" else "Preserve parallel work and public lifecycle metadata.","coverage_source":"Early bounded content review."} for path in ("app.txt","unrelated.txt",f.task_ref+"/task.json")]}
        prepared=f.wrapper(package.name,"prepare-task-commit.sh","--input",f.write("early.json",public),"--candidate-json",f.write("early-authoring.json",authoring))
        self.assertEqual("pre_review_committed",prepared["typed_exit"])
        candidate=json.loads((f.repo/prepared["candidate_artifact"]).read_text())
        self.assertNotIn("check_result_id",candidate)
        self.assertNotIn("phase2_commit_anchor",candidate["git"])
        result=f.wrapper(package.name,"invoke.sh","--candidate-artifact",prepared["candidate_artifact"])
        self.assertEqual("pre_review_committed",result["exit_id"])
        self.assertEqual("app.txt",f.git("diff","--name-only",f.head,result["branch_review_commit"]).strip())
        self.assertEqual(result,f.wrapper(package.name,"invoke.sh","--candidate-artifact",prepared["candidate_artifact"]))
        self.assertEqual("parallel work\n",(f.repo/"unrelated.txt").read_text())
        selected=f.projection.resolve(f.key)
        self.assertEqual("implementing",selected["phase"])
        self.assertIsNone(selected["results"]["check"])
        self.assertIsNone(selected["results"]["full_review"])
        # Preserve the dirty-path unrelated work before selecting clean reentry.
        (f.repo/"unrelated.txt").unlink()
        public["profile"]="delivery_pre_review_committed_reentry"
        semantic={"status":"passed","summary":"Retain the real integration/fix commit.","evidence":["Complete fixed range and committed Planning reviewed."]}
        clean=f.wrapper(package.name,"invoke.sh","--input",f.write("clean.json",public),"--owner-result",f.write("clean-owner.json",semantic))
        self.assertEqual(result,clean)
        # Commit does not manufacture either upstream gate.
        self.assertIsNone(f.projection.resolve(f.key)["results"]["check"])
        old={**public,"profile":"delivery_draft_committed_reentry"}
        rejected=f.wrapper(package.name,"invoke.sh","--input",f.write("old.json",old),"--owner-result",f.write("old-owner.json",semantic),success=False)
        self.assertEqual("schema_mismatch",rejected["code"])


if __name__ == "__main__":
    unittest.main()
