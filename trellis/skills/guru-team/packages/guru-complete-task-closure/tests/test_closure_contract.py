import json,os,subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json
PACKAGE=Path(__file__).resolve().parents[1]; ROOT=PACKAGE.parents[1]
def test_contract_assets():
    value=json.loads((PACKAGE/"interface.json").read_text()); validate_json(value,ROOT/"schemas/skill-interface-1.4.schema.json","interface")

def test_no_mutation_and_closed_recovery(tmp_path):
    env=os.environ.copy(); env["PYTHONPATH"]=str(ROOT)
    public={"profile":"completion_approved","mode":"standalone","task_ref":".trellis/tasks/demo","completion_ref":"completion:v1:demo","source_issue":{"repo_ref":"castbox/guru-trellis","number":436,"disposition":"reference_only"}}
    semantic={"profile":"completion_approved","mode":"standalone","route":{"typed_exit":"no_mutation","reason":"reference only"}}
    ip=tmp_path/"input.json"; sp=tmp_path/"semantic.json"; fp=tmp_path/"facts.json"
    ip.write_text(json.dumps(public)); sp.write_text(json.dumps(semantic))
    command=[sys.executable,str(PACKAGE/"runtime/invoke.py"),"--root",str(tmp_path),"--input",str(ip),"--semantic-result",str(sp)]
    output=json.loads(subprocess.run(command,text=True,capture_output=True,env=env,check=True).stdout)
    assert output["exit_id"]=="no_mutation" and output["closure_ref"].endswith("completion:v1:demo")
    public["source_issue"]["disposition"]="exact_source"; semantic["route"]={"typed_exit":"close_issue","reason":"completed"}
    ip.write_text(json.dumps(public)); sp.write_text(json.dumps(semantic)); fp.write_text(json.dumps({"issue":{"state":"CLOSED"}}))
    recovered=json.loads(subprocess.run(command+["--confirmed-close","--facts",str(fp)],text=True,capture_output=True,env=env,check=True).stdout)
    assert recovered["exit_id"]=="closed" and recovered["issue_ref"]=="castbox/guru-trellis#436"
