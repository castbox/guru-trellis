# Guru Team Workflow Skill Package Contract

## Ownership

`trellis/skills/guru-team/` is the only canonical source for reusable Guru
Team workflow skill packages. The global workflow owns phase order, mandatory
invocation, cross-skill transitions, and typed-exit consumers. Each active
package owns its complete step-local behavior. Installed copies under
`.trellis/guru-team/skills/` and platform skill roots are generated runtime
assets and never become semantic sources of truth.

The workflow marketplace installs `.trellis/workflow.md`; it does not install
external skill packages. The Guru Team preset is the complete extension
configurator and installs active packages after validating the canonical source.

## Registry Lifecycle

`trellis/skills/guru-team/registry.json` is validated by
`schemas/skill-registry.schema.json` and has three states:

- `reserved` claims a stable `guru-<action>-<object>` id only. It has no package,
  route, interface, or platform destination and must never be installed.
- `planned` claims a future stable consumer id only. It has no package,
  interface, invoke marker, exit marker, or platform destination and must never
  be installed. An active Skill may declare a typed exit to that id; callers
  stop at the missing-Skill gate until a later delivery promotes it to a
  complete active package.
- `active` declares a package path, interface path, supported platform targets,
  validator command, and workflow route identity. Every referenced file and
  route must pass source validation before installation.

Activating, renaming, or retiring an id is a public API change. A breaking
change requires a new id or an explicit migration contract. Production
registries must never contain test fixtures.

The task work commit migration keeps `guru-create-work-commit` reserved as a
compatibility tombstone and activates `guru-create-task-commit`. The reserved
reason identifies the active replacement; the old id must never acquire a
different package or route meaning.

## Package And Interface

An active package contains a short `SKILL.md`, `interface.json`, and the
references/scripts/examples/tests declared by its interface. `SKILL.md` starts
with exactly one closed `---` frontmatter block containing only `name` and
`description`. `name` equals the stable `guru-<action>-<object>` id in the
registry and interface; `description` is non-empty and byte-for-byte equal to
the interface description. Missing, duplicated, unclosed, ambiguous, or drifted
frontmatter fails source validation. The Markdown body contains only triggering,
routing, execution entry, and fail-closed rules. Long behavior and authoring
guidance belong in package-local `references/`.

`interface.json` is validated by `schemas/skill-interface.schema.json` and
declares stable identity, workflow and standalone modes, identical entry
preconditions, evidence identity and freshness, `judgment_mode`, ordered stages, artifacts,
schemas, objective validators, external exits, re-entry behavior, tests, and
platform destinations. The stage profile is exact:

1. `semantic`: forward behavior, AI Review Gate, conditional human
   confirmation, deterministic recorder/validator, exactly one typed exit;
2. `deterministic`: forward behavior, deterministic recorder/validator,
   exactly one typed exit.

Only a Skill whose inputs, state transitions, side effects, and pass/block
conditions are completely machine-verifiable may declare `deterministic`, and
only when its boundary contains no scope, sufficiency, finding, revision,
user-choice, or route-intent judgment. Caller-side AI route classification can
precede invocation but is not a Skill-internal post-execution Gate. Any semantic
judgment or human confirmation forces the `semantic` profile.

Every `tests[]` entry is a package-relative `tests/<file>` path. It must be
unique, lexically safe, resolve to an existing regular file below that active
package's `tests/` root, and pass the same component-by-component `lstat`
boundary as other package assets. Labels, missing paths, paths outside
`tests/`, and symlink-backed evidence are invalid. Package tests are part of the
installed/package/platform inventories rather than an untracked assertion.

Workflow and standalone execution use the same preconditions and may reuse
evidence only when its identity and freshness still match. Missing, stale, or
ambiguous evidence fails closed. A deterministic script may execute, record, or
validate machine facts, but never decides scope, sufficiency, findings,
revision action, human-confirmation need, semantic pass, or route intent.

`workflow` and `standalone` are stable routing mode ids, not package formats.
`workflow.routing=global_workflow` means the global workflow loads the package
through its mandatory marker. `standalone.routing=direct_discovery` means a
selected platform may discover and invoke the package without global workflow
routing. Both modes still require the complete, compatible Guru Team preset,
extension runtime, shared dispatcher, companion scripts, installed manifest,
and managed package inventory. `standalone` never means that one copied Skill
directory is self-contained or portable outside that installation.

Every active interface declares the closed `runtime_dependency` object with
extension id, runtime API version, installed manifest path, shared dispatcher
id, preset distribution id, and package portability. Each validator declares a
stable `runtime_command` that the extension manifest publishes. Source and
installed validation bind those fields to the extension capability, and reject
missing fields, wrong routing, dependency drift, unknown commands, or different
workflow/standalone preconditions before a package command can run.

## Public Skill I/O And Private State

### 0. Versioned Interface And Registry Migration

`guru-team-skill-interface-1.2` is the frozen legacy contract. Its schema file,
schema id, and field meanings are not reinterpreted by the minimal-handoff
rollout. All nine current production packages now select the independent
`guru-team-skill-interface-1.3` contract; archived 1.2 artifacts remain
historical and are never rewritten as public handoff state.

Registry schema `guru-team-skill-registry-1.1` is the exact version selector.
Every active row declares `interface_schema_id` and `io_contract_state`; only
`1.2 + legacy` and `1.3 + minimal_handoff` are legal. Reserved and planned rows
remain lifecycle-only and must not carry package or I/O contract fields. The
completed #145 and #146 activation units own the public migration history; the
live active registry contains no `legacy` row.

The validator selects the interface schema from the registry row. It must not
guess from optional fields, file presence, package content, or extension
defaults. The extension publishes both supported ids, names 1.3 as current for
new work, uses compatibility scalar `interface_schema_id=1.3`, and publishes
exact public-input, typed-output, and private-artifact schema inventories for
all nine active production packages.

### 1. Scope And Trigger

This contract applies whenever a new public Guru Team Skill is introduced or an
existing Skill's input, typed exits, consumer mapping, schema, recorder, or
runtime boundary is materially changed. Existing packages migrate through
separate reviewed issues and explicit compatibility contracts; this rule does
not silently reinterpret or break an already published API.

Public Skill I/O is a transport contract between independently owned workflow
steps. It is not a serialization of the producing Skill's complete reasoning,
live repository snapshot, recorder state, recovery state, or audit trail.

### 2. Signatures And Ownership

Each Skill owns one concise public input contract. Each typed exit owns one
independent output contract whose sole purpose is to hand the minimum required
data to that exit's declared consumer or fail-closed stop. When several exits
have different shapes, publish separate exit schemas; an optional aggregate
schema may use `oneOf` only as a validator index, never as an authoring template
filled with nullable fields.

The consumer independently owns its input contract. A `kind=skill` consumer
normally uses `contract.kind=skill_input`. The three production semantic edges
declared below use the additive
`contract.kind=skill_input_authoring_seed`; both kinds exact-reference the
target Interface and profile, and the referenced interface id must equal the
declared consumer id. A producer-owned or third-party schema cannot stand in
for the target Skill's input. A structured `kind=workflow` consumer uses a
canonical locator below `consumers/workflow/`; a structured `kind=stop`
consumer uses one below `consumers/stop/`. The original locator must equal its
normalized repo-relative spelling, include a file below that exact owner root,
and must not use producer package/output paths, the other consumer root,
absolute paths, parent traversal, `.` segments, repeated separators, or
symlink-backed components. A zero-payload stop has no schema locator. A producer
output may be passed directly only when it already matches the independently
owned input exactly. Otherwise the workflow/runtime declares one thin
deterministic projection from the selected exit output to the consumer input.
The projection may select, rename, or normalize fields; it must not recover
hidden semantics by reading Python source, replaying the producer's AI judgment,
or understanding its private artifact.

A deterministic Skill may use scalar CLI arguments instead of an input JSON
schema when those arguments fully express the public call. Do not create an
input schema merely for structural symmetry.

Every Interface 1.3 scalar argument explicitly declares boolean `required`.
Only arguments with `required=false` may be omitted; remaining flag/value pairs
preserve declaration order, may not repeat, and still pass their declared type
validator. `guru-sync-base.base_branch` is optional. Omitting it passes an
unspecified value to the same owner resolver used by explicit calls, so the
existing configured-scalar, ordered-candidate, and remote-default precedence is
not duplicated in the wrapper.

### 3. Input, Output, And Private Contracts

Public input contains only values the caller must intentionally supply. Public
output contains only values the next consumer must receive. Every public output
field must name at least one direct consumer use in the package contract and
tests. A field with no direct consumer is removed rather than retained for
possible future debugging, reporting, or audit.

