# ADR-014: Task Identity Session Binding Ownership

状态：`accepted`。来源：Issue #443 reviewed contribution；提升：`.56 -> .57`。

## Context

Task creation attach与terminal lifecycle已经存在，但binding丢失、跨session续接、同session切换task、
Reactivate generation变化及runtime mappings同时缺失仍需要一个统一owner。若把session、branch或worktree当作
长期身份，或为恢复再建binding ledger，会与official Trellis task/session authority形成双写和恢复歧义。

## Decision

Task identity保持唯一长期主身份。official Trellis `active_task` / `session_storage`与task/workspace mappings
继续拥有底层resolver、store和identity facts；`guru-bind-task-session`是lifecycle-aware resume、rebind、switch、
reactivate rebind与authorized manual recovery的唯一semantic owner和deterministic writer/validator。

每次操作fresh验证task artifact、repository common dir、branch、worktree、HEAD、base provenance、mappings、
session context和lifecycle generation。base provenance不得从调用时live base反推；mismatch在任何write前停止。
manual recovery只重建最小ignored mappings和当前binding，写后重新验证；合法重试幂等。public DTO排除runtime
binding identity、绝对路径、完整snapshot、authorization、semantic pass和private recovery state。

Package以active/deferred进入32/142/102 registry closure。#438保留creation attach，#436保留Completion/Closure/
Finish/Cleanup/Reactivate ownership，#434独占production graph activation和旧edge retirement。

## Consequences

`.57` current authority包含task identity session binding能力，但production workflow仍为22 mandatory invokes /
98 exits。Promotion不授权Publication、push、PR、merge、Release、Issue closure或cleanup；promotion-created diff
必须通过fresh Phase 2、Task Commit和independent complete Branch Review。
