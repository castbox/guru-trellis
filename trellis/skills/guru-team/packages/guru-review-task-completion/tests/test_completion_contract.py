import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json


PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
CLOSURE = PACKAGE.parent / "guru-complete-task-closure"


@pytest.fixture
def current():
    import importlib.util
    path=PACKAGE.parent/'guru-check-task/tests/test_delivery_flow.py'
    spec=importlib.util.spec_from_file_location('completion_current_fixture',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    item=module.DeliveryFlow();item.setUp()
    yield item
    item.doCleanups()


def fixture(current):
    public={'profile':'delivery_completion','mode':'workflow','task_ref':current.task_ref,'task_key':{'task_id':'flow-task','lifecycle_generation':0}}
    semantic={'profile':public['profile'],'mode':'workflow','reviewed_task_key':public['task_key'].copy(),'reviewed_scope':current.projection.read_record()['accepted_scope'],'reviewed_delivery_result_ids':[],'evidence':[current.projection.read_record()['accepted_scope']],'remaining_work_refs':[],'result_id':'completion:test','route':{'typed_exit':'completed'}}
    return public,semantic


def invoke(tmp_path, public, semantic):
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    return subprocess.run(
        [sys.executable, str(PACKAGE / "runtime/invoke.py"), "--root", str(tmp_path),
         "--input", str(input_path), "--semantic-result", str(semantic_path)],
        text=True, capture_output=True, env=env,
    )


def test_contract_assets_and_projection(current):
    interface=json.loads((PACKAGE/'interface.json').read_text())
    validate_json(interface,ROOT/'schemas/skill-interface-1.7.schema.json','interface')
    for group in ('artifacts','schemas'):
        for item in interface[group]:assert (PACKAGE/item['path']).is_file()
    for output in interface['public_contracts']['outputs']:
        validate_json(json.loads((PACKAGE/output['example']['path']).read_text()),PACKAGE/output['schema']['path'],output['exit_id'])
    # Known undelivered scope is not complete; first use the actual stop owner.
    current.test_scope_withdrawal_and_stop_stdout_recovery()
    public,semantic=fixture(current)
    result=invoke(current.repo,public,semantic);assert result.returncode==0,result.stderr
    output=json.loads(result.stdout);assert set(output)=={'exit_id','result_ref'}
    assert output['result_ref']['task_id']==public['task_key']['task_id']
    contract=next(row for row in interface['public_contracts']['consumer_inputs'] if row['id']=='closure')['contract']
    projection=next(row for row in interface['public_contracts']['projections'] if row['id']=='closure')
    authored=json.loads((PACKAGE/contract['authoring_example']['path']).read_text())
    authored.update({row['target']:output[row['source']] for row in projection['mappings']})
    authored['evidence_slots']['completion']=output['result_ref']['result_id']
    validate_json(authored,CLOSURE/'schemas/public-input.schema.json','closure')


@pytest.mark.parametrize("lineage,slots", [
    ("closeout", ["planning", "task_commit_pair", "phase2_check", "branch_review", "closeout_publication"]),
    ("pre_cutover_recovered", ["planning", "restore", "merge_recovery"]),
])
def test_pre_cutover_lineage_cannot_enter_current_completion(tmp_path, lineage, slots):
    public=json.loads((PACKAGE / "examples/public-input.json").read_text())
    semantic=json.loads((PACKAGE / "examples/semantic-result.json").read_text())
    public["merge_result"] = {
        "task_id": "example-task", "lifecycle_generation": 0, "repo_ref": "castbox/guru-trellis",
        "pr_number": 2, "merge_commit_sha": "c" * 40, "merge_lineage": lineage, "result_id": "merge:current",
    }
    public["evidence_slots"] = {name: name + ":current" for name in slots}
    semantic["reviewed_evidence_slots"] = copy.deepcopy(public["evidence_slots"])
    result = invoke(tmp_path, public, semantic)
    assert result.returncode != 0
    assert json.loads(result.stderr)["code"] == "schema_mismatch"


@pytest.mark.parametrize('change',['generation','task_id','scope','delivery_history','remaining'])
def test_stale_and_incomplete_facts_do_not_complete(current,change):
    public,semantic=fixture(current)
    if change=='generation':public['task_key']['lifecycle_generation']=1
    elif change=='task_id':public['task_key']['task_id']='other-task'
    elif change=='scope':semantic['reviewed_scope']['revision']='sha256:'+'a'*64
    elif change=='delivery_history':semantic['reviewed_delivery_result_ids']=['delivery:missing']
    else:semantic['remaining_work_refs']=['scope:unfinished']
    result=invoke(current.repo,public,semantic)
    assert result.returncode==3,result.stderr
    assert json.loads(result.stderr)['code']=='stale_identity'
    assert current.projection.read_record()['completion_results']==[]


@pytest.mark.parametrize('route',['remaining_work','evidence_pending','additional_delivery_required','requirements_revision_required','implementation_revision_required','blocked'])
def test_noncomplete_routes_use_task_key_and_reason(current,route):
    public,semantic=fixture(current);semantic['route']={'typed_exit':route,'reason':{'reason_code':'work_pending','reason_refs':['scope:current']}};semantic['remaining_work_refs']=['scope:current']
    result=invoke(current.repo,public,semantic);assert result.returncode==0,result.stderr
    output=json.loads(result.stdout);assert output['exit_id']==route;assert output['reason']==semantic['route']['reason']
    assert ('task_key' in output)==(route!='blocked')
    assert 'resume_target' not in output and 'task_artifact' not in output
    assert current.projection.read_record()['completion_results']==[]


@pytest.mark.parametrize('archive_month',['2026-09','2026-08'])
def test_reactivation_validation_and_evidence_refresh(current,archive_month):
    current.test_no_mutation_closure_records_public_result_and_recovers()
    scope=current.projection.read_record()['accepted_scope']
    current.projection.apply({'api_version':'1.0','operation':'reopen_task','key':{'task_id':'flow-task','lifecycle_generation':0},'owner_role':'task_scope','owner_id':'guru-test-task_scope','authority':scope})
    public,semantic=fixture(current)
    public.update(profile='delivery_reactivation_validation',task_key={'task_id':'flow-task','lifecycle_generation':1},reactivation_anchor={'task_id':'flow-task','archived_generation':0,'archive_ref':f'.trellis/tasks/archive/{archive_month}/flow-task','archive_head':current.head})
    semantic.update(profile=public['profile'],reviewed_task_key=public['task_key'],reviewed_delivery_result_ids=['delivery:flow'])
    semantic['route']={'typed_exit':'evidence_pending','reason':{'reason_code':'evidence_pending','reason_refs':['validation:current']}}
    pending=invoke(current.repo,public,semantic);assert pending.returncode==0,pending.stderr
    pending=json.loads(pending.stdout)
    refreshed={'profile':'delivery_evidence_refresh','mode':'workflow','task_ref':current.task_ref,'task_key':pending['task_key'],'source_exit':'evidence_pending','reason':pending['reason']}
    semantic.update(profile='delivery_evidence_refresh',route={'typed_exit':'completed'},result_id='completion:revalidation')
    output=invoke(current.repo,refreshed,semantic);assert output.returncode==0,output.stderr
    assert json.loads(output.stdout)['result_ref']['lifecycle_generation']==1
    assert not any(row['lifecycle_generation']==1 for row in current.projection.read_record()['deliveries'])


@pytest.mark.parametrize('change',['old_merge','dual_basis','wrong_generation','wrong_task','old_owner_profile'])
def test_reactivation_cannot_inherit_old_completion_or_delivery(current,change):
    public,semantic=fixture(current)
    public.update(profile='delivery_reactivation_validation',reactivation_anchor={'task_id':'flow-task','archived_generation':0,'archive_ref':'.trellis/tasks/archive/2026-10/flow-task','archive_head':current.head})
    semantic['profile']=public['profile']
    code='schema_mismatch'
    if change=='old_merge':public.pop('reactivation_anchor');public['merge_result']={'result_id':'merge:old'}
    elif change=='dual_basis':public['merge_result']={'result_id':'merge:old'}
    elif change=='wrong_generation':public['task_key']['lifecycle_generation']=2;code='stale_identity'
    elif change=='wrong_task':public['reactivation_anchor']['task_id']='other-task';code='stale_identity'
    else:public['profile']='reactivation_validation'
    result=invoke(current.repo,public,semantic);assert result.returncode!=0
    assert json.loads(result.stderr)['code']==code
