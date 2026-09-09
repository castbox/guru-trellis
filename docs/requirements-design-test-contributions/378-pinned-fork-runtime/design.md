# Design Contribution

## Ownership

`D378-01` owns explicit source validation and direct Fork CLI use; `D378-02`
owns the Fork resolver/main-hook boundary; `D378-03` owns preset source-record
projection; `D378-04` owns verifier fixture composition and full/focused routing.

`castbox/Trellis` owns framework source and official generated templates.
`guru-trellis` owns Guru workflow/preset assets and source provenance records.
The fixed Fork SHA is the source identity; Guru does not create a second
framework implementation or patch installed upstream files directly.

## Integration

The existing verifier consumes the source lock and validates an explicitly
supplied Fork checkout. The Fork's own install/build commands produce the CLI;
the verifier calls its Node entry directly for init/update and reapplies the
Guru preset. No new launcher, distribution package, or dist-copy mechanism is
introduced. Source and installed checks consume the same lock; failure does not
select the original npm distribution.

## Compatibility

Use direct evolution for the original framework source path. No permanent
dual-source fallback is introduced. Existing local customizations, session
files, sidecars and unrelated worktrees are preserved and audited separately.
