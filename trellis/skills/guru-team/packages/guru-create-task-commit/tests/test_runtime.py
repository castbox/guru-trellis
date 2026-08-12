from __future__ import annotations
import json, os, stat, subprocess, sys, tempfile, unittest
import contextlib, io
from pathlib import Path
from jsonschema import Draft202012Validator

PACKAGE=Path(__file__).resolve().parents[1]
SKILLS=PACKAGE.parents[1]
RUNTIME=SKILLS/"runtime"
if str(SKILLS) not in sys.path: sys.path.insert(0,str(SKILLS))
from runtime.command import main
PACKAGE_RUNTIME=PACKAGE/"runtime"
if str(PACKAGE_RUNTIME) not in sys.path: sys.path.insert(0,str(PACKAGE_RUNTIME))
from common import canonical_message, capture_snapshot
from execute import index_entries, run as execute_commit
from runtime.io import CommandError

class PackageLocalRuntimeTest(unittest.TestCase):
 def git(self,repo,*args,input=None,check=True):
  result=subprocess.run(["git",*args],cwd=repo,text=True,input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  if check and result.returncode:
   self.fail(f"git {' '.join(args)} failed: {result.stderr}")
  return result

 def hook_case(self,hook_name,hook_body):
  temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
  repo=Path(temporary.name)/"repo";repo.mkdir()
  self.git(repo,"init","-q","-b","feature/hooks")
  self.git(repo,"config","user.name","Task Commit Test")
  self.git(repo,"config","user.email","task-commit@example.test")
  (repo/"exact.txt").write_text("before\n");(repo/"unrelated.txt").write_text("base\n")
  self.git(repo,"add","exact.txt","unrelated.txt");self.git(repo,"commit","-q","-m","base")
  parent=self.git(repo,"rev-parse","HEAD").stdout.strip()
  (repo/"exact.txt").write_text("reviewed\n");(repo/"unrelated.txt").write_text("preserved\n")
  self.git(repo,"add","unrelated.txt")
  message=canonical_message({"type":"fix","scope":"hooks","summary":"验证钩子失败边界","background":"真实钩子可能拒绝提交。","changes":"记录稳定失败证据。","boundaries":"不发布真实分支。","validations":"验证恢复输入保持。"},211)
  candidate={"$schema":"https://github.com/castbox/guru-trellis/schemas/guru-task-commit-candidate-5.0.json","schema_version":"5.0","skill_id":"guru-create-task-commit","sequence":"001","task":{"id":"08-12-hooks","path":".trellis/tasks/08-12-hooks","status":"in_progress","branch":"feature/hooks"},"git":{"base_branch":"main","base_ref":"main","pre_commit_head":parent,"phase2_commit_anchor":parent},"dirty_snapshot":capture_snapshot(repo),"path_classifications":[{"path":"exact.txt","category":"task-reviewed","reason":"requested","coverage_source":"phase2"},{"path":"unrelated.txt","category":"unrelated-preserved","reason":"parallel state","coverage_source":"live snapshot"}],"exact_stage_paths":["exact.txt"],"message":message,"ai_review":{"status":"passed","summary":"reviewed","evidence":["phase2"]}}
  candidate_path=repo/"candidate.json";candidate_path.write_text(json.dumps(candidate,ensure_ascii=False))
  phase2=repo/".trellis/.runtime/guru-team/owner-checkpoints/08-12-hooks/phase2-check.json";phase2.parent.mkdir(parents=True);phase2.write_text("{}\n")
  hook=repo/".git/hooks"/hook_name;hook.write_text("#!/bin/sh\nset -eu\n"+hook_body+"\n");hook.chmod(hook.stat().st_mode|stat.S_IXUSR)
  return repo,parent,candidate_path,phase2

 def test_pre_commit_rejection_preserves_live_state_and_recovery_inputs(self):
  repo,parent,candidate_path,phase2=self.hook_case("pre-commit","exit 23")
  index_before=self.git(repo,"ls-files","--stage","-z").stdout
  worktrees_before=self.git(repo,"worktree","list","--porcelain").stdout
  with self.assertRaises(CommandError) as raised:
   execute_commit(PACKAGE,{},["--root",str(repo),"--candidate-artifact",str(candidate_path)])
  self.assertEqual("pre_commit",raised.exception.response["transaction_stage"])
  self.assertNotIn("created_commit_sha",raised.exception.response)
  self.assertEqual(parent,self.git(repo,"rev-parse","HEAD").stdout.strip())
  self.assertEqual(index_before,self.git(repo,"ls-files","--stage","-z").stdout)
  self.assertEqual(worktrees_before,self.git(repo,"worktree","list","--porcelain").stdout)
  self.assertTrue(candidate_path.is_file());self.assertTrue(phase2.is_file())
  self.assertEqual("preserved\n",(repo/"unrelated.txt").read_text())

 def test_post_commit_rejection_reports_created_commit_and_preserves_live_state(self):
  repo,parent,candidate_path,phase2=self.hook_case("post-commit","exit 29")
  index_before=self.git(repo,"ls-files","--stage","-z").stdout
  with self.assertRaises(CommandError) as raised:
   execute_commit(PACKAGE,{},["--root",str(repo),"--candidate-artifact",str(candidate_path)])
  evidence=raised.exception.response
  self.assertEqual("post_commit",evidence["transaction_stage"])
  created=evidence["created_commit_sha"]
  self.assertEqual(parent,self.git(repo,"show","-s","--format=%P",created).stdout.strip())
  self.assertEqual("reviewed",self.git(repo,"show",f"{created}:exact.txt").stdout.strip())
  self.assertEqual(parent,self.git(repo,"rev-parse","HEAD").stdout.strip())
  self.assertEqual(index_before,self.git(repo,"ls-files","--stage","-z").stdout)
  self.assertTrue(candidate_path.is_file());self.assertTrue(phase2.is_file())

 def test_hook_mutation_and_message_rewrite_fail_before_live_ref_publication(self):
  cases={
   "prepare-commit-msg":'printf "\\nrewritten\\n" >> "$1"',
   "pre-commit":'printf "injected\\n" > injected.txt\ngit add injected.txt',
   "pre-commit-exact-modify":'printf "hook changed\\n" > exact.txt',
   "pre-commit-unstage":'git reset -q HEAD -- exact.txt',
   "post-commit":'printf "surprise\\n" > post-commit-untracked.txt',
  }
  for hook_name,body in cases.items():
   with self.subTest(hook=hook_name):
    installed_name=hook_name.split("-exact",1)[0].split("-unstage",1)[0]
    repo,parent,candidate_path,phase2=self.hook_case(installed_name,body)
    with self.assertRaises(CommandError) as raised:
     execute_commit(PACKAGE,{},["--root",str(repo),"--candidate-artifact",str(candidate_path)])
    evidence=raised.exception.response
    expected_stage="pre_publication_validation" if hook_name=="prepare-commit-msg" else "post_commit_validation"
    self.assertEqual(expected_stage,evidence["transaction_stage"])
    self.assertIn("created_commit_sha",evidence)
    self.assertEqual(parent,self.git(repo,"rev-parse","HEAD").stdout.strip())
    self.assertTrue(candidate_path.is_file());self.assertTrue(phase2.is_file())

 def test_execute_honors_configured_hooks_path(self):
  repo,parent,candidate_path,_phase2=self.hook_case("prepare-commit-msg",'test "$2" = message\ntest -f "$1"\nexit 31')
  configured=repo/"configured-hooks";configured.mkdir()
  original=repo/".git/hooks/prepare-commit-msg";target=configured/"prepare-commit-msg";original.replace(target)
  self.git(repo,"config","core.hooksPath","configured-hooks")
  with self.assertRaises(CommandError) as raised:
   execute_commit(PACKAGE,{},["--root",str(repo),"--candidate-artifact",str(candidate_path)])
  self.assertEqual("pre_commit",raised.exception.response["transaction_stage"])
  self.assertIn({"name":"prepare-commit-msg","exit_code":31},raised.exception.response["hook_results"])
  self.assertEqual(parent,self.git(repo,"rev-parse","HEAD").stdout.strip())

 def test_hook_cannot_mutate_live_worktree_before_publication(self):
  repo,parent,candidate_path,phase2=self.hook_case("post-commit",'printf "hook changed live state\\n" > "'+"LIVE_PATH"+'"')
  hook=repo/".git/hooks/post-commit"
  hook.write_text(hook.read_text().replace("LIVE_PATH",str(repo/"unrelated.txt")))
  index_before=self.git(repo,"ls-files","--stage","-z").stdout
  with self.assertRaises(CommandError) as raised:
   execute_commit(PACKAGE,{},["--root",str(repo),"--candidate-artifact",str(candidate_path)])
  evidence=raised.exception.response
  self.assertEqual("pre_publication_validation",evidence["transaction_stage"])
  self.assertIn("created_commit_sha",evidence)
  self.assertEqual(parent,self.git(repo,"rev-parse","HEAD").stdout.strip())
  self.assertEqual(index_before,self.git(repo,"ls-files","--stage","-z").stdout)
  self.assertEqual("hook changed live state\n",(repo/"unrelated.txt").read_text())
  self.assertTrue(candidate_path.is_file());self.assertTrue(phase2.is_file())

 def test_stat_cache_refresh_does_not_change_semantic_index_identity(self):
  with tempfile.TemporaryDirectory() as temporary:
   repo=Path(temporary)/"repo";repo.mkdir()
   self.git(repo,"init","-q","-b","main");self.git(repo,"config","user.name","Index Test");self.git(repo,"config","user.email","index@example.test")
   clean=repo/"clean.txt";clean.write_text("stable\n");self.git(repo,"add","clean.txt");self.git(repo,"commit","-q","-m","base")
   semantic_before=index_entries(repo);raw_before=(repo/".git/index").read_bytes()
   current=clean.stat();os.utime(clean,ns=(current.st_atime_ns,current.st_mtime_ns+2_000_000_000))
   self.git(repo,"update-index","--refresh")
   raw_after=(repo/".git/index").read_bytes()
   self.assertNotEqual(raw_before,raw_after)
   self.assertEqual(semantic_before,index_entries(repo))

 def test_execute_runs_all_commit_hooks_against_exact_candidate(self):
  with tempfile.TemporaryDirectory() as temporary:
   repo=Path(temporary)/"repo";repo.mkdir()
   self.git(repo,"init","-q","-b","feature/hooks")
   self.git(repo,"config","user.name","Task Commit Test")
   self.git(repo,"config","user.email","task-commit@example.test")
   (repo/"exact.txt").write_text("before\n")
   self.git(repo,"add","exact.txt");self.git(repo,"commit","-q","-m","base")
   parent=self.git(repo,"rev-parse","HEAD").stdout.strip()
   (repo/"exact.txt").write_text("reviewed\n")
   message=canonical_message({
    "type":"fix","scope":"hooks","summary":"运行真实提交钩子",
    "background":"隔离事务需要普通提交语义。","changes":"执行四类提交钩子。",
    "boundaries":"不发布无关状态。","validations":"真实仓库回归测试。",
   },211)
   evidence=Path(temporary)/"evidence";evidence.mkdir()
   expected_message=evidence/"message";expected_message.write_text(message["bytes"])
   hook_log=evidence/"hooks.log"
   hooks=repo/".git/hooks"
   scripts={
    "pre-commit":f'''#!/bin/sh
set -eu
test "$(git rev-parse HEAD)" = "{parent}"
test "$(git show :exact.txt)" = "reviewed"
test "$(cat exact.txt)" = "reviewed"
printf '%s\\n' pre-commit >> "{hook_log}"
''',
    "prepare-commit-msg":f'''#!/bin/sh
set -eu
cmp "$1" "{expected_message}"
test "$2" = message
printf '%s\\n' prepare-commit-msg >> "{hook_log}"
''',
    "commit-msg":f'''#!/bin/sh
set -eu
cmp "$1" "{expected_message}"
printf '%s\\n' commit-msg >> "{hook_log}"
''',
    "post-commit":f'''#!/bin/sh
set -eu
test "$(git show -s --format=%P HEAD)" = "{parent}"
test "$(git show HEAD:exact.txt)" = "reviewed"
printf '%s\\n' post-commit >> "{hook_log}"
''',
   }
   for name,body in scripts.items():
    path=hooks/name;path.write_text(body);path.chmod(path.stat().st_mode|stat.S_IXUSR)
   snapshot=capture_snapshot(repo)
   candidate={
    "$schema":"https://github.com/castbox/guru-trellis/schemas/guru-task-commit-candidate-5.0.json",
    "schema_version":"5.0","skill_id":"guru-create-task-commit","sequence":"001",
    "task":{"id":"08-12-hooks","path":".trellis/tasks/08-12-hooks","status":"in_progress","branch":"feature/hooks"},
    "git":{"base_branch":"main","base_ref":"main","pre_commit_head":parent,"phase2_commit_anchor":parent},
    "dirty_snapshot":snapshot,
    "path_classifications":[{"path":"exact.txt","category":"task-reviewed","reason":"requested","coverage_source":"phase2"}],
    "exact_stage_paths":["exact.txt"],"message":message,
    "ai_review":{"status":"passed","summary":"reviewed","evidence":["phase2"]},
   }
   candidate_path=repo/"candidate.json";candidate_path.write_text(json.dumps(candidate,ensure_ascii=False))
   result=execute_commit(PACKAGE,{},["--root",str(repo),"--candidate-artifact",str(candidate_path)])
   self.assertEqual("committed",result["exit"])
   self.assertEqual(["pre-commit","prepare-commit-msg","commit-msg","post-commit"],hook_log.read_text().splitlines())
   self.assertEqual(parent,self.git(repo,"show","-s","--format=%P","HEAD").stdout.strip())
   raw=self.git(repo,"cat-file","commit","HEAD").stdout
   self.assertEqual(message["bytes"],raw.partition("\n\n")[2])

 def test_exact_file_commit_preserves_parent_gitlink_and_unrelated_live_state(self):
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary);submodule=root/"submodule";repo=root/"repo";submodule.mkdir();repo.mkdir()
   self.git(submodule,"init","-q","-b","main");self.git(submodule,"config","user.name","Submodule Test");self.git(submodule,"config","user.email","submodule@example.test")
   (submodule/"content.txt").write_text("submodule\n");self.git(submodule,"add","content.txt");self.git(submodule,"commit","-q","-m","submodule base")
   gitlink_oid=self.git(submodule,"rev-parse","HEAD").stdout.strip()
   self.git(repo,"init","-q","-b","feature/hooks");self.git(repo,"config","user.name","Task Commit Test");self.git(repo,"config","user.email","task-commit@example.test")
   self.git(repo,"-c","protocol.file.allow=always","submodule","add","-q",str(submodule),"module")
   (repo/"exact.txt").write_text("before\n");(repo/"staged.txt").write_text("before\n");(repo/"unstaged.txt").write_text("before\n")
   self.git(repo,"add","exact.txt","staged.txt","unstaged.txt","module",".gitmodules");self.git(repo,"commit","-q","-m","base")
   parent=self.git(repo,"rev-parse","HEAD").stdout.strip()
   (repo/"exact.txt").write_text("reviewed\n");(repo/"staged.txt").write_text("staged\n");self.git(repo,"add","staged.txt")
   (repo/"unstaged.txt").write_text("unstaged\n");(repo/"untracked.txt").write_text("untracked\n")
   message=canonical_message({"type":"fix","scope":"hooks","summary":"保留父提交 gitlink","background":"隔离事务包含父树 gitlink。","changes":"仅提交普通文件。","boundaries":"保留无关工作区状态。","validations":"真实 submodule 仓库测试。"},211)
   snapshot=capture_snapshot(repo)
   classifications=[{"path":row["path"],"category":"task-reviewed" if row["path"]=="exact.txt" else "unrelated-preserved","reason":"reviewed" if row["path"]=="exact.txt" else "parallel state","coverage_source":"phase2" if row["path"]=="exact.txt" else "live snapshot"} for row in snapshot["entries"]]
   candidate={"$schema":"https://github.com/castbox/guru-trellis/schemas/guru-task-commit-candidate-5.0.json","schema_version":"5.0","skill_id":"guru-create-task-commit","sequence":"001","task":{"id":"08-12-hooks","path":".trellis/tasks/08-12-hooks","status":"in_progress","branch":"feature/hooks"},"git":{"base_branch":"main","base_ref":"main","pre_commit_head":parent,"phase2_commit_anchor":parent},"dirty_snapshot":snapshot,"path_classifications":classifications,"exact_stage_paths":["exact.txt"],"message":message,"ai_review":{"status":"passed","summary":"reviewed","evidence":["phase2"]}}
   candidate_path=repo/"candidate.json";candidate_path.write_text(json.dumps(candidate,ensure_ascii=False))
   unrelated_before=capture_snapshot(repo,{"candidate.json","exact.txt"})
   index_before=index_entries(repo,{"exact.txt"});worktrees_before={line for line in self.git(repo,"worktree","list","--porcelain").stdout.splitlines() if line.startswith("worktree ")}
   result=execute_commit(PACKAGE,{},["--root",str(repo),"--candidate-artifact",str(candidate_path)])
   self.assertEqual("committed",result["exit"])
   self.assertEqual(f"160000 commit {gitlink_oid}\tmodule",self.git(repo,"ls-tree",result["commit_sha"],"module").stdout.strip())
   self.assertEqual(index_before,index_entries(repo,{"exact.txt"}))
   self.assertEqual(unrelated_before,capture_snapshot(repo,{"candidate.json","exact.txt"}))
   self.assertEqual(worktrees_before,{line for line in self.git(repo,"worktree","list","--porcelain").stdout.splitlines() if line.startswith("worktree ")})

 def test_command_and_error_contract_close(self):
  commands=json.loads((PACKAGE/"commands.json").read_text())
  catalog=json.loads((PACKAGE/"errors/catalog.json").read_text())
  command_schema=json.loads((SKILLS/"schemas/skill-commands.schema.json").read_text())
  error_schema=json.loads((SKILLS/"schemas/skill-error-catalog.schema.json").read_text())
  self.assertEqual([],list(Draft202012Validator(command_schema).iter_errors(commands)))
  self.assertEqual([],list(Draft202012Validator(error_schema).iter_errors(catalog)))
  codes={x["code"] for x in catalog["errors"]}
  for command in commands["commands"]:
   self.assertEqual(PACKAGE.name,command["owner"])
   self.assertTrue((PACKAGE/command["entrypoint"]).is_file())
   self.assertLessEqual(set(command["errors"]),codes)

 def test_every_command_help_is_side_effect_free(self):
  commands=json.loads((PACKAGE/"commands.json").read_text())
  for command in commands["commands"]:
   before=subprocess.run(["git","status","--porcelain=v1"],cwd=SKILLS.parents[2],text=True,stdout=subprocess.PIPE).stdout
   with self.subTest(command=command["id"]):
    self.assertEqual(0,main(PACKAGE,[command["id"],"--help"]))
   after=subprocess.run(["git","status","--porcelain=v1"],cwd=SKILLS.parents[2],text=True,stdout=subprocess.PIPE).stdout
   self.assertEqual(before,after)

 def test_runtime_and_launchers_do_not_reference_monolith(self):
  for root in (PACKAGE/"runtime",PACKAGE/"scripts"):
   for path in root.iterdir():
    if path.is_file():
     self.assertNotIn("guru_team_trellis.py",path.read_text())
     self.assertNotIn("test_guru_team_trellis.py",path.read_text())

 def test_launchers_are_executable_and_bind_interface_validators(self):
  interface=json.loads((PACKAGE/"interface.json").read_text())
  for validator in interface["validators"]:
   wrapper=PACKAGE/validator["command"]
   self.assertTrue(os.access(wrapper,os.X_OK),wrapper)
   self.assertIn("source \"$LAUNCHER\" "+validator["runtime_command"],wrapper.read_text())

 def test_prepare_requires_live_task_and_phase2_context(self):
  output=io.StringIO()
  with contextlib.redirect_stdout(output):
   status=main(PACKAGE,["prepare-task-commit","--input","examples/public-initial-commit-input.json","--candidate-json","examples/task-commit-candidate.json","--json"])
  self.assertEqual(2,status)
  self.assertEqual("input.task_ref",json.loads(output.getvalue())["field_path"])

if __name__=="__main__": unittest.main()
