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
`schemas/skill-registry.schema.json` and has two states:

- `planned` claims a future stable consumer id only. It has no package,
  interface, invoke marker, exit marker, or platform destination and must never
  be installed. An active Skill may declare a typed exit to that id; callers
  stop at the missing-Skill gate until a later delivery promotes it to a
  complete active package.
- `active` declares a package path, interface path, supported platform targets,
  validator command, and workflow route identity. Every referenced file and
  route must pass source validation before installation.

Activating, renaming, or retiring an id is a public API change. A breaking
current-contract delivery must use an explicit new schema/interface identity;
retired inputs fail closed and do not remain as registry rows or executors.
Production registries must never contain test fixtures.

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

`interface.json` is validated by `schemas/skill-interface-1.3.schema.json` and
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

### 0. Current Interface And Registry Contract

Issue #180 activated the historical fifteen-package/57-exit graph. The current
Registry 1.4 graph contains sixteen active packages and 62 package exits while
retaining older Interface/Registry assets as immutable legacy contracts.
`guru-merge-task-pr` is a current semantic package with exactly
`merged`, `merge_blocked`, and `closure_mismatch`. Current Finalizer exposes
`ready_for_merge` in place of `published`; the old published schema/example
remain immutable legacy assets but are not selected by the Interface, registry,
workflow or extension manifest. The integrated business graph has 15 invoke
markers, 60 exit markers and 36 unique workflow/stop targets.

The Finalizer-to-Merge edge is target-authored. Finalizer returns canonical
repository/PR identity, `expected_head_sha`, expected base/head branch identity,
and the reviewed close-Issue number set; Merge supplies only its fixed
`profile=ready_for_merge` and `mode=workflow`. These are the minimal facts the
consumer cannot rederive from live PR state without turning that mutable state
into authority. No transaction, review narrative, authorization, task runtime or
local checkout identity crosses the edge. Merge standalone/re-entry accepts the
same expected authority from its caller and rebuilds live evidence without an
active task.

The Merge AI owns readiness, close scope, policy/method sufficiency, the exact
displayed action and the dialogue-local confirmation. Its deterministic
commands own repo-bound fact capture, gate checking, expected-head merge and
post-merge read-only validation. A terminal projection retires the merge gate.
Neither Finalizer nor Merge calls Issue-close APIs, enters Phase 0, invokes base
sync, updates the PR branch, synchronizes local `main`, or cleans resources.

Fifteen integrated packages select Interface 1.4.
`guru-verify-extension-installation` selects Interface 1.5 and
`workflow_integration_state=standalone_only`. Registry schema
`guru-team-skill-registry-1.4` is the exact current selector; planned rows remain
lifecycle-only and carry no package or I/O fields. Any other row or schema
identity fails closed.

The validator selects the interface schema from the registry row. It must not
guess from optional fields, file presence, package content, or extension
defaults. The extension publishes one `interface_schema_id`, the registry id,
and exact public-input, typed-output, and private-artifact schema inventories
for all sixteen active packages and their 62 external exits. The
`production-current-v2` manifest remains exactly three packages and 11 exits;
additive activation of later packages, including `guru-finalize-task`, does not
rewrite that membership.

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
normally uses `contract.kind=skill_input`. The five production semantic edges
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

Every current Interface 1.4 scalar argument explicitly declares boolean `required`.
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

A producer-owned checkpoint has one local lifecycle consumer: that same Skill's
public wrapper. The wrapper runs the objective checker, builds and validates the
selected typed output, then deletes its own checkpoint and any empty owner
directory. A failed checker or invalid output may retain it only for genuine
same-owner active-task repair. Pre-task and standalone calls remain repository
side-effect-free and transport owner results through stdin/stdout. The next
Skill consumes only the DTO and live facts; it must never read, interpret, or
delete the producer's private checkpoint. Stale recovery deletes the current
checkpoint and reruns from live authority instead of creating a replacement
chain. Finalization follows the same rule but may retain its own checkpoint
across same-plan recovery until a terminal output validates.

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
- downstream Skill reads or deletes a producer-private checkpoint -> move
  objective checking and retirement into the producer wrapper, then pass only a
  schema-validated minimal DTO;
- required freshness cannot be proved from the minimal handoff -> add the
  narrowest stable identity/token and its consumer validation, not a full
  snapshot;
- an existing public field must change incompatibly -> publish a new schema/id
  or an explicit migration contract.

For a closed public schema (`additionalProperties=false`), adding a required
field is incompatible even when producer and consumer change in one repository
commit. The published path, `$id`, and bytes remain as a legacy validation
asset. The current contract uses a new versioned path and `$id`; any aggregate
schema whose relative reference would otherwise change meaning also receives a
new version. The Interface selects only the new current contracts while keeping
the legacy assets in its package schema inventory. Package tests must validate
both generations, reject cross-version substitution, and execute the current
projection against the target-owned current input. A legacy route must either
have an explicit deterministic migration whose missing values come from an
owned authoritative input, or fail closed and rerun the current producer; it
must never synthesize a required identity from a neighboring field or live
ambient state.

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

### 8. Interface 1.3 Legacy Foundation And Interface 1.4 Current Contracts

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
  `stdout_only_pre_task`, `task_local_tracked`,
  `task_local_archive_transaction`, or `ignored_runtime` persistence.
  `task_local_archive_transaction` means the checkpoint is untracked while the
  task is active and becomes tracked only through the predeclared single archive
  transaction; it must never cause a standalone evidence or metadata commit.

Interface 1.4 retains those closed public sections and adds the versioned
call-local invocation contract selected by the current activation. The legacy
1.3 schema and examples remain byte-stable but are not selected by the current
registry, extension inventory, production manifest, or installed package graph.

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
length/uniqueness/items/contains, and object properties/required/non-negative
`minProperties`/boolean-or-object-schema `additionalProperties`. Nested `$id`
resource boundaries, boolean schema nodes,
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

Discovery resolves the exact active registry row first and requires Interface
1.3. It returns one closed index locating input, invocation, every exit output,
consumer contract, projection, examples, and private artifacts. Discovery
returns metadata only and does not execute the semantic Skill. Any other
registry/interface identity fails closed rather than selecting another variant.

Unknown skill, version/state mismatch, missing/unsafe contract path, invalid
schema/example, or installed drift exits non-zero with stable `code`,
repo-relative `field_path`, and actionable `remediation`. Callers need only
`SKILL.md`, `interface.json`, package-local public assets, and command help;
they never import or read `guru_team_trellis.py`.

