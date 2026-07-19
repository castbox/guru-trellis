#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

WORK_DIR="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
WORKFLOW_SOURCE="${TRELLIS_WORKFLOW_SOURCE:-gh:castbox/guru-trellis/trellis#main}"
ALLOW_PUBLIC_SAMPLE="${TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE:-0}"
OWNERSHIP_CHECK="$REPO_ROOT/trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh"
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

ownership_checkpoint() {
  local checkpoint="$1"
  printf 'Upstream ownership checkpoint: %s\n' "$checkpoint"
  "$OWNERSHIP_CHECK" --repo "$REPO_ROOT" --json
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

file_sha256() {
  python3 - "$1" <<'PY'
import hashlib
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.is_file():
    raise SystemExit(f"expected regular file: {path}")
print(hashlib.sha256(path.read_bytes()).hexdigest())
PY
}

assert_official_state_absent() {
  local root="$1"
  local label="$2"
  if [[ -e "$root/.trellis/.developer" || -e "$root/.trellis/workspace" ]]; then
    echo "Guru operation recreated official identity/workspace state during $label" >&2
    exit 2
  fi
}

verify_change_request_review_package() {
  local label="$1"
  printf 'Change request review package smoke: %s\n' "$label"
  python3 "$TARGET/.agents/skills/guru-review-change-request/tests/test_contract.py" -q
}

fail_if_python_cache() {
  local label="$1"
  local root="$2"
  local residue
  residue="$(find "$root" \( -type d -name '__pycache__' -o -type f \( -name '*.pyc' -o -name '*.pyo' \) \) -print)"
  if [[ -n "$residue" ]]; then
    echo "Unexpected Python cache residue in $label:" >&2
    printf '%s\n' "$residue" >&2
    exit 2
  fi
}

verify_requirements_clarification_exits() {
  local label="$1"
  local probe_dir="$WORK_DIR/requirements-clarification-$label"
  local fake_bin="$probe_dir/bin"
  mkdir -p "$probe_dir" "$fake_bin"
  cat >"$fake_bin/gh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" != "issue" || "${2:-}" != "view" ]]; then
  echo "unsupported throwaway gh invocation" >&2
  exit 2
fi

number="${3:-}"
case "$number" in
  7)
    state="${GURU_FAKE_ISSUE_7_STATE:-closed}"
    if [[ "$state" == "open" ]]; then
      updated_at="2026-01-01T00:00:02Z"
    else
      updated_at="2026-01-01T00:00:00Z"
    fi
    ;;
  8)
    state="open"
    updated_at="2026-01-01T00:00:00Z"
    ;;
  *)
    echo "unknown throwaway issue: $number" >&2
    exit 2
    ;;
esac

printf '{"number":%s,"url":"https://github.com/example/guru-extension/issues/%s","state":"%s","updatedAt":"%s","body":"Reviewed source issue body."}\n' \
  "$number" "$number" "$state" "$updated_at"
SH
  chmod +x "$fake_bin/gh"
  python3 - "$TARGET" "$probe_dir" <<'PY'
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
probe_dir = Path(sys.argv[2])
runtime = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
spec = importlib.util.spec_from_file_location("installed_requirements_clarification_runtime", runtime)
if spec is None or spec.loader is None:
    raise SystemExit(f"could not load installed clarification runtime: {runtime}")
gtt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gtt
spec.loader.exec_module(gtt)
example = json.loads(
    (root / ".agents/skills/guru-clarify-requirements/examples/requirements-clarification.json")
    .read_text(encoding="utf-8")
)
multiline_markdown = "# Clarification\n\n- first\tvalue\r\n- second"
issue_body = "Reviewed source issue body."


def derive(payload):
    return gtt.derive_requirements_clarification_result(payload)


def issue_target(payload, *, state="open"):
    payload = copy.deepcopy(payload)
    payload["invocation_context"] = {
        "kind": "initial_issue",
        "caller": "throwaway install",
        "task_locator": None,
        "resume_target": "guru-review-contract-wording",
    }
    projection = {
        "kind": "issue",
        "repo": "example/guru-extension",
        "issue_number": 7,
        "url": "https://github.com/example/guru-extension/issues/7",
        "state": state,
        "updated_at": "2026-01-01T00:00:00Z",
        "body_sha256": hashlib.sha256(issue_body.encode("utf-8")).hexdigest(),
    }
    payload["review_target"] = {
        **projection,
        "facts_sha256": gtt.context_digest(projection),
    }
    return payload


def candidate(number, decision):
    projection = {
        "repo": "example/guru-extension",
        "number": number,
        "identity": f"#{number}",
        "url": f"https://github.com/example/guru-extension/issues/{number}",
        "state": "open",
        "updated_at": "2026-01-01T00:00:00Z",
    }
    return {
        **projection,
        "facts_sha256": gtt.context_digest(projection),
        "decision": decision,
        "reason": "The candidate was compared with the reviewed delivery unit.",
    }


def disposition(
    payload,
    kind,
    *,
    candidates=None,
    selected_issue=None,
    original_target_role="primary",
    confirmation_ref=None,
):
    payload = copy.deepcopy(payload)
    payload["target_disposition"] = {
        "disposition": kind,
        "duplicate_query": "repo:example/guru-extension is:issue is:open reviewed target",
        "duplicate_checked_at": "2026-01-01T00:00:00Z",
        "duplicate_candidates": candidates or [],
        "duplicate_facts_sha256": "0" * 64,
        "selected_issue": selected_issue,
        "original_target_role": original_target_role,
        "decision_summary": f"The AI selected {kind} from the current evidence.",
        "confirmation_ref": confirmation_ref,
        "disposition_digest": "0" * 64,
    }
    return derive(payload)


def confirm(payload, *action_ids):
    payload = derive(payload)
    actions = {
        action["action_id"]: action
        for action in payload["source_actions"]
        if isinstance(action, dict)
    }
    payload["human_confirmation"] = {
        "status": "confirmed",
        "confirmation_kind": (
            "exact_source_action_and_target"
            if action_ids
            else "exact_target_disposition"
        ),
        "action_digest": (
            gtt.context_digest([
                actions[action_id]["action_digest"] for action_id in action_ids
            ])
            if action_ids
            else None
        ),
        "target_disposition_digest": payload["target_disposition"]["disposition_digest"],
        "proposal_digests": [],
        "confirmed_actions": list(action_ids),
        "confirmer": "throwaway-user",
        "confirmed_at": "2026-01-01T00:00:01Z",
        "evidence_summary": "The exact target disposition and actions were confirmed.",
    }
    return derive(payload)


def retarget(payload):
    selected_candidate = candidate(8, "selected")
    selected_issue = {
        "repo": selected_candidate["repo"],
        "issue_number": selected_candidate["number"],
        "url": selected_candidate["url"],
        "state": selected_candidate["state"],
        "updated_at": selected_candidate["updated_at"],
        "facts_sha256": selected_candidate["facts_sha256"],
    }
    payload = copy.deepcopy(payload)
    payload["typed_exit"] = "retarget_context"
    payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
    payload["source_actions"] = [{
        "action_id": "select_existing",
        "kind": "select_existing_issue",
        "target": {"repo": selected_candidate["repo"], "issue_number": 8},
        "payload": selected_issue,
        "preimage_sha256": payload["review_target"]["facts_sha256"],
        "payload_sha256": None,
        "action_digest": "0" * 64,
        "status": "validated",
        "mutation_evidence": None,
    }]
    payload = disposition(
        payload,
        "retarget_existing_issue",
        candidates=[selected_candidate],
        selected_issue=selected_issue,
        original_target_role="related",
        confirmation_ref="selected_target_confirmation",
    )
    return confirm(payload, "select_existing")


def reopened():
    payload = issue_target(example, state="closed")
    payload["typed_exit"] = "refresh_context"
    payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
    payload["source_actions"] = [{
        "action_id": "reopen_source",
        "kind": "reopen_issue",
        "target": {"repo": "example/guru-extension", "issue_number": 7},
        "payload": {"state": "open"},
        "preimage_sha256": payload["review_target"]["facts_sha256"],
        "payload_sha256": None,
        "action_digest": "0" * 64,
        "status": "executed",
        "mutation_evidence": {"source": "ai-reviewed-gh"},
    }]
    payload = disposition(
        payload,
        "reopen_closed_issue",
        confirmation_ref="reopen_target_confirmation",
    )
    action_digest = payload["source_actions"][0]["action_digest"]
    payload["mutation_results"] = [{
        "action_id": "reopen_source",
        "kind": "reopen_issue",
        "status": "succeeded",
        "url": payload["review_target"]["url"],
        "state": "open",
        "updated_at": "2026-01-01T00:00:02Z",
        "content_sha256": payload["review_target"]["body_sha256"],
        "action_digest": action_digest,
        "facts_sha256": "0" * 64,
    }]
    return confirm(payload, "reopen_source")


def followup(body=multiline_markdown):
    payload = issue_target(example, state="closed")
    payload["typed_exit"] = "new_task"
    payload["consumer"] = {"kind": "workflow", "id": "guru-full-task-intake-chain"}
    payload["source_actions"] = [{
        "action_id": "new_issue",
        "kind": "new_issue_draft",
        "target": {"repo": "example/guru-extension"},
        "payload": {"title": "Independent follow-up delivery", "body": body},
        "preimage_sha256": None,
        "payload_sha256": None,
        "action_digest": "0" * 64,
        "status": "draft_ready",
        "mutation_evidence": None,
    }]
    payload = disposition(
        payload,
        "create_followup_draft",
        original_target_role="related",
        confirmation_ref="followup_target_confirmation",
    )
    return confirm(payload, "new_issue")


def complete():
    payload = issue_target(example, state="closed")
    payload["typed_exit"] = "blocked"
    payload["consumer"] = {"kind": "stop", "id": "requirements-clarification-blocked"}
    payload["ai_review_gate"]["status"] = "blocked"
    payload["error"] = {
        "codes": ["requirements_target_complete"],
        "summary": "The closed target is complete and no independent gap remains.",
    }
    payload = disposition(
        payload,
        "block_target_complete",
        original_target_role="reference",
        confirmation_ref="complete_target_confirmation",
    )
    return confirm(payload)


def add_authority_round(payload, *, impact, action_ids):
    payload = copy.deepcopy(payload)
    payload["clarification_rounds"] = [{
        "round_id": "round_authority",
        "question_id": "acceptance_boundary",
        "atomic_group_id": None,
        "atomic_group_reason": None,
        "category": "product_intent",
        "question": "Which acceptance boundary is authoritative?",
        "answer_summary": "The user confirmed the exact acceptance boundary.",
        "answer_status": "complete",
        "authority_impact": impact,
        "authority_action_ids": action_ids,
        "affected_contracts": ["acceptance criteria"],
        "opened_question_ids": ["acceptance_boundary"],
        "closed_question_ids": ["acceptance_boundary"],
    }]
    payload["open_questions"] = []
    return derive(payload)


def issue_authority(kind):
    body = f"Confirmed load-bearing authority through {kind}."
    payload = issue_target(example, state="open")
    payload["typed_exit"] = "refresh_context"
    payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
    payload["source_actions"] = [{
        "action_id": "persist_authority",
        "kind": kind,
        "target": {"repo": "example/guru-extension", "issue_number": 7},
        "payload": {"body": body},
        "preimage_sha256": payload["review_target"]["body_sha256"],
        "payload_sha256": None,
        "action_digest": "0" * 64,
        "status": "executed",
        "mutation_evidence": {"source": "ai-reviewed-gh"},
    }]
    payload = disposition(payload, "keep_current_open_issue")
    action_digest = payload["source_actions"][0]["action_digest"]
    payload["human_confirmation"] = {
        "status": "confirmed",
        "confirmation_kind": "exact_source_action",
        "action_digest": gtt.context_digest([action_digest]),
        "target_disposition_digest": None,
        "proposal_digests": [],
        "confirmed_actions": ["persist_authority"],
        "confirmer": "throwaway-user",
        "confirmed_at": "2026-01-01T00:00:01Z",
        "evidence_summary": "The exact authority mutation was confirmed.",
    }
    url = payload["review_target"]["url"]
    if kind == "issue_comment":
        url += "#issuecomment-99"
    payload["mutation_results"] = [{
        "action_id": "persist_authority",
        "kind": kind,
        "status": "succeeded",
        "url": url,
        "state": "open",
        "updated_at": "2026-01-01T00:00:02Z",
        "content_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "action_digest": action_digest,
        "facts_sha256": "0" * 64,
    }]
    return add_authority_round(
        payload,
        impact="load_bearing",
        action_ids=["persist_authority"],
    )


def draft_authority():
    body = "The proposed draft persists the load-bearing acceptance boundary."
    payload = copy.deepcopy(example)
    payload["typed_exit"] = "refresh_context"
    payload["consumer"] = {"kind": "skill", "id": "guru-sync-base"}
    payload["review_target"]["body_sha256"] = hashlib.sha256(body.encode("utf-8")).hexdigest()
    payload["source_actions"] = [{
        "action_id": "persist_draft",
        "kind": "proposed_draft_update",
        "target": {"repo": "example/guru-extension"},
        "payload": {"title": "Clarified draft", "body": body},
        "preimage_sha256": "1" * 64,
        "payload_sha256": None,
        "action_digest": "0" * 64,
        "status": "validated",
        "mutation_evidence": None,
    }]
    payload = derive(payload)
    action_digest = payload["source_actions"][0]["action_digest"]
    payload["human_confirmation"] = {
        "status": "confirmed",
        "confirmation_kind": "exact_source_action",
        "action_digest": gtt.context_digest([action_digest]),
        "target_disposition_digest": None,
        "proposal_digests": [],
        "confirmed_actions": ["persist_draft"],
        "confirmer": "throwaway-user",
        "confirmed_at": "2026-01-01T00:00:01Z",
        "evidence_summary": "The exact proposed draft update was confirmed.",
    }
    payload["mutation_results"] = [{
        "action_id": "persist_draft",
        "kind": "proposed_draft_update",
        "status": "succeeded",
        "url": None,
        "state": "draft",
        "updated_at": None,
        "content_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "action_digest": action_digest,
        "facts_sha256": "0" * 64,
    }]
    return add_authority_round(
        payload,
        impact="load_bearing",
        action_ids=["persist_draft"],
    )


def assert_structural(label, payload):
    errors = gtt.requirements_clarification_structural_errors(root, payload, None)
    if errors:
        raise SystemExit(f"installed {label} fixture failed: {errors}")

clear = derive(example)
needs_context = copy.deepcopy(clear)
needs_context["typed_exit"] = "needs_context"
needs_context["consumer"] = {"kind": "skill", "id": "guru-discover-change-context"}
needs_context["context_evidence"] = {
    "status": "missing", "schema_id": None, "snapshot_sha256": None,
    "evidence_refs": ["repository evidence"],
    "missing_reason": "Current repository context is unavailable.",
}
cases = {
    "clear": clear,
    "needs_context": derive(needs_context),
    "refresh_context": reopened(),
    "retarget_context": retarget(example),
    "new_task": followup(),
    "blocked": complete(),
}