The following values are private by default and must not appear in a public
typed handoff unless a named consumer cannot complete its next step without the
specific value:

- derived hashes, projection digests, timestamps, file size/mode/mtime, and full
  Git status or changed-path snapshots;
- complete GitHub/Trellis/live-source payloads that the consumer can reread from
  a stable identity;
- scanner hit inventories, excluded candidates, review narratives, reviewer
  identity, finding history, and validation command transcripts;
- recorder bookkeeping, re-entry history, transaction state, and recovery
  details.

When ordinary stale/mismatch prevention is required, expose only the smallest
identity or freshness token the consumer actually validates. Runtime-private
checkpoint state may persist task-locally or in the ignored runtime namespace
under its existing ownership rules, but its schema is not a public Skill output
schema. Gate evidence may remain auditable under the workflow evidence contract;
it is a separate artifact and must not inflate the handoff DTO.

### 4. Validation And Error Matrix

- output field has no declared direct consumer -> reject the package contract;
- one nullable/optional object represents structurally different exits -> split
  it into independent exit contracts;
- consumer needs producer-private fields or source-code knowledge -> add a thin
  projection or redesign the boundary before activation;
- runtime-derived fact appears in authoring input without caller ownership ->
  derive it inside runtime or remove it;
- a semantic Skill handoff cannot fill its target profile from the minimal DTO
  alone -> use the target-owned `skill_input_authoring_seed` contract only for
  an approved edge, then merge projected seed fields with fresh caller-authored
  fields without overwrite; do not add defaults, private lookups, or semantic
  inference;
- audit/checkpoint field appears only for history or diagnostics -> keep it in a
  private artifact or remove it from the workflow entirely;
- required freshness cannot be proved from the minimal handoff -> add the
  narrowest stable identity/token and its consumer validation, not a full
  snapshot;
- an existing public field must change incompatibly -> publish a new schema/id
  or an explicit migration contract.

### 5. Good, Base, And Bad Cases

Good: `context_ready` returns a target identity plus the small set of relevant
context values consumed by requirements clarification. `refresh_base` returns
only its exit identity and the retry reason/token consumed by base sync. Their
schemas are independent.

Base: a deterministic Git synchronization Skill accepts `--base`, `--remote`,
and an expected resolution token as CLI arguments and returns the selected base
identity required by the next Skill. It does not add an input JSON schema.

Bad: one final artifact schema contains AI review prose, every prerequisite
projection, complete live Git/GitHub facts, digests, timestamps, recovery
history, and fields for all exits, and callers must read runtime source to learn
which subset to author or consume.

### 6. Tests Required

Package and integration tests for a new or materially revised Skill I/O must:

- validate one independent input example and one output example for every
  structurally distinct typed exit;
- assert that every output field is consumed by the declared next Skill,
  workflow transition, or explicit stop response;
- validate every producer-output-to-consumer-input projection without importing
  or reading the companion runtime source;
- prove that removing private audit/checkpoint fields from public output does not
  break supported freshness, re-entry, or recovery behavior;
- run the normal clean-install workflow path with no Agent read/import of
  `guru_team_trellis.py` or another private runtime implementation to construct
  public input or interpret public output.

Examples cover each structurally distinct exit/profile, not the Cartesian
product of equivalent modes. They are executable contract fixtures, not large
illustrative audit records.

### 7. Wrong Versus Correct

Wrong:

```json
{
  "typed_exit": "context_ready",
  "generated_at": "...",
  "reviewer": "...",
  "all_scan_hits": [],
  "all_git_facts": {},
  "facts_sha256": "...",
  "refresh_base_reason": null,
  "blocked_reason": null
}
```

Correct producer exit output:

```json
{
  "exit": "context_ready",
  "target": {"repo": "castbox/guru-trellis", "issue": 130},
  "context": {"requirements": ["minimal typed handoff"]},
  "source_version": "2026-07-20T10:00:00Z"
}
```

The consumer's independently owned input schema may accept that object directly
or declare a deterministic projection to its own field names. The producer's
audit evidence and private checkpoint remain outside this public DTO.

### 8. Interface 1.3 Closed Public Contracts

Interface 1.3 keeps the closed-loop identity, modes, stages, validators,
external exits, re-entry, tests, and platform destinations of 1.2 and adds one
required closed `public_contracts` object with exactly six owned sections:

- `input`: either `structured_json` profiles with package-local closed Draft
  2020-12 schemas/examples and a discriminator plus aggregate `oneOf`, or
  `scalar_cli` arguments with exact ordered argv and no artificial input JSON
  schema;
- `invocation`: one command id, package-local executable wrapper, exact input
  binding, `single_typed_exit` stdout, stable closed error schema/example, and
  one executable example argv;
- `outputs`: one independent schema and complete example for every declared
  external exit, plus non-empty direct consumer-use references;
- `consumer_inputs`: locators owned by the target Skill, workflow transition,
  or stop response; a Skill locator exactly equals the canonical target
  interface path registered for that active target id, self-reentry points to a
  distinct input profile of the same Skill, structured workflow and stop
  locators use their exact `consumers/workflow/` and `consumers/stop/` roots,
  and a stop may explicitly declare zero payload;
- `projections`: exactly one output/consumer projection using only `direct`,
  `select`, `rename`, or the closed deterministic `normalize` operations;
- `private_artifacts`: only `runtime_checkpoint` or `gate_evidence`, with
  `stdout_only_pre_task`, `task_local_tracked`, or `ignored_runtime`
  persistence.

All ids and locators are unique, package paths are regular non-symlink files,
and public output schema ids and paths are each independently disjoint from
private artifact schema ids and paths. Projection source fields come only from
the selected public output; target fields come only from the declared consumer
input. Every non-`direct` projection, and every `direct` projection into
`scalar_cli`, must statically prove that each required consumer field comes from
a required producer field and that every legal source value remains valid after
the declared mapping/normalizer or direct same-name pass-through. The 1.3 proof
grammar is deliberately conservative: exact property schemas, finite `const`/`enum`
normalization, non-empty scalar strings, positive integers, and ASCII trim with
an explicit non-blank source pattern are accepted; an unprovable relation fails
activation even when one example passes. Runtime facts, private artifacts,
arbitrary expressions, script paths, and semantic reconstruction are outside
the projection grammar.

The additive target-owned `skill_input_authoring_seed` consumer contract is
valid only for a structured target profile. It exact-references that target
Interface/profile and declares unique non-empty `seed_fields`, unique non-empty
`authoring_fields`, and one package-local authoring example. The two field sets
must be disjoint and their union must exactly equal the target profile's
top-level `required` set. The authoring example contains exactly
`authoring_fields`; the producer projection consumes every public output field
and produces exactly `seed_fields` using only the existing
`direct|select|rename|normalize` operation grammar. Validation checks the seed
and authoring objects independently, performs a no-overwrite merge, then
validates the merged object against the complete target profile schema.
Missing, extra, unknown, duplicate, overlapping, overwritten, defaulted, or
runtime-authored fields fail closed. This consumer kind does not add a fifth
projection operation and does not authorize reading producer private state or
reconstructing AI judgment.

An explicit `zero_payload` stop still receives the producer's typed-exit
routing identity, but that identity is not forwarded as stop-response payload.
Its output schema therefore contains only required `exit_id` with the matching
exit constant, and its unique projection is `select` with an empty `mappings`
array. Empty `select` is invalid for every non-zero consumer, and any additional
zero-stop output field is an unconsumed public field rather than audit data to
preserve.

Every 1.3 public input, output, consumer, invocation-error, and private-artifact
schema uses the standard-library Draft 2020-12-compatible closed subset. The
accepted grammar is recursive and contains only `$schema`, root-only `$id`, `$defs`,
local `$ref`, annotations, `type`,
`const`, `enum`, `allOf|anyOf|oneOf|not|if|then|else`, string length/pattern and
supported format constraints, numeric minimum/maximum, array
length/uniqueness/items/contains, and object properties/required/boolean
`additionalProperties`. Nested `$id` resource boundaries, boolean schema nodes,
unresolved/remote/unsafe/recursive refs,
unknown keywords such as `patternProperties`, malformed keyword values,
unsupported formats, and invalid patterns fail source and installed validation.
This is not a claim that the companion implements the complete Draft 2020-12
vocabulary. The one package-relative exception is the aggregate structured
input's exact ordered profile-schema index. Each target must be a regular
non-symlink object-schema file within the same validated package boundary and
is independently checked as a declared profile contract.

#### Portable Pattern Grammar

The closed subset does not accept an arbitrary Python, PCRE, or ECMA regular
expression. A `pattern` source is limited to printable ASCII `U+0020` through
`U+007E`, and both schema validation and instance matching use this exact
grammar (EBNF braces mean repetition; quoted braces are pattern characters):

