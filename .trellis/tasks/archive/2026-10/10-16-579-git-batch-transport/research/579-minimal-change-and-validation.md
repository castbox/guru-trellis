# Research: #579 minimal change and validation

- Query: Locate the smallest Git batch transport repair, direct consumers, distribution projections, and verification/architecture ownership.
- Scope: internal
- Date: 2026-10-16

## Findings

### Files found and code patterns

- `trellis/skills/guru-team/packages/guru-review-branch/runtime/common.py:340`: `tree_identity` reads a committed tree, batches blob requests, then hashes ordered path/content identities. Its `subprocess.run(input=..., stdout=PIPE)` batch call is at line 371. Keep blob parsing, ordered rows, gitlink handling and final digest unchanged; replace only input transport.
- `trellis/skills/guru-team/packages/guru-review-branch/runtime/record.py:127`: continuity recorder checks the current committed tree against `candidate_tree_sha256`.
- `trellis/skills/guru-team/packages/guru-review-branch/runtime/common.py:546`: existing gate validation independently recomputes that same candidate identity.
- `trellis/skills/guru-team/packages/guru-review-branch/tests/test_contract.py:216`: independent per-blob digest oracle; line 602 covers recorder, checker and invoke retirement in the normal continuity path. This offers a direct regression seam without a new workflow profile.
- `trellis/skills/guru-team/packages/guru-review-branch/evals/evals.json:94`: existing `base-continuity-passed` scenario already owns the unchanged semantic route.
- `trellis/skills/guru-team/packages/guru-reconcile-task-base/runtime/common.py:186`: reconciliation already reads individual blobs; it does not use the affected dual-pipe batch transport.
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:1316`: package projection installer. Dogfood package copies are `.trellis/guru-team/skills/packages/guru-review-branch`, `.agents/skills/guru-review-branch`, and `.codex/skills/guru-review-branch`; use canonical source plus installer rather than hand editing copies.

### Minimal verification

Run `python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-review-branch/tests -p 'test_*.py'`. A regression should use real Git objects large enough to cross request/output pipe capacities, a finite completion bound, and the independent digest oracle. Include ordinary binary/empty/repeated blob content as needed to demonstrate preserved batch semantics. Exercise recorder/checker continuation using the existing normal integration fixture. Exact incident object count and 162 MB output need not become a fixed CI requirement.

Run `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` and `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` in the execution checkout, inspecting any generated sidecars. Package-private tests execute in the source checkout; clean installed repositories validate public projections rather than source-only tests. Full multi-platform installation/release matrices are outside this bounded defect unless live Issue authority explicitly adds them.

### Related specs and design ownership

- `.trellis/spec/workflow/quality-guidelines.md`, Base Evolution Gate Quality: normal bounded continuity and existing identity checks remain authoritative.
- `docs/architecture/00-foundation/baseline.md`: Markdown semantic owners versus deterministic runtime facts and minimum state remain unchanged.
- `docs/architecture/06-governance/change-contract.md`, Change paths and lifecycle: `no_architecture_impact` is available when transport changes leave architecture/public contracts/owners/state unchanged. Architecture owner must judge applicability; do not invent an ADR merely for an implementation transport detail. Any necessary design decision belongs in the appropriate existing baseline location under that owner.
- `docs/requirements-design-test-contributions/567-fixed-development-baseline/`: example of the existing RDT contribution organization (`manifest.yaml`, requirements, design, test, traceability), if the RDT owner requires durable synchronization.
- `trellis/skills/guru-team/tests/legacy_base_continuity_integration.py`: historical fixture, not a reason to reactivate retired workflow paths.

### External references

No external technical fact was needed for this file-location research. Trellis official extension documentation remains required before implementation changes to extension surfaces: https://docs.trytrellis.app/index.md ; https://docs.trytrellis.app/advanced/custom-workflow.md ; https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md .

## Caveats / Not Found

This research locates implementation and verification seams; it does not repeat incident diagnosis or claim current test execution. Line numbers describe source inspected before implementation and may move. No change to public DTOs, route semantics, identity algorithm, retries, timeout policy or unrelated subprocess users is proposed. A fixture should prove normal completion and identity preservation, not merely assert the implementation uses a temporary file.
