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
  printf 'Current Guru ownership checkpoint: %s\n' "$checkpoint"
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

verify_task_publication_validator_wrappers() {
  local label="$1"
  printf 'Task publication validator wrapper smoke: %s\n' "$label"
  python3 - "$TARGET" "$label" <<'PY'
import json
import os
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
label = sys.argv[2]
skill_id = "guru-review-task-publication"
layouts = {
    "installed-shared": root / ".trellis/guru-team/skills/packages" / skill_id,
    "agents": root / ".agents/skills" / skill_id,
    "codex": root / ".codex/skills" / skill_id,
    "cursor": root / ".cursor/skills" / skill_id,
    "claude": root / ".claude/skills" / skill_id,
}
interface = json.loads(
    (layouts["installed-shared"] / "interface.json").read_text(encoding="utf-8")
)
validator_ids = {
    "publication_review_recorder",
    "publication_review_checker",
}
validators = {
    item["id"]: item
    for item in interface["validators"]
    if item["id"] in validator_ids
}
if set(validators) != validator_ids:
    raise SystemExit(
        f"{label}: publication validator command declarations drifted: "
        f"{sorted(validators)}"
    )

env = os.environ.copy()
env.pop("GURU_TEAM_DISPATCHER", None)
for layout, package_root in layouts.items():
    if not package_root.is_dir():
        raise SystemExit(f"{label}: missing publication layout: {layout}")
    for validator_id in sorted(validator_ids):
        validator = validators[validator_id]
        command = package_root / validator["command"]
        result = subprocess.run(
            [str(command), "--help"],
            cwd=root,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        expected_usage = (
            "usage: guru_team_trellis.py "
            f"{validator['runtime_command']}"
        )
        if result.returncode != 0 or expected_usage not in result.stdout:
            raise SystemExit(
                f"{label}: {layout}/{validator_id} did not reach the "
                f"shared dispatcher help (rc={result.returncode}, "
                f"stderr={result.stderr!r})"
            )
print(f"{label}: 10/10 publication validator wrappers reached shared help")
PY
}

verify_finish_family_integration() {
  local label="$1"
  printf 'Installed Finish-family integration: %s\n' "$label"
  GURU_FINISH_INTEGRATION_MODE=installed \
    GURU_FINISH_INTEGRATION_ROOT="$TARGET" \
    python3 "$TARGET/.trellis/guru-team/skills/tests/test_finish_family_integration.py" -q
}

verify_issue_174_controlled_replay() {
  printf 'Issue #174 controlled replay counters\n'
  local replay_root="$WORK_DIR/issue-174-controlled-replay"
  local report="$replay_root/report.json"
  mkdir -p "$replay_root"
  GURU_FINISH_INTEGRATION_MODE=installed \
    GURU_FINISH_INTEGRATION_ROOT="$TARGET" \
    GURU_ISSUE_174_REPLAY_REPORT="$report" \
    python3 "$TARGET/.trellis/guru-team/skills/tests/test_finish_family_integration.py" \
      FinishFamilyIntegrationTests.test_issue_174_controlled_replay_is_one_chained_session \
      -q
  python3 - "$report" <<'PY'
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if report.get("status") != "passed" or report.get("terminal_artifacts") != []:
    raise SystemExit("controlled replay report is incomplete or non-terminal")
print(json.dumps(report, indent=2, sort_keys=True))
PY
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

if [[ "${1:-}" == "auth" && "${2:-}" == "status" ]]; then
  exit 0
fi

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

printf '{"number":%s,"title":"Reviewed source issue","url":"https://github.com/example/guru-extension/issues/%s","state":"%s","updatedAt":"%s","body":"Reviewed source issue body.","comments":[],"assignees":[],"labels":[]}\n' \
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
        "disposition_digest": "0" * 64,
    }
    return derive(payload)


def finalized(payload):
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
    )
    return finalized(payload)


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
    return finalized(payload)


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
    )
    return finalized(payload)


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
    )
    return finalized(payload)


def add_authority_round(payload, *, impact, action_ids):
    payload = copy.deepcopy(payload)
    payload["clarification_rounds"] = [{
        "round_id": "round_authority",
        "question_id": "acceptance_boundary",
        "atomic_group_id": None,
        "atomic_group_reason": None,
        "category": "product_intent",
        "question": "Which acceptance boundary is authoritative?",
        "answer_summary": "The exact acceptance boundary was selected.",
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
    "status": "missing",
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
)
retain_draft = finalized(retain_draft)
retain_issue = disposition(
    issue_target(example),
    "keep_current_open_issue",
    candidates=[rejected],
)
retain_issue = finalized(retain_issue)
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

wrong_disposition = copy.deepcopy(cases["retarget_context"])
wrong_disposition["target_disposition"]["disposition_digest"] = "f" * 64
if "requirements_target_disposition_digest_mismatch" not in gtt.requirements_clarification_structural_errors(
    root, wrong_disposition, None
):
    raise SystemExit("installed retarget fixture accepted a stale disposition digest")

stale_action = copy.deepcopy(cases["retarget_context"])
stale_action["source_actions"][0]["payload"]["updated_at"] = "2026-01-01T00:00:09Z"
stale_action = derive(stale_action)
if "select_existing_issue_action_binding_invalid" not in gtt.requirements_clarification_structural_errors(
    root, stale_action, None
):
    raise SystemExit("installed retarget fixture accepted stale selected action")

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
                "rescan_sha256": live_scan["scan_sha256"],
                "change_request_mutation": {
                    "source_identity": body_item["source_identity"],
                    "locator": body_item["id"],
                    "field": "body",
                    "preimage_sha256": "0" * 64,
                    "reread_content_sha256": body_item["content_sha256"],
                    "source_updated_at": body_item["updated_at"],
                },
            }],
            "classifications": [],
            "ai_review_gate": {
                "status": "passed",
                "reviewer": "throwaway-live-mutation-review",
                "summary": "The installed runtime reviewed the exact mutation target and current reread result.",
                "reviewed_scan_sha256": live_scan["scan_sha256"],
                "checked_dimensions": {
                    name: True for name in gtt.CONTRACT_WORDING_REVIEW_DIMENSIONS
                },
            },
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
  local changed_result="$probe_dir/planning_artifacts.content_changed.result.json"
  local pass_result="$probe_dir/planning_artifacts.pass.result.json"
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
            "reason": "The reviewed wording rewrite is already reflected in current bytes.",
            "rescan_sha256": scan["scan_sha256"],
        }],
        "classifications": [
            dict(row) for row in classifications
        ],
        "ai_review_gate": dict(gate),
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
    --task "$task_rel" --input "$changed_input" >"$changed_result"
  "$TARGET/.agents/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh" \
    --root "$TARGET" --json --task "$task_rel" --input "$changed_result" >/dev/null
  "$TARGET/.agents/skills/guru-review-contract-wording/scripts/record-contract-wording-review.sh" \
    --root "$TARGET" --json --mode workflow --profile planning_artifacts \
    --task "$task_rel" --input "$input" >"$pass_result"
  "$TARGET/.agents/skills/guru-review-contract-wording/scripts/check-contract-wording-review.sh" \
    --root "$TARGET" --json --task "$task_rel" --input "$pass_result" >/dev/null
  test ! -e "$TARGET/$task_rel/contract-wording-review.json"
  python3 - "$pass_result" "$changed_result" "$TARGET" "$task_rel" "$bytes_before" <<'PY'
import json
import sys

payload = json.load(open(sys.argv[1], encoding="utf-8"))
changed = json.load(open(sys.argv[2], encoding="utf-8"))
root = __import__("pathlib").Path(sys.argv[3])
task_rel = sys.argv[4]
before = json.load(open(sys.argv[5], encoding="utf-8"))
assert payload["typed_exit"] == "pass"
assert payload["semantic_review"]["revisions"] == []
assert changed["typed_exit"] == "content_changed"
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
  local public_input="$TARGET/.trellis/.runtime/guru-team/throwaway-inputs/planning-approval-$phase.json"
  local owner_result
  local public_output
  python3 - "$TARGET" "$task_rel" "$input" "$phase" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
task_rel = sys.argv[2]
output = Path(sys.argv[3])
phase = sys.argv[4]
task_dir = root / task_rel
authored = {
    "mode": "workflow",
    "authority_refs": [f"task:{task_rel}/prd.md"],
    "docs_ssot_plan": {
        "strategy": "ssot_first",
        "durable_paths": [".trellis/workflow.md"],
        "summary": "The durable workflow contract is updated before implementation.",
    },
    "semantic_review": {
        "status": "passed",
        "summary": "The installed planning package reviewed the disposable task for activation.",
        "checked_dimensions": {
            name: True for name in (
                "requirement_authority",
                "scope_boundary",
                "design_adequacy",
                "implementation_plan",
                "acceptance_verifiability",
                "docs_ssot",
                "provenance",
                "unusual_scenarios",
            )
        },
        "findings": [],
        "revision_actions": [],
        "scope_proposals": [],
        "blocking_reasons": [],
    },
    "typed_exit": "approved",
    "consumer": {"kind": "workflow", "id": "phase-1-task-activation"},
    "reason": f"The installed planning recorder and checker path is under test for {phase}.",
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
  python3 -c 'import json,sys; payload=json.load(open(sys.argv[1], encoding="utf-8")); assert payload["schema_version"] == "3.0"; assert payload["skill_id"] == "guru-approve-task-plan"; assert payload["typed_exit"] == "approved"' "$result"
  owner_result="$(python3 -c 'import json,pathlib,sys; root=pathlib.Path(sys.argv[1]).resolve(); path=pathlib.Path(json.load(open(sys.argv[2], encoding="utf-8"))["artifact_path"]).resolve(); print(path.relative_to(root).as_posix())' "$TARGET" "$result")"
  mkdir -p "$(dirname "$public_input")"
  python3 - "$task_rel" "$public_input" <<'PY'
import json
import sys
from pathlib import Path

Path(sys.argv[2]).write_text(
    json.dumps(
        {
            "profile": "initial_review",
            "mode": "workflow",
            "task_ref": sys.argv[1],
            "source_exit": "planning_ready",
        },
        ensure_ascii=False,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)
PY
  public_output="$(
    "$TARGET/.agents/skills/guru-approve-task-plan/scripts/invoke.sh" \
      --input "${public_input#"$TARGET/"}" \
      --owner-result "$owner_result"
  )"
  rm -f "$public_input"
  python3 -c 'import json,pathlib,sys; payload=json.load(sys.stdin); assert payload == {"exit_id":"approved","task_ref":sys.argv[1]}; assert not (pathlib.Path(sys.argv[2]) / sys.argv[3]).exists()' "$task_rel" "$TARGET" "$owner_result" <<<"$public_output"
  printf '%s\n' "$public_output"
}

