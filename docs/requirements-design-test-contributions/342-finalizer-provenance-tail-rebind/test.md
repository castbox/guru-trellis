# #342 Test contribution

- `T342-01`: a real Git fixture creates predecessor publication, pushes it to a
  bare remote, then adds one valid manifest-only provenance tail.
- `T342-02`: Ready/LF-convergence and Draft/metadata-equal variants assert
  strict ancestry, one new Publication push, zero PR create, correct metadata
  edit count, archive completion and Ready action.
- `T342-03`: mutation events prove transaction rebind precedes content push and
  every PR/archive/Ready mutation; terminal retry repeats nothing.
- `T342-04`: fixed-field, stage/mode/binding, remote-head and business-tail
  regressions block the new classifier; existing recovery tests retain the
  multiple/fork/terminal/scope/head/metadata/archive/gate matrix.
- `T342-05`: #338 equal-HEAD focused and real-topology tests remain passing and
  continue to report no publication push.
- `T342-06`: canonical/installed Finalizer tests, finish-family integration,
  all-platform preset reapply, ownership/drift/package/task/diff/sidecar checks
  provide targeted evidence; the full Release/Throwaway matrix is not run.
