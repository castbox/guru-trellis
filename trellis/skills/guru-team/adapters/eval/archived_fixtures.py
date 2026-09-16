"""Post-owner transport fixtures, not evidence of native semantic review."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from adapters.eval.eval_constants import OWNER_INPUT
from adapters.eval.fixture_io import bind_review_input_argument, bind_semantic_result_argument, run_git
from adapters.eval.owner_runtime import load_package_owner_runtime


MERGE = "guru-merge-task-pr"
BRANCH = "guru-review-branch"
PUBLICATION = "guru-review-task-publication"
FINALIZER = "guru-finalize-task"
RECIPES = {
    "merge-archived-review": (MERGE, "archived_review_request"),
    "review-archived-passed": (BRANCH, "archived_review"),
    "review-archived-blocked": (BRANCH, "archived_review"),
    "publication-archived-ready": (PUBLICATION, "archived_publication_review"),
    "publication-archived-metadata-blocked": (PUBLICATION, "archived_publication_review"),
    "publication-archived-task-work-blocked": (PUBLICATION, "archived_publication_review"),
    "publication-archived-external-blocked": (PUBLICATION, "archived_publication_review"),
    "finalization-archived-review-refresh": (FINALIZER, "archived_review_refresh"),
}
FIXTURE_NOTE = "Post-owner deterministic fixture input; not native semantic-review evidence."


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def executable(path: Path, source: str) -> None:
    path.write_text(f"#!{sys.executable}\n" + source, encoding="utf-8")
    path.chmod(0o755)


def call(fixture: Path, skill: str, script: str, argv: list[str], environment: dict[str, str]) -> dict:
    package = fixture / ".trellis/guru-team/skills/packages" / skill
    env = {**os.environ, **environment, "PYTHONDONTWRITEBYTECODE": "1"}
    env.pop("GURU_TEAM_EVAL_STAGING", None)
    result = subprocess.run([str(package / "scripts" / script), "--root", str(fixture), *argv, "--json"],
                            cwd=fixture, env=env, text=True, capture_output=True)
    if result.returncode:
        raise ValueError(f"Archived post-owner wrapper failed: {skill}/{script}: {result.stdout or result.stderr}")
    output = json.loads(result.stdout)
    if not isinstance(output, dict):
        raise ValueError("Archived post-owner wrapper did not return one object")
    return output


def project(packages: Path, skill: str, output: dict) -> dict:
    """Consume actual producer stdout through the declared target-owned seed."""
    contracts = read(packages / skill / "interface.json")["public_contracts"]
    projection, = [row for row in contracts["projections"] if row["exit_id"] == output["exit_id"]]
    target = next(row for row in contracts["consumer_inputs"] if row["id"] == projection["consumer_input_id"])
    contract = target["contract"]
    if projection["operation"] != "select" or contract["kind"] != "skill_input_authoring_seed":
        raise ValueError("Archived fixture requires the declared select/authoring-seed edge")
    authoring = read(packages / target["consumer"]["id"] / contract["authoring_example"]["path"])
    return {**authoring, **{row["target"]: output[row["source"]] for row in projection["mappings"]}}


def build_archive(fixture: Path, target: Path) -> tuple[dict, dict, dict[str, str]]:
    from adapters.eval.production_fixtures import production_task_fixture

    owner = load_package_owner_runtime(target, FINALIZER)
    task, base = production_task_fixture(owner, fixture)
    (fixture / ".trellis/guru-team/config.yml").write_text(
        "workspace_mode: current\ngithub_repo: example/guru-extension\n", encoding="utf-8",
    )
    remote = fixture.parent / "archived-remote.git"
    run_git(fixture, "init", "-q", "--bare", str(remote))
    run_git(fixture, "config", f"url.{remote}.insteadOf", "https://github.com/example/guru-extension.git")
    run_git(fixture, "push", "-q", "origin", "main")
    started = subprocess.run([sys.executable, "-B", str(fixture / ".trellis/scripts/task.py"), "start", str(task)],
                             cwd=fixture, text=True, capture_output=True)
    if started.returncode:
        raise ValueError("Official task start failed in the archived post-owner fixture")
    (fixture / "src/production-eval.txt").write_text("Reviewed fixture change.\n", encoding="utf-8")
    run_git(fixture, "add", "-A")
    run_git(fixture, "commit", "-qm", "Prepare normal archived eval task")
    original_tip = run_git(fixture, "rev-parse", "HEAD")
    context = owner.load_task_runtime_identity(task, owner.load_config(fixture), allow_rebuild=False)
    plan = owner.build_finalization_plan(
        fixture, task, context, owner.task_json(task), repo="example/guru-extension", remote="origin",
        base_branch="main", head_branch="eval/current", branch_review_commit=original_tip,
        title="\u5f52\u6863\u590d\u5ba1 fixture", body="## \u53d8\u66f4\u6458\u8981\n\n- Preserve the exact completed archive during post-owner review transport.\n\nRefs #146\n\nExact trailing bytes.  \n",
        review_facts={"changed_paths": [".trellis/tasks/current/task.json", "src/production-eval.txt"]},
    )
    pr = {"number": 146, "url": "https://github.com/example/guru-extension/pull/146"}
    owner.write_json(task / owner.FINISH_SUMMARY_ARTIFACT, owner.closeout_summary_for_pr(plan, pr))
    archived, _ = owner.execute_archive_metadata_transaction(fixture, task, plan, bound_pr=pr)
    head = run_git(fixture, "rev-parse", "HEAD")
    pr.update(state="OPEN", isDraft=False, headRefName="eval/current", baseRefName="main", headRefOid=head,
              headRepository={"nameWithOwner": "example/guru-extension"}, headRepositoryOwner={"login": "example"}, isCrossRepository=False,
              title=plan["publish"]["title"], body=plan["publish"]["body"], mergeable="MERGEABLE",
              mergeStateStatus="CLEAN", reviewDecision="APPROVED", statusCheckRollup=[], mergedAt=None, mergeCommit=None)
    runtime = fixture / ".trellis/.runtime/guru-team/evals"
    provider = write(runtime / "archived-provider.json", {"pr": pr, "base": base})
    binary = runtime / "archived-bin"
    binary.mkdir()
    real_git = shutil.which("git")
    if not real_git:
        raise ValueError("Git is unavailable for archived fixture staging")
    executable(binary / "gh", '''import json, os, sys
from pathlib import Path
a = sys.argv[1:]
p = json.loads(Path(os.environ["ARCHIVED_EVAL_PROVIDER"]).read_text())
with Path(os.environ["ARCHIVED_EVAL_LOG"]).open("a") as log:
    log.write(json.dumps(["gh", *a]) + "\\n")
repository = "example/guru-extension"
bound = "--repo" in a and a[a.index("--repo") + 1] == repository
if a == ["--version"]: print("gh fixture"); sys.exit(0)
if a == ["auth", "status"]: sys.exit(0)
if a == ["api", "repos/" + repository]:
    result = {"full_name": repository, "default_branch": "main", "allow_merge_commit": True, "allow_squash_merge": False, "allow_rebase_merge": False}
elif a == ["api", "repos/" + repository + "/git/ref/heads/main"]:
    result = {"ref": "refs/heads/main", "object": {"sha": p["base"], "type": "commit"}}
elif a[:3] == ["pr", "view", "146"] and bound: result = p["pr"]
elif a[:2] == ["pr", "list"] and bound: result = [p["pr"]]
elif a[:3] == ["pr", "checks", "146"] and bound: result = []
else: print("Unsupported archived fixture operation", file=sys.stderr); sys.exit(91)
print(json.dumps(result))
''')
    executable(binary / "git", '''import json, os, sys
from pathlib import Path
a = sys.argv[1:]
with Path(os.environ["ARCHIVED_EVAL_LOG"]).open("a") as log:
    log.write(json.dumps(["git", *a]) + "\\n")
if a in (["remote", "get-url", "origin"], ["remote", "get-url", "--all", "origin"], ["remote", "get-url", "--push", "--all", "origin"]):
    print("https://github.com/example/guru-extension.git"); sys.exit(0)
if a and a[0] in {"push", "fetch", "commit", "add", "update-ref", "checkout", "switch", "merge", "reset", "rebase", "stash"}:
    print("Archived post-owner execution is read-only", file=sys.stderr); sys.exit(92)
os.execv(os.environ["ARCHIVED_EVAL_REAL_GIT"], [os.environ["ARCHIVED_EVAL_REAL_GIT"], *a])
''')
    environment = {"PATH": str(binary) + os.pathsep + os.environ.get("PATH", ""),
                   "ARCHIVED_EVAL_PROVIDER": str(provider), "ARCHIVED_EVAL_LOG": str(runtime / "archived-transport.jsonl"),
                   "ARCHIVED_EVAL_REAL_GIT": real_git}
    public = {"schema_version": "2.0", "profile": "archived_review_request", "mode": "workflow",
              "task_ref": archived.relative_to(fixture).as_posix(), "repo_ref": "example/guru-extension",
              "pr_number": 146, "expected_head_sha": head}
    return public, pr, environment


def branch_semantic(package: Path, head: str, blocked: bool) -> dict:
    example = read(package / "examples/review-gate.json")
    value = {key: example[key] for key in ("candidate_classifications", "semantic_review", "verification_evidence")}
    value["verification_evidence"]["evidence"] = [FIXTURE_NOTE]
    value["semantic_review"]["ai_review_gate"].update(status="blocked" if blocked else "archived_review_passed", summary=FIXTURE_NOTE)
    if blocked:
        candidate = value["candidate_classifications"][0]
        candidate["decision"] = "qualified_current"
        value["semantic_review"]["rejected_candidates"] = [r for r in value["semantic_review"]["rejected_candidates"] if r["candidate_ref"] != candidate["candidate_ref"]]
        value["semantic_review"]["qualified_findings"] = [{
            "candidate_ref": candidate["candidate_ref"], "disposition": "qualified_finding",
            "affected_behavior": "Required fixture behavior remains incomplete.", "path": "src/production-eval.txt",
            "evidence_refs": ["docs/requirements.md"], "finding_ref": "finding:fixture-behavior",
            "severity": "P2", "introduced_head": head, "fix_head": None, "closure_head": None,
            "status": "open", "closure_evidence": [],
        }]
    return value


def publication_semantic(package: Path, public: dict, pr: dict, recipe: str) -> dict:
    example = read(package / "examples/pr-readiness.json")
    value = {**public, **{key: example[key] for key in ("candidate_classifications", "dimensions", "findings", "conclusions")},
             "pr_payload": {"title": pr["title"], "body": pr["body"]}, "route": {"typed_exit": "archived_ready"}}
    route_class = {"publication-archived-metadata-blocked": "metadata_revision", "publication-archived-task-work-blocked": "task_work",
                   "publication-archived-external-blocked": "external_blocker"}.get(recipe)
    if route_class:
        state = "blocked" if route_class == "external_blocker" else "finding"
        value["dimensions"][0]["status"] = state
        value["conclusions"]["issue_scope"]["status"] = state
        value["route"] = {"typed_exit": "blocked", "reason_code": "fixture_current_finding", "remediation": "Resolve the fixture finding outside read-only review."}
        value["findings"] = [{"finding_ref": "publication:fixture-finding", "candidate_ref": value["candidate_classifications"][0]["candidate_ref"],
                              "dimension": value["dimensions"][0]["id"], "summary": FIXTURE_NOTE,
                              "scope_basis": "Current archived fixture contract.", "evidence_refs": ["current-pr"],
                              "affected_artifacts": ["PR body"], "route_class": route_class, "status": "open", "closure_evidence": []}]
    return value


def stage_archived_owner_execution(request: dict, fixture: Path, target: Path, request_package: Path,
                                   recipe: str, public_input_path: Path) -> tuple[Path, Path, dict[str, str]]:
    skill, profile = RECIPES[recipe]
    template = read(public_input_path)
    if request["skill_id"] != skill or template.get("profile") != profile or request.get("native_execution_mode", "post_owner") != "post_owner":
        raise ValueError("Archived fixture recipe requires its exact Skill/profile in post_owner mode")
    packages = fixture / ".trellis/guru-team/skills/packages"
    package = packages / skill
    for name in ("interface.json", "evals/evals.json"):
        if hashlib.sha256((package / name).read_bytes()).digest() != hashlib.sha256((request_package / name).read_bytes()).digest():
            raise ValueError("Archived staging package differs from the evaluated contract")
    public, pr, environment = build_archive(fixture, target)
    public["mode"] = template["mode"]
    runtime = fixture / ".trellis/.runtime/guru-team/evals"
    merge_review = read(packages / MERGE / "examples/archived-review-semantic-input.json")
    for dimension in merge_review["semantic_review"]["dimensions"]:
        dimension["summary"] = FIXTURE_NOTE
    merge_path = write(runtime / "merge-review.json", merge_review)
    write(fixture / OWNER_INPUT, public)
    if skill == MERGE:
        bind_review_input_argument(request, fixture, merge_path)
        return package, target, environment
    output = call(fixture, MERGE, "invoke.sh", ["--input", str(fixture / OWNER_INPUT), "--review-input", str(merge_path)], environment)
    public = project(packages, MERGE, output)
    public["mode"] = template["mode"]
    write(fixture / OWNER_INPUT, public)
    blocked = recipe == "review-archived-blocked"
    semantic_path = write(runtime / "branch-semantic.json", branch_semantic(packages / BRANCH, public["branch_review_commit"], blocked))
    call(fixture, BRANCH, "review-branch.sh", ["--task", public["task_ref"], "--skill-input", str(fixture / OWNER_INPUT),
         "--semantic-review-file", str(semantic_path), "--typed-exit", "blocked" if blocked else "archived_review_passed"], environment)
    call(fixture, BRANCH, "check-review-gate.sh", ["--task", public["task_ref"]], environment)
    if skill == BRANCH:
        return package, target, environment
    output = call(fixture, BRANCH, "invoke.sh", ["--input", str(fixture / OWNER_INPUT)], environment)
    public = project(packages, BRANCH, output)
    public["mode"] = template["mode"]
    write(fixture / OWNER_INPUT, public)
    publication_path = write(runtime / "publication-owner-input.json", publication_semantic(packages / PUBLICATION, public, pr, recipe))
    if skill == PUBLICATION:
        bind_semantic_result_argument(request, fixture, publication_path)
        return package, target, environment
    output = call(fixture, PUBLICATION, "invoke.sh", ["--input", str(fixture / OWNER_INPUT), "--semantic-result", str(publication_path)], environment)
    public = project(packages, PUBLICATION, output)
    public["mode"] = template["mode"]
    write(fixture / OWNER_INPUT, public)
    review = read(package / "examples/semantic-review-input.json")
    review["review"]["summary"] = FIXTURE_NOTE
    final_review = write(runtime / "semantic-review.json", review)
    bind_review_input_argument(request, fixture, final_review)
    return package, target, environment