```text
pattern             = alternative, { "|", alternative } ;
alternative         = { term } ;
term                = assertion | atom, [ quantifier ] ;
assertion           = "^" | "$" | negative-lookahead ;
negative-lookahead  = "(?!", pattern, ")" ;
atom                = literal | "." | escape | character-class | group ;
group               = "(", pattern, ")" | "(?:", pattern, ")" ;
quantifier          = "*" | "+" | "?"
                    | "{", decimal, "}"
                    | "{", decimal, ",}"
                    | "{", decimal, ",", decimal, "}" ;
decimal             = digit, [ digit, [ digit, [ digit, [ digit, [ digit ] ] ] ] ] ;
digit               = "0" | "1" | "2" | "3" | "4"
                    | "5" | "6" | "7" | "8" | "9" ;
```

`literal` is one printable ASCII character other than
`\ [ ] ( ) | ^ $ . * + ? { }`; those syntax characters are literals only
through an allowed syntax escape. `escape` is exactly one of:

- `\\t`, `\\n`, `\\v`, `\\f`, or `\\r`;
- `\\u` plus exactly four hexadecimal digits whose value is at most `U+007F`;
- `\\s` or `\\S` outside a character class;
- a backslash followed by one of `^ $ \\ . * + ? ( ) [ ] { } | /`.

A `character-class` is `[` plus optional leading `^`, one or more class items,
and `]`. A class item is one ASCII code point, one ascending range of two ASCII
code points, one allowed control/ASCII-`\\u`/syntax escape, or `\\s`. A raw `-`
is a literal when it is not between two range endpoints; `\\-` is also allowed.
Classes are non-empty, cannot nest, cannot use `\\S`, and cannot use a set escape
as a range endpoint.

Matching is unanchored search, equivalent to
`new RegExp(pattern, "u").test(instance)`, unless the pattern supplies its own
anchors. Search probes UTF-16 code-unit boundaries, so a zero-width assertion
may succeed between the high and low surrogate of one astral code point. A
consuming Unicode atom still treats that valid surrogate pair as one code point,
cannot split it through backtracking, and cannot start at the interior low
surrogate boundary. An isolated high or low surrogate is one independently
consumable code point. A neighboring BMP code unit does not make it part of a
pair: an isolated high surrogate before a BMP code unit and an isolated low
surrogate after a BMP code unit remain two independently consumable code points.
No multiline, ignore-case, or dot-all flag is available.
`$` means strict end of input, including rejection before a final line
terminator. `.` matches one Unicode-aware code point except `LF`, `CR`,
`U+2028`, and `U+2029`.
`\\s` is exactly `U+0009-U+000D`, `U+0020`, `U+00A0`, `U+1680`,
`U+2000-U+200A`, `U+2028`, `U+2029`, `U+202F`, `U+205F`, `U+3000`, and
`U+FEFF`; `\\S` is its complement. Capturing and non-capturing groups have the
same matching behavior because backreferences are not in the grammar.

The grammar rejects every other escape or group form, including `\\d`, `\\D`,
`\\w`, `\\W`, Unicode property escapes, backreferences, named groups, positive
lookahead, lookbehind, and inline flags. It also rejects non-ASCII source or
`\\u` values, raw control characters, empty/nested/malformed classes, descending
ranges, malformed or descending bounded quantifiers, a bound longer than six
decimal digits, and lazy, possessive, misplaced, or repeated quantifiers. The
runtime must fail closed at the schema grammar gate and must not fall back to
Python `re.compile(pattern)` or `re.search(pattern, instance)`.

All 1.3 registry, interface, schema, example, workflow-marker, package-local
reference, invocation-stdout, and discovery JSON boundaries use standard JSON
decoding. The runtime rejects `NaN`, `Infinity`, `-Infinity`, and JSON numbers
that overflow its finite numeric range; the same finite guard applies to
in-memory schema and instance values. Public DTO encoding rejects non-finite or
otherwise non-serializable values and returns the existing structured error
shape without a traceback. Supported `date-time` validates RFC 3339 calendar,
clock, the `0000` through `9999` year domain, numeric-offset, lowercase `t`/`z`,
and leap-second notation only at the corresponding UTC June/December month-end
boundary. Supported `uri` validates the RFC 3986 ASCII generic syntax,
including a required scheme, component and authority grammar, case-insensitive
IPvFuture `v`, controls/whitespace, and percent encoding. These two formats
remain the complete supported format set for this closed subset.

### 9. Discovery, Invocation, And Error Contract

The extension public command id is `discover-skill-contract`. Its installed
wrapper has the exact public form:

```bash
.trellis/guru-team/scripts/bash/discover-skill-contract.sh \
  --root <repo> --mode <source|installed> --skill <guru-id> --json
```

Discovery resolves the exact registry row first. A 1.2 row returns a closed
`legacy` variant with interface identity, migration state, and #145/#146
boundary; it never fabricates 1.3 input/output contracts. A 1.3 row returns a
closed `minimal_handoff` index locating input, invocation, every exit output,
consumer contract, projection, examples, and private artifacts. Discovery
returns metadata only and does not execute the semantic Skill.

Unknown skill, version/state mismatch, missing/unsafe contract path, invalid
schema/example, or installed drift exits non-zero with stable `code`,
repo-relative `field_path`, and actionable `remediation`. Callers need only
`SKILL.md`, `interface.json`, package-local public assets, and command help;
they never import or read `guru_team_trellis.py`.

Source validation executes the declared representative 1.3 example invocation,
requires exactly one declared typed-exit object on stdout, and validates it
with that exit's independent schema. The mixed test-only fixture contains one
1.2 legacy package, one structured semantic 1.3 package, and one scalar CLI
deterministic 1.3 package. It covers Skill/workflow/stop consumers,
self-reentry, the closed projection operations, stdout-only and task-local
private state, distinct exits, and stable errors, but never enters production
registry, extension inventories, workflow routes, or installed platform roots.

### Stage 0 Production Activation

`stage0-minimal-handoff-v1` is one atomic production activation unit. It contains
exactly these active packages and exits:

- `guru-sync-base`: `synced`, `skipped`, `blocked`;
- `guru-discover-change-context`: `context_ready`, `refresh_base`, `blocked`;
- `guru-clarify-requirements`: `clear`, `needs_context`, `refresh_context`,
  `retarget_context`, `new_task`, `blocked`;
- `guru-review-contract-wording`: `pass`, `content_changed`, `blocked`;
- `guru-review-change-request`: `ready`, `clarify_requirements`,
  `review_wording`, `refresh_context`, `blocked`;
- `guru-create-task-workspace`: `created`, `refresh_review`, `cancelled`,
  `blocked`.

All six select `guru-team-skill-interface-1.3` plus `minimal_handoff` together.
The Stage 0 manifest retains its historical three-id `legacy_skill_ids`
boundary as frozen migration metadata; the live registry no longer treats
those ids as legacy after the independent production activation.
The registry, workflow markers, extension inventories, migration manifest,
canonical packages, installed packages, and selected platform copies must expose
the same six-package and 24-exit sets. A mixed Stage 0 graph is invalid even when
each package validates in isolation.

The six package input contracts are consumer-owned and closed. `guru-sync-base`
retains a scalar CLI signature; the other packages use discriminator-based
structured profiles for pre-task/re-entry, initial/scope-change/standalone,
wording target, readiness target, and initial/recovery mutation families.
Each profile has an executable example. Each exit has its own schema/example,
one consumer, one declarative projection, and direct-use pointers for every
public output field. Stop exits use `exit_id` plus empty `select` projection to
`zero_payload`; errors and review evidence remain private.

Existing recorder/checker results stay owner-private `runtime_checkpoint` or
`gate_evidence` with `stdout_only_pre_task`, `task_local_tracked`, or
`ignored_runtime` persistence. Re-entry passes only caller-owned continuation
and task-relative locators; the owner runtime rereads live facts, validates the
old artifact with its published schema, and emits a current 1.3 DTO without
rewriting archived bytes.

The five semantic public wrappers run only after their Agent-owned semantic
loop and recorder/checker stage. Their invocation accepts the closed
caller-owned public input plus repo-relative owner-result/supporting locators,
reruns the existing objective checker, and derives the exit only from the
checker-passed owner result. A caller-selected expected exit, public output
example, or private artifact body is never a production routing input. Declared
package examples and repo-relative caller JSON files are the only structured
public-input path families; pre-task callers do not need to write into a
managed package.

For `guru-clarify-requirements:clear`, a checker-passed
`active_task_scope_change` result may legitimately carry
`target_disposition=null` when the accepted action updates only the active task
scope. That one fixed profile projects to public `retained`; null disposition in
initial or standalone profiles remains an invalid owner projection.