prepare_task_commit_candidate() {
  local profile="$1"
  local subject="$2"
  local passed_dto="$3"
  local input_path
  local authoring_json
  local prepared_json
  input_path="$(mktemp "${TMPDIR:-/tmp}/guru-task-commit-input.XXXXXX")"
  authoring_json="$(python3 - "$TARGET" "$TASK_REL" "$profile" "$subject" "$input_path" "$passed_dto" <<'PY'
import importlib.util
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
task_rel = sys.argv[2]
profile = sys.argv[3]
subject = sys.argv[4]
input_path = Path(sys.argv[5])
passed_dto = json.loads(sys.argv[6])
runtime = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
spec = importlib.util.spec_from_file_location("installed_task_commit_runtime", runtime)
if spec is None or spec.loader is None:
    raise SystemExit(f"could not load installed task commit runtime: {runtime}")
gtt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gtt
spec.loader.exec_module(gtt)

task_dir = root / task_rel
snapshot = gtt.task_commit_snapshot_without_digest(
    gtt.capture_task_commit_snapshot(root, set())
)
unrelated = "unrelated-preserved.log"
classifications = []
for entry in snapshot["entries"]:
    path = str(entry["path"])
    is_unrelated = path == unrelated
    classifications.append({
        "path": path,
        "category": "unrelated-preserved" if is_unrelated else "task-reviewed",
        "reason": "Preserve unrelated throwaway state." if is_unrelated else "Fresh throwaway Phase 2 evidence covers this path.",
        "coverage_source": "AI throwaway scope review" if is_unrelated else "guru-check-task passed DTO",
    })

ledger = gtt.read_json(task_dir / "issue-scope-ledger.json")
primary_issue = int(ledger["primary_issue"]["number"])
subject_match = re.fullmatch(
    r"(?P<type>[a-z]+)\((?P<scope>[a-z0-9._/-]+)\): #(?P<issue>[1-9][0-9]*) (?P<summary>.+)",
    subject,
)
if subject_match is None or int(subject_match.group("issue")) != primary_issue:
    raise SystemExit(f"unsupported throwaway task commit subject: {subject}")
if passed_dto != {
    "exit_id": "passed",
    "task_ref": task_rel,
    "phase2_commit_anchor": passed_dto.get("phase2_commit_anchor"),
}:
    raise SystemExit(f"invalid guru-check-task passed DTO: {passed_dto}")
public_input = {
    "profile": profile,
    "mode": "workflow",
    "task_ref": passed_dto["task_ref"],
    "source_exit": passed_dto["exit_id"],
    "phase2_commit_anchor": passed_dto["phase2_commit_anchor"],
}
input_path.write_text(
    json.dumps(public_input, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
authoring = {
    "path_classifications": classifications,
    "message": {
        "type": subject_match.group("type"),
        "scope": subject_match.group("scope"),
        "summary": subject_match.group("summary"),
        "background": "需要验证安装后的 task commit 闭环。",
        "changes": "提交当前轮次经过检查的精确路径。",
        "boundaries": "保留无关工作区状态且不执行 push。",
        "validations": "候选校验与真实提交后置条件均通过。",
    },
    "ai_review": {
        "status": "passed",
        "summary": "Reviewed the exact fixture paths, message, upgrade boundary and unrelated preservation.",
        "evidence": ["Fresh Phase 2 evidence covers every task-reviewed fixture path."],
    },
    "routine_auto_commit_eligible": {
        "eligible": True,
        "reason": "The isolated unpublished task worktree has one current scope, canonical message and no remote consumer.",
        "evidence_refs": [
            "dedicated_task_worktree",
            "dedicated_task_branch",
            "default_branch_excluded",
            "protected_branch_excluded",
            "shared_branch_excluded",
            "other_task_branch_excluded",
            "remote_branch_absent",
            "open_pull_request_absent",
            "phase2_current",
            "exact_task_owned_staging",
            "ordinary_new_commit",
            "scope_purpose_unique",
            "authority_unchanged",
            "canonical_message_unique",
        ],
    },
}
print(json.dumps(authoring, ensure_ascii=False, separators=(",", ":")))
PY
  )"
  prepared_json="$(
    "$TARGET/.agents/skills/guru-create-task-commit/scripts/prepare-task-commit.sh" \
      --root "$TARGET" \
      --json \
      --input "$input_path" \
      --candidate-json "$authoring_json"
  )"
  rm -f "$input_path"
  python3 -c 'import json,sys; payload=json.load(sys.stdin); assert payload["status"] == "prepared"; assert payload["typed_exit"] == "committed"; assert payload["message"]["subject"] == sys.argv[1]; print(payload["candidate_artifact"])' "$subject" <<<"$prepared_json"
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

WORKSPACE_TREE_DIGEST_BEFORE="$(workspace_tree_digest "$TARGET/.trellis/workspace")"
DEVELOPER_IDENTITY_DIGEST_BEFORE="$(file_sha256 "$TARGET/.trellis/.developer")"

"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$TARGET" \
  --platform claude \
  --platform codex \
  --platform cursor

test -f "$TARGET/.trellis/workflow.md"
grep -q "Guru Team Development Workflow" "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-review-branch","required":true}' "$TARGET/.trellis/workflow.md"
! grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"
grep -q 'Planning produces non-empty `prd.md`, `design.md`, and `implement.md`' "$TARGET/.trellis/workflow.md"
! grep -q "record-agent-recovery.sh" "$TARGET/.trellis/workflow.md"
! grep -q "check-agent-recovery.sh" "$TARGET/.trellis/workflow.md"
! grep -q "record-subagent-liveness-event.sh" "$TARGET/.trellis/workflow.md"
! grep -q "check-subagent-liveness.sh" "$TARGET/.trellis/workflow.md"
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
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"blocked","consumer":{"kind":"stop","id":"task-workspace-blocked"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-invoke: {"skill":"guru-merge-task-pr","required":true}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-finalize-task","exit":"ready_for_merge","consumer":{"kind":"skill","id":"guru-merge-task-pr"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-merge-task-pr","exit":"merged","consumer":{"kind":"workflow","id":"guru-finalization-finish-response"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-merge-task-pr","exit":"merge_blocked","consumer":{"kind":"stop","id":"task-pr-merge-blocked"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-skill-exit: {"skill":"guru-merge-task-pr","exit":"closure_mismatch","consumer":{"kind":"stop","id":"task-pr-closure-mismatch"}}' "$TARGET/.trellis/workflow.md"
grep -q 'guru-stop-target: {"id":"change-request-review-blocked"}' "$TARGET/.trellis/workflow.md"
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
test -x "$TARGET/.trellis/guru-team/scripts/bash/discover-skill-contract.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/discover-skill-evals.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/run-skill-evals.sh"
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
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-agent-recovery.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-agent-recovery.sh"
test ! -e "$TARGET/.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh"
test ! -e "$TARGET/.trellis/guru-team/scripts/bash/check-subagent-liveness.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/execute-extension-verification.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-extension-verification.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-extension-verification.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/invoke-extension-verification.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/preview-finalization.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-finalization-gate.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-finalization-gate.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/execute-finalization-transition.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/preview-task-pr-merge.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-task-pr-merge.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-task-pr-merge.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/execute-task-pr-merge.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/invoke-task-pr-merge.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-commit-messages.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/create-task-commit.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/format-merge-commit.sh"
test -f "$TARGET/.trellis/guru-team/extension.json"
python3 - \
  "$TARGET/.trellis/guru-team/extension.json" \
  "$TARGET" \
  "$REPO_ROOT/trellis/presets/guru-team/ownership/upstream-ownership.json" <<'PY'
import json
import pathlib
import sys

manifest_path = pathlib.Path(sys.argv[1])
root = pathlib.Path(sys.argv[2])
ownership = json.loads(pathlib.Path(sys.argv[3]).read_text(encoding="utf-8"))
payload = json.loads(manifest_path.read_text(encoding="utf-8"))
extension = payload["extension"]
install = payload["install"]
skills = payload["skill_packages"]
api = extension["public_api"]
assets = install["managed_assets"]
assert payload["schema_version"] == "2.0"
assert set(payload) == {
    "schema_version", "extension", "installed_at", "source", "install",
    "skill_packages", "overlays", "notes",
}
assert ownership["schema_version"] == "3.0"
assert ownership["inventory_id"] == "guru-team-upstream-ownership"
assert ownership["overlay_root"] == "trellis/presets/guru-team/overlays"
assert len(ownership["guru_owned_rules"]) == 11
assert len(ownership["managed_path_claims"]) == 9
assert extension["extension_id"] == "guru-team"
assert extension["version"] == "0.6.5-guru.25"
assert extension["target_trellis_cli"] == "0.6.5"
assert assets == sorted(set(assets))
assert len(assets) == 62
assert all((root / path).is_file() for path in assets)
skills_root = root / ".trellis/guru-team/skills"
assert {
    path.name for path in (skills_root / "schemas").iterdir() if path.is_file()
} == {
    "production-contract-manifest.schema.json",
    "skill-eval-adapter-request.schema.json",
    "skill-eval-adapter-response.schema.json",
    "skill-eval-human-feedback.schema.json",
    "skill-eval-native-trace.schema.json",
    "skill-eval-run.schema.json",
    "skill-eval-semantic-grading.schema.json",
    "skill-evals.schema.json",
    "skill-interface-1.3.schema.json",
    "skill-registry.schema.json",
}
for artifact in (
    "review-gate.json", "pr-readiness.json",
    "finalization-transaction.json", "task-pr-merge-gate.json",
    "marketplace-verification.json", "finish-summary.json", "issue-review.json",
):
    assert artifact in api["artifact_contracts"]
assert "closeout-plan.json" not in api["artifact_contracts"]
for artifact in ("agent-assignment.json", "review.md", "task-commit-plans/*.json"):
    assert artifact not in api["artifact_contracts"]
for command in (
    "resolve-human-artifacts", "record-agent-recovery",
    "check-agent-recovery", "check-commit-messages",
    "create-task-commit", "discover-skill-contract", "discover-skill-evals", "run-skill-evals", "run-skill-command", "sync-base", "check-base-sync",
    "preview-change-context-history", "record-context-discovery", "check-context-discovery",
    "record-requirements-clarification", "check-requirements-clarification",
    "record-contract-wording-review", "check-contract-wording-review",
    "record-change-request-review", "check-change-request-review",
    "record-task-workspace-plan", "create-task-workspace", "check-task-workspace-result",
    "record-planning-approval", "check-planning-approval",
    "record-phase2-check", "check-phase2-check",
    "preview-finalization", "record-finalization-gate",
    "check-finalization-gate", "execute-finalization-transition",
    "preview-task-pr-merge", "record-task-pr-merge",
    "check-task-pr-merge", "execute-task-pr-merge", "invoke-task-pr-merge",
    "record-task-publication-review", "check-task-publication-review",
    "execute-extension-verification", "record-extension-verification",
    "check-extension-verification", "invoke-extension-verification",
    "format-merge-commit",
    "check-skill-packages",
):
    assert command in api["companion_scripts"]
assert api["skill_contracts"]["canonical_root"] == "trellis/skills/guru-team/"
assert api["skill_contracts"]["active_skill_ids"] == ["guru-approve-task-plan", "guru-check-task", "guru-clarify-requirements", "guru-create-task-commit", "guru-create-task-workspace", "guru-discover-change-context", "guru-finalize-task", "guru-merge-task-pr", "guru-review-branch", "guru-review-change-request", "guru-review-contract-wording", "guru-review-task-publication", "guru-select-workflow-mode", "guru-sync-base", "guru-verify-extension-installation"]
assert api["skill_contracts"]["planned_skill_ids"] == []
assert "guru-base-sync-result-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-change-context-owner-result-2.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-change-context-recovery-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-requirements-clarification-2.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-contract-wording-review-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-phase2-check-4.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-planning-approval-3.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-change-request-review-1.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-extension-installation-verification-3.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-issue-scope-ledger-2.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-review-gate-3.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-task-publication-readiness-4.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-task-workspace-plan-2.0" in api["skill_contracts"]["artifact_schema_ids"]
assert "guru-task-workspace-result-2.0" in api["skill_contracts"]["artifact_schema_ids"]
assert api["skill_contracts"]["interface_schema_id"] == "guru-team-skill-interface-1.3"
assert api["skill_contracts"]["registry_schema_id"] == "guru-team-skill-registry-1.2"
assert set(api["skill_contracts"]) == {
    "canonical_root", "installed_root", "registry_schema_id",
    "interface_schema_id", "public_input_schema_ids",
    "typed_output_schema_ids", "private_artifact_schema_ids",
    "artifact_schema_ids", "active_skill_ids", "planned_skill_ids",
    "registry_lifecycle", "contract_manifests",
    "workflow_markers",
}
assert len(api["skill_contracts"]["public_input_schema_ids"]) == 35
assert len(api["skill_contracts"]["typed_output_schema_ids"]) == 57
assert len(api["skill_contracts"]["private_artifact_schema_ids"]) == 17
assert api["skill_contracts"]["contract_manifests"] == [
    {
        "id": "production-current-v1",
        "schema_id": "guru-team-production-contract-manifest-1.0",
        "path": "contracts/production-current.json",
    },
]
assert api["skill_evals"]["schema_id"] == "guru-team-skill-evals-1.0"
assert api["skill_evals"]["adapter_ids"] == ["shared", "codex", "claude", "cursor"]
assert api["skill_runtime"] == {
    "api_version": "1.0",
    "dispatcher": "run-skill-command",
    "manifest_path": ".trellis/guru-team/extension.json",
}
assert skills["status"] == "ok"
assert skills["active_ids"] == ["guru-approve-task-plan", "guru-check-task", "guru-clarify-requirements", "guru-create-task-commit", "guru-create-task-workspace", "guru-discover-change-context", "guru-finalize-task", "guru-merge-task-pr", "guru-review-branch", "guru-review-change-request", "guru-review-contract-wording", "guru-review-task-publication", "guru-select-workflow-mode", "guru-sync-base", "guru-verify-extension-installation"]
assert skills["selected_platforms"] == ["claude", "codex", "cursor"]
assert skills["sidecars"] == []
skill_paths = [entry["path"] for entry in skills["files"]]
assert len(skill_paths) == len(set(skill_paths))
assert all((root / path).is_file() for path in skill_paths)
registry = json.loads((root / ".trellis/guru-team/skills/registry.json").read_text(encoding="utf-8"))
planned = [entry for entry in registry["skills"] if entry.get("state") == "planned"]
assert [entry["id"] for entry in planned] == []
assert (root / ".trellis/guru-team/skills/packages/guru-finalize-task").is_dir()
assert (root / ".trellis/guru-team/skills/packages/guru-merge-task-pr").is_dir()
assert (root / ".trellis/guru-team/skills/packages/guru-review-task-publication").is_dir()
assert (root / ".trellis/guru-team/skills/packages/guru-verify-extension-installation").is_dir()
PY
test -f "$TARGET/.trellis/guru-team/skills/schemas/skill-interface-1.3.schema.json"
test -f "$TARGET/.trellis/guru-team/skills/schemas/skill-evals.schema.json"
test -f "$TARGET/.trellis/guru-team/skills/schemas/skill-eval-adapter-request.schema.json"
test -f "$TARGET/.trellis/guru-team/skills/schemas/skill-eval-adapter-response.schema.json"
test -f "$TARGET/.trellis/guru-team/skills/schemas/skill-eval-run.schema.json"
test -f "$TARGET/.trellis/guru-team/skills/adapters/eval/shared.json"
test -f "$TARGET/.trellis/guru-team/skills/adapters/eval/codex.json"
test -f "$TARGET/.trellis/guru-team/skills/adapters/eval/claude.json"
test -f "$TARGET/.trellis/guru-team/skills/adapters/eval/cursor.json"
test -f "$TARGET/.trellis/guru-team/skills/adapters/eval/native_adapter.py"
test -x "$TARGET/.trellis/guru-team/skills/adapters/eval/shared.sh"
test -x "$TARGET/.trellis/guru-team/skills/adapters/eval/codex.sh"
test -x "$TARGET/.trellis/guru-team/skills/adapters/eval/claude.sh"
test -x "$TARGET/.trellis/guru-team/skills/adapters/eval/cursor.sh"
SOURCE_SKILL_VALIDATION_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$REPO_ROOT" --json --mode source)"
INSTALLED_SKILL_VALIDATION_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$TARGET" --json --mode installed)"
python3 -c 'import json, sys; source = json.loads(sys.argv[1]); installed = json.load(sys.stdin); assert source["status"] == installed["status"] == "passed"; expected={"invoke_markers":15,"exit_markers":57,"target_markers":33,"planned_ids":[]}; assert all(source["facts"][key] == installed["facts"][key] == value for key,value in expected.items())' "$SOURCE_SKILL_VALIDATION_JSON" <<<"$INSTALLED_SKILL_VALIDATION_JSON"
MINIMAL_CONTRACT_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/discover-skill-contract.sh" --root "$TARGET" --mode installed --skill guru-sync-base --json)"
python3 -c 'import json, sys; payload=json.load(sys.stdin); assert set(payload) == {"status","skill_id","interface_schema_id","input","invocation","outputs","consumer_inputs","projections","private_artifacts"}; assert payload["interface_schema_id"] == "guru-team-skill-interface-1.3"' <<<"$MINIMAL_CONTRACT_JSON"
MINIMAL_EVAL_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/discover-skill-evals.sh" --root "$TARGET" --mode installed --skill guru-sync-base --json)"
python3 -c 'import json, sys; payload=json.load(sys.stdin); assert payload["corpus_schema_id"] == "guru-team-skill-evals-1.0"; assert payload["case_ids"] == ["synced-route", "skipped-route", "blocked-route"]' <<<"$MINIMAL_EVAL_JSON"
while IFS='|' read -r skill_id expected_case_ids; do
  PRODUCTION_CONTRACT_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/discover-skill-contract.sh" --root "$TARGET" --mode installed --skill "$skill_id" --json)"
  python3 -c 'import json, sys; payload=json.load(sys.stdin); assert set(payload) == {"status","skill_id","interface_schema_id","input","invocation","outputs","consumer_inputs","projections","private_artifacts"}; assert payload["interface_schema_id"] == "guru-team-skill-interface-1.3"' <<<"$PRODUCTION_CONTRACT_JSON"
  PRODUCTION_EVAL_JSON="$("$TARGET/.trellis/guru-team/scripts/bash/discover-skill-evals.sh" --root "$TARGET" --mode installed --skill "$skill_id" --json)"
  python3 -c 'import json, sys; payload=json.load(sys.stdin); assert payload["corpus_schema_id"] == "guru-team-skill-evals-1.0"; assert payload["case_ids"] == json.loads(sys.argv[1])' "$expected_case_ids" <<<"$PRODUCTION_EVAL_JSON"
done <<'EOF'
guru-approve-task-plan|["approved-initial","revision-required","clarify-scope","blocked-initial"]
guru-check-task|["passed-initial","implementation-required","planning-stale","blocked-initial"]
guru-create-task-commit|["committed-initial","revision-required","committed-finding-fix","blocked-recovery"]
guru-finalize-task|["publication-verification-required","publication-review-stale","same-plan-resume","cross-month-reprepare","ready-for-merge-recovery","publication-ready-ready-for-merge","same-plan-ready-for-merge","blocked-private-state","verified-reentry-ready-for-merge","not-required-reentry-ready-for-merge"]
guru-merge-task-pr|["workflow-expected-head-merged","standalone-draft-blocked","workflow-head-drift-blocked","workflow-branch-drift-blocked","workflow-close-keyword-mismatch-blocked","workflow-added-close-keyword-blocked","workflow-post-merge-closure-mismatch"]
guru-review-branch|["workflow-passed","standalone-passed","implementation-required","scope-confirmation-required","blocked-stale","finding-fix-passed","fresh-final-passed"]
guru-review-task-publication|["workflow-initial-ready","standalone-initial-ready","return-to-task-work","blocked-external","stale-reentry-ready","metadata-fix-fresh-ready","metadata-fix-durable-drift-return"]
guru-verify-extension-installation|["workflow-required-verified","workflow-applicability-conflict-blocked","standalone-not-required","task-install-finding-return","standalone-remote-unavailable","workflow-transient-retry-verified","workflow-stale-plan-reentry-verified"]
EOF
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-approve-task-plan/SKILL.md"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-approve-task-plan/schemas/planning-approval.schema.json"
test -x "$TARGET/.agents/skills/guru-approve-task-plan/scripts/record-planning-approval.sh"
test -x "$TARGET/.agents/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -x "$TARGET/.claude/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -x "$TARGET/.codex/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -x "$TARGET/.cursor/skills/guru-approve-task-plan/scripts/check-planning-approval.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-create-task-commit/SKILL.md"
test -x "$TARGET/.agents/skills/guru-create-task-commit/scripts/prepare-task-commit.sh"
test -x "$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh"
test -x "$TARGET/.agents/skills/guru-create-task-commit/scripts/create-task-commit.sh"
"$TARGET/.agents/skills/guru-create-task-commit/scripts/prepare-task-commit.sh" --help >/dev/null
"$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh" --help >/dev/null
test -x "$TARGET/.claude/skills/guru-create-task-commit/scripts/prepare-task-commit.sh"
test -x "$TARGET/.claude/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.codex/skills/guru-create-task-commit/scripts/prepare-task-commit.sh"
test -x "$TARGET/.codex/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -x "$TARGET/.cursor/skills/guru-create-task-commit/scripts/prepare-task-commit.sh"
test -x "$TARGET/.cursor/skills/guru-create-task-commit/scripts/create-task-commit.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-review-branch/SKILL.md"
test -x "$TARGET/.agents/skills/guru-review-branch/scripts/invoke.sh"
test -x "$TARGET/.agents/skills/guru-review-branch/scripts/review-branch.sh"
test -x "$TARGET/.agents/skills/guru-review-branch/scripts/check-review-gate.sh"
test -x "$TARGET/.claude/skills/guru-review-branch/scripts/invoke.sh"
test -x "$TARGET/.codex/skills/guru-review-branch/scripts/invoke.sh"
test -x "$TARGET/.cursor/skills/guru-review-branch/scripts/invoke.sh"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-review-task-publication/SKILL.md"
test -x "$TARGET/.agents/skills/guru-review-task-publication/scripts/invoke.sh"
test -x "$TARGET/.agents/skills/guru-review-task-publication/scripts/record-task-publication-review.sh"
test -x "$TARGET/.agents/skills/guru-review-task-publication/scripts/check-task-publication-review.sh"
test -x "$TARGET/.claude/skills/guru-review-task-publication/scripts/invoke.sh"
test -x "$TARGET/.codex/skills/guru-review-task-publication/scripts/invoke.sh"
test -x "$TARGET/.cursor/skills/guru-review-task-publication/scripts/invoke.sh"
verify_task_publication_validator_wrappers "fresh-install"
test -f "$TARGET/.trellis/guru-team/skills/packages/guru-verify-extension-installation/SKILL.md"
for root in .agents .claude .codex .cursor; do
  test -x "$TARGET/$root/skills/guru-verify-extension-installation/scripts/invoke.sh"
  test -x "$TARGET/$root/skills/guru-verify-extension-installation/scripts/execute-extension-verification.sh"
  test -x "$TARGET/$root/skills/guru-verify-extension-installation/scripts/record-extension-verification.sh"
  test -x "$TARGET/$root/skills/guru-verify-extension-installation/scripts/check-extension-verification.sh"
done
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
test -f "$TARGET/.codex/prompts/guru-finish-work.md"
test -f "$TARGET/.claude/commands/guru/finish-work.md"
test -f "$TARGET/.cursor/commands/guru-finish-work.md"
test -f "$TARGET/.trellis/guru-team/skills/tests/test_finish_family_integration.py"
verify_requirements_clarification_exits "initial"
verify_contract_wording_standalone_profiles "initial"
verify_change_request_review_package "initial"
test ! -e "$TARGET/.agents/skills/guru-example-action"
test ! -e "$TARGET/.codex/skills/guru-example-action"
test ! -e "$TARGET/.cursor/skills/guru-example-action"
test ! -e "$TARGET/.claude/skills/guru-example-action"
(cd "$REPO_ROOT" && python3 -m unittest \
  trellis.skills.guru-team.tests.test_skill_packages.DistributionTests.test_unchanged_reapply \
  trellis.skills.guru-team.tests.test_skill_packages.SourceValidationTests.test_representative_active_package_and_routes_pass \
  trellis.skills.guru-team.tests.test_skill_packages.SourceValidationTests.test_representative_wrappers_emit_distinct_exits_and_stable_errors \
  trellis.skills.guru-team.tests.test_skill_packages.EvalRunnerTests.test_four_adapters_execute_same_corpus_and_expected_non_success_exits)
verify_finish_family_integration "initial"
test -f "$TARGET/.trellis/guru-team/schemas/closeout-plan.schema.json"
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
grep -q "def ensure_closeout_draft_pr" "$TARGET/.trellis/guru-team/scripts/python/guru_team_trellis.py"
for relative in \
  ".codex/prompts/guru-finish-work.md" \
  ".claude/commands/guru/finish-work.md" \
  ".cursor/commands/guru-finish-work.md"; do
  test -f "$TARGET/$relative"
  cmp -s "$REPO_ROOT/trellis/presets/guru-team/overlays/$relative" "$TARGET/$relative"
  grep -q '<!-- guru-team-overlay: v1 -->' "$TARGET/$relative"
  grep -q 'guru-review-task-publication' "$TARGET/$relative"
  grep -q 'guru-verify-extension-installation' "$TARGET/$relative"
  grep -q 'guru-finalize-task' "$TARGET/$relative"
done
test -z "$(find "$TARGET" -type f \( -name '*.new' -o -name '*.bak' \) -print -quit)"
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
  echo "finish-work direct dry-run unexpectedly bypassed guru-finalize-task" >&2
  exit 2
fi
printf '%s\n' "$FINISH_ERROR_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "error"; assert payload["blocked_step"] == "finish-work"; assert payload["required_entrypoint"] == "guru-finish-work"; assert "intent_flag" not in payload; assert "guru-finalize-task" in payload["error"]' <<<"$FINISH_ERROR_JSON"

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

DISCOVERY_INPUT="$WORK_DIR/change-context-owner-result.json"
DISCOVERY_ZERO_INPUT="$WORK_DIR/change-context-zero-owner-result.json"
DISCOVERY_RECOVERY_INPUT="$WORK_DIR/change-context-recovery-owner-result.json"
python3 - \
  "$TARGET" \
  "$SYNC_RESULT_JSON" \
  "$DISCOVERY_CANDIDATE_JSON" \
  "$DISCOVERY_ZERO_JSON" \
  "$DISCOVERY_INPUT" \
  "$DISCOVERY_ZERO_INPUT" \
  "$DISCOVERY_RECOVERY_INPUT" <<'PY'
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
zero_preview = json.loads(sys.argv[4])
runtime = root / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
spec = importlib.util.spec_from_file_location(
    "installed_ephemeral_context_runtime", runtime
)
if spec is None or spec.loader is None:
    raise SystemExit(f"could not load installed context runtime: {runtime}")
gtt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gtt
spec.loader.exec_module(gtt)

head = subprocess.run(
    ["git", "rev-parse", "HEAD"],
    cwd=root,
    check=True,
    text=True,
    capture_output=True,
).stdout.strip()

def blob(relative: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()

query = preview["canonical_query"]
candidate = preview["candidates"][0]
candidate_task = candidate["finish_summary_path"].rsplit("/", 1)[0]
body_sha256 = hashlib.sha256(
    b"throwaway context discovery request"
).hexdigest()
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
payload = {
    "schema_version": "2.0",
    "skill_id": "guru-discover-change-context",
    "generated_at": "2026-01-01T00:00:00Z",
    "mode": "standalone",
    "typed_exit": "context_ready",
    "repository": {
        "repo": "castbox/guru-trellis-throwaway",
        "selected_base": "main",
        "decision_branch": "main",
    },
    "base_evidence": {
        "schema_id": "guru-base-sync-result-1.0",
        "sync_result": sync_result,
        "remote": sync_result["resolution"]["remote"],
        "base_head": head,
        "decision_head": sync_result["decision_checkout"]["head_after"],
        "local_head": sync_result["git"]["local_head_after"],
        "remote_head": sync_result["git"]["remote_head_after"],
        "post_sync_resolution_sha256": sync_result[
            "post_sync_resolution_sha256"
        ],
        "clean": sync_result["decision_checkout"]["clean_after"],
    },
    "change_input": {
        key: query[key]
        for key in gtt.CONTEXT_QUERY_KINDS
    },
    "live_change": live_change,
    "duplicate_search": {
        "query": "repo:castbox/guru-trellis-throwaway is:issue is:open context discovery",
        "checked_at": "2026-01-01T00:00:00Z",
        "scope": "open_issues",
        "candidates": [{
            **duplicate_facts,
            "facts_sha256": gtt.context_digest(duplicate_facts),
            "reason": "The open issue may describe the same change.",
            "observation": "Clarification must decide reuse or a new target.",
        }],
    },
    "current_state": {
        "sequence_trace": list(gtt.CONTEXT_SEQUENCE_TRACE),
        "docs": [{
            "path": "docs/context-discovery-smoke.md",
            "blob_or_content_sha256": blob("docs/context-discovery-smoke.md"),
            "purpose": "Review the durable current-state contract.",
            "observation": "Current evidence precedes archived history.",
            "query_clues": ["current state"],
        }],
        "code_contracts": [{
            "path": "src/context_discovery_smoke.py",
            "blob_or_content_sha256": blob("src/context_discovery_smoke.py"),
            "purpose": "Review deterministic runtime ownership.",
            "observation": "Runtime validates facts without semantic judgment.",
            "query_clues": ["runtime"],
        }],
        "tests": [{
            "path": "tests/test_context_discovery_smoke.py",
            "blob_or_content_sha256": blob("tests/test_context_discovery_smoke.py"),
            "purpose": "Review installed verification coverage.",
            "observation": "Throwaway covers candidate and zero-candidate paths.",
            "query_clues": ["throwaway"],
        }],
        "observations": [
            "Current repository evidence was reviewed before history preview."
        ],
    },
    "canonical_query": query,
    "history_preview": preview,
    "history_review": {
        "selected_candidates": [{
            "candidate_id": candidate["candidate_id"],
            "reason": "Exact issue, path, and command clues match.",
        }],
        "excluded_candidates": [],
        "deep_reads": [{
            "candidate_id": candidate["candidate_id"],
            "source": "task_artifact",
            "locator": f"{candidate_task}/design.md",
            "purpose": "Verify archived runtime ownership.",
            "conclusion": "The selected artifact confirms narrow deep-read behavior.",
        }],
    },
    "mem_review": {
        "status": "not_needed",
        "reason": "Current and selected task evidence is sufficient.",
        "load_bearing_question": None,
        "exhausted_sources": {
            "task_artifacts": False,
            "current_docs_code_tests": False,
            "github": False,
            "git_history": False,
        },
        "summary": None,
    },
    "ai_review_gate": {
        "status": "passed",
        "reviewer": "throwaway-context-review",
        "reviewed_scope": [
            "live draft",
            "current Docs/code/tests",
            "selected archived task artifact",
        ],
        "excluded_scope": ["duplicate reuse decision"],
        "relevance": "The evidence directly covers installed context discovery.",
        "sufficiency": "Current and archived evidence support the conclusions.",
        "conflicts": [],
        "reusable": ["installed dispatcher"],
        "not_reusable": ["workspace journal"],
        "load_bearing_conclusions": [{
            "conclusion": "Current state is reviewed before archived history.",
            "evidence_refs": [
                "docs/context-discovery-smoke.md",
                f"{candidate_task}/design.md",
            ],
        }],
        "findings": [],
        "reason": "Every required semantic dimension passed.",
    },
    "result_identity": {},
    "error": None,
}
payload["result_identity"] = gtt.context_result_identity(payload)
if gtt.context_structural_errors(root, payload):
    raise SystemExit("installed candidate owner result is structurally invalid")
Path(sys.argv[5]).write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

zero = copy.deepcopy(payload)
zero_query = zero_preview["canonical_query"]
zero["change_input"] = {
    key: zero_query[key]
    for key in gtt.CONTEXT_QUERY_KINDS
}
zero["live_change"]["issue_binding"] = None
zero["canonical_query"] = zero_query
zero["history_preview"] = zero_preview
zero["history_review"] = {
    "selected_candidates": [],
    "excluded_candidates": [],
    "deep_reads": [],
}
zero["mem_review"] = {
    "status": "not_needed",
    "reason": "The zero-candidate preview needs no other history source.",
    "load_bearing_question": None,
    "exhausted_sources": {
        "task_artifacts": False,
        "current_docs_code_tests": False,
        "github": False,
        "git_history": False,
    },
    "summary": None,
}
zero["ai_review_gate"]["reviewed_scope"] = [
    "live draft",
    "current Docs/code/tests",
    "zero-candidate history preview",
]
zero["ai_review_gate"]["load_bearing_conclusions"] = [{
    "conclusion": "Zero candidates require no deep-read or memory source.",
    "evidence_refs": ["docs/context-discovery-smoke.md"],
}]
zero["result_identity"] = gtt.context_result_identity(zero)
if gtt.context_structural_errors(root, zero):
    raise SystemExit("installed zero-candidate owner result is structurally invalid")
Path(sys.argv[6]).write_text(
    json.dumps(zero, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

recovery = copy.deepcopy(payload)
recovery["mode"] = "workflow"
recovery["result_identity"] = gtt.context_result_identity(recovery)
if gtt.context_structural_errors(root, recovery):
    raise SystemExit("installed recovery owner result is structurally invalid")
Path(sys.argv[7]).write_text(
    json.dumps(recovery, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

DISCOVERY_FAKE_BIN="$WORK_DIR/context-discovery-fake-bin"
mkdir -p "$DISCOVERY_FAKE_BIN"
DISCOVERY_REAL_GIT="$(command -v git)"
cat >"$DISCOVERY_FAKE_BIN/gh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "auth" && "${2:-}" == "status" ]]; then
  exit 0
fi
if [[ "${1:-}" == "issue" && "${2:-}" == "view" && "${3:-}" == "111" ]]; then
  printf '%s\n' '{"number":111,"title":"Throwaway context discovery request","url":"https://github.com/castbox/guru-trellis-throwaway/issues/111","state":"OPEN","updatedAt":"2026-01-01T00:00:00Z","body":"throwaway context discovery request","comments":[],"assignees":[],"labels":[]}'
  exit 0
fi
if [[ "${1:-}" == "issue" && "${2:-}" == "view" && "${3:-}" == "99" ]]; then
  printf '%s\n' '{"number":99,"title":"Throwaway duplicate candidate","url":"https://github.com/castbox/guru-trellis-throwaway/issues/99","state":"OPEN","updatedAt":"2026-01-01T00:00:00Z","body":"throwaway duplicate candidate","comments":[],"assignees":[],"labels":[]}'
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
DISCOVERY_RESULT_SHA256="$(
  python3 -c 'import json, sys; payload=json.load(sys.stdin); assert payload["schema_version"] == "2.0"; assert payload["typed_exit"] == "context_ready"; print(payload["result_identity"]["result_sha256"])' \
    <<<"$DISCOVERY_PRETASK_JSON"
)"
DISCOVERY_ZERO_RESULT_SHA256="$(
  python3 -c 'import json, sys; payload=json.load(sys.stdin); assert payload["history_preview"]["candidates"] == []; assert payload["history_review"] == {"selected_candidates": [], "excluded_candidates": [], "deep_reads": []}; assert payload["mem_review"]["status"] == "not_needed"; print(payload["result_identity"]["result_sha256"])' \
    <<<"$DISCOVERY_ZERO_PRETASK_JSON"
)"
DISCOVERY_CHECK_JSON="$(
  printf '%s' "$DISCOVERY_PRETASK_JSON" | \
    DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" \
    "$DISCOVERY_CHECK" \
      --root "$TARGET" \
      --json \
      --input - \
      --expected-result-sha256 "$DISCOVERY_RESULT_SHA256"
)"
DISCOVERY_ZERO_CHECK_JSON="$(
  printf '%s' "$DISCOVERY_ZERO_PRETASK_JSON" | \
    DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" \
    "$DISCOVERY_CHECK" \
      --root "$TARGET" \
      --json \
      --input - \
      --expected-result-sha256 "$DISCOVERY_ZERO_RESULT_SHA256"
)"
python3 -c 'import json, sys; checked=json.loads(sys.argv[1]); zero=json.load(sys.stdin); assert checked["status"] == zero["status"] == "passed"; assert checked["typed_exit"] == zero["typed_exit"] == "context_ready"; assert checked["result_sha256"] == sys.argv[2]; assert zero["result_sha256"] == sys.argv[3]' \
  "$DISCOVERY_CHECK_JSON" \
  "$DISCOVERY_RESULT_SHA256" \
  "$DISCOVERY_ZERO_RESULT_SHA256" \
  <<<"$DISCOVERY_ZERO_CHECK_JSON"

DISCOVERY_PUBLIC_INPUT_REL=".trellis/.runtime/guru-team/discovery-public-input.json"
DISCOVERY_PUBLIC_INPUT="$TARGET/$DISCOVERY_PUBLIC_INPUT_REL"
mkdir -p "$(dirname "$DISCOVERY_PUBLIC_INPUT")"
python3 - "$DISCOVERY_PUBLIC_INPUT" <<'PY'
import json
import sys
from pathlib import Path

Path(sys.argv[1]).write_text(json.dumps({
    "profile": "pre_task",
    "source_exit": "start",
    "mode": "standalone",
    "repo_locator": "castbox/guru-trellis-throwaway",
    "base_branch": "main",
    "continuation_id": "throwaway-ephemeral-context",
}, indent=2) + "\n", encoding="utf-8")
PY
DISCOVERY_PUBLIC_JSON="$(
  printf '%s' "$DISCOVERY_PRETASK_JSON" | \
    DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" \
    "$TARGET/.agents/skills/guru-discover-change-context/scripts/invoke.sh" \
      --input "$DISCOVERY_PUBLIC_INPUT_REL" \
      --owner-result -
)"
python3 -c 'import json, sys; payload=json.load(sys.stdin); assert set(payload) == {"exit_id", "handoff_profile", "handoff_mode", "handoff_target_locator", "handoff_continuation_id"}; assert payload["exit_id"] == "context_ready"; assert payload["handoff_profile"] == "initial_change_request"; assert payload["handoff_mode"] == "standalone"; assert payload["handoff_continuation_id"] == "throwaway-ephemeral-context"' \
  <<<"$DISCOVERY_PUBLIC_JSON"
rm "$DISCOVERY_PUBLIC_INPUT"
DISCOVERY_STATUS_NORMAL_FINAL="$(git -C "$TARGET" status --porcelain=v1)"
if [[ "$DISCOVERY_STATUS_NORMAL_FINAL" != "$DISCOVERY_STATUS_BEFORE" ]]; then
  echo "Ephemeral context record/check/invoke modified the throwaway repository" >&2
  exit 2
fi

DISCOVERY_RECOVERY_TASK_REL=".trellis/tasks/08-07-context-recovery"
DISCOVERY_RECOVERY_TASK="$TARGET/$DISCOVERY_RECOVERY_TASK_REL"
DISCOVERY_RECOVERY_BRANCH="codex/throwaway-context-recovery"
git -C "$TARGET" checkout -q -b "$DISCOVERY_RECOVERY_BRANCH"
mkdir -p "$DISCOVERY_RECOVERY_TASK"
printf '{"id":"08-07-context-recovery","status":"in_progress","branch":"%s"}\n' \
  "$DISCOVERY_RECOVERY_BRANCH" >"$DISCOVERY_RECOVERY_TASK/task.json"
git -C "$TARGET" add "$DISCOVERY_RECOVERY_TASK_REL/task.json"
git -C "$TARGET" commit -q -m "chore: add throwaway active recovery task"
DISCOVERY_RECOVERY_CONTINUATION="throwaway-active-recovery"
DISCOVERY_ACTIVE_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_RECORD" \
    --root "$TARGET" \
    --json \
    --mode workflow \
    --input "$DISCOVERY_RECOVERY_INPUT" \
    --active-task "$DISCOVERY_RECOVERY_TASK_REL"
)"
DISCOVERY_ACTIVE_SHA256="$(
  python3 -c 'import json, sys; print(json.load(sys.stdin)["result_identity"]["result_sha256"])' \
    <<<"$DISCOVERY_ACTIVE_JSON"
)"
printf '%s' "$DISCOVERY_ACTIVE_JSON" | \
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" \
  "$DISCOVERY_CHECK" \
    --root "$TARGET" \
    --json \
    --input - \
    --expected-result-sha256 "$DISCOVERY_ACTIVE_SHA256" \
    --active-task "$DISCOVERY_RECOVERY_TASK_REL" >/dev/null