# The clean install exercises the complete #139 normal-path scenario matrix
# against the installed runtime, while the wrapper loop below verifies every
# public exit through its recorder and checker.
rejected = candidate(8, "rejected")
retain_draft = disposition(
    example,
    "keep_current_draft",
    candidates=[rejected],
    confirmation_ref="retain_draft_confirmation",
)
retain_draft = confirm(retain_draft)
retain_issue = disposition(
    issue_target(example),
    "keep_current_open_issue",
    candidates=[rejected],
    confirmation_ref="retain_issue_confirmation",
)
retain_issue = confirm(retain_issue)
open_without_duplicate = disposition(
    issue_target(example),
    "keep_current_open_issue",
)
matrix = {
    "draft_duplicate_retain": retain_draft,
    "draft_duplicate_retarget": cases["retarget_context"],
    "issue_duplicate_retain": retain_issue,
    "issue_duplicate_retarget": retarget(issue_target(example)),
    "open_issue_without_duplicate": open_without_duplicate,
    "closed_issue_reopen": cases["refresh_context"],
    "closed_issue_followup": cases["new_task"],
    "closed_issue_complete": cases["blocked"],
    "issue_load_bearing_comment": issue_authority("issue_comment"),
    "issue_load_bearing_body_edit": issue_authority("issue_body_edit"),
    "draft_load_bearing_update": draft_authority(),
}
for scenario, payload in matrix.items():
    assert_structural(scenario, payload)

illegal_load_bearing = add_authority_round(
    example,
    impact="load_bearing",
    action_ids=[],
)
illegal_errors = gtt.requirements_clarification_structural_errors(
    root, illegal_load_bearing, None
)
for code in (
    "load_bearing_round_requires_authority_action",
    "load_bearing_authority_update_requires_refresh_context",
):
    if code not in illegal_errors:
        raise SystemExit(f"installed load-bearing none+clear did not fail with {code}")
non_load_bearing = add_authority_round(
    example,
    impact="non_load_bearing",
    action_ids=[],
)
assert_structural("non_load_bearing_without_mutation", non_load_bearing)

refresh_without_disposition = copy.deepcopy(matrix["draft_load_bearing_update"])
refresh_without_disposition["target_disposition"] = None
refresh_without_disposition = derive(refresh_without_disposition)
if "requirements_target_disposition_required" not in gtt.requirements_clarification_structural_errors(
    root, refresh_without_disposition, None
):
    raise SystemExit("installed authority refresh accepted a missing target disposition")

wrong_confirmation = copy.deepcopy(cases["retarget_context"])
wrong_confirmation["human_confirmation"]["target_disposition_digest"] = "f" * 64
wrong_confirmation = derive(wrong_confirmation)
if "target_disposition_requires_exact_confirmation" not in gtt.requirements_clarification_structural_errors(
    root, wrong_confirmation, None
):
    raise SystemExit("installed retarget fixture accepted stale target confirmation")

stale_action = copy.deepcopy(cases["retarget_context"])
stale_action["source_actions"][0]["payload"]["updated_at"] = "2026-01-01T00:00:09Z"
stale_action = derive(stale_action)
if "select_existing_issue_action_binding_invalid" not in gtt.requirements_clarification_structural_errors(
    root, stale_action, None
):
    raise SystemExit("installed retarget fixture accepted stale selected action")

