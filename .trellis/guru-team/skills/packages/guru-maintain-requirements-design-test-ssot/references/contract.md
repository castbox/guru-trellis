# Requirements Design Test SSOT Contract

This semantic package owns one atomic repository authority across Requirements,
Design, and Test. The default versioned roots are `docs/requirements/`,
`docs/design/`, and `docs/test/`; the default isolated task contribution is
`docs/requirements-design-test-contributions/<task-ref>/` with `manifest.yaml`,
`requirements.md`, `design.md`, `test.md`, and `traceability.md`.

Every active requirement or behavior links to an owning design responsibility
or contract and at least one test strategy, scenario, or case. References carry
identity and location, not duplicated prose. Subtraction and structural changes
preserve predecessor/successor and version history. Two parallel tasks use
different contribution locators and do not mutate the same shared current file.

The package inherits the public Architecture Baseline identity as
locator/version/status. It does not read Architecture private state or copy
Architecture content. Repository authority remains separate from Trellis
task-local `prd.md`, `design.md`, and `implement.md`.

The AI owns provenance, authority, completeness, traceability, conflict,
revision, sync, and route decisions. The deterministic runtime validates the
AI-authored exact public-input digest, Architecture Baseline
locator/version/status, explicit AI gate, declared mode/profile, continuation
identity, safe locator, direct version/freshness binding, unique consumer,
minimal output, and schema. It never overwrites those semantic-owner bindings. Public
output never contains document bodies, scan history, review narrative, Git
facts, authorization, recorder state, or private digests.

## Public input digest

For every profile, `owner_result.input_sha256` is the lowercase hexadecimal
SHA-256 of the complete `public_input` object in the current invocation.
Serialize that object with
`json.dumps(public_input, ensure_ascii=False, sort_keys=True, separators=(',', ':'))`,
then encode the resulting text as UTF-8. Do not append a newline to the hashed
bytes. Use the 64 hexadecimal characters directly, without a `sha256:` prefix.

Hash the object value, rather than the original file bytes or the complete
`{"public_input": ..., "owner_result": ...}` envelope. File indentation,
object key order and a file's final newline do not change this digest. Preserve
all input values; do not normalize Unicode, paths, whitespace inside strings,
arrays or versions. This existing binding checks consistency within this
invocation. It is not semantic approval or another producer's private identity.

The following standard-library recipe reads a regular file containing only
your actual `public_input` object and writes the digest to stdout. The printed
newline is not part of the digest.

```sh
python3 - path/to/public-input.json <<'PY'
import hashlib
import json
import sys

with open(sys.argv[1], encoding='utf-8') as source:
    public_input = json.load(source)
encoded = json.dumps(
    public_input, ensure_ascii=False, sort_keys=True, separators=(',', ':')
).encode('utf-8')
print(hashlib.sha256(encoded).hexdigest())
PY
```

For example, the following teaching input uses the existing bootstrap example
with a Chinese `applicability_scope`:

```json
{"profile":"bootstrap_foundation","source_exit":"start","mode":"workflow","continuation_id":"rdt-bootstrap","repo_locator":".","target_version":"1.0","applicability_scope":"闭区间筛选","architecture_baseline":{"locator":"docs/architecture/README.md","version":"1.0","status":"current"}}
```

Its digest is
`e38aad1ac49d5abdf00b316f9c496a8a0251e1995fb69a1c7600fe052c0e7e03`.
This example teaches encoding only; it supplies no current authority or gate.
When an input value changes, reread its applicable evidence, repeat this
owner's semantic review, and compute the digest from that current input.

## Owner result bindings

After the semantic review, bind only the fields needed by the selected exit.
The existing runtime compares the following values with the current public input:

| Owner-result field | Existing input binding |
| --- | --- |
| `profile`, `mode`, `continuation_id` | Copy the corresponding public-input values unchanged. |
| `input_sha256` | Compute the complete public-input digest using the recipe above. |
| `architecture_baseline` | Copy the complete public-input locator/version/status object unchanged. |
| `authority_locator`, `authority_version`, `task_locator`, `target_version`, `contribution_locator`, `sync_kind` | When a field occurs in both objects, preserve its public-input value. |
| `freshness` | When the selected result includes this field, copy public-input `authority_freshness` if that field exists; otherwise copy public-input `freshness` if supplied. |

For `ssot_current`, `active_version` equals the input's `target_version` in
`bootstrap_foundation` and `promotion`. It equals the input's
`authority_version` in `task_impact_sync` and `repair`. These bindings do not
select a version for the owner or establish that the documents are current.

After actual promotion writes and readback, keep this invocation's input
`freshness` in the owner result. A new description of the updated documents
does not replace that binding during the same invocation. The actual
`authority_locator`, `active_version`, status and semantic review describe
the integrated authority. A subsequent invocation rereads its applicable
authority and constructs its own current input. For a profile whose input has
neither freshness field, the owner supplies its reviewed observation according
to that profile; this copying rule introduces no new required input.

