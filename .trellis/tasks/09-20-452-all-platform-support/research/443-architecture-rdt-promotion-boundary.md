# Research: #443 Architecture and RDT promotion boundary for .57

- Query: Enumerate the minimum Architecture/RDT authority changes required to promote `current-main-0.6.17-guru.56` to `.57`, absorb #443 as 32 packages / 142 exits / 102 commands, preserve the 22-invoke / 98-exit production graph, and identify `.trellis/spec` projection sync points.
- Scope: internal
- Date: 2026-09-20

## Findings

### Live before/after facts

- Current shared authority remains `.56/active`: `docs/architecture/README.md:3-9`, `docs/requirements/README.md:9,34-36`, `docs/design/README.md:3-9,35`, and `docs/test/README.md:3-9` all bind #436 and 31 packages / 136 exits / 101 commands.
- The live dirty candidate registry is already 32 active packages / 142 external exits / 102 commands. The additive delta is exactly `guru-bind-task-session`: one package, six external exits, and one command. Its canonical registry row is `trellis/skills/guru-team/registry.json:404-411`; its complete interface and command declarations are currently one-line JSON at `trellis/skills/guru-team/packages/guru-bind-task-session/interface.json:1` and `commands.json:1`.
- The canonical production workflow still derives to 22 `guru-skill-invoke` markers / 98 `guru-skill-exit` markers. Therefore `.57` must describe #443 as `active/deferred`; it must not add #443 workflow markers, consumers, or route activation. The existing boundary is stated in `docs/architecture/contributions/443-task-identity-session-binding.md:5,12,22,26` and `trellis/presets/guru-team/spec/workflow/skill-package-contract.md:2050-2052`.
- Existing `.56` promotion pattern is immutable-copy plus successor revision, not in-place rewriting. The current version has exactly 4 Requirements files, 5 Design files, and 3 Test files; the successor should copy these twelve files into new `.57` directories, then revise identity headers, internal cross-version links, #443 sections, traceability, counts, source binding, and evidence boundary. See `.56` opening contracts at `docs/requirements/versions/current-main-0.6.17-guru.56/requirement-main.md:3-8`, `docs/design/versions/current-main-0.6.17-guru.56/design-main.md:3-8`, `docs/design/versions/current-main-0.6.17-guru.56/manifest.yaml:1-19`, and `docs/test/versions/current-main-0.6.17-guru.56/test-strategy.md:3-8`.

### Minimum Architecture file set

The minimum Architecture promotion set is ten files. Foundation, target, and the generic change contract do not need semantic changes unless review finds a new cross-cutting rule beyond the existing single-writer/freshness rules.

1. `docs/architecture/README.md`
   - Change `.56/active` to `.57/active`, predecessor `.56`, source baseline reviewed #443 contribution, registry 32/142/102, and retain production 22/98 and #434 exclusivity. Current identity is at lines 3-9.
2. `docs/architecture/01-current/system.md`
   - Add `ARCH-CUR-034` for the reviewed #443 additive/deferred package and make it the current graph fact. Existing latest current entry `ARCH-CUR-033` is at lines 102-109; current identity summary at 111-115 must become `.57` without rewriting historical entries.
3. `docs/architecture/03-domains/ownership.md`
   - Add `ARCH-DOM-019` for task-identity session binding: official Trellis `active_task`/`session_storage` remain resolver/store; `guru-bind-task-session` is the only lifecycle-aware bind/rebind/switch/resume writer/validator; #438 keeps creation attach, #436 keeps Reactivate/Finish/Cleanup receipt ownership, and #434 alone consumes the deferred routes. Existing domain sequence ends with `ARCH-DOM-018` at lines 21-24.
4. `docs/architecture/04-integrations/distribution.md`
   - Add `ARCH-INT-022` describing one additive/deferred package projected to canonical, installed, Shared/Codex/Claude/Cursor/OpenCode surfaces while production markers remain 22/98. Existing sequence ends with `ARCH-INT-021` at lines 86-89.
5. `docs/architecture/05-gaps/current-to-target.md`
   - Revise `ARCH-GAP-009` at line 13 so CURRENT says `.57` includes Delivery, terminal lifecycle, and session-binding prerequisites, while the remaining gap is still #434's atomic production cutover. Do not mark production activation closed.
6. `docs/architecture/07-plans/roadmap.md`
   - Change the current promotion note at lines 3-5 and add a #443 row after #436 at lines 16-17: expected `.56` to `.57`, 32/142/102, package deferred, production 22/98, #434 still owner.