DISCOVERY_RECOVERY_PUBLIC_INPUT_REL=".trellis/.runtime/guru-team/discovery-recovery-public-input.json"
DISCOVERY_RECOVERY_PUBLIC_INPUT="$TARGET/$DISCOVERY_RECOVERY_PUBLIC_INPUT_REL"
python3 - "$DISCOVERY_RECOVERY_PUBLIC_INPUT" "$DISCOVERY_RECOVERY_CONTINUATION" <<'PY'
import json
import sys
from pathlib import Path

Path(sys.argv[1]).write_text(json.dumps({
    "profile": "pre_task",
    "source_exit": "needs_context",
    "mode": "workflow",
    "repo_locator": "castbox/guru-trellis-throwaway",
    "base_branch": "main",
    "continuation_id": sys.argv[2],
}, indent=2) + "\n", encoding="utf-8")
PY
DISCOVERY_ACTIVE_PUBLIC_JSON="$(
  printf '%s' "$DISCOVERY_ACTIVE_JSON" | \
    DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" \
    "$TARGET/.agents/skills/guru-discover-change-context/scripts/invoke.sh" \
      --input "$DISCOVERY_RECOVERY_PUBLIC_INPUT_REL" \
      --owner-result - \
      --active-task "$DISCOVERY_RECOVERY_TASK_REL"
)"
python3 -c 'import json, sys; payload=json.load(sys.stdin); assert payload["exit_id"] == "context_ready"; assert payload["handoff_continuation_id"] == sys.argv[1]' \
  "$DISCOVERY_RECOVERY_CONTINUATION" \
  <<<"$DISCOVERY_ACTIVE_PUBLIC_JSON"