### Production Planning, Check, And Commit Activation

`production-minimal-handoff-v1` is a separate atomic activation unit. It does
not modify the ordered Stage 0 manifest, its `activation_unit_id`, its six-skill
identity, or its 24-exit set. The production unit contains exactly:

- `guru-approve-task-plan`: `approved`, `revision_required`, `clarify_scope`,
  `blocked`;
- `guru-check-task`: `passed`, `implementation_required`, `planning_stale`,
  `blocked`;
- `guru-create-task-commit`: `committed`, `revision-required`, `blocked`.

The ten closed structured input profiles are `initial_review`,
`revision_reentry`, `clarification_reentry`, `initial_check`,
`finding_fix_rerun`, `planning_reentry`, `initial_commit`,
`revision_reentry`, `finding_fix_commit`, and `recovery_resume`. Profile ids are
package-local: the two `revision_reentry` profiles are intentionally owned by
different Skills. Each profile has one executable example and at least one
current eval case binding.

The public DTOs are exact. Planning emits `approved(exit_id, task_ref,
approval_ref)`, `revision_required(exit_id, task_ref)`,
`clarify_scope(exit_id, task_ref, proposal_refs)`, or blocked `exit_id` only.
Check emits `passed(exit_id, task_ref, checked_head, check_ref)`,
`implementation_required(exit_id, task_ref, finding_refs)`,
`planning_stale(exit_id, task_ref, planning_route, proposal_refs)`, or blocked
`exit_id` only. Commit emits `committed(exit_id, task_ref, base_ref,
committed_head)`, `revision-required(exit_id, task_ref)`, or blocked `exit_id`
only. `branch-review-or-finding-closure` continues to consume exactly
`task_ref`, `base_ref`, and `committed_head`; Issue #146 does not activate or
change the planned downstream package.

Planning and check wrappers materialize their existing task-local owner input,
invoke the existing recorder/checker pair, and project only the checker-passed
actual exit. The commit wrapper uses a deterministic private candidate builder
to combine caller-owned message/path/review/authorization intent with live
task, Phase 2, ledger, Git, snapshot, and sequence facts. The builder then
calls the existing candidate validator and transaction executor unchanged.
Caller-selected `expected_exit`, artifact bodies, digests, file metadata,
absolute paths, and runtime snapshots are not public input.

Exactly three semantic handoffs use target-owned authoring seeds:
`guru-approve-task-plan:revision_required -> revision_reentry`,
`guru-check-task:passed -> guru-create-task-commit:initial_commit`, and
`guru-create-task-commit:revision-required -> revision_reentry`. Their projected
seed fields are respectively `source_exit/task_ref`,
`source_exit/task_ref/checked_head/check_ref`, and
`source_exit/task_ref`. Target package authoring examples supply every remaining
required fresh semantic field. The validator proves disjoint partition,
required-set equality, no-overwrite merge, and full target-schema validity;
all other Skill/workflow/stop consumers keep their existing contracts.

Active closure is derived from the live registry plus the frozen Stage 0
manifest, the production manifest, and any future complete active Interface
1.3 rows absent from both manifests. Every active profile and exit must have a
current canonical case binding and byte-identical selected-platform corpus.
The current cardinality assertion is nine active Skills and 35 exits; missing,
extra, duplicate, renamed, legacy, unknown, partially activated, or
case-mismatched entries fail closed.

## Workflow Markers And Typed Exits

Mandatory routing is machine-readable HTML-comment JSON:

```markdown
<!-- guru-skill-invoke: {"skill":"guru-example-action","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-example-action","exit":"completed","consumer":{"kind":"workflow","id":"phase-3"}} -->
```

Every active skill has exactly one mandatory invocation identity. Every
external exit has exactly one workflow/skill consumer or one explicit
fail-closed stop. Unknown, duplicate, multiple, or unmapped markers fail source
validation. Reserved ids must not appear in markers. Planned ids may appear
only as a Skill consumer; a planned invoke or exit marker is invalid.
Frontmatter auto-match is discovery assistance only and never replaces
mandatory invocation markers.

`guru-approve-task-plan` is the only semantic owner of Phase 1 planning
approval and the single `planning-approval.json` artifact. Its interface uses
`judgment_mode=semantic`, declares the same ordered entry preconditions in
workflow and standalone modes (`runtime_dependency`, `task_workspace`,
`requirement_authority`, `planning_artifacts`, `docs_ssot_plan`,
`contract_wording_evidence`, `scope_ledger`, `repository_snapshot`, and
`invocation_freshness`), and depends on the shared runtime commands
`record-planning-approval` and `check-planning-approval`.

The package owns adequacy and ambiguity review, the authoritative load-bearing
provenance review, implementation-choice review, unusual-scenario proposal
review, planning revision, final AI Review Gate, conditional dedicated
proposal confirmation, explicit post-planning confirmation, and re-entry.
`guru-review-contract-wording:planning_artifacts:pass` remains the only wording
owner. Recorder/checker consume AI-reviewed input and may validate only paths,
schema, hashes, locators, projections, repository facts, freshness, and the
closed Gate/exit/consumer union; they must not select load-bearing statements,
assign provenance, judge an implementation choice or scenario, create a
confirmation, pass the AI Gate, or select a route.

An `approved_scope_expansion` entry uses a closed `proposal_binding`,
`confirmation`, and `authority_binding`. The proposal source is either one
controlled current planning-artifact locator or one canonical unusual candidate
id. Runtime recomputes that source digest, requires the source-appropriate
`dedicated-scope-expansion` or `dedicated-unusual-scenario` confirmation, binds
the same digest plus the runtime-materialized current authority SHA-256, and
requires that authority in the entry refs. An unusual candidate link projects
the candidate's existing confirmation/authority rather than creating a second
approval. A caller-only digest, wrong locator/candidate/confirmation/authority,
or disagreement between any proposal digest fails closed in both modes.

The `approved` union has no unresolved AI review state: findings, revision
actions, scope proposals, and blocking reasons are all empty, and both the
post-planning prompt and confirmation timestamps are non-null date-times.
Every unusual candidate records at least one alternative. A candidate with
`disposition=explicit_requirement` records at least one source requirement ref,
and every recorded source requirement ref resolves to a current requirement
authority id. The schema, recorder, and checker enforce these objective
shape/reference constraints.

The task projection's `scope_ledger_sha256`, and any requirement-authority
entry that points to the same task-local ledger, use the canonical digest of
only the semantic scope categories: positive issue numbers from `primary_issue`,
`close_issues`, `related_issues`, and `followup_issues`, with each list sorted
and deduplicated. It excludes acceptance evidence, `scope_decisions`, embedded
planning-approval hashes, and other ledger metadata. Those records have their
own evidence bindings and may evolve after approval without creating a circular
planning identity; moving an issue between scope categories still invalidates
approval.

The four external exits and unique consumers are:

- `approved` -> workflow target `phase-1-task-activation`;
- `revision_required` -> Skill `guru-approve-task-plan`;
- `clarify_scope` -> workflow target `guru-task-plan-clarify-scope-router`;
- `blocked` -> stop `task-plan-approval-blocked`.

Before task activation, repository snapshot freshness includes selected base,
base ref/HEAD, invocation HEAD, and dirty paths. After activation, normal
implementation HEAD/dirty drift does not invalidate otherwise current planning.

`revision_required` restarts after task-local planning changes and a fresh
wording review. `clarify_scope` delegates through the three-field routing-only
workflow target, which establishes scope context and mandatory invokes
`guru-clarify-requirements:active_task_scope_change`; the caller AI authors the
complete clarification input from fresh live context before all nine planning
entry checks restart. Unknown, duplicate, multiple, unmapped, or
consumer-mismatched exits fail closed. The package uses closed schema
`guru-planning-approval-2.0`; active schema 1.2 approval artifacts require a
complete semantic re-entry and v2 recording, while archived artifacts remain
historical.