7. `docs/architecture/evidence/current-evidence.md`
   - Add `EVD-032` after `EVD-031` at lines 146-159. It must bind the exact committed #443 candidate, independent full-diff review, package/runtime and A-to-B-to-A/rebind/reactivate-generation/mismatch-zero-write checks, projection/ownership/drift evidence, and 32/142/102 versus 22/98. It must explicitly not prove #434 activation, Release matrix, or production business operations.
8. `docs/architecture/adr/README.md`
   - Add accepted `ADR-014` after `ADR-013` at lines 16-17 and a locator after line 29.
9. `docs/architecture/adr/014-task-identity-session-binding.md` (new)
   - Record the durable decision: use official Trellis session resolver/store, one lifecycle-aware binding owner, stable task identity plus lifecycle generation, mismatch zero-write, no duplicate binding ledger/store, and deferred graph integration until #434. This is ADR-worthy because #443 establishes a new owner/persistence/freshness boundary, analogous to ADR-013's owner topology.
10. `docs/architecture/contributions/443-task-identity-session-binding.md`
    - Expand the current candidate-only document at lines 1-26 to the established promoted-contribution shape used by `docs/architecture/contributions/436-post-delivery-completion-finish.md:3-16,54-68`: add candidate identity, `reviewed_promoted`, source authority/task locator, related RDT contribution, expected `.56` and successor `.57`, concern matrix, exact project-check evidence, ADR/EVD references, and promotion boundary.

No minimum change is required in `docs/architecture/00-foundation/*`, `02-target/target.md`, or `06-governance/{rules,change-contract}.md`: `ARCH-GOV-002..005,008` already require evidence, Architecture/RDT/projection consistency, isolated contributions, and expected-current-bound serialized promotion (`docs/architecture/06-governance/rules.md:4-10`). Add a new governance rule only if the reviewed #443 contribution identifies a reusable policy not already captured by the new domain/ADR.

### Minimum RDT contribution set

The repository has no `docs/requirements-design-test-contributions/443-task-identity-session-binding/` directory. Before promotion it needs the same five-file contribution shape shown by #436 at `docs/requirements-design-test-contributions/436-post-delivery-completion-finish/manifest.yaml:1-18`:

- `docs/requirements-design-test-contributions/443-task-identity-session-binding/manifest.yaml`
- `docs/requirements-design-test-contributions/443-task-identity-session-binding/requirements.md`
- `docs/requirements-design-test-contributions/443-task-identity-session-binding/design.md`
- `docs/requirements-design-test-contributions/443-task-identity-session-binding/test.md`
- `docs/requirements-design-test-contributions/443-task-identity-session-binding/traceability.md`

Final promoted state should be `reviewed_promoted`; source and expected-current version `.56`; target `.57`; Architecture contribution locator `docs/architecture/contributions/443-task-identity-session-binding.md`. Requirements should define stable identity, rebind/switch/resume/manual-recovery routes, lifecycle-generation invalidation, idempotence, mismatch zero-write, official resolver/store reuse, complete projections, and #434 deferral. Design should define the semantic owner plus deterministic validator/write boundary and minimal exit-specific DTOs. Test should distinguish executed evidence from the acceptance matrix. Traceability should close `R443 -> D443 -> T443 -> ARCH-CUR-034/ARCH-DOM-019/ARCH-INT-022/ADR-014/EVD-032`.

### Minimum `.57` shared RDT version set

Copy all twelve immutable `.56` files to `.57`, then revise them. Omitting any file would break the current three-layer version shape and cross-links.

Requirements, four files:

- `docs/requirements/versions/current-main-0.6.17-guru.57/requirement-main.md`
- `docs/requirements/versions/current-main-0.6.17-guru.57/requirement-non-functional.md`
- `docs/requirements/versions/current-main-0.6.17-guru.57/decisions.md`
- `docs/requirements/versions/current-main-0.6.17-guru.57/traceability.md`

Design, five files:

- `docs/design/versions/current-main-0.6.17-guru.57/design-main.md`
- `docs/design/versions/current-main-0.6.17-guru.57/capability-inventory.md`
- `docs/design/versions/current-main-0.6.17-guru.57/decisions.md`
- `docs/design/versions/current-main-0.6.17-guru.57/traceability.md`
- `docs/design/versions/current-main-0.6.17-guru.57/manifest.yaml`

Test, three files:

- `docs/test/versions/current-main-0.6.17-guru.57/test-strategy.md`
- `docs/test/versions/current-main-0.6.17-guru.57/test-plan.md`
- `docs/test/versions/current-main-0.6.17-guru.57/traceability.md`

Required revision pattern is visible in the `.55 -> .56` delta: update every opening identity/source/count block, append one stable requirement/design/test section, append one decision block, append bidirectional trace tables, regenerate the Design capability inventory from live registry/interfaces/commands, and keep all historical counts scoped to their historical versions. Existing #436 append points are `requirement-main.md:503-512`, `requirements decisions.md:98-101`, `requirements traceability.md:242-255`, `design-main.md:510-522`, `design decisions.md:104-107`, `design traceability.md:211-224`, `test-strategy.md:368-383`, `test-plan.md:328-339`, and `test traceability.md:225-238`.

