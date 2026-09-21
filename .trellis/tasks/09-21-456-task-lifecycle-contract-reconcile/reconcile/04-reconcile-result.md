# Reconcile Result

## 1. Result

**Document-level reconcile complete against `#454@b695adc928c2064bd27f07e2bb3bbbd034540571`.**

The #443, #436, and #434 current consumer groups now have a closed mapping to one target contract. This result authorizes
only downstream planning: it does not implement substrate, migrate packages, or activate the production graph.

```text
Current contract analysis
  -> exact #454 target mapping
  -> one retain/replace/retire/out_of_scope disposition per item
  -> one downstream owner, dependency, activation block, and completion proof per migration item
```

## 2. Fixed Conclusions

1. Session stored/public payload is `TaskLifecycleDTO(task_id, lifecycle_generation)` only. Bind never emits TaskRef,
   path, branch, HEAD, ownership, authorization, or session locator.
2. TaskRef is a mutable artifact locator freshly derived by the direct consumer when required.
3. Task/workspace mappings and path-bearing authority are retired without alias or compatibility adapter.
4. Reactivate retains only planning/blocking identity from the old exit set, retires direct requirements/implementation/
   evidence exits, and adds session recovery, transaction resume, and source correction routes.
5. Completion, Closure, Finish, and Cleanup retain semantic ownership but replace their public DTOs and recovery contracts.
6. The common-dir resource ledger is the only resource ownership authority. Finish seals the generation inventory;
   Cleanup alone owns deletion and Cleanup result.
7. #434 may compose and activate the graph only after substrate and package migrations pass. It cannot copy identity,
   session, branch, checkout, transaction, ledger, Finish inventory, or Cleanup result authority.

## 3. Closure Counts

| Check | Result |
| --- | --- |
| Inventory Item IDs | 47 |
| Mapping Item IDs | 47, exact set match |
| Items without disposition | 0 |
| `replace|retire` items | 33 |
| Migration boundary rows | 33, exact set match |
| Out-of-scope items | 1 (`434-DIRTY-WORKTREE`) |
| Target SHA across four documents | one full SHA |
| Exact public schema fields | enumerated in Inventory section 6 and bound to one Item ID each |
| Exact current exits/consumers | enumerated in Inventory section 7 and bound to one Item ID each |
| Replace/retire rows with multiple owners | 0 |

## 4. Successor Order

1. Phase C: implement and validate #454 substrate.
2. Phase D443: migrate Bind package/schema/runtime/projections.
3. Phase D436: migrate Reactivate, Completion, Closure, Finish, and Cleanup packages.
4. Phase E434: fresh reconcile current package contracts, then atomically activate workflow/registry/manifest/projections.

No successor may use the old Interface `1.4` payloads as target authority or reuse the separate #434 dirty planning state.

## 5. Durable Boundary

This document records the contract reconcile only. It does not authorize push, PR, merge, implementation, package or
schema migration, workflow or production-graph activation, release, or cleanup. Current Git and Trellis workflow progress
is not part of the business reconcile authority and must be reread by each successor owner from live state.

The conclusions above do not claim that substrate, package, schema, workflow, or production graph work has been implemented,
migrated, validated, or activated.

## 6. Preserved Boundaries

- No production code, schema, package interface, workflow, registry, manifest, projection, or installer was modified.
- Historical #443/#436/#434 task artifacts were not modified.
- The #434 dirty worktree was not modified.
- No implementation, production workflow/graph activation, push, PR, merge, release, or cleanup is authorized by this
  document-level result.
