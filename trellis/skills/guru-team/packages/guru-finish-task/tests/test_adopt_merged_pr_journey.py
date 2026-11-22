"""Exercise the installed owners with real Git and a local GitHub substitute."""

import json
import os
import subprocess
import sys
from pathlib import Path

from .test_finish_contract import ROOT, current_task_metadata, git, write_fake_gh
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore


def write_adoption_provider(directory):
    write_fake_gh(directory / "bookkeeping-gh")
    gh = directory / "gh"
    gh.write_text(
        "#!" + sys.executable + "\n" + """import json, os, sys
from pathlib import Path

args = sys.argv[1:]
facts = json.loads(Path(os.environ["ADOPTION_PROVIDER_FACTS"]).read_text())
if args[:2] == ["auth", "status"]:
    sys.exit(0)
if args[0] == "api":
    value = facts["api"][args[1]]
elif args[:3] == ["pr", "view", str(facts["pr"]["number"])]:
    value = facts["pr"]
else:
    if args[:2] == ["issue", "close"]:
        raise SystemExit("the source Issue is already closed")
    if args[:3] == ["pr", "merge", str(facts["pr"]["number"])]:
        raise SystemExit("the original PR is already merged")
    helper = str(Path(__file__).with_name("bookkeeping-gh"))
    os.execv(helper, [helper, *args])
with Path(os.environ["FAKE_GH_LOG"]).open("a") as log:
    log.write(json.dumps(args) + "\\n")
print(json.dumps(value))
""",
        encoding="utf-8",
    )
    gh.chmod(0o755)