The complete teaching envelope below shows a promotion returning
`ssot_current` after actual write/readback. Its sample facts and gate are
illustrative. Author the real review yourself, use the actual selected profile
and source facts, and recompute `input_sha256` from that complete current
public input. This sample is neither an executed promotion nor a current gate.

```json
{
  "public_input": {
    "schema_version": "2.0",
    "profile": "promotion",
    "stage": "final_integration",
    "source_exit": "candidate_checked",
    "mode": "workflow",
    "continuation_id": "rdt-promotion-example",
    "authority_locator": "docs",
    "target_version": "1.0",
    "contribution_locator": "docs/requirements-design-test-contributions/example-task",
    "sync_kind": "promotion",
    "freshness": "reviewed-authority:example",
    "architecture_baseline": {
      "locator": "docs/architecture/README.md",
      "version": "1.0",
      "status": "current"
    }
  },
  "owner_result": {
    "profile": "promotion",
    "mode": "workflow",
    "continuation_id": "rdt-promotion-example",
    "input_sha256": "26bda821344d42c16c8e86fe6e32f8764e0b63741b23dc75fde54760307e29d4",
    "architecture_baseline": {
      "locator": "docs/architecture/README.md",
      "version": "1.0",
      "status": "current"
    },
    "ai_review_gate": {
      "status": "passed",
      "reviewed_scope": "Teaching sample: the original owner has reviewed the proposed and current complete definitions.",
      "evidence_summary": "Teaching sample: candidate Check preceded actual writes, and the owner read back the integrated units and relationships.",
      "findings": [],
      "conclusion": "Illustrative completed promotion; replace this entire review with the current owner's actual judgment."
    },
    "typed_exit": "ssot_current",
    "consumer": {
      "kind": "workflow",
      "id": "guru-requirements-design-test-ssot-current-router"
    },
    "authority_locator": "docs",
    "active_version": "1.0",
    "status": "active",
    "applicability_scope": "repository",
    "freshness": "reviewed-authority:example"
  }
}
```

## Stage applicability

Read [current-knowledge.md](current-knowledge.md) completely before every
profile. That shared contract owns unit completeness, status, stable identity,
necessary relationships, reading, structural revision and migration. This
package remains the only RDT semantic owner. Its current impact and promotion
inputs are 2.0 with explicit phase2 and final_integration stages. Bootstrap and
repair keep their original contracts. The old 1.0 impact/promotion schemas are
history-only; current runtime rejects their shape rather than dual-parsing.

This owner selects the RDT/Architecture versions applicable to the current
Task plan and candidate. Use actual immutable version/Git-history authority
when shared CURRENT advances without affecting this Task. Such advancement
does not require contribution rewrite, promotion or fresh business gates.
Explicitly applicable rules and real requirement/scope/dependency/solution
changes still enter the original revision owners. Shared-current promotion
retains its own live expected-current and subtraction/traceability checks.

## Complete-definition maintenance by profile

- `bootstrap_foundation`: establish the applicable entries and complete
  R/D/T units. When migrating an existing authority, compare all effective
  predecessor constraints, list migrated and unmigrated scope, and retain old
  complete-source navigation until the reviewed cutover.
- `task_impact_sync`: read the applicable complete units and necessary
  relationships before judging the delta. Select the original no-op,
  isolated-contribution, repair or revision route. An
  isolated delta identifies complete resulting definitions at its own
  proposed-target locators without duplicating unchanged authority. Complete
  changed proposals return `candidate_ready` with only contribution_locator,
  authority_locator and authority_version; the latter remains the applicable
  source identity. No-change returns actual `ssot_current`.
- `promotion` at final_integration: after candidate Check, reread the actual
  target, reconcile intervening changes, and
  integrate the reviewed contribution into complete current R/D/T units.
  Check surviving conditions, subtraction, stable identities and relationships
  before updating navigation/version entry. Historical contributions remain
  sources, not required assembly steps for ordinary migrated queries.
- `repair`: name missing or conflicting objects and affected conclusions.
  Restore complete definitions and links within the existing scope, or return
  the original incomplete/revision/blocked exit. Never infer that an
  unmigrated object is complete because its navigation resolves.

Apply current-knowledge.md's Stage limits and result observations contract
within these same profiles. On actual release of a limit, maintain affected
complete current units, guides and derived descriptions; coordinate assertion
updates with implementation. Review result cutoffs and original formal-result
references before returning the current route. Neither a historical failure
nor a later terminal result is rewritten into a different observation.

Only actual completed promotion returns `ssot_current` as an updated authority;
`candidate_ready` is not a promotion result. The owner writes and reads back
actual files before invoking the validator. There is no automatic document
writer or semantic inference from stage, version, directory or schema success.

All profiles retain their existing gate, freshness, confirmation, invocation
and typed-exit contracts. Planning and implementation consume selected bodies;
final Check and independent Review judge their current candidate and
reconciliation. Those stages do not inherit semantic pass from navigation,
promotion or an earlier stage.
