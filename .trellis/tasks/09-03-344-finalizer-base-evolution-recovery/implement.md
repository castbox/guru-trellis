# Implementation Plan

1. Read the canonical Finalizer package contract, runtime, focused tests, and
   quality guidelines for recovery topology ownership.
2. Add a bounded classifier/route projection that falls back from an
   inapplicable provenance-tail candidate to existing-PR strict-ancestor
   recovery without weakening genuine errors.
3. Add real Git-topology tests for one base merge and multiple base commits,
   including mutation counts, transaction identity, zero PR creation, one
   push, and retry idempotence.
4. Retain and rerun #342 direct-child provenance-tail, #338 equal-HEAD, and
   existing fail-closed recovery tests.
5. Apply the canonical preset projection and verify installed/platform copies
   and overlay drift.
6. Run the targeted package/runtime and projection checks required by the
   accepted scope; explicitly record any release-wide or production gates not
   covered.
