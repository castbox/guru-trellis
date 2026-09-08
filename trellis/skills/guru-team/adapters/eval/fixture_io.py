from __future__ import annotations

from pathlib import Path
from typing import Any
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys

from adapters.eval.eval_constants import (
    MANAGED_PYTHON_SHEBANG,
)


def run_git(root: Path, *arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments], cwd=root, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.strip()
        raise ValueError(f"owner staging git command failed: {' '.join(arguments)}: {detail}")
    return process.stdout.strip()

def commit_qualification_owner_fixture(root: Path) -> None:
    process = subprocess.run(
        ["git", "commit", "-q", "-m", "stage qualification production fixture"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={
            **os.environ,
            "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z",
            "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z",
        },
    )
    if process.returncode != 0:
        raise ValueError("qualification owner fixture commit failed")

def normalize_qualification_owner_extension(root: Path) -> None:
    extension_path = root / ".trellis/guru-team/extension.json"
    try:
        extension = json.loads(extension_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("qualification owner extension manifest is invalid") from exc
    if not isinstance(extension, dict) or not isinstance(extension.get("installed_at"), str):
        raise ValueError("qualification owner extension install identity is invalid")
    extension["installed_at"] = "2000-01-01T00:00:00Z"
    extension_path.write_text(
        json.dumps(extension, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

def owner_recipe(request: dict[str, Any]) -> tuple[str, Path, dict[str, Any]]:
    workdir = Path(request["workdir"]).resolve()
    recipe: str | None = None
    public_input: Path | None = None
    owner_staging: dict[str, Any] | None = None
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        staging = payload.get("owner_staging")
        if isinstance(staging, dict):
            candidate = staging.get("recipe")
            if not isinstance(candidate, str) or not candidate:
                raise ValueError("owner staging recipe is invalid")
            if recipe is not None:
                raise ValueError("multiple case files declare owner staging recipes")
            recipe = candidate
            owner_staging = copy.deepcopy(staging)
        if payload.get("profile") and payload.get("mode"):
            if public_input is not None:
                raise ValueError("multiple case files declare public inputs")
            public_input = path
    if recipe is None or public_input is None or owner_staging is None:
        raise ValueError("semantic case does not declare one owner staging recipe and public input")
    return recipe, public_input, owner_staging

def bind_owner_result_argument(
    request: dict[str, Any],
    fixture: Path,
    owner_result: Path | str,
) -> str:
    result_path = Path(owner_result).resolve()
    try:
        result_relative = result_path.relative_to(fixture.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError("owner result must stay inside the installed eval fixture") from exc
    if result_path.is_symlink() or not result_path.is_file():
        raise ValueError("owner result is unavailable or unsafe")

    workdir = Path(request["workdir"]).resolve()
    rewritten = 0
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        invocation = payload.get("public_invocation")
        arguments = invocation.get("arguments") if isinstance(invocation, dict) else None
        if not isinstance(arguments, list) or "--owner-result" not in arguments:
            continue
        index = arguments.index("--owner-result")
        if index + 1 >= len(arguments) or not isinstance(arguments[index + 1], str):
            raise ValueError("case owner-result invocation argument is invalid")
        arguments[index + 1] = result_relative
        path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
        rewritten += 1
    if rewritten != 1:
        raise ValueError("semantic case must declare one owner-result invocation argument")
    return result_relative

def bind_review_input_argument(
    request: dict[str, Any],
    fixture: Path,
    review_input: Path | str,
) -> str:
    review_path = Path(review_input).resolve()
    try:
        review_relative = review_path.relative_to(fixture.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError("review input must stay inside the installed eval fixture") from exc
    if review_path.is_symlink() or not review_path.is_file():
        raise ValueError("review input is unavailable or unsafe")

    workdir = Path(request["workdir"]).resolve()
    rewritten = 0
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        invocation = payload.get("public_invocation")
        arguments = invocation.get("arguments") if isinstance(invocation, dict) else None
        if not isinstance(arguments, list) or "--review-input" not in arguments:
            continue
        index = arguments.index("--review-input")
        if index + 1 >= len(arguments) or not isinstance(arguments[index + 1], str):
            raise ValueError("case review-input invocation argument is invalid")
        arguments[index + 1] = review_relative
        path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
        rewritten += 1
    if rewritten != 1:
        raise ValueError("semantic case must declare one review-input invocation argument")
    return review_relative

def bind_merge_gate_argument(
    request: dict[str, Any],
    fixture: Path,
    gate_path: Path,
) -> str:
    try:
        gate_relative = gate_path.resolve().relative_to(fixture.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError("merge gate must stay inside the installed eval fixture") from exc
    if gate_path.is_symlink() or not gate_path.is_file():
        raise ValueError("merge gate is unavailable or unsafe")

    workdir = Path(request["workdir"]).resolve()
    rewritten = 0
    for relative in request.get("files", []):
        path = workdir / str(relative)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        invocation = payload.get("public_invocation")
        arguments = invocation.get("arguments") if isinstance(invocation, dict) else None
        if not isinstance(arguments, list) or "--gate" not in arguments:
            continue
        index = arguments.index("--gate")
        if index + 1 >= len(arguments) or not isinstance(arguments[index + 1], str):
            raise ValueError("case merge-gate invocation argument is invalid")
        arguments[index + 1] = gate_relative
        path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
        rewritten += 1
    if rewritten != 1:
        raise ValueError("semantic merge case must declare one gate invocation argument")
    return gate_relative

def stage_clean_installed_owner_repo(
    execution_root: Path, runtime_target: Path, request_package: Path,
) -> tuple[Path, Path]:
    fixture = execution_root / "owner-repo"
    source_repo = runtime_target.parents[4]
    source_scripts = source_repo / ".trellis/scripts"
    source_workflow = source_repo / ".trellis/workflow.md"
    apply_script = source_repo / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py"
    if (
        source_scripts.is_symlink() or not source_scripts.is_dir()
        or source_workflow.is_symlink() or not source_workflow.is_file()
    ):
        raise ValueError("installed Trellis inputs are unavailable for owner staging")
    (fixture / ".trellis").mkdir(parents=True)
    shutil.copytree(
        source_scripts, fixture / ".trellis/scripts",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    shutil.copy2(source_workflow, fixture / ".trellis/workflow.md")
    (fixture / ".gitignore").write_text(
        ".trellis/.runtime/\n__pycache__/\n*.py[cod]\n",
        encoding="utf-8",
    )
    run_git(fixture, "init", "-q", "-b", "main")
    run_git(fixture, "config", "user.email", "stage0-eval@example.invalid")
    run_git(fixture, "config", "user.name", "Stage0 Eval")
    canonical_packages = source_repo / "trellis/skills/guru-team/packages"
    try:
        request_package.relative_to(canonical_packages)
        source_mode = True
    except ValueError:
        source_mode = False
    if source_mode:
        if apply_script.is_symlink() or not apply_script.is_file():
            raise ValueError("canonical preset inputs are unavailable for owner staging")
        canonical_workflow = source_repo / "trellis/workflows/guru-team/workflow.md"
        if canonical_workflow.is_symlink() or not canonical_workflow.is_file():
            raise ValueError("canonical workflow input is unavailable for owner staging")
        shutil.copy2(canonical_workflow, fixture / ".trellis/workflow.md")
        applied = subprocess.run(
            [sys.executable, str(apply_script), "--repo", str(fixture), "--all-platforms"],
            cwd=source_repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if applied.returncode != 0:
            raise ValueError("canonical preset apply failed during owner staging")
    else:
        installed_root = source_repo / ".trellis/guru-team"
        extension_path = installed_root / "extension.json"
        try:
            extension = json.loads(extension_path.read_text(encoding="utf-8"))
            skill_packages = extension["skill_packages"]
            files = skill_packages["files"]
            overlays = extension["overlays"]
            overlay_files = overlays["files"]
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("installed Skill and overlay provenance is unavailable") from exc
        if (
            not isinstance(skill_packages, dict)
            or skill_packages.get("status") != "ok"
            or skill_packages.get("conflicts") != []
            or skill_packages.get("sidecars") != []
            or not isinstance(files, list)
            or not isinstance(overlays, dict)
            or overlays.get("status") != "ok"
            or overlays.get("conflicts") != []
            or overlays.get("sidecars") != []
            or not isinstance(overlay_files, list)
            or installed_root.is_symlink() or not installed_root.is_dir()
        ):
            raise ValueError("installed Skill and overlay provenance is not reusable")
        shutil.copytree(
            installed_root, fixture / ".trellis/guru-team", dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        copied_paths: set[str] = set()
        for row in [*files, *overlay_files]:
            if not isinstance(row, dict) or not isinstance(row.get("path"), str):
                raise ValueError("installed Skill or overlay file provenance is invalid")
            relative = Path(row["path"])
            relative_text = relative.as_posix()
            if (
                relative.is_absolute()
                or not relative.parts
                or ".." in relative.parts
                or relative_text in copied_paths
            ):
                raise ValueError("installed Skill or overlay file provenance path is unsafe")
            copied_paths.add(relative_text)
            source = source_repo / relative
            target = fixture / relative
            expected_sha256 = row.get("sha256")
            if (
                source.is_symlink() or not source.is_file()
                or not isinstance(expected_sha256, str)
                or hashlib.sha256(source.read_bytes()).hexdigest() != expected_sha256
            ):
                raise ValueError("installed Skill or overlay provenance does not match live bytes")
            if relative.parts[:3] == (".trellis", "guru-team", "skills"):
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        runtime_assets = fixture / ".trellis/guru-team/runtime"
        bootstrap = runtime_assets / "bootstrap.py"
        if bootstrap.is_symlink() or not bootstrap.is_file():
            raise ValueError("installed managed runtime bootstrap is unavailable")
        runtime = subprocess.run(
            [
                sys.executable,
                str(bootstrap),
                "--repo",
                str(fixture),
                "--runtime-assets",
                str(runtime_assets),
                "--python",
                sys.executable,
                "--json",
            ],
            cwd=fixture,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if runtime.returncode != 0:
            raise ValueError("installed managed runtime bootstrap failed during owner staging")
    return fixture, source_repo

def write_fake_gh(execution_root: Path, recipe: str) -> Path:
    binary = execution_root / "owner-bin"
    binary.mkdir(parents=True, exist_ok=True)
    target = binary / "gh"
    issue_145_state = "CLOSED" if recipe == "clarity-new-task" else "OPEN"
    workspace_recipe = recipe.startswith("workspace-")
    issue_title = (
        "Stage 0 workspace owner staging"
        if workspace_recipe else "Issue 145 owner staging"
    )
    issue_body = (
        "The current Intake workflow is one independently deliverable unit."
        if workspace_recipe else "Issue 145 owner staging body"
    )
    issue_assignees = [{"login": "stage0-eval"}] if workspace_recipe else []
    target.write_text(
        MANAGED_PYTHON_SHEBANG
        +
        "import json,sys\n"
        f"states={{145:{issue_145_state!r},146:'OPEN'}}\n"
        f"titles={{145:{issue_title!r},146:'Issue 146 owner staging'}}\n"
        f"bodies={{145:{issue_body!r},146:'Issue 146 owner staging body'}}\n"
        f"assignees={{145:{issue_assignees!r},146:[]}}\n"
        "args=sys.argv[1:]\n"
        "if args[:2]==['auth','status']:\n"
        " raise SystemExit(0)\n"
        "if args[:2]==['api','user']:\n"
        " print(json.dumps({'login':'stage0-eval'})); raise SystemExit(0)\n"
        "if len(args)>=3 and args[:2]==['issue','view']:\n"
        " number=int(args[2]); state=states.get(number,'OPEN')\n"
        " title=titles.get(number,f'Issue {number} owner staging'); body=bodies.get(number,f'Issue {number} owner staging body')\n"
        " print(json.dumps({'number':number,'url':f'https://github.com/example/guru-extension/issues/{number}',"
        "'state':state,'updatedAt':'2026-01-01T00:00:00Z','title':title,'body':body,"
        "'comments':[],'assignees':assignees.get(number,[]),'labels':[]}))\n"
        " raise SystemExit(0)\n"
        "print('unsupported fake gh invocation',file=sys.stderr); raise SystemExit(2)\n",
        encoding="utf-8",
    )
    target.chmod(0o755)
    real_git = shutil.which("git")
    if real_git is None:
        raise ValueError("git is unavailable for owner staging")
    git_target = binary / "git"
    git_target.write_text(
        MANAGED_PYTHON_SHEBANG
        +
        "import os,subprocess,sys\n"
        f"real_git={real_git!r}\n"
        f"workspace_recipe={workspace_recipe!r}\n"
        "args=sys.argv[1:]\n"
        "if args and args[0]=='fetch': raise SystemExit(0)\n"
        "if workspace_recipe and args==['ls-remote','--heads','origin','main']:\n"
        " head=subprocess.run([real_git,'rev-parse','--verify','refs/remotes/origin/main'],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)\n"
        " if head.returncode!=0: raise SystemExit(head.returncode)\n"
        " print(f'{head.stdout.strip()}\\trefs/heads/main'); raise SystemExit(0)\n"
        "os.execv(real_git,[real_git,*args])\n",
        encoding="utf-8",
    )
    git_target.chmod(0o755)
    return binary

def write_fake_merge_gh(
    execution_root: Path,
    recipe: str,
    *,
    repo_ref: str = "castbox/guru-trellis",
    pr_number: int = 176,
    issue_number: int = 174,
    head_sha: str | None = None,
    base_branch: str | None = None,
    head_branch: str | None = None,
) -> Path:
    configurations = {
        "merge-workflow-merged": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "body": "Closes #174\n",
            "closure_mismatch": False,
        },
        "merge-standalone-draft-blocked": {
            "draft": True,
            "head": "1" * 40,
            "merge_state_status": "BLOCKED",
            "body": "Closes #174\n",
            "closure_mismatch": False,
        },
        "merge-workflow-head-drift-blocked": {
            "draft": False,
            "head": "3" * 40,
            "merge_state_status": "CLEAN",
            "body": "Closes #174\n",
            "closure_mismatch": False,
        },
        "merge-workflow-branch-drift-blocked": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "base_branch": "release",
            "head_branch": "codex/other-task",
            "body": "Closes #174\n",
            "closure_mismatch": False,
        },
        "merge-workflow-added-close-scope-blocked": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "body": "Closes #174\nCloses #180\n",
            "closure_mismatch": False,
        },
        "merge-workflow-close-scope-blocked": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "body": "Related #174\n",
            "closure_mismatch": False,
        },
        "merge-workflow-closure-mismatch": {
            "draft": False,
            "head": "1" * 40,
            "merge_state_status": "CLEAN",
            "body": "Closes #174\n",
            "closure_mismatch": True,
        },
    }
    configuration = copy.deepcopy(configurations.get(recipe))
    if configuration is None:
        raise ValueError(f"unsupported merge owner staging recipe: {recipe}")
    if head_sha is not None:
        configuration["head"] = head_sha
    if base_branch is not None:
        configuration["base_branch"] = base_branch
    if head_branch is not None:
        configuration["head_branch"] = head_branch
    binary = execution_root / "merge-owner-bin"
    binary.mkdir(parents=True, exist_ok=True)
    state_path = binary / "state.json"
    state_path.write_text(
        json.dumps({"merged": False, "calls": []}) + "\n",
        encoding="utf-8",
    )
    target = binary / "gh"
    target.write_text(
        MANAGED_PYTHON_SHEBANG
        +
        "import json,sys\n"
        "from pathlib import Path\n"
        f"state_path={str(state_path)!r}\n"
        f"config={configuration!r}\n"
        f"repo={repo_ref!r}; number={pr_number!r}; issue_number={issue_number!r}\n"
        "base_head='0'*40; merge_sha='2'*40\n"
        "args=sys.argv[1:]\n"
        "state=json.load(open(state_path,encoding='utf-8'))\n"
        "state.setdefault('calls',[]).append(args)\n"
        "open(state_path,'w',encoding='utf-8').write(json.dumps(state)+'\\n')\n"
        "pr_url=f'https://github.com/{repo}/pull/{number}'\n"
        "issue_url=f'https://github.com/{repo}/issues/{issue_number}'\n"
        "if args==['auth','status']:\n"
        " raise SystemExit(0)\n"
        "if len(args)>=2 and args[:2]==['pr','view']:\n"
        " payload={'number':number,'url':pr_url,'state':'MERGED' if state['merged'] else 'OPEN',"
        "'isDraft':config['draft'],'baseRefName':config.get('base_branch','main'),"
        "'headRefName':config.get('head_branch','codex/180-eval'),"
        "'headRefOid':config['head'],'mergeable':'MERGEABLE',"
        "'mergeStateStatus':config['merge_state_status'],'reviewDecision':'APPROVED',"
        "'statusCheckRollup':[{'name':'contract','conclusion':'SUCCESS'}],'body':config['body'],"
        "'mergedAt':'2026-08-05T06:21:00Z' if state['merged'] else None,"
        "'mergeCommit':{'oid':'2'*40} if state['merged'] else None}\n"
        " print(json.dumps(payload)); raise SystemExit(0)\n"
        "if args[:2]==['api',f'repos/{repo}']:\n"
        " print(json.dumps({'full_name':repo,'allow_merge_commit':True,'allow_squash_merge':False,'allow_rebase_merge':False})); raise SystemExit(0)\n"
        "if len(args)>=2 and args[0]=='api' and args[1].startswith(f'repos/{repo}/git/ref/heads/'):\n"
        " branch_ref=args[1].split('/git/ref/heads/',1)[1]\n"
        " current=merge_sha if state['merged'] else base_head\n"
        " print(json.dumps({'ref':f'refs/heads/{branch_ref}','object':{'sha':current}})); raise SystemExit(0)\n"
        "if args[:2]==['api',f'repos/{repo}/git/commits/{merge_sha}']:\n"
        " commit=state.get('commit')\n"
        " if not commit: raise SystemExit(2)\n"
        " print(json.dumps(commit,ensure_ascii=False)); raise SystemExit(0)\n"
        "if len(args)>=3 and args[:2]==['issue','view']:\n"
        " closed=state['merged'] and not config['closure_mismatch']\n"
        " print(json.dumps({'number':issue_number,'state':'CLOSED' if closed else 'OPEN',"
        "'closedAt':'2026-08-05T06:21:05Z' if closed else None,'url':issue_url})); raise SystemExit(0)\n"
        "if len(args)>=3 and args[:2]==['pr','merge']:\n"
        " expected=args[args.index('--match-head-commit')+1] if '--match-head-commit' in args else ''\n"
        " subject=args[args.index('--subject')+1] if '--subject' in args else ''\n"
        " body_file=args[args.index('--body-file')+1] if '--body-file' in args else ''\n"
        " body=Path(body_file).read_text(encoding='utf-8') if body_file else ''\n"
        " if expected!=config['head'] or config['draft'] or not config['body'].startswith('Closes #') or '--merge' not in args or not subject.startswith('chore(merge): #') or not body:\n"
        "  print('merge precondition failed',file=sys.stderr); raise SystemExit(1)\n"
        " state['merged']=True\n"
        " state['commit']={'sha':merge_sha,'message':subject+'\\n\\n'+body,'parents':[{'sha':base_head},{'sha':config['head']}]}\n"
        " open(state_path,'w',encoding='utf-8').write(json.dumps(state)+'\\n')\n"
        " raise SystemExit(0)\n"
        "print('unsupported merge fake gh invocation: '+repr(args),file=sys.stderr); raise SystemExit(2)\n",
        encoding="utf-8",
    )
    target.chmod(0o755)
    return binary

def with_path_prefix(binary: Path, callback: Any) -> Any:
    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = f"{binary}{os.pathsep}{previous_path or ''}"
    try:
        return callback()
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path