DISCOVERY_OWNER_ROOT="$TARGET/.trellis/.runtime/guru-team/owner-checkpoints"
if [[ -d "$DISCOVERY_OWNER_ROOT" ]] && find "$DISCOVERY_OWNER_ROOT" -mindepth 1 -print -quit | grep -q .; then
  echo "Normal active-task context invocation created an owner checkpoint" >&2
  exit 2
fi

DISCOVERY_ACTIVE_EDIT="$TARGET/active-task-context-edit.txt"
printf '%s\n' 'ordinary active task worktree edit' >"$DISCOVERY_ACTIVE_EDIT"
DISCOVERY_RECOVERY_JSON="$(
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" "$DISCOVERY_RECORD" \
    --root "$TARGET" \
    --json \
    --mode workflow \
    --input "$DISCOVERY_RECOVERY_INPUT" \
    --active-task "$DISCOVERY_RECOVERY_TASK_REL" \
    --recovery-continuation-id "$DISCOVERY_RECOVERY_CONTINUATION"
)"
DISCOVERY_RECOVERY_SHA256="$(
  python3 -c 'import json, sys; print(json.load(sys.stdin)["result_identity"]["result_sha256"])' \
    <<<"$DISCOVERY_RECOVERY_JSON"
)"
printf '%s' "$DISCOVERY_RECOVERY_JSON" | \
  DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" \
  "$DISCOVERY_CHECK" \
    --root "$TARGET" \
    --json \
    --input - \
    --expected-result-sha256 "$DISCOVERY_RECOVERY_SHA256" \
    --active-task "$DISCOVERY_RECOVERY_TASK_REL" \
    --recovery-continuation-id "$DISCOVERY_RECOVERY_CONTINUATION" >/dev/null