`guru-create-task-commit` is mandatory after a fresh final Phase 2 pass and
before every task work stage/commit side effect. It exposes only `committed`,
`revision-required`, and `blocked`: Branch Review/finding closure consumes the
first, the skill re-enters on the second, and the workflow stops on the third.
Finding-fix task work returns through implementation and full Phase 2 before a
new plan sequence may invoke the skill again. Workflow and standalone entry
preconditions include ordinary Git operation state. Gitlink snapshot identity
is conditional on index mode `160000` and binds an initialized, clean worktree
HEAD; for non-deleted gitlinks that artifact HEAD is also the exact index OID,
not a hint for `git add` to reread from the worktree. Ordinary legacy plan
entries do not require gitlink-only or copy-relation fields. New snapshot
producers distinguish rename and copy with mutually exclusive `renamed_from`
and `copied_from`. Only a rename source inherits destination deletion/exact-
stage authority; copy provenance never stages its source, and a dirty copy
source requires an independent classification. Existing SHA-256/mode/delete/
rename facts remain the ordinary exact-index authority for historical plans.
The validated in-memory plan is the only candidate-self byte authority. Executor
staging and hooks run on an isolated index/detached transaction HEAD; only a
fully validated commit/index/result is published. The executor retains the
real Git index lock through conditional ref/candidate publication and rollback,
immediately guards and verifies the conditionally advanced loose ref, uses a
candidate guard plus exact published-result identity for candidate
rollback, keeps `index.lock` as a sentinel while an independent temporary file
publishes the live index, and linearizes success at the final candidate
inode/content identity read after ref/index/result publication. A candidate
writer before that read forces owned ref/index rollback while preserving its
bytes; a writer after it is a preserved later operation and immutable commit
blob/result digest evidence remains committed.
A failed stage, hook, operation, postcondition or publication preserves exact
transaction-owned preimages; loss of conditional ref/candidate ownership
preserves third-party state and fails closed without claiming exact restore.

`guru-sync-base` is mandatory immediately after tool-free Phase 0 request
classification and before the first repo/network semantic read. It declares
`judgment_mode=deterministic`; its workflow and standalone modes have identical
entry preconditions: `runtime_dependency`, `decision_checkout`,
`selected_base_resolution`, `clean_checkout`, and `result_facts`.
Standalone requires an explicit refresh/verify request and cannot return
`skipped`. Workflow exits are exactly `synced` to
`guru-discover-change-context`, `skipped` to `original-request-route`, and
`blocked` to `base-sync-blocked`.

The package declares `sync-base` and `check-base-sync` runtime commands and
schema `guru-base-sync-result-1.0`. Its wrappers remain dispatcher-only. The
caller owns tool-free route classification and standalone intent recognition.
The runtime deterministically selects the first existing configured candidate;
multiple existing candidates follow config order and are not ambiguous.
Resolution/result facts remain on stdout. The executor preserves
`resolution_sha256` as the pre-sync resolve-to-execute identity and emits
`post_sync_resolution` plus `post_sync_resolution_sha256` after synchronization.
`check-base-sync` validates both identities, schema, facts digest, and live Git
equality without mutation, then returns the post-sync digest. `prepare-task`
reuses the same resolver/sync core for its query-only reads and consumes the
current post-sync digest. It has no mutation guard; active workspace mutation
freshness belongs to `guru-create-task-workspace`.

`guru-discover-change-context` is the active semantic consumer of
`guru-sync-base:synced`. Both modes require identical `runtime_dependency`,
`fresh_base`, `repository_identity`, `change_input`, and
`evidence_freshness` preconditions. Its exact semantic stages are the schema
1.2 five-stage profile. The package owns the fixed current-state-before-history
sequence, AI candidate selection/deep-read, AI Review Gate, conditional human
confirmation recorded as not required, same-snapshot recorder/validator, and
the exits `context_ready`, `refresh_base`, and `blocked`.

Its base evidence embeds the complete validator-passed
`guru-base-sync-result-1.0` object rather than a HEAD-only projection. Runtime
validation rechecks the result/schema digests, post-sync resolution, decision
branch, selected remote refs, strict GitHub remote repository identity, and a
fail-closed Git status read before later semantic sources. Pre-task and
standalone validation bind the live checkout to the sync result's decision
branch. Direct active task recording/checking instead binds the live checkout
to `task.json.branch`, because task/worktree creation may move the same HEAD to
a feature branch after the stdout snapshot was reviewed; it still requires the
original HEAD, complete sync provenance, selected local/remote base refs,
repository identity, direct active task locator/status, and task-local-only
dirty paths. A proposed draft
that names a created issue carries a separate live issue binding whose body
digest must equal the original reviewed draft digest. Semantic evidence shape
requires a non-empty mem summary when used and non-empty reviewed scope plus
load-bearing conclusions for a passed AI Gate. A zero-candidate preview fixes
selected/excluded/deep-read evidence to empty and fixes mem review to the
`not_needed` shape, so it cannot reach `trellis mem` or another history source;
candidate previews retain the four-source insufficiency gate. Scripts validate
these shapes but do not supply the judgment.
The live source change may bind an `open` or `closed` issue after normalizing
the supported GitHub state spelling; duplicate candidates and a draft-created
issue binding remain open-only. Current-state evidence that records a Git
object id must resolve `HEAD:<path>` to exactly a blob. A tree, gitlink commit,
tag, missing object, or mismatched blob cannot satisfy the required Docs,
code/contracts, or tests evidence groups.

Duplicate candidate facts are not caller-trusted free-form fields. Their
canonical digest projection is normalized bound `repo`, positive `number`,
`identity=#<number>`, canonical issue URL, `state=open`, and `updated_at`.
Source validation/runtime pure checks recompute that digest, identity, and URL
from the fields returned by the one duplicate search. They do not issue a
second search or re-read candidates after AI review. The package result schema
and runtime also enforce
`typed_exit=blocked` if and only if `ai_review_gate.status=blocked`.

Deep-read shape is source-discriminated: selected archived task artifact,
canonical GitHub issue/PR URL, or exact live Git object/ref. Each locator is
validated by its own closed structural contract, and active-task
`task_branch_stale` remains a normal refreshable complete re-entry reason.

External consumer resolution is part of both source and installed validation.
Skill consumers must name an active or planned registry id. An active consumer
must resolve to its complete installed package; a planned consumer is an
explicit unavailable transition and stops fail closed without fallback.
Workflow/stop consumers must have exactly one matching
`guru-workflow-target` / `guru-stop-target` marker; missing, duplicate,
kind-mismatched, or dangling targets fail closed.

The package publishes artifact schema `guru-context-discovery-1.0`, scoring
algorithm id `guru-context-history-score-1.0`, and dispatcher-only wrappers for
`preview-change-context-history`, `record-context-discovery`, and
`check-context-discovery`. The history command may enumerate only
`.trellis/tasks/archive/**/finish-summary.json` and project only top-level
`index`; it never reads index siblings, workspace/runtime state, or a repo-level
archive index/cache. Scripts validate AI-authored selection and Gate evidence
but do not select candidates, judge sufficiency, decide duplicate reuse, or
synthesize semantic pass.

For `refresh_base`, the result records the current stable stale codes,
superseded query digest, superseded snapshot digest, reason, and detection
time. Recorder/checker compare those caller-authored facts with current live
freshness and require complete skill re-entry. The commands consume only the
current payload and expected snapshot identity; they do not reconstruct an
external ancestry chain.
Task-local record/check also require the exact target to be non-ignored under
`git check-ignore --quiet --no-index --` before and after recording and during
checking. Ignore matches or unreadable trackability fail closed; pre-task mode
remains stdout-only and does not perform this target gate.
The `task_local_reentry` wrapper validates `task_locator` and the fixed
`prior_snapshot_locator=context-discovery.json` before binding the owner result;
the owner checker receives that exact task locator and may not infer it from
private artifact content. Task-local snapshots carry private
`task_worktree_state` bound to current HEAD and every dirty path/status/content/
mode/rename fact, excluding only the fixed snapshot itself and ignored runtime
state. A different-byte fixed snapshot may be replaced only after the existing
target is proved regular and trackable, its schema/identity matches an explicit
`--expected-prior-snapshot-sha256`, and the complete new snapshot passes live
and worktree-state checks. The replacement binds the prior identity through
`superseded_snapshot_sha256`; same-byte retry is idempotent.

`guru-clarify-requirements` is an active semantic package with identical
workflow/standalone preconditions: compatible runtime, current review target,
current context evidence, source authority, and invocation-context freshness.
Its exact schema 1.2 stages are `forward_behavior -> ai_review_gate ->
conditional_human_confirmation -> recorder_validator -> typed_exit`. The Skill
loads `trellis-brainstorm` as its one-question method, but owns question
selection, convergence, scope classification, action selection, confirmation
necessity, semantic pass/block, and typed route.

The result uses closed top-level fields and artifact schema
`guru-requirements-clarification-1.0`. Repository-answerable questions must be
`answered` or `not_answerable` with at least one checked evidence reference
before the first user
question. Each clarification round contains one `question_id`; an
`atomic_group` is permitted only for an indivisible product choice and records
its reason. Every round's `question_id` must be opened in that round or already
open; `answer_status=partial` cannot close any question and therefore cannot
disappear through an empty lifecycle. The reducer keeps exactly
`open_questions = opened - closed`, rejects closing-before-open and reopening
after closure. The recorder
derives all proposal, action, payload, content, and result digests; the checker
recomputes them and validates current live/task facts without generating
questions, choosing actions, classifying scope, executing GitHub writes, or
turning deterministic success into a semantic pass.

