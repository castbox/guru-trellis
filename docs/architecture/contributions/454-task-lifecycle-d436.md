# #454 D436 Terminal Lifecycle Package Architecture Contribution

- Identity: `architecture-contribution-454-task-lifecycle-d436-v1`.
- State: reviewed and promoted from immutable `.65` to current `.66`.
- Source: live #454, generation 6 task, #456 `436-*` migration inventory, and reviewed Phase C/D443 substrate.
- Change path: `target_native`; the existing identity/framework ownership remains with ADR-015. No new ADR is proposed.

The five historical deferred packages still project task workspace mappings, path-bearing task locators,
predecessor closeout receipts, or resource-list authority. D436 migrates their canonical package contracts
onto stable TaskId/generation, current source/scope/target, exact lifecycle results, live checkout/binding
resolution, and the one Git common-dir resource ledger. Completion alone judges accepted-scope completion;
Closure alone decides and performs Issue disposition; Finish alone persists the terminal archive and seals
the resource inventory; Cleanup alone deletes Guru-owned resources; Reactivate starts the next generation
of the same task. No package derives another owner's semantic pass from archive, PR, Issue or branch state.

Closure's frozen action set and Finish's pre-mutation Issue reread prevent a stale close result from sealing
resources. The Finish result and resource seal bind the current generation. A real non-fast-forward
bookkeeping merge leaves the task branch at the PR head: Finish seals that PR head as the resource
cleanup head, verifies the target archive at the separate merge SHA, then retires this generation's
branch binding. Cleanup rejects prior-generation
receipts and preserves caller-owned or unknown resources. Reactivate uses C3-C5 acquisition, binding and
ownership, not a second workspace mapping or copied official task/session store.

The reviewed contribution changes only canonical package majors and task-owned knowledge. The production graph,
registry selector, active manifest, installed/platform bytes and predecessor retirement remain E434/#434
responsibilities. Focused tests passed for the current source; the promotion-created committed range still
requires a fresh complete Branch Review. Historical #436 results and D443 evidence do not establish D436 pass.
