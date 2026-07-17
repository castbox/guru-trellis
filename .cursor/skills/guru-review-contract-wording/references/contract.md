# Contract Wording Review Contract

## Ownership And Modes

`guru-review-contract-wording` is the semantic owner of controlled contract
wording review. The global workflow owns only mandatory invocation, profile
routing, unique typed-exit consumers, and fail-closed stops. Shared runtime
owns only deterministic scope construction, scanning, recording, and checking.

Workflow and standalone modes have identical entry preconditions. A copied
package is not portable without the compatible Guru Team preset, extension
manifest, dispatcher, runtime scripts, installed inventory, and selected
platform discovery copy.

## Fixed Profiles

### `change_request`

The scope is one live issue or side-effect-free draft. Title and body are
always required and cannot be excluded. The AI may select authoritative
comments before review; every selected comment records stable identity, author,
updated time, selection reason, and content hash. Unselected comments are not
contract authority. Live mutation requires exact payload confirmation,
preimage match, mutation evidence, and live reread. For each live issue
revision, the recorder derives one confirmed-payload digest from source
identity, locator, field, preimage hash, and confirmed content hash, plus one
mutation-result identity from the same target, preimage, reread content hash,
and current source update time. Human confirmation binds the ordered set of
confirmed payload digests; the checker requires the mutation result to match
the rebuilt live scope. Draft review remains side-effect-free.

### `planning_artifacts`

The scope is exactly the current active task's `prd.md`, `design.md`, and
`implement.md`, in that order. All three must be regular files. The caller may
not supply a selector, alias, replacement, or exclusion. Passed evidence is
task-local `contract-wording-review.json`; older different evidence may be
replaced only during an explicit same-profile re-entry after it is proven
stale.

In addition to the common wording Review Gate, this profile must explicitly
review and record all seven planning semantics inherited from #93:

- `no_requirement_weakening`: the planning artifacts do not weaken a confirmed
  requirement.
- `source_issue_semantics_preserved`: the source issue's confirmed semantics
  remain present and unchanged.
- `conditional_paths_have_conditions`: every conditional path names its exact
  trigger and resulting behavior.
- `no_parallel_implementation_paths`: the plan selects one owner/path for each
  behavior instead of leaving competing implementations active.
- `gates_have_machine_verifiable_conditions`: every deterministic gate names
  objective pass/block conditions that its recorder or validator can check.
- `acceptance_criteria_are_deterministic`: every acceptance criterion has an
  exact observable outcome rather than implementation discretion.
- `external_quotes_are_labeled_non_contract`: external quotations and historical
  text are explicitly labeled as non-contract when they are not operative
  requirements.

The AI records these results under
`ai_review_gate.planning_checked_dimensions`. Every key is required for this
profile. A successful exit requires every value to be `true`; a false value
requires a blocked Gate and revision or escalation. `change_request` and
`explicit_paths` must not carry this planning-only object.

### `explicit_paths`

The scope is the non-empty set of repo-relative Markdown files explicitly
named by the standalone user for this invocation. Absolute paths, parent
traversal, non-Markdown files, missing files, symlinks, and paths outside the
repository fail closed. This profile cannot replace either workflow profile
and writes no fixed repository cache.

## Vocabulary `contract-wording-v2`

The complete controlled-term set is:

`可以`, `允许`, `建议`, `推荐`, `可选`, `尽量`, `尽可能`, `最好`, `应该`,
`应当`, `原则上`, `一般`, `通常`, `视情况`, `根据情况`, `根据需要`, `按需`,
`必要时`, `如有需要`, `需要时`, `适当`, `适当时`, `合理`, `合理时`, `类似`,
`相关`, `相应`, `等`, `等等`, `之类`, `一些`, `若干`, `部分`, `至少`, `默认`.

The deterministic scanner emits every term occurrence in vocabulary order for
each scope item and one-based line. A hit identity binds the scope item,
locator, line, term, text, and current content SHA-256. Scanner output never
contains classification or semantic pass judgment.

## Classifications `contract-wording-classifications-v1`

Every current hit has exactly one AI-selected classification and a non-empty
reason:

- `contract_violation`: unresolved weak or ambiguous contract wording; always
  unchecked and blocking.