DISCOVERY_RECOVERY_PUBLIC_JSON="$(
  printf '%s' "$DISCOVERY_RECOVERY_JSON" | \
    DISCOVERY_REAL_GIT="$DISCOVERY_REAL_GIT" PATH="$DISCOVERY_FAKE_BIN:$PATH" \
    "$TARGET/.agents/skills/guru-discover-change-context/scripts/invoke.sh" \
      --input "$DISCOVERY_RECOVERY_PUBLIC_INPUT_REL" \
      --owner-result - \
      --active-task "$DISCOVERY_RECOVERY_TASK_REL" \
      --recovery-continuation-id "$DISCOVERY_RECOVERY_CONTINUATION"
)"
python3 -c 'import json, sys; payload=json.load(sys.stdin); assert payload["exit_id"] == "context_ready"; assert payload["handoff_continuation_id"] == sys.argv[1]' \
  "$DISCOVERY_RECOVERY_CONTINUATION" \
  <<<"$DISCOVERY_RECOVERY_PUBLIC_JSON"
rm "$DISCOVERY_RECOVERY_PUBLIC_INPUT"
rm "$DISCOVERY_ACTIVE_EDIT"
git -C "$TARGET" checkout -q main
git -C "$TARGET" branch -D "$DISCOVERY_RECOVERY_BRANCH" >/dev/null
if [[ -d "$DISCOVERY_OWNER_ROOT" ]] && find "$DISCOVERY_OWNER_ROOT" -mindepth 1 -print -quit | grep -q .; then
  echo "Ephemeral context invocation left an owner checkpoint" >&2
  exit 2
