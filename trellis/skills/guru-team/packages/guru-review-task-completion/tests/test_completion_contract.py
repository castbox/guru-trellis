import json
import os
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]

def test_contract_assets():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    validate_json(interface, ROOT / "schemas/skill-interface-1.4.schema.json", "interface")
    assert [item["id"] for item in interface["external_exits"]] == ["remaining_work", "evidence_pending", "additional_delivery_required", "requirements_revision_required", "implementation_revision_required", "completed", "blocked"]
    for group in ("artifacts", "schemas"):
        for item in interface[group]: assert (PACKAGE / item["path"]).is_file()

def test_completion_requires_all_delivery_facts(tmp_path):
    public={"profile":"completion","mode":"standalone","task_ref":".trellis/tasks/demo","delivery_facts":[{"delivery_cycle_ref":"delivery:a","merge_commit_sha":"a"*40},{"delivery_cycle_ref":"delivery:b","merge_commit_sha":"b"*40}],"evidence_refs":["tests:ok"]}
    semantic={"profile":"completion","mode":"standalone","authority_refs":["requirements:current"],"delivery_refs":["delivery:a"],"evidence_refs":["tests:ok"],"remaining_work_refs":[],"route":{"typed_exit":"completed"}}
    input_path=tmp_path/"input.json"; semantic_path=tmp_path/"semantic.json"
    input_path.write_text(json.dumps(public)); semantic_path.write_text(json.dumps(semantic))
    env=os.environ.copy(); env["PYTHONPATH"]=str(ROOT)
    command=[sys.executable,str(PACKAGE/"runtime/invoke.py"),"--root",str(tmp_path),"--input",str(input_path),"--semantic-result",str(semantic_path)]
    failed=subprocess.run(command,text=True,capture_output=True,env=env)
    assert failed.returncode==3
    semantic["delivery_refs"].append("delivery:b"); semantic_path.write_text(json.dumps(semantic))
    passed=subprocess.run(command,text=True,capture_output=True,env=env,check=True)
    assert json.loads(passed.stdout)["exit_id"]=="completed"