Source validation executes the declared representative 1.4 example invocation,
requires exactly one declared typed-exit object on stdout, and validates it
with that exit's independent schema. The current-only test fixture contains one
structured semantic 1.4 package and one scalar CLI deterministic 1.4 package.
It covers Skill/workflow/stop consumers,
self-reentry, the closed projection operations, stdout-only and task-local
private state, distinct exits, and stable errors, but never enters production
registry, extension inventories, workflow routes, or installed platform roots.

### Current Intake Production Activation

The live registry and current Interface 1.4 packages contain exactly these
Intake packages and exits:

- `guru-sync-base`: `synced`, `skipped`, `blocked`;
- `guru-discover-change-context`: `context_ready`, `refresh_base`, `blocked`;
- `guru-clarify-requirements`: `clear`, `needs_context`, `refresh_context`,
  `retarget_context`, `new_task`, `blocked`;
- `guru-review-contract-wording`: `pass`, `content_changed`, `blocked`;
- `guru-review-change-request`: `ready`, `clarify_requirements`,
  `review_wording`, `refresh_context`, `blocked`;
- `guru-create-task-workspace`: `created`, `refresh_review`, `blocked`.

All six packages select `guru-team-skill-interface-1.4`. The current
six-package/23-exit contract is derived only from the live registry, current
Interface 1.4 packages, workflow markers, extension inventories, and selected
platform copies. User refusal stops before recorder/executor and emits no DTO,
while optional `guru-sync-base` scalar arguments are derived by the runtime
when omitted. A partially updated current Intake graph is invalid even when
each package validates in isolation. Validation and installation consume exactly
the live registry and current package graph.

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
`ignored_runtime` persistence. A finalizer transaction checkpoint may instead
declare `task_local_archive_transaction` under the lifecycle above. Re-entry
passes only caller-owned continuation and task-relative locators; the owner
runtime rereads live facts, validates the current artifact with its published
schema, and emits a current 1.3 DTO without rewriting archived bytes.

The five semantic public wrappers run only after their Agent-owned semantic
loop and recorder/checker stage. Their invocation accepts the closed
caller-owned public input, the workflow-owned current transition, and the
current Skill's owner result through a versioned call-local invocation
envelope. Runtime reruns the existing objective checker and derives the exit
only from the checker-passed owner result. A caller-selected expected exit,
public output example, or private artifact body is never a production routing
input.

The Phase 0 transition family has five independent closed stages:
`base_current`, `context_current`, `clarity_current`, `wording_current`, and
`readiness_current`. Each stage is owned by workflow orchestration, contains
only the identity/freshness projection required by its one next consumer, and
is replaced rather than extended when refresh/re-entry invalidates it. A stage
is not a producer checkpoint, audit artifact, semantic result, or optional-field
aggregate. Unknown, missing, multiple, stale, cross-stage, or unmapped state
fails closed.

`base_current` preserves resolution source, selected base, remote, ordered
candidates, decision HEAD, local base HEAD, remote base HEAD, and post-sync
digest as distinct consumer-bound fields. The three HEAD roles must not collapse
into a generic `base_head`. The formal closed schema/runtime state matrix owns
whether a missing remote ref is legal for a diagnostic state; a caller never
synthesizes a nullable fallback.

The call-local transport uses distinct closed envelopes for deterministic sync,
semantic invocation, and confirmed workspace mutation. Its public stdin form is
exactly `--invocation -`; it cannot be combined with locator transport flags.
A semantic envelope
separates `public_input`, `transition`, and `owner_result`; the owner result
belongs only to the currently invoked Skill and is never projected downstream.
The initial sync has no upstream transition, and workspace plan/result transport
does not persist confirmation. Normal pre-task execution carries envelopes and
transitions through stdin/stdout or caller memory and creates no owner-result,
prerequisite, transition, task, workspace, or `.trellis/.runtime/**` repository
file. It also never imports the shared runtime source to reconstruct an input.

Legacy `--input <path>` or `--owner-* <path>` forms may remain only when a
documented compatibility consumer still exists. They are excluded from the
workflow happy path, production evals, and clean-install transcript; their
owner, short lifecycle, and removal condition must be explicit. They cannot be
used to satisfy a missing current transition or to preserve authorization.

Any previously published closed Phase 0 input/output schema and example keeps
its original path, `$id`, and bytes. Adding transition or provenance fields uses
a new versioned path/identity, and the current Interface selects only that new
contract while inventory retains the immutable legacy assets required by the
compatibility contract. A legacy DTO that cannot establish the current stage or
source-preserving provenance fails closed and reruns its current producer; it
must not default missing fields or derive them from ambient live state.

For `guru-clarify-requirements:clear`, a checker-passed
`active_task_scope_change` result may legitimately carry
`target_disposition=null` when the accepted action updates only the active task
scope. That one fixed profile projects to public `retained`; null disposition in
initial or standalone profiles remains an invalid owner projection.

### Production Planning, Check, And Commit Activation

`trellis/skills/guru-team/contracts/production-current-2.0.json` with contract id
`production-current-v2` is the sole current planning/check/commit manifest. It
extends the live six-Skill/23-exit Intake contract. The production contract
contains exactly:

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

The public DTOs are exact. Planning emits `approved(exit_id, task_ref)`,
`revision_required(exit_id, task_ref)`,
`clarify_scope(exit_id, task_ref, proposal_refs)`, or blocked `exit_id` only.
Check emits `passed(exit_id, task_ref, phase2_commit_anchor)`,
`implementation_required(exit_id, task_ref, finding_refs)`,
`planning_stale(exit_id, task_ref, planning_route, proposal_refs)`, or blocked
`exit_id` only. Commit emits `committed(exit_id, task_ref, base_ref,
branch_review_commit)`, `revision-required(exit_id, task_ref)`, or blocked
`exit_id` only. Active `guru-review-branch` consumes exactly `task_ref`,
`base_ref`, and `branch_review_commit`; the caller authors only `profile`, `mode`, and
`review_intent` for the selected aggregate schema 3.0 profile. Branch Review
emits `passed(exit_id, task_ref, branch_review_commit)`,
`continuity_passed(exit_id, task_ref, branch_review_commit, task_head,
old_base_head, new_base_head, candidate_tree_sha256, resume_target)`,
`implementation_required(exit_id, task_ref, branch_review_commit, finding_refs)`,
`scope_confirmation_required(exit_id, task_ref, proposal_refs)`, or blocked
`exit_id` only.

