#!/usr/bin/env bash
set -euo pipefail

USER_NAME="${TRELLIS_USER:-throwaway}"
WORK_DIR="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
WORKFLOW_SOURCE="${TRELLIS_WORKFLOW_SOURCE:-gh:castbox/guru-trellis/trellis#v0.6.5-guru.3}"
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

CURRENT_BRANCH="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
CURRENT_DIRTY="$(git -C "$REPO_ROOT" status --short -- trellis/index.json trellis/workflows/guru-team/workflow.md 2>/dev/null || true)"
if [[ "$WORKFLOW_SOURCE" == gh:castbox/guru-trellis/trellis && ( "$CURRENT_BRANCH" != "main" || -n "$CURRENT_DIRTY" ) && "$ALLOW_PUBLIC_SAMPLE" != "1" ]]; then
  python3 - <<PY
import json
payload = {
  "status": "error",
  "error": "throwaway install would sample the public marketplace, not the current branch workflow source",
  "workflow_source": "$WORKFLOW_SOURCE",
  "current_branch": "$CURRENT_BRANCH",
  "dirty_marketplace_paths": [line for line in """$CURRENT_DIRTY""".splitlines() if line.strip()],
  "next_steps": [
    "push the branch or create the release tag, then rerun with TRELLIS_WORKFLOW_SOURCE pointing at a supported gh: source with #ref, for example gh:castbox/guru-trellis/trellis#v0.6.5-guru.3",
    "or rerun with TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 and report that current-branch marketplace install was not verified",
  ],
}
print(json.dumps(payload, ensure_ascii=False, indent=2))
PY
  exit 2
fi

mkdir "$TARGET"
git -C "$TARGET" init -q
git -C "$TARGET" remote add origin https://github.com/castbox/guru-trellis-throwaway.git

(
  cd "$TARGET"
  trellis init -y -u "$USER_NAME" --codex --cursor \
    --workflow guru-team \
    --workflow-source "$WORKFLOW_SOURCE"
)

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
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-subagent-liveness.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-commit-messages.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/format-merge-commit.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh"
test -f "$TARGET/.trellis/guru-team/extension.json"
python3 -c 'import json, sys; payload = json.load(open(sys.argv[1], encoding="utf-8")); extension = payload["extension"]; api = extension["public_api"]; assert extension["extension_id"] == "guru-team"; assert extension["version"]; assert extension["target_trellis_cli"] == "0.6.5"; assert "agent-assignment.json" in api["artifact_contracts"]; assert "pr-body.md" in api["artifact_contracts"]; assert "closeout-plan.json" in api["artifact_contracts"]; assert "finish-summary.json" in api["artifact_contracts"]; assert "resolve-human-artifacts" in api["companion_scripts"]; assert "record-subagent-liveness-event" in api["companion_scripts"]; assert "check-subagent-liveness" in api["companion_scripts"]; assert "check-commit-messages" in api["companion_scripts"]; assert "format-merge-commit" in api["companion_scripts"]; assert "backfill-finish-summary" in api["companion_scripts"]' "$TARGET/.trellis/guru-team/extension.json"
test -f "$TARGET/.trellis/guru-team/schemas/closeout-plan.schema.json"
mkdir -p "$TARGET/.trellis/tasks/archive"
BACKFILL_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh" --root "$TARGET" --json --dry-run)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["mode"] == "dry-run"; assert payload["scanned_tasks"] == 0; assert payload["to_write"] == []; assert payload["skipped"] == []; assert payload["errors"] == []' <<<"$BACKFILL_JSON"
grep -q "def prepare_closeout" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
grep -q "def resolve_closeout_state" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
grep -q "def ensure_closeout_draft_pr" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
grep -q "If any stage fails, rerun this same entry with the same expected digest" "$TARGET/.agents/skills/trellis-finish-work/SKILL.md"
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
grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"

(
  cd "$TARGET"
  trellis update --force
)
(
  cd "$TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force
)
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$TARGET" \
  --platform codex \
  --platform cursor

grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"
test -f "$TARGET/.trellis/guru-team/schemas/finish-summary.schema.json"
test -f "$TARGET/.trellis/guru-team/schemas/closeout-plan.schema.json"
test -x "$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh"
BACKFILL_AFTER_UPDATE_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh" --root "$TARGET" --json --dry-run)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["mode"] == "dry-run"; assert payload["scanned_tasks"] == 0; assert payload["errors"] == []' <<<"$BACKFILL_AFTER_UPDATE_JSON"
grep -q '^session_auto_commit: false$' "$TARGET/.trellis/config.yaml"
grep -q '^\.trellis/workspace/$' "$TARGET/.gitignore"

FINAL_SIDECARS="$(find "$TARGET" -type f \( -name '*.new' -o -name '*.bak' \) -print)"
if [[ -n "$FINAL_SIDECARS" ]]; then
  echo "Unexpected .new/.bak sidecars after preview, switch, update, and preset reapply:" >&2
  printf '%s\n' "$FINAL_SIDECARS" >&2
  exit 2
fi

echo "Verified throwaway Guru Team Trellis install at $TARGET"