Source actions are `none`, `issue_comment`, `issue_body_edit`,
`proposed_draft_update`, `new_issue_draft`, and
`active_task_scope_update`. GitHub mutation remains AI-owned: after exact
action-digest-bound confirmation, the AI uses an existing connector or a
reviewed `gh` command, rereads live facts, and supplies mutation evidence to
the recorder. Checker binds the human-confirmed action payload, canonical
payload digest, mutation result content digest, and reread live body/comment;
any byte mismatch fails closed. Generic continuation, task creation, planning approval, or
review confirmation cannot satisfy action or scope-proposal confirmation.
`unconfirmed_expansion + accepted_current` requires a dedicated
proposal-digest-bound confirmation. A proposal with
`optional_mechanism_origin=true` cannot be `accepted_current`; the mechanism is
removed/replaced or its independent product value is proposed separately.
For an active task, `unconfirmed_expansion` classified as `related`,
`followup`, `new_task`, or `out_of_scope` also requires dedicated
proposal-digest-bound user decision evidence; an AI-only classification is not
a final auditable decision.

The five exits and unique consumers are `clear` -> workflow target
`guru-requirements-clear-router`, `needs_context` -> Skill
`guru-discover-change-context`, `refresh_context` -> Skill `guru-sync-base`,
`new_task` -> workflow target `guru-full-task-intake-chain`, and `blocked` ->
stop `requirements-clarification-blocked`. Active-task `clear`/`new_task`
requires a non-empty terminal proposal set. `clear` requires no open questions,
a passed current AI Gate, current authority/context, every five-class scope
classification exactly confirmed, confirmation-free mechanism dispositions,
and no unrefreshed mutation. A successful GitHub mutation
returns `refresh_context`; a reviewed side-effect-free new issue draft returns
`new_task`; `blocked` is valid if and only if the AI Gate is blocked.

Pre-task and standalone results remain stdout-only. There is no dedicated
tracked clarification artifact. Every five-class active-task classification binds a
structured `decision_trail` that must exactly match one current
`issue-scope-ledger.json.scope_decisions[]` entry. The trail records exact
proposal decisions, user-decision evidence, live GitHub comment/body authority
including `updated_at`, `context_before_task_update_sha256`, all three planning documents, planning
approval, review state, interrupted resume target, stale downstream identities,
and re-entry owners `guru-approve-task-plan`, `guru-check-task`, and
`guru-review-branch`. The active-task checker reuses the shared complete schema
1.2 planning validator and exact-binds reviewed/approved document evidence; a
prior file hash, placeholder planning body, or minimal approval JSON does not
qualify. GitHub authority mutation returns `refresh_context`; only a context
snapshot generated at or after authority `updated_at`, followed by a task update
bound to that snapshot, may later return active-task `clear` or `new_task`.
That `active_task_scope_update` is authorized by the same
`exact_source_action_and_scope` confirmation as the classification proposals:
its action id is listed in `confirmed_actions[]`, and the confirmation action
digest exact-binds the canonical confirmed action set. Proposal-only
confirmation, planning approval, or validated task evidence cannot substitute.
Task-only update requires no second refresh. `mechanism_removed/replaced`
remains outside confirmation/trail/action mutation. `new_task` still contains only the
side-effect-free reviewed draft and #112 owns creation. A copied package without
the complete compatible preset remains non-portable and fails closed through
the dispatcher.

`invocation_context.resume_target` is caller-aware and closed. Initial
issue/draft accepts only `guru-review-contract-wording`; standalone accepts only
`guru-standalone-caller`; active-task accepts the planning-review target or one
of the declared interrupted Phase 1/2/3/Branch Review targets. Accepted-current
scope requires the planning-review target.

`guru-review-contract-wording` is the active semantic owner for controlled
contract wording review. Workflow and standalone modes use identical runtime,
scope, mutation-authority, semantic-evidence, and freshness preconditions. Its
exact schema 1.2 stages are `forward_behavior -> ai_review_gate ->
conditional_human_confirmation -> recorder_validator -> typed_exit`.

The package owns vocabulary `contract-wording-v2`, classification contract
`contract-wording-classifications-v1`, the rewrite/classification/review loop,
profile scope contracts, confirmation policy, artifact schema
`guru-contract-wording-review-1.0`, and exits `pass`, `content_changed`, and
`blocked`. The three profiles are closed: `change_request` always includes
title/body plus AI-selected authoritative comments whose stable identity,
non-empty author, update time, selection reason, and content hash are all
present; `planning_artifacts`
always binds the active task's `prd.md`, `design.md`, and `implement.md` and
requires the canonical contract's exact
`semantic_review.ai_review_gate.planning_checked_dimensions` object before a
successful exit; it writes task-local `contract-wording-review.json`.
`change_request` and `explicit_paths` prohibit that planning-only object, and
`explicit_paths` accepts only
the standalone caller's explicit repo-relative Markdown regular files and is
stdout-only. Workflow callers cannot substitute `explicit_paths` for either
fixed workflow profile.

The deterministic runtime publishes `record-contract-wording-review` and
`check-contract-wording-review`. It builds fixed scope facts, scans current
content, derives identities/digests and unchecked hits, validates schema,
classification/reason structure, freshness, rescan binding, Gate/exit
invariants, exact planning-dimension shape/value, and trackability. It never
chooses scope, rewrite, classification,
reason sufficiency, semantic pass/block, confirmation need, or route intent.
It also never infers or defaults a planning semantic result; only the AI Review
Gate may produce the values required by the canonical package contract.
Every content change invalidates the prior scope/scan identity and requires a
complete rebuild and rescan before evidence can pass.
Task-local evidence replacement uses one objective state transition contract.
Stale evidence requires `--replace-stale`. After the fixed consumer has entered
a complete same-profile re-entry, structurally current `content_changed` or
`blocked` evidence may be superseded only when
`--supersede-reentry-facts-sha256` equals the existing `facts_sha256`; the new
evidence must differ from the old artifact and independently pass full current
validation. The flags are mutually exclusive; identical-result, wrong-profile,
or stale supersession fails closed, and a current `pass` remains protected. The
recorder validates these facts but does not decide that the AI/workflow should
re-enter or which new exit is correct.
For a live issue revision, the recorder derives the exact confirmed-payload
digest from source identity, locator, field, preimage hash, and confirmed
content hash, and derives a mutation-result identity from the current reread
content plus source update time. The checker requires human confirmation to
bind the ordered payload digest set and the mutation result to equal the
rebuilt live scope. This is deterministic normal-flow consistency evidence,
not an authenticity, hostile-input, locking, or TOCTOU boundary.

Unique consumers are `pass` -> workflow target
`guru-contract-wording-pass-router`, `content_changed` -> workflow target
`guru-contract-wording-change-router`, and `blocked` -> stop
`contract-wording-blocked`. Those routers use only the checker-validated
profile and exit. Unknown, multiple, stale, or unmapped profile/exit evidence
fails closed. Planning approval is only a consumer/projection of current
`planning_artifacts:pass` evidence and cannot become a second vocabulary,
classification, scanner, or semantic-review owner.
Its compatibility projection copies each already-validated planning dimension
from that evidence. Planning evidence recorded before the planning-only field
existed is stale even with schema id `guru-contract-wording-review-1.0`; active
tasks must perform a complete fresh AI review, display all three planning
documents again, and obtain fresh post-planning confirmation. Missing booleans
must never be patched into old evidence, while archived artifacts remain
historical.

## Change Request Readiness Package

Active semantic Skill `guru-review-change-request` is the sole pre-task
readiness owner after `guru-review-contract-wording:change_request:pass`. It
consumes current context, clarification, and wording results; normalizes one
`existing_issue`, `proposed_draft`, or `standalone_request`; reviews the fixed
ten dimensions; records findings, scope conclusion, AI Review Gate, optional
confirmation, and exactly one exit. Its exits are `ready` -> active
`guru-create-task-workspace`, `clarify_requirements` ->
`guru-clarify-requirements`, `review_wording` ->
`guru-review-contract-wording`, `refresh_context` -> `guru-sync-base`, and
`blocked` -> stop `change-request-review-blocked`.