Planning and check wrappers materialize their existing owner input,
invoke the existing recorder/checker pair, and project only the checker-passed
actual exit. The commit public input contains only profile/mode/task/source-exit/
`phase2_commit_anchor`. Target-owned AI authoring supplies path classifications,
structured message fields, and the semantic result to a deterministic private
candidate builder, which combines them with the passed Phase 2 DTO and live
task, ledger, Git, snapshot, and sequence facts. It canonicalizes and validates
the complete candidate before dialogue-local commit confirmation; neither the
candidate nor any persisted state records user authorization. The checked
executor consumes only that private candidate.
Caller-selected `expected_exit`, artifact bodies, digests, file metadata,
absolute paths, and runtime snapshots are not public input.

Exactly nine semantic handoffs use target-owned authoring seeds. The first
five are
`guru-approve-task-plan:revision_required -> revision_reentry`,
`guru-check-task:passed -> guru-create-task-commit:initial_commit`, and
`guru-create-task-commit:revision-required -> revision_reentry`, and
`guru-create-task-commit:committed -> guru-review-branch:branch_review`, and
`guru-review-branch:passed -> guru-review-task-publication:publication_review`.
The finalization family adds
`guru-review-task-publication:ready -> guru-finalize-task:publication_ready`,
and the finalizer's `publication_review_stale`, `same_plan_resume`, and
`reprepare_preview` targets. Their projected seed fields are respectively `source_exit/task_ref`,
`source_exit/task_ref/phase2_commit_anchor`, `source_exit/task_ref`,
`task_ref/base_ref/branch_review_commit`, and
`task_ref/branch_review_commit`. Publication `ready` seeds Finalizer with
`task_ref/branch_review_commit/pr_title/pr_body`; every other finalization-family seed
is the minimal field set declared by its target profile, with reprepare fixed to
`task_ref/reason_code/branch_review_commit/publication_head`. Target package
authoring examples supply every remaining
required fresh semantic field. The validator proves disjoint partition,
required-set equality, no-overwrite merge, and full target-schema validity;
all other Skill/workflow/stop consumers keep their existing contracts.

Active closure is derived from the live registry, the production current
manifest, and every complete active Interface 1.4 row. Every
active profile and exit must have
a current canonical case binding and byte-identical selected-platform corpus.
The current package cardinality assertion is sixteen active Skills and 62
exits. The integrated business workflow projection contains 15 invoke markers,
60 exit markers, and 36 target markers. Missing,
extra, duplicate, renamed, unknown, partially activated, or
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
validation. Planned ids may appear only as a Skill consumer; a planned invoke
or exit marker is invalid.
Frontmatter auto-match is discovery assistance only and never replaces
mandatory invocation markers.

`guru-select-workflow-mode` is the semantic owner before normal Intake. Its
owner-private result binds `mode` and `continuation_id`; selected results carry
exactly one matching `selection`, while `blocked` carries no invented mode.
The public DTO contains only `exit_id`. The semantic corpus covers explicit
intent, automatic/one-question/standard selection, simple/insufficient/complex
Issue evidence, equal file-count with different risk, checkout suitability,
same-scope reuse, automatic and explicit risk expansion, and
selection-unavailable blocking. Wrapper regressions independently reject
missing, unknown, multiple, unmapped, or stale-continuation owner results and
missing package/marker state.

`guru-approve-task-plan` is the only semantic owner of Phase 1 planning
approval. Its interface uses `judgment_mode=semantic`, declares the same eight
ordered entry preconditions in workflow and standalone modes
(`runtime_dependency`, `task_workspace`, `current_authority`,
`planning_documents`, `docs_ssot`, `wording_result`, `issue_scope`, and
`invocation_freshness`), and owns the package-local runtime commands
`record-planning-approval` and `check-planning-approval`.

The owner directly rereads live authority and current files, reviews requirement
authority, scope boundary, design adequacy, implementation plan, acceptance
verifiability, Docs SSOT, provenance, and supported unusual scenarios, and
classifies semantic versus equivalent deltas. A necessary task-activation or
scope-choice authorization occurs only in the current conversation. No
authorization value, wording, timestamp, digest, or reference enters the
public input, private checkpoint, archive, or output.

New private evidence uses `guru-planning-approval-3.0` under ignored runtime.
It stores only mode, task/planning locators, authority refs, compact Docs SSOT,
one composite planning-content freshness token, the final semantic result,
typed exit, reason, and consumer. The token serves only the local checker before
activation and Phase 2 recording; a mismatch returns to the owner for AI delta
classification. It is not authorization, semantic approval, public handoff, or
whole-chain authority. The checkpoint contains no repository snapshot, file
metadata, per-file or artifact digest bundle, provenance transcript, review
report, assignment, liveness, or confirmation chain. The public input
only selects `initial_review`, `revision_reentry`, or
`clarification_reentry`; callers never preselect findings or an exit.

The four external exits and unique consumers are:

- `approved` -> workflow target `phase-1-task-activation`;
- `revision_required` -> Skill `guru-approve-task-plan`;
- `clarify_scope` -> workflow target `guru-task-plan-clarify-scope-router`;
- `blocked` -> stop `task-plan-approval-blocked`.

`revision_required` restarts after task-local planning changes and a fresh
wording review. `clarify_scope` delegates through the three-field routing-only
workflow target, which establishes scope context and mandatory invokes
`guru-clarify-requirements:active_task_scope_change`; the caller AI authors the
complete clarification input from fresh live context before all eight planning
entry checks restart. Unknown, duplicate, multiple, unmapped, or
consumer-mismatched exits fail closed. The package uses current-only closed
schema `guru-planning-approval-3.0`; any other shape fails schema validation and
requires a complete current semantic review.

