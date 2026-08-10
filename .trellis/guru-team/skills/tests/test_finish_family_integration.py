from __future__ import annotations

import argparse
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock


SOURCE_REPO = Path(__file__).resolve().parents[4]
EXECUTION_MODE = os.environ.get("GURU_FINISH_INTEGRATION_MODE", "source")
if EXECUTION_MODE not in {"source", "installed"}:
    raise RuntimeError("GURU_FINISH_INTEGRATION_MODE must be source or installed")
REPO = Path(
    os.environ.get("GURU_FINISH_INTEGRATION_ROOT", str(SOURCE_REPO))
).resolve()
EXTENSION_SOURCE_REPO = Path(
    os.environ.get("GURU_FINISH_INTEGRATION_SOURCE_ROOT", str(SOURCE_REPO))
).resolve()
if EXECUTION_MODE == "installed":
    SKILLS_ROOT = REPO / ".trellis/guru-team/skills"
    WORKFLOW = REPO / ".trellis/workflow.md"
    EVAL_RUNNER = REPO / ".trellis/guru-team/scripts/bash/run-skill-evals.sh"
else:
    SKILLS_ROOT = REPO / "trellis/skills/guru-team"
    WORKFLOW = REPO / "trellis/workflows/guru-team/workflow.md"
    EVAL_RUNNER = (
        REPO / "trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh"
    )