The record/check commands are stdout-only before task creation. They reuse the
existing objective context, clarification, and wording validators; project
portable hashes and error codes; rebuild target/linkage/facts digests; and
validate closed schema, fixed dimensions/findings references, Gate/exit
invariants, consumer identity, and freshness. They never search history or
duplicates, read Docs/code/tests for semantic judgment, generate findings,
select a delivery unit, infer a Gate, or map objective error codes to an exit.
For a proposed draft or standalone request they derive `source_request_sha256`
from #113's exact draft authority projection: `kind=draft`, normalized repo,
null issue/URL/update authority, `state=draft`, and current reviewed-body
SHA-256. Title hash and draft/request/caller identity stay separately bound.
An arbitrary 64-hex value, including a normal producer's stale prior digest,
fails closed before prerequisite linkage is accepted.
Only the active `guru-create-task-workspace` package may persist the exact
checker-passed bytes as task-local `issue-review.json` while creating the
workspace. `ready` has no legacy prepare fallback.

## Task Workspace Package

Active semantic Skill `guru-create-task-workspace` is the sole owner of GitHub
issue creation and branch/worktree/task creation after change-request
readiness. Workflow and standalone modes use identical `runtime_dependency`,
`base_evidence`, `context_evidence`, `clarity_evidence`, `wording_evidence`,
`readiness_evidence`, `target_authority`, `naming_and_assignee`,
`side_effect_authorization`, and `invocation_freshness` preconditions. Its
exact stages are `forward_behavior -> ai_review_gate ->
conditional_human_confirmation -> recorder_validator -> typed_exit`.

The package owns target presentation, semantic naming, assignee routing, exact
side-effect plan, two mutually exclusive confirmation scopes, AI Review Gate,
ordinary recovery disposition, and typed route. Runtime commands are
`record-task-workspace-plan`, `create-task-workspace`, and
`check-task-workspace-result`; artifact schemas are
`guru-task-workspace-plan-1.0` and `guru-task-workspace-result-1.0`. Recorder,
executor, and checker validate deterministic facts only and never select a
duplicate, target, closed-state disposition, semantic name, assignee route,
confirmation need, Gate status, or exit intent.

A reviewed-draft invocation may only create the exact confirmed issue. Before
create, it searches live open issues for the exact reviewed title, body,
labels, and a creation time not earlier than the reviewed plan. Zero matches
permits one create, one match is recovered and reread, and multiple matches
fail closed. It binds the live title/body/update facts to the reviewed draft
and confirmation, returns `refresh_review`, and performs no
branch/worktree/task/runtime mutation. An open-issue invocation uses a separate
`workspace_and_task_mutation` confirmation and may return `created` only after
the branch/worktree/task, four tracked task-local Intake artifacts, ignored
runtime mappings, and workspace boundary all pass objective validation.
The non-mutation matrix is equally explicit: passed Gate plus a digest-bound
`refused` active confirmation yields `cancelled`; `reroute` with no active
confirmation yields `refresh_review`; `blocked` with no active confirmation
yields `blocked`. Runtime preserves these AI-authored facts and may mutate only
for passed plus confirmed.

An open-issue plan that continues a workflow-created draft embeds the complete
prior checker-passed `created_issue` result and its binding digest. The result
facts digest, binding facts digest, reviewed draft id/digest, creation
confirmation digest, current issue authority, and complete Intake rerun's live
existing-issue identity must all agree. The fresh context is `kind=issue` with
canonical URL/open state/update time/body/facts identity and null
`issue_binding`. Ordinary existing issues carry null result and binding fields;
missing, partial, or mixed provenance fails closed.

The plan also binds the checker-passed base result's
`post_sync_resolution_sha256`. Before the first GitHub issue or workspace/task
mutation, the executor runs the shared resolver and sync core once. The fresh
selected base, refs, decision/local/remote HEADs, and post-sync identity must
equal the reviewed plan. A normal remote advance may be fetched and safely
fast-forwarded, but it returns `refresh_review` before issue, branch, worktree,
task, artifact, or runtime mutation because the reviewed base identity changed.

Assignee resolution order is explicit input, exactly one issue assignee, zero
issue assignees to current GitHub login, then an AI/user choice for multiple or
unresolved candidates. In an isolated subprocess, the exact executor calls
official `common.task_store.cmd_create` with the resolved assignee and replaces
that module's developer accessor with a null result only for the handler
invocation. The official fallback therefore writes
`task.json.creator=task.json.assignee=<reviewed-login>` without reading or
rewriting `.trellis/.developer`. The executor never copies, initializes, or
restores `.trellis/.developer` or `.trellis/workspace/**`; existing official
identity/journal bytes are outside this package and remain unchanged.

External exits are exactly `created` to workflow target
`guru-task-workspace-created`, `refresh_review` to active Skill
`guru-sync-base`, `cancelled` to stop `task-workspace-cancelled`, and `blocked`
to stop `task-workspace-blocked`. A target/disposition change is
`refresh_review` with zero writes. Unknown, multiple, unmapped, stale, or
consumer-mismatched exits fail closed.
Public plan/result stdout and examples contain no absolute workspace path; the
checker derives the expected worktree from current repo config, reviewed slug,
and live Git facts. Absolute mappings stay only in ignored runtime files.

## Phase 2 Task Check Package

`guru-check-task` is the only semantic owner of the complete Phase 2 task
check and of the single task-local `phase2-check.json` artifact. It declares
`judgment_mode=semantic`, the exact five-stage semantic profile, and identical
workflow/standalone preconditions in this order: `runtime_dependency`,
`task_workspace`, `approved_planning`, `requirement_provenance`,
`implementation_handoff`, `repository_check_inputs`, `docs_ssot_plan`,
`issue_scope_ledger`, `agent_assignment_recovery`, `repository_snapshot`, and
`invocation_freshness`.

The Skill owns repository check selection, scope qualification before severity,
complete adequacy and Docs SSOT review, current-scope findings, full-rerun
identity, the AI Review Gate, re-entry, and exactly four exits:
`passed` -> active Skill `guru-create-task-commit`,
`implementation_required` -> workflow target `guru-resume-implementation`,
`planning_stale` -> workflow target `guru-task-check-planning-router`, and
`blocked` -> stop `task-check-blocked`. The planning router consumes only the
checker-validated `reapprove_plan` or `clarify_requirements` discriminator and
maps it to one exact active Skill; it does not repeat semantic scope judgment.

Official unchanged `trellis-check` workers provide review evidence only. They
cannot own the Guru Gate, artifact, finding severity, or route. The package
publishes closed schema `guru-phase2-check-2.0`; active legacy schema 1.0
requires complete semantic re-entry, while archived artifacts remain historical.
Recorder/checker runtime commands accept AI-authored closed input and validate
only objective schema, linkage, digest, HEAD/diff/dirty, agent recovery,
full-round, and exit/consumer invariants. Legacy `--pass --coverage` calls must
fail closed rather than synthesize a semantic result.

The entry evidence collections for requirement provenance, implementation
handoff, Docs SSOT durable paths, repository reviewed paths, and executed
commands are non-empty. Every adequacy dimension has a non-empty reference to
a known current-round evidence source, the round covers planning, provenance,
handoff, Docs SSOT, repository, execution, and agent evidence, and
`current_scope` / `scope_change_required` candidates carry non-empty trigger
references. These are objective existence and reference-closure checks; AI
still owns semantic sufficiency.

The checker recomputes execution/scope/adequacy digests, every Gate binding,
finding count, and full-round digest from source fields and requires exact
equality. If an implementation handoff lists task-local
`agent-assignment.json`, a legal post-commit Branch Review metadata tail may
retain the recorded raw file digest only while the independent Phase-2-stable
agent projection remains equal; implementation/check/recovery drift fails
closed.

The objective agent projection requires task-local assignment evidence. Its
non-empty implementation/check id sets exactly equal the effective completed
events for those roles, and worker evidence covers exactly the completed check
agent set. Missing, partial, failed, unfinished, stale, or replacement-only
agent evidence fails entry before any typed exit can be recorded. The projection
digests only Phase-2-stable implementation/check agents, status/liveness,
corrections, recovery links, exact completed sets, and recovery closure. It
excludes later Branch Review role/round/reuse metadata, while the Branch Review
Gate separately validates the complete current assignment artifact and digest.

## Distribution And Managed Hashes

The preset installs an audited canonical registry/schema/package copy under
`.trellis/guru-team/skills/`, then distributes each active package to
`.agents/skills/<id>/` and only the selected platform roots:
`.codex/skills/<id>/`, `.cursor/skills/<id>/`, and
`.claude/skills/<id>/`. Unselected roots are not created.

Every distributed file uses exact previous managed hashes, never overlay
content heuristics:

| Target state | Result |
| --- | --- |
| missing | install canonical bytes and record the hash |
| equals canonical | unchanged; refresh deterministic provenance |
| differs, but equals the previous managed hash | write `.bak`, then install the new canonical bytes |
| unknown local edit | preserve target, write canonical bytes to `.new`, fail closed |
| missing or invalid provenance with different bytes | preserve target, write `.new` or fail before mutation |