`guru-create-task-commit` is mandatory after a fresh final Phase 2 pass and
before every task work stage/commit side effect. It exposes only `committed`,
`revision-required`, and `blocked`: Branch Review/finding closure consumes the
first, the skill re-enters on the second, and the workflow stops on the third.
Finding-fix task work returns through implementation and full Phase 2 before a
new plan sequence may invoke the skill again. Workflow and standalone entry
preconditions include ordinary Git operation state. Gitlink snapshot identity
is conditional on index mode `160000` and binds an initialized, clean worktree
HEAD; for non-deleted gitlinks that artifact HEAD is also the exact index OID,
not a hint for `git add` to reread from the worktree. Current snapshot
producers distinguish rename and copy with mutually exclusive `renamed_from`
and `copied_from`. Only a rename source inherits destination deletion/exact-
stage authority; copy provenance never stages its source, and a dirty copy
source requires an independent classification. Current schema 3.0
SHA-256/mode/delete/rename facts are the only exact-index authority.
The validated in-memory plan is the only candidate-self byte authority. Executor
staging and hooks run on an isolated index/detached transaction HEAD; parent,
message, path set, complete tree, candidate, worktree, operation state, branch
ref, and live index preimage are checked before publication. Standard
`git update-ref <ref> <new> <old>` conditionally advances the branch and `git
reset --mixed --quiet HEAD` refreshes the live index. The executor owns no
custom lock, atomic-replace, rollback, concurrency, or linearization protocol.
Failure before the conditional ref update leaves the live ref/index untouched;
failure after a successful ref advance reports the created commit for bounded
same-plan recovery. On success Git remains the source of commit facts and the
ignored candidate is removed.

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
equality without mutation, then returns the post-sync digest. The public wrapper
projects the checked source, selected base, remote, ordered candidates,
decision/local/remote HEADs, and post-sync digest into `base_current`.
Compatibility-only `prepare-task` requires that complete reviewed provenance,
not only its digest; missing provenance blocks locally before GitHub read or
fetch. It has no mutation guard and never produces a workflow transition;
active workspace mutation freshness belongs to `guru-create-task-workspace`.

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
repository identity, direct active task locator/status, and the current task
worktree's ordinary in-progress dirty paths. Active-task invocation identity is
supplied ephemerally and does not itself create a checkpoint; only an explicit
recovery continuation enables lazy same-owner checkpoint persistence. A proposed draft
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

The package publishes stdout-only owner-result schema
`guru-change-context-owner-result-2.0`, scoring algorithm id
`guru-context-history-score-1.0`, and dispatcher-only wrappers for
`preview-change-context-history`, `record-context-discovery`, and
`check-context-discovery`. The history command may enumerate only
`.trellis/tasks/archive/**/finish-summary.json` and project only top-level
`index`; it never reads index siblings, workspace/runtime state, or a repo-level
archive index/cache. Scripts validate AI-authored selection and Gate evidence
but do not select candidates, judge sufficiency, decide duplicate reuse, or
synthesize semantic pass.

Recorder/checker accept the current AI-authored result through stdin or one
explicit file, compare it with current live facts, and return canonical/checked
JSON on stdout. They do not resolve, write, replace, or supersede a task
artifact. Normal active-task record/check/invoke accepts one ephemeral direct
task identity, binds its live task branch, and permits ordinary current-worktree
edits without creating a checkpoint. Only an explicit recovery continuation
creates/checks the one lazy same-owner checkpoint. The public wrapper supports
stdin owner transport, validates the selected minimal DTO, and retires that
checkpoint after successful consumption. Clarification, readiness, and workspace creation
do not receive an owner-result locator and do not read Discovery private
evidence. `refresh_base` reruns the owner from live authority without a prior
result chain.

`guru-clarify-requirements` is an active semantic package with identical
workflow/standalone preconditions: current runtime, current review target,
current context evidence, source authority, and invocation-context freshness.
Its Interface 1.4 semantic stages are `forward_behavior -> ai_review_gate ->
conditional_human_confirmation -> recorder_validator -> typed_exit`. The Skill
loads `trellis-brainstorm` as its one-question method, but owns question
selection, convergence, scope classification, action selection, confirmation
necessity, semantic pass/block, and typed route.

The result uses closed top-level fields and active artifact schema
`guru-requirements-clarification-2.0`. Repository-answerable questions must be
`answered` or `not_answerable` with at least one checked evidence reference
before the first user
question. Each clarification round contains one `question_id`; an
`atomic_group` is permitted only for an indivisible product choice and records
its reason. Every round's `question_id` must be opened in that round or already
open; `answer_status=partial` cannot close any question and therefore cannot
disappear through an empty lifecycle. The reducer keeps exactly
`open_questions = opened - closed`, rejects closing-before-open and reopening
after closure. The recorder derives all proposal, action, payload, content, and
result digests as local deterministic identities for this recorder/checker pair; the checker
recomputes them and validates current live/task facts without generating
questions, choosing actions, classifying scope, executing GitHub writes, or
turning deterministic success into a semantic pass.

Source actions are `none`, `issue_comment`, `issue_body_edit`,
`proposed_draft_update`, `new_issue_draft`, `select_existing_issue`,
`reopen_issue`, and `active_task_scope_update`. GitHub mutation remains
AI-owned: after the required current-dialogue choice, the AI uses only
authenticated, explicit repo-bound `gh` / `gh api`, rereads live facts, and
supplies only objective mutation evidence to the recorder. GitHub App, MCP,
connector, browser UI, and implicit repository context are forbidden fallback
channels. Checker binds the action payload,
canonical payload digest, mutation result content digest, and reread live body/comment;
any byte mismatch fails closed. Generic continuation, task creation, planning approval, or
review confirmation cannot replace a real scope or side-effect choice.
`unconfirmed_expansion + accepted_current` requires that dialogue choice, but
no result, checkpoint, artifact, or DTO records authorization. A proposal with
`optional_mechanism_origin=true` cannot be `accepted_current`; the mechanism is
removed/replaced or its independent product value is proposed separately.
For an active task, `unconfirmed_expansion` classified as `related`,
`followup`, `new_task`, or `out_of_scope` also requires the real dialogue
decision when the classification is not already explicit.

The six exits and unique consumers are `clear` -> workflow target
`guru-requirements-clear-router`, `needs_context` -> Skill
`guru-discover-change-context`, `refresh_context` -> Skill `guru-sync-base`,
`retarget_context` -> Skill `guru-sync-base`, `new_task` -> workflow target
`guru-full-task-intake-chain`, and `blocked` -> stop
`requirements-clarification-blocked`. Active-task `clear`/`new_task`
requires a non-empty terminal proposal set. `clear` requires no open questions,
a passed current AI Gate, current authority/context, every five-class scope
classification finalized, mechanism dispositions kept outside the trail,
and no unrefreshed mutation. A successful GitHub mutation
returns `refresh_context`; a reviewed side-effect-free new issue draft returns
`new_task`; an exactly selected open duplicate returns `retarget_context` and
reruns the complete initial chain; `blocked` is valid if and only if the AI Gate
is blocked.