fi
DISCOVERY_STATUS_FINAL="$(git -C "$TARGET" status --porcelain=v1)"
if [[ "$DISCOVERY_STATUS_FINAL" != "$DISCOVERY_STATUS_BEFORE" ]]; then
  echo "Active-task context recovery left throwaway repository residue" >&2
  exit 2
fi

PHASE0_FAKE_BIN="$WORK_DIR/phase0-fake-bin"
mkdir -p "$PHASE0_FAKE_BIN"
cat >"$PHASE0_FAKE_BIN/gh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "auth" && "${2:-}" == "status" ]]; then
  exit 0
fi
if [[ "${1:-}" == "issue" && "${2:-}" == "view" ]]; then
  printf '%s\n' '{"number":110,"title":"Verify Phase 0 stdout base facts","url":"https://github.com/castbox/guru-trellis-throwaway/issues/110","body":"Exercise installed workflow base synchronization across planner and mutation guards.","comments":[],"state":"OPEN","updatedAt":"2026-01-01T00:00:00Z","assignees":[],"labels":[]}'
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
python3 -c 'import json, sys; payload = json.load(sys.stdin); freshness = payload["base_freshness"]; assert payload["source_issue"]["number"] == 110; assert "preflight" not in payload; assert "workspace_ready" not in payload; assert freshness["reviewed_resolution_sha256"] == sys.argv[1]; assert freshness["three_way_equal"] is True; assert freshness["post_sync_resolution_sha256"]' "$PHASE0_POST_DIGEST" <<<"$PHASE0_PLANNER_JSON"

cp "$SYNC_CONFIG_BACKUP" "$TARGET/.trellis/guru-team/config.yml"
git -C "$TARGET" add .trellis/guru-team/config.yml
git -C "$TARGET" commit -q -m "chore: restore throwaway preset config"
git -C "$TARGET" push -q origin main
BASELINE_HEAD="$(git -C "$TARGET" rev-parse HEAD)"
TASK_BRANCH="feat/122-installed-task-commit"
TASK_REL=".trellis/tasks/07-13-122-installed-task-commit"
INSTALL_TARGET="$TARGET"
TASK_COMMIT_TARGET="$WORK_DIR/installed-task-commit-worktree"
git -C "$INSTALL_TARGET" worktree add -q -b "$TASK_BRANCH" "$TASK_COMMIT_TARGET" main
TARGET="$TASK_COMMIT_TARGET"

TASK_COMMIT_FAKE_BIN="$WORK_DIR/task-commit-fake-bin"
TASK_COMMIT_REAL_GIT="$(command -v git)"
TASK_COMMIT_ORIGINAL_PATH="$PATH"
mkdir -p "$TASK_COMMIT_FAKE_BIN"
cat >"$TASK_COMMIT_FAKE_BIN/git" <<'SH'
#!/usr/bin/env bash
set -euo pipefail

if [[ "$*" == "config --null --show-origin --get-all remote.origin.url" ]]; then
  printf 'command line:\0https://github.com/castbox/guru-trellis-throwaway.git\0'
  exit 0
fi
if [[ "$*" == "config --null --show-origin --get-all remote.origin.pushurl" ]]; then
  exit 1
fi
if [[ "$*" == 'remote get-url --all origin' || "$*" == 'remote get-url --push --all origin' || "$*" == 'remote get-url origin' ]]; then
  printf '%s\n' 'https://github.com/castbox/guru-trellis-throwaway.git'
  exit 0
fi
exec "$TASK_COMMIT_REAL_GIT" "$@"
SH
cat >"$TASK_COMMIT_FAKE_BIN/gh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "auth" && "${2:-}" == "status" ]]; then
  exit 0