The installed manifest binds registry digest/schema version, reserved and
active ids, selected platforms, package/interface/tree digests, each installed
repo-relative path, file digest, executable bit, managed removals, conflicts,
and sidecar outcome. `files[]` is the complete current managed-file inventory;
`removals[]` records previous-managed paths removed during platform shrink;
`conflicts[]` records preserved paths plus explicit remediation; and
`sidecars[]` exactly equals the `.new`/`.bak` files on disk. A manifest with an
unresolved conflict or sidecar has `status=conflict`, never `ok`. It never stores
an absolute local path.

A conflict manifest is reusable as previous managed provenance only for the
deterministic known-upgrade recovery state: `conflicts[]` is empty, every
declared sidecar is a unique repo-relative `.bak` adjacent to a current
`files[]` path, and every still-present sidecar is a regular file behind a
non-symlink path. Reapply preserves the remaining `.bak` inventory and stays
blocked; after all declared backups are removed, the next reapply may return
`status=ok`. A `.new`, semantic conflict, malformed path, unbound backup, or
non-regular sidecar never enters this recovery path and invalidates previous
provenance.

Every source, installed, platform, target, and sidecar path is lexically bound
to the repository. Before any read, write, removal, chmod, or digest, the
installer/validator walks every component with `lstat`. A regular, dangling,
internal, external, or multilevel symlink at the target or any ancestor fails
closed; no asset may be read from or written through it.

Package command files are thin wrappers. Interface 1.3 source validation binds
the invocation command to one declared validator and requires the complete
wrapper bytes to match the supported dispatcher-only template; a dispatcher
name in a comment, dead branch, or adjacent local output/behavior is not route
evidence. Accepted wrappers locate only the managed `run-skill-command`
dispatcher, pass their package root and fixed validator id, and forward the
original arguments. They must not locate an old companion
command directly, parse task/gate evidence, validate commit messages, stage Git
content, or implement transaction/rollback behavior. Missing or incompatible
runtime state fails before the target companion command and reports that the
package is not self-contained/portable, that the complete Guru Team preset must
be installed or upgraded, and that unresolved `.new` / `.bak` sidecars and
source/installed validation must be handled before retry.

## Deterministic Validation

The stable command is:

```bash
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
```

`source` binds the canonical registry/interface Draft 2020-12 schemas by exact
dialect, schema id, and contract digest, validates their closed supported
keyword grammar, then applies every accepted constraint to production and
fixture instances. Interface 1.3 contract assets use the same recursive
Draft 2020-12-compatible closed subset described above; unsupported standard
vocabulary is rejected rather than ignored. Source also validates ids, paths,
required package files, parseable package-local artifact schemas, safe existing
artifact/schema/validator/test files, strict `SKILL.md` discovery frontmatter,
workflow markers, and unique exit mappings.
Every decoded JSON value is standard, finite where numeric, and type-checked
before set, hash, path, or string operations; malformed values return
structured `failed` errors without a Python traceback. `installed` validates
manifest provenance, selected roots, installed
file/package inventory, hashes and modes, reserved absence, unexpected or
unknown platform copies, drift, and declared-versus-actual `.new`/`.bak` files.
Both modes report objective facts and fail with
non-zero status on structural errors; neither substitutes for an AI review.

## Upgrade, Test, And Safety Contract

After `trellis update`, reapply the selected marketplace workflow, reapply the
Guru Team preset, resolve every `.new`/`.bak`, and rerun source, installed, and
dogfood drift validation. Tests must cover registry/interface failures,
missing/reserved/unknown/multiple/unmapped routes, schema and provenance
failure, every managed-hash transition, platform selection, fixture discovery,
and clean throwaway update/reapply.

Public packages, fixtures, manifests, and examples must not contain active task
state, workspace journals, platform prompts, project-private data, secrets,
signed URLs, `.env` values, or machine-specific absolute paths.

## Package-Local Skill Evaluation Contract

Interface 1.3 packages may publish a behavior corpus only at
`<skill-root>/evals/evals.json`. The closed schema id is
`guru-team-skill-evals-1.0`: `schema_version=1.0`, exact `skill_name`, and a
non-empty `evals[]` whose case ids are unique stable strings. Each case owns a
prompt, expected typed exit, human-readable expected output, optional exact
input-profile reference, optional non-empty regular files below `evals/files/`,
and optional non-empty deterministic/semantic assertion groups. Unknown fields,
`null`, unsafe paths, symlinks, unknown profile/exit/assertion references, and
canonical `expectations` fail closed. Legacy `expectations[]` is accepted only
by the one-way migration adapter and never written as canonical corpus.

The eval runner discovers the Interface 1.3 public invocation and executes its
declared wrapper for every selected case. It records the actual typed exit and
validates the DTO against that exit's independent output schema. Deterministic
grading is limited to closed JSON-pointer, isolated-file, and public-invocation
trace operations. Semantic assertions can pass only through complete external
grading bound to comparison-side/case/assertion identity; human feedback is separate and cannot
override a deterministic failure. Status is exactly `passed`,
`evaluation_failed`, `execution_error`, or `unsupported`; an expected blocked,
refresh, re-entry, or stop exit is a pass when its exit/schema/assertions pass.

The stable adapter ids are `shared`, `codex`, `claude`, and `cursor`. The runner
reads the canonical corpus outside native execution. Adapters then create a
repo/package-external public-only projection containing exact `SKILL.md`,
`interface.json`, the exact public wrapper, and only the public Interface
schemas/examples needed for invocation. Native execution receives that
projection, staged files, prompt, helper, and a minimal native request; it does
not receive the canonical package root, corpus locator, adapter request, or
private runtime source. Adapters return stdout/stderr/trace/timing locators.
They consume the same corpus bytes and do not own schema, grading,
consumer projection, semantic judgment, or platform-specific corpus. Missing
native capability returns `unsupported`. Comparison accepts only a pair of
caller-resolved exact package paths, binds grading and feedback to each side
independently, and never interprets floating refs. Before either side executes,
the runner independently validates each side's closed Interface 1.3 contract,
byte-identical corpus, fixtures, and public invocation/output assets, then
creates a side-local invocation and per-exit output-schema DTO. The adapter
binds that DTO back to the exact package Interface and invokes that side's
declared wrapper, so valid versions may use different wrapper paths. Missing
outputs, fixtures, or public assets return a closed eval error/status rather
than an uncaught runtime exception. The runner then resolves one exact public
runtime target from the selected source/installed extension context. Current
and comparison adapters receive
that same locator only through their private adapter requests; neither exact
package path is used to infer runtime location.

Every adapter descriptor owns an executable package-relative wrapper and a
non-empty native command. Source/installed discovery validates the descriptor,
regular executable mode, and exact adapter identity before use. The runner
always calls that wrapper; it does not use a hidden executable environment
override as an alternate implementation. `shared.sh`, `codex.sh`, `claude.sh`,
and `cursor.sh` delegate only platform capability detection, native argv,
isolated context, output unwrapping, and trace collection to the shared adapter
runtime. The native context includes only projected Skill/public-wrapper
locators, case prompt, staged files, and helper read/invoke commands, never
canonical package/corpus locators, inline Skill bytes, private runtime source,
corpus assertions, grader policy, or the runner-private runtime target.
Wrappers reach required runtime only through the runner-owned public invocation
boundary. An explicit compatibility/test dispatcher override may select the
runner-private target, but normal execution never depends on an environment
override.

Native execution trace is the independent closed
`guru-team-skill-eval-native-trace-1.0` contract. The repo-external adapter
context supplies a trace helper instead of embedding `SKILL.md` content. The
receipt binds the minimal native request digest, projection root, and exact
Skill/wrapper content digests. A
native CLI must use that helper to read the exact Skill contract and invoke the
exact public wrapper. The helper binds read/invocation events to the adapter
request and records path/content identity, wrapper argv/return code, and
normalized stdout/stderr identity. Only a complete receipt whose wrapper stdout
matches the returned typed DTO may produce trace invariants. A valid DTO with
no verified wrapper receipt is `execution_error`, not behavior success. The
projection physically omits `evals/` and private runtime source; four-platform
negative execution proves direct reads through received package/context
locators fail at that boundary rather than relying on prompt instructions.

Every writable run result lives below an explicit absolute temporary run root
outside the repository and package. Closed evidence is diagnostic comparison
data, not public Skill I/O, a consumer handoff, gate, checkpoint, audit chain,
or release proof. Normal workflow and standalone invocation never read eval
corpus, fixtures, adapter descriptors, or runner evidence. The six Stage 0
packages change atomically through #145, and the three production packages
change atomically through the separate #146 activation unit.
