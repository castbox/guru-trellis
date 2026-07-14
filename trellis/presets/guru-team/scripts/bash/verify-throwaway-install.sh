#!/usr/bin/env bash
set -euo pipefail

USER_NAME="${TRELLIS_USER:-throwaway}"
WORK_DIR="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
WORKFLOW_SOURCE="${TRELLIS_WORKFLOW_SOURCE:-gh:castbox/guru-trellis/trellis#main}"
ALLOW_PUBLIC_SAMPLE="${TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE:-0}"
ENGLISH_LANGUAGE_RULE_PATTERN='All documentation (must|should) be written in .*English'
STALE_PLANNING_HINT_PATTERN='PRD-only|Lightweight tasks may be PRD-only|Lightweight tasks may have only|Lightweight task can (ask|request)|lightweight task with `?prd\.md`? complete|Missing optional artifacts|skipped for lightweight tasks|optional `?design\.md`? / `?implement\.md`?|optional `?design\.md`?|optional `?implement\.md`?|ask for start review, then run `?task\.py start`?|design\.md if present|implement\.md if present|`?design\.md`?[^[:cntrl:]]*(\(if exists\)|if exists|if present)|`?implement\.md`?[^[:cntrl:]]*(\(if exists\)|if exists|if present)|technical design if present|execution plan if present|technical design \(if exists\)|execution plan \(if exists\)|design\.md / implement\.md if present|when present, design\.md / implement\.md|when those files are present|technical design and implementation plan when present'

if [[ -z "$WORK_DIR" ]]; then
  WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/guru-trellis-install.XXXXXX")"
fi

mkdir -p "$WORK_DIR"
TARGET="$WORK_DIR/project"

if [[ -e "$TARGET" ]]; then
  echo "Target already exists: $TARGET" >&2
  exit 2
fi

command -v trellis >/dev/null 2>&1 || {
  echo "trellis CLI not found on PATH" >&2
  exit 127
}

command -v git >/dev/null 2>&1 || {
  echo "git not found on PATH" >&2
  exit 127
}

fail_if_english_language_rule() {
  local label="$1"
  shift
  local matches
  if [[ "$#" -eq 0 ]]; then
    return 0
  fi
  matches="$(grep -RInE "$ENGLISH_LANGUAGE_RULE_PATTERN" "$@" 2>/dev/null || true)"
  if [[ -n "$matches" ]]; then
    echo "Unexpected English documentation language rule in $label:" >&2
    printf '%s\n' "$matches" >&2
    exit 2
  fi
}

fail_if_stale_planning_hint() {
  local label="$1"
  shift
  local matches
  if [[ "$#" -eq 0 ]]; then
    return 0
  fi
  matches="$(grep -RInE "$STALE_PLANNING_HINT_PATTERN" "$@" 2>/dev/null || true)"
  if [[ -n "$matches" ]]; then
    echo "Unexpected legacy planning hint in $label:" >&2
    printf '%s\n' "$matches" >&2
    exit 2
  fi
}

workspace_tree_digest() {
  python3 - "$1" <<'PY'
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
digest = hashlib.sha256()
if root.is_dir():
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
print(digest.hexdigest())
PY
}