Pre-task and standalone results remain stdout-only. There is no dedicated
tracked clarification artifact. Every five-class active-task classification binds a
compact owner-result `decision_trail`. It contains only `trail_id`, exact
proposal id/digest/decision rows, and live GitHub comment/body authority kind,
URL, and content checksum. It contains no
user identity, confirmation reference, authorization state/digest, authority
timestamp, planning identity, review state, context snapshot, interrupted
target, or re-entry route. The active-task checker independently rereads
the closed scope-only Ledger 2.0, current planning, context, task-update
preimage, re-entry facts, and live authority time from their owners. The trail
stays in the transient owner result and is never written to the Ledger. Inputs
outside the current closed schema fail before normalization. GitHub authority
mutation returns `refresh_context`; only a context
snapshot generated at or after authority `updated_at`, followed by a task update
bound to that snapshot, may later return active-task `clear` or `new_task`.
The AI resolves any real scope choice only in the current dialogue; the result
and compact classification never stores that authorization process. Task-only
update requires no second refresh. `mechanism_removed/replaced` remains outside
the compact classification and action mutation. `new_task` still contains only the
side-effect-free reviewed draft and #112 owns creation. A copied package without
the complete current preset remains non-portable and fails closed through
the dispatcher.

`invocation_context.resume_target` is caller-aware and closed. Initial
issue/draft accepts only `guru-review-contract-wording`; standalone accepts only
`guru-standalone-caller`; active-task accepts the planning-review target or one
of the declared interrupted Phase 1/2/3/Branch Review targets. Accepted-current
scope requires the planning-review target.

`guru-review-contract-wording` is the active semantic owner for controlled
contract wording review. Workflow and standalone modes use the same runtime,
fixed profile scope, semantic-evidence, and freshness preconditions. The exact
semantic stages remain `forward_behavior -> ai_review_gate ->
conditional_human_confirmation -> recorder_validator -> typed_exit`, but any
necessary authorization stays in the current dialogue and is never a result
field, digest, reference, or persisted checkpoint.

The package owns vocabulary `contract-wording-v2`, classification contract
`contract-wording-classifications-v1`, the rewrite/classification/review loop,
the three closed profiles, schema `guru-contract-wording-review-1.0`, and exits
`pass`, `content_changed`, and `blocked`. `change_request` binds current
title/body plus any AI-selected authoritative comments; `planning_artifacts`
binds the active task's `prd.md`, `design.md`, and `implement.md` and requires
the exact seven-key `planning_checked_dimensions` result; `explicit_paths`
accepts only a standalone caller's explicit repo-relative Markdown files.
Every profile emits stdout-only owner-private evidence. No profile writes
task-local `contract-wording-review.json`.

The deterministic runtime publishes `record-contract-wording-review` and
`check-contract-wording-review`. It builds fixed scope facts, scans current
content, derives local identities and unchecked hits, and validates schema,
classification/reason shape, rescan binding, Gate/exit invariants, and the
planning-dimension shape/value. It never chooses scope, rewrite,
classification, reason sufficiency, semantic pass/block, confirmation need, or
route intent, and it never invents a planning semantic result.

Stale stdout evidence is discarded. The owner rebuilds current scope and scan,
reruns the complete semantic loop, and emits one current result. There is no
`--replace-stale`, supersession flag, prior-result digest chain, or task-local
replacement history. For a live issue revision, the runtime validates only the
objective preimage, exact proposed bytes, current reread bytes, source identity,
and update time needed by that mutation consumer; it never records or validates
user authorization.

Unique consumers are `pass` -> workflow target
`guru-contract-wording-pass-router`, `content_changed` -> workflow target
`guru-contract-wording-change-router`, and `blocked` -> stop
`contract-wording-blocked`. Those routers use only the checker-validated
profile and exit. Unknown, multiple, stale, or unmapped profile/exit evidence
fails closed. Planning approval consumes only the current checked
`planning_artifacts:pass` exit and cannot become a second vocabulary,
classification, scanner, or semantic-review owner. It rereads the three current
planning files and does not import scanner hits, classification history, file
digests, or the wording owner's private result. Inputs outside the current
Interface 1.4 contracts fail closed; only the checked current invocation output
may be consumed.

## Change Request Readiness Package

Active semantic Skill `guru-review-change-request` is the sole pre-task
readiness owner after `guru-review-contract-wording:change_request:pass`. It
consumes current context, clarification, and wording results; normalizes one
`existing_issue`, `proposed_draft`, or `standalone_request`; reviews the fixed
ten dimensions; records findings, scope conclusion, AI Review Gate, and exactly
one exit. Any real choice or side-effect authorization remains dialogue-local
and is never part of this result. Its exits are `ready` -> active
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
workspace. `ready` invokes only `guru-create-task-workspace`.

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
ignored-runtime `guru-task-workspace-plan-2.0` and
`guru-task-workspace-result-2.0`. Recorder,
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
the branch/worktree/task, one tracked task-local Issue Scope Ledger, ignored
runtime mappings, and workspace boundary all pass objective validation.
Refusal stops before the recorder/executor and produces no plan, result, or DTO.
The non-mutation matrix is `reroute` -> `refresh_review` and `blocked` ->
`blocked`; runtime preserves these AI-authored facts and may mutate only for a
passed Gate plus current confirmation.

An open-issue plan that continues a workflow-created draft embeds the complete
prior checker-passed `created_issue` result and its binding digest. The result
facts digest, binding facts digest, reviewed draft id/digest, creation
identity, current issue authority, and complete Intake rerun's live existing-
issue identity must all agree. No confirmation digest or authorization field is
accepted. The fresh context is `kind=issue` with
canonical URL/open state/update time/body/facts identity and null
`issue_binding`. Ordinary existing issues carry null result and binding fields;
missing, partial, or mixed provenance fails closed.