Three current navigation files must also move `.56` to superseded and `.57` to active:

- `docs/requirements/README.md:9-10,33-36,94`
- `docs/design/README.md:3,9-10,35`
- `docs/test/README.md:3-10,33`

The `.57` Design manifest must set predecessor `.56`, all RDT locators to `.57`, `active_skill_count: 32`, `external_exit_count: 142`, `command_count: 102`, and provenance reviewed #443 while preserving extension `0.6.17-guru.42`, CLI `0.6.17`, repository target `v0.6.17-guru.1`, and fixed framework source unless a separate live authority changes them. The `.56` manifest pattern is at `docs/design/versions/current-main-0.6.17-guru.56/manifest.yaml:1-19`.

### `.trellis/spec` projection sync points

Two project-local authority projections are already stale at `.55`, even before `.57` promotion:

- `.trellis/spec/architecture/baseline-usage.md:5-12` must be repaired to `.57/active`, reviewed #443 + inherited immutable `.56`, 32/142/102, `ARCH-CUR-034` / `ARCH-DOM-019` / `ARCH-INT-022` / `ARCH-GAP-009` / `ADR-014`, production 22/98, and #434 deferral.
- `.trellis/spec/docs/requirements-design-test-ssot.md:5-11,21` must be repaired to `.57/active`, Architecture `.57/active`, reviewed #443 source binding, 32/142/102, and `R443/D443/T443` current delta. This file currently points to `.55`, although shared docs already point to `.56`.

The reusable canonical/dogfood workflow spec pair already contains #443 and currently has byte parity:

- `trellis/presets/guru-team/spec/workflow/data-contracts.md:1925-1929`
- `.trellis/spec/workflow/data-contracts.md:1925-1929`
- `trellis/presets/guru-team/spec/workflow/skill-package-contract.md:2050-2052`
- `.trellis/spec/workflow/skill-package-contract.md:2050-2052`

However, `skill-package-contract.md:2052` says “five typed exits” while the live interface declares five success exits plus `binding_blocked`, six external exits total. Because 136 -> 142 depends on six exits, the canonical and dogfood copies should be corrected together (for example, “five successful routes plus one blocked exit”) and remain byte-identical. The canonical-to-dogfood managed projection is declared in `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:157-190`; local `docs/` and `architecture/` projections are repository-specific and are not generated by that preset list.

### Contribution and evidence state transitions

- Architecture contribution: candidate/task-owned -> independently reviewed -> `reviewed_promoted`, absorbed by `.57`; expected current `.56`, successor `.57`.
- RDT contribution manifest and four documents: task contribution -> `reviewed_promoted`; source/expected `.56`, target `.57`.
- ADR-014: new -> `accepted` only as part of the paired reviewed promotion; it must not claim runtime activation.
- EVD-032: new reviewed-promotion-source evidence. It records exact review/test facts and remaining gates; it is not Release or production evidence.
- Shared Architecture/RDT: `.56` becomes immutable `superseded`; `.57` becomes the sole `active` current authority.
- Runtime/package integration: `guru-bind-task-session` remains `state=active`, `workflow_integration_state=deferred`; production workflow remains 22/98 until #434.

## Caveats / Not Found

- The worktree is heavily dirty and the branch is one commit behind its configured upstream. This research used current live workspace bytes only. No exact committed candidate range or independent #443 review evidence was found in the inspected authority documents, so `reviewed_promoted`, ADR acceptance, and EVD-032 facts cannot yet be truthfully asserted.
- `docs/architecture/contributions/443-task-identity-session-binding.md:16` calls the record an “ignored binding”, while the reusable spec says the package must use official `active_task`/`session_storage` and must not create a duplicate `.trellis/.runtime/guru-team/session-bindings/` store (`data-contracts.md:1927-1929`). Promotion wording must remove any ambiguity about a second store.
- The #443 Architecture contribution currently says validation is required (`:24-26`) but contains no concrete executed counts, committed range, review identity, or promotion state. Those details must come from fresh evidence, not be copied from #436.
- The current project-local `.trellis/spec` identity lag (`.55` while shared docs are `.56`) is already a repair condition under `ARCH-GOV-004` and the projections' own freshness rules. Promoting directly to `.57` without correcting both projections would leave Architecture/RDT/projection locators inconsistent.
- No tests, installer, apply/reapply, validators, network calls, Git mutations, or external commands with side effects were run. Existing unrelated workspace changes were not modified or reverted.