- `quoted_source_non_contract`: text is an explicitly labeled external quote,
  not the current contract.
- `term_definition`: text defines or explains a controlled term without using
  it as an operative requirement.
- `literal_identifier`: the term occurs inside an exact identifier, command,
  path, field, or other literal token.
- `historical_record_non_contract`: text records prior behavior or history and
  is explicitly non-normative.
- `deterministic_threshold`: `至少` is bound to a concrete numeric threshold.
- `deterministic_default`: `默认` is bound to one concrete fallback value or
  deterministic resolution rule.
- `deterministic_option`: an option is a closed enumerated user/product choice,
  not implementation discretion.
- `deterministic_reference`: words such as `相关` or `相应` name an exact,
  auditable reference object.

Unknown, missing, duplicate, stale, or empty-reason classifications fail
closed. `contract_violation` and every unclassified current hit are projected
into `unchecked_normative_hits`; a passed result requires that array to be
empty.

## Semantic Closed Loop

Execute exactly:

1. validate entry and build the complete fixed profile scope;
2. run the deterministic scan;
3. prefer an authorized rewrite that makes weak clauses deterministic;
4. classify each retained lexical hit and record a non-empty reason;
5. after any mutation, rebuild the complete scope and rescan current content;
6. complete the AI Review Gate;
7. obtain exact human confirmation only when mutation or semantic preservation
   requires it;
8. call the recorder and checker; and
9. return exactly one typed exit.

The common AI Review Gate confirms the required profile scope was not narrowed,
every current hit is classified, unchecked hits are empty for a passed Gate,
rewrites did not change unconfirmed product meaning, retained classifications
match current text and deterministic conditions, and zero lexical hits were
not treated as a substitute for complete requirements review. The
`planning_artifacts` profile then performs the seven additional planning
semantic checks defined above; neither another profile nor the deterministic
runtime may infer those results.

## Evidence And Exits

Schema `guru-contract-wording-review-1.0` binds profile, mode, normalized scope
items, content hashes, scope/scan/result digests, every scanner hit, revisions,
classifications, derived unchecked hits, the AI Review Gate, conditional human
confirmation, and exactly one exit.

For `planning_artifacts`, the same schema conditionally requires the exact
seven-key `planning_checked_dimensions` object. Missing, false-on-success,
extra, or non-planning use fails closed. The recorder/checker validate the
recorded shape and values; they do not perform the semantic review or generate
`true` values.

The schema keeps the `1.0` id while adding backward-compatible optional live
issue mutation fields. They are mandatory only for a current
`change_request` live issue revision. Planning, explicit-path, draft, and
historical no-revision evidence do not acquire a synthetic mutation binding.

- `pass`: current scope/scan, all hits classified, zero unchecked hits, passed
  Gate, and no revision awaiting caller handling.
- `content_changed`: one or more authorized revisions are bound to current
  post-change scope and rescan plus a passed Gate; the fixed profile consumer
  performs complete re-entry.
- `blocked`: the Gate is blocked because scope, authority, confirmation, or a
  violation prevents safe completion.

The exit/Gate relation is biconditional: `blocked` if and only if the Gate is
blocked. Unknown profile, exit, consumer, selector, or stale identity fails
closed.

## Planning Approval Migration

`record-planning-approval` consumes only current `planning_artifacts:pass`
evidence through `--contract-wording-evidence`. It deterministically projects
all hits, classifications, reasons, empty unchecked hits, and each already
validated `planning_checked_dimensions` value into the existing planning
approval audit shape, while preserving explicit post-planning user confirmation
and the three planning document digests. It never defaults or derives a
planning semantic result. The planning recorder does not own vocabulary,
scanning, classification, or the seven planning judgments.

`check-planning-approval` first validates current wording evidence, then its
projection and planning approval facts. A pre-migration active approval without
current wording evidence must rerun this Skill and obtain fresh explicit
post-planning approval before implementation. Archived task artifacts are not
rewritten.

Evidence recorded before the seven profile-specific fields were introduced is
also stale migration input, even when it uses schema id
`guru-contract-wording-review-1.0`. Regenerate the wording evidence through a
fresh AI review of all common and planning-specific dimensions, display the
three planning documents, obtain fresh explicit post-planning confirmation,
and record a new approval. Never patch the missing booleans into old evidence.