fi
if [[ "${1:-}" == "pr" && "${2:-}" == "list" && "$*" == *"--repo castbox/guru-trellis-throwaway"* ]]; then
  printf '%s\n' '[]'
  exit 0
fi
printf 'unexpected task-commit fake gh invocation: %s\n' "$*" >&2
exit 2
SH
chmod +x "$TASK_COMMIT_FAKE_BIN/git" "$TASK_COMMIT_FAKE_BIN/gh"
export TASK_COMMIT_REAL_GIT
export PATH="$TASK_COMMIT_FAKE_BIN:$PATH"

python3 - "$TARGET" "$TASK_REL" "$TASK_BRANCH" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
task_rel = sys.argv[2]
branch = sys.argv[3]
task_dir = root / task_rel
task_dir.mkdir(parents=True)
(root / "src").mkdir(exist_ok=True)

task = {
    "id": "122-installed-task-commit",
    "name": "122-installed-task-commit",
    "title": "#122 验证安装后 task commit",
    "status": "in_progress",
    "branch": branch,
    "base_branch": "main",
}
issue = {
    "number": 122,
    "url": "https://github.com/castbox/guru-trellis-throwaway/issues/122",
    "title": "验证安装后 task commit",
    "reason": "当前 throwaway task 的完整交付范围。",
}
ledger = {
    "schema_version": "2.0",
    "primary_issue": issue,
    "close_issues": [issue],
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
    ("task.json", task),
    ("issue-scope-ledger.json", ledger),
):
    (task_dir / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
workspace_slug = task["id"]
runtime_root = root / ".trellis/.runtime/guru-team"
runtime_payloads = (
    (
        runtime_root / "workspaces" / f"{workspace_slug}.json",
        {
            "schema_version": "1.0",
            "workspace_slug": workspace_slug,
            "workspace_path": str(root.resolve()),
            "source_checkout": str(root.resolve()),
            "branch_name": branch,
            "updated_at": "2026-08-01T00:00:00Z",
        },
    ),
    (
        runtime_root / "tasks" / f"{task['id']}.json",
        {
            "schema_version": "1.0",
            "task_slug": task["id"],
            "workspace_slug": workspace_slug,
            "workspace_path": str(root.resolve()),
            "task_artifact_dir": task_rel,
            "updated_at": "2026-08-01T00:00:00Z",
        },
    ),
)
for path, payload in runtime_payloads:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(root / "src/task-commit-smoke.txt").write_text("initial task change\n", encoding="utf-8")
(root / "unrelated-preserved.log").write_text("preserve this exact state\n", encoding="utf-8")
PY

record_planning_contract_wording "$TASK_REL"
PLANNING_DTO="$(record_and_check_planning_approval "$TASK_REL" "initial")"
python3 -c 'import json,sys; assert json.load(sys.stdin) == {"exit_id":"approved","task_ref":sys.argv[1]}' "$TASK_REL" <<<"$PLANNING_DTO"

record_throwaway_phase2() {
  local summary="$1"
  local profile="$2"
  local input_path
  local public_input
  local record_json
  local check_json
  local owner_result
  local public_output
  input_path="$(mktemp "${TMPDIR:-/tmp}/guru-phase2-input.XXXXXX")"
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
payload = {
    key: payload[key]
    for key in (
        "mode", "reviewed_paths", "validation", "docs_ssot",
        "semantic_review", "typed_exit", "route", "reason", "consumer",
    )
}
payload["mode"] = "workflow"
payload["reviewed_paths"] = [
    f"{task_rel}/contract-wording-review.json",
    f"{task_rel}/design.md",
    f"{task_rel}/implement.md",
    f"{task_rel}/issue-scope-ledger.json",
    f"{task_rel}/prd.md",
    f"{task_rel}/task.json",
    "src/task-commit-smoke.txt",
    "unrelated-preserved.log",
]
payload["validation"]["commands"] = [{
    "id": "installed-guru-check-task-smoke",
    "outcome": "passed",
    "summary": summary,
}]
payload["validation"]["summary"] = summary
payload["docs_ssot"] = {
    "status": "passed",
    "strategy": "ssot_first",
    "durable_paths": [".trellis/workflow.md"],
    "summary": "已安装的 canonical workflow 是本次 smoke 的 durable SSOT 输入。",
}
payload["semantic_review"]["summary"] = summary
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
  python3 -c 'import json,sys; recorded=json.loads(sys.argv[1]); checked=json.load(sys.stdin); assert recorded["schema_version"] == "4.0"; assert recorded["skill_id"] == "guru-check-task"; assert recorded["typed_exit"] == checked["typed_exit"] == "passed"; assert checked["consumer"] == {"kind":"skill","id":"guru-create-task-commit"}' "$record_json" <<<"$check_json"
  owner_result="$(python3 -c 'import json,pathlib,sys; root=pathlib.Path(sys.argv[1]).resolve(); path=pathlib.Path(json.loads(sys.argv[2])["artifact_path"]).resolve(); print(path.relative_to(root).as_posix())' "$TARGET" "$record_json")"
  mkdir -p "$TARGET/.trellis/.runtime/guru-team/throwaway-inputs"
  public_input="$(mktemp "$TARGET/.trellis/.runtime/guru-team/throwaway-inputs/phase2.XXXXXX")"
  python3 - "$TASK_REL" "$profile" "$public_input" <<'PY'
import json
import sys
from pathlib import Path

task_ref = sys.argv[1]
profile = sys.argv[2]
payload = {
    "profile": profile,
    "mode": "workflow",
    "task_ref": task_ref,
}
if profile == "initial_check":
    payload["source_exit"] = "implementation_complete"
elif profile == "finding_fix_rerun":
    payload.update(
        {
            "source_exit": "implementation_required",
            "rerun_reason": "finding_fix",
            "finding_refs": ["throwaway-finding-1"],
        }
    )
else:
    raise SystemExit(f"unsupported throwaway Phase 2 profile: {profile}")
Path(sys.argv[3]).write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY
  public_output="$(
    "$TARGET/.agents/skills/guru-check-task/scripts/invoke.sh" \
      --input "${public_input#"$TARGET/"}" \
      --owner-result "$owner_result"
  )"
  rm -f "$public_input"
  python3 -c 'import json,pathlib,re,sys; payload=json.load(sys.stdin); assert set(payload) == {"exit_id","task_ref","phase2_commit_anchor"}; assert payload["exit_id"] == "passed"; assert payload["task_ref"] == sys.argv[1]; assert re.fullmatch(r"[0-9a-f]{40}", payload["phase2_commit_anchor"]); assert (pathlib.Path(sys.argv[2]) / sys.argv[3]).is_file()' "$TASK_REL" "$TARGET" "$owner_result" <<<"$public_output"
  printf '%s\n' "$public_output"
}

PHASE2_DTO="$(record_throwaway_phase2 "已检查初次提交的需求、设计、代码、测试、文档与安装边界。" initial_check)"
INITIAL_PLAN="$(prepare_task_commit_candidate initial_commit "feat(trellis): #122 验证安装后任务提交" "$PHASE2_DTO")"
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
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert set(payload) == {"status", "exit", "pre_commit_head", "commit_sha"}; assert payload["status"] == payload["exit"] == "committed"' <<<"$INITIAL_COMMIT_JSON"
INITIAL_COMMIT="$(python3 -c 'import json, sys; print(json.load(sys.stdin)["commit_sha"])' <<<"$INITIAL_COMMIT_JSON")"
test "$(git -C "$TARGET" show -s --format=%P "$INITIAL_COMMIT")" = "$BASELINE_HEAD"
test "$(git -C "$TARGET" show -s --format=%s "$INITIAL_COMMIT")" = "feat(trellis): #122 验证安装后任务提交"
test ! -e "$TARGET/$INITIAL_PLAN"
test -z "$(git -C "$TARGET" status --short --untracked-files=no)"
test "$(git -C "$TARGET" status --short -- unrelated-preserved.log)" = "?? unrelated-preserved.log"
test "$(cat "$TARGET/unrelated-preserved.log")" = "preserve this exact state"

printf '%s\n' "finding fix task change" >"$TARGET/src/task-commit-smoke.txt"
REVISION_PHASE2_DTO="$(record_throwaway_phase2 "已在 finding fix 后重新检查全部范围并绑定新的 HEAD 与 dirty state。" finding_fix_rerun)"
REVISION_PLAN="$(prepare_task_commit_candidate finding_fix_commit "fix(trellis): #122 验证 finding 修订提交" "$REVISION_PHASE2_DTO")"
REVISION_CANDIDATE_JSON="$(
  "$TARGET/.agents/skills/guru-create-task-commit/scripts/check-task-commit-plan.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --json \
    --candidate-artifact "$REVISION_PLAN"
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["candidate_validation"]["sequence"] == "001"; assert payload["candidate_validation"]["pre_commit_head"] == sys.argv[1]' "$INITIAL_COMMIT" <<<"$REVISION_CANDIDATE_JSON"
REVISION_COMMIT_JSON="$(
  "$TARGET/.agents/skills/guru-create-task-commit/scripts/create-task-commit.sh" \
    --root "$TARGET" \
    --task "$TASK_REL" \
    --json \
    --candidate-artifact "$REVISION_PLAN"
)"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert set(payload) == {"status", "exit", "pre_commit_head", "commit_sha"}; assert payload["status"] == payload["exit"] == "committed"; assert payload["pre_commit_head"] == sys.argv[1]' "$INITIAL_COMMIT" <<<"$REVISION_COMMIT_JSON"
REVISION_COMMIT="$(python3 -c 'import json, sys; print(json.load(sys.stdin)["commit_sha"])' <<<"$REVISION_COMMIT_JSON")"
test "$(git -C "$TARGET" show -s --format=%P "$REVISION_COMMIT")" = "$INITIAL_COMMIT"
test "$(git -C "$TARGET" show -s --format=%s "$REVISION_COMMIT")" = "fix(trellis): #122 验证 finding 修订提交"
test "$(git -C "$TARGET" rev-list --count main..HEAD)" = "2"
test ! -e "$TARGET/$REVISION_PLAN"
test -z "$(git -C "$TARGET" status --short --untracked-files=no)"
test "$(git -C "$TARGET" status --short -- unrelated-preserved.log)" = "?? unrelated-preserved.log"
test "$(cat "$TARGET/unrelated-preserved.log")" = "preserve this exact state"
if git -C "$TARGET" ls-tree -r --name-only HEAD | grep -Eq '(^|/)task-commit-plans/|^\.trellis/\.runtime/'; then
  echo "Task commit runtime evidence unexpectedly entered the committed tree" >&2
  exit 2