legacy = copy.deepcopy(example)
legacy["schema_version"] = "1.0"
(probe_dir / "legacy.input.json").write_text(
    json.dumps(legacy, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

for typed_exit, payload in cases.items():
    (probe_dir / f"{typed_exit}.input.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
PY

  local typed_exit input result result_sha
  for typed_exit in clear needs_context refresh_context retarget_context new_task blocked; do
    input="$probe_dir/$typed_exit.input.json"
    result="$probe_dir/$typed_exit.result.json"
    if [[ "$typed_exit" == "refresh_context" ]]; then
      export GURU_FAKE_ISSUE_7_STATE="open"
    else
      export GURU_FAKE_ISSUE_7_STATE="closed"
    fi
    PATH="$fake_bin:$PATH" "$TARGET/.agents/skills/guru-clarify-requirements/scripts/record-requirements-clarification.sh" \
      --root "$TARGET" --json --mode standalone --input "$input" >"$result"
    result_sha="$(python3 -c 'import json, sys; payload=json.load(open(sys.argv[1], encoding="utf-8")); assert payload["typed_exit"] == sys.argv[2]; print(payload["content_identity"]["result_sha256"])' "$result" "$typed_exit")"
    PATH="$fake_bin:$PATH" "$TARGET/.agents/skills/guru-clarify-requirements/scripts/check-requirements-clarification.sh" \
      --root "$TARGET" --json --input "$result" \
      --expected-result-sha256 "$result_sha" >/dev/null
  done
  unset GURU_FAKE_ISSUE_7_STATE

  local legacy_error
  legacy_error="$probe_dir/legacy.error.json"
  if PATH="$fake_bin:$PATH" "$TARGET/.agents/skills/guru-clarify-requirements/scripts/check-requirements-clarification.sh" \
    --root "$TARGET" --json --input "$probe_dir/legacy.input.json" >"$legacy_error" 2>&1; then
    echo "Installed clarification checker accepted legacy schema 1.0" >&2
    exit 2
  fi
  grep -q 'requirements_clarification_legacy_schema_requires_refresh' "$legacy_error"
}

verify_contract_wording_standalone_profiles() {
  local label="$1"
  local probe_dir="$WORK_DIR/contract-wording-$label"
  local explicit_rel="docs/contract-wording-$label.md"
  local draft_rel="docs/contract-wording-$label-draft.json"
  mkdir -p "$probe_dir" "$TARGET/docs"
  printf '# Contract wording\n\n建议保留为已定义术语。\n' >"$TARGET/$explicit_rel"
  cat >"$TARGET/$draft_rel" <<'JSON'
{
  "kind": "draft",
  "draft_id": "throwaway-contract-wording",
  "title": "Exact contract wording title",
  "body": "建议保留为已定义术语。",
  "selected_comments": []
}
JSON
  python3 - "$TARGET" "$probe_dir" "$explicit_rel" "$draft_rel" <<'PY'
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
probe_dir = Path(sys.argv[2])
explicit_rel = sys.argv[3]
draft_rel = sys.argv[4]
runtime = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
spec = importlib.util.spec_from_file_location("installed_contract_wording_runtime", runtime)
if spec is None or spec.loader is None:
    raise SystemExit(f"could not load installed contract wording runtime: {runtime}")
gtt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gtt
spec.loader.exec_module(gtt)

cases = {
    "explicit_paths": gtt.contract_wording_build_scope(
        root, "explicit_paths", "standalone", explicit_paths=[explicit_rel]
    ),
    "change_request": gtt.contract_wording_build_scope(
        root, "change_request", "standalone", change_request_input=draft_rel
    ),
}
for profile, (scope, contents) in cases.items():
    scan = gtt.scan_contract_wording(scope, contents)
    authored = {
        "generated_at": "2026-07-17T00:00:00Z",
        "semantic_review": {
            "revisions": [],
            "classifications": [
                {
                    "hit_id": hit["hit_id"],
                    "classification": "term_definition",
                    "reason": "Throwaway semantic review confirms this retained wording is an explicit term definition.",
                }
                for hit in scan["hits"]
            ],
            "ai_review_gate": {
                "status": "passed",
                "reviewer": "throwaway-contract-wording-review",
                "summary": "The complete current throwaway scope and deterministic scan were reviewed.",
                "reviewed_scan_sha256": scan["scan_sha256"],
                "checked_dimensions": {
                    name: True for name in gtt.CONTRACT_WORDING_REVIEW_DIMENSIONS
                },
            },
        },
        "human_confirmation": {
            "status": "not_required",
            "confirmed_by": None,
            "confirmed_at": None,
            "reason": "No content mutation is required for this throwaway profile smoke.",
        },
        "typed_exit": "pass",
    }
    (probe_dir / f"{profile}.input.json").write_text(
        json.dumps(authored, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

issue_rel = f"docs/contract-wording-{probe_dir.name}-issue.json"
(root / issue_rel).write_text(json.dumps({
    "kind": "issue",
    "repo": "castbox/guru-trellis",
    "number": 114,
    "selected_comments": [],
}), encoding="utf-8")
live_issue = {
    "title": "Exact live issue title",
    "body": "Exact rewritten live issue body",
    "url": "https://github.com/castbox/guru-trellis/issues/114",
    "updatedAt": "2026-07-17T08:00:00Z",
    "comments": [],
}
original_auth = gtt.require_gh_auth
original_view = gtt.issue_view
gtt.require_gh_auth = lambda _root: None
gtt.issue_view = lambda _repo, _number, _root: live_issue
try:
    live_scope, live_contents = gtt.contract_wording_build_scope(
        root, "change_request", "standalone", change_request_input=issue_rel
    )
finally:
    gtt.require_gh_auth = original_auth
    gtt.issue_view = original_view
live_scan = gtt.scan_contract_wording(live_scope, live_contents)
body_item = next(item for item in live_scope["items"] if item["field"] == "body")
payload_fact = {
    "source_identity": body_item["source_identity"],
    "locator": body_item["id"],
    "field": "body",
    "preimage_sha256": "0" * 64,
    "content_sha256": body_item["content_sha256"],
}
live_result = gtt.contract_wording_derive_result(
    "change_request",
    "standalone",
    live_scope,
    live_scan,
    {
        "generated_at": "2026-07-17T08:01:00Z",
        "semantic_review": {
            "revisions": [{
                "revision_id": "throwaway-live-revision",
                "locator": body_item["id"],
                "before_sha256": "0" * 64,
                "after_sha256": body_item["content_sha256"],
                "reason": "The installed runtime binds the exact live issue rewrite.",
                "mutation_authority": "The exact payload was confirmed before the live mutation.",
                "rescan_sha256": live_scan["scan_sha256"],
                "change_request_mutation": {
                    "source_identity": body_item["source_identity"],
                    "locator": body_item["id"],
                    "field": "body",
                    "preimage_sha256": "0" * 64,
                    "confirmed_content_sha256": body_item["content_sha256"],
                    "reread_content_sha256": body_item["content_sha256"],
                    "source_updated_at": body_item["updated_at"],
                },
            }],
            "classifications": [],
            "ai_review_gate": {
                "status": "passed",
                "reviewer": "throwaway-live-mutation-review",
                "summary": "The installed runtime reviewed the exact confirmed payload and current reread result.",
                "reviewed_scan_sha256": live_scan["scan_sha256"],
                "checked_dimensions": {
                    name: True for name in gtt.CONTRACT_WORDING_REVIEW_DIMENSIONS
                },
            },
        },
        "human_confirmation": {
            "status": "confirmed",
            "confirmed_by": "throwaway-user",
            "confirmed_at": "2026-07-17T07:59:00Z",
            "reason": "The exact live issue payload was confirmed.",
            "confirmed_payload_sha256": gtt.context_digest([gtt.context_digest(payload_fact)]),
        },
        "typed_exit": "content_changed",
    },
)
assert gtt.contract_wording_structural_errors(root, live_result, live_scope, live_scan) == []

missing_comment_rel = f"docs/contract-wording-{probe_dir.name}-missing-comment.json"
(root / missing_comment_rel).write_text(json.dumps({
    "kind": "draft",
    "draft_id": "throwaway-missing-comment-metadata",
    "title": "Exact title",
    "body": "Exact body",
    "selected_comments": [{
        "id": "comment-1",
        "author": None,
        "updated_at": "2026-07-17T00:00:00Z",
        "selection_reason": "This comment is authoritative.",
        "body": "Exact comment body.",
    }],
}), encoding="utf-8")
try:
    gtt.contract_wording_build_scope(
        root, "change_request", "standalone", change_request_input=missing_comment_rel
    )
except gtt.WorkflowError:
    pass
else:
    raise AssertionError("installed runtime accepted selected comment without author")
PY

  local profile input result facts
  for profile in explicit_paths change_request; do
    input="$probe_dir/$profile.input.json"
    result="$probe_dir/$profile.result.json"
    if [[ "$profile" == "explicit_paths" ]]; then
      "$TARGET/.agents/skills/guru-review-contract-wording/scripts/record-contract-wording-review.sh" \
        --root "$TARGET" --json --mode standalone --profile "$profile" \
        --path "$explicit_rel" --input "$input" >"$result"
      facts="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["facts_sha256"])' "$result")"
      "$TARGET/.agents/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh" \
        --root "$TARGET" --json --input "$result" --path "$explicit_rel" \
        --expected-facts-sha256 "$facts" >/dev/null
    else
      "$TARGET/.agents/skills/guru-review-contract-wording/scripts/record-contract-wording-review.sh" \
        --root "$TARGET" --json --mode standalone --profile "$profile" \
        --change-request-input "$draft_rel" --input "$input" >"$result"
      facts="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["facts_sha256"])' "$result")"
      "$TARGET/.agents/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh" \
        --root "$TARGET" --json --input "$result" --change-request-input "$draft_rel" \
        --expected-facts-sha256 "$facts" >/dev/null
    fi
    python3 -c 'import json,sys; payload=json.load(open(sys.argv[1], encoding="utf-8")); assert payload["profile"] == sys.argv[2]; assert payload["typed_exit"] == "pass"; assert "planning_checked_dimensions" not in payload["semantic_review"]["ai_review_gate"]' "$result" "$profile"
  done
}

record_planning_contract_wording() {
  local task_rel="$1"
  local probe_dir="$WORK_DIR/contract-wording-planning"
  local input="$probe_dir/planning_artifacts.input.json"
  local changed_input="$probe_dir/planning_artifacts.content_changed.input.json"
  local bytes_before="$probe_dir/planning_artifacts.bytes.json"
  mkdir -p "$probe_dir"
  python3 - "$TARGET" "$task_rel" "$input" "$changed_input" "$bytes_before" <<'PY'
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
task_rel = sys.argv[2]
output = Path(sys.argv[3])
changed_output = Path(sys.argv[4])
bytes_output = Path(sys.argv[5])
runtime = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
spec = importlib.util.spec_from_file_location("installed_planning_wording_runtime", runtime)
if spec is None or spec.loader is None:
    raise SystemExit(f"could not load installed planning wording runtime: {runtime}")
gtt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gtt
spec.loader.exec_module(gtt)
scope, contents = gtt.contract_wording_build_scope(
    root, "planning_artifacts", "workflow", task_dir=root / task_rel
)
scan = gtt.scan_contract_wording(scope, contents)
gate = {
    "status": "passed",
    "reviewer": "throwaway-planning-wording-review",
    "summary": "The fixed three-file planning scope and complete current scan were reviewed.",
    "reviewed_scan_sha256": scan["scan_sha256"],
    "checked_dimensions": {
        name: True for name in gtt.CONTRACT_WORDING_REVIEW_DIMENSIONS
    },
    "planning_checked_dimensions": {
        name: True
        for name in gtt.CONTRACT_WORDING_PLANNING_REVIEW_DIMENSIONS
    },
}
classifications = [
    {
        "hit_id": hit["hit_id"],
        "classification": "term_definition",
        "reason": "Throwaway planning review confirms this retained wording is explicitly defined.",
    }
    for hit in scan["hits"]
]
authored = {
    "generated_at": "2026-07-17T00:00:01Z",
    "semantic_review": {
        "revisions": [],
        "classifications": classifications,
        "ai_review_gate": gate,
    },
    "human_confirmation": {
        "status": "not_required",
        "confirmed_by": None,
        "confirmed_at": None,
        "reason": "The complete re-entry requires no further content mutation.",
    },
    "typed_exit": "pass",
}
first = scope["items"][0]
changed_authored = {
    "generated_at": "2026-07-17T00:00:00Z",
    "semantic_review": {
        "revisions": [{
            "revision_id": "throwaway-planning-content-change",
            "locator": first["path"],
            "before_sha256": "0" * 64,
            "after_sha256": first["content_sha256"],
            "reason": "The authorized wording rewrite is already reflected in current bytes.",
            "mutation_authority": "The throwaway workflow authorized this planning wording rewrite.",
            "rescan_sha256": scan["scan_sha256"],
        }],
        "classifications": [
            dict(row) for row in classifications
        ],
        "ai_review_gate": dict(gate),
    },
    "human_confirmation": {
        "status": "not_required",
        "confirmed_by": None,
        "confirmed_at": None,
        "reason": "The authorized rewrite did not require a separate confirmation.",
    },
    "typed_exit": "content_changed",
}
output.write_text(json.dumps(authored, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
changed_output.write_text(
    json.dumps(changed_authored, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
bytes_output.write_text(
    json.dumps({
        name: (root / task_rel / name).read_bytes().hex()
        for name in gtt.CONTRACT_WORDING_PLANNING_SCOPE
    }, sort_keys=True) + "\n",
    encoding="utf-8",
)
PY
  "$TARGET/.agents/skills/guru-review-contract-wording/scripts/record-contract-wording-review.sh" \
    --root "$TARGET" --json --mode workflow --profile planning_artifacts \
    --task "$task_rel" --input "$changed_input" >/dev/null
  "$TARGET/.agents/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh" \
    --root "$TARGET" --json --task "$task_rel" >/dev/null
  local prior_facts
  prior_facts="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["facts_sha256"])' "$TARGET/$task_rel/contract-wording-review.json")"
  "$TARGET/.agents/skills/guru-review-contract-wording/scripts/record-contract-wording-review.sh" \
    --root "$TARGET" --json --mode workflow --profile planning_artifacts \
    --task "$task_rel" --input "$input" \
    --supersede-reentry-facts-sha256 "$prior_facts" >/dev/null
  "$TARGET/.agents/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh" \
    --root "$TARGET" --json --task "$task_rel" >/dev/null
  python3 - "$TARGET/$task_rel/contract-wording-review.json" "$TARGET" "$task_rel" "$bytes_before" <<'PY'
import json
import sys

payload = json.load(open(sys.argv[1], encoding="utf-8"))
root = __import__("pathlib").Path(sys.argv[2])
task_rel = sys.argv[3]
before = json.load(open(sys.argv[4], encoding="utf-8"))
assert payload["typed_exit"] == "pass"
assert payload["semantic_review"]["revisions"] == []
assert before == {
    name: (root / task_rel / name).read_bytes().hex()
    for name in ("prd.md", "design.md", "implement.md")
}
dimensions = payload["semantic_review"]["ai_review_gate"]["planning_checked_dimensions"]
assert set(dimensions) == {
    "no_requirement_weakening",
    "source_issue_semantics_preserved",
    "conditional_paths_have_conditions",
    "no_parallel_implementation_paths",
    "gates_have_machine_verifiable_conditions",
    "acceptance_criteria_are_deterministic",
    "external_quotes_are_labeled_non_contract",
}
assert all(value is True for value in dimensions.values())
PY
}

record_and_check_planning_approval() {
  local task_rel="$1"
  local phase="$2"
  local input="$WORK_DIR/planning-approval-$phase.input.json"
  local result="$WORK_DIR/planning-approval-$phase.result.json"
  python3 - "$TARGET" "$task_rel" "$input" "$phase" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
task_rel = sys.argv[2]
output = Path(sys.argv[3])
phase = sys.argv[4]
task_dir = root / task_rel
prd_heading = next(
    line.lstrip("#").strip()
    for line in (task_dir / "prd.md").read_text(encoding="utf-8").splitlines()
    if line.startswith("#")
)
authored = {
    "mode": "workflow",
    "requirement_authorities": [{
        "id": f"throwaway-{phase}-prd",
        "kind": "task_artifact",
        "locator": f"{task_rel}/prd.md",
        "sha256": "0" * 64,
        "updated_at": None,
    }],
    "docs_ssot_plan": {
        "strategy": "ssot_first",
        "artifact_path": "design.md",
        "locator": "Docs SSOT Plan",
        "statement_sha256": "0" * 64,
        "durable_paths": [".trellis/workflow.md"],
    },
    "provenance_review": {
        "entries": [{
            "id": f"throwaway-{phase}-requirement",
            "artifact_path": "prd.md",
            "locator": prd_heading,
            "statement_sha256": "0" * 64,
            "classification": "explicit_requirement",
            "authority_refs": [f"throwaway-{phase}-prd"],
            "reason": "The throwaway task explicitly requires the installed planning path.",
            "implementation_choice": None,
            "scope_expansion": None,
            "out_of_scope_proposal": None,
        }],
        "coverage": {
            "reviewer": "throwaway-planning-review",
            "summary": "All load-bearing throwaway planning statements were reviewed.",
            "reviewed_entry_ids": [f"throwaway-{phase}-requirement"],
            "all_load_bearing_items_covered": True,
            "review_sha256": "0" * 64,
        },
    },
    "unusual_scenario_review": {
        "reviewer": "throwaway-planning-review",
        "summary": "No unusual scenario proposal is required by this disposable task.",
        "candidates": [],
        "unresolved_count": 0,
        "review_sha256": "0" * 64,
    },
    "semantic_review": {"ai_review_gate": {
        "status": "passed",
        "reviewer": "throwaway-planning-review",
        "summary": "The installed planning package may activate this disposable task.",
        "reviewed_at": "2026-07-19T00:00:00Z",
        "findings": [],
        "revision_actions": [],
        "scope_proposals": [],
        "blocking_reasons": [],
    }},
    "user_confirmation": {
        "kind": "post-planning-approval",
        "status": "confirmed",
        "prompt_presented_at": "2026-07-19T00:01:00Z",
        "confirmed_at": "2026-07-19T00:02:00Z",
        "evidence_summary": "The disposable fixture explicitly confirms its three planning documents.",
    },
    "typed_exit": "approved",
    "consumer": {"kind": "workflow", "id": "phase-1-task-activation"},
    "reason": "The installed v2 recorder and checker path is under test.",
    "supersedes_facts_sha256": None,
}
output.write_text(
    json.dumps(authored, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY
  "$TARGET/.agents/skills/guru-approve-task-plan/scripts/record-planning-approval.sh" \
    --root "$TARGET" --json --task "$task_rel" --input "$input" >"$result"
  "$TARGET/.agents/skills/guru-approve-task-plan/scripts/check-planning-approval.sh" \
    --root "$TARGET" --json --task "$task_rel" --require-exit approved >/dev/null
  python3 -c 'import json,sys; payload=json.load(open(sys.argv[1], encoding="utf-8")); assert payload["schema_version"] == "2.0"; assert payload["skill_id"] == "guru-approve-task-plan"; assert payload["typed_exit"] == "approved"; assert payload["dry_run"] is False' "$result"
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
  local target="${1:-$TARGET}"
  if [[ "$USE_LOCAL_WORKFLOW_SAMPLE" == "1" ]]; then
    cp "$REPO_ROOT/trellis/workflows/guru-team/workflow.md" "$target/.trellis/workflow.md"
  fi
}

mkdir "$TARGET"
git -C "$TARGET" init -q
git -C "$TARGET" remote add origin https://github.com/castbox/guru-trellis-throwaway.git
git -C "$TARGET" config user.name "Guru Team Throwaway Bootstrap"
git -C "$TARGET" config user.email "guru-team-throwaway-bootstrap@example.invalid"
git -C "$TARGET" branch -M main
printf '%s\n' 'throwaway repository baseline' >"$TARGET/.throwaway-baseline"
git -C "$TARGET" add .throwaway-baseline
git -C "$TARGET" commit -q -m "chore: initialize throwaway repository"

(
  cd "$TARGET"
  trellis init -y --claude --codex --cursor \
    --workflow guru-team \
    --workflow-source "$WORKFLOW_SOURCE"
)
apply_local_workflow_sample
if [[ "$USE_LOCAL_WORKFLOW_SAMPLE" == "1" ]]; then
  cmp -s "$REPO_ROOT/trellis/workflows/guru-team/workflow.md" "$TARGET/.trellis/workflow.md"
fi

ownership_checkpoint "initial-init-before-preset-apply"

test -f "$TARGET/.trellis/.developer"
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
DEVELOPER_IDENTITY_DIGEST_BEFORE="$(file_sha256 "$TARGET/.trellis/.developer")"

"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$TARGET" \
  --platform claude \
  --platform codex \
  --platform cursor

test -f "$TARGET/.trellis/workflow.md"
grep -q "Guru Team Development Workflow" "$TARGET/.trellis/workflow.md"
grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"
grep -q 'Guru Team implementation tasks require `prd.md`, `design.md`, and `implement.md`' "$TARGET/.trellis/workflow.md"
grep -q "record-subagent-liveness-event.sh" "$TARGET/.trellis/workflow.md"
grep -q "check-subagent-liveness.sh" "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-sync-base","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-discover-change-context","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-discover-change-context","exit":"context_ready","consumer":{"kind":"skill","id":"guru-clarify-requirements"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-discover-change-context","exit":"refresh_base","consumer":{"kind":"skill","id":"guru-sync-base"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-discover-change-context","exit":"blocked","consumer":{"kind":"stop","id":"change-context-blocked"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-clarify-requirements","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"clear","consumer":{"kind":"workflow","id":"guru-requirements-clear-router"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"needs_context","consumer":{"kind":"skill","id":"guru-discover-change-context"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"refresh_context","consumer":{"kind":"skill","id":"guru-sync-base"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"retarget_context","consumer":{"kind":"skill","id":"guru-sync-base"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"new_task","consumer":{"kind":"workflow","id":"guru-full-task-intake-chain"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"blocked","consumer":{"kind":"stop","id":"requirements-clarification-blocked"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-review-contract-wording","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-contract-wording","exit":"pass","consumer":{"kind":"workflow","id":"guru-contract-wording-pass-router"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-contract-wording","exit":"content_changed","consumer":{"kind":"workflow","id":"guru-contract-wording-change-router"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-contract-wording","exit":"blocked","consumer":{"kind":"stop","id":"contract-wording-blocked"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-review-change-request","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"ready","consumer":{"kind":"skill","id":"guru-create-task-workspace"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"clarify_requirements","consumer":{"kind":"skill","id":"guru-clarify-requirements"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"review_wording","consumer":{"kind":"skill","id":"guru-review-contract-wording"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"refresh_context","consumer":{"kind":"skill","id":"guru-sync-base"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"blocked","consumer":{"kind":"stop","id":"change-request-review-blocked"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-create-task-workspace","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"created","consumer":{"kind":"workflow","id":"guru-task-workspace-created"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"refresh_review","consumer":{"kind":"skill","id":"guru-sync-base"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"cancelled","consumer":{"kind":"stop","id":"task-workspace-cancelled"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"blocked","consumer":{"kind":"stop","id":"task-workspace-blocked"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-stop-target: {"id":"change-request-review-blocked"}' "$TARGET/.trellis/workflow.md"
if grep -Eq 'guru-skill-exit: \{"skill":"guru-review-change-request"[^\n]*"id":"guru-full-task-intake-chain"' "$TARGET/.trellis/workflow.md"; then
  echo "Change request readiness retained the legacy full-intake fallback" >&2
  exit 2
fi
grep -q "dispatch_mode: sub-agent" "$TARGET/.trellis/config.yaml"
fail_if_english_language_rule ".trellis/spec" "$TARGET/.trellis/spec"
WORKSPACE_TREE_DIGEST_AFTER="$(workspace_tree_digest "$TARGET/.trellis/workspace")"
if [[ "$WORKSPACE_TREE_DIGEST_AFTER" != "$WORKSPACE_TREE_DIGEST_BEFORE" ]]; then
  echo "Preset modified .trellis/workspace content" >&2
  exit 2
fi
if [[ "$(file_sha256 "$TARGET/.trellis/.developer")" != "$DEVELOPER_IDENTITY_DIGEST_BEFORE" ]]; then
  echo "Preset modified .trellis/.developer content" >&2
  exit 2
fi
if [[ -d "$TARGET/.trellis/tasks/00-bootstrap-guidelines" ]]; then
  fail_if_english_language_rule "00-bootstrap-guidelines" "$TARGET/.trellis/tasks/00-bootstrap-guidelines"
fi
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-env.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/version.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/run-skill-command.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/sync-base.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-base-sync.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/preview-change-context-history.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-context-discovery.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-context-discovery.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-requirements-clarification.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-requirements-clarification.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-contract-wording-review.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-contract-wording-review.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-change-request-review.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-change-request-review.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-task-workspace-plan.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/create-task-workspace.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-task-workspace-result.sh"
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
assert extension["version"] == "0.6.5-guru.17"
assert extension["target_trellis_cli"] == "0.6.5"
assert assets == sorted(set(assets))
assert len(assets) == 88
assert all((root / path).is_file() for path in assets)
for artifact in (
    "agent-assignment.json", "pr-body.md", "closeout-plan.json",
    "finish-summary.json", "task-commit-plans/*.json",
    "context-discovery.json", "issue-review.json",
):
    assert artifact in api["artifact_contracts"]
for command in (
    "resolve-human-artifacts", "record-subagent-liveness-event",
    "check-subagent-liveness", "check-commit-messages",
    "create-task-commit", "run-skill-command", "sync-base", "check-base-sync",
    "preview-change-context-history", "record-context-discovery", "check-context-discovery",
    "record-requirements-clarification", "check-requirements-clarification",
    "record-contract-wording-review", "check-contract-wording-review",
    "record-change-request-review", "check-change-request-review",
    "record-task-workspace-plan", "create-task-workspace", "check-task-workspace-result",
    "record-planning-approval", "check-planning-approval",
    "record-phase2-check", "check-phase2-check",
    "format-merge-commit",
    "backfill-finish-summary", "check-skill-packages",
):
    assert command in api["companion_scripts"]
assert api["skill_contracts"]["canonical_root"] == "trellis/skills/guru-team/"
assert api["skill_contracts"]["active_skill_ids"] == ["guru-approve-task-plan", "guru-check-task", "guru-clarify-requirements", "guru-create-task-commit", "guru-create-task-workspace", "guru-discover-change-context", "guru-review-change-request", "guru-review-contract-wording", "guru-sync-base"]
assert api["skill_contracts"]["planned_skill_ids"] == []
assert "guru-base-sync-result-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-context-discovery-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-requirements-clarification-2.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-contract-wording-review-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-phase2-check-2.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-planning-approval-2.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-change-request-review-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-task-workspace-plan-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-task-workspace-result-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert api["skill_contracts"]["interface_schema_id"] == "guru-team-skill-interface-1.2"
assert api["skill_runtime"] == {
    "api_version": "1.0",
    "dispatcher": "run-skill-command",
    "manifest_path": ".trellis/guru-team/extension.json",
}
assert skills["status"] == "ok"
assert skills["reserved_ids"] == ["guru-create-work-commit"]
assert skills["active_ids"] == ["guru-approve-task-plan", "guru-check-task", "guru-clarify-requirements", "guru-create-task-commit", "guru-create-task-workspace", "guru-discover-change-context", "guru-review-change-request", "guru-review-contract-wording", "guru-sync-base"]
assert skills["selected_platforms"] == ["claude", "codex", "cursor"]
assert skills["sidecars"] == []
skill_paths = [entry["path"] for entry in skills["files"]]
assert len(skill_paths) == len(set(skill_paths))
assert all((root / path).is_file() for path in skill_paths)
registry = json.loads((root / ".trellis/guru-team/skills/registry.json").read_text(encoding="utf-8"))
planned = [entry for entry in registry["skills"] if entry.get("state") == "planned"]
assert planned == []
PY
SOURCE_SKILL_VALIDATION_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$REPO_ROOT" --json --mode source)"
INSTALLED_SKILL_VALIDATION_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$TARGET" --json --mode installed)"
python3 -c 'import json, sys; source = json.loads(sys.argv[1]); installed = json.load(sys.stdin); assert source["status"] == installed["status"] == "passed"; expected={"invoke_markers":9,"exit_markers":35,"target_markers":20,"planned_ids":[]}; assert all(source["facts"][key] == installed["facts"][key] == value for key,value in expected.items())' "$SOURCE_SKILL_VALIDATION_JSON" <<<"$INSTALLED_SKILL_VALIDATION_JSON"
test ! -e "$TARGET/.agents/skills/guru-create-work-commit"
test ! -e "$TARGET/.codex/skills/guru-create-work-commit"
test ! -e "$TARGET/.cursor/skills/guru-create-work-commit"
test ! -e "$TARGET/.claude/skills/guru-create-work-commit"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-approve-task-plan/SKILL.md"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-approve-task-plan/schemas/planning-approval.schema.json"
test -x "$TARGET/.agents/skills/guru-approve-task-plan/scripts/record-planning-approval.sh"
test -x "$TARGET/.agents/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -x "$TARGET/.claude/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -x "$TARGET/.codex/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -x "$TARGET/.cursor/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-commit/SKILL.md"
test -x "$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh"
test -x "$TARGET/.agents/skills/guru-create-task-commit/scripts/create-task-commit.sh"
"$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh" --help >/dev/null
test -x "$TARGET/.claude/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.codex/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.cursor/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-check-task/SKILL.md"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-check-task/schemas/phase2-check.schema.json"
test -x "$TARGET/.agents/skills/guru-check-task/scripts/record-phase2-check.sh"
test -x "$TARGET/.agents/skills/guru-check-task/scripts/check-phase2-check.sh"
test -x "$TARGET/.claude/skills/guru-check-task/scripts/check-phase2-check.sh"
test -x "$TARGET/.codex/skills/guru-check-task/scripts/record-phase2-check.sh"
test -x "$TARGET/.cursor/skills/guru-check-task/scripts/check-phase2-check.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-sync-base/SKILL.md"
test -x "$TARGET/.agents/skills/guru-sync-base/scripts/sync-base.sh"
test -x "$TARGET/.agents/skills/guru-sync-base/scripts/check-base-sync.sh"
test -x "$TARGET/.claude/skills/guru-sync-base/scripts/sync-base.sh"
test -x "$TARGET/.codex/skills/guru-sync-base/scripts/sync-base.sh"
test -x "$TARGET/.cursor/skills/guru-sync-base/scripts/sync-base.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-discover-change-context/SKILL.md"
test -x "$TARGET/.agents/skills/guru-discover-change-context/scripts/preview-change-context-history.sh"
test -x "$TARGET/.agents/skills/guru-discover-change-context/scripts/record-context-discovery.sh"
test -x "$TARGET/.agents/skills/guru-discover-change-context/scripts/check-context-discovery.sh"
test -x "$TARGET/.claude/skills/guru-discover-change-context/scripts/preview-change-context-history.sh"
test -x "$TARGET/.codex/skills/guru-discover-change-context/scripts/preview-change-context-history.sh"
test -x "$TARGET/.cursor/skills/guru-discover-change-context/scripts/preview-change-context-history.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-clarify-requirements/SKILL.md"
test -x "$TARGET/.agents/skills/guru-clarify-requirements/scripts/record-requirements-clarification.sh"
test -x "$TARGET/.agents/skills/guru-clarify-requirements/scripts/check-requirements-clarification.sh"
test -x "$TARGET/.claude/skills/guru-clarify-requirements/scripts/check-requirements-clarification.sh"
test -x "$TARGET/.codex/skills/guru-clarify-requirements/scripts/record-requirements-clarification.sh"
test -x "$TARGET/.cursor/skills/guru-clarify-requirements/scripts/check-requirements-clarification.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-review-contract-wording/SKILL.md"
test -x "$TARGET/.agents/skills/guru-review-contract-wording/scripts/record-contract-wording-review.sh"
test -x "$TARGET/.agents/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh"
test -x "$TARGET/.claude/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh"
test -x "$TARGET/.codex/skills/guru-review-contract-wording/scripts/record-contract-wording-review.sh"
test -x "$TARGET/.cursor/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-review-change-request/SKILL.md"
test -x "$TARGET/.agents/skills/guru-review-change-request/scripts/record-change-request-review.sh"
test -x "$TARGET/.agents/skills/guru-review-change-request/scripts/check-change-request-review.sh"
test -x "$TARGET/.claude/skills/guru-review-change-request/scripts/check-change-request-review.sh"
test -x "$TARGET/.codex/skills/guru-review-change-request/scripts/record-change-request-review.sh"
test -x "$TARGET/.codex/skills/guru-review-change-request/scripts/check-change-request-review.sh"
test -x "$TARGET/.cursor/skills/guru-review-change-request/scripts/record-change-request-review.sh"
test -x "$TARGET/.cursor/skills/guru-review-change-request/scripts/check-change-request-review.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-workspace/SKILL.md"
test -x "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-workspace/scripts/record-task-workspace-plan.sh"
test -x "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-workspace/scripts/create-task-workspace.sh"
test -x "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-workspace/scripts/check-task-workspace-result.sh"
test -f "$TARGET/.agents/skills/guru-create-task-workspace/SKILL.md"
test -x "$TARGET/.agents/skills/guru-create-task-workspace/scripts/record-task-workspace-plan.sh"
test -x "$TARGET/.claude/skills/guru-create-task-workspace/scripts/create-task-workspace.sh"
test -x "$TARGET/.codex/skills/guru-create-task-workspace/scripts/create-task-workspace.sh"
test -x "$TARGET/.cursor/skills/guru-create-task-workspace/scripts/check-task-workspace-result.sh"
verify_requirements_clarification_exits "initial"
verify_contract_wording_standalone_profiles "initial"
verify_change_request_review_package "initial"
test ! -e "$TARGET/.agents/skills/guru-example-action"
test ! -e "$TARGET/.codex/skills/guru-example-action"
test ! -e "$TARGET/.cursor/skills/guru-example-action"
test ! -e "$TARGET/.claude/skills/guru-example-action"
(cd "$REPO_ROOT" && python3 -m unittest trellis.skills.guru-team.tests.test_skill_packages.DistributionTests.test_unchanged_reapply)
test -f "$TARGET/.trellis/guru-team/schemas/closeout-plan.schema.json"
mkdir -p "$TARGET/.trellis/tasks/archive"
BACKFILL_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh" --root "$TARGET" --json --dry-run)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["mode"] == "dry-run"; assert payload["scanned_tasks"] == 0; assert payload["to_write"] == []; assert payload["skipped"] == []; assert payload["errors"] == []' <<<"$BACKFILL_JSON"
python3 - "$TARGET" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
archive = root / ".trellis/tasks/archive/2025-12/context-discovery-fixture"
archive.mkdir(parents=True)
(archive / "design.md").write_text(
    "# Archived context discovery design\n\nThe runtime reads only explicit task artifacts.\n",
    encoding="utf-8",
)
index = {
    "problem": "A reusable change context discovery contract was needed.",
    "outcome": "The archived task recorded deterministic context discovery behavior.",
    "changed_behavior": ["Added deterministic archived context preview."],
    "affected_surfaces": [{
        "kind": "workflow",
        "name": "context discovery",
        "paths": ["docs/context-discovery-smoke.md"],
        "change": "Current evidence is reviewed before archived history.",
    }],
    "contract_changes": [],
    "search_terms": {
        "issue_refs": ["#111"],
        "pr_refs": [],
        "branches": ["feat/111-context-discovery"],
        "paths": ["docs/context-discovery-smoke.md"],
        "commands": ["preview-change-context-history"],
        "config_keys": [],
        "schema_fields": ["snapshot_sha256"],
        "symbols": ["context-discovery"],
        "phrases": [
            "context-discovery 历史索引预览已完成",
            "preview-change-context-history 命令已新增",
            "context-discovery 支持检索",
        ],
    },
    "retrieval_text": (
        "context-discovery 历史索引预览已完成\n"
        "preview-change-context-history 命令已新增\n"
        "context-discovery 支持检索\n"
        "current evidence before archived history and same snapshot persistence"
    ),
}
(archive / "finish-summary.json").write_text(
    json.dumps({"ignored": {"private": "not consumed"}, "index": index}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
current_files = {
    "docs/context-discovery-smoke.md": "# Current context discovery contract\n",
    "src/context_discovery_smoke.py": "CONTEXT_DISCOVERY = 'current-before-history'\n",
    "tests/test_context_discovery_smoke.py": "def test_context_discovery_smoke():\n    assert True\n",
}
for relative, content in current_files.items():
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
PY
grep -q "def prepare_closeout" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
! grep -q "def resolve_closeout_state" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
grep -q "publish-pr is a compatibility-only blocked command" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
grep -q "def ensure_closeout_draft_pr" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
grep -q "If any ordinary stage fails, rerun this same entry with the same expected digest" "$TARGET/.agents/skills/trellis-finish-work/SKILL.md"
grep -q "archive-month-preflight" "$TARGET/.agents/skills/trellis-finish-work/SKILL.md"
grep -q "hooks.after_archive" "$TARGET/.agents/skills/trellis-finish-work/SKILL.md"
test -z "$(find "$TARGET" -type f \( -name '*.new' -o -name '*.bak' \) -print -quit)"
test -d "$TARGET/.agents/skills"
test -d "$TARGET/.claude/skills"
test -d "$TARGET/.codex"
test -d "$TARGET/.cursor"
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
SYNC_REMOTE="$WORK_DIR/base-sync-remote.git"
git init -q --bare "$SYNC_REMOTE"
git -C "$SYNC_REMOTE" symbolic-ref HEAD refs/heads/main
git -C "$TARGET" remote set-url origin "$SYNC_REMOTE"
SYNC_CONFIG_BACKUP="$WORK_DIR/base-sync-config.yml"
cp "$TARGET/.trellis/guru-team/config.yml" "$SYNC_CONFIG_BACKUP"
python3 - "$TARGET/.trellis/guru-team/config.yml" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
lines = path.read_text(encoding="utf-8").splitlines()
updated = False
for index, line in enumerate(lines):
    if line.startswith("github_repo:"):
        lines[index] = 'github_repo: "castbox/guru-trellis-throwaway"'
        updated = True
        break
if not updated:
    raise SystemExit("throwaway Guru Team config is missing github_repo")
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
git -C "$TARGET" add .trellis/guru-team/config.yml
git -C "$TARGET" commit -q -m "chore: configure throwaway base remote"
git -C "$TARGET" push -q origin main
SYNC_RESOLUTION_JSON="$(
  "$TARGET/.agents/skills/guru-sync-base/scripts/sync-base.sh" \
    --root "$TARGET" \
    --mode standalone \
    --resolve-only \
    --base main \
    --remote origin
)"
SYNC_RESOLUTION_DIGEST="$(python3 -c 'import json, sys; print(json.load(sys.stdin)["resolution_sha256"])' <<<"$SYNC_RESOLUTION_JSON")"
SYNC_RESULT_JSON="$(
  "$TARGET/.agents/skills/guru-sync-base/scripts/sync-base.sh" \
    --root "$TARGET" \
    --mode standalone \
    --execute \
    --expected-resolution-sha256 "$SYNC_RESOLUTION_DIGEST" \
    --base main \
    --remote origin
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "synced"; assert payload["fresh"] is True; assert payload["git"]["fast_forwarded"] is False; assert payload["resolution"]["resolution_sha256"] == payload["post_sync_resolution_sha256"]; assert payload["decision_checkout"]["head_after"] == payload["git"]["local_head_after"] == payload["git"]["remote_head_after"]' <<<"$SYNC_RESULT_JSON"
SYNC_VALIDATION_JSON="$(
  "$TARGET/.agents/skills/guru-sync-base/scripts/check-base-sync.sh" \
    --root "$TARGET" \
    --mode standalone \
    --result-json "$SYNC_RESULT_JSON" \
    --expected-resolution-sha256 "$SYNC_RESOLUTION_DIGEST"
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "validated"; assert payload["selected_base"] == "main"; assert payload["post_sync_resolution_sha256"] == sys.argv[1]' "$SYNC_RESOLUTION_DIGEST" <<<"$SYNC_VALIDATION_JSON"

DISCOVERY_PREVIEW="$TARGET/.agents/skills/guru-discover-change-context/scripts/preview-change-context-history.sh"
DISCOVERY_RECORD="$TARGET/.agents/skills/guru-discover-change-context/scripts/record-context-discovery.sh"
DISCOVERY_CHECK="$TARGET/.agents/skills/guru-discover-change-context/scripts/check-context-discovery.sh"
DISCOVERY_ZERO_JSON="$(
  "$DISCOVERY_PREVIEW" \
    --root "$TARGET" \
    --json \
    --term "quasar nebula xyzzy"
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["algorithm_id"] == "guru-context-history-score-1.0"; assert payload["candidates"] == []; assert payload["invalid"] == []' <<<"$DISCOVERY_ZERO_JSON"
DISCOVERY_CANDIDATE_JSON="$(
  "$DISCOVERY_PREVIEW" \
    --root "$TARGET" \
    --json \
    --issue-ref '#111' \
    --path docs/context-discovery-smoke.md \
    --command preview-change-context-history \
    --schema-field snapshot_sha256 \
    --term "context discovery" \
    --query "current evidence before archived history"
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert len(payload["candidates"]) == 1; candidate = payload["candidates"][0]; assert candidate["finish_summary_path"].endswith("context-discovery-fixture/finish-summary.json"); assert candidate["score"]["total"] > 0; assert payload["preview_sha256"]' <<<"$DISCOVERY_CANDIDATE_JSON"

DISCOVERY_INPUT="$WORK_DIR/context-discovery-input.json"
python3 - "$TARGET" "$SYNC_RESULT_JSON" "$DISCOVERY_CANDIDATE_JSON" "$DISCOVERY_INPUT" <<'PY'
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sync_result = json.loads(sys.argv[2])
preview = json.loads(sys.argv[3])
output = Path(sys.argv[4])
runtime = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
spec = importlib.util.spec_from_file_location("installed_context_discovery_runtime", runtime)
if spec is None or spec.loader is None:
    raise SystemExit(f"could not load installed context discovery runtime: {runtime}")
gtt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gtt
spec.loader.exec_module(gtt)

head = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, capture_output=True,
).stdout.strip()
if head != sync_result["decision_checkout"]["head_after"]:
    raise SystemExit("throwaway context discovery base evidence is stale")

def blob(relative: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"], cwd=root, check=True, text=True, capture_output=True,
    ).stdout.strip()

query = preview["canonical_query"]
candidate = preview["candidates"][0]
candidate_task = candidate["finish_summary_path"].rsplit("/", 1)[0]
body_sha256 = hashlib.sha256(b"throwaway context discovery request").hexdigest()
live_change = {
    "kind": "draft",
    "identity": f"draft:{body_sha256}",
    "state": "draft",
    "updated_at": "2026-01-01T00:00:00Z",
    "body_sha256": body_sha256,
}
live_change["facts_sha256"] = gtt.context_digest(live_change)
issue_binding = {
    "repo": "castbox/guru-trellis-throwaway",
    "number": 111,
    "url": "https://github.com/castbox/guru-trellis-throwaway/issues/111",
    "state": "open",
    "updated_at": "2026-01-01T00:00:00Z",
    "body_sha256": body_sha256,
}
issue_binding["facts_sha256"] = gtt.context_digest(issue_binding)
live_change["issue_binding"] = issue_binding
duplicate_facts = {
    "repo": "castbox/guru-trellis-throwaway",
    "number": 99,
    "identity": "#99",
    "url": "https://github.com/castbox/guru-trellis-throwaway/issues/99",
    "state": "open",
    "updated_at": "2026-01-01T00:00:00Z",
}
duplicate_candidate = {
    **duplicate_facts,
    "facts_sha256": gtt.context_digest(duplicate_facts),
    "reason": "The open issue may describe the same change.",
    "observation": "Clarification must decide reuse or a new target.",
}
payload = {
    "schema_version": "1.0",
    "skill_id": "guru-discover-change-context",
    "generated_at": "2026-01-01T00:00:00Z",
    "mode": "standalone",
    "typed_exit": "context_ready",
    "repository": {"repo": "castbox/guru-trellis-throwaway", "selected_base": "main", "decision_branch": "main"},
    "base_evidence": {
        "schema_id": "guru-base-sync-result-1.0",
        "sync_result": sync_result,
        "remote": sync_result["resolution"]["remote"],
        "base_head": head,
        "decision_head": sync_result["decision_checkout"]["head_after"],
        "local_head": sync_result["git"]["local_head_after"],
        "remote_head": sync_result["git"]["remote_head_after"],
        "post_sync_resolution_sha256": sync_result["post_sync_resolution_sha256"],
        "clean": sync_result["decision_checkout"]["clean_after"],
    },
    "change_input": {
        key: query[key]
        for key in (
            "issue_refs", "pr_refs", "branches", "paths", "commands", "config_keys",
            "schema_fields", "symbols", "terms", "queries",
        )
    },
    "live_change": live_change,
    "duplicate_search": {
        "query": "repo:castbox/guru-trellis-throwaway is:issue is:open context discovery",
        "checked_at": "2026-01-01T00:00:00Z", "scope": "open_issues",
        "candidates": [duplicate_candidate],
    },
    "current_state": {
        "sequence_trace": list(gtt.CONTEXT_SEQUENCE_TRACE),
        "docs": [{
            "path": "docs/context-discovery-smoke.md", "blob_or_content_sha256": blob("docs/context-discovery-smoke.md"),
            "purpose": "Review the durable current-state contract.",
            "observation": "Current evidence must precede archived history.", "query_clues": ["current state"],
        }],
        "code_contracts": [{
            "path": "src/context_discovery_smoke.py", "blob_or_content_sha256": blob("src/context_discovery_smoke.py"),
            "purpose": "Review deterministic runtime ownership.",
            "observation": "The runtime validates facts without making semantic decisions.", "query_clues": ["runtime"],
        }],
        "tests": [{
            "path": "tests/test_context_discovery_smoke.py", "blob_or_content_sha256": blob("tests/test_context_discovery_smoke.py"),
            "purpose": "Review installed verification coverage.",
            "observation": "The throwaway covers candidate and zero-candidate paths.", "query_clues": ["throwaway"],
        }],
        "observations": ["Current repository evidence was reviewed before history preview."],
    },
    "canonical_query": query,
    "history_preview": preview,
    "history_review": {
        "selected_candidates": [{"candidate_id": candidate["candidate_id"], "reason": "Exact issue, path and command clues match."}],
        "excluded_candidates": [],
        "deep_reads": [{
            "candidate_id": candidate["candidate_id"], "source": "task_artifact",
            "locator": f"{candidate_task}/design.md", "purpose": "Verify archived runtime ownership.",
            "conclusion": "The selected artifact confirms explicit narrow deep-read behavior.",
        }],
    },
    "mem_review": {
        "status": "not_needed", "reason": "Current and selected task evidence is sufficient.",
        "load_bearing_question": None,
        "exhausted_sources": {"task_artifacts": False, "current_docs_code_tests": False, "github": False, "git_history": False},
        "summary": None,
    },
    "ai_review_gate": {
        "status": "passed", "reviewer": "throwaway-context-review",
        "reviewed_scope": ["live draft", "current Docs/code/tests", "selected archived task artifact"],
        "excluded_scope": ["duplicate reuse decision"],
        "relevance": "The evidence directly covers installed context discovery.",
        "sufficiency": "Current and archived evidence support the load-bearing conclusions.",
        "conflicts": [], "reusable": ["installed dispatcher"], "not_reusable": ["workspace journal"],
        "load_bearing_conclusions": [{
            "conclusion": "Current state is reviewed before archived history.",
            "evidence_refs": ["docs/context-discovery-smoke.md", f"{candidate_task}/design.md"],
        }],
        "findings": [], "reason": "Every required semantic dimension passed.",
    },
    "human_confirmation": {"status": "not_required", "reason": "decision_owned_by_guru-clarify-requirements"},
    "refresh_history": [], "snapshot_identity": {}, "error": None,
}
payload["snapshot_identity"] = gtt.context_snapshot_identity(payload)

if gtt.context_reviewed_blob_errors(root, payload):
    raise SystemExit("installed context discovery rejected reviewed file blobs")
tree_evidence = copy.deepcopy(payload)
tree_evidence["current_state"]["docs"][0]["path"] = "docs"
tree_evidence["current_state"]["docs"][0]["blob_or_content_sha256"] = blob("docs")
if "reviewed_blob_stale" not in gtt.context_reviewed_blob_errors(root, tree_evidence):
    raise SystemExit("installed context discovery accepted a reviewed tree as a blob")

closed_body = "Closed source issue remains valid discovery input."
closed_body_sha256 = hashlib.sha256(closed_body.encode("utf-8")).hexdigest()
closed_facts = {
    "repo": "castbox/guru-trellis-throwaway",
    "number": 111,
    "url": "https://github.com/castbox/guru-trellis-throwaway/issues/111",
    "state": "closed",
    "updated_at": "2026-01-01T00:00:00Z",
    "body_sha256": closed_body_sha256,
}
closed_facts["facts_sha256"] = gtt.context_digest(closed_facts)
closed_source = copy.deepcopy(payload)
closed_source["live_change"] = {
    "kind": "issue",
    "identity": closed_facts["url"],
    "state": closed_facts["state"],
    "updated_at": closed_facts["updated_at"],
    "body_sha256": closed_facts["body_sha256"],
    "facts_sha256": closed_facts["facts_sha256"],
    "issue_binding": None,
}
closed_source["snapshot_identity"] = gtt.context_snapshot_identity(closed_source)
if gtt.context_structural_errors(root, closed_source):
    raise SystemExit("installed context discovery rejected a closed source issue")
closed_duplicate = copy.deepcopy(closed_source)
closed_duplicate["duplicate_search"]["candidates"] = [{
    "repo": "castbox/guru-trellis-throwaway",
    "number": 99,
    "identity": "#99",
    "url": "https://github.com/castbox/guru-trellis-throwaway/issues/99",
    "state": "closed",
    "updated_at": "2026-01-01T00:00:00Z",
    "facts_sha256": "a" * 64,
    "reason": "Possible duplicate.",
    "observation": "Closed issues cannot enter the open duplicate candidate set.",
}]
closed_duplicate["snapshot_identity"] = gtt.context_snapshot_identity(closed_duplicate)
if "context_schema_validation_failed" not in gtt.context_structural_errors(root, closed_duplicate):
    raise SystemExit("installed context discovery accepted a closed duplicate candidate")

wrong_duplicate_digest = copy.deepcopy(payload)
wrong_duplicate_digest["duplicate_search"]["candidates"][0]["facts_sha256"] = "f" * 64
wrong_duplicate_digest["snapshot_identity"] = gtt.context_snapshot_identity(wrong_duplicate_digest)
if "duplicate_candidate_facts_digest_mismatch" not in gtt.context_structural_errors(root, wrong_duplicate_digest):
    raise SystemExit("installed context discovery accepted a mismatched duplicate digest")

for field, value, expected_code in (
    ("identity", "#100", "duplicate_candidate_identity_mismatch"),
    ("url", "https://github.com/castbox/guru-trellis-throwaway/issues/100", "duplicate_candidate_url_mismatch"),
):
    variant = copy.deepcopy(payload)
    candidate_variant = variant["duplicate_search"]["candidates"][0]
    candidate_variant[field] = value
    candidate_variant["facts_sha256"] = gtt.context_digest({
        key: candidate_variant[key]
        for key in ("repo", "number", "identity", "url", "state", "updated_at")
    })
    variant["snapshot_identity"] = gtt.context_snapshot_identity(variant)
    if expected_code not in gtt.context_structural_errors(root, variant):
        raise SystemExit(f"installed context discovery accepted duplicate {field} mismatch")

blocked_with_passed_gate = copy.deepcopy(payload)
blocked_with_passed_gate["typed_exit"] = "blocked"
blocked_with_passed_gate["error"] = {
    "codes": ["semantic_review_blocked"],
    "summary": "The semantic review could not form safe evidence.",
}
blocked_with_passed_gate["snapshot_identity"] = gtt.context_snapshot_identity(blocked_with_passed_gate)
if "blocked_requires_blocked_gate" not in gtt.context_structural_errors(root, blocked_with_passed_gate):
    raise SystemExit("installed context discovery accepted blocked with a passed Gate")
blocked_gate_with_ready_exit = copy.deepcopy(payload)
blocked_gate_with_ready_exit["ai_review_gate"]["status"] = "blocked"
blocked_gate_with_ready_exit["snapshot_identity"] = gtt.context_snapshot_identity(blocked_gate_with_ready_exit)
if "blocked_gate_requires_blocked_exit" not in gtt.context_structural_errors(root, blocked_gate_with_ready_exit):
    raise SystemExit("installed context discovery accepted a blocked Gate with context_ready")

empty_change_input = copy.deepcopy(payload)
empty_change_input["change_input"] = {
    kind: [] for kind in gtt.CONTEXT_QUERY_KINDS
}
empty_change_input["snapshot_identity"] = gtt.context_snapshot_identity(empty_change_input)
empty_change_errors = gtt.context_structural_errors(root, empty_change_input)
if not {
    "context_schema_validation_failed",
    "change_input_has_no_clues",
}.issubset(empty_change_errors):
    raise SystemExit("installed context discovery accepted an empty change_input")
single_clue_values = {
    "issue_refs": "#111",
    "pr_refs": "PR #111",
    "branches": "feat/context",
    "paths": "docs/context-discovery-smoke.md",
    "commands": "/trellis:continue",
    "config_keys": "context.mode",
    "schema_fields": "snapshot_sha256",
    "symbols": "ContextDiscovery",
    "terms": "change context",
    "queries": "discover current and archived context",
}
for kind, value in single_clue_values.items():
    variant = copy.deepcopy(payload)
    variant["change_input"] = {
        clue_kind: [value] if clue_kind == kind else []
        for clue_kind in gtt.CONTEXT_QUERY_KINDS
    }
    if kind != "issue_refs":
        variant["live_change"]["issue_binding"] = None
    variant["snapshot_identity"] = gtt.context_snapshot_identity(variant)
    errors = gtt.context_structural_errors(root, variant)
    if "context_schema_validation_failed" in errors or "change_input_has_no_clues" in errors:
        raise SystemExit(f"installed context discovery rejected single {kind} clue")

source_specific_locators = (
    ("task_artifact", f"{candidate_task}/design.md"),
    ("github", "https://github.com/castbox/guru-trellis-throwaway/issues/111"),
    ("github", "https://github.com/castbox/guru-trellis-throwaway/pull/111"),
    ("git", f"git:object:{head}"),
    ("git", f"git:ref:refs/heads/main@{head}"),
)
for source, locator in source_specific_locators:
    variant = copy.deepcopy(payload)
    variant["history_review"]["deep_reads"][0].update({
        "source": source,
        "locator": locator,
    })
    variant["snapshot_identity"] = gtt.context_snapshot_identity(variant)
    if (
        gtt.context_structural_errors(root, variant)
        or gtt.context_repo_bound_locator_errors(root, variant)
    ):
        raise SystemExit(f"installed context discovery rejected canonical {source} locator")

invalid_locators = (
    ("task_artifact", ".trellis/tasks/archive/2025-12/other-task/design.md"),
    ("github", "https://github.com/castbox/guru-trellis-throwaway/issues/111?view=full"),
    ("git", f"git:ref:refs/heads/missing@{head}"),
)
for source, locator in invalid_locators:
    variant = copy.deepcopy(payload)
    variant["history_review"]["deep_reads"][0].update({
        "source": source,
        "locator": locator,
    })
    variant["snapshot_identity"] = gtt.context_snapshot_identity(variant)
    if not (
        gtt.context_structural_errors(root, variant)
        or gtt.context_repo_bound_locator_errors(root, variant)
    ):
        raise SystemExit(f"installed context discovery accepted invalid {source} locator")

output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

DISCOVERY_ZERO_INPUT="$WORK_DIR/context-discovery-zero-input.json"
DISCOVERY_ZERO_USED_INPUT="$WORK_DIR/context-discovery-zero-used-input.json"
DISCOVERY_ZERO_INCONSISTENT_INPUT="$WORK_DIR/context-discovery-zero-inconsistent-input.json"
python3 - \
  "$TARGET" \
  "$DISCOVERY_INPUT" \
  "$DISCOVERY_ZERO_JSON" \
  "$DISCOVERY_ZERO_INPUT" \
  "$DISCOVERY_ZERO_USED_INPUT" \
  "$DISCOVERY_ZERO_INCONSISTENT_INPUT" <<'PY'
import copy
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
payload = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
preview = json.loads(sys.argv[3])
runtime = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
spec = importlib.util.spec_from_file_location("installed_zero_context_runtime", runtime)
if spec is None or spec.loader is None:
    raise SystemExit(f"could not load installed context discovery runtime: {runtime}")
gtt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gtt
spec.loader.exec_module(gtt)

payload["canonical_query"] = preview["canonical_query"]
payload["change_input"] = {
    key: preview["canonical_query"][key]
    for key in (
        "issue_refs", "pr_refs", "branches", "paths", "commands", "config_keys",
        "schema_fields", "symbols", "terms", "queries",
    )
}
payload["live_change"]["issue_binding"] = None
payload["history_preview"] = preview
payload["history_review"] = {
    "selected_candidates": [],
    "excluded_candidates": [],
    "deep_reads": [],
}
payload["mem_review"] = {
    "status": "not_needed",
    "reason": "The zero-candidate preview requires no other history source.",
    "load_bearing_question": None,
    "exhausted_sources": {
        "task_artifacts": False,
        "current_docs_code_tests": False,
        "github": False,
        "git_history": False,
    },
    "summary": None,
}
payload["ai_review_gate"]["reviewed_scope"] = [
    "live draft", "current Docs/code/tests", "zero-candidate history preview",
]
payload["ai_review_gate"]["sufficiency"] = (
    "Current evidence and the zero-candidate preview are sufficient without another history source."
)
payload["ai_review_gate"]["load_bearing_conclusions"] = [{
    "conclusion": "Zero candidates require no deep-read or memory source.",
    "evidence_refs": ["docs/context-discovery-smoke.md"],
}]
payload["snapshot_identity"] = gtt.context_snapshot_identity(payload)
Path(sys.argv[4]).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

used = copy.deepcopy(payload)
used["mem_review"] = {
    "status": "used",
    "reason": "Invalid zero-candidate memory attempt.",
    "load_bearing_question": "Which history source should be read?",
    "exhausted_sources": {
        "task_artifacts": True,
        "current_docs_code_tests": True,
        "github": True,
        "git_history": True,
    },
    "summary": "Invalid memory evidence.",
}
used["snapshot_identity"] = gtt.context_snapshot_identity(used)
Path(sys.argv[5]).write_text(json.dumps(used, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

inconsistent = copy.deepcopy(payload)
inconsistent["mem_review"]["load_bearing_question"] = "Inconsistent not-needed question."
inconsistent["mem_review"]["exhausted_sources"]["git_history"] = True
inconsistent["mem_review"]["summary"] = "Inconsistent not-needed summary."
inconsistent["snapshot_identity"] = gtt.context_snapshot_identity(inconsistent)
Path(sys.argv[6]).write_text(
    json.dumps(inconsistent, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

DISCOVERY_FAKE_BIN="$WORK_DIR/context-discovery-fake-bin"
mkdir -p "$DISCOVERY_FAKE_BIN"
DISCOVERY_REAL_GIT="$(command -v git)"
cat >"$DISCOVERY_FAKE_BIN/gh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "issue" && "${2:-}" == "view" && "${3:-}" == "111" ]]; then
  printf '%s\n' '{"number":111,"url":"https://github.com/castbox/guru-trellis-throwaway/issues/111","state":"OPEN","updatedAt":"2026-01-01T00:00:00Z","body":"throwaway context discovery request"}'
  exit 0
fi
if [[ "${1:-}" == "issue" && "${2:-}" == "view" && "${3:-}" == "99" ]]; then
  printf '%s\n' '{"number":99,"url":"https://github.com/castbox/guru-trellis-throwaway/issues/99","state":"OPEN","updatedAt":"2026-01-01T00:00:00Z","body":"throwaway duplicate candidate"}'
  exit 0
fi
exit 2
SH
chmod +x "$DISCOVERY_FAKE_BIN/gh"
cat >"$DISCOVERY_FAKE_BIN/git" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "config" && "${2:-}" == "--null" && "${3:-}" == "--show-origin" && "${4:-}" == "--get-all" && "${5:-}" == "remote.origin.url" ]]; then
  printf 'command line:\0https://github.com/castbox/guru-trellis-throwaway.git\0'
  exit 0
fi
if [[ "${1:-}" == "remote" && "${2:-}" == "get-url" && "${3:-}" == "--all" && "${4:-}" == "origin" ]]; then
  printf '%s\n' 'https://github.com/castbox/guru-trellis-throwaway.git'
  exit 0
fi
if [[ "${1:-}" == "remote" && "${2:-}" == "get-url" && "${3:-}" == "--push" && "${4:-}" == "--all" && "${5:-}" == "origin" ]]; then
  printf '%s\n' 'https://github.com/castbox/guru-trellis-throwaway.git'
  exit 0
fi
exec "${DISCOVERY_REAL_GIT:?}" "$@"
SH
chmod +x "$DISCOVERY_FAKE_BIN/git"

DISCOVERY_STATUS_BEFORE="$(git -C "$TARGET" status --porcelain=v1)"
DISCOVERY_PRETASK_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_RECORD" \
    --root "$TARGET" \
    --json \
    --mode standalone \
    --input "$DISCOVERY_INPUT"
)"
DISCOVERY_ZERO_PRETASK_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_RECORD" \
    --root "$TARGET" \
    --json \
    --mode standalone \
    --input "$DISCOVERY_ZERO_INPUT"
)"
DISCOVERY_STATUS_AFTER="$(git -C "$TARGET" status --porcelain=v1)"
if [[ "$DISCOVERY_STATUS_AFTER" != "$DISCOVERY_STATUS_BEFORE" ]]; then
  echo "Pre-task context discovery modified the throwaway repository" >&2
  exit 2
fi
DISCOVERY_SNAPSHOT_SHA256="$(python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["typed_exit"] == "context_ready"; print(payload["snapshot_identity"]["snapshot_sha256"])' <<<"$DISCOVERY_PRETASK_JSON")"
DISCOVERY_ZERO_SNAPSHOT_SHA256="$(python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["typed_exit"] == "context_ready"; assert payload["history_preview"]["candidates"] == []; assert payload["history_review"] == {"selected_candidates": [], "excluded_candidates": [], "deep_reads": []}; assert payload["mem_review"]["status"] == "not_needed"; print(payload["snapshot_identity"]["snapshot_sha256"])' <<<"$DISCOVERY_ZERO_PRETASK_JSON")"

for INVALID_DISCOVERY_INPUT in "$DISCOVERY_ZERO_USED_INPUT" "$DISCOVERY_ZERO_INCONSISTENT_INPUT"; do
  set +e
  DISCOVERY_INVALID_JSON="$(
    DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_RECORD" \
      --root "$TARGET" \
      --json \
      --mode standalone \
      --input "$INVALID_DISCOVERY_INPUT" 2>&1
  )"
  DISCOVERY_INVALID_STATUS=$?
  set -e
  if [[ "$DISCOVERY_INVALID_STATUS" -eq 0 ]]; then
    echo "Zero-candidate context discovery accepted an invalid mem shape" >&2
    exit 2
  fi
  python3 -c 'import json, sys; payload = json.load(sys.stdin); codes = payload["error_codes"]; assert "context_schema_validation_failed" in codes; assert any(code in codes for code in ("zero_candidate_mem_must_be_not_needed", "mem_not_needed_shape_invalid"))' <<<"$DISCOVERY_INVALID_JSON"
done

DISCOVERY_TASK_BRANCH="feat/111-context-discovery-task"
DISCOVERY_TASK_WORKTREE="$WORK_DIR/context-discovery-feature-worktree"
git -C "$TARGET" worktree add -q -b "$DISCOVERY_TASK_BRANCH" "$DISCOVERY_TASK_WORKTREE" "$(git -C "$TARGET" rev-parse HEAD)"
DISCOVERY_TASK_RECORD="$DISCOVERY_TASK_WORKTREE/.agents/skills/guru-discover-change-context/scripts/record-context-discovery.sh"
DISCOVERY_TASK_CHECK="$DISCOVERY_TASK_WORKTREE/.agents/skills/guru-discover-change-context/scripts/check-context-discovery.sh"
DISCOVERY_TASK_REL=".trellis/tasks/01-01-context-discovery-smoke"
DISCOVERY_ZERO_TASK_REL=".trellis/tasks/01-01-context-discovery-zero"
mkdir -p "$DISCOVERY_TASK_WORKTREE/$DISCOVERY_TASK_REL"
printf '%s\n' "{\"id\":\"context-discovery-smoke\",\"status\":\"planning\",\"branch\":\"$DISCOVERY_TASK_BRANCH\"}" >"$DISCOVERY_TASK_WORKTREE/$DISCOVERY_TASK_REL/task.json"
DISCOVERY_TASK_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_TASK_RECORD" \
    --root "$DISCOVERY_TASK_WORKTREE" \
    --json \
    --mode standalone \
    --input "$DISCOVERY_INPUT" \
    --task "$DISCOVERY_TASK_REL" \
    --expected-snapshot-sha256 "$DISCOVERY_SNAPSHOT_SHA256"
)"
DISCOVERY_CHECK_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_TASK_CHECK" \
    --root "$DISCOVERY_TASK_WORKTREE" \
    --json \
    --task "$DISCOVERY_TASK_REL" \
    --expected-snapshot-sha256 "$DISCOVERY_SNAPSHOT_SHA256"
)"
python3 -c 'import json, sys; recorded = json.loads(sys.argv[1]); checked = json.load(sys.stdin); assert recorded["snapshot_identity"]["snapshot_sha256"] == checked["snapshot_sha256"] == sys.argv[2]; assert checked["status"] == "passed"; assert checked["typed_exit"] == "context_ready"' "$DISCOVERY_TASK_JSON" "$DISCOVERY_SNAPSHOT_SHA256" <<<"$DISCOVERY_CHECK_JSON"
rm "$DISCOVERY_TASK_WORKTREE/$DISCOVERY_TASK_REL/context-discovery.json"
DISCOVERY_GIT_EXCLUDE="$(git -C "$DISCOVERY_TASK_WORKTREE" rev-parse --git-path info/exclude)"
if [[ "$DISCOVERY_GIT_EXCLUDE" != /* ]]; then
  DISCOVERY_GIT_EXCLUDE="$DISCOVERY_TASK_WORKTREE/$DISCOVERY_GIT_EXCLUDE"
fi
DISCOVERY_GIT_EXCLUDE_BACKUP="$WORK_DIR/context-discovery-git-exclude.backup"
cp "$DISCOVERY_GIT_EXCLUDE" "$DISCOVERY_GIT_EXCLUDE_BACKUP"
printf '/%s/context-discovery.json\n' "$DISCOVERY_TASK_REL" >>"$DISCOVERY_GIT_EXCLUDE"
for DISCOVERY_IGNORE_KIND in record check; do
  set +e
  if [[ "$DISCOVERY_IGNORE_KIND" == "record" ]]; then
    DISCOVERY_IGNORE_JSON="$(
      DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_TASK_RECORD" \
        --root "$DISCOVERY_TASK_WORKTREE" --json --mode standalone \
        --input "$DISCOVERY_INPUT" --task "$DISCOVERY_TASK_REL" \
        --expected-snapshot-sha256 "$DISCOVERY_SNAPSHOT_SHA256" 2>&1
    )"
  else
    DISCOVERY_IGNORE_JSON="$(
      DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_TASK_CHECK" \
        --root "$DISCOVERY_TASK_WORKTREE" --json \
        --input "$DISCOVERY_INPUT" --task "$DISCOVERY_TASK_REL" \
        --expected-snapshot-sha256 "$DISCOVERY_SNAPSHOT_SHA256" 2>&1
    )"
  fi
  DISCOVERY_IGNORE_STATUS=$?
  set -e
  if [[ "$DISCOVERY_IGNORE_STATUS" -eq 0 ]]; then
    echo "Context discovery accepted an ignored task artifact target: $DISCOVERY_IGNORE_KIND" >&2
    exit 2
  fi
  python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["error_codes"] == ["context_discovery_target_ignored"], payload' <<<"$DISCOVERY_IGNORE_JSON"
  test ! -e "$DISCOVERY_TASK_WORKTREE/$DISCOVERY_TASK_REL/context-discovery.json"
done
cp "$DISCOVERY_GIT_EXCLUDE_BACKUP" "$DISCOVERY_GIT_EXCLUDE"
python3 - "$DISCOVERY_TASK_WORKTREE/$DISCOVERY_TASK_REL/task.json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
payload["branch"] = "invalid branch"
path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
PY
DISCOVERY_REFRESH_INPUT="$WORK_DIR/context-discovery-refresh-input.json"
DISCOVERY_REFRESH_SNAPSHOT_SHA256="$(python3 - "$DISCOVERY_TASK_WORKTREE" "$DISCOVERY_INPUT" "$DISCOVERY_REFRESH_INPUT" <<'PY'
import copy
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
payload = copy.deepcopy(json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")))
runtime = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
spec = importlib.util.spec_from_file_location("installed_refresh_context_runtime", runtime)
if spec is None or spec.loader is None:
    raise SystemExit(f"could not load installed context discovery runtime: {runtime}")
gtt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gtt
spec.loader.exec_module(gtt)
superseded = payload["snapshot_identity"]["snapshot_sha256"]
payload["typed_exit"] = "refresh_base"
payload["refresh_history"] = [{
    "reason": "The active task branch no longer matches the feature worktree.",
    "error_codes": ["task_branch_stale"],
    "superseded_query_sha256": payload["canonical_query"]["query_sha256"],
    "superseded_snapshot_sha256": superseded,
    "detected_at": "2026-01-01T00:02:00Z",
}]
payload["snapshot_identity"] = gtt.context_snapshot_identity(payload)
Path(sys.argv[3]).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(payload["snapshot_identity"]["snapshot_sha256"])
PY
)"
set +e
DISCOVERY_NON_REFRESHABLE_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_TASK_RECORD" \
    --root "$DISCOVERY_TASK_WORKTREE" \
    --json \
    --mode standalone \
    --input "$DISCOVERY_REFRESH_INPUT" \
    --task "$DISCOVERY_TASK_REL" \
    --expected-snapshot-sha256 "$DISCOVERY_REFRESH_SNAPSHOT_SHA256" 2>&1
)"
DISCOVERY_NON_REFRESHABLE_STATUS=$?
set -e
if [[ "$DISCOVERY_NON_REFRESHABLE_STATUS" -eq 0 ]]; then
  echo "Context discovery accepted invalid_task_branch as refreshable" >&2
  exit 2
fi
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert "invalid_task_branch" in payload["error_codes"]; assert "refresh_base_has_non_refreshable_error" in payload["error_codes"]' <<<"$DISCOVERY_NON_REFRESHABLE_JSON"
python3 - "$DISCOVERY_TASK_WORKTREE/$DISCOVERY_TASK_REL/task.json" "$DISCOVERY_TASK_BRANCH" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
payload["branch"] = sys.argv[2] + "-stale"
path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
PY
DISCOVERY_REFRESH_TASK_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_TASK_RECORD" \
    --root "$DISCOVERY_TASK_WORKTREE" \
    --json \
    --mode standalone \
    --input "$DISCOVERY_REFRESH_INPUT" \
    --task "$DISCOVERY_TASK_REL" \
    --expected-snapshot-sha256 "$DISCOVERY_REFRESH_SNAPSHOT_SHA256"
)"
DISCOVERY_REFRESH_CHECK_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_TASK_CHECK" \
    --root "$DISCOVERY_TASK_WORKTREE" \
    --json \
    --task "$DISCOVERY_TASK_REL" \
    --expected-snapshot-sha256 "$DISCOVERY_REFRESH_SNAPSHOT_SHA256"
)"
python3 -c 'import json, sys; recorded = json.loads(sys.argv[1]); checked = json.load(sys.stdin); assert recorded["typed_exit"] == checked["typed_exit"] == "refresh_base"; assert recorded["snapshot_identity"]["snapshot_sha256"] == checked["snapshot_sha256"] == sys.argv[2]' "$DISCOVERY_REFRESH_TASK_JSON" "$DISCOVERY_REFRESH_SNAPSHOT_SHA256" <<<"$DISCOVERY_REFRESH_CHECK_JSON"
rm -rf "$DISCOVERY_TASK_WORKTREE/$DISCOVERY_TASK_REL"
mkdir -p "$DISCOVERY_TASK_WORKTREE/$DISCOVERY_ZERO_TASK_REL"
printf '%s\n' "{\"id\":\"context-discovery-zero\",\"status\":\"planning\",\"branch\":\"$DISCOVERY_TASK_BRANCH\"}" >"$DISCOVERY_TASK_WORKTREE/$DISCOVERY_ZERO_TASK_REL/task.json"
DISCOVERY_ZERO_TASK_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_TASK_RECORD" \
    --root "$DISCOVERY_TASK_WORKTREE" \
    --json \
    --mode standalone \
    --input "$DISCOVERY_ZERO_INPUT" \
    --task "$DISCOVERY_ZERO_TASK_REL" \
    --expected-snapshot-sha256 "$DISCOVERY_ZERO_SNAPSHOT_SHA256"
)"
DISCOVERY_ZERO_CHECK_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_TASK_CHECK" \
    --root "$DISCOVERY_TASK_WORKTREE" \
    --json \
    --task "$DISCOVERY_ZERO_TASK_REL" \
    --expected-snapshot-sha256 "$DISCOVERY_ZERO_SNAPSHOT_SHA256"
)"
python3 -c 'import json, sys; recorded = json.loads(sys.argv[1]); checked = json.load(sys.stdin); assert recorded["history_preview"]["candidates"] == []; assert recorded["mem_review"]["status"] == "not_needed"; assert recorded["snapshot_identity"]["snapshot_sha256"] == checked["snapshot_sha256"] == sys.argv[2]; assert checked["status"] == "passed"' "$DISCOVERY_ZERO_TASK_JSON" "$DISCOVERY_ZERO_SNAPSHOT_SHA256" <<<"$DISCOVERY_ZERO_CHECK_JSON"
git -C "$TARGET" worktree remove --force "$DISCOVERY_TASK_WORKTREE"
git -C "$TARGET" branch -D "$DISCOVERY_TASK_BRANCH" >/dev/null
test -z "$(git -C "$TARGET" status --porcelain=v1)"

PHASE0_FAKE_BIN="$WORK_DIR/phase0-fake-bin"
mkdir -p "$PHASE0_FAKE_BIN"
cat >"$PHASE0_FAKE_BIN/gh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "auth" && "${2:-}" == "status" ]]; then
  exit 0
fi
if [[ "${1:-}" == "issue" && "${2:-}" == "view" ]]; then
  printf '%s\n' '{"number":110,"title":"Verify Phase 0 stdout base facts","url":"https://github.com/castbox/guru-trellis-throwaway/issues/110","body":"Exercise installed workflow base synchronization across planner and mutation guards.","comments":[],"state":"OPEN"}'
  exit 0
fi
printf 'unexpected fake gh invocation: %s\n' "$*" >&2
exit 2
SH
chmod +x "$PHASE0_FAKE_BIN/gh"

PHASE0_RESOLUTION_JSON="$(
  "$TARGET/.agents/skills/guru-sync-base/scripts/sync-base.sh" \
    --root "$TARGET" \
    --mode workflow \
    --resolve-only \
    --base main \
    --remote origin
)"
PHASE0_RESOLUTION_DIGEST="$(python3 -c 'import json, sys; print(json.load(sys.stdin)["resolution_sha256"])' <<<"$PHASE0_RESOLUTION_JSON")"
SYNC_UPSTREAM="$WORK_DIR/base-sync-upstream"
git clone -q "$SYNC_REMOTE" "$SYNC_UPSTREAM"
git -C "$SYNC_UPSTREAM" config user.name "Throwaway Base Upstream"
git -C "$SYNC_UPSTREAM" config user.email "throwaway-base-upstream@example.invalid"
printf '%s\n' "remote advanced after workflow resolution" >"$SYNC_UPSTREAM/phase0-behind.txt"
git -C "$SYNC_UPSTREAM" add phase0-behind.txt
git -C "$SYNC_UPSTREAM" commit -q -m "test: advance throwaway base after resolution"
git -C "$SYNC_UPSTREAM" push -q origin main
PHASE0_RESULT_JSON="$(
  "$TARGET/.agents/skills/guru-sync-base/scripts/sync-base.sh" \
    --root "$TARGET" \
    --mode workflow \
    --execute \
    --expected-resolution-sha256 "$PHASE0_RESOLUTION_DIGEST" \
    --base main \
    --remote origin
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "synced"; assert payload["fresh"] is True; assert payload["git"]["fast_forwarded"] is True; assert payload["resolution"]["resolution_sha256"] == sys.argv[1]; assert payload["post_sync_resolution_sha256"] != sys.argv[1]' "$PHASE0_RESOLUTION_DIGEST" <<<"$PHASE0_RESULT_JSON"
PHASE0_VALIDATION_JSON="$(
  "$TARGET/.agents/skills/guru-sync-base/scripts/check-base-sync.sh" \
    --root "$TARGET" \
    --mode workflow \
    --result-json "$PHASE0_RESULT_JSON" \
    --expected-resolution-sha256 "$PHASE0_RESOLUTION_DIGEST"
)"
PHASE0_POST_DIGEST="$(python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "validated"; assert payload["mode"] == "workflow"; print(payload["post_sync_resolution_sha256"])' <<<"$PHASE0_VALIDATION_JSON")"
if [[ "$PHASE0_POST_DIGEST" == "$PHASE0_RESOLUTION_DIGEST" ]]; then
  echo "Fast-forwarded workflow validation did not return a new post-sync digest" >&2
  exit 2
fi

PHASE0_BRANCH="chore/110-phase0-stdout-facts"
PHASE0_ISSUE_URL="https://github.com/castbox/guru-trellis-throwaway/issues/110"
PHASE0_PLANNER_JSON="$(
  PATH="$PHASE0_FAKE_BIN:$PATH" \
  "$TARGET/.trellis/guru-team/scripts/bash/prepare-task.sh" \
    --root "$TARGET" \
    --json \
    --expected-resolution-sha256 "$PHASE0_POST_DIGEST" \
    --base-branch main \
    --branch "$PHASE0_BRANCH" \
    --short-name "110-phase0-stdout-facts" \
    --workspace-slug "110-phase0-stdout-facts" \
    --task-slug "110-phase0-stdout-facts" \
    --assignee throwaway \
    "$PHASE0_ISSUE_URL"
)"
PHASE0_PLANNER_POST_DIGEST="$(python3 -c 'import json, sys; payload = json.load(sys.stdin); freshness = payload["preflight"]["base_freshness"]; assert payload["source_issue"]["number"] == 110; assert payload["workspace_ready"] is False; assert freshness["reviewed_resolution_sha256"] == sys.argv[1]; assert freshness["three_way_equal"] is True; print(freshness["post_sync_resolution_sha256"])' "$PHASE0_POST_DIGEST" <<<"$PHASE0_PLANNER_JSON")"

PHASE0_STATUS_BEFORE="$(git -C "$TARGET" status --porcelain=v1)"
PHASE0_WORKTREES_BEFORE="$(git -C "$TARGET" worktree list --porcelain)"
set +e
PHASE0_LEGACY_MUTATION_JSON="$(
  PATH="$PHASE0_FAKE_BIN:$PATH" \
  "$TARGET/.trellis/guru-team/scripts/bash/prepare-task.sh" \
    --root "$TARGET" \
    --json \
    --expected-resolution-sha256 "$PHASE0_PLANNER_POST_DIGEST" \
    --base-branch main \
    --branch "$PHASE0_BRANCH" \
    --short-name "110-phase0-stdout-facts" \
    --workspace-slug "110-phase0-stdout-facts" \
    --task-slug "110-phase0-stdout-facts" \
    --assignee throwaway \
    --create-worktree \
    "$PHASE0_ISSUE_URL" 2>&1
)"
PHASE0_LEGACY_MUTATION_STATUS=$?
set -e
if [[ "$PHASE0_LEGACY_MUTATION_STATUS" -ne 2 ]]; then
  echo "Legacy prepare-task mutation did not fail with the migration exit" >&2
  exit 2
fi
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "error"; assert payload["migration"] == "guru-create-task-workspace"; assert payload["legacy_mutation_flags"] == ["--create-worktree"]; assert payload["required_prerequisite_skills"] == ["guru-sync-base", "guru-discover-change-context", "guru-clarify-requirements", "guru-review-contract-wording", "guru-review-change-request"]; assert payload["writes_performed"] is False' <<<"$PHASE0_LEGACY_MUTATION_JSON"
if [[ "$(git -C "$TARGET" status --porcelain=v1)" != "$PHASE0_STATUS_BEFORE" ]]; then
  echo "Legacy prepare-task mutation changed the working tree" >&2
  exit 2
fi
if [[ "$(git -C "$TARGET" worktree list --porcelain)" != "$PHASE0_WORKTREES_BEFORE" ]]; then
  echo "Legacy prepare-task mutation changed the worktree list" >&2
  exit 2
fi
if git -C "$TARGET" show-ref --verify --quiet "refs/heads/$PHASE0_BRANCH"; then
  echo "Legacy prepare-task mutation created the target branch" >&2
  exit 2
fi
cp "$SYNC_CONFIG_BACKUP" "$TARGET/.trellis/guru-team/config.yml"
git -C "$TARGET" add .trellis/guru-team/config.yml
git -C "$TARGET" commit -q -m "chore: restore throwaway preset config"
git -C "$TARGET" push -q origin main
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
    "design.md": "# 技术设计\n\n使用已安装 skill package、候选校验器与精确 executor。\n\n## Docs SSOT Plan\n\nStrategy: ssot_first.\n",
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

record_planning_contract_wording "$TASK_REL"
record_and_check_planning_approval "$TASK_REL" "initial"

record_throwaway_completed_agent() {
  local role="$1"
  local agent_id="$2"
  local nickname="$3"
  "$TARGET/.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --source-repo "$TARGET" \
    --agent-id "$agent_id" \
    --event assigned \
    --logical-role "$role" \
    --platform-nickname "$nickname" \
    --evidence "Throwaway assigned $role for installed guru-check-task verification." \
    --json >/dev/null
  "$TARGET/.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --source-repo "$TARGET" \
    --agent-id "$agent_id" \
    --event completed \
    --evidence "Throwaway $role completed its full assigned scope." \
    --json >/dev/null
}

record_throwaway_completed_agent "实现代理" "throwaway-implement" "Throwaway Implement"
record_throwaway_completed_agent "阶段二检查代理" "throwaway-check" "Throwaway Check"

record_throwaway_phase2() {
  local summary="$1"
  local input_path
  local record_json
  local check_json
  input_path="$(mktemp "${TMPDIR:-/tmp}/guru-phase2-input.XXXXXX.json")"
  python3 - "$TARGET" "$TASK_REL" "$summary" "$input_path" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
task_rel = sys.argv[2]
summary = sys.argv[3]
output = Path(sys.argv[4])
payload = json.loads((
    root / ".trellis/guru-team/skills/packages/guru-check-task/examples/phase2-check.json"
).read_text(encoding="utf-8"))
payload["mode"] = "workflow"
payload["requirement_provenance"] = {
    "summary": "已复核 throwaway task 的 approved requirement provenance。",
    "artifacts": [{"path": f"{task_rel}/prd.md"}],
    "facts_sha256": "0" * 64,
}
payload["docs_ssot_plan"].update({
    "strategy": "ssot_first",
    "durable_paths": [{"path": ".trellis/workflow.md"}],
    "sync_result": "已安装的 canonical workflow 是本次 smoke 的 durable SSOT 输入。",
    "task_delta_merged": True,
    "task_history_only": ["throwaway implementation and check evidence"],
    "no_update_reason": None,
    "followup_or_pr_limit": None,
})
payload["implementation_handoff"] = {
    "summary": "已完成 throwaway implementation handoff，并覆盖文件、测试与 Docs SSOT。",
    "artifacts": [{"path": f"{task_rel}/implement.md"}],
    "facts_sha256": "0" * 64,
}
payload["agent_assignment"].update({
    "implementation_agent_ids": ["throwaway-implement"],
    "check_agent_ids": ["throwaway-check"],
})
payload["repository_snapshot"]["reviewed_paths"] = [
    {"path": "src/task-commit-smoke.txt"},
]
payload["check_execution"]["commands"] = [{
    "id": "installed-guru-check-task-smoke",
    "argv": ["check installed package, schema, workflow, and task commit path"],
    "exit_code": 0,
    "stdout_sha256": "0" * 64,
    "stdout_size_bytes": 0,
    "stderr_sha256": "0" * 64,
    "stderr_size_bytes": 0,
    "summary": summary,
}]
payload["check_execution"]["worker_evidence"] = [{
    "source": "official_trellis_check",
    "agent_id": "throwaway-check",
    "summary": "Unchanged official trellis-check supplied evidence only.",
    "evidence_only": True,
    "facts_sha256": "0" * 64,
}]
payload["semantic_review"]["ai_review_gate"]["summary"] = summary
output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
  record_json="$("$TARGET/.agents/skills/guru-check-task/scripts/record-phase2-check.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --input "$input_path" \
    --json)"
  check_json="$("$TARGET/.agents/skills/guru-check-task/scripts/check-phase2-check.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --json)"
  rm -f "$input_path"
  python3 -c 'import json,sys; recorded=json.loads(sys.argv[1]); checked=json.load(sys.stdin); assert recorded["schema_version"] == "2.0"; assert recorded["skill_id"] == "guru-check-task"; assert recorded["typed_exit"] == checked["typed_exit"] == "passed"; assert checked["consumer"] == {"kind":"skill","id":"guru-create-task-commit"}' "$record_json" <<<"$check_json"
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
INITIAL_TASK_WORKSPACE_JSON="$(python3 "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py" --installed-repo "$TARGET" --work-root "$WORK_DIR/installed-task-workspace-initial")"
printf '%s\n' "$INITIAL_TASK_WORKSPACE_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["typed_exit"] == "created"; assert payload["checker_status"] == "passed"; assert payload["artifact_names"] == ["context-discovery.json", "issue-review.json", "issue-scope-ledger.json", "task-start-context.json"]; assert payload["task_creator"] == "fixture-maintainer"; assert payload["developer_identity_preserved"] is False; assert not any(payload[key] for key in ("source_developer_identity", "target_developer_identity", "source_workspace_journal", "target_workspace_journal"))' <<<"$INITIAL_TASK_WORKSPACE_JSON"

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
ownership_checkpoint "post-update-before-workflow-and-preset-reapply"
(
  cd "$TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force
)
apply_local_workflow_sample
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$TARGET" \
  --platform claude \
  --platform codex \
  --platform cursor
ownership_checkpoint "post-preset-reapply-before-final-checks"

if [[ "$(workspace_tree_digest "$TARGET/.trellis/workspace")" != "$WORKSPACE_TREE_DIGEST_BEFORE" ]]; then
  echo "Update/reapply modified existing official workspace content" >&2
  exit 2
fi
if [[ "$(file_sha256 "$TARGET/.trellis/.developer")" != "$DEVELOPER_IDENTITY_DIGEST_BEFORE" ]]; then
  echo "Update/reapply modified existing official developer identity" >&2
  exit 2
fi

grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-discover-change-context","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-clarify-requirements","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"retarget_context","consumer":{"kind":"skill","id":"guru-sync-base"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-review-contract-wording","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-review-change-request","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"ready","consumer":{"kind":"skill","id":"guru-create-task-workspace"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"clarify_requirements","consumer":{"kind":"skill","id":"guru-clarify-requirements"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"review_wording","consumer":{"kind":"skill","id":"guru-review-contract-wording"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"refresh_context","consumer":{"kind":"skill","id":"guru-sync-base"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-review-change-request","exit":"blocked","consumer":{"kind":"stop","id":"change-request-review-blocked"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-create-task-workspace","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"created","consumer":{"kind":"workflow","id":"guru-task-workspace-created"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"refresh_review","consumer":{"kind":"skill","id":"guru-sync-base"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"cancelled","consumer":{"kind":"stop","id":"task-workspace-cancelled"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"blocked","consumer":{"kind":"stop","id":"task-workspace-blocked"}}' "$TARGET/.trellis/workflow.md"
test -f "$TARGET/.trellis/guru-team/schemas/finish-summary.schema.json"
test -f "$TARGET/.trellis/guru-team/schemas/closeout-plan.schema.json"
test -x "$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/run-skill-command.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/sync-base.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-base-sync.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/preview-change-context-history.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-context-discovery.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-context-discovery.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-requirements-clarification.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-requirements-clarification.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-contract-wording-review.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-contract-wording-review.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-change-request-review.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-change-request-review.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-task-workspace-plan.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/create-task-workspace.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-task-workspace-result.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/create-task-commit.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-commit/SKILL.md"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-sync-base/SKILL.md"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-discover-change-context/SKILL.md"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-clarify-requirements/SKILL.md"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-review-contract-wording/SKILL.md"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-review-change-request/SKILL.md"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-workspace/SKILL.md"
test -x "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-workspace/scripts/create-task-workspace.sh"
test -x "$TARGET/.agents/skills/guru-create-task-commit/scripts/create-task-commit.sh"
"$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh" --help >/dev/null
test -x "$TARGET/.claude/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -x "$TARGET/.codex/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -x "$TARGET/.cursor/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -x "$TARGET/.claude/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.codex/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.cursor/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.agents/skills/guru-sync-base/scripts/sync-base.sh"
test -x "$TARGET/.claude/skills/guru-sync-base/scripts/sync-base.sh"
test -x "$TARGET/.codex/skills/guru-sync-base/scripts/sync-base.sh"
test -x "$TARGET/.cursor/skills/guru-sync-base/scripts/sync-base.sh"
test -x "$TARGET/.agents/skills/guru-discover-change-context/scripts/preview-change-context-history.sh"
test -x "$TARGET/.claude/skills/guru-discover-change-context/scripts/preview-change-context-history.sh"
test -x "$TARGET/.codex/skills/guru-discover-change-context/scripts/preview-change-context-history.sh"
test -x "$TARGET/.cursor/skills/guru-discover-change-context/scripts/preview-change-context-history.sh"
test -x "$TARGET/.agents/skills/guru-clarify-requirements/scripts/record-requirements-clarification.sh"
test -x "$TARGET/.claude/skills/guru-clarify-requirements/scripts/check-requirements-clarification.sh"
test -x "$TARGET/.codex/skills/guru-clarify-requirements/scripts/check-requirements-clarification.sh"
test -x "$TARGET/.cursor/skills/guru-clarify-requirements/scripts/check-requirements-clarification.sh"
test -x "$TARGET/.agents/skills/guru-review-contract-wording/scripts/record-contract-wording-review.sh"
test -x "$TARGET/.claude/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh"
test -x "$TARGET/.codex/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh"
test -x "$TARGET/.cursor/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh"
test -x "$TARGET/.agents/skills/guru-review-change-request/scripts/record-change-request-review.sh"
test -x "$TARGET/.claude/skills/guru-review-change-request/scripts/check-change-request-review.sh"
test -x "$TARGET/.codex/skills/guru-review-change-request/scripts/check-change-request-review.sh"
test -x "$TARGET/.cursor/skills/guru-review-change-request/scripts/check-change-request-review.sh"
test -f "$TARGET/.agents/skills/guru-create-task-workspace/SKILL.md"
test -x "$TARGET/.agents/skills/guru-create-task-workspace/scripts/record-task-workspace-plan.sh"
test -x "$TARGET/.claude/skills/guru-create-task-workspace/scripts/create-task-workspace.sh"
test -x "$TARGET/.codex/skills/guru-create-task-workspace/scripts/create-task-workspace.sh"
test -x "$TARGET/.cursor/skills/guru-create-task-workspace/scripts/check-task-workspace-result.sh"
"$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$REPO_ROOT" --json --mode source >/dev/null
"$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$TARGET" --json --mode installed >/dev/null
DISCOVERY_AFTER_UPDATE_JSON="$(
  "$TARGET/.agents/skills/guru-discover-change-context/scripts/preview-change-context-history.sh" \
    --root "$TARGET" \
    --json \
    --issue-ref '#111' \
    --command preview-change-context-history
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["algorithm_id"] == "guru-context-history-score-1.0"; assert any(row["finish_summary_path"].endswith("context-discovery-fixture/finish-summary.json") for row in payload["candidates"])' <<<"$DISCOVERY_AFTER_UPDATE_JSON"
verify_requirements_clarification_exits "after-update"
verify_contract_wording_standalone_profiles "after-update"
verify_change_request_review_package "after-update"
POST_UPDATE_TASK_REL=".trellis/tasks/07-17-114-contract-wording-after-update"
POST_UPDATE_BRANCH="$(git -C "$TARGET" branch --show-current)"
POST_UPDATE_HEAD="$(git -C "$TARGET" rev-parse HEAD)"
python3 - "$TARGET" "$POST_UPDATE_TASK_REL" "$POST_UPDATE_BRANCH" "$POST_UPDATE_HEAD" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
task_rel = sys.argv[2]
branch = sys.argv[3]
head = sys.argv[4]
task_dir = root / task_rel
task_dir.mkdir(parents=True)
task = {
    "id": "contract-wording-after-update",
    "name": "contract-wording-after-update",
    "title": "Post-update contract wording review",
    "status": "planning",
    "branch": branch,
    "base_branch": "main",
}
context = {
    "schema_version": "1.0",
    "source_issue": {
        "number": 114,
        "url": "https://github.com/castbox/guru-trellis/issues/114",
        "title": "Post-update contract wording review",
        "created_by_workflow": False,
    },
    "source_repo": {
        "repo": "castbox/guru-trellis-throwaway",
        "url": "https://github.com/castbox/guru-trellis-throwaway",
    },
    "task_slug": "contract-wording-after-update",
    "task_title": "Post-update contract wording review",
    "task_artifact_dir": task_rel,
    "branch_name": branch,
    "base_branch": "main",
    "base_ref": "main",
    "base_head_sha": head,
    "remote_head_sha": head,
    "workspace_slug": "",
    "task_workspace_id": "contract-wording-after-update",
    "assignee": "throwaway",
    "actor": {"login": "throwaway"},
    "issue_scope_ledger_seed": {},
    "intake_summary": {},
}
ledger = {
    "schema_version": "1.0",
    "primary_issue": {"number": 114},
    "close_issues": [{"number": 114}],
    "related_issues": [],
    "followup_issues": [],
}
for name, payload in (
    ("task.json", task),
    ("task-start-context.json", context),
    ("issue-scope-ledger.json", ledger),
):
    (task_dir / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(task_dir / "prd.md").write_text(
    "# Post-update wording review\n\nThe required planning scope remains exact.\n", encoding="utf-8"
)
(task_dir / "design.md").write_text(
    "# Post-update design\n\nThe installed checker rebuilds all three planning artifacts.\n\n"
    "## Docs SSOT Plan\n\nStrategy: ssot_first.\n",
    encoding="utf-8",
)
(task_dir / "implement.md").write_text(
    "# Post-update implementation\n\nRecord and validate the current installed planning evidence.\n", encoding="utf-8"
)
PY
record_planning_contract_wording "$POST_UPDATE_TASK_REL"
record_and_check_planning_approval "$POST_UPDATE_TASK_REL" "after-update"
"$TARGET/.agents/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh" \
  --root "$TARGET" --json --task "$POST_UPDATE_TASK_REL" >/dev/null
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh"
BACKFILL_AFTER_UPDATE_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/backfill-finish-summary.sh" --root "$TARGET" --json --dry-run)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["mode"] == "dry-run"; assert payload["scanned_tasks"] == 2; assert len(payload["skipped"]) == 2; assert all(row["reason"] == "finish-summary exists" for row in payload["skipped"]); assert payload["errors"] == []' <<<"$BACKFILL_AFTER_UPDATE_JSON"
grep -q '^session_auto_commit: false$' "$TARGET/.trellis/config.yaml"
grep -q '^\.trellis/workspace/$' "$TARGET/.gitignore"

UPDATED_CLOSEOUT_JSON="$(python3 "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_closeout.py" --repo "$TARGET" --case after-update)"
printf '%s\n' "$UPDATED_CLOSEOUT_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["issue"] == 106; assert payload["local_head"] == payload["remote_head"] == payload["pr_head"]; assert payload["pr_ready"] is True; assert payload["after_archive_hook_preflight"] is True' <<<"$UPDATED_CLOSEOUT_JSON"
UPDATED_TASK_WORKSPACE_JSON="$(python3 "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py" --installed-repo "$TARGET" --work-root "$WORK_DIR/installed-task-workspace-after-update" --existing-developer-identity)"
printf '%s\n' "$UPDATED_TASK_WORKSPACE_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["typed_exit"] == "created"; assert payload["checker_status"] == "passed"; assert payload["artifact_names"] == ["context-discovery.json", "issue-review.json", "issue-scope-ledger.json", "task-start-context.json"]; assert payload["task_creator"] == "fixture-maintainer"; assert payload["developer_identity_preserved"] is True; assert all(payload[key] for key in ("source_developer_identity", "target_developer_identity")); assert not any(payload[key] for key in ("source_workspace_journal", "target_workspace_journal"))' <<<"$UPDATED_TASK_WORKSPACE_JSON"

ABSENCE_TARGET="$WORK_DIR/no-developer-project"
mkdir "$ABSENCE_TARGET"
git -C "$ABSENCE_TARGET" init -q
git -C "$ABSENCE_TARGET" remote add origin https://github.com/castbox/guru-trellis-throwaway.git
git -C "$ABSENCE_TARGET" config user.name "Guru Team No Developer Fixture"
git -C "$ABSENCE_TARGET" config user.email "guru-team-no-developer@example.invalid"
git -C "$ABSENCE_TARGET" branch -M main
printf '%s\n' 'no-developer repository baseline' >"$ABSENCE_TARGET/.throwaway-baseline"
git -C "$ABSENCE_TARGET" add .throwaway-baseline
git -C "$ABSENCE_TARGET" commit -q -m "chore: initialize no-developer fixture"
(
  cd "$ABSENCE_TARGET"
  trellis init -y --claude --codex --cursor \
    --workflow guru-team \
    --workflow-source "$WORKFLOW_SOURCE"
)
apply_local_workflow_sample "$ABSENCE_TARGET"
test -f "$ABSENCE_TARGET/.trellis/.developer"
test -d "$ABSENCE_TARGET/.trellis/workspace"
rm -rf "$ABSENCE_TARGET/.trellis/.developer" "$ABSENCE_TARGET/.trellis/workspace"
assert_official_state_absent "$ABSENCE_TARGET" "no-developer fixture setup"
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$ABSENCE_TARGET" \
  --platform claude \
  --platform codex \
  --platform cursor
assert_official_state_absent "$ABSENCE_TARGET" "initial preset apply"
(
  cd "$ABSENCE_TARGET"
  trellis update --force
)
assert_official_state_absent "$ABSENCE_TARGET" "trellis update"
(
  cd "$ABSENCE_TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force
)
apply_local_workflow_sample "$ABSENCE_TARGET"
assert_official_state_absent "$ABSENCE_TARGET" "workflow reapply"
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$ABSENCE_TARGET" \
  --platform claude \
  --platform codex \
  --platform cursor
assert_official_state_absent "$ABSENCE_TARGET" "preset reapply"
"$ABSENCE_TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$ABSENCE_TARGET" --json --mode installed >/dev/null
ABSENCE_SIDECARS="$(find "$ABSENCE_TARGET" -type f \( -name '*.new' -o -name '*.bak' \) -print)"
if [[ -n "$ABSENCE_SIDECARS" ]]; then
  echo "Unexpected no-developer fixture sidecars after update/reapply:" >&2
  printf '%s\n' "$ABSENCE_SIDECARS" >&2
  exit 2
fi

fail_if_python_cache "throwaway target" "$TARGET"
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
