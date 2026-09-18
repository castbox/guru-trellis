# #435 执行计划

状态：Phase 1 candidate。下列动作仅在当前计划被用户接受并由 workflow执行 `task.py start` 后进入；本轮不执行。

## 1. 实施顺序

1. 每轮写入前运行 workspace boundary check，fresh读取 #435/#434/#436、task、current diff、Architecture/RDT authority与现有 package interfaces。
2. 创建 `guru-review-task-delivery` canonical package：closed public profiles/exits、private semantic gate、recorder/checker/public wrapper、errors、examples、evals与 tests。
3. 从 current Finalizer抽取或复用纯 deterministic Git/GitHub primitives，创建 `guru-publish-task-delivery`；删除所有 archive/finish/completion/closure responsibility，移植 #405 equal-head recovery。
4. 创建 `guru-merge-task-delivery`：固定 merge-commit method、exact subject/body/trailer、independent confirmation、terminal recovery与 `delivered` projection；禁止 closing keyword。
5. 为 Planning/Approval加入 closed Delivery policy；对 Check、Task Commit、Branch Review做最小 sliced-delivery语义与 projection修改，保持单一现有 owner。
6. 扩展 `guru-reconcile-task-base` 的 #407 resolved-tree path，绑定 fresh Phase 2与 exact merge tree，完成同一 commit recovery。
7. 增加 cross-package integration：Review -> Publish -> Merge -> minimal #436 consumer fixture；两个顺序 Delivery；Reactivate current-binding seed；bookkeeping exclusion；base conflict resolved merge。
8. 更新 canonical workflow/spec/README、skill registry/interface consumer declarations、preset installer/validator、manifest与 source package closure；不激活 production edges。
9. 运行 preset apply同步 dogfood与声明平台 projections；逐项解决 `.new/.bak`，检查 installed manifest/package tree/hash。
10. 创建完整 RDT contribution并与 Architecture contribution/ADR、task artifacts、code/tests建立 traceability。
11. 执行 targeted source/installed package tests、integration、representative clean throwaway、reapply/drift、projection、task、JSON/Python/shell与 diff checks；不执行专门 Release Issue的完整多平台矩阵。
12. 进入 Phase 2 semantic check、Task Commit、independent full-diff Branch Review。Architecture/RDT promotion仅在 review通过后串行执行；promotion diff再次运行 Phase 2/commit/review。

## 2. 需求—设计—验证映射

| Requirement | Design | Verification |
| --- | --- | --- |
| R435-01 | D435-01 | T435-01..04 |
| R435-02 | D435-02, D435-06 | T435-05..10 |
| R435-03 | D435-03, D435-07 | T435-11..16 |
| R435-04 | D435-04 | T435-17..22 |
| R435-05 | D435-05 | T435-23..28 |
| R435-06 | D435-04..05 | T435-29..33 |
| R435-07 | D435-08 | T435-34..39 |
| R435-08 | D435-09 | T435-40..45 |

## 3. 验证矩阵