fi

TARGET="$INSTALL_TARGET"
PATH="$TASK_COMMIT_ORIGINAL_PATH"
unset TASK_COMMIT_REAL_GIT

INITIAL_CLOSEOUT_JSON="$(python3 "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_closeout.py" --repo "$TARGET" --case initial)"
printf '%s\n' "$INITIAL_CLOSEOUT_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["issue"] == 105; assert payload["local_head"] == payload["remote_head"] == payload["pr_head"]; assert payload["pr_ready"] is True; assert payload["after_archive_hook_preflight"] is True' <<<"$INITIAL_CLOSEOUT_JSON"
INITIAL_TASK_WORKSPACE_JSON="$(python3 "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py" --installed-repo "$TARGET" --work-root "$WORK_DIR/installed-task-workspace-initial")"
printf '%s\n' "$INITIAL_TASK_WORKSPACE_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["typed_exit"] == "created"; assert payload["checker_status"] == "passed"; assert payload["artifact_names"] == ["issue-scope-ledger.json"]; assert payload["task_creator"] == "fixture-maintainer"; assert payload["developer_identity_preserved"] is False; assert not any(payload[key] for key in ("source_developer_identity", "target_developer_identity", "source_workspace_journal", "target_workspace_journal"))' <<<"$INITIAL_TASK_WORKSPACE_JSON"

rm -f "$TARGET/.trellis/workflow.md.new"
(
  cd "$TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --create-new
)
test -f "$TARGET/.trellis/workflow.md.new"
if [[ "$USE_LOCAL_WORKFLOW_SAMPLE" == "1" ]]; then
  grep -q "Guru Team Development Workflow" "$TARGET/.trellis/workflow.md.new"
else
  grep -q 'guru-skill-invoke: {"skill":"guru-review-branch","required":true}' "$TARGET/.trellis/workflow.md.new"
  ! grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md.new"
fi
rm -f "$TARGET/.trellis/workflow.md.new"
test ! -e "$TARGET/.trellis/workflow.md.new"
(
  cd "$TARGET"
  trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force
)
apply_local_workflow_sample
grep -q 'guru-skill-invoke: {"skill":"guru-review-branch","required":true}' "$TARGET/.trellis/workflow.md"
! grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"

(
  cd "$TARGET"
  trellis update --force
)
verify_task_publication_validator_wrappers "after-trellis-update"
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
verify_task_publication_validator_wrappers "after-preset-reapply"

if [[ "$(workspace_tree_digest "$TARGET/.trellis/workspace")" != "$WORKSPACE_TREE_DIGEST_BEFORE" ]]; then
  echo "Update/reapply modified existing official workspace content" >&2
  exit 2
fi
if [[ "$(file_sha256 "$TARGET/.trellis/.developer")" != "$DEVELOPER_IDENTITY_DIGEST_BEFORE" ]]; then
  echo "Update/reapply modified existing official developer identity" >&2
  exit 2
fi

grep -q 'guru-skill-invoke: {"skill":"guru-review-branch","required":true}' "$TARGET/.trellis/workflow.md"
! grep -q "review-source independent-agent" "$TARGET/.trellis/workflow.md"
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
grep -q 'guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"blocked","consumer":{"kind":"stop","id":"task-workspace-blocked"}}' "$TARGET/.trellis/workflow.md"
test -f "$TARGET/.trellis/guru-team/schemas/finish-summary.schema.json"
test -f "$TARGET/.trellis/guru-team/schemas/closeout-plan.schema.json"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/discover-skill-contract.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/discover-skill-evals.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/run-skill-evals.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/run-skill-command.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/preview-finalization.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/record-finalization-gate.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/check-finalization-gate.sh"
test -x "$TARGET/.trellis/guru-team/scripts/bash/execute-finalization-transition.sh"
test -f "$TARGET/.trellis/guru-team/skills/adapters/eval/native_adapter.py"
test -x "$TARGET/.trellis/guru-team/skills/adapters/eval/shared.sh"
test -x "$TARGET/.trellis/guru-team/skills/adapters/eval/codex.sh"
test -x "$TARGET/.trellis/guru-team/skills/adapters/eval/claude.sh"
test -x "$TARGET/.trellis/guru-team/skills/adapters/eval/cursor.sh"
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
verify_finish_family_integration "after-update-reapply"
verify_issue_174_controlled_replay
"$TARGET/.trellis/guru-team/scripts/bash/discover-skill-contract.sh" --root "$TARGET" --mode installed --skill guru-sync-base --json >/dev/null
EXTENSION_CONTRACT_AFTER_UPDATE_JSON="$(
  "$TARGET/.trellis/guru-team/scripts/bash/discover-skill-contract.sh" \
    --root "$TARGET" \
    --mode installed \
    --skill guru-verify-extension-installation \
    --json
)"
python3 -c 'import json, sys; payload=json.load(sys.stdin); assert set(payload) == {"status","skill_id","interface_schema_id","input","invocation","outputs","consumer_inputs","projections","private_artifacts"}; assert payload["interface_schema_id"] == "guru-team-skill-interface-1.3"' <<<"$EXTENSION_CONTRACT_AFTER_UPDATE_JSON"
for root in .agents .claude .codex .cursor; do
  test -x "$TARGET/$root/skills/guru-verify-extension-installation/scripts/invoke.sh"
  test -x "$TARGET/$root/skills/guru-verify-extension-installation/scripts/execute-extension-verification.sh"
  test -x "$TARGET/$root/skills/guru-verify-extension-installation/scripts/record-extension-verification.sh"
  test -x "$TARGET/$root/skills/guru-verify-extension-installation/scripts/check-extension-verification.sh"
done
EXTENSION_EVAL_AFTER_UPDATE_JSON="$(
  "$TARGET/.trellis/guru-team/scripts/bash/run-skill-evals.sh" \
    --root "$TARGET" \
    --mode installed \
    --skill guru-verify-extension-installation \
    --adapter shared \
    --run-root "$WORK_DIR/extension-verification-after-update-eval" \
    --json
)"
python3 -c 'import json, sys; payload=json.load(sys.stdin); assert payload["status"] == "passed"; assert payload["interface_schema_id"] == "guru-team-skill-interface-1.3"; assert [case["actual_exit"] for case in payload["cases"]] == ["verified", "blocked", "not_required", "return_to_task_work", "blocked", "verified", "verified"]; assert all(case["status"] == "passed" for case in payload["cases"])' <<<"$EXTENSION_EVAL_AFTER_UPDATE_JSON"
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
python3 - "$TARGET" "$POST_UPDATE_TASK_REL" "$POST_UPDATE_BRANCH" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
task_rel = sys.argv[2]
branch = sys.argv[3]
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
issue = {
    "number": 114,
    "url": "https://github.com/castbox/guru-trellis-throwaway/issues/114",
    "title": "Post-update contract wording review",
    "reason": "Current post-update planning scope.",
}
ledger = {
    "schema_version": "2.0",
    "primary_issue": issue,
    "close_issues": [issue],
    "related_issues": [],
    "followup_issues": [],
}
for name, payload in (
    ("task.json", task),
    ("issue-scope-ledger.json", ledger),
):
    (task_dir / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
workspace_slug = task["id"]
runtime_root = root / ".trellis/.runtime/guru-team"
runtime_payloads = (
    (
        runtime_root / "workspaces" / f"{workspace_slug}.json",
        {
            "schema_version": "1.0",
            "workspace_slug": workspace_slug,
            "workspace_path": str(root.resolve()),
            "source_checkout": str(root.resolve()),
            "branch_name": branch,
            "updated_at": "2026-08-01T00:00:00Z",
        },
    ),
    (
        runtime_root / "tasks" / f"{task['id']}.json",
        {
            "schema_version": "1.0",
            "task_slug": task["id"],
            "workspace_slug": workspace_slug,
            "workspace_path": str(root.resolve()),
            "task_artifact_dir": task_rel,
            "updated_at": "2026-08-01T00:00:00Z",
        },
    ),
)
for path, payload in runtime_payloads:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
"$REPO_ROOT/trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh"
grep -q '^session_auto_commit: false$' "$TARGET/.trellis/config.yaml"
grep -q '^\.trellis/workspace/$' "$TARGET/.gitignore"

UPDATED_CLOSEOUT_JSON="$(python3 "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_closeout.py" --repo "$TARGET" --case after-update)"
printf '%s\n' "$UPDATED_CLOSEOUT_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["issue"] == 106; assert payload["local_head"] == payload["remote_head"] == payload["pr_head"]; assert payload["pr_ready"] is True; assert payload["after_archive_hook_preflight"] is True' <<<"$UPDATED_CLOSEOUT_JSON"
UPDATED_TASK_WORKSPACE_JSON="$(python3 "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py" --installed-repo "$TARGET" --work-root "$WORK_DIR/installed-task-workspace-after-update" --existing-developer-identity)"
printf '%s\n' "$UPDATED_TASK_WORKSPACE_JSON"
python3 -c 'import json, sys; payload = json.load(sys.stdin); assert payload["status"] == "ok"; assert payload["typed_exit"] == "created"; assert payload["checker_status"] == "passed"; assert payload["artifact_names"] == ["issue-scope-ledger.json"]; assert payload["task_creator"] == "fixture-maintainer"; assert payload["developer_identity_preserved"] is True; assert all(payload[key] for key in ("source_developer_identity", "target_developer_identity")); assert not any(payload[key] for key in ("source_workspace_journal", "target_workspace_journal"))' <<<"$UPDATED_TASK_WORKSPACE_JSON"

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
