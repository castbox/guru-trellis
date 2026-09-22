---
name: guru-ensure-task-checkout
description: Resolve or acquire one live execution checkout for an existing task lifecycle without creating a second checkout authority.
---

# Guru Ensure Task Checkout

Use this semantic owner only for an existing `TaskLifecycleKey` and current
branch binding. Discover and validate every live registered checkout before
choosing a route. Exactly one valid candidate may resolve automatically; zero
or multiple candidates require reviewed selection or acquisition.

The only acquisition routes are `adopt_invocation_checkout` and
`provision_linked_worktree`. Paths, HEADs, dirty paths and topology are
call-local facts. Never read or write task/workspace mappings, persist a
checkout locator, or bypass an authority conflict through selection.

After the AI review and any required side-effect confirmation, invoke the
package wrapper with the checked semantic result. Return exactly one declared
typed exit. Recovery resumes only the same checkout-acquisition transaction.
