"""Bounded #814 native adoption observations on isolated Git fixtures.

Setup uses public native Task/Delivery/session commands and the original Guru
C4 writer. Runtime audit observes actual Git subprocesses without replacing them.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

BOOTSTRAP = r"""
import atexit,json,runpy,sys,time,traceback
from pathlib import Path
entry,audit_path,*args=sys.argv[1:]
calls=[]
def audit(event,args):
    if event=='subprocess.Popen' and Path(str(args[0])).name=='git':
        frames=traceback.extract_stack()
        source=next((f.name for f in reversed(frames) if f.filename.endswith('session_storage.py') and f.name!='_git'),'other')
        calls.append(dict(argv=args[1],source=source,observed_at=time.perf_counter()))
sys.addaudithook(audit)
starts={}
def profile(frame,event,arg):
    if frame.f_code.co_filename.endswith('subprocess.py') and frame.f_code.co_name=='run':
        if event=='call':starts[id(frame)]=(time.perf_counter(),len(calls))
        elif event=='return' and id(frame) in starts:
            start,index=starts.pop(id(frame))
            if len(calls)>index:calls[index]['elapsed_seconds']=time.perf_counter()-start
sys.setprofile(profile)
atexit.register(lambda:Path(audit_path).write_text(json.dumps(calls),encoding='utf-8'))
sys.path.insert(0,str(Path(entry).parent))
sys.argv=[entry,*args]
runpy.run_path(entry,run_name='__main__')
"""

class Driver:
    def __init__(self,args):
        self.target=Path(args.target).resolve()
        self.fork=Path(args.fork_source).resolve()
        self.base=Path(args.state_dir).resolve()
        self.env={k:v for k,v in os.environ.items() if k in {'PATH','SYSTEMROOT','SystemRoot','WINDIR','PATHEXT','HOME'}}
        self.env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=str(self.base/'absent-config'),
            GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='core.hooksPath',GIT_CONFIG_VALUE_0=str(self.base/'empty-hooks'),
            PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1',TRELLIS_CONTEXT_ID='fixture-bound')
        self.cli=self.fork/'packages/cli/bin/trellis.js'
    def boundary(self):
        r=subprocess.run(['bash',str(self.target/'.trellis/guru-team/scripts/bash/check-task-checkout-boundary.sh'),
            '--json','--task','.trellis/tasks/11-13-814-context-validation'],cwd=self.target,capture_output=True,text=True)
        assert r.returncode==0 and json.loads(r.stdout)['status']=='ok',r.stdout+r.stderr
    def save(self,name,value):
        self.boundary()
        self.base.mkdir(parents=True,exist_ok=True)
        (self.base/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    def run(self,root,argv,env=None,check=True):
        start=time.perf_counter()
        r=subprocess.run([str(x) for x in argv],cwd=root,env=env or self.env,capture_output=True,text=True)
        row=dict(argv=[str(x) for x in argv],cwd=str(root),returncode=r.returncode,
            elapsed_seconds=round(time.perf_counter()-start,4),stdout=r.stdout,stderr=r.stderr)
        with (self.base/'commands.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        if check and r.returncode:raise RuntimeError(json.dumps(row))
        return row
    def git(self,root,*args):
        return self.run(root,['git','-C',root,*args])['stdout'].strip()
    def native(self,root,entry,*args,env=None):
        return self.run(root,[sys.executable,'-B',root/'.trellis/scripts'/entry,*args],env)
    def setup(self):
        self.boundary()
        assert not self.base.exists(),'Use a new state directory; retained attempts are not overwritten.'
        self.base.mkdir(parents=True)
        fixtures=[]
        for count in (3,169):
            root=self.base/str(count)/'primary space'
            root.mkdir(parents=True)
            self.git(root,'init','-q','-b','main')
            self.git(root,'config','user.name','Fixture')
            self.git(root,'config','user.email','fixture@example.invalid')
            self.git(root,'config','commit.gpgsign','false')
            self.git(root,'config','maintenance.auto','false')
            self.git(root,'config','gc.auto','0')
            self.git(root,'commit','--allow-empty','-qm','Fixture root')
            roots=[root]
            for i in range(1,count):
                peer=root.parent/f'peer-{i}'
                self.git(root,'worktree','add','-q','-b',f'peer-{i}',str(peer))
                roots.append(peer)
            for peer in roots[:3]:
                self.run(peer,['node',self.cli,'init','--yes','--codex','--no-monorepo','--workflow','native-delivery-v1'])
                (peer/'.trellis/config.yaml').write_text('task_auto_commit: false\n',encoding='utf-8')
            workflow=(root/'.trellis/workflow.md').read_text()
            for i,peer in enumerate(roots):
                (peer/'.trellis').mkdir(exist_ok=True)
                (peer/'.trellis/workflow.md').write_text(workflow.replace('"task_scope": "trellis-start"',f'"task_scope": "fixture-owner-{i}"'))
            peer=roots[1]
            self.native(peer,'task.py','create','Measured Task','--description','Native context fixture',
                '--task-id','measured-task','--slug','measured-task','--schema-version','2.0','--no-start')
            task=next((peer/'.trellis/tasks').glob('*-measured-task'))
            taskref=task.relative_to(peer).as_posix()
            (task/'prd.md').write_text('验证原生 context 的 Task、Delivery 和会话解析。\n',encoding='utf-8')
            authority=dict(locator=taskref+'/prd.md',revision='sha256:'+hashlib.sha256((task/'prd.md').read_bytes()).hexdigest())
            common=dict(api_version='1.0',key=dict(task_id='measured-task',lifecycle_generation=0))
            self.native(peer,'delivery.py','accept-scope','--task',taskref,'--input',json.dumps(dict(common,
                operation='accept_scope',owner_role='task_scope',owner_id='fixture-owner-1',authority=authority)))
            did=str(uuid.uuid4())
            self.native(peer,'delivery.py','create','--task',taskref,'--input',json.dumps(dict(common,
                operation='create_delivery',key=dict(common['key'],delivery_id=did),owner_role='creation',
                owner_id='trellis-start',scope_ref=dict(authority=authority,anchors=['native-context']),profile='local_commit')))
            self.git(peer,'add','--',taskref)
            self.git(peer,'commit','-qm','Create measured fixture Task through native writer')
            data=dict(profile='delivery_active_task',mode='standalone',action='establish',task_id='measured-task',task_ref=taskref,lifecycle_generation=0)
            wrapper=self.target/'.trellis/guru-team/skills/packages/guru-establish-task-branch-binding/scripts/invoke.sh'
            bound=self.run(peer,['bash',wrapper,'--root',peer,'--input',json.dumps(data)])
            assert json.loads(bound['stdout'])['exit_id']=='binding_established',bound
            self.native(peer,'task.py','start',taskref,'--allow-empty-context')
            self.native(peer,'delivery.py','select','--task',taskref,'--delivery',did)
            installed=peer/'.trellis/scripts/common/session_storage.py'
            assert installed.read_bytes()==(self.target/'.trellis/scripts/common/session_storage.py').read_bytes()
            fixtures.append(dict(count=count,root=str(root),peer=str(peer),other=str(roots[2]),task=str(task),taskref=taskref,delivery_id=did))
            self.save('state.json',dict(fixtures=fixtures))
        self.save('state.json',dict(fixtures=fixtures,fork_head=self.git(self.fork,'rev-parse','HEAD'),
            installed_session_sha256=hashlib.sha256((self.target/'.trellis/scripts/common/session_storage.py').read_bytes()).hexdigest()))
    def snapshot(self,fixture):
        root=Path(fixture['root'])
        common=Path(self.git(root,'rev-parse','--path-format=absolute','--git-common-dir'))
        roots=[Path(v[9:]) for v in self.git(root,'worktree','list','--porcelain').splitlines() if v.startswith('worktree ')]
        files=[]
        for workspace in roots:
            files.extend(p for p in (workspace/'.trellis').rglob('*') if p.is_file())
            if (workspace/'.git').is_file():files.append(workspace/'.git')
        for folder in (common/'trellis',common/'worktrees'):
            files.extend(p for p in folder.rglob('*') if p.is_file())
        return {str(p):(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mode) for p in files if '__pycache__' not in p.parts}
    def sample(self,fixture,label,root,entry,args,key='fixture-bound',expected_code=0):
        self.boundary()
        env=dict(self.env,TRELLIS_CONTEXT_ID=key)
        before=self.snapshot(fixture)
        audit=self.base/f'{fixture["count"]}-{label}-audit.json'
        row=self.run(root,[sys.executable,'-B','-c',BOOTSTRAP,root/'.trellis/scripts'/entry,audit,*args],env,check=False)
        after=self.snapshot(fixture)
        calls=json.loads(audit.read_text())
        row.update(count=fixture['count'],shape=label,git_calls=len(calls),
            sources=dict(Counter(c['source'] for c in calls)),
            families=dict(Counter(' '.join(c['argv'][3:]) for c in calls)),
            source_elapsed_seconds={source:round(sum(c.get('elapsed_seconds',0) for c in calls if c['source']==source),4) for source in {c['source'] for c in calls}},
            task_session_peer_bytes_and_modes_unchanged=before==after,audit=str(audit))
        self.save(f'{fixture["count"]}-{label}.json',row)
        assert row['returncode']==expected_code and before==after,row
        return row
    def measure(self):
        state=json.loads((self.base/'state.json').read_text())
        rows=[]
        for f in state['fixtures']:
            root,peer=Path(f['root']),Path(f['peer'])
            self.boundary()
            self.native(peer,'delivery.py','select','--task',f['taskref'],'--delivery',f['delivery_id'])
            self.native(peer,'task.py','start',f['taskref'],'--allow-empty-context',env=dict(self.env,TRELLIS_CONTEXT_ID='fixture-explicit'))
            for shape,where,entry,args,key in (
                ('known-key-miss',root,'get_context.py',['--mode','runtime-contract','--json'],'fixture-missing'),
                ('bound-remote',root,'get_context.py',['--mode','runtime-contract','--json'],'fixture-bound'),
                ('bound-continuation',root,'get_context.py',['--mode','continuation','--json'],'fixture-bound'),
                ('explicit-task-preserving-delivery',peer,'task.py',['start',f['taskref'],'--allow-empty-context'],'fixture-explicit')):
                existing=self.base/f'{f["count"]}-{shape}.json'
                if existing.exists():
                    row=json.loads(existing.read_text())
                    assert row['returncode']==0 and row['task_session_peer_bytes_and_modes_unchanged'],row
                else:row=self.sample(f,shape,where,entry,args,key)
                if entry=='get_context.py' and shape!='bound-continuation':
                    assert json.loads(row['stdout'])['owners']['task_scope']==('fixture-owner-0' if shape=='known-key-miss' else 'fixture-owner-1'),row
                rows.append(row)
        self.save('measurements.json',dict(samples=rows,source=state))
    def probes(self):
        api=(self.fork/'packages/cli/dist/index.js').as_uri()
        code=r"""import fs from 'node:fs';
