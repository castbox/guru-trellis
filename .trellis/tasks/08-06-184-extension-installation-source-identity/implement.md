# #184 Implementation Plan

## 1. Preconditions

- [ ] Planning wording review passes for current `prd.md`, `design.md`, `implement.md`.
- [ ] `guru-approve-task-plan` passes with Issue #184 as the only close scope.
- [ ] `task.py start` activates the exact task in the exact worktree.
- [ ] `trellis-before-dev` loads workflow/preset/docs specs before source edits.
- [ ] Implementation sub-agent receives only the new task worktree and treats the old dirty
      candidate as read-only design input.

## 2. Ordered Implementation

### I1. Source provenance resolver

- [ ] Add closed manifest source parsing and canonical credential-safe GitHub locator helpers.
- [ ] Make clean Git preset installation record the full source commit as both immutable
      `source.ref` and `source.commit`; keep archive provenance non-verifiable.
- [ ] Add an isolated full-OID fetch path that requires `FETCH_HEAD^{commit}` to match both the
      requested OID and manifest commit before source assets are read.
- [ ] Preserve the canonical locator as the full-OID checkout's `origin` so nested source-owned
      preset/throwaway installs record a non-null `source.repo` provenance.
- [ ] Separate direct object from peeled commit and bind the selected commit to manifest source.
- [ ] Implement task-bearing required-manifest and taskless absent-manifest fallback branches.
- [ ] Add focused resolver tests for annotated/lightweight tags, branches, drift, malformed
      manifest and credential URL redaction.

### I2. Dual checkout executor

- [ ] Split target and extension source temp roots and record distinct checkout ownership.
- [ ] Keep target ref/HEAD/reviewed-content continuity entirely in target checkout/current task.
- [ ] Run installer/canonical assets/ownership/sidecars entirely from extension source checkout.
- [ ] Ensure removal of installer from target fixture does not affect source-driven success.

### I3. Private/execution schema and checker

- [ ] Introduce current-only target/source evidence schema and update runtime schema constants.
- [ ] Bind recorder/checker freshness to both identities and reject cross-owned or stale facts.
- [ ] Keep public input/exit ids and minimal DTO consumers unchanged.
- [ ] Update package examples/evals/contract tests without compatibility aliases.

### I4. Canonical distribution and docs

- [ ] Update preset manifest/installer inventory and tests from canonical sources.
- [ ] Update the seven Docs SSOT surfaces from `design.md`.
- [ ] Run preset apply to synchronize installed and Agents/Codex/Claude/Cursor copies.
- [ ] Resolve every generated `.new`/`.bak`, then prove byte equality and zero sidecars.

## 3. Validation Matrix

### Focused runtime and package tests

```bash
python3 -m unittest \
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest \
  trellis/skills/guru-team/packages/guru-verify-extension-installation/tests/test_contract.py
python3 -m unittest \
  trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
```

Required distinct regressions: target/source separation, annotated tag direct/peeled selection,
full-OID source fetch with canonical `origin`, target branch advance after manifest creation with a fixed source OID,
task-bearing manifest required, malformed manifest blocked, source drift, both checkout mismatches,
target content drift, missing source installer, taskless fallback, credential URL redaction and
stale evidence.

### Mechanical and distribution closure

```bash
python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh \
  trellis/presets/guru-team/scripts/bash/*.sh
python3 trellis/skills/guru-team/tests/test_skill_packages.py
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
git diff --check
```

### Clean install/update/reapply

- [ ] Run the repository's clean throwaway verification from a source-capable environment.
- [ ] Verify target fixture without an installer and source fixture with the canonical installer.
- [ ] Verify `trellis update`, preset reapply, source/installed/platform equality, ownership and
      recursive zero `.new`/`.bak`.
- [ ] Prove the real remote accepts an exact 40-hex commit fetch and that advancing the target ref
      does not alter the selected source commit; do not create an auxiliary tag or branch for this
      proof.
- [ ] Record any network/remote limitation separately; local tests do not prove pushed immutable
      ref or Afizzy production readiness.

## 4. Check And Review

- [ ] Run `guru-check-task` over the complete current task scope and full test matrix.
- [ ] Fix findings and rerun the complete check, not only the failing command.
- [ ] Reconcile Docs SSOT and decide whether any additional spec update is required.
- [ ] Keep commit/push/PR/release/Afizzy rerun outside implementation authorization.
