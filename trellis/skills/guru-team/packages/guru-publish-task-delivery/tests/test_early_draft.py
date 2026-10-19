"""Production Publication actions against stateful external-provider ports.

GitHub effects are local provider fixtures; these tests do not prove real PRs.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]
spec=importlib.util.spec_from_file_location("draft_pub_flow",SKILLS/"packages/guru-check-task/tests/test_delivery_flow.py")
flow_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(flow_module)
spec=importlib.util.spec_from_file_location("draft_pub_owner",PACKAGE/"runtime/owner.py")
owner=importlib.util.module_from_spec(spec);spec.loader.exec_module(owner)


class EarlyDraftPublication(unittest.TestCase):
    def setUp(self):
        self.f=flow_module.DeliveryFlow();self.f.delivery_profile="pull_request";self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.f.repo=self.f.repo.resolve()
        from runtime.delivery_projection.gates import rework
        from runtime.delivery_projection.adapter import authority_ref
        rework(self.f.projection,self.f.key,"check","implementation",authority_ref(self.f.repo/"requirements.md",self.f.repo),["check","full_review","readiness"])
        self.base=self.f.git("rev-parse","main").strip();self.remote=None;self.pr=None;self.effects=[];self.drop=None
        self.addCleanup(sys.path.remove,str(PACKAGE/"runtime"));sys.path.insert(0,str(PACKAGE/"runtime"))
        self.addCleanup(patch.stopall)
        patch.dict(sys.modules,{"owner":owner}).start()
        patch.object(owner,"repository_identity",return_value="example/repo").start()
        patch.object(owner,"remote_head",side_effect=lambda *args:self.remote).start()
        patch.object(owner,"gh_json",side_effect=self.github).start()
        patch.object(owner,"_run",side_effect=self.mutate).start()

    def github(self,root,argv):
        if argv[:2]==["pr","list"]:return [dict(self.pr)] if self.pr else []
        if argv[:2]==["pr","view"]:return dict(self.pr)
        self.fail(f"Unexpected provider read: {argv}")

    def mutate(self,root,argv,**kwargs):
        # Only external Git/GitHub writes are replaced. All Planning, identity,
        # state, gate, preview and transaction functions are production code.
        if argv[:2]==["git","push"]:
            self.effects.append("push");self.remote=argv[-1].split(":")[0]
            if self.pr:self.pr["headRefOid"]=self.remote
        elif argv[:3]==["gh","pr","create"]:
            self.effects.append("create");self.pr={"number":42,"url":"https://github.com/example/repo/pull/42","state":"OPEN","isDraft":True,"title":argv[argv.index("--title")+1],"body":argv[argv.index("--body")+1],"headRefName":"feat/flow","headRefOid":self.remote,"baseRefName":"main","headRepositoryOwner":{"login":"example"}}
        elif argv[:3]==["gh","pr","edit"]:
            self.effects.append("edit");self.pr.update(title=argv[argv.index("--title")+1],body=argv[argv.index("--body")+1])
        elif argv[:3]==["gh","pr","ready"]:
            self.effects.append("draft" if "--undo" in argv else "ready");self.pr["isDraft"]="--undo" in argv
        else:
            return subprocess.run(argv,cwd=root,text=True,capture_output=True)
        if self.drop==self.effects[-1]:
            self.drop=None
            raise owner.WorkflowError("Provider mutation succeeded; stdout was lost.",code="external_command_failed")
        return subprocess.CompletedProcess(argv,0,"","")

    def public(self):
        return {"profile":"delivery_draft_publish","mode":"workflow","task_ref":self.f.task_ref,"delivery_key":self.f.key,"base_ref":self.base,"candidate_head":self.f.head,"pr_title":"提前反馈：当前候选","pr_body":"HEAD最小自检已执行。完整Check/Review待完成；组合候选未执行。\nRefs #636"}

    def invoke(self,public):
        path=self.f.write("publish.json",public)
        context=owner.plan_from_input(self.f.repo,public)
        exit=owner.expected_publication_exit(self.f.repo,public)
        review={"schema_version":"1.0","skill_id":PACKAGE.name,"review":{"status":"passed","summary":"Reviewed the exact Draft/Ready action, payload and evidence limits."},"route":{"typed_exit":exit}}
        return owner.invoke(self.f.repo,path,self.f.write("publish-review.json",review),context.get("confirmation_identity"))

    def test_create_output_loss_recovers_same_draft_without_final_publication(self):
        public=self.public();self.drop="create"
        first=self.invoke(public)
        self.assertEqual("resume_publication",first["exit_id"])
        resumed=self.invoke({"profile":"delivery_same_plan_resume","mode":"workflow","task_ref":self.f.task_ref,"delivery_key":self.f.key,"transaction_ref":first["transaction_ref"]})
        self.assertEqual("draft_published",resumed["exit_id"])
        self.assertEqual(resumed,self.invoke(public));self.assertEqual(["push","create"],self.effects)
        self.assertTrue(self.pr["isDraft"]);self.assertIsNone(self.f.projection.resolve(self.f.key)["publication_result"])
        selected=self.f.projection.resolve(self.f.key);self.assertEqual("implementing",selected["phase"]);self.assertIsNone(selected["results"]["check"])
        final={"profile":"delivery_review_ready","mode":"workflow","task_ref":self.f.task_ref,"delivery_key":self.f.key,"readiness_result_id":"missing-current-gate","reviewed_head":self.f.head,"pr_title":"最终交付","pr_body":"Refs #636","remaining_work_state":"none"}
        self.assertEqual("review_stale",self.invoke(final)["exit_id"])
        self.assertNotIn("ready",self.effects)

    def test_existing_ready_is_draft_before_push_and_lost_transition_recovers(self):
        # A current Ready PR may also be observed before its final local output.
        # This early-update scenario does not infer a passed public gate.
        self.remote=self.f.head
        self.pr={"number":42,"url":"https://github.com/example/repo/pull/42","state":"OPEN","isDraft":False,"title":"旧候选","body":"Refs #636","headRefName":"feat/flow","headRefOid":self.remote,"baseRefName":"main","headRepositoryOwner":{"login":"example"}}
        (self.f.repo/"app.txt").write_text("new candidate\n");self.f.git("add","app.txt");self.f.git("commit","-qm","candidate fix");self.f.head=self.f.git("rev-parse","HEAD").strip()
        self.drop="draft"
        first=self.invoke(self.public());self.assertEqual("resume_publication",first["exit_id"])
        self.assertEqual(["draft"],self.effects)
        result=self.invoke(self.public());self.assertEqual("draft_published",result["exit_id"])
        self.assertEqual(["draft","push","edit"],self.effects)
        self.assertEqual(42,result["pr_number"]);self.assertTrue(self.pr["isDraft"])
        self.assertEqual(result,self.invoke(self.public()));self.assertEqual(1,self.effects.count("draft"))

    def provider_reads(self):
        original=subprocess.run
        def observed(command,*args,**kwargs):
            if command[:3]==["gh","pr","view"]:
                return subprocess.CompletedProcess(command,0,json.dumps(self.pr),"")
            return original(command,*args,**kwargs)
        return patch("subprocess.run",side_effect=observed)

    def final_input(self):
        self.f.projection.begin_check(self.f.key,self.f.projection.candidate(["app.txt"],head_ref=self.f.head,base_ref=self.base))
        ready=self.f.readiness(self.f.full_review(self.f.check()))
        return {"profile":"delivery_review_ready","mode":"workflow","task_ref":self.f.task_ref,"delivery_key":self.f.key,
                "readiness_result_id":ready["readiness_result_id"],"reviewed_head":self.f.head,
                "pr_title":ready["pr_title"],"pr_body":ready["pr_body"],"remaining_work_state":ready["remaining_work_state"]}

    def test_same_pr_ready_draft_ready_with_public_rework_and_old_gate_rejection(self):
        first=self.invoke(self.public())
        final=self.final_input()
        with self.provider_reads():
            ready=self.invoke(final)
        self.assertEqual("ready_for_merge",ready["exit_id"]);self.assertFalse(self.pr["isDraft"])
        returning={"profile":"delivery_return_to_draft","mode":"workflow","task_ref":self.f.task_ref,"delivery_key":self.f.key,"revision_reason":"Correct a normal implementation finding before publishing the new candidate."}
        self.drop="draft"
        with self.provider_reads():
            interrupted=self.invoke(returning)
        self.assertEqual("resume_publication",interrupted["exit_id"])
        self.assertTrue(self.pr["isDraft"])
        revised=self.invoke(returning)
        self.assertEqual("draft_revision_ready",revised["exit_id"]);self.assertEqual(revised,self.invoke(returning))
        current=self.f.projection.resolve(self.f.key)
        self.assertEqual("implementing",current["phase"])
        for role in ("check","full_review","readiness"):self.assertIsNone(current["results"][role])
        self.assertIsNotNone(current["results"]["planning"])
        (self.f.repo/"app.txt").write_text("reviewed correction\n");self.f.git("add","app.txt");self.f.git("commit","-qm","normal correction");self.f.head=self.f.git("rev-parse","HEAD").strip()
        second=self.invoke(self.public());self.assertEqual(first["pr_number"],second["pr_number"])
        self.assertEqual("review_stale",self.invoke(final)["exit_id"])
        self.assertTrue(self.pr["isDraft"])
        latest=self.final_input()
        with self.provider_reads():
            final_result=self.invoke(latest)
        self.assertEqual("ready_for_merge",final_result["exit_id"]);self.assertFalse(self.pr["isDraft"])
        self.assertEqual(first["pr_number"],final_result["pr_number"])
        self.assertEqual(1,self.effects.count("create"))



if __name__=="__main__":unittest.main()