create_task_commit_plan() {
  local sequence="$1"
  local subject="$2"
  python3 - "$TARGET" "$TASK_REL" "$sequence" "$subject" <<'PY'
import hashlib
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
task_rel = sys.argv[2]
sequence = int(sys.argv[3])
subject = sys.argv[4]
runtime = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
spec = importlib.util.spec_from_file_location("installed_task_commit_runtime", runtime)
if spec is None or spec.loader is None:
    raise SystemExit(f"could not load installed task commit runtime: {runtime}")
gtt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gtt
spec.loader.exec_module(gtt)

task_dir = root / task_rel
candidate = task_dir / gtt.TASK_COMMIT_PLAN_DIR / f"{sequence:03d}.json"
candidate_rel = candidate.relative_to(root).as_posix()
snapshot = gtt.capture_task_commit_snapshot(root, {candidate_rel})
unrelated = "unrelated-preserved.log"
classifications = []
reviewed_paths = set()
for entry in snapshot["entries"]:
    path = str(entry["path"])
    is_unrelated = path == unrelated
    classifications.append({
        "path": path,
        "category": "unrelated-preserved" if is_unrelated else "task-reviewed",
        "reason": "Preserve unrelated throwaway state." if is_unrelated else "Fresh throwaway Phase 2 evidence covers this path.",
        "coverage_source": "AI throwaway scope review" if is_unrelated else "phase2-check.json",
    })
    if not is_unrelated:
        reviewed_paths.add(path)
classifications.append({
    "path": candidate_rel,
    "category": "task-reviewed",
    "reason": "Current throwaway skill invocation evidence.",
    "coverage_source": "skill-artifact",
})
reviewed_paths.add(candidate_rel)
snapshot_by_path = {str(item["path"]): item for item in snapshot["entries"]}
exact_paths = set(reviewed_paths)
for path in list(reviewed_paths):
    renamed_from = snapshot_by_path.get(path, {}).get("renamed_from")
    if renamed_from:
        exact_paths.add(str(renamed_from))

body = (
    "背景：\n需要验证安装后的 task commit 闭环。\n\n"
    "变更：\n提交当前轮次经过检查的精确路径。\n\n"
    "边界：\n保留无关工作区状态且不执行 push。\n\n"
    "验证：\n候选校验与真实提交后置条件均通过。\n\n"
    "Refs #122"
)
message_bytes = f"{subject}\n\n{body}\n"
task = gtt.read_json(task_dir / "task.json")
ledger = gtt.read_json(task_dir / "issue-scope-ledger.json")
primary_issue = int(ledger["primary_issue"]["number"])
plan = {
    "$schema": gtt.TASK_COMMIT_PLAN_SCHEMA_ID,
    "schema_version": gtt.TASK_COMMIT_PLAN_SCHEMA_VERSION,
    "skill_id": gtt.TASK_COMMIT_SKILL_ID,
    "sequence": f"{sequence:03d}",
    "task": {
        "id": task["id"],
        "path": task_rel,
        "status": task["status"],
        "branch": task["branch"],
    },
    "issue": {
        "primary_issue": primary_issue,
        "ledger_sha256": hashlib.sha256((task_dir / "issue-scope-ledger.json").read_bytes()).hexdigest(),
    },
    "git": {
        "base_branch": task["base_branch"],
        "base_ref": gtt.diff_base_ref(root, task["base_branch"]),
        "pre_commit_head": gtt.current_head(root),
    },
    "evidence": {
        "planning_approval": gtt.task_commit_file_evidence(root, task_dir / "planning-approval.json"),
        "phase2_check": gtt.task_commit_file_evidence(root, task_dir / "phase2-check.json"),
        "issue_scope_ledger": gtt.task_commit_file_evidence(root, task_dir / "issue-scope-ledger.json"),
        "task": gtt.task_commit_file_evidence(root, task_dir / "task.json"),
    },
    "dirty_snapshot": snapshot,
    "path_classifications": classifications,
    "exact_stage_paths": sorted(exact_paths),
    "message": {
        "subject": subject,
        "body": body,
        "bytes": message_bytes,
        "sha256": hashlib.sha256(message_bytes.encode("utf-8")).hexdigest(),
    },
    "ai_review": {
        "status": "passed",
        "reviewer": "throwaway-task-commit-review",
        "summary": "Reviewed the exact fixture paths, message, upgrade boundary and unrelated preservation.",
        "evidence": ["Fresh Phase 2 evidence covers every task-reviewed fixture path."],
    },
    "authorization": {
        "authorized": True,
        "source": "explicit-throwaway-test-authorization",
        "evidence": "The verifier authorizes this exact disposable repository commit plan.",
    },
    "freshness": {"captured_at": gtt.now_iso(), "plan_digest": ""},
    "result": {"status": "planned", "exit": None},
}
plan["freshness"]["plan_digest"] = gtt.task_commit_plan_digest(plan)
gtt.write_json(candidate, plan)
print(candidate_rel)
PY
}