const {maintenance:m}=await import(process.argv[1]);
const [root,state]=process.argv.slice(2);
const inspection=await m.inspectToolsTarget({root});
const decisions=inspection.files.filter(r=>r.status==='conflict').map(r=>({path:r.path,source:r.source,action:'preserve'}));
const plan=await m.prepareToolsInstallation({root,workflow:{action:'preserve'},file_decisions:decisions});
fs.writeFileSync(state+'/public-plan.json',JSON.stringify(plan,null,2));
const result=await m.applyMaintenance(plan,{state_dir:state});
console.log(JSON.stringify({inspection,plan,result}));"""
        for f in json.loads((self.base/'state.json').read_text())['fixtures']:
            self.boundary()
            folder=self.base/str(f['count'])/'public-probes'
            folder.mkdir()
            root=Path(f['root'])
            def preserved():
                return {k:v for k,v in self.snapshot(f).items() if not k.startswith(str(root/'.trellis')+'/') or k.startswith(str(root/'.trellis/tasks')+'/')}
            before=preserved()
            row=self.run(root,['node','--input-type=module','-e',code,api,str(root),str(folder)],check=False)
            after=preserved()
            row['task_session_peer_bytes_and_modes_unchanged']=before==after
            self.save(f'{f["count"]}-public-probes.json',row)
            assert row['returncode']==0,row
            assert before==after,'Public tools updated fixture managed assets; inspect explicit preservation subset.'
    def identity(self):
        for f in json.loads((self.base/'state.json').read_text())['fixtures']:
            root=Path(f['root'])
            self.sample(f,'identity-task',root,'task.py',['current','--json'])
            self.sample(f,'identity-delivery',root,'delivery.py',['current','--json'])
    def negative(self):
        f=json.loads((self.base/'state.json').read_text())['fixtures'][0]
        root,peer,other=Path(f['root']),Path(f['peer']),Path(f['other'])
        self.boundary()
        saved=self.base/'3-stale-branch.json'
        if saved.exists():row=json.loads(saved.read_text())
        else:
            self.git(peer,'switch','-c','peer-1-stale')
            row=self.sample(f,'stale-branch',root,'get_context.py',['--mode','runtime-contract','--json'],expected_code=1)
        assert row['returncode']==1 and row['task_session_peer_bytes_and_modes_unchanged'],row
        assert 'current_task_checkout_unresolved' in row['stderr'],row
        self.git(peer,'switch','peer-1')
        env=dict(self.env,TRELLIS_CONTEXT_ID='fixture-ambiguous')
        self.native(other,'task.py','create','Other task','--description','Normal second task',
            '--task-id','other-task','--slug','other-task','--schema-version','2.0','--no-start',env=env)
        task=next((other/'.trellis/tasks').glob('*-other-task'))
        ref=task.relative_to(other).as_posix()
        self.native(other,'task.py','start',ref,'--allow-empty-context',env=env)
        self.git(other,'add','--',ref)
        self.git(other,'commit','-qm','Create second fixture Task through native writer')
        commit=self.git(other,'rev-parse','HEAD')
        self.git(root,'cherry-pick',commit)
        row=self.sample(f,'nonunique-task',peer,'get_context.py',['--mode','runtime-contract','--json'],key='fixture-ambiguous',expected_code=1)
        assert 'ambiguous_task_identity' in row['stderr'],row
        self.git(root,'revert','--no-edit',commit)
        self.sample(f,'healthy-after-rejections',root,'get_context.py',['--mode','runtime-contract','--json'])

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('action',choices=['setup','measure','probes','negative','identity'])
    p.add_argument('--target',required=True)
    p.add_argument('--fork-source',required=True)
    p.add_argument('--state-dir',required=True)
    a=p.parse_args()
    d=Driver(a)
    getattr(d,{'setup':'setup','measure':'measure','probes':'probes','negative':'negative','identity':'identity'}[a.action])()
