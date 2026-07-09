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

"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$TARGET" \
  --platform codex \
  --platform cursor

test -f "$TARGET/.trellis/workflow.md"
grep -q "Guru Team Development Workflow" "$TARGET/.trellis/workflow.md"
grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"
grep -q 'required `prd.md`, `design.md`, and `implement.md`' "$TARGET/.trellis/workflow.md"
grep -q "record-subagent-liveness-event.sh" "$TARGET/.trellis/workflow.md"
grep -q "check-subagent-liveness.sh" "$TARGET/.trellis/workflow.md"
grep -q "dispatch_mode: sub-agent" "$TARGET/.trellis/config.yaml"
fail_if_english_language_rule ".trellis/spec" "$TARGET/.trellis/spec"
WORKSPACE_LANGUAGE_FILES=()
if [[ -f "$TARGET/.trellis/workspace/index.md" ]]; then
  WORKSPACE_LANGUAGE_FILES+=("$TARGET/.trellis/workspace/index.md")
fi
while IFS= read -r -d '' path; do
  WORKSPACE_LANGUAGE_FILES+=("$path")
done < <(find "$TARGET/.trellis/workspace" -mindepth 2 -maxdepth 2 -type f -name index.md -print0 2>/dev/null || true)
fail_if_english_language_rule ".trellis/workspace index files" "${WORKSPACE_LANGUAGE_FILES[@]}"
if [[ -d "$TARGET/.trellis/tasks/00-bootstrap-guidelines" ]]; then
  fail_if_english_language_rule "00-bootstrap-guidelines" "$TARGET/.trellis/tasks/00-bootstrap-guidelines"
fi
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-env.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/version.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-subagent-liveness.sh"
test -f "$TARGET/.trellis/guru-team/extension.json"
python3 -c 'import json, sys; payload = json.load(open(sys.argv[1], encoding="utf-8")); extension = payload["extension"]; api = extension["public_api"]; assert extension["extension_id"] == "guru-team"; assert extension["version"]; assert extension["target_trellis_cli"] == "0.6.5"; assert "agent-assignment.json" in api["artifact_contracts"]; assert "record-subagent-liveness-event" in api["companion_scripts"]; assert "check-subagent-liveness" in api["companion_scripts"]' "$TARGET/.trellis/guru-team/extension.json"
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
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "error"; assert payload["blocked_step"] == "publish-pr"; assert payload["recovery_flag"] == "--recovery-after-finish-work"' <<<"$PUBLISH_ERROR_JSON"

rm -f "$TARGET/.trellis/workflow.md.new"
(
  cd "$TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --create-new
)
test -f "$TARGET/.trellis/workflow.md.new"
grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md.new"
(
  cd "$TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force
)
grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"

echo "Verified throwaway Guru Team Trellis install at $TARGET"
