# Workflow Mode Selector Contract

This is a semantic Skill with a minimal public handoff. The public input only
identifies the invocation mode and caller continuation. The AI must not infer
the selection from a script, keyword list, or recorder result.

Entry includes proposed-change requirements discussion, feature design, and
planning even when this turn defers file writes or resource creation. A direct
information-only answer about existing facts remains outside this entry.
For no-task change intent, loading an upstream method does not replace the
actual public selection or the selected Guru owner. Respect deferred side
effects while following the workflow's mandatory graph.

The owner-private result is transient and contains the semantic selection,
confirmation disposition, and current continuation identity. The public DTO
contains only `exit_id`; the consumer is selected by the typed exit. Missing,
stale, duplicate, unknown, or unmapped results fail closed.

The selection has three AI-owned outcomes when there is no explicit task-free
intent: high-confidence bounded low-risk work selects `task_free`; likely but
insufficient evidence opens one mode question; clearly complex or high-risk
work, requirements clarification, or full change planning selects
`standard_intake`. The AI judges that need from the current request and facts;
deferred writes alone neither select task-free nor introduce a mode question.
An already bounded local edit retains the ordinary task-free selection rules,
including explicit intent and the one real mode choice when needed.
Issue presence, file count, paths, and keywords
cannot independently decide the outcome.

For a local fix, trace the actual changed behavior and its unchanged consumers
before judging risk. A purchase-eligibility prompt or its display condition does
not by itself change pricing, charging, entitlement, or a payment protocol.
Conversely, a UI-only diff may alter one of those behaviors through a shared
consumer. Read the relevant condition, data source and call path, then choose
the route from the actual effect and required validation. Reuse investigation
facts whose current inputs and dependencies still apply; redo the current mode
judgment when scope, authority or risk changes. An already relevant formal Task
continues through its original lifecycle rather than this no-task selection.

Checkout suitability is owned by `guru-execute-task-free-change`, not this DTO.
That Skill reads live local topology, binding, scope and dirty facts and owns
linked non-base execution location selection before writes; isolation alone
never selects standard Intake. It never queries branch protection. The selector
decides only mode and never acquires resources or creates a Task identity. The dialogue-local origin of the selection distinguishes
automatic re-selection from explicit-task-free scope narrowing without adding
public fields or persisted authorization state.

## Public Invocation

Complete the AI-owned selection before invoking the wrapper. Author public input
under [public-input.schema.json](../schemas/public-input.schema.json), using the
current [initial_request example](../examples/public-input.json). Author the
transient owner result under
[workflow-mode-selection.schema.json](../schemas/workflow-mode-selection.schema.json),
using the [selection example](../examples/workflow-mode-selection.json). Set the
actual selected `typed_exit` and matching `selection`; a `blocked` result has no
`selection`. Both objects carry the same current `mode` and `continuation_id`.
The example illustrates shape; it does not decide the current route.

The existing wrapper supports two alternative transports:

- `--invocation` accepts an inline JSON object or `-` for stdin. Its two fields
  are `public_input` and `owner_result`, each containing the complete object.
  It does not accept a file locator. For example, after the corresponding
  semantic selection:

  ```sh
  bash scripts/invoke.sh --invocation '{"public_input":{"profile":"initial_request","mode":"workflow","continuation_id":"no-task-turn-1"},"owner_result":{"schema_version":"1.0","typed_exit":"task_free","mode":"workflow","selection":"task_free","continuation_id":"no-task-turn-1"}}'
  ```

  To read that same envelope from a call-local UTF-8 file through stdin, use
  `bash scripts/invoke.sh --invocation - < call.json`.
- `--input` and `--owner-result` each accept a regular UTF-8 JSON file locator
  or `-` for stdin. Relative locators resolve first from the current working
  directory, then from this package. For the declared examples:
  `bash scripts/invoke.sh --input examples/public-input.json --owner-result examples/workflow-mode-selection.json`.
  At most one parameter can consume stdin. These two flags do not accept inline
  JSON objects; use `--invocation` for inline transport.

Resolve `scripts/invoke.sh` from this package or its installed platform projection.
Do not combine `--invocation` with either separate flag. Consume the complete
stdout as one formal result under the selected original output schema:
[standard_intake](../schemas/public-standard-intake-output.schema.json),
[task_free](../schemas/public-task-free-output.schema.json), or
[blocked](../schemas/public-blocked-output.schema.json). Each output contains
only `exit_id`. Preserve a failed command's exit status, stdout and stderr and
follow its specific remediation; a failed invocation is not a selected route.

## Environment and configured path query

`scripts/check-env.sh --root <invocation-checkout> --json` remains the public
read-only environment entry. `worktree_root` now reports the absolute generated
root from the confirmed primary project's `.trellis/guru-team/config.yml`.
The query confirms primary with live Git topology, actual toplevel and
common-dir/gitdir identity. The common-dir parent and porcelain first row are
not sufficient anchors. Empty configuration resolves to
`<primary-parent>/<primary-name>-worktrees`; relative values resolve from
primary; absolute values are used directly. The response includes `primary_root` and `worktree_config_path` for the calling
AI to review. When a worktree name is supplied, `checkout_root` is the absolute
generated target. Read these fields from the command receipt's `result`.
It is a call-local
query, not the selector's typed DTO or a persisted location map.

Pass `--worktree-name <single-directory-name>` to derive a new target. Add
`--checkout-root <absolute-planned-path>` to check that plan against the derived
target before creation. A checkout-root check requires a worktree name. A path
mismatch, unavailable primary anchor or conflicting nonempty invocation
configuration produces a diagnostic; it does not silently choose another path
or modify configuration. An empty linked template is not a separate location
choice. Normal spaces and quoted scalar values follow the supported config
scalar parsing contract.

The formal creation owner consumes this fact and validates
`acquisition.path_source=configured` again before acquisition. The task-free
owner consumes the prechecked target through ordinary Git and rereads the
actual directory and registration. Each owner first separates adoption or
recovery from new generation. Genuine explicit locations, adopted external
checkouts and original Task recovery retain their original checks, without a
configured-root allowlist. Mode selection, semantic review, naming and exact
side-effect confirmation remain with their original AI owners.

See [MIGRATION-760](../../../../../presets/guru-team/MIGRATION-760.md) for
published absolute-path input compatibility and the environment output change.