def test_adopt_merged_pr_completes_and_archives_original_task(tmp_path):
    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    repo.mkdir()
    git(repo, "init", "-qb", "main")
    git(repo, "init", "-q", "--bare", str(remote))
    git(repo, "config", "user.email", "fixture@example.invalid")
    git(repo, "config", "user.name", "Journey fixture")
    repo_ref = "example/repo"
    remote_url = f"https://github.com/{repo_ref}.git"
    git(repo, "remote", "add", "origin", remote_url)
    # Route every fixture Git push to a local bare repository.
    git(repo, "config", f"url.{remote}.insteadOf", remote_url)
    (repo / ".gitignore").write_text(".trellis/.runtime/\n__pycache__/\n")
    issue_number = 7
    source = {"kind": "issue", "repo_ref": repo_ref, "number": issue_number, "disposition": "exact_source"}
    task_id = "adopted-delivery"
    task_ref = f".trellis/tasks/{task_id}"
    branch = f"codex/{task_id}"
    task_key = {"task_id": task_id, "lifecycle_generation": 0}
    delivery_key = {**task_key, "delivery_id": "43134b50-2c8b-4d70-b114-218a735a82e2"}
    # Start with the real Task2 creator's bytes and install the matching preset.
    original_task = current_task_metadata(repo, task_id, 0, source)
    sdk_package = Path(os.environ["GURU_UPSTREAM_DELIVERY_SCRIPTS"]).parents[3] / "package.json"
    (repo / ".trellis/.version").write_text(json.loads(sdk_package.read_text())["version"] + "\n")
    applied = subprocess.run(
        ["bash", str(ROOT.parents[2] / "trellis/presets/guru-team/scripts/bash/apply.sh"), "--repo", str(repo)],
        cwd=ROOT.parents[2], text=True, capture_output=True,
    )
    assert applied.returncode == 0, applied.stdout + applied.stderr
    assert json.loads(applied.stdout)["skill_installed_validation"]["returncode"] == 0

    (repo / "README.md").write_text("Journey fixture.\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "Start the target branch")
    base = git(repo, "rev-parse", "HEAD")
    git(repo, "switch", "-qc", branch)
    task_dir = repo / task_ref
    task_dir.mkdir(parents=True)
    (task_dir / "task.json").write_text(json.dumps(original_task))
    (task_dir / "prd.md").write_text("R1: Deliver the working greeting to main.\n")
    projection = DeliveryProjection(repo, task_ref)
    scope = authority_ref(task_dir / "prd.md", repo)
    projection.scope(scope)
    owners = projection.declaration()["owners"]
    scope_ref = {"authority": scope, "anchors": ["R1"]}
    projection.apply({
        "api_version": "1.0", "operation": "create_delivery", "key": delivery_key,
        "owner_role": "creation", "owner_id": owners["creation"], "profile": "pull_request",
        "scope_ref": scope_ref,
    })
    planning = projection.planning_directory(delivery_key)
    planning.mkdir(parents=True, exist_ok=True)
    (planning / "prd.md").write_text("Deliver the working greeting in this PR.\n")
    (planning / "design.md").write_text("A Python script prints one greeting.\n")
    (planning / "implement.md").write_text("Run the script and check the greeting.\n")
    projection.apply({
        "api_version": "1.0", "operation": "record_gate", "key": delivery_key,
        "owner_role": "planning", "owner_id": owners["planning"], "expected_phase": "planning",
        "result": {
            "result_id": "planning:journey", "owner_role": "planning", "owner_id": owners["planning"],
            "outcome": "accepted", "scope_ref": scope_ref, "plan_ref": authority_ref(planning / "design.md", repo),
            "candidate": None, "predecessor_result_id": None, "obligations": [], "evidence": [scope],
        },
    })
    original_delivery = projection.resolve(delivery_key)
    assert original_delivery["phase"] == "implementing"
    assert original_delivery["publication_result"] is None
    assert original_delivery["delivery_result"] is None

    (repo / "greeting.py").write_text('print("hello from the merged PR")\n')
    git(repo, "add", task_ref, "greeting.py")
    git(repo, "commit", "-qm", "Deliver the greeting")
    head = git(repo, "rev-parse", "HEAD")
    git(repo, "switch", "-q", "main")
    git(repo, "merge", "--no-ff", "-qm", "Merge the greeting PR outside Guru", branch)
    merge = git(repo, "rev-parse", "HEAD")
    assert git(repo, "rev-list", "--parents", "-n", "1", merge).split() == [merge, base, head]
    git(repo, "push", "-q", "-u", "origin", "main")
    git(repo, "switch", "-q", branch)
    lifecycle_key = TaskLifecycleKey(task_id, 0)
    store = ResourceLedgerStore(inspect_repository(repo))
    binding = BranchBindingStore(store.repository).establish(lifecycle_key, branch)
    store.establish_current(lifecycle_key, binding_revision=binding.binding_revision, branch_name=branch,
                            branch_ownership="guru_owned", worktree_ownership="not_applicable")

    # The substitute reports the Git objects created above and one historical CI fact.
    pr_number = 42
    pr_ref = f"https://github.com/{repo_ref}/pull/{pr_number}"
    merged_at = "2026-09-19T00:00:00Z"
    checks = [{"name": "optional job", "status": "COMPLETED", "conclusion": "FAILURE"}]
    provider_facts = {
        "api": {
            f"repos/{repo_ref}": {"full_name": repo_ref},
            f"repos/{repo_ref}/pulls/{pr_number}": {
                "number": pr_number, "state": "closed", "merged_at": merged_at, "merge_commit_sha": merge,
                "base": {"ref": "main", "repo": {"full_name": repo_ref}},
                "head": {"sha": head, "repo": {"full_name": repo_ref}},
            },
            f"repos/{repo_ref}/git/commits/{merge}": {"sha": merge, "parents": [{"sha": base}, {"sha": head}]},
            f"repos/{repo_ref}/git/ref/heads/main": {"object": {"sha": merge}},
        },
        "pr": {
            "number": pr_number, "url": pr_ref, "state": "MERGED", "mergedAt": merged_at,
            "headRefOid": head, "baseRefName": "main", "mergeCommit": {"oid": merge}, "statusCheckRollup": checks,
            "reviewDecision": "",
        },
    }
    facts_path = tmp_path / "adoption-facts.json"
    facts_path.write_text(json.dumps(provider_facts))
    state_path = tmp_path / "gh-state.json"
    state_path.write_text(json.dumps({"issue_state": "CLOSED"}))
    log = tmp_path / "gh.log"
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    write_adoption_provider(fake_bin)
    env = {
        **os.environ, "PATH": str(fake_bin) + os.pathsep + os.environ["PATH"],
        "FAKE_GH_STATE": str(state_path), "FAKE_GH_LOG": str(log),
        "FAKE_REPO_PATH": str(repo), "FAKE_REMOTE_PATH": str(remote),
        "ADOPTION_PROVIDER_FACTS": str(facts_path),
    }
    installed = repo / ".trellis/guru-team/skills/packages"

    def invoke(skill, public, review, *flags, review_flag="--semantic-result"):
        public_path = tmp_path / f"{skill}-input.json"
        semantic_path = tmp_path / f"{skill}-review.json"
        public_path.write_text(json.dumps(public))
        semantic_path.write_text(json.dumps(review))
        result = subprocess.run(
            ["bash", str(installed / skill / "scripts/invoke.sh"), "--root", str(repo),
             "--input", str(public_path), review_flag, str(semantic_path), *flags],
            cwd=repo, env=env, text=True, capture_output=True,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        return json.loads(result.stdout)

    adoption = invoke(
        "guru-merge-task-delivery",
        {"profile": "delivery_adopt_merged_pr", "mode": "workflow", "task_ref": task_ref,
         "delivery_key": delivery_key, "repo_ref": repo_ref, "pr_number": pr_number},
        {"reviewed_delivery_key": delivery_key, "reviewed_scope_ref": scope_ref,
         "reviewed_pr": {"repo_ref": repo_ref, "pr_number": pr_number, "head_sha": head,
                         "merge_sha": merge, "target_ref": "main"},
         "observed_checks": checks,
         "ai_review_gate": {"status": "passed", "summary": "Read the PR and landed ranges and the historical optional check."}},
        review_flag="--review-input",
    )
    assert adoption == {"exit_id": "delivered", "task_ref": task_ref, "task_key": task_key}
    accepted_delivery = projection.resolve(delivery_key)
    delivery_fact = accepted_delivery["delivery_result"]
    assert delivery_fact["merge_commit"] == merge
    assert delivery_fact["candidate"]["head_ref"] == head
    assert accepted_delivery["publication_result"] is None
    assert accepted_delivery["results"] == original_delivery["results"]
    assert projection.read_record()["completion_results"] == []

    # Obtain acceptance evidence from the delivered tree. Optional historical CI is separate.
    landed_script = git(repo, "show", f"{delivery_fact['merge_commit']}:greeting.py")
    executed = subprocess.run([sys.executable, "-"], input=landed_script, text=True, capture_output=True, check=True)
    assert executed.stdout == "hello from the merged PR\n"
    completed = invoke(
        "guru-review-task-completion",
        {"profile": "delivery_completion", "mode": "workflow", "task_ref": adoption["task_ref"],
         "task_key": adoption["task_key"]},
        {"profile": "delivery_completion", "mode": "workflow", "reviewed_task_key": adoption["task_key"],
         "reviewed_scope": scope, "reviewed_delivery_result_ids": [delivery_fact["result_id"]],
         "evidence": delivery_fact["evidence"], "remaining_work_refs": [], "result_id": "completion:journey",
         "route": {"typed_exit": "completed"}},
    )
    assert completed["exit_id"] == "completed"
    actions = [{"issue_ref": {"repo_ref": repo_ref, "issue_number": issue_number}, "disposition": "already_closed_at_review"}]
    closed = invoke(
        "guru-complete-task-closure",
        {"profile": "completion_approved", "source_exit": completed["exit_id"], "mode": "workflow",
         "completion_result": completed["result_ref"], "source": source, "accepted_scope_identity": scope["revision"],
         "delivery_target": {"repo_ref": repo_ref, "branch_ref": "main"}, "content_head": head,
         "binding_ref": {**task_key, "binding_revision": binding.binding_revision},
         "evidence_slots": {"completion": completed["result_ref"]["result_id"]}, "action_set": actions},
        {"profile": "completion_approved", "mode": "workflow", "reviewed_action_set": actions,
         "route": {"typed_exit": "apply"}},
    )
    assert closed["exit_id"] == "closed"

    archive_ref = f".trellis/tasks/archive/2026-09/{task_id}"
    finish_input = {"profile": "closure_completed", "mode": "standalone", "closure_result": closed["result_ref"]}
    finish_review = {
        "profile": "closure_completed", "mode": "standalone", "allowlist": [task_ref, archive_ref],
        "bookkeeping": {
            "repo_ref": repo_ref, "base_branch": "main", "head_branch": branch, "archive_ref": archive_ref,
            "commit_subject": "chore(trellis): 归档已验收任务", "commit_body": "记录原任务收尾。\n\nRefs #7",
            "pr_title": "归档已验收任务", "pr_body": "仅归档原任务。\n\nRefs #7",
            "merge_subject": "chore(merge): 合入任务归档", "merge_body": "合入已审核的归档。\n\nRefs #7",
        },
        "route": {"typed_exit": "success"},
    }
    for flag in ("--confirmed-finish", "--confirmed-bookkeeping-publish"):
        out = invoke("guru-finish-task", finish_input, finish_review, flag)
        assert out["exit_id"] == "resume_finish", out
    finished = invoke("guru-finish-task", finish_input, finish_review, "--confirmed-bookkeeping-merge")
    assert finished["exit_id"] == "success", finished

    target = git(remote, "rev-parse", "refs/heads/main")
    assert git(repo, "rev-parse", f"{target}^1") == merge
    archived = json.loads(git(repo, "show", f"{target}:{archive_ref}/task.json"))
    assert (archived["id"], archived["lifecycle_generation"], archived["source"]) == (task_id, 0, source)
    assert archived["deliveries"] == [accepted_delivery]
    assert archived["completion_results"][0]["delivery_result_ids"] == [delivery_fact["result_id"]]
    assert archived["closure_results"][0]["result_id"] == closed["result_ref"]["result_id"]
    assert git(repo, "ls-tree", target, "--", f"{archive_ref}/finish-summary.json")
    assert not git(repo, "ls-tree", target, "--", task_ref)
    calls = [json.loads(line) for line in log.read_text().splitlines()]
    assert any(row[:3] == ["issue", "view", str(issue_number)] for row in calls)
    assert not any(row[:2] == ["issue", "close"] for row in calls)
    assert [row[2] for row in calls if row[:2] == ["pr", "merge"]] == ["7"]
