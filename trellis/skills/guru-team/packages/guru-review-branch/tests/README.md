# Bounded continuity benchmark

`benchmark_continuity.py` is a source-private integration harness using the
existing `DeliveryFlow`, real Git and public Review wrappers. Semantic results
and provider values are fixtures; it does not prove native AI judgment or live
GitHub publication. Source and installed fixtures use the actually supported
`pull_request` profile.

From the selected source checkout:

```bash
.trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime \
  trellis/skills/guru-team/packages/guru-review-branch/tests/benchmark_continuity.py \
  --api-common .trellis/scripts/common --paths 1000 --kind duplicates \
  --pass timing --output /tmp/NEW-CONTINUITY-RESULT
```

`--source PATH` chooses the canonical checkout; default is this checkout.
`--api-common PATH` or `TRELLIS_DELIVERY_API_COMMON` selects the matching reviewed
upstream Delivery API. `--installation PATH` uses the original fixture's
`GURU_DELIVERY_TEST_INSTALLATION` contract: copy a real installed template into
fresh Git context, then run the original preset reapply and installed wrappers.
No installed runtime is patched. The tool reuses source-private observation
helpers from the Merge package's benchmark harness; run it from a complete
source checkout, not a standalone installed package.

Each output directory must be new. Inputs are `--paths 1000 --kind duplicates`,
`--paths 10000 --kind duplicates` and `--paths 10000 --kind unique`. Small assets
are 4096 bytes, duplicate pool64, plus one16MiB blob. The actual committed tree
includes Task metadata and fixture/installed files; its path and unique object
counts and bytes are reported independently from the asset count.

Preparation runs actual Full Review -> independent main advancement -> actual
merge -> fresh current Check. It computes `candidate_tree_sha256` outside the
timer. Each operation then runs the complete public `review-branch.sh` recorder,
`check-review-gate.sh`, and `invoke.sh`, retaining every validator and normal
Git command. The default two repetitions use the same prepared candidate and
take their median; subcall times and actual results remain in `summary.json`.
No OS-cache purge or cold-cache claim. Three independent wrapper processes each
confirm facts; no cross-process cache is added by the benchmark.

Use separate new output directories for independent passes:

- `--pass timing`: original public-wrapper wall time. All Git subprocesses are
  observed through PATH/Trace2 and analyzed as a stream after the operation.
- `--pass volume`: additionally copies regular-file batch stdin with `pread`,
  preserving its input offset and avoiding pipes. One post-operation file-based
  `--batch-check` probes type/size outside timing/Trace2. Counts include only
  real content requests, not metadata `-e`. Byte totals are logical successful
  blob bytes, not physical disk IO. Request totals span both repetitions.
- `--pass rss`: macOS BSD time measures each actual wrapper runtime and Git
  process in bytes. These are individual maxima, not simultaneous group RSS;
  preparation/controller/installer memory is excluded.
- `--pass profile --profile-mode legacy`: independent cProfile of the original
  public dispatcher, bypassing the launcher. It retains the original before
  observer of `tree_identity`'s SHA256 constructor arguments. Legacy initial
  payload statistics do **not** measure streamed update bytes or actual
  completed content hashes after implementation changes.
- `--pass profile --profile-mode plain`: independent cProfile without hash
  observers. Compare only matching before/after profiling methods; the older
  instrumented profile and plain profile have different costs.
- `--pass hashes`: independent hash observation, excluded from timing/profile
  comparisons. Tracks constructed hash objects, all update bytes/calls and final
  digest under the `tree_identity` call stack, including hashes created in a
  helper. Reports origins by file/function/line and unique completed digests;
  map origins to the actual blob and final tree hash code. Do not interpret
  zero calls at an old source line as zero content hashing.

Cumulative `tree_identity` includes its internal work; never add nested
`validate_gate` cumulative times again. Record's repeated invocation count and
actual blob hash count are separate facts. Profile, hash observation, volume,
RSS and plain timing have different instrumentation costs and cannot be summed
or treated as interchangeable acceptance evidence. This harness does not set
performance thresholds; use the selected Delivery's pre-implementation contract.

## Promotion reference alignment

`test_promotion_alignment.py` runs the actual public Full Review, legal Check
rework, reference-alignment recorder/checker/invocation and Delivery Review on
one Git fixture. It checks current Check/candidate binding, original-output
recovery after checkpoint retirement, the cleared old full_review slot, full
Git-delta consistency, stale/missing input, and original-owner stop. Run it with
`TRELLIS_DELIVERY_API_COMMON` set to the matching public API common directory.
Semantic results in these tests are fixtures. They prove deterministic
transport and consumers, not an independent AI's reference-only judgment.
Existing continuity tests retain their separate integration meaning.
