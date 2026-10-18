# Lifecycle Git object benchmark

These source-private tools measure the original `CreateTaskTests` and
`BranchBindingTests` fixtures through actual public wrappers. They create
throwaway repositories and never edit the caller's Task records. They are not
part of the installed runtime inventory, a public Skill, or an automatic test
suite. Semantic/context inputs are fixtures; results do not prove native AI
review, live GitHub operation, or the complete installer/release matrix.

## Run

Use a source checkout's bootstrapped managed CPython 3.14.8, Git, Bash, and
macOS BSD `/usr/bin/time -l` for RSS. The managed runtime supplies the existing
fixture/dispatcher dependencies; bare PATH Python is not dependency evidence.
`--fork` must select the complete reviewed Fork checkout (D3 used commit
`2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`, CLI/Core
`0.7.0-castbox.3`), including `packages/cli/src/templates/trellis/scripts`.
No upstream assets are patched. Select the Fork path explicitly:

```bash
source_checkout="$PWD"
fork_checkout="/path/to/reviewed-fork"
benchmark_dir="trellis/skills/guru-team/runtime/task_lifecycle/tests/benchmarks"
run_root="$(mktemp -d)"
.trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime \
  "$benchmark_dir/run_suite.py" \
  --source "$source_checkout" --fork "$fork_checkout" \
  --output "$run_root/results" --pool "$run_root/pools"
```

This runs source16 then installed6 groups, fully serially. Each group runs two
fresh fixtures, preserving all samples and separately invoking recovery. Use a
new output directory for each run; failed directories are not replaced. Keep
the generated Task pools for the matched after run. They contain only legal
Task files from the original official writer, never copied binding/ledger
state. Preserve the pool's exact paths and bytes; recreating it on another day
changes date-bearing paths and is a new baseline.

For one group, select `--entry create|binding`, `--count 10|100`, and
`--pass timing|profile|rss|volume`:

```bash
.trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime \
  "$benchmark_dir/benchmark_lifecycle.py" \
  --source "$source_checkout" --fork "$fork_checkout" \
  --entry create --count 100 --pass timing --repeats 2 \
  --output "$run_root/single-group" --pool "$run_root/pools/pool-100"
```

Append `--installed` to use the original canonical preset installer in each
fresh fixture. The installer runs outside the operation timer using managed
`sys.executable` **and** its supported `--python sys.executable` flag. Merely
launching the installer with managed Python leaves its internal bootstrap's
PATH-Python default unchanged. The installed resolver must return the exact
source managed executable. Installed runtime/package files that map to source
are compared byte-for-byte; Task JSON paths/sizes before and after apply are
recorded. Creation commits installed assets, fast-forwards its primary, and
refreshes payload heads as the original installed test does. Binding receives
the same complete official scripts/version before original apply. Source and
installed trees differ legitimately and are not treated as paired identical
trees. The fixed suite measures installed timing/RSS/volume, without claiming
an installed pure-profile result.

## Measurement boundaries

- `create` changes existing official-writer-generated active Task count 10/100,
  holding refs=2 and worktrees=2. These are not archived or completed Tasks.
  The operation includes real creation followed by ensure, all validators,
  and the unchanged official `task.py create` child. `binding` changes extra
  no-target-Task branches 10/100, holding worktrees=1, unique heads=2, and the
  target Task content fixed. It preserves both normal first-invocation
  resolution scans and independently checks both results.
- Plain timing covers the complete real public-wrapper operation. Setup,
  installation, trace analysis, and object-size probes remain outside the
  timer. Recovery has separate wall time and trace offsets, excluded from
  initial-operation medians. No sample is discarded, no OS cache is flushed,
  and there is no extra warmup. Match order, environment, dependencies, Task
  pool, workload and repeat policy before comparing results.
- Profile is an independent pure cProfile pass of the original dispatcher,
  bypassing its launcher. It retains the real official writer subprocess and
  records its wall wait plus Trace2 offsets. Parent waiting is not official
  writer CPU. `prepare_creation_inputs` and `discover_branch_candidates` are
  the D3 hotspots. Cumulative nested rows overlap: do not add their internal
  path-read/resolve/establish time or subtract time across independent passes.
- RSS separately measures each real wrapper invocation and individual Git
  processes in bytes. Wrapper maximum cannot split parent Python from the
  synchronous official writer, and is not a simultaneous process-group sum.
  Controller/setup are excluded. Git RSS analysis occurs before recovery, so
  later recovery lines in the raw file are outside that reported maximum.
  Normal installed-tree `git status` is included in the Git maximum.
- Volume captures only regular-file `cat-file --batch` content input and
  scalar content requests. `--batch-check`/`-e` metadata is excluded. Outside
  the timer, object probes separate missing requests, successful blobs,
  unique OIDs, logical returned bytes, unique bytes, and largest blob.
  Returned bytes do not mean physical disk IO. A metadata/content batch may
  preserve per-path checks while fetching unique content once; the original
  official writer remains a distinct consumer and its cost must stay visible.

Each group retains `summary.json`, per-sample raw Trace2, inputs, stdout/stderr,
and pass-specific profile/RSS/request files. Wrapper call ranges and official
writer profile ranges permit independent classification of Git subprocesses.
Elapsed values from profile/RSS/volume must not replace plain timing medians.
The harness reports facts; task-specific semantic acceptance thresholds belong
to the selected Delivery's pre-implementation performance contract.

## D3 provenance

The initial D3 before used source `c422692bca2d385a264da4db0030612b1b306fe1`.
Its frozen temporary source harness SHA256 was
`cb451ad3832b5a9f7649b0c72fc88f6b47ea0f5a31c5183bcff516245d617508`,
profile helper was
`1cd0af1e0b9cde8acc3ec46fb0224be7a98f0d9613225e1d7f85d2c17e184bda`,
and installed variant was
`9b790dc06590c3ce80f6907ef862d6a8271d5a87f861f91611c7c21bff470e59`.
Those originals remain the matched D3 after tools. This canonical copy joins
only their duplicate source/installed plumbing behind `--installed`, preserves
their control flow/values, and parameterizes machine-local runner paths; it does
not replace already frozen evidence or introduce a second acceptance policy.