FINISH_EXITS = {
    "guru-review-task-publication": {"ready", "return_to_task_work", "blocked"},
    "guru-verify-extension-installation": {
        "verified", "not_required", "return_to_task_work", "blocked",
    },
    "guru-finalize-task": {
        "verification_required", "publication_review_stale",
        "resume_finalization", "reprepare_required", "ready_for_merge", "blocked",
    },
    "guru-merge-task-pr": {"merged", "merge_blocked", "closure_mismatch"},
}
EXPECTED_CONSUMERS = {
    ("guru-review-task-publication", "ready"): ("skill", "guru-finalize-task"),
    ("guru-review-task-publication", "return_to_task_work"): (
        "workflow", "guru-task-publication-work-router",
    ),
    ("guru-review-task-publication", "blocked"): (
        "stop", "task-publication-review-blocked",
    ),
    ("guru-verify-extension-installation", "verified"): (
        "skill", "guru-finalize-task",
    ),
    ("guru-verify-extension-installation", "not_required"): (
        "skill", "guru-finalize-task",
    ),
    ("guru-verify-extension-installation", "return_to_task_work"): (
        "workflow", "guru-extension-verification-work-router",
    ),
    ("guru-verify-extension-installation", "blocked"): (
        "stop", "extension-installation-verification-blocked",
    ),
    ("guru-finalize-task", "verification_required"): (
        "skill", "guru-verify-extension-installation",
    ),
    ("guru-finalize-task", "publication_review_stale"): (
        "skill", "guru-review-task-publication",
    ),
    ("guru-finalize-task", "resume_finalization"): (
        "skill", "guru-finalize-task",
    ),
    ("guru-finalize-task", "reprepare_required"): (
        "skill", "guru-finalize-task",
    ),
    ("guru-finalize-task", "ready_for_merge"): (
        "skill", "guru-merge-task-pr",
    ),
    ("guru-finalize-task", "blocked"): (
        "stop", "task-finalization-blocked",
    ),
    ("guru-merge-task-pr", "merged"): (
        "workflow", "guru-finalization-finish-response",
    ),
    ("guru-merge-task-pr", "merge_blocked"): (
        "stop", "task-pr-merge-blocked",
    ),
    ("guru-merge-task-pr", "closure_mismatch"): (
        "stop", "task-pr-closure-mismatch",
    ),
}
ROUTE_GROUPS = {
    "normal": [
        ("guru-review-task-publication", "ready"),
        ("guru-finalize-task", "ready_for_merge"),
        ("guru-merge-task-pr", "merged"),
    ],
    "extension": [
        ("guru-finalize-task", "verification_required"),
        ("guru-verify-extension-installation", "verified"),
        ("guru-finalize-task", "ready_for_merge"),
        ("guru-merge-task-pr", "merged"),
    ],
    "return_to_work": [
        ("guru-review-task-publication", "return_to_task_work"),
        ("guru-verify-extension-installation", "return_to_task_work"),
    ],
    "publication_refresh": [
        ("guru-finalize-task", "publication_review_stale"),
        ("guru-review-task-publication", "ready"),
    ],
    "same_plan_or_reprepare": [
        ("guru-finalize-task", "resume_finalization"),
        ("guru-finalize-task", "reprepare_required"),
    ],
    "terminal": [
        ("guru-review-task-publication", "blocked"),
        ("guru-verify-extension-installation", "blocked"),
        ("guru-finalize-task", "blocked"),
        ("guru-merge-task-pr", "merge_blocked"),
        ("guru-merge-task-pr", "closure_mismatch"),
    ],
}
PRIVATE_FIELDS = {
    "facts_sha256", "generated_at", "reviewer", "review_history",
    "transaction_state", "recovery_history", "closeout_plan",
    "changed_paths", "command_transcript",
}
GURU_ENTRIES = (
    ".codex/prompts/guru-finish-work.md",
    ".claude/commands/guru/finish-work.md",
    ".cursor/commands/guru-finish-work.md",
)
TERMINAL_CASES = {
    "publication-ready-ready-for-merge": (
        "publication_ready",
        "evals/files/publication-ready-ready-for-merge-facts.json",
        "finalization-publication-ready-ready-for-merge",
    ),
    "same-plan-ready-for-merge": (
        "same_plan_resume",
        "evals/files/same-plan-ready-for-merge-facts.json",
        "finalization-same-plan-ready-for-merge",
    ),
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain one JSON object")
    return value


def package(skill_id: str) -> Path:
    return SKILLS_ROOT / "packages" / skill_id


def workflow_exits() -> list[dict[str, Any]]:
    text = WORKFLOW.read_text(encoding="utf-8")
    return [
        json.loads(value)
        for value in re.findall(r"<!-- guru-skill-exit: (\{.*?\}) -->", text)
    ]


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def output_object_branches(schema: dict[str, Any]) -> list[dict[str, Any]]:
    if schema.get("type") == "object":
        return [schema]
    branches = schema.get("oneOf")
    if isinstance(branches, list) and branches:
        return [branch for branch in branches if branch.get("type") == "object"]
    return []


def load_selected_runtime() -> Any:
    runtime = (
        REPO / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
        if EXECUTION_MODE == "installed"
        else REPO / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"
    )
    spec = importlib.util.spec_from_file_location(
        f"guru_finish_family_runtime_{EXECUTION_MODE}",
        runtime,
    )
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load runtime: {runtime}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_selected_native_adapter() -> Any:
    adapter = (
        REPO / ".trellis/guru-team/skills/adapters/eval/native_adapter.py"
        if EXECUTION_MODE == "installed"
        else REPO / "trellis/skills/guru-team/adapters/eval/native_adapter.py"
    )
    spec = importlib.util.spec_from_file_location(
        f"guru_finish_family_native_adapter_{EXECUTION_MODE}",
        adapter,
    )
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load native adapter: {adapter}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FinishFamilyIntegrationTests(unittest.TestCase):
    def test_issue_174_controlled_replay_is_one_chained_session(self) -> None:
        runtime = load_selected_runtime()
        adapter = load_selected_native_adapter()
        events: list[dict[str, Any]] = []
        report_path = os.environ.get("GURU_ISSUE_174_REPLAY_REPORT")
        temporary_replay: Any = None
        if report_path:
            replay_root = Path(report_path).resolve().parent / "chained-session"
            self.assertFalse(replay_root.exists())
            replay_root.mkdir(parents=True)
        else:
            temporary_replay = tempfile.TemporaryDirectory(
                prefix="guru-174-chained-replay-"
            )
            self.addCleanup(temporary_replay.cleanup)
            replay_root = Path(temporary_replay.name)

        marker_pattern = re.compile(
            r"<!-- guru-confirmation-boundary: (\{.*?\}) -->"
        )
        markers = [
            json.loads(value)
            for value in marker_pattern.findall(WORKFLOW.read_text(encoding="utf-8"))
        ]
        marker_by_id = {item["id"]: item for item in markers}
        self.assertEqual(len(marker_by_id), len(markers))
        self.assertEqual(
            set(marker_by_id),
            {
                "workspace_and_task",
                "issue_creation",
                "finalizer_side_effect_set",
                "expected_head_merge",
            },
        )

        dispatcher = REPO / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        self.assertTrue(dispatcher.is_file())
        fixture, _ = adapter.stage_clean_installed_owner_repo(
            replay_root / "owner-staging",
            dispatcher,
            package("guru-review-branch"),
        )
        canonical_trellis = EXTENSION_SOURCE_REPO / "trellis"
        self.assertTrue(canonical_trellis.is_dir())
        shutil.copytree(canonical_trellis, fixture / "trellis")
        fixture_dispatcher = (
            fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        )
        runtime = adapter.load_owner_runtime(fixture_dispatcher)

        def fixture_package(skill_id: str) -> Path:
            return fixture / ".trellis/guru-team/skills/packages" / skill_id

        interfaces = {
            skill_id: read_json(fixture_package(skill_id) / "interface.json")
            for skill_id in (
                "guru-review-branch",
                "guru-review-task-publication",
                "guru-finalize-task",
                "guru-verify-extension-installation",
                "guru-merge-task-pr",
            )
        }

        def validate_output(skill_id: str, output: dict[str, Any]) -> None:
            interface = interfaces[skill_id]
            contract = next(
                item
                for item in interface["public_contracts"]["outputs"]
                if item["exit_id"] == output["exit_id"]
            )
            schema = read_json(
                fixture_package(skill_id) / contract["schema"]["path"]
            )
            errors = runtime.skill_json_schema_validation_errors(
                output,
                schema,
                f"#174 replay {skill_id}:{output['exit_id']}",
            )
            self.assertEqual(errors, [])

        def repo_relative(path: Path) -> str:
            return path.resolve().relative_to(fixture.resolve()).as_posix()

        def invoke_wrapper(
            skill_id: str,
            input_path: Path,
            owner_flag: str,
            owner_path: Path,
            *,
            environment: dict[str, str] | None = None,
        ) -> tuple[dict[str, Any], str]:
            wrapper = fixture_package(skill_id) / "scripts/invoke.sh"
            argv = [
                str(wrapper),
                "--input",
                repo_relative(input_path),
                owner_flag,
                repo_relative(owner_path),
            ]
            process = subprocess.run(
                argv,
                cwd=fixture,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                env={
                    **os.environ,
                    "PYTHONDONTWRITEBYTECODE": "1",
                    **(environment or {}),
                },
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            public_output = json.loads(process.stdout)
            self.assertIsInstance(public_output, dict)
            validate_output(skill_id, public_output)
            receipt_id = f"wrapper-{sum(e['kind'] == 'wrapper_receipt' for e in events) + 1:02d}"
            receipt_path = (
                fixture
                / ".trellis/.runtime/guru-team/replay/receipts"
                / f"{receipt_id}-{skill_id}.json"
            )
            receipt = {
                "receipt_id": receipt_id,
                "skill": skill_id,
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "owner_locator": repo_relative(owner_path),
                "returncode": process.returncode,
                "stdout": process.stdout,
                "stderr": process.stderr,
            }
            runtime.write_json(receipt_path, receipt)
            events.append({
                "kind": "wrapper_receipt",
                "receipt_id": receipt_id,
                "skill": skill_id,
                "exit_id": public_output["exit_id"],
                "input_sha256": receipt["input_sha256"],
                "receipt_locator": repo_relative(receipt_path),
                "stdout_sha256": hashlib.sha256(
                    process.stdout.encode("utf-8")
                ).hexdigest(),
            })
            return public_output, receipt_id

        def project(
            skill_id: str,
            projection_id: str,
            output: dict[str, Any],
            source_receipt_id: str,
        ) -> tuple[dict[str, Any], Path]:
            interface = interfaces[skill_id]
            projection = next(
                item
                for item in interface["public_contracts"]["projections"]
                if item["id"] == projection_id
            )
            consumer = next(
                item
                for item in interface["public_contracts"]["consumer_inputs"]
                if item["id"] == projection["consumer_input_id"]
            )
            contract = consumer["contract"]
            self.assertEqual(contract["kind"], "skill_input_authoring_seed")
            seed = runtime.skill_apply_projection(projection, output)
            target_skill = consumer["consumer"]["id"]
            authoring = read_json(
                fixture_package(target_skill)
                / contract["authoring_example"]["path"]
            )
            self.assertFalse(set(seed) & set(authoring))
            target_input = {**seed, **authoring}
            target_interface = interfaces[target_skill]
            target_profile = next(
                item
                for item in target_interface["public_contracts"]["input"]["profiles"]
                if item["id"] == contract["profile_id"]
            )
            target_schema = read_json(
                fixture_package(target_skill) / target_profile["schema"]["path"]
            )
            errors = runtime.skill_json_schema_validation_errors(
                target_input,
                target_schema,
                f"#174 replay projection {projection_id}",
            )
            self.assertEqual(errors, [])
            target_path = (
                fixture
                / ".trellis/.runtime/guru-team/replay/inputs"
                / f"{len([e for e in events if e['kind'] == 'projection']) + 1:02d}-{target_skill}.json"
            )
            runtime.write_json(target_path, target_input)
            target_sha256 = hashlib.sha256(target_path.read_bytes()).hexdigest()
            events.append({
                "kind": "projection",
                "source_receipt_id": source_receipt_id,
                "producer": skill_id,
                "projection_id": projection_id,
                "consumer": target_skill,
                "target_input_locator": repo_relative(target_path),
                "target_input_sha256": target_sha256,
            })
            return target_input, target_path

        nested_verifier = (
            fixture
            / "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh"
        )
        nested_verifier.write_text(
            r"""#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

WORK_DIR="${1:?missing work directory}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
TARGET="$WORK_DIR/project"

mkdir -p "$TARGET/.trellis"
git -C "$TARGET" init -q -b main
git -C "$TARGET" config user.name "Nested Replay Verifier"
git -C "$TARGET" config user.email "nested-replay@example.invalid"
cp -R "$REPO_ROOT/.trellis/scripts" "$TARGET/.trellis/scripts"
cp "$REPO_ROOT/trellis/workflows/guru-team/workflow.md" "$TARGET/.trellis/workflow.md"
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$TARGET" --all-platforms --json >/dev/null
"$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" \
  --root "$TARGET" --mode installed --json >/dev/null
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh" \
  --repo "$REPO_ROOT" --json >/dev/null
if find "$REPO_ROOT" "$TARGET" -type f \( -name '*.new' -o -name '*.bak' \) -print -quit | grep -q .; then
  echo "nested replay produced sidecars" >&2
  exit 2
fi
""",
            encoding="utf-8",
        )
        nested_verifier.chmod(0o755)
        nested_apply = subprocess.run(
            [
                str(fixture / "trellis/presets/guru-team/scripts/bash/apply.sh"),
                "--repo",
                str(fixture),
                "--all-platforms",
                "--json",
            ],
            cwd=fixture,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(nested_apply.returncode, 0, nested_apply.stderr)

        manifest_path = fixture / ".trellis/guru-team/extension.json"
        manifest = read_json(manifest_path)
        manifest["source"].update(
            {
                "repo": "https://github.com/castbox/guru-trellis.git",
                "ref": "0" * 40,
                "commit": "0" * 40,
                "tree_state": "clean",
                "is_mutable_ref": False,
            }
        )
        runtime.write_json(manifest_path, manifest)
        task, _ = adapter.production_task_fixture(runtime, fixture)
        adapter.run_git(
            fixture,
            "remote",
            "set-url",
            "origin",
            "https://github.com/castbox/guru-trellis.git",
        )
        config_path = fixture / ".trellis/guru-team/config.yml"
        config_path.write_text(
            'workspace_mode: current\ngithub_repo: "castbox/guru-trellis"\n',
            encoding="utf-8",
        )
        task_payload = read_json(task / "task.json")
        task_payload["title"] = "#174 controlled finalization replay"
        runtime.write_json(task / "task.json", task_payload)
        historical_issue = {
            "number": 174,
            "url": "https://github.com/castbox/guru-trellis/issues/174",
            "title": "Controlled historical replay authority",
            "reason": "Sanitized immutable lifecycle evidence only.",
        }
        runtime.write_json(
            task / "issue-scope-ledger.json",
            {
                "schema_version": "2.0",
                "primary_issue": historical_issue,
                "close_issues": [historical_issue],
                "related_issues": [],
                "followup_issues": [],
            },
        )
        runtime.write_runtime_mappings(
            fixture,
            runtime.load_config(fixture),
            {
                "workspace_slug": "current",
                "task_slug": "current",
                "task_dir": repo_relative(task),
                "branch_name": "eval/current",
            },
            fixture,
        )
        adapter.run_git(fixture, "add", ".")
        adapter.run_git(fixture, "commit", "-q", "-m", "bind #174 replay authority")

        adapter.production_record_planning(runtime, fixture, task, "approved")
        task_payload = read_json(task / "task.json")
        task_payload["status"] = "in_progress"
        runtime.write_json(task / "task.json", task_payload)
        adapter.run_git(fixture, "add", repo_relative(task))
        adapter.run_git(fixture, "commit", "-q", "-m", "activate replay task")
        task_start = subprocess.run(
            [
                adapter.sys.executable,
                str(fixture / ".trellis/scripts/task.py"),
                "start",
                repo_relative(task),
            ],
            cwd=fixture,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(task_start.returncode, 0, task_start.stderr)
        with nested_verifier.open("a", encoding="utf-8") as handle:
            handle.write("\n# reviewed extension change for the controlled replay\n")
        (fixture / "src/production-eval.txt").write_text(
            "issue-174-controlled-replay\n", encoding="utf-8"
        )
        phase2_package = fixture_package("guru-check-task")
        checked_phase2 = adapter.production_record_phase2(
            runtime, fixture, task, phase2_package, "passed"
        )
        production_facts = adapter.write_fake_production_commit_facts(
            replay_root,
            repo_ref="castbox/guru-trellis",
            head_branch="eval/current",
        )
        adapter.with_path_prefix(
            production_facts,
            lambda: adapter.production_commit_for_review(
                runtime, fixture, task, checked_phase2
            ),
        )
        branch_input = {
            "profile": "branch_review",
            "mode": "workflow",
            "task_ref": repo_relative(task),
            "base_ref": "origin/main",
            "branch_review_commit": adapter.run_git(fixture, "rev-parse", "HEAD"),
            "review_intent": "fresh_final_review",
        }
        branch_owner = adapter.with_path_prefix(
            production_facts,
            lambda: adapter.production_record_review(
                runtime,
                fixture,
                task,
                branch_input,
                "review-fresh-final-passed",
            ),
        )
        branch_input_path = fixture / adapter.OWNER_INPUT
        branch_output, branch_receipt = invoke_wrapper(
            "guru-review-branch",
            branch_input_path,
            "--owner-result",
            Path(branch_owner["artifact_path"]),
            environment={"PATH": f"{production_facts}{os.pathsep}{os.environ.get('PATH', '')}"},
        )
        publication_input, publication_input_path = project(
            "guru-review-branch",
            "project_passed",
            branch_output,
            branch_receipt,
        )
        self.assertEqual(
            publication_input["branch_review_commit"],
            branch_output["branch_review_commit"],
        )

        publication_authoring_path = adapter.production_publication_authoring(
            runtime,
            fixture,
            task,
            publication_input,
            "publication-ready",
        )
        publication_authoring = read_json(publication_authoring_path)
        publication_authoring["pr_payload"]["title"] = "完成：#174 受控回放"
        publication_authoring["pr_payload"]["body"] = publication_authoring[
            "pr_payload"
        ]["body"].replace("#146", "#174")
        runtime.write_json(publication_authoring_path, publication_authoring)
        publication_owner = adapter.with_path_prefix(
            production_facts,
            lambda: runtime.cmd_record_task_publication_review(argparse.Namespace(
                root=str(fixture),
                task=repo_relative(task),
                input=repo_relative(publication_authoring_path),
                branch_review_commit=publication_input["branch_review_commit"],
                dry_run=False,
            )),
        )
        publication_output, publication_receipt = invoke_wrapper(
            "guru-review-task-publication",
            publication_input_path,
            "--owner-result",
            Path(publication_owner["artifact_path"]),
            environment={"PATH": f"{production_facts}{os.pathsep}{os.environ.get('PATH', '')}"},
        )
        finalizer_input, finalizer_input_path = project(
            "guru-review-task-publication",
            "project_ready",
            publication_output,
            publication_receipt,
        )
        self.assertEqual(finalizer_input["pr_body"], publication_output["pr_body"])

        remote_repo = replay_root / "target.git"
        subprocess.run(
            ["git", "init", "-q", "--bare", str(remote_repo)],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "push",
                "-q",
                str(remote_repo),
                "eval/current:refs/heads/eval/current",
            ],
            cwd=fixture,
            check=True,
        )
        finalizer_bin = replay_root / "finalizer-bin"
        finalizer_bin.mkdir()
        real_git = shutil.which("git")
        self.assertIsNotNone(real_git)
        fake_git = finalizer_bin / "git"
        fake_git.write_text(
            "#!/usr/bin/env python3\n"
            "import os,sys\n"
            f"real_git={real_git!r}\n"
            f"remote_repo={str(remote_repo)!r}\n"
            "args=sys.argv[1:]\n"
            "canonical='https://github.com/castbox/guru-trellis.git'\n"
            "if args and args[0]=='push' and 'origin' in args:\n"
            " args=[remote_repo if value=='origin' else value for value in args]\n"
            " args=[value for value in args if value!='-u']\n"
            "elif args and args[0]=='ls-remote':\n"
            " args=[remote_repo if value in {'origin',canonical} else value for value in args]\n"
            "elif args and args[0]=='clone':\n"
            " args=[remote_repo if value==canonical else value for value in args]\n"
            "elif args and args[0]=='fetch' and 'origin' in args:\n"
            " args=[remote_repo if value=='origin' else value for value in args]\n"
            "os.execv(real_git,[real_git,*args])\n",
            encoding="utf-8",
        )
        fake_git.chmod(0o755)
        finalizer_state = finalizer_bin / "state.json"
        runtime.write_json(
            finalizer_state,
            {"created": False, "draft": True, "title": "", "body": "", "calls": []},
        )
        fake_gh = finalizer_bin / "gh"
        fake_gh.write_text(
            "#!/usr/bin/env python3\n"
            "import json,subprocess,sys\n"
            f"state_path={str(finalizer_state)!r}\n"
            f"real_git={real_git!r}\n"
            "repo='castbox/guru-trellis'; number=176\n"
            "args=sys.argv[1:]\n"
            "state=json.load(open(state_path,encoding='utf-8'))\n"
            "state['calls'].append(args)\n"
            "def save(): open(state_path,'w',encoding='utf-8').write(json.dumps(state)+'\\n')\n"
            "def head(): return subprocess.check_output([real_git,'rev-parse','HEAD'],text=True).strip()\n"
            "def pr():\n"
            " return {'number':number,'url':f'https://github.com/{repo}/pull/{number}',"
            "'title':state['title'],'body':state['body'],'headRefName':'eval/current',"
            "'baseRefName':'main','headRefOid':head(),'isDraft':state['draft'],"
            "'state':'OPEN','headRepository':{'nameWithOwner':repo},"
            "'headRepositoryOwner':{'login':'castbox'},'isCrossRepository':False}\n"
            "if args[:2]==['auth','status']:\n"
            " save(); raise SystemExit(0)\n"
            "if args[:2]==['pr','list']:\n"
            " save(); print(json.dumps([pr()] if state['created'] else [])); raise SystemExit(0)\n"
            "if args[:2]==['pr','create']:\n"
            " state['created']=True; state['draft']='--draft' in args\n"
            " state['title']=args[args.index('--title')+1]\n"
            " state['body']=open(args[args.index('--body-file')+1],encoding='utf-8').read()\n"
            " save(); print(f'https://github.com/{repo}/pull/{number}'); raise SystemExit(0)\n"
            "if args[:2]==['pr','edit']:\n"
            " state['title']=args[args.index('--title')+1]\n"
            " state['body']=open(args[args.index('--body-file')+1],encoding='utf-8').read()\n"
            " save(); raise SystemExit(0)\n"
            "if args[:2]==['pr','ready']:\n"
            " state['draft']=False; save(); raise SystemExit(0)\n"
            "if args[:2]==['pr','view']:\n"
            " save(); print(json.dumps(pr())); raise SystemExit(0)\n"
            "if len(args)>=3 and args[:2]==['issue','view']:\n"
            " issue=int(args[2]); save(); print(json.dumps({'number':issue,'state':'OPEN',"
            "'url':f'https://github.com/{repo}/issues/{issue}'})); raise SystemExit(0)\n"
            "save(); print('unsupported finalizer gh invocation: '+repr(args),file=sys.stderr); raise SystemExit(2)\n",
            encoding="utf-8",
        )
        fake_gh.chmod(0o755)

        def with_finalizer_transport(callback: Any) -> Any:
            return adapter.with_path_prefix(finalizer_bin, callback)

        def finalization_args(
            input_path: Path,
            *,
            review_input: Path | None = None,
            gate: Path | None = None,
        ) -> argparse.Namespace:
            return argparse.Namespace(
                root=str(fixture),
                input=repo_relative(input_path),
                repo="castbox/guru-trellis",
                base_branch="main",
                remote="origin",
                title=None,
                task_name=None,
                validation=None,
                review_input=(
                    repo_relative(review_input) if review_input is not None else None
                ),
                dry_run=False,
                gate=repo_relative(gate) if gate is not None else None,
                json=True,
            )

        def run_finalization_round(
            public_input: dict[str, Any],
            input_path: Path,
            *,
            exit_id: str,
            output: dict[str, Any],
        ) -> tuple[dict[str, Any], Path]:
            review_path = (
                fixture
                / ".trellis/.runtime/guru-team/replay"
                / f"finalizer-{exit_id}-review.json"
            )
            runtime.write_json(
                review_path,
                {
                    "schema_version": "2.0",
                    "skill_id": "guru-finalize-task",
                    "review": {
                        "status": "reroute" if exit_id == "reprepare_required" else "passed",
                        "summary": f"The replay reviewed the live {exit_id} transition.",
                    },
                    "route": {
                        "typed_exit": exit_id,
                        "consumer": runtime.FINALIZATION_CONSUMERS[exit_id],
                        "output": output,
                    },
                },
            )
            args = finalization_args(input_path, review_input=review_path)
            with_finalizer_transport(lambda: runtime.cmd_preview_finalization(args))
            recorded = with_finalizer_transport(
                lambda: runtime.cmd_record_finalization_gate(args)
            )
            gate_path = Path(recorded["artifact_path"])
            checked_args = finalization_args(input_path, gate=gate_path)
            checked = with_finalizer_transport(
                lambda: runtime.cmd_check_finalization_gate(checked_args)
            )
            self.assertEqual(checked["typed_exit"], exit_id)
            transitioned = with_finalizer_transport(
                lambda: runtime.cmd_execute_finalization_transition(checked_args)
            )
            self.assertEqual(transitioned["typed_exit"], exit_id)
            return transitioned, gate_path

        for boundary, source in (
            ("workspace_and_task", "sanitized_open_issue_lifecycle_receipt"),
            ("issue_creation", "sanitized_new_issue_lifecycle_receipt"),
            ("finalizer_side_effect_set", "current_chained_finalizer_plan"),
        ):
            events.append({
                "kind": "confirmation",
                "boundary": marker_by_id[boundary]["id"],
                "source": source,
            })

        provenance = with_finalizer_transport(
            lambda: runtime.prepare_provenance_metadata_tail(
                fixture,
                finalizer_input["branch_review_commit"],
            )
        )
        self.assertEqual(
            provenance["reviewed_content_head"],
            finalizer_input["branch_review_commit"],
        )
        finalizer_preview = with_finalizer_transport(
            lambda: runtime.cmd_preview_finalization(
                finalization_args(finalizer_input_path)
            )
        )
        self.assertIn(
            finalizer_preview["transaction_state"],
            {"prepared", "content_pushed"},
            finalizer_preview,
        )
        self.assertTrue(finalizer_preview["verification_required"], finalizer_preview)
        verification_route = {
            "exit_id": "verification_required",
            "task_ref": finalizer_input["task_ref"],
            "plan_ref": finalizer_preview["plan_ref"],
            "repo_ref": "castbox/guru-trellis",
            "branch_review_commit": finalizer_preview["branch_review_commit"],
            "publication_head": provenance["publication_head"],
            "verification_target": "extension-installation",
        }
        _, verification_gate = run_finalization_round(
            finalizer_input,
            finalizer_input_path,
            exit_id="verification_required",
            output=verification_route,
        )
        verification_required, finalizer_required_receipt = invoke_wrapper(
            "guru-finalize-task",
            finalizer_input_path,
            "--owner-result",
            verification_gate,
            environment={
                "PATH": f"{finalizer_bin}{os.pathsep}{os.environ.get('PATH', '')}"
            },
        )
        verification_input, verification_input_path = project(
            "guru-finalize-task",
            "project_verification_required",
            verification_required,
            finalizer_required_receipt,
        )

        capabilities = list(runtime.EXTENSION_VERIFICATION_CAPABILITIES)
        verifier_execution_path = (
            fixture / ".trellis/.runtime/guru-team/evals/replay-verifier-execution.json"
        )
        verifier_review_path = (
            fixture / ".trellis/.runtime/guru-team/evals/replay-verifier-review.json"
        )
        runtime.write_json(
            verifier_execution_path,
            with_finalizer_transport(
                lambda: runtime.cmd_execute_extension_verification(
                    argparse.Namespace(
                        root=str(fixture),
                        input=repo_relative(verification_input_path),
                        capability=capabilities,
                    )
                )
            ),
        )
        runtime.write_json(
            verifier_review_path,
            adapter.extension_verification_review("verified", capabilities),
        )
        verifier_owner = runtime.cmd_record_extension_verification(argparse.Namespace(
            root=str(fixture),
            input=repo_relative(verification_input_path),
            execution_input=repo_relative(verifier_execution_path),
            review_input=repo_relative(verifier_review_path),
        ))
        verifier_owner_path = task / "marketplace-verification.json"
        checked_verifier = with_finalizer_transport(
            lambda: runtime.cmd_check_extension_verification(
                argparse.Namespace(
                    root=str(fixture),
                    input=repo_relative(verifier_owner_path),
                    public_input=repo_relative(verification_input_path),
                )
            )
        )
        self.assertEqual(checked_verifier["typed_exit"], "verified")
        verified_output, verifier_receipt = invoke_wrapper(
            "guru-verify-extension-installation",
            verification_input_path,
            "--owner-result",
            verifier_owner_path,
            environment={
                "PATH": f"{finalizer_bin}{os.pathsep}{os.environ.get('PATH', '')}"
            },
        )
        verified_finalizer_input, verified_finalizer_input_path = project(
            "guru-verify-extension-installation",
            "project_verified",
            verified_output,
            verifier_receipt,
        )
        self.assertEqual(
            verified_finalizer_input["verification_ref"],
            verified_output["verification_ref"],
        )

        ready_result, ready_gate = run_finalization_round(
            verified_finalizer_input,
            verified_finalizer_input_path,
            exit_id="ready_for_merge",
            output=runtime.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
        )
        self.assertEqual(ready_result["stage"], "ready")
        ready_for_merge, ready_receipt = invoke_wrapper(
            "guru-finalize-task",
            verified_finalizer_input_path,
            "--owner-result",
            ready_gate,
            environment={
                "PATH": f"{finalizer_bin}{os.pathsep}{os.environ.get('PATH', '')}"
            },
        )
        merge_input, merge_input_path = project(
            "guru-finalize-task",
            "project_ready_for_merge",
            ready_for_merge,
            ready_receipt,
        )
        self.assertEqual(merge_input["expected_close_issues"], [174])

        merge_binary = adapter.write_fake_merge_gh(
            replay_root,
            "merge-workflow-merged",
            repo_ref=merge_input["repo_ref"],
            pr_number=merge_input["pr_number"],
            issue_number=174,
            head_sha=merge_input["expected_head_sha"],
            base_branch=merge_input["expected_base_branch"],
            head_branch=merge_input["expected_head_branch"],
        )
        merge_environment = {
            "PATH": f"{merge_binary}{os.pathsep}{os.environ.get('PATH', '')}"
        }
        merge_review_path = (
            fixture / ".trellis/.runtime/guru-team/evals/replay-merge-review.json"
        )
        runtime.write_json(
            merge_review_path,
            {
                "semantic_review": {
                    "dimensions": [
                        {
                            "id": identifier,
                            "status": "passed",
                            "summary": f"The chained replay passes {identifier}.",
                        }
                        for identifier in runtime.TASK_PR_MERGE_DIMENSIONS
                    ]
                },
                "route": {"typed_exit": "merged", "merge_method": "merge"},
            },
        )
        previous_path = os.environ.get("PATH")
        os.environ["PATH"] = merge_environment["PATH"]
        try:
            merge_record = runtime.cmd_record_task_pr_merge(argparse.Namespace(
                root=str(fixture),
                input=repo_relative(merge_input_path),
                review_input=str(merge_review_path),
            ))
            merge_gate = fixture / merge_record["gate"]
            events.append({
                "kind": "confirmation",
                "boundary": marker_by_id["expected_head_merge"]["id"],
                "source": "current_expected_head_merge_plan",
            })
            merge_execution = runtime.cmd_execute_task_pr_merge(argparse.Namespace(
                root=str(fixture),
                input=repo_relative(merge_input_path),
                gate=repo_relative(merge_gate),
            ))
        finally:
            if previous_path is None:
                os.environ.pop("PATH", None)
            else:
                os.environ["PATH"] = previous_path
        self.assertEqual(merge_execution["typed_exit"], "merged")
        merged_output, _ = invoke_wrapper(
            "guru-merge-task-pr",
            merge_input_path,
            "--gate",
            merge_gate,
            environment=merge_environment,
        )
        self.assertEqual(merged_output["exit_id"], "merged")

        merge_state = read_json(merge_binary / "state.json")
        calls = merge_state["calls"]
        merge_call_index = next(
            index
            for index, argv in enumerate(calls)
            if argv[:2] == ["pr", "merge"]
        )
        pre_issue_reads = [
            index
            for index, argv in enumerate(calls[:merge_call_index])
            if argv[:2] == ["issue", "view"]
        ]
        post_issue_reads = [
            index
            for index, argv in enumerate(calls[merge_call_index + 1 :], merge_call_index + 1)
            if argv[:2] == ["issue", "view"]
        ]
        self.assertTrue(pre_issue_reads)
        self.assertTrue(post_issue_reads)
        self.assertTrue(merge_state["merged"])
        self.assertFalse(
            any(argv[:2] == ["issue", "close"] for argv in calls)
        )
        events.append({
            "kind": "github_state_transition",
            "pre_merge_issue_reads": len(pre_issue_reads),
            "expected_head_merge_call": calls[merge_call_index],
            "post_merge_issue_reads": len(post_issue_reads),
            "merged": merge_state["merged"],
            "calls_sha256": hashlib.sha256(
                json.dumps(calls, separators=(",", ":")).encode("utf-8")
            ).hexdigest(),
        })

        terminal_names = {
            "finalization-transaction.json",
            "task-finalization-gate.json",
            "task-finalization-transition.json",
            "closeout-plan.json",
        }
        terminal_artifacts = [
            path.relative_to(fixture).as_posix()
            for path in fixture.rglob("*")
            if path.is_file()
            and path.name in terminal_names
            and ".trellis" in path.parts
            and (".runtime" in path.parts or "tasks" in path.parts)
        ]

        confirmation_profiles = {
            profile: [
                marker["id"]
                for marker in markers
                if profile in marker["profiles"]
            ]
            for profile in ("open_issue", "new_issue")
        }
        confirmation_counts = {
            profile: sum(
                event["kind"] == "confirmation"
                and profile in marker_by_id[event["boundary"]]["profiles"]
                for event in events
            )
            for profile in confirmation_profiles
        }
        counters = {
            "open_issue_confirmations": confirmation_counts["open_issue"],
            "new_issue_confirmations": confirmation_counts["new_issue"],
            "commit_confirmations": sum(
                event.get("boundary") == "task_commit"
                for event in events
                if event["kind"] == "confirmation"
            ),
            "branch_review_executions": sum(
                event.get("skill") == "guru-review-branch"
                for event in events
                if event["kind"] == "wrapper_receipt"
            ),
            "immutable_verification_executions": sum(
                event.get("skill") == "guru-verify-extension-installation"
                for event in events
                if event["kind"] == "wrapper_receipt"
            ),
            "finalizer_confirmations": sum(
                event.get("boundary") == "finalizer_side_effect_set"
                for event in events
                if event["kind"] == "confirmation"
            ),
            "merge_confirmations": sum(
                event.get("boundary") == "expected_head_merge"
                for event in events
                if event["kind"] == "confirmation"
            ),
            "terminal_transaction_artifacts": len(terminal_artifacts),
        }
        self.assertEqual(
            counters,
            {
                "open_issue_confirmations": 3,
                "new_issue_confirmations": 4,
                "commit_confirmations": 0,
                "branch_review_executions": 1,
                "immutable_verification_executions": 1,
                "finalizer_confirmations": 1,
                "merge_confirmations": 1,
                "terminal_transaction_artifacts": 0,
            },
        )
        report = {
            "status": "passed",
            "authority": {
                "historical_issue": 174,
                "historical_pr": 176,
                "mode": "sanitized_fixture",
                "start": "last_reviewed_content_commit",
                "external_mutation": False,
            },
            "confirmation_boundaries": confirmation_profiles,
            "events": events,
            "counters": counters,
            "terminal_artifacts": terminal_artifacts,
        }
        event_log_path = replay_root / "event-log.json"
        event_log_path.write_text(
            json.dumps(events, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        report["event_log"] = str(event_log_path)
        if report_path:
            Path(report_path).write_text(
                json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )

    def test_branch_review_passed_dto_reaches_side_effect_free_finalizer_preview(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        branch_package = package("guru-review-branch")
        publication_package = package("guru-review-task-publication")
        gate = read_json(branch_package / "examples/review-gate.json")
        self.assertEqual(gate["schema_version"], "3.0")
        self.assertEqual(gate["typed_exit"], "passed")

        branch_output = {
            "exit_id": "passed",
            "task_ref": gate["task_dir"],
            "branch_review_commit": gate["review_commit"],
        }
        branch_interface = read_json(branch_package / "interface.json")
        branch_projection = next(
            item
            for item in branch_interface["public_contracts"]["projections"]
            if item["id"] == "project_passed"
        )
        publication_seed = runtime.skill_apply_projection(
            branch_projection,
            branch_output,
        )
        self.assertEqual(
            publication_seed,
            {
                "task_ref": gate["task_dir"],
                "branch_review_commit": gate["review_commit"],
            },
        )

        publication_output = {
            "exit_id": "ready",
            **publication_seed,
            "pr_title": "完成：Finalizer 直接消费 Publication payload",
            "pr_body": "## 变更摘要\n\n- Publication 直接输出 PR payload。",
        }
        publication_interface = read_json(publication_package / "interface.json")
        publication_projection = next(
            item
            for item in publication_interface["public_contracts"]["projections"]
            if item["id"] == "project_ready"
        )
        finalization_seed = runtime.skill_apply_projection(
            publication_projection,
            publication_output,
        )
        finalization_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            **finalization_seed,
        }
        self.assertFalse(PRIVATE_FIELDS & set(publication_output))
        self.assertFalse(PRIVATE_FIELDS & set(finalization_input))

        with tempfile.TemporaryDirectory(prefix="guru-direct-finalizer-") as temporary:
            root = Path(temporary)
            task_dir = root / gate["task_dir"]
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_text(
                json.dumps({"status": "in_progress"}),
                encoding="utf-8",
            )
            task_context = {"task_artifact_dir": gate["task_dir"]}
            plan = {
                "plan_digest": "c" * 64,
                "task": {
                    "active_locator": gate["task_dir"],
                    "archive_locator": (
                        ".trellis/tasks/archive/2026-08/example-task"
                    ),
                },
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "base_branch": "main",
                    "head_branch": "codex/example-task",
                    "branch_review_commit": gate["review_commit"],
                },
                "marketplace": {"required": False},
            }
            prepared = {
                "plan": plan,
                "ledger": {},
                "gate": None,
                "month_supersession": None,
            }
            repository = {
                "head": gate["review_commit"],
                "branch": "codex/example-task",
                "base_ref": "origin/main",
                "diff_paths": ["src/example.py"],
                "status_paths": [],
            }
            before = tree_bytes(root)

            def prepare(
                _root: Path,
                _args: argparse.Namespace,
                _config: dict[str, Any],
                _task_dir: Path,
                _task_context: dict[str, Any],
                *,
                publication_ready: dict[str, Any] | None = None,
                verification_owner_result: Any = None,
                allowed_current_gate: dict[str, Any] | None = None,
                current_finalizer: bool = False,
            ) -> dict[str, Any]:
                self.assertEqual(publication_ready, finalization_input)
                self.assertIsNone(verification_owner_result)
                self.assertIsNone(allowed_current_gate)
                self.assertTrue(current_finalizer)
                return prepared

            args = argparse.Namespace(
                root=str(root),
                input="inline-publication-ready.json",
                include_finalization_gate=True,
            )
            with (
                mock.patch.dict(os.environ, {"GURU_TEAM_EVAL_STAGING": "0"}),
                mock.patch.object(runtime, "repo_root", return_value=root),
                mock.patch.object(
                    runtime,
                    "finalization_public_input",
                    return_value=(finalization_input, args.input),
                ),
                mock.patch.object(runtime, "load_config", return_value={}),
                mock.patch.object(
                    runtime,
                    "load_task_runtime_identity",
                    return_value=task_context,
                ),
                mock.patch.object(runtime, "assert_workspace_boundary"),
                mock.patch.object(
                    runtime,
                    "finalization_verification_owner_result",
                    return_value=None,
                ),
                mock.patch.object(
                    runtime,
                    "task_publication_repository_binding",
                    return_value=repository,
                ),
                mock.patch.object(
                    runtime,
                    "task_publication_unexpected_status_paths",
                    return_value=[],
                ),
                mock.patch.object(
                    runtime,
                    "current_head",
                    return_value=gate["review_commit"],
                ),
                mock.patch.object(
                    runtime,
                    "review_branch_content_continuity_errors",
                    return_value=[],
                ),
                mock.patch.object(
                    runtime,
                    "reviewed_content_identity",
                    return_value={"sha256": gate["reviewed_content_sha256"]},
                ),
                mock.patch.object(runtime, "prepare_closeout", side_effect=prepare),
                mock.patch.object(
                    runtime,
                    "resolve_closeout_pre_draft_state",
                    return_value="prepared",
                ),
                mock.patch.object(
                    runtime,
                    "task_publication_path",
                    side_effect=AssertionError(
                        "Finalizer reopened Publication private evidence"
                    ),
                ) as private_artifact,
                mock.patch.object(
                    runtime,
                    "cmd_check_task_publication_review",
                    side_effect=AssertionError(
                        "Finalizer reran the Publication owner checker"
                    ),
                ) as owner_checker,
            ):
                preview = runtime.cmd_preview_finalization(args)

            self.assertFalse(preview["side_effects"])
            self.assertEqual(preview["transaction_state"], "prepared")
            self.assertEqual(preview["task_ref"], gate["task_dir"])
            self.assertEqual(
                preview["branch_review_commit"],
                gate["review_commit"],
            )
            self.assertEqual(tree_bytes(root), before)
            private_artifact.assert_not_called()
            owner_checker.assert_not_called()

    def test_verification_verified_reentry_keeps_scope_ledger_unchanged(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        task_ref = ".trellis/tasks/example-finalizer-reentry"
        ledger_locator = f"{task_ref}/issue-scope-ledger.json"
        branch_review_commit = "a" * 40
        issue = {
            "number": 177,
            "url": "https://github.com/castbox/guru-trellis/issues/177",
            "title": "Content identity boundary",
            "reason": "Primary delivered scope.",
        }
        ledger = {
            "schema_version": "2.0",
            "primary_issue": issue,
            "close_issues": [issue],
            "related_issues": [],
            "followup_issues": [],
        }

        with tempfile.TemporaryDirectory(prefix="guru-finalizer-reentry-") as temporary:
            root = Path(temporary)
            task_dir = root / task_ref
            task_dir.mkdir(parents=True)
            (task_dir / "issue-scope-ledger.json").write_text(
                json.dumps(ledger),
                encoding="utf-8",
            )
            ledger_before = (task_dir / "issue-scope-ledger.json").read_bytes()
            plan = {
                "schema_version": runtime.CLOSEOUT_PLAN_SCHEMA_VERSION,
                "plan_digest": "d" * 64,
                "task": {
                    "active_locator": task_ref,
                    "archive_locator": (
                        ".trellis/tasks/archive/2026-08/"
                        "example-finalizer-reentry"
                    ),
                },
                "git": {"branch_review_commit": branch_review_commit},
                "review": {"changed_paths": []},
                "publish": {"title": "title", "body": "body"},
                "marketplace": {"required": True},
                "inputs": {
                    "issue_scope_ledger": {
                        "path": ledger_locator,
                        "sha256": hashlib.sha256(ledger_before).hexdigest(),
                    },
                },
            }
            (task_dir / runtime.CLOSEOUT_PLAN_ARTIFACT).write_text(
                json.dumps(plan),
                encoding="utf-8",
            )
            with mock.patch.object(
                runtime,
                "git_status_paths",
                return_value=[ledger_locator],
            ):
                self.assertEqual(
                    runtime.finalizer_unreviewed_dirty_paths(root, task_dir),
                    [],
                )
            owner_result = {
                "profile": "verification_required",
                "typed_exit": "verified",
            }
            checked_result = {"status": "ok", "typed_exit": "verified"}
            args = argparse.Namespace(
                repo=None,
                remote=None,
            )
            with ExitStack() as stack:
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "official_after_archive_hook_state",
                        return_value={},
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_closeout_plan",
                        side_effect=lambda value: value,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_closeout_plan_for_migration",
                        side_effect=lambda value: value,
                    )
                )
                private_review_gate = stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_review_gate",
                        side_effect=AssertionError(
                            "Finalizer reopened Branch Review private evidence"
                        ),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_closeout_reviewed_content",
                        return_value="c" * 64,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "current_head",
                        return_value=branch_review_commit,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "closeout_reviewed_change_facts",
                        return_value={
                            "changed_paths": [],
                            "candidate_surfaces": ["workflow"],
                            "marketplace_required": True,
                        },
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "git_status_paths",
                        return_value=[ledger_locator],
                    )
                )
                dirty_paths = stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "finalizer_unreviewed_dirty_paths",
                        wraps=runtime.finalizer_unreviewed_dirty_paths,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "load_issue_scope_ledger",
                        return_value=ledger,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_ledger_for_publish",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_pr_body_quality",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "task_json",
                        return_value={"status": "in_progress"},
                    )
                )
                stack.enter_context(
                    mock.patch.object(runtime, "validate_closeout_task_children")
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "infer_github_repo",
                        return_value="castbox/guru-trellis",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "normalize_github_repository",
                        return_value="castbox/guru-trellis",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "base_branch_from_sources",
                        return_value="main",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "current_branch",
                        return_value="codex/example",
                    )
                )
                stack.enter_context(
                    mock.patch.object(runtime, "validate_github_remote_repository")
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "pr_title_from_task",
                        return_value="title",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "build_closeout_plan",
                        return_value=plan,
                    )
                )
                prepared = runtime.prepare_closeout(
                    root,
                    args,
                    {},
                    task_dir,
                    {},
                    verification_owner_result=(owner_result, checked_result),
                )

            self.assertEqual(prepared["plan"], plan)
            private_review_gate.assert_not_called()
            dirty_paths.assert_called_once_with(root, task_dir)
            self.assertEqual(
                (task_dir / "issue-scope-ledger.json").read_bytes(),
                ledger_before,
            )
            with mock.patch.object(
                runtime,
                "git_status_paths",
                return_value=[ledger_locator, "unrelated.txt"],
            ):
                self.assertEqual(
                    runtime.finalizer_unreviewed_dirty_paths(root, task_dir),
                    ["unrelated.txt"],
                )

    def test_stale_finalizer_projection_returns_content_drift_to_phase_2(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        finalizer_package = package("guru-finalize-task")
        publication_package = package("guru-review-task-publication")
        finalizer_interface = read_json(finalizer_package / "interface.json")
        publication_interface = read_json(publication_package / "interface.json")

        stale_output = read_json(
            finalizer_package
            / "examples/public-publication-review-stale-output.json"
        )
        stale_projection = next(
            item
            for item in finalizer_interface["public_contracts"]["projections"]
            if item["id"] == "project_publication_review_stale"
        )
        stale_seed = runtime.skill_apply_projection(
            stale_projection,
            stale_output,
        )
        stale_authoring = read_json(
            finalizer_package
            / "examples/public-publication-review-stale-authoring.json"
        )
        stale_input = {**stale_seed, **stale_authoring}
        stale_profile = next(
            item
            for item in publication_interface["public_contracts"]["input"][
                "profiles"
            ]
            if item["id"] == "publication_review_stale"
        )
        stale_input_schema = read_json(
            publication_package / stale_profile["schema"]["path"]
        )
        self.assertEqual(
            runtime.skill_json_schema_validation_errors(
                stale_input,
                stale_input_schema,
                "Finalizer stale projection",
            ),
            [],
        )
        self.assertEqual(
            stale_input["branch_review_commit"],
            stale_output["branch_review_commit"],
        )

        owner = read_json(publication_package / "examples/pr-readiness.json")
        owner["task_ref"] = stale_input["task_ref"]
        owner["branch_review_commit"] = stale_input["branch_review_commit"]
        owner["dimensions"][0]["status"] = "finding"
        owner["findings"] = [{
            "finding_ref": "PUB-STALE-CONTENT-001",
            "dimension": "diff_outcome_consistency",
            "summary": "Current reviewed-content identity differs from the Branch Review anchor.",
            "scope_basis": "The task implementation changed after Branch Review.",
            "evidence_refs": ["git:branch_review_commit", "git:HEAD"],
            "affected_artifacts": ["trellis/workflows/guru-team/workflow.md"],
            "route_class": "task_work",
            "status": "open",
            "closure_evidence": [],
        }]
        owner["conclusions"]["issue_scope"]["status"] = "finding"
        owner["route"] = {"typed_exit": "return_to_task_work"}
        self.assertEqual(
            runtime.task_publication_semantic_errors(
                owner,
                branch_review_commit=stale_input["branch_review_commit"],
            ),
            [],
        )

        with tempfile.TemporaryDirectory(prefix="guru-stale-publication-") as temporary:
            root = Path(temporary)
            task_dir = root / stale_input["task_ref"]
            task_dir.mkdir(parents=True)
            continuity_error = (
                runtime.BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX
                + "trellis/workflows/guru-team/workflow.md"
            )
            with (
                mock.patch.object(
                    runtime,
                    "task_publication_schema",
                    return_value=read_json(
                        publication_package / "schemas/pr-readiness.schema.json"
                    ),
                ),
                mock.patch.object(runtime, "load_config", return_value={}),
                mock.patch.object(runtime, "current_head", return_value="d" * 40),
                mock.patch.object(
                    runtime,
                    "review_branch_content_continuity_errors",
                    return_value=[continuity_error],
                ),
                mock.patch.object(
                    runtime,
                    "task_publication_entry_precondition_bindings",
                    return_value=({}, [continuity_error], {}, {}),
                ),
            ):
                self.assertEqual(
                    runtime.task_publication_check_errors(root, task_dir, owner),
                    [],
                )

        return_schema = read_json(
            publication_package
            / "schemas/public-return-to-task-work-output.schema.json"
        )
        returned = runtime.stage0_build_output(
            "guru-review-task-publication",
            "return_to_task_work",
            stale_input,
            owner,
            None,
            None,
            return_schema,
        )
        self.assertEqual(
            returned,
            {
                "exit_id": "return_to_task_work",
                "task_ref": stale_input["task_ref"],
                "finding_refs": ["PUB-STALE-CONTENT-001"],
                "resume_target": "phase-2",
            },
        )

    def test_selected_runtime_converges_pr_head_and_bounds_persistent_mismatch(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        local_head = "a" * 40
        stale_head = "b" * 40
        body = "Issue #119 finalizer recovery\n"
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/119-finish-family-integration-main",
                "base_branch": "main",
            },
            "publish": {
                "title": "#119 完成 Finish family combined integration",
                "body": body,
            },
        }
        draft = {
            "number": 166,
            "url": "https://github.com/castbox/guru-trellis/pull/166",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": plan["git"]["head_branch"],
            "baseRefName": "main",
            "headRefOid": stale_head,
            "isDraft": True,
            "headRepository": {"nameWithOwner": "castbox/guru-trellis"},
            "headRepositoryOwner": {"login": "castbox"},
            "isCrossRepository": False,
        }
        converged = dict(draft, headRefOid=local_head)
        ready = dict(converged, isDraft=False)
        with tempfile.TemporaryDirectory(prefix="guru-finish-head-") as temporary:
            root = Path(temporary)
            with (
                mock.patch.object(
                    runtime,
                    "resolve_closeout_pull_request",
                    side_effect=[draft, converged, ready],
                ) as resolve,
                mock.patch.object(runtime, "current_head", return_value=local_head),
                mock.patch.object(
                    runtime,
                    "closeout_remote_branch_head",
                    return_value=local_head,
                ),
                mock.patch.object(
                    runtime,
                    "run",
                    return_value=mock.Mock(returncode=0, stdout="", stderr=""),
                ) as command,
                mock.patch.object(runtime.time, "sleep") as sleeper,
            ):
                result = runtime.ensure_closeout_pr_ready(
                    root,
                    plan,
                    bound_pr=draft,
                )
            self.assertEqual(result["status"], "ready")
            self.assertEqual(result["pr"]["number"], 166)
            self.assertEqual(resolve.call_count, 3)
            sleeper.assert_called_once_with(
                runtime.CLOSEOUT_PR_HEAD_READ_DELAY_SECONDS,
            )
            ready_calls = [
                call for call in command.call_args_list
                if call.args[0][:3] == ["gh", "pr", "ready"]
            ]
            self.assertEqual(len(ready_calls), 1)

            with (
                mock.patch.object(
                    runtime,
                    "resolve_closeout_pull_request",
                    return_value=draft,
                ) as resolve,
                mock.patch.object(runtime, "current_head", return_value=local_head),
                mock.patch.object(
                    runtime,
                    "closeout_remote_branch_head",
                    return_value=local_head,
                ),
                mock.patch.object(runtime, "run") as command,
                mock.patch.object(runtime.time, "sleep") as sleeper,
                self.assertRaises(runtime.WorkflowError),
            ):
                runtime.ensure_closeout_pr_ready(root, plan, bound_pr=draft)
            self.assertEqual(
                resolve.call_count,
                runtime.CLOSEOUT_PR_HEAD_READ_ATTEMPTS,
            )
            self.assertEqual(
                sleeper.call_count,
                runtime.CLOSEOUT_PR_HEAD_READ_ATTEMPTS - 1,
            )
            command.assert_not_called()

    def test_selected_runtime_recovers_compact_archive_before_readiness_check(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        plan_digest = "a" * 64
        branch_review_commit = "b" * 40
        active = ".trellis/tasks/07-31-119-combined-finish-family-integration"
        archive = (
            ".trellis/tasks/archive/2026-08/"
            "07-31-119-combined-finish-family-integration"
        )
        plan = {
            "plan_digest": plan_digest,
            "task": {"active_locator": active, "archive_locator": archive},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/119-finish-family-integration-main",
                "base_branch": "main",
                "branch_review_commit": branch_review_commit,
            },
            "marketplace": {"required": True},
        }
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": active,
            "plan_ref": f"closeout-plan:{plan_digest}",
        }
        publication = {
            "owner_status": "current",
            "publication_ref": f"publication:{'c' * 64}",
        }
        verification = (
            {"source": "committed-finalization-gate"},
            {
                "status": "ok",
                "typed_exit": "verified",
                "verification_ref": "extension-verification:checked",
            },
        )
        transaction = {
            "commit": "d" * 40,
            "parent": "e" * 40,
            "summary_pr": {
                "number": 166,
                "url": "https://github.com/castbox/guru-trellis/pull/166",
            },
        }
        with tempfile.TemporaryDirectory(prefix="guru-finish-archive-") as temporary:
            root = Path(temporary)
            archived = root / archive
            archived.mkdir(parents=True)
            retained = set(runtime.CLOSEOUT_ARCHIVE_CORE_ARTIFACTS)
            retained.update(runtime.CLOSEOUT_ARCHIVE_OPTIONAL_ARTIFACTS)
            for relative in retained:
                path = archived / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("committed fixture\n", encoding="utf-8")
            self.assertLessEqual(
                len(retained), runtime.CLOSEOUT_ARCHIVE_MAX_ARTIFACTS,
            )
            self.assertFalse((archived / runtime.CLOSEOUT_PLAN_ARTIFACT).exists())
            self.assertFalse((archived / runtime.PR_READINESS_ARTIFACT).exists())

            def committed_blob(
                _root: Path,
                commit: str,
                locator: str,
            ) -> bytes | None:
                self.assertEqual(commit, transaction["commit"])
                self.assertEqual(
                    locator,
                    f"{archive}/{runtime.CLOSEOUT_PLAN_ARTIFACT}",
                )
                return json.dumps(plan).encode("utf-8")

            with (
                mock.patch.object(
                    runtime,
                    "finalization_task_dir",
                    return_value=archived,
                ),
                mock.patch.object(runtime, "task_dir_is_archived", return_value=True),
                mock.patch.object(runtime, "load_config", return_value={}),
                mock.patch.object(
                    runtime,
                    "current_head",
                    return_value=transaction["commit"],
                ),
                mock.patch.object(
                    runtime,
                    "closeout_optional_commit_blob_bytes",
                    side_effect=committed_blob,
                ),
                mock.patch.object(
                    runtime,
                    "validate_closeout_plan_for_migration",
                    side_effect=lambda value: value,
                ),
                mock.patch.object(
                    runtime,
                    "resolve_committed_closeout_archive_transaction",
                    return_value=transaction,
                ),
                mock.patch.object(
                    runtime,
                    "finalization_archived_owner_results",
                    return_value=(publication, verification),
                ),
                mock.patch.object(
                    runtime,
                    "finalization_archived_published_facts",
                    return_value=(False, None),
                ),
                mock.patch.object(
                    runtime,
                    "finalization_publication_owner_result",
                    side_effect=AssertionError("active readiness was reopened"),
                ) as readiness,
                mock.patch.object(
                    runtime,
                    "finalization_verification_owner_result",
                    side_effect=AssertionError("archived #117 artifact was reopened"),
                ) as verification_owner,
                mock.patch.object(runtime, "create_pull_request") as create_pr,
                mock.patch.object(
                    runtime,
                    "execute_archive_metadata_transaction",
                ) as archive_transaction,
            ):
                context = runtime.finalization_preview_context(
                    root,
                    mock.Mock(include_finalization_gate=True),
                    public_input,
                )
            self.assertEqual(context["transaction_state"], "archived")
            self.assertEqual(context["publication"], publication)
            readiness.assert_not_called()
            verification_owner.assert_not_called()
            create_pr.assert_not_called()
            archive_transaction.assert_not_called()

    def test_selected_runtime_archived_transition_skips_gate_and_verifier_mutation(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        plan_digest = "a" * 64
        active = ".trellis/tasks/07-31-119-combined-finish-family-integration"
        archive = (
            ".trellis/tasks/archive/2026-08/"
            "07-31-119-combined-finish-family-integration"
        )
        plan = {
            "plan_digest": plan_digest,
            "task": {"active_locator": active, "archive_locator": archive},
            "git": {"branch_review_commit": "b" * 40},
            "marketplace": {"required": True},
        }
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": active,
            "plan_ref": f"closeout-plan:{plan_digest}",
        }
        context = {
            "task_dir": Path("unused"),
            "task_context": None,
            "prepared": None,
            "plan": plan,
            "plan_ref": public_input["plan_ref"],
            "transaction_state": "archived",
            "published_transition_complete": False,
            "publication": {"owner_status": "current"},
            "publication_status": "current",
            "publication_stale_reason": None,
            "verification": (
                {"source": "committed-finalization-gate"},
                {"status": "ok", "typed_exit": "verified"},
            ),
            "facts": {"transaction_state": "archived"},
            "current_facts_sha256": "c" * 64,
        }
        gate = {
            "route": {
                "typed_exit": "ready_for_merge",
                "consumer": runtime.FINALIZATION_CONSUMERS["ready_for_merge"],
                "output": runtime.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
            }
        }
        reviewed = {
            "review": {
                "status": "passed",
                "summary": "The committed recovery is ready.",
                "evidence_refs": ["publication:current"],
            },
            "route": gate["route"],
            "supersedes_gate_ref": "task-finalization-gate:committed",
        }
        args = argparse.Namespace(
            root=None,
            input="unused-input.json",
            review_input="unused-review.json",
            gate=None,
            dry_run=False,
        )
        with tempfile.TemporaryDirectory(prefix="guru-finish-transition-") as temporary:
            root = Path(temporary)
            archived = root / archive
            archived.mkdir(parents=True)
            gate_path = archived / runtime.TASK_FINALIZATION_GATE_ARTIFACT
            gate_path.write_text("committed gate bytes\n", encoding="utf-8")
            committed_bytes = gate_path.read_bytes()
            context["task_dir"] = archived
            args.root = str(root)
            ready_for_merge_gate = {
                "route": {
                    "output": {
                        "exit_id": "ready_for_merge",
                        "repo_ref": "castbox/guru-trellis",
                        "pr_number": 166,
                        "pr_url": "https://github.com/castbox/guru-trellis/pull/166",
                        "expected_head_sha": "b" * 40,
                        "expected_base_branch": "main",
                        "expected_head_branch": "codex/119-finish-family",
                        "expected_close_issues": [119],
                    }
                }
            }
            finish_result = {
                "archived_task_dir": str(archived),
                "publish": {
                    "pr": {
                        "number": 166,
                        "url": "https://github.com/castbox/guru-trellis/pull/166",
                    }
                },
            }
            with (
                mock.patch.object(
                    runtime,
                    "finalization_public_input",
                    return_value=(public_input, "unused-input.json"),
                ),
                mock.patch.object(
                    runtime,
                    "finalization_semantic_review_input",
                    return_value=reviewed,
                ),
                mock.patch.object(
                    runtime,
                    "finalization_preview_context",
                    return_value=context,
                ),
                mock.patch.object(runtime, "finalization_validate_route"),
                mock.patch.object(
                    runtime,
                    "finalization_gate_schema",
                    return_value={},
                ),
                mock.patch.object(
                    runtime,
                    "skill_json_schema_validation_errors",
                    return_value=[],
                ),
            ):
                recorded = runtime.cmd_record_finalization_gate(args)
            self.assertEqual(recorded["typed_exit"], "ready_for_merge")
            self.assertEqual(gate_path.read_bytes(), committed_bytes)

            with (
                mock.patch.object(
                    runtime,
                    "finalization_public_input",
                    return_value=(public_input, "unused-input.json"),
                ),
                mock.patch.object(
                    runtime,
                    "finalization_gate_input",
                    return_value=(gate, gate_path),
                ),
                mock.patch.object(
                    runtime,
                    "check_finalization_gate_result",
                    return_value=(gate, context),
                ),
                mock.patch.object(
                    runtime,
                    "cmd_finish_work",
                    return_value=finish_result,
                ) as finish,
                mock.patch.object(
                    runtime,
                    "finalization_gate_with_ready_for_merge_output",
                    return_value=ready_for_merge_gate,
                ),
            ):
                transitioned = runtime.cmd_execute_finalization_transition(args)
            self.assertEqual(transitioned["output"]["pr_number"], 166)
            self.assertIsNone(getattr(finish.call_args.args[0], "external_verification", None))
            self.assertEqual(gate_path.read_bytes(), committed_bytes)

    def test_16_public_exits_have_unique_consumers_and_private_fields_stay_private(
        self,
    ) -> None:
        self.assertEqual(sum(len(exits) for exits in FINISH_EXITS.values()), 16)
        self.assertEqual(set(EXPECTED_CONSUMERS), {
            (skill_id, exit_id)
            for skill_id, exits in FINISH_EXITS.items()
            for exit_id in exits
        })
        for skill_id, expected_exits in FINISH_EXITS.items():
            interface = read_json(package(skill_id) / "interface.json")
            exits = interface["external_exits"]
            self.assertEqual({item["id"] for item in exits}, expected_exits)
            self.assertEqual(len(exits), len(expected_exits))
            outputs = interface["public_contracts"]["outputs"]
            projections = interface["public_contracts"]["projections"]
            consumers = interface["public_contracts"]["consumer_inputs"]
            for exit_id in expected_exits:
                with self.subTest(skill=skill_id, exit=exit_id):
                    external = [item for item in exits if item["id"] == exit_id]
                    output = [item for item in outputs if item["exit_id"] == exit_id]
                    projection = [
                        item for item in projections if item["exit_id"] == exit_id
                    ]
                    self.assertEqual(len(external), 1)
                    self.assertEqual(len(output), 1)
                    self.assertEqual(len(projection), 1)
                    consumer = [
                        item for item in consumers
                        if item["id"] == projection[0]["consumer_input_id"]
                    ]
                    self.assertEqual(len(consumer), 1)
                    self.assertEqual(
                        (
                            external[0]["consumer"]["kind"],
                            external[0]["consumer"]["id"],
                        ),
                        EXPECTED_CONSUMERS[(skill_id, exit_id)],
                    )
                    self.assertEqual(
                        external[0]["consumer"], consumer[0]["consumer"],
                    )
                    example = read_json(
                        package(skill_id) / output[0]["example"]["path"]
                    )
                    schema = read_json(
                        package(skill_id) / output[0]["schema"]["path"]
                    )
                    self.assertEqual(example["exit_id"], exit_id)
                    self.assertFalse(PRIVATE_FIELDS & set(example))
                    branches = output_object_branches(schema)
                    self.assertTrue(branches)
                    for branch in branches:
                        self.assertFalse(
                            branch.get("additionalProperties", True)
                        )
                        self.assertFalse(
                            PRIVATE_FIELDS & set(branch["properties"])
                        )

    def test_workflow_keeps_57_production_exits_33_targets_and_six_route_groups(
        self,
    ) -> None:
        rows = workflow_exits()
        production_rows = [
            row for row in rows if row.get("skill") != "guru-example-action"
        ]
        self.assertEqual(len(production_rows), 57)
        targets = set(
            re.findall(
                r'<!-- guru-(?:workflow|stop)-target: \{"id":"([^"]+)"\} -->',
                WORKFLOW.read_text(encoding="utf-8"),
            )
        )
        self.assertEqual(len(targets), 33)
        finish_rows: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in rows:
            key = (row["skill"], row["exit"])
            if key in EXPECTED_CONSUMERS:
                finish_rows.setdefault(key, []).append(row)
        self.assertEqual(set(finish_rows), set(EXPECTED_CONSUMERS))
        for key, expected in EXPECTED_CONSUMERS.items():
            self.assertEqual(len(finish_rows[key]), 1, key)
            consumer = finish_rows[key][0]["consumer"]
            self.assertEqual((consumer["kind"], consumer["id"]), expected)
        self.assertEqual(len(ROUTE_GROUPS), 6)
        for group, edges in ROUTE_GROUPS.items():
            with self.subTest(group=group):
                self.assertTrue(edges)
                self.assertTrue(all(edge in finish_rows for edge in edges))

    def test_guru_entries_are_equal_thin_managed_routes(self) -> None:
        canonical_root = (
            REPO / "trellis/presets/guru-team/overlays"
            if EXECUTION_MODE == "source"
            else None
        )
        installed_payloads: list[bytes] = []
        for relative in GURU_ENTRIES:
            path = REPO / relative
            self.assertTrue(path.is_file(), relative)
            self.assertFalse(path.is_symlink(), relative)
            text = path.read_text(encoding="utf-8")
            self.assertIn("guru-team-overlay: v1", text)
            self.assertIn(".trellis/workflow.md", text)
            for skill_id in FINISH_EXITS:
                self.assertIn(skill_id, text)
            self.assertIn("not user choices", text)
            self.assertIn("Do not add a routine confirmation", text)
            self.assertNotIn("finish-work.sh", text)
            self.assertNotIn("--expected-plan-digest", text)
            installed_payloads.append(path.read_bytes())
            if canonical_root is not None:
                self.assertEqual(
                    path.read_bytes(), (canonical_root / relative).read_bytes(),
                )
        self.assertEqual(len(set(installed_payloads)), 1)

    def test_terminal_corpus_is_equal_across_runtime_and_platform_discovery(
        self,
    ) -> None:
        canonical = package("guru-finalize-task") / "evals"
        roots = [
            SKILLS_ROOT / "packages/guru-finalize-task/evals",
            REPO / ".agents/skills/guru-finalize-task/evals",
            REPO / ".codex/skills/guru-finalize-task/evals",
            REPO / ".claude/skills/guru-finalize-task/evals",
            REPO / ".cursor/skills/guru-finalize-task/evals",
        ]
        expected = tree_bytes(canonical)
        cases = {
            item["id"]: item
            for item in read_json(canonical / "evals.json")["evals"]
        }
        for case_id, (profile, facts_path, recipe) in TERMINAL_CASES.items():
            self.assertIn(case_id, cases)
            self.assertEqual(cases[case_id]["expected_exit"], "ready_for_merge")
            self.assertEqual(cases[case_id]["input_profile_id"], profile)
            facts = read_json(package("guru-finalize-task") / facts_path)
            self.assertEqual(facts["owner_staging"]["recipe"], recipe)
        for root in roots:
            with self.subTest(root=root):
                self.assertTrue(root.is_dir())
                self.assertEqual(tree_bytes(root), expected)

    def test_terminal_cases_execute_through_shared_public_wrapper(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guru-finish-terminal-") as temporary:
            for case_id in TERMINAL_CASES:
                with self.subTest(case=case_id):
                    process = subprocess.run(
                        [
                            str(EVAL_RUNNER), "--root", str(REPO),
                            "--mode", EXECUTION_MODE,
                            "--skill", "guru-finalize-task",
                            "--adapter", "shared", "--case", case_id,
                            "--run-root", str(Path(temporary) / case_id),
                            "--json",
                        ],
                        cwd=REPO,
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    result = json.loads(process.stdout)
                    self.assertEqual(result["status"], "passed", result)
                    self.assertEqual(
                        result["cases"][0]["actual_exit"], "ready_for_merge",
                    )

if __name__ == "__main__":
    unittest.main()