CURRENT_BRANCH="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
CURRENT_DIRTY="$(git -C "$REPO_ROOT" status --short -- trellis/index.json trellis/workflows/guru-team/workflow.md 2>/dev/null || true)"
USE_LOCAL_WORKFLOW_SAMPLE=0
if [[ ( "$WORKFLOW_SOURCE" == gh:castbox/guru-trellis/trellis || "$WORKFLOW_SOURCE" == gh:castbox/guru-trellis/trellis#main ) && ( "$CURRENT_BRANCH" != "main" || -n "$CURRENT_DIRTY" ) ]]; then
  if [[ "$ALLOW_PUBLIC_SAMPLE" != "1" ]]; then
    python3 - <<PY
import json
payload = {
  "status": "error",
  "error": "throwaway install would sample the public marketplace, not the current branch workflow source",
  "workflow_source": "$WORKFLOW_SOURCE",
  "current_branch": "$CURRENT_BRANCH",
  "dirty_marketplace_paths": [line for line in """$CURRENT_DIRTY""".splitlines() if line.strip()],
  "next_steps": [
    "push the branch, then rerun with TRELLIS_WORKFLOW_SOURCE pointing at that exact branch ref; release validation may instead use an existing release tag",
    "or rerun with TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 and report that current-branch marketplace install was not verified",
  ],
}
print(json.dumps(payload, ensure_ascii=False, indent=2))
PY
    exit 2
  fi
  USE_LOCAL_WORKFLOW_SAMPLE=1
fi

apply_local_workflow_sample() {
  if [[ "$USE_LOCAL_WORKFLOW_SAMPLE" == "1" ]]; then
    cp "$REPO_ROOT/trellis/workflows/guru-team/workflow.md" "$TARGET/.trellis/workflow.md"
  fi
}

mkdir "$TARGET"
git -C "$TARGET" init -q
git -C "$TARGET" remote add origin https://github.com/castbox/guru-trellis-throwaway.git

(
  cd "$TARGET"
  trellis init -y -u "$USER_NAME" --codex --cursor \
    --workflow guru-team \
    --workflow-source "$WORKFLOW_SOURCE"
)
apply_local_workflow_sample
if [[ "$USE_LOCAL_WORKFLOW_SAMPLE" == "1" ]]; then
  cmp -s "$REPO_ROOT/trellis/workflows/guru-team/workflow.md" "$TARGET/.trellis/workflow.md"
fi

WORKSPACE_SENTINEL="$TARGET/.trellis/workspace/private/shared-start-secret-journal.md"
mkdir -p "$(dirname "$WORKSPACE_SENTINEL")"
printf '%s\n' 'SHARED_START_SECRET_JOURNAL_CONTENT' >"$WORKSPACE_SENTINEL"
NO_WORKSPACE_GUARD_DIR="$(mktemp -d "$WORK_DIR/no-workspace-guard.XXXXXX")"
cat >"$NO_WORKSPACE_GUARD_DIR/sitecustomize.py" <<'PY'
import os
import sys


def _reject_workspace_access(event, args):
    if event not in {"open", "os.listdir", "os.scandir"} or not args:
        return
    try:
        value = os.fspath(args[0]).replace("\\", "/")
    except TypeError:
        return
    if ".trellis/workspace" in value:
        os._exit(91)


sys.addaudithook(_reject_workspace_access)
PY

WORKSPACE_TREE_DIGEST_BEFORE="$(workspace_tree_digest "$TARGET/.trellis/workspace")"

"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$TARGET" \
  --platform codex \
  --platform cursor

test -f "$TARGET/.trellis/workflow.md"
grep -q "Guru Team Development Workflow" "$TARGET/.trellis/workflow.md"
grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"
grep -q 'Guru Team implementation tasks require `prd.md`, `design.md`, and `implement.md`' "$TARGET/.trellis/workflow.md"
grep -q "record-subagent-liveness-event.sh" "$TARGET/.trellis/workflow.md"
grep -q "check-subagent-liveness.sh" "$TARGET/.trellis/workflow.md"
grep -q "dispatch_mode: sub-agent" "$TARGET/.trellis/config.yaml"
fail_if_english_language_rule ".trellis/spec" "$TARGET/.trellis/spec"
WORKSPACE_TREE_DIGEST_AFTER="$(workspace_tree_digest "$TARGET/.trellis/workspace")"
if [[ "$WORKSPACE_TREE_DIGEST_AFTER" != "$WORKSPACE_TREE_DIGEST_BEFORE" ]]; then
  echo "Preset modified .trellis/workspace content" >&2
  exit 2
fi
if [[ -d "$TARGET/.trellis/tasks/00-bootstrap-guidelines" ]]; then
  fail_if_english_language_rule "00-bootstrap-guidelines" "$TARGET/.trellis/tasks/00-bootstrap-guidelines"
fi
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-env.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/version.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-subagent-liveness.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-commit-messages.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/create-task-commit.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/format-merge-commit.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh"
test -f "$TARGET/.trellis/guru-team/extension.json"
python3 - "$TARGET/.trellis/guru-team/extension.json" "$TARGET" <<'PY'
import json
import pathlib
import sys

manifest_path = pathlib.Path(sys.argv[1])
root = pathlib.Path(sys.argv[2])
payload = json.loads(manifest_path.read_text(encoding="utf-8"))
extension = payload["extension"]
install = payload["install"]
skills = payload["skill_packages"]
api = extension["public_api"]
assets = install["managed_assets"]
assert extension["extension_id"] == "guru-team"
assert extension["version"] == "0.6.5-guru.5"
assert extension["target_trellis_cli"] == "0.6.5"
assert assets == sorted(set(assets))
assert len(assets) == 68
assert all((root / path).is_file() for path in assets)
for artifact in (
    "agent-assignment.json", "pr-body.md", "closeout-plan.json",
    "finish-summary.json", "task-commit-plans/*.json",
):
    assert artifact in api["artifact_contracts"]
for command in (
    "resolve-human-artifacts", "record-subagent-liveness-event",
    "check-subagent-liveness", "check-commit-messages",
    "create-task-commit", "format-merge-commit",
    "backfill-finish-summary", "check-skill-packages",
):
    assert command in api["companion_scripts"]
assert api["skill_contracts"]["canonical_root"] == "trellis/skills/guru-team/"
assert api["skill_contracts"]["active_skill_ids"] == ["guru-create-task-commit"]
assert skills["status"] == "ok"
assert skills["reserved_ids"] == ["guru-create-work-commit"]
assert skills["active_ids"] == ["guru-create-task-commit"]
assert skills["selected_platforms"] == ["codex", "cursor"]
assert skills["sidecars"] == []
assert len(skills["files"]) == 35
PY
"$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$REPO_ROOT" --json --mode source >/dev/null
"$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$TARGET" --json --mode installed >/dev/null
test ! -e "$TARGET/.agents/skills/guru-create-work-commit"
test ! -e "$TARGET/.codex/skills/guru-create-work-commit"
test ! -e "$TARGET/.cursor/skills/guru-create-work-commit"
test ! -e "$TARGET/.claude/skills/guru-create-work-commit"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-commit/SKILL.md"
test -x "$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh"
test -x "$TARGET/.agents/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.codex/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.cursor/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test ! -e "$TARGET/.claude/skills/guru-create-task-commit"
test ! -e "$TARGET/.agents/skills/guru-example-action"
test ! -e "$TARGET/.codex/skills/guru-example-action"
test ! -e "$TARGET/.cursor/skills/guru-example-action"
test ! -e "$TARGET/.claude/skills/guru-example-action"
(cd "$REPO_ROOT" && python3 -m unittest trellis.skills.guru-team.tests.test_skill_packages.DistributionTests.test_unchanged_reapply)
test -f "$TARGET/.trellis/guru-team/schemas/closeout-plan.schema.json"
mkdir -p "$TARGET/.trellis/tasks/archive"
BACKFILL_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh" --root "$TARGET" --json --dry-run)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["mode"] == "dry-run"; assert payload["scanned_tasks"] == 0; assert payload["to_write"] == []; assert payload["skipped"] == []; assert payload["errors"] == []' <<<"$BACKFILL_JSON"
grep -q "def prepare_closeout" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
! grep -q "def resolve_closeout_state" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
grep -q "publish-pr is a compatibility-only blocked command" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
grep -q "def ensure_closeout_draft_pr" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
grep -q "If any ordinary stage fails, rerun this same entry with the same expected digest" "$TARGET/.agents/skills/trellis-finish-work/SKILL.md"
grep -q "archive-month-preflight" "$TARGET/.agents/skills/trellis-finish-work/SKILL.md"
grep -q "hooks.after_archive" "$TARGET/.agents/skills/trellis-finish-work/SKILL.md"
test -z "$(find "$TARGET" -type f \( -name '*.new' -o -name '*.bak' \) -print -quit)"
test -d "$TARGET/.agents/skills"
test -d "$TARGET/.codex"
test -d "$TARGET/.cursor"
test ! -e "$TARGET/.claude"
test -f "$TARGET/.codex/hooks/session-start.py"
test -f "$TARGET/.cursor/hooks/session-start.py"
test -f "$TARGET/.cursor/hooks/inject-subagent-context.py"
test -f "$TARGET/.agents/skills/trellis-brainstorm/SKILL.md"
test -f "$TARGET/.agents/skills/trellis-before-dev/SKILL.md"
test -f "$TARGET/.agents/skills/trellis-check/SKILL.md"
test -f "$TARGET/.cursor/skills/trellis-brainstorm/SKILL.md"
test -f "$TARGET/.cursor/skills/trellis-before-dev/SKILL.md"
test -f "$TARGET/.cursor/skills/trellis-check/SKILL.md"
test -f "$TARGET/.agents/skills/trellis-meta/references/local-architecture/task-system.md"
test -f "$TARGET/.agents/skills/trellis-meta/references/local-architecture/context-injection.md"
test -f "$TARGET/.agents/skills/trellis-meta/references/customize-local/change-context-loading.md"
test -f "$TARGET/.agents/skills/trellis-meta/references/customize-local/change-workflow.md"
test -f "$TARGET/.agents/skills/trellis-meta/references/platform-files/agents.md"
test -f "$TARGET/.cursor/skills/trellis-meta/references/local-architecture/task-system.md"
test -f "$TARGET/.cursor/skills/trellis-meta/references/local-architecture/context-injection.md"
test -f "$TARGET/.cursor/skills/trellis-meta/references/customize-local/change-context-loading.md"
test -f "$TARGET/.cursor/skills/trellis-meta/references/customize-local/change-workflow.md"
test -f "$TARGET/.cursor/skills/trellis-meta/references/platform-files/agents.md"
fail_if_stale_planning_hint \
  "workflow, Codex/Cursor hooks, brainstorm skills, and trellis-meta planning references" \
  "$TARGET/.trellis/workflow.md" \
  "$TARGET/.codex/hooks/session-start.py" \
  "$TARGET/.cursor/hooks/session-start.py" \
  "$TARGET/.cursor/hooks/inject-subagent-context.py" \
  "$TARGET/.agents/skills/trellis-brainstorm/SKILL.md" \
  "$TARGET/.agents/skills/trellis-before-dev/SKILL.md" \
  "$TARGET/.agents/skills/trellis-check/SKILL.md" \
  "$TARGET/.cursor/skills/trellis-brainstorm/SKILL.md" \
  "$TARGET/.cursor/skills/trellis-before-dev/SKILL.md" \
  "$TARGET/.cursor/skills/trellis-check/SKILL.md" \
  "$TARGET/.agents/skills/trellis-meta/references/local-architecture/task-system.md" \
  "$TARGET/.agents/skills/trellis-meta/references/local-architecture/context-injection.md" \
  "$TARGET/.agents/skills/trellis-meta/references/customize-local/change-context-loading.md" \
  "$TARGET/.agents/skills/trellis-meta/references/customize-local/change-workflow.md" \
  "$TARGET/.agents/skills/trellis-meta/references/platform-files/agents.md" \
  "$TARGET/.cursor/skills/trellis-meta/references/local-architecture/task-system.md" \
  "$TARGET/.cursor/skills/trellis-meta/references/local-architecture/context-injection.md" \
  "$TARGET/.cursor/skills/trellis-meta/references/customize-local/change-context-loading.md" \
  "$TARGET/.cursor/skills/trellis-meta/references/customize-local/change-workflow.md" \
  "$TARGET/.cursor/skills/trellis-meta/references/platform-files/agents.md"
grep -q "post-planning confirmation" "$TARGET/.codex/hooks/session-start.py"
grep -q "post-planning confirmation" "$TARGET/.cursor/hooks/session-start.py"
set +e
PHASE_CONTEXT_OUTPUT="$(cd "$TARGET" && PYTHONPATH="$NO_WORKSPACE_GUARD_DIR" python3 ./.trellis/scripts/get_context.py --mode phase 2>&1)"
PHASE_CONTEXT_STATUS=$?
PACKAGE_CONTEXT_OUTPUT="$(cd "$TARGET" && PYTHONPATH="$NO_WORKSPACE_GUARD_DIR" python3 ./.trellis/scripts/get_context.py --mode packages 2>&1)"
PACKAGE_CONTEXT_STATUS=$?
CURRENT_TASK_OUTPUT="$(cd "$TARGET" && PYTHONPATH="$NO_WORKSPACE_GUARD_DIR" python3 ./.trellis/scripts/task.py current --source 2>&1)"
CURRENT_TASK_STATUS=$?
set -e
if [[ "$PHASE_CONTEXT_STATUS" -ne 0 || "$PACKAGE_CONTEXT_STATUS" -ne 0 ]]; then
  echo "Guru Team no-workspace phase/packages context command failed" >&2
  exit 2
fi
if [[ "$CURRENT_TASK_STATUS" -ne 0 && "$CURRENT_TASK_STATUS" -ne 1 ]]; then
  echo "Guru Team no-workspace current-task command returned an unexpected status" >&2
  exit 2
fi
NO_WORKSPACE_CONTEXT_OUTPUT="$PHASE_CONTEXT_OUTPUT
$PACKAGE_CONTEXT_OUTPUT
$CURRENT_TASK_OUTPUT"
if grep -Eq 'shared-start-secret-journal\.md|SHARED_START_SECRET_JOURNAL_CONTENT|JOURNAL FILE|Line count:' <<<"$NO_WORKSPACE_CONTEXT_OUTPUT"; then
  echo "Guru Team no-workspace context disclosed the workspace journal sentinel" >&2
  exit 2
fi
grep -q "required design.md" "$TARGET/.cursor/hooks/inject-subagent-context.py"
grep -q "explicit post-planning confirmation" "$TARGET/.agents/skills/trellis-brainstorm/SKILL.md"
grep -q "explicit post-planning confirmation" "$TARGET/.cursor/skills/trellis-brainstorm/SKILL.md"
grep -q "required \`design.md\`" "$TARGET/.agents/skills/trellis-before-dev/SKILL.md"
grep -q "required \`design.md\`" "$TARGET/.cursor/skills/trellis-before-dev/SKILL.md"
grep -q "required \`design.md\`" "$TARGET/.agents/skills/trellis-check/SKILL.md"
grep -q "required \`design.md\`" "$TARGET/.cursor/skills/trellis-check/SKILL.md"
grep -q "Guru Team requires this document before implementation" "$TARGET/.agents/skills/trellis-meta/references/local-architecture/task-system.md"
grep -q "Guru Team requires this document before implementation" "$TARGET/.cursor/skills/trellis-meta/references/local-architecture/task-system.md"
grep -q "required \`design.md\`" "$TARGET/.agents/skills/trellis-meta/references/local-architecture/context-injection.md"
grep -q "required \`design.md\`" "$TARGET/.cursor/skills/trellis-meta/references/local-architecture/context-injection.md"
grep -q "required \`design.md\`" "$TARGET/.agents/skills/trellis-meta/references/customize-local/change-context-loading.md"
grep -q "required \`design.md\`" "$TARGET/.cursor/skills/trellis-meta/references/customize-local/change-context-loading.md"
grep -q "explicit post-planning confirmation" "$TARGET/.agents/skills/trellis-meta/references/customize-local/change-workflow.md"
grep -q "explicit post-planning confirmation" "$TARGET/.cursor/skills/trellis-meta/references/customize-local/change-workflow.md"
grep -q 'required `prd.md`, `design.md`, `implement.md`' "$TARGET/.agents/skills/trellis-meta/references/platform-files/agents.md"
grep -q 'required `prd.md`, `design.md`, `implement.md`' "$TARGET/.cursor/skills/trellis-meta/references/platform-files/agents.md"
test -f "$TARGET/.trellis/agents/implement.md"
grep -q "实现代理" "$TARGET/.trellis/agents/implement.md"
test -f "$TARGET/.trellis/agents/check.md"
grep -q "required Guru Team technical design" "$TARGET/.trellis/agents/check.md"
test -f "$TARGET/.codex/agents/trellis-implement.toml"
grep -q "实现代理" "$TARGET/.codex/agents/trellis-implement.toml"
grep -q 'nickname_candidates.*Implement Agent' "$TARGET/.codex/agents/trellis-implement.toml"
if grep -q 'nickname_candidates.*实现代理' "$TARGET/.codex/agents/trellis-implement.toml"; then
  echo "Codex nickname_candidates must stay ASCII or Codex ignores the agent file" >&2
  exit 2
fi
test -f "$TARGET/.codex/agents/trellis-check.toml"
grep -q "阶段二检查代理" "$TARGET/.codex/agents/trellis-check.toml"
grep -q "required \`design.md\`" "$TARGET/.codex/agents/trellis-check.toml"
test -f "$TARGET/.cursor/agents/trellis-check.md"
grep -q "阶段二检查代理" "$TARGET/.cursor/agents/trellis-check.md"
grep -q "required .*design.md" "$TARGET/.cursor/agents/trellis-check.md"
fail_if_stale_planning_hint \
  "check agent files" \
  "$TARGET/.trellis/agents/check.md" \
  "$TARGET/.codex/agents/trellis-check.toml" \
  "$TARGET/.cursor/agents/trellis-check.md"
python3 "$TARGET/.trellis/scripts/get_context.py" --mode packages >/dev/null
CHECK_ENV_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/check-env.sh" --root "$TARGET" --json)"
printf '%s\n' "$CHECK_ENV_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["github_repo"] == "castbox/guru-trellis-throwaway"; assert payload["status"] == "ok"; assert payload["guru_team_extension"]["status"] == "ok"; assert payload["guru_team_extension"]["version"]; assert payload["guru_team_extension"]["target_trellis_cli"] == "0.6.5"' <<<"$CHECK_ENV_JSON"
VERSION_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/version.sh" --root "$TARGET" --json)"
printf '%s\n' "$VERSION_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["guru_team_extension"]["status"] == "ok"; assert payload["guru_team_extension"]["version"]; assert payload["guru_team_extension"]["target_trellis_cli"] == "0.6.5"' <<<"$VERSION_JSON"

set +e
FINISH_ERROR_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/finish-work.sh" --root "$TARGET" --json --dry-run 2>&1)"
FINISH_STATUS=$?
set -e
if [[ "$FINISH_STATUS" -eq 0 ]]; then
  echo "finish-work direct dry-run unexpectedly succeeded without explicit trellis-finish-work intent" >&2
  exit 2
fi
printf '%s\n' "$FINISH_ERROR_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "error"; assert payload["blocked_step"] == "finish-work"; assert payload["intent_flag"] == "--from-trellis-finish-work"' <<<"$FINISH_ERROR_JSON"

set +e
PUBLISH_ERROR_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/publish-pr.sh" --root "$TARGET" --json --dry-run 2>&1)"
PUBLISH_STATUS=$?
set -e
if [[ "$PUBLISH_STATUS" -eq 0 ]]; then
  echo "publish-pr direct dry-run unexpectedly succeeded before finish-work" >&2
  exit 2
fi
printf '%s\n' "$PUBLISH_ERROR_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "error"; assert payload["blocked_step"] == "publish-pr"; assert payload["required_entrypoint"] == "trellis-finish-work"' <<<"$PUBLISH_ERROR_JSON"

git -C "$TARGET" config user.name "Installed Task Commit Smoke"
git -C "$TARGET" config user.email "installed-task-commit@example.invalid"
git -C "$TARGET" branch -M main
git -C "$TARGET" add -A
git -C "$TARGET" commit -q -m "chore: install Guru Team throwaway baseline"
BASELINE_HEAD="$(git -C "$TARGET" rev-parse HEAD)"
TASK_BRANCH="feat/122-installed-task-commit"
TASK_REL=".trellis/tasks/07-13-122-installed-task-commit"
git -C "$TARGET" switch -q -c "$TASK_BRANCH"

python3 - "$TARGET" "$TASK_REL" "$TASK_BRANCH" "$BASELINE_HEAD" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
task_rel = sys.argv[2]
branch = sys.argv[3]
base_head = sys.argv[4]
task_dir = root / task_rel
task_dir.mkdir(parents=True)
(root / "src").mkdir(exist_ok=True)

context = {
    "schema_version": "1.0",
    "source_issue": {
        "number": 122,
        "url": "https://github.com/castbox/guru-trellis/issues/122",
        "title": "installed task commit smoke",
        "created_by_workflow": False,
    },
    "source_repo": {
        "repo": "castbox/guru-trellis-throwaway",
        "url": "https://github.com/castbox/guru-trellis-throwaway",
    },
    "task_slug": "122-installed-task-commit",
    "task_title": "#122 验证安装后 task commit",
    "task_artifact_dir": task_rel,
    "branch_name": branch,
    "base_branch": "main",
    "base_ref": "main",
    "base_head_sha": base_head,
    "remote_head_sha": base_head,
    "workspace_slug": "",
    "task_workspace_id": "122-installed-task-commit",
    "assignee": "throwaway",
    "actor": {"login": "throwaway"},
    "issue_scope_ledger_seed": {},
    "intake_summary": {},
}
task = {
    "id": "122-installed-task-commit",
    "name": "122-installed-task-commit",
    "title": "#122 验证安装后 task commit",
    "status": "in_progress",
    "branch": branch,
    "base_branch": "main",
}
ledger = {
    "schema_version": "1.0",
    "primary_issue": {"number": 122},
    "close_issues": [{"number": 122}],
    "related_issues": [],
    "followup_issues": [],
}
documents = {
    "prd.md": "# 安装后任务提交验证\n\n## 目标\n\n执行初次提交与修订提交，保留无关文件。\n",
    "design.md": "# 技术设计\n\n使用已安装 skill package、候选校验器与精确 executor。\n",
    "implement.md": "# 实施计划\n\n1. 记录检查证据。\n2. 执行两轮独立候选提交。\n",
}
for name, content in documents.items():
    (task_dir / name).write_text(content, encoding="utf-8")
for name, payload in (
    ("task-start-context.json", context),
    ("task.json", task),
    ("issue-scope-ledger.json", ledger),
):
    (task_dir / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(root / "src/task-commit-smoke.txt").write_text("initial task change\n", encoding="utf-8")
(root / "unrelated-preserved.log").write_text("preserve this exact state\n", encoding="utf-8")
PY

"$TARGET/.trellis/guru-team/scripts/bash/record-planning-approval.sh" \
  --root "$TARGET" \
  --task "$TASK_REL" \
  --reviewer "throwaway-planning-review" \
  --summary "已复核三份 throwaway 规划文档与固定提交范围。" \
  --ambiguity-reviewer "throwaway-ambiguity-review" \
  --ambiguity-summary "已检查弱约束词、入口边界与验收口径，无未决歧义。" \
  --user-confirmation "已明确授权 disposable throwaway 进入实现验证。" \
  >/dev/null

record_throwaway_phase2() {
  local summary="$1"
  "$TARGET/.trellis/guru-team/scripts/bash/record-phase2-check.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --pass \
    --checker "throwaway-phase2-check" \
    --summary "$summary" \
    --coverage requirements \
    --coverage design \
    --coverage code \
    --coverage tests \
    --coverage spec_sync \
    --coverage cross_layer \
    --coverage docs_ssot \
    --coverage deployment \
    --validation "installed task commit smoke|passed" \
    >/dev/null
}

record_throwaway_phase2 "已检查初次提交的需求、设计、代码、测试、文档与安装边界。"
INITIAL_PLAN="$(create_task_commit_plan 1 "feat(trellis): #122 验证安装后任务提交")"
INITIAL_CANDIDATE_JSON="$(
  "$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --json \
    --candidate-artifact "$INITIAL_PLAN"
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["mode"] == "candidate"; assert payload["checked_commits"] == []; assert payload["candidate_validation"]["sequence"] == "001"' <<<"$INITIAL_CANDIDATE_JSON"
INITIAL_COMMIT_JSON="$(
  "$TARGET/.agents/skills/guru-create-task-commit/scripts/create-task-commit.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --json \
    --candidate-artifact "$INITIAL_PLAN"
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == payload["exit"] == "committed"; assert payload["sequence"] == "001"; assert "unrelated-preserved.log" in payload["unrelated_preserved_paths"]' <<<"$INITIAL_COMMIT_JSON"
INITIAL_COMMIT="$(python3 -c 'import json, sys; print(json.load(sys.stdin)["commit_sha"])' <<<"$INITIAL_COMMIT_JSON")"
test "$(git -C "$TARGET" show -s --format=%P "$INITIAL_COMMIT")" = "$BASELINE_HEAD"
test "$(git -C "$TARGET" show -s --format=%s "$INITIAL_COMMIT")" = "feat(trellis): #122 验证安装后任务提交"
test "$(git -C "$TARGET" status --short -- unrelated-preserved.log)" = "?? unrelated-preserved.log"
test "$(cat "$TARGET/unrelated-preserved.log")" = "preserve this exact state"

printf '%s\n' "finding fix task change" >"$TARGET/src/task-commit-smoke.txt"
record_throwaway_phase2 "已在 finding fix 后重新检查全部范围并绑定新的 HEAD 与 dirty state。"
REVISION_PLAN="$(create_task_commit_plan 2 "fix(trellis): #122 验证 finding 修订提交")"
REVISION_CANDIDATE_JSON="$(
  "$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --json \
    --candidate-artifact "$REVISION_PLAN"
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["candidate_validation"]["sequence"] == "002"; assert payload["candidate_validation"]["pre_commit_head"] == sys.argv[1]' "$INITIAL_COMMIT" <<<"$REVISION_CANDIDATE_JSON"
REVISION_COMMIT_JSON="$(
  "$TARGET/.agents/skills/guru-create-task-commit/scripts/create-task-commit.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --json \
    --candidate-artifact "$REVISION_PLAN"
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == payload["exit"] == "committed"; assert payload["sequence"] == "002"; assert payload["pre_commit_head"] == sys.argv[1]' "$INITIAL_COMMIT" <<<"$REVISION_COMMIT_JSON"
REVISION_COMMIT="$(python3 -c 'import json, sys; print(json.load(sys.stdin)["commit_sha"])' <<<"$REVISION_COMMIT_JSON")"
test "$(git -C "$TARGET" show -s --format=%P "$REVISION_COMMIT")" = "$INITIAL_COMMIT"
test "$(git -C "$TARGET" show -s --format=%s "$REVISION_COMMIT")" = "fix(trellis): #122 验证 finding 修订提交"
test "$(git -C "$TARGET" rev-list --count main..HEAD)" = "2"
test "$(git -C "$TARGET" status --short -- unrelated-preserved.log)" = "?? unrelated-preserved.log"
test "$(cat "$TARGET/unrelated-preserved.log")" = "preserve this exact state"
python3 - "$TARGET/$INITIAL_PLAN" "$TARGET/$REVISION_PLAN" <<'PY'
import json
import sys
from pathlib import Path

first = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
second = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
assert first["result"]["status"] == first["result"]["exit"] == "committed"
assert second["result"]["status"] == second["result"]["exit"] == "committed"
assert first["result"]["commit_sha"] != second["result"]["commit_sha"]
PY
set +e
STALE_PLAN_JSON="$(
  "$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --json \
    --candidate-artifact "$INITIAL_PLAN" \
    2>&1
)"
STALE_PLAN_STATUS=$?
set -e
if [[ "$STALE_PLAN_STATUS" -eq 0 ]]; then
  echo "Old task commit plan unexpectedly passed after the revision commit" >&2
  exit 2
fi
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "blocked"; assert any("stale" in item or "planned state" in item for item in payload["errors"])' <<<"$STALE_PLAN_JSON"

INITIAL_CLOSEOUT_JSON="$(python3 "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_closeout.py" --repo "$TARGET" --case initial)"
printf '%s\n' "$INITIAL_CLOSEOUT_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["issue"] == 105; assert payload["local_head"] == payload["remote_head"] == payload["pr_head"]; assert payload["pr_ready"] is True; assert payload["after_archive_hook_preflight"] is True' <<<"$INITIAL_CLOSEOUT_JSON"

rm -f "$TARGET/.trellis/workflow.md.new"
(
  cd "$TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --create-new
)
test -f "$TARGET/.trellis/workflow.md.new"
grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md.new"
rm -f "$TARGET/.trellis/workflow.md.new"
test ! -e "$TARGET/.trellis/workflow.md.new"
(
  cd "$TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force
)
apply_local_workflow_sample
grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"

(
  cd "$TARGET"
  trellis update --force
)
(
  cd "$TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force
)
apply_local_workflow_sample
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$TARGET" \
  --platform codex \
  --platform cursor

grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"
test -f "$TARGET/.trellis/guru-team/schemas/finish-summary.schema.json"
test -f "$TARGET/.trellis/guru-team/schemas/closeout-plan.schema.json"
test -x "$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/create-task-commit.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-commit/SKILL.md"
test -x "$TARGET/.agents/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.codex/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.cursor/skills/guru-create-task-commit/scripts/create-task-commit.sh"
"$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$REPO_ROOT" --json --mode source >/dev/null
"$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$TARGET" --json --mode installed >/dev/null
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh"
BACKFILL_AFTER_UPDATE_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh" --root "$TARGET" --json --dry-run)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["mode"] == "dry-run"; assert payload["scanned_tasks"] == 1; assert payload["errors"] == []' <<<"$BACKFILL_AFTER_UPDATE_JSON"
grep -q '^session_auto_commit: false$' "$TARGET/.trellis/config.yaml"
grep -q '^\.trellis/workspace/$' "$TARGET/.gitignore"

UPDATED_CLOSEOUT_JSON="$(python3 "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_closeout.py" --repo "$TARGET" --case after-update)"
printf '%s\n' "$UPDATED_CLOSEOUT_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["issue"] == 106; assert payload["local_head"] == payload["remote_head"] == payload["pr_head"]; assert payload["pr_ready"] is True; assert payload["after_archive_hook_preflight"] is True' <<<"$UPDATED_CLOSEOUT_JSON"

FINAL_SIDECARS="$(find "$TARGET" -type f \( -name '*.new' -o -name '*.bak' \) -print)"
if [[ -n "$FINAL_SIDECARS" ]]; then
  echo "Unexpected .new/.bak sidecars after preview, switch, update, and preset reapply:" >&2
  printf '%s\n' "$FINAL_SIDECARS" >&2
  exit 2
fi

if [[ "$USE_LOCAL_WORKFLOW_SAMPLE" == "1" ]]; then
  echo "Verified public marketplace discovery plus local unpublished workflow sample at $TARGET"
else
  echo "Verified throwaway Guru Team Trellis install at $TARGET"
fi
