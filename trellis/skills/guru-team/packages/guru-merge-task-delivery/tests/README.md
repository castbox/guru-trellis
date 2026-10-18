# Local Git object benchmark

`benchmark_git_objects.py` is a source-private harness for the existing
`ManualRecoveryTests` / `DeliveryFlow` fixtures and real public wrappers. It
creates new temporary repositories; it does not edit historical Tasks. GitHub
responses and semantic judgments are fixtures. These results do not prove live
GitHub publication or native AI review.

From the source repository, use its managed Python:

```bash
.trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime \
  trellis/skills/guru-team/packages/guru-merge-task-delivery/tests/benchmark_git_objects.py \
  --api-common .trellis/scripts/common --paths 1000 --kind duplicates \
  --entry manual --repeats 2 --output /tmp/guru-bench-manual-1000
```

Each output directory must be new. `summary.json` contains samples and their
median; `git.trace.jsonl` retains raw Trace2. Preparation and streaming trace
analysis are outside the timer. Manual repeats are initial recording followed
by original-result recovery; history repeats query the same prepared cutoff.
The fixtures do not force cold OS caches. Path count means 4096-byte assets,
plus `app.txt` and one 16 MiB asset. Duplicate inputs use 64 small unique blobs;
`--kind unique` makes all small asset contents distinct.

Use `--paths 10000 --kind duplicates` and `--paths 10000 --kind unique` for the
large-path cases. For history path scaling use `--entry history --paths 100`
and `--entry history --paths 1000`. For Delivery scaling hold `--paths 10`
constant and choose `--entry history --deliveries 2` or `--deliveries 4`.
Additional fixture Deliveries use original public operations and Check/Review
wrappers; their semantic results remain fixture evidence.

`--source PATH` chooses the canonical checkout (default: this checkout).
`--installation PATH` selects an existing clean installed template through
`GURU_DELIVERY_TEST_INSTALLATION`; the original fixture copies it and reapplies
the selected source preset in its fresh Git context, then runs its installed
wrappers. This is source/installed local automation, not a full release matrix.
`--api-common PATH` (or `TRELLIS_DELIVERY_API_COMMON`) must point to the matching
reviewed upstream public Delivery API.

Run each instrumented pass with a separate new output directory and the same
input flags:

- `--pass timing` (default): original public wrapper wall time and all Git
  processes; `cat-file`, `show`, and `ls-tree` counts are analyzed afterward.
- `--pass volume`: additionally copies regular-file `cat-file --batch` stdin,
  never pipes. Counts scalar blob and batch content requests, unique OIDs,
  successful bytes, and largest blob across the repeated operations. Post-run
  size probes use real Git outside the timer/trace. This is logical returned
  content volume, not physical disk IO. Use this pass's raw request/trace files
  to compare per-operation reuse; its elapsed time is not a timing baseline.
- `--pass rss`: macOS BSD `/usr/bin/time -l` measures each actual wrapper runtime
  and Git process separately in bytes. These maxima are not a simultaneous
  process-group sum; fixture/controller preparation is excluded.
- `--pass profile`: a separate cProfile run of the original public dispatcher
  records candidate reconstruction, official hash, history candidate, and local
  provider subprocess time. It bypasses the launcher for profiling and cannot
  replace original-wrapper timing. Cumulative function times may overlap and
  must not be summed as disjoint stages.

All passes retain the public validators and store operations. Compare matching
passes, input sizes, repeats, dependencies, and installation modes. Instrumented
elapsed times must not be combined with plain timing samples or claimed as
remote network latency; fixture network waiting is zero.