The plan also binds the checker-passed base result's
`post_sync_resolution_sha256`. Before the first GitHub issue or workspace/task
mutation, the executor reconstructs the reviewed resolution, revalidates its
local decision/base/remote-tracking facts, and uses read-only
`git ls-remote --heads` to compare the current remote base HEAD. This guard must
not fetch, fast-forward, or update any local ref. A normal remote advance
returns `refresh_review` with decision HEAD, local base, remote-tracking ref,
issue, branch, worktree, task, artifact, and runtime state all unchanged; the
next complete Intake round re-enters the sole authoritative
`guru-sync-base` public invocation.

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
`guru-sync-base`, and `blocked` to stop `task-workspace-blocked`. A target/disposition change is
`refresh_review` with zero writes. Unknown, multiple, unmapped, stale, or
consumer-mismatched exits fail closed.
Public plan/result stdout and examples contain no absolute workspace path; the
checker derives the expected worktree from current repo config, reviewed slug,
and live Git facts. Absolute mappings stay only in ignored runtime files.

## Phase 2 Task Check Package

`guru-check-task` is the only semantic owner of the complete Phase 2 task
check and of the single ignored-runtime `phase2-check.json` checkpoint. It declares
`judgment_mode=semantic`, the exact five-stage semantic profile, and identical
workflow/standalone preconditions in this order: `runtime_dependency`,
`task_workspace`, `approved_planning`, `live_implementation`,
`validation_scope`, `docs_ssot`, `issue_scope`, and `invocation_freshness`.

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
publishes current-only schema `guru-phase2-check-4.0`. Recorder/checker runtime
commands accept AI-authored closed input and validate only objective schema,
`phase2_capture_commit` ancestry, recomputed
`guru-reviewed-content-1.0` identity, current dirty reviewed-path coverage,
finding/scope linkage, and exit/consumer invariants. Any non-current input or
checkpoint shape fails closed rather than synthesizing a semantic result.

Reviewed paths and validation evidence are non-empty. Every adequacy dimension
has current evidence from planning, implementation, Docs SSOT, repository,
tests, and issue scope. These are direct semantic inputs; AI still owns
sufficiency, qualification, findings, and route.

Candidate hygiene treats exact bytes at an exact repo-relative path as upstream
Trellis template-managed only when that path has a valid matching SHA-256 entry
in schema-v2 `.trellis/.template-hashes.json`. The `HEAD`, index, and worktree
projections are matched independently, and each match suppresses only that
projection's Git diff-check or untracked-text trailing-whitespace and blank-EOF
findings, including tracked upstream-template migration deltas. Missing/invalid
provenance, unknown paths, local edits, or hash mismatch remain ordinary
candidates, while path, UTF-8, and JSON validation is never bypassed.

The ignored-runtime schema 4.0 checkpoint contains only
`phase2_capture_commit`, `reviewed_content_sha256`, reviewed paths, validation
evidence, final Docs SSOT result, semantic dimensions/findings, and typed route.
The content identity serves only the local checker before Task Commit; a
mismatch returns to the owner for AI delta classification. Metadata-only
HEAD/status changes do not change the identity. It is not authorization,
semantic approval, public handoff, or whole-chain authority.
Routine assignment, handoff, liveness, raw worker payload, recovery transcript,
review rounds, repository snapshots, per-file or artifact digest bundles, and
`implementation_handoff` are absent. The checker rereads live entry facts and
validates this compact result without creating another artifact.

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

The installed manifest binds registry digest/schema version, planned and
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

Package command files are thin wrappers. Interface 1.4 source validation binds
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
fixture instances. Interface 1.4 contract assets use the same recursive
Draft 2020-12-compatible closed subset described above; unsupported standard
vocabulary is rejected rather than ignored. Source also validates ids, paths,
required package files, parseable package-local artifact schemas, safe existing
artifact/schema/validator/test files, strict `SKILL.md` discovery frontmatter,
workflow markers, and unique exit mappings.
Every decoded JSON value is standard, finite where numeric, and type-checked
before set, hash, path, or string operations; malformed values return
structured `failed` errors without a Python traceback. `installed` validates
manifest provenance, selected roots, installed
file/package inventory, hashes and modes, planned absence, unexpected or
unknown platform copies, drift, and declared-versus-actual `.new`/`.bak` files.
Both modes report objective facts and fail with
non-zero status on structural errors; neither substitutes for an AI review.

## Upgrade, Test, And Safety Contract

After `trellis update`, reapply the selected marketplace workflow, reapply the
Guru Team preset, resolve every `.new`/`.bak`, and rerun source, installed, and
dogfood drift validation. Tests must cover registry/interface failures,
missing/planned/unknown/multiple/unmapped routes, schema and provenance
failure, every managed-hash transition, platform selection, fixture discovery,
and clean throwaway update/reapply.

Public packages, fixtures, manifests, and examples must not contain active task
state, workspace journals, platform prompts, project-private data, secrets,
signed URLs, `.env` values, or machine-specific absolute paths.

## Package-Local Skill Evaluation Contract

Interface 1.4 packages may publish a behavior corpus only at
`<skill-root>/evals/evals.json`. The closed schema id is
`guru-team-skill-evals-1.0`: `schema_version=1.0`, exact `skill_name`, and a
non-empty `evals[]` whose case ids are unique stable strings. Each case owns a
prompt, expected typed exit, human-readable expected output, optional exact
input-profile reference, optional non-empty regular files below `evals/files/`,
and optional non-empty deterministic/semantic assertion groups. Unknown fields,
including `expectations`, `null`, unsafe paths, symlinks, and unknown
profile/exit/assertion references fail closed. Adapters accept only this current
corpus shape and never translate or rewrite another input contract.

The eval runner discovers the Interface 1.4 public invocation and executes its
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
the runner independently validates each side's closed Interface 1.4 contract,
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
boundary. An explicit test dispatcher override may select the
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
corpus, fixtures, adapter descriptors, or runner evidence. The six Intake
packages and the three planning/check/commit packages are each validated as a
complete current activation unit.

## Branch Review Owner And Active Publication Bridge

`guru-review-branch` is the semantic owner of the post-commit full-range review
and bounded base-continuity review. Aggregate public input schema 3.0 dispatches
two profiles. The `branch_review` schema 2.0 profile requires exactly `profile`,
`mode`, `task_ref`, `base_ref`, `branch_review_commit`, and `review_intent`; the
committed producer supplies the three identity fields and the caller AI freshly
authors `profile`, `mode`, and `review_intent`. The `base_continuity` schema 1.0
profile consumes the exact old/new base candidate and unchanged task review
from `guru-reconcile-task-base:review_continuity_required`. Neither profile
reopens the Phase 2 private checkpoint. Current issue scope, findings, range,
candidate identity, and freshness remain owner-private evidence. The
current-only compact gate schema 4.0 is ignored runtime state and stores
profile-specific identity plus `review_commit` and
`reviewed_content_sha256`. Aggregate input schema 2.0 and gate schema 3.0 remain
legacy compatibility inventory, not current runtime authority; any other
current shape fails closed.

