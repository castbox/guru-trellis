# Requirements Contribution

## Scope

Adopt the patched `castbox/Trellis` commit `ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`
as the actual Guru Trellis framework source and preserve strict session-scoped
active-task resolution.

## Requirements

Stable contribution IDs: `R378-01` fixed source and no fallback; `R378-02`
session isolation; `R378-03` installed projection consistency; `R378-04`
preserved verifier entry and fixture ownership. These IDs reference the live
#378 scope, not a second product authority.

- New and existing-project update flows consume the fixed Fork source and do not
  silently fall back to the original Trellis npm/repository source.
- Main Codex/session contexts without a matching identity do not borrow a sole
  sibling session; explicitly selected child-agent fallback remains supported.
- Source, installed runtime, selected platform projections, and reapply/drift
  evidence identify the same behavior and source commit.

## Acceptance

- Fixed-SHA source build and update path succeeds in isolated clean/existing
  fixtures, with no original framework package installation.
- Canonical/installed session tests cover zero, one, multiple, stale, exact and
  child-agent cases without changing non-owner session files.
- Shared current authority is not modified directly by this contribution.
