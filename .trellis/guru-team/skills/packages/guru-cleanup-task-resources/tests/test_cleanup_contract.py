import json,os,subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json
PACKAGE=Path(__file__).resolve().parents[1]; ROOT=PACKAGE.parents[1]
FINISH_REF="finish:v1:0123456789abcdef"
def test_contract_assets(): validate_json(json.loads((PACKAGE/"interface.json").read_text()),ROOT/"schemas/skill-interface-1.4.schema.json","interface")

def test_cleanup_requires_confirmation_and_current_finish_receipt(tmp_path):
    subprocess.run(["git","init","-q","-b","main"],cwd=tmp_path,check=True)
    runtime=tmp_path/".trellis/.runtime/guru-team/demo.json"; runtime.parent.mkdir(parents=True); runtime.write_text(json.dumps({"task_ref":".trellis/tasks/demo"})+"\n")
    receipt=tmp_path/".trellis/.runtime/guru-team/finish/0123456789abcdef.json"; receipt.parent.mkdir(parents=True); receipt.write_text(json.dumps({"schema_version":"1.0","stage":"success","task_ref":".trellis/tasks/demo","closure_ref":"closure:v1:demo","finish_ref":FINISH_REF,"repo_ref":"example/repo","base_branch":"main","head_branch":"codex/demo","expected_base_head":"a"*40,"archive_ref":".trellis/tasks/archive/2026-09/demo","parent_head":"a"*40,"commit":"b"*40,"pr_number":1,"pr_url":"https://github.com/example/repo/pull/1","target_head":"c"*40}))
    public={"profile":"finish_success","mode":"standalone","task_ref":".trellis/tasks/demo","finish_ref":FINISH_REF,"resources":[{"kind":"runtime","locator":".trellis/.runtime/guru-team/demo.json"}]}
    semantic={"profile":"finish_success","mode":"standalone","owned_resources":public["resources"],"route":{"typed_exit":"cleaned"}}
    ip=tmp_path/"input.json"; sp=tmp_path/"semantic.json"; ip.write_text(json.dumps(public)); sp.write_text(json.dumps(semantic))
    env=os.environ.copy(); env["PYTHONPATH"]=str(ROOT); command=[sys.executable,str(PACKAGE/"runtime/invoke.py"),"--root",str(tmp_path),"--input",str(ip),"--semantic-result",str(sp)]
    pending=json.loads(subprocess.run(command,text=True,capture_output=True,env=env,check=True).stdout); assert pending["exit_id"]=="remaining_resources" and runtime.exists()
    cleaned=json.loads(subprocess.run(command+["--confirmed-cleanup"],text=True,capture_output=True,env=env,check=True).stdout); assert cleaned["exit_id"]=="cleaned" and not runtime.exists() and not receipt.exists()

def test_cleanup_rejects_unbound_or_current_worktree(tmp_path):
    repo=tmp_path/"repo"; repo.mkdir(); subprocess.run(["git","init","-q","-b","main"],cwd=repo,check=True)
    subprocess.run(["git","config","user.email","test@example.com"],cwd=repo,check=True); subprocess.run(["git","config","user.name","Test"],cwd=repo,check=True)
    (repo/"tracked").write_text("x\n"); subprocess.run(["git","add","."],cwd=repo,check=True); subprocess.run(["git","commit","-qm","base"],cwd=repo,check=True)
    head=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,text=True,capture_output=True,check=True).stdout.strip(); subprocess.run(["git","update-ref","refs/remotes/origin/main",head],cwd=repo,check=True)
    receipt=repo/".trellis/.runtime/guru-team/finish/0123456789abcdef.json"; receipt.parent.mkdir(parents=True); receipt.write_text(json.dumps({"schema_version":"1.0","stage":"success","task_ref":".trellis/tasks/demo","closure_ref":"closure:v1:demo","finish_ref":FINISH_REF,"repo_ref":"example/repo","base_branch":"main","head_branch":"codex/demo","expected_base_head":head,"archive_ref":".trellis/tasks/archive/2026-09/demo","parent_head":head,"commit":head,"pr_number":1,"pr_url":"https://github.com/example/repo/pull/1","target_head":head}))
    public={"profile":"finish_success","mode":"standalone","task_ref":".trellis/tasks/demo","finish_ref":FINISH_REF,"resources":[{"kind":"worktree","locator":str(repo)}]}; semantic={"profile":"finish_success","mode":"standalone","owned_resources":public["resources"],"route":{"typed_exit":"cleaned"}}
    ip=tmp_path/"input.json"; sp=tmp_path/"semantic.json"; ip.write_text(json.dumps(public)); sp.write_text(json.dumps(semantic)); env=os.environ.copy(); env["PYTHONPATH"]=str(ROOT)
    command=[sys.executable,str(PACKAGE/"runtime/invoke.py"),"--root",str(repo),"--input",str(ip),"--semantic-result",str(sp),"--confirmed-cleanup"]
    rejected=subprocess.run(command,text=True,capture_output=True,env=env); assert rejected.returncode==3 and repo.exists()