The five outputs are independent minimal DTOs:

- `passed`: `exit_id`, `task_ref`, `branch_review_commit`;
- `continuity_passed`: `exit_id`, `task_ref`, `branch_review_commit`,
  `task_head`, `old_base_head`, `new_base_head`, `candidate_tree_sha256`, and
  `resume_target`;
- `implementation_required`: `exit_id`, `task_ref`, `branch_review_commit`,
  `finding_refs`;
- `scope_confirmation_required`: `exit_id`, `task_ref`, `proposal_refs`;
- `blocked`: `exit_id`.

The Branch Review `passed` edge supplies only
`task_ref/branch_review_commit` through `skill_input_authoring_seed`; the
caller authors `profile/mode/review_intent` for active
`guru-review-task-publication`. The commit remains the Git range/ancestry anchor;
the shared reviewed-content identity remains fresh across excluded workflow
metadata changes and becomes stale for any reviewed-content change.

For every structured projection, an `exit_id` field whose schema is the exact
matching const may be omitted only as the already selected route discriminator.
Every other producer field must be consumed. If the consumer requires
`exit_id`, it must still be projected. This rule is general and does not permit
dropping business data or inventing another projection operation.

## Task Publication Review Owner

`guru-review-task-publication` is the active Interface 1.4 semantic owner
between `guru-review-branch:passed` and finalization. Workflow and standalone
use the same eight entry preconditions, ten-dimension AI Review Gate,
conditional confirmation, ignored-runtime recorder/checker, metadata revision
loop, freshness rules, and typed-exit conditions.

The package owns two closed structured profiles. `publication_review` requires
`profile/mode/task_ref/branch_review_commit/review_intent`; the Branch Review
producer supplies only `task_ref/branch_review_commit`, and the target-owned
authoring example supplies `profile/mode/review_intent`.
`publication_review_stale` requires
`profile/mode/task_ref/branch_review_commit/stale_reason/review_intent`; its
Finalizer producer supplies only
`task_ref/branch_review_commit/stale_reason`. Both partitions are disjoint,
cover the complete target required set, and merge without overwrite. Inputs
outside the current profile schemas fail closed; Publication never reads or
projects another Skill's checkpoint.

In workflow and standalone mode, the Publication AI authors the exact Chinese
PR title and Markdown body directly from live authority and reviews that payload
inside the same semantic loop. Neither the caller nor another Skill creates a
task-local PR body or finish-summary index candidate. Publication remains the
sole owner of payload sufficiency, Issue closure, all ten dimensions, finding
routing, revision, and readiness; Finalizer may consume only the checked payload
returned by `ready` and may not create or reinterpret it.

The independent minimal outputs are
`ready(exit_id,task_ref,branch_review_commit,pr_title,pr_body)` to active
`guru-finalize-task`,
`return_to_task_work(exit_id,task_ref,finding_refs,resume_target=phase-2)` to
the task-work workflow router, and `blocked(exit_id,reason_code,remediation)` to
an explicit stop. Review narrative, findings, artifact paths, live facts, and
digest bundles remain private.

The sole private gate is ignored-runtime `pr-readiness.json` under
`guru-task-publication-readiness-4.0`. It contains only task,
`branch_review_commit`, `reviewed_content_sha256`, the closed exact
`pr_payload(title,body)`,
the ten AI-reviewed dimensions, findings with closure evidence, three
scope/Docs/safety conclusions, and the selected route. The recorder/checker
rebuild all eight objective entry preconditions transiently; those live facts,
artifact digests, repository snapshots, reviewer metadata, confirmation state,
and Finalizer internals never enter the checkpoint or public DTO. `ready`
requires every objective entry precondition, all ten dimensions, and all three
conclusions to pass, with every finding closed. It also runs the exact
side-effect-free Finalizer closeout preflight before returning ready, so schema,
length, duplicate, derived-field, archive, and plan constraints cannot produce
a false-ready followed by an immediately stale first preview.

`return_to_task_work` requires an open `task_work` finding bound to a `finding`
dimension and cannot carry blocked evidence. `blocked` requires an open
`external_blocker` finding bound to a `blocked` dimension and at least one
blocked scope/Docs/safety conclusion. Open metadata-revision findings remain
inside the Skill loop and cannot satisfy an external exit. Non-current input or
checkpoint shapes fail schema validation. For a stale-profile invocation whose
`branch_review_commit` has normal content
continuity drift, only a semantic `return_to_task_work` may pass the checker;
`ready` and `blocked` do not bypass continuity. This exception requires a valid
commit proven to be an ancestor of current HEAD and a successful shared-identity
comparison; invalid or non-ancestor identities and inspection failure remain
fail closed on every exit.

For `publication_review_stale`, `branch_review_commit` binds producer,
invocation, and checked owner result while `stale_reason` binds the current
automatic re-entry invocation only. Neither is persisted as re-entry narrative
or copied into a Publication exit. The fresh semantic result replaces the
single owner-private checkpoint; no supersession ref or user confirmation is
required for mapped stale/re-entry handling.

Metadata-only findings may revise only the owner-private PR payload or Issue
Scope Ledger publication metadata, followed by
a dependency-scoped review: reread all eight objective preconditions, re-review
dimensions whose direct evidence changed, and carry a prior passed dimension
only while its evidence remains current and byte-identical. Source, test,
durable docs, spec, workflow, schema, config, preset, CI/CD, deployment, or
Branch Review drift exits to task work. Scripts preserve AI-authored conclusions
and never decide sufficiency, issue closure, dimension status, finding route,
or `ready`.

The publication repository binding uses the shared reviewed-content boundary,
scope-only `issue-scope-ledger.json`, and the exact owner-private PR payload.
Branch Review continuity comes from the public Git
anchor, shared content identity, and live Git, not from reopening its private checkpoint. The recorder-owned
ignored `pr-readiness.json` is excluded from its own snapshot. Runtime input is
allowed only when the current command explicitly names that regular file under
`.trellis/.runtime/guru-team/`; neither the whole task prefix nor the runtime
prefix is allowed. Any other status path records a failed
`review_range_and_working_tree` binding and prevents `ready`.