| ID | 场景 | 客观通过条件 |
| --- | --- | --- |
| T435-01 | Review ready | current slice、remaining work、independent conditions、validation与Refs payload完整时只输出`ready` |
| T435-02 | Review planning gap | Delivery policy缺失/含糊只输出`planning_revision_required` |
| T435-03 | Review content finding | current slice finding只输出`implementation_required`，不得移入remaining work |
| T435-04 | Review stale | requirement/Architecture/RDT/base/Branch Review任一stale时零ready |
| T435-05 | First publish | exact reviewed HEAD push一次、创建唯一Draft PR、metadata exact、Ready一次 |
| T435-06 | Existing PR | 唯一same-repository strict-ancestor PR按合同接管，零第二PR |
| T435-07 | #405 equal head | bind前output loss恢复同一PR，零重复push/create/edit/Ready |
| T435-08 | Draft/Ready | Draft执行一次Ready；already-Ready零mutation |
| T435-09 | Publish drift | multiple/fork/terminal PR、head/base/body/scope drift在mutation前阻断 |
| T435-10 | Publish output loss | terminal live facts恢复同一`ready_for_merge` DTO |
| T435-11 | Merge preview | live expected head/base/checks/method/message/trailer current才展示一次merge action |
| T435-12 | Merge success | `--merge --match-head-commit --subject --body-file`一次成功，post-check exact |
| T435-13 | Merge result loss | read-only重建同一merge commit与`delivered`，零第二merge |
| T435-14 | Provider blocker | blocker解除后fresh gate继续；旧确认仅在plan identity不变时有效 |
| T435-15 | Refs only | PR body有`Refs #435`且无`Closes/Fixes/Resolves`；Issue merge后仍Open |
| T435-16 | No premature terminal | merge后task status仍active，零archive/closure/cleanup mutation |
| T435-17 | A/B first slice | A通过Planning/Check/Commit/Branch Review/Delivery，B明确remaining |
| T435-18 | B second slice | 同一task在A merge后追加B，创建新PR并产生第二Delivery result |
| T435-19 | Current slice defect | A内缺陷阻断Check/Branch Review/Delivery Review |
| T435-20 | Remaining disclosure | PR body与Delivery result不把B声明完成 |
| T435-21 | Task Commit | fresh sliced Check pass是唯一入口；零绕过或empty commit |
| T435-22 | Completion boundary | Delivery packages无completed/closure/archive/finish/cleanup exit或字段 |
| T435-23 | Trailer parse | exact三字段、version=1、stable task与reviewed head匹配 |
| T435-24 | Cross branch discovery | 删除旧remote branch并换current branch后仍发现两次历史Delivery |
| T435-25 | PR body mutation | merge后修改或不同PR正文不改变Delivery identity |
| T435-26 | Bookkeeping exclusion | 无Delivery trailer的Finish bookkeeping PR不进入历史集合 |
| T435-27 | Unsupported method | 仅支持squash/rebase时mutation前返回明确blocked |
| T435-28 | Identity drift | trailer/head/parents/repo/base/PR facts不一致时fail closed |
| T435-29 | Reactivate new binding | #436 fixture提供同task新branch/worktree后产生新Delivery |
| T435-30 | Old PR | historical merged PR不被重新打开、更新或追加 |
| T435-31 | Tracked move | archive->active与业务变更进入同一正常Delivery candidate |
| T435-32 | Validation-only Reactivate | 零业务diff时不调用Publish/Merge，不生成空Delivery |
| T435-33 | Old success | 上一轮Completion/Finish output不能进入本轮Merge或Cleanup |
| T435-34 | #407 conflict | candidate conflict返回implementation path并保持同一active task |
| T435-35 | Resolved candidate | exact MERGE_HEAD/stage-0 tree/digest/parents/fresh Phase 2通过后创建一个local merge commit |
| T435-36 | Resolved drift | HEAD/base/index/tree/message/checkpoint任一漂移时零commit |
| T435-37 | Git operation state | unresolved/unstaged/untracked/其它sequencer任一存在时零commit |
| T435-38 | Reconcile output loss | 只恢复同一merge commit，branch ref不再前进 |
| T435-39 | Downstream review | resolved merge进入完整Branch Review，不伪装base-only continuity |
| T435-40 | Additive graph | 三package完整注册/分发，但production workflow mandatory invokes/edges不变 |
| T435-41 | No adapter | 无old-output adapter、dual graph、ledger或PR-body identity reader |
| T435-42 | Projection parity | canonical/installed/Shared/Codex/Claude/Cursor package bytes与modes一致 |
| T435-43 | Preset reapply | representative clean install + reapply无未知`.new/.bak`与managed drift |
| T435-44 | Package closure | source/installed interface/schema/consumer/command/eval closure通过 |
| T435-45 | Repository checks | task validate、JSON、Python compile、shell syntax、ownership、dogfood drift、`git diff --check`通过 |

## 4. 计划命令族

写入前：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --root . \
  --task .trellis/tasks/09-18-435-active-task-delivery-loop --json
```

实现验证从每个 package 的 live `commands.json`、`interface.json` 与 tests解析。仓库级最小集合：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-18-435-active-task-delivery-loop
git diff --check
```

普通 #435 scope执行一个代表性 clean throwaway与reapply验证；完整多平台 clean/existing/update/workflow-switch/release-candidate matrix保留给专门 Release Issue。

## 5. Docs SSOT checkpoint

- strategy：`delta_first`；
- Phase 2前：task artifacts、RDT contribution、Architecture contribution/proposed ADR、canonical package/spec/docs与tests完整；
- Branch Review前：managed projections与installed manifest完整，production workflow未激活新edges；
- Review后：Architecture/RDT以expected `.54` serialized promotion，promotion-created diff fresh重跑下游gates；
- #434 boundary：只有#434能激活新图、退休旧edge和更新最终graph counts；
- #436 boundary：Completion/Closure/Finish/Reactivate实现与其完整E2E由#436拥有。

## 6. 风险与回滚点

- Merge trailer、merge method与Delivery discovery是一个合同单元，不能只实现parser或只修改message。
- Publish抽取不能保留Finalizer archive/finish side effect；发现共享runtime耦合时先拆纯deterministic primitive，再接两个清晰owner。
- Sliced-delivery适配不能弱化current candidate完整影响检查；只有satisfaction boundary按approved slice判定。
- #407 resolved-tree path必须绑定fresh Phase 2；不得新增通用dirty-worktree commit入口。
- Canonical/installed/platform与manifest必须同轮同步；sidecar与用户并行改动保持不动。
- 本Phase 1确认不授权`task.py start`、commit、push、PR、merge、release或cleanup。
