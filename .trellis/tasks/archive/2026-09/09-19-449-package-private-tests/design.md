# Design

## Boundary

The canonical package tree is the source-validation authority. The installed
package tree under `.trellis/guru-team/skills/packages` is a public runtime
projection and must not carry package-private `tests/` or other test-only
assets. Platform projections retain their existing public filtering rules.

## Installer

Introduce one package projection helper shared by installed package materialization
and the package inventory/provenance calculation. It filters only package-private
test assets while preserving the package's declared public contracts, schemas,
examples, wrapper, and runtime entrypoint. The canonical package tree remains
unchanged.

The desired installed path set is derived from canonical declarations and the
previous manifest. Existing stale-path removal is therefore reused for historical
`tests/` copies. The removal record keeps the installed path, action, and previous
managed SHA-256. Unknown local edits remain conflicts with `.new` provenance and
do not get deleted.

## Validation and reporting

Installed validation checks the installed package corpus independently from
platform projection checks and rejects any package-local `tests/` directory or
test file. Source validation continues to validate canonical package contracts
and tests. Installer result fields and tests distinguish source tests from
installed package/runtime validation; no installed result claims to execute
canonical package-private tests.

## Generated and dogfood projections

Canonical installer code and specs are the source of truth. After implementation,
reapply the preset in the dogfood checkout, inspect any `.new`/`.bak` files, and
regenerate the managed extension manifest/projections through the supported
installer path. Generated manifests are updated only as a consequence of that
deterministic reapply.

## Non-goals

- Do not delete canonical package tests.
- Do not change Skill runtime behavior or public semantic contracts.
- Do not modify business repositories.
- Do not add a second ledger, workspace mechanism, or hostile-input boundary.