The current ready output schema is
`guru-production-review-task-publication-output-ready-4.0`; the active
Finalizer input is `guru-finalize-task-input-publication-ready-4.0`, with
aggregate input schema `guru-finalize-task-input-aggregate-6.0`. Aggregate
3.0/4.0/5.0 remain compatibility assets. The integrated
`select` projection carries exactly `task_ref`, `branch_review_commit`,
`pr_title`, and `pr_body`; Finalizer target authoring supplies only
`profile/mode`. Any legacy 3.0 input or output shape fails closed and requires a
fresh Publication invocation. No alias, task-local fallback, compatibility
reader, or migration executor is part of the current contract.

The current additive activation set contributes to the live closure of sixteen
active Skills and 62 exits. The production current manifest remains exactly
three Skills and 11 exits.

## Extension Installation Verification Owner

`guru-verify-extension-installation` was the fifteenth active package and selects
Interface 1.5 with `workflow_integration_state=standalone_only`. It is outside
the three-Skill `production-current-v2` manifest and outside the mandatory
business workflow graph. Its only current structured input is
`source_repository_verification`, fixed to standalone mode and explicit caller
intent from a clean `castbox/guru-trellis` source checkout.

`guru-reconcile-task-base` is the sixteenth active package and the fifteenth
integrated business-workflow owner. Its six exits and the additive Branch
Review and Finalizer exits produce the current 62-package-exit and
60-workflow-exit closure.

Source preflight validates canonical source assets, credential-free canonical
`origin`, `repo_ref`, requested ref resolution, current HEAD, and clean tree
before clone, tempdir creation, installer execution, artifact write, or Git/
GitHub mutation. Task-bearing fields, non-source repositories, ref/HEAD mismatch,
and dirty source state fail closed with stable invocation errors and zero
executor calls. The package then owns capability selection, adequacy, findings,
redaction, and one of two exits: `verified` or `blocked`. Both return directly
to the standalone caller; neither has a Finalizer projection or workflow marker.

Private execution and semantic result state is ignored source-session runtime,
removed after direct consumption, and never written below `.trellis/tasks/**`.
Changed paths, installed manifests, business repository state, Publication,
Finalizer, finish-work, re-entry, and recovery cannot make this Skill applicable.
Legacy workflow/task-bearing input, `not_required`, `return_to_task_work`, and
Finalizer projection schemas remain immutable compatibility assets only; current
Interface, registry, eval corpus, manifest inventory, and runtime reject them.

## Task Finalization Owner

`guru-finalize-task` is the active Interface 1.4 semantic owner of the complete
business task closeout loop. Current aggregate input 6.0 has four profiles:
`publication_ready`, `same_plan_resume`, `reprepare_preview`, and
`standalone_finalization`. It has six outputs: `base_reconciliation_required`,
`publication_review_stale`, `resume_finalization`, `reprepare_required`,
`ready_for_merge`, and `blocked`. The base-reconciliation exit owns only a
base-only mismatch and remains distinct from stale Publication content.
Producer seed fields and target-owned authoring fields remain disjoint and cover
each current input schema exactly.

The five-stage semantic profile is preview/current-state discovery, AI review,
confirmation of one displayed side-effect plan when required, ignored-runtime
gate recorder/checker, and one typed exit. Current gate 5.0 and transaction 3.0
bind exact Publication input and Finalizer-owned recovery state. Ordinary mode
continues to a new Draft PR. The private `existing_pr_recovery` mode binds a
unique same-repository PR, pre-push HEAD, original Draft/Ready state and scope,
then converges metadata, archives, and preserves Ready or marks Draft Ready.
Both modes produce the same minimal Merge handoff. Finalizer does
not invoke verifier, emit `verification_required`, accept verification re-entry,
read verifier owner state, or archive a verifier artifact.

`publication_review_stale` projects exactly
`task_ref/branch_review_commit/stale_reason` to Publication. Publication itself
retains `return_to_task_work` for real content drift. `reprepare_required`
projects only task/reason and reviewed/publication HEAD identity needed by the
next Finalizer invocation. `ready_for_merge` carries the canonical PR and
expected-head/branch/close-Issue authority needed by `guru-merge-task-pr`.
Internal transaction state, semantic review, authorization, live facts, paths,
and digests remain private.
Transaction 2.0 remains an explicit legacy schema and is not current Interface
authority.

Current archive contains exactly six durable core files: `task.json`, `prd.md`,
`design.md`, `implement.md`, `issue-scope-ledger.json`, and
`finish-summary.json`. Legacy closeout-plan and task-bearing verification schemas
remain immutable compatibility assets and never enter current Interface,
registry, workflow, preparation, recovery, eval, or archive routes.

## Task Base Reconciliation Owner

`guru-reconcile-task-base` is the package-local semantic owner for active-task
base evolution. Its public inputs are separated by caller profile and bind the
task ref and task-content HEAD, selected base ref, old and current base HEAD,
and one closed `resume_target`. A caller continuity identity is included only
when this owner must judge whether that caller's semantic result remains valid.
The Skill reads the canonical
`.trellis/spec/workflow/semantic-retrieval.md`; its package, workflow, platform
entries, examples, and docs must not copy the bilingual concept families or
negative-existence algorithm.

The package exposes six independently versioned output schemas:
`reconciled`, `review_continuity_required`, `implementation_required`,
`planning_stale`, `scope_confirmation_required`, and `blocked`. Each
output contains only pair/route identity that its unique consumer cannot
rebuild. Complete authority reads, base-delta scans, candidate state,
validation history, findings, and derived digests remain owner-private. No
single aggregate output with nullable fields may substitute for the six
contracts.

The semantic review independently classifies authority impact, task-content
impact, and integration-only impact, checks one temporary integration
candidate, selects affected validation, and returns exactly one exit. It never
merges or rebases the task branch, creates a durable ref or commit, imports
another package's private runtime, or persists authorization. A current result
may be retained only in ignored task-local owner runtime for its next declared
consumer and is deleted after successful consumption.

`guru-review-branch` additionally owns a bounded base-continuity input
profile. It reuses the existing semantic task review only when the task-content
HEAD is unchanged, then independently reviews the semantically selected base
delta, temporary candidate, conflict resolution, and affected validation. A
continuity pass establishes integration readiness for that exact pair; it does
not rewrite the prior reviewed HEAD. Required task bytes return to
implementation, while planning or authority changes route to their real owner.
