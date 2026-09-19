from __future__ import annotations
import argparse,hashlib,json,sys,subprocess
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json

def load(root, package, value, field):
    p=Path(value); choices=[p] if p.is_absolute() else [root/p,package/p]
    source=next((x for x in choices if x.is_file() and not x.is_symlink()),None)
    if source is None: raise CommandError("invalid_json",field,"Provide one regular JSON file.")
    try: v=json.loads(source.read_text())
    except json.JSONDecodeError as exc: raise CommandError("invalid_json",field,"Provide valid JSON.") from exc
    if not isinstance(v,dict): raise CommandError("invalid_json",field,"Provide one JSON object.")
    return v

def closure_ref(public, action):
    issue=public.get("source_issue") or {}
    binding=hashlib.sha256(json.dumps({"source_issue":issue,"action":action},sort_keys=True,separators=(",",":")).encode()).hexdigest()[:16]
    identity={"task_ref":public["task_ref"],"completion_ref":public["completion_ref"],"source_issue":issue,"action":action}
    digest=hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(",",":")).encode()).hexdigest()[:16]
    return "closure:v3:"+binding+":"+digest

def closure_output(public, exit_id, action, **extra):
    out={"exit_id":exit_id,"task_ref":public["task_ref"],"closure_ref":closure_ref(public,action),"source_issue":public["source_issue"]}
    out.update(extra)
    return out

def run(package_root:Path, command:dict, argv:list[str])->dict:
    p=argparse.ArgumentParser(add_help=False); p.add_argument("--root"); p.add_argument("--input",required=True); p.add_argument("--semantic-result",required=True); p.add_argument("--facts"); p.add_argument("--confirmed-close",action="store_true")
    try:a=p.parse_args(argv)
    except SystemExit as exc: raise CommandError("invalid_arguments","arguments","Use the closure command contract.") from exc
    root=Path(a.root or ".").resolve(); public=load(root,package_root,a.input,"input"); semantic=load(root,package_root,a.semantic_result,"semantic_result")
    validate_json(public,package_root/"schemas/public-input.schema.json","input"); validate_json(semantic,package_root/"schemas/semantic-result.schema.json","semantic_result")
    if public["profile"]!=semantic["profile"] or public["mode"]!=semantic["mode"]: raise CommandError("stale_identity","semantic_result","Completion and closure identity differ.",3)
    route=semantic["route"]; exit_id=route["typed_exit"]; issue=public.get("source_issue") or {}
    action="close_issue" if exit_id=="close_issue" else "no_mutation" if exit_id=="no_mutation" else exit_id
    expected_closure_ref=closure_ref(public,action)
    if public.get("source_exit")=="resume_closure":
        if public.get("closure_ref")!=expected_closure_ref:
            raise CommandError("stale_identity","closure_ref","Resume must carry the exact original closure transaction identity.",3)
    if exit_id=="close_issue" and issue.get("disposition")!="exact_source": raise CommandError("stale_identity","source_issue.disposition","Only the exact source Issue may be closed.",3)
    if exit_id=="no_mutation" and issue.get("disposition")=="exact_source": raise CommandError("stale_identity","semantic_result.route.typed_exit","The exact source Issue must use the live close path.",3)
    if exit_id=="close_issue":
        if not a.confirmed_close: return closure_output(public,"resume_closure",action,completion_ref=public["completion_ref"])
        if a.facts:
            facts=load(root,package_root,a.facts,"facts")
            validate_json(facts,package_root/"schemas/live-facts.schema.json","facts")
            fact_issue=facts["issue"]
            if fact_issue["repo_ref"]!=issue["repo_ref"]: raise CommandError("stale_identity","facts.issue.repo_ref","Recovery facts must describe the exact source Issue repository.",3)
            if fact_issue["number"]!=issue["number"]: raise CommandError("stale_identity","facts.issue.number","Recovery facts must describe the exact source Issue number.",3)
        observed=subprocess.run(["gh","issue","view",str(issue["number"]),"--repo",issue["repo_ref"],"--json","state","--jq",".state"],cwd=root,text=True,capture_output=True)
        if observed.returncode!=0: return closure_output(public,"resume_closure",action,completion_ref=public["completion_ref"])
        state=observed.stdout.strip().upper()
        if state=="CLOSED":
            out=closure_output(public,"closed",action,issue_ref=f'{issue["repo_ref"]}#{issue["number"]}',closure_exit="closed")
            validate_json(out,package_root/"schemas/public-output.schema.json","stdout"); return out
        if state!="OPEN": raise CommandError("stale_identity","source_issue","Issue state is not a recoverable close boundary.",3)
        proc=subprocess.run(["gh","issue","close",str(issue["number"]),"--repo",issue["repo_ref"],"--reason","completed"],cwd=root,text=True,capture_output=True)
        if proc.returncode!=0: return closure_output(public,"resume_closure",action,completion_ref=public["completion_ref"])
        verify=subprocess.run(["gh","issue","view",str(issue["number"]),"--repo",issue["repo_ref"],"--json","state","--jq",".state"],cwd=root,text=True,capture_output=True)
        if verify.returncode!=0 or verify.stdout.strip().upper()!="CLOSED": raise CommandError("external_command_failed","source_issue","Issue close result could not be verified; resume the same closure transaction.",4)
        out=closure_output(public,"closed",action,issue_ref=f'{issue["repo_ref"]}#{issue["number"]}',closure_exit="closed")
    elif exit_id=="no_mutation": out=closure_output(public,"no_mutation",action,closure_exit="no_mutation")
    else: out={"exit_id":"blocked"}
    validate_json(out,package_root/"schemas/public-output.schema.json","stdout"); return out

if __name__=="__main__":
    try: print(json.dumps(run(Path(__file__).parents[1],{},sys.argv[1:]),ensure_ascii=False))
    except CommandError as exc: print(json.dumps({"code":exc.code,"field_path":exc.field_path,"remediation":exc.remediation},ensure_ascii=False),file=sys.stderr); raise SystemExit(exc.exit_status)
