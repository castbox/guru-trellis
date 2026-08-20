# 技术设计

## 1. 设计目标

将 #260 实现为“冻结 before-state -> 迁移 canonical/dogfood -> 全平台业务仓库证明 -> 双 task 生命周期证明 -> SSOT promotion”的单一兼容闭环。所有版本、平台、路径和 public contract 从 live authority 派生；脚本只执行事实动作与客观检查，AI 保留 scope、finding、充分性、migration 语义和 gate 结论。

## 2. 边界与权威层

### 2.1 输入权威

1. Git/GitHub：live Issue #260、current branch base、remote main、replacement tag 与 predecessor archive summaries。
2. 版本与分发：两个 extension manifests、installed manifest、skill registry、package interfaces、upstream ownership manifest、marketplace index。
3. 产品/架构：Requirements -> Design -> Test -> Architecture current locators 与最小 `.trellis/spec` projection。
4. Official Trellis：`@mindfoldhq/trellis@0.6.5`、`@mindfoldhq/trellis@0.6.15` 和官方 upgrade/update/workflow marketplace 行为。

任一输入在矩阵开始前或 merge gate 前发生 identity drift，当前 evidence 失效并从该阶段重新派生，不继承旧摘要。

### 2.2 输出权威

- canonical extension source、preset、workflow、installer、verifier、tests 与 manifests 承载实现。
- dogfood 与 `.agents` / Claude / Codex / Cursor 副本是受管投影，不成为源头。
- versioned Requirements / Design / Test、Architecture current/evidence 与 README locators 承载 current-main 兼容结论。
- task-local planning/history 承载任务过程；下游只消费 R260-08 最小合同。

## 3. 迁移流水线

### 3.1 Freeze

构建 `before` inventory：

- source commit、replacement tag object/peeled commit、extension version、Trellis version；
- selected platforms、managed assets、overlay paths、file modes、template hashes、ownership classes；
- active skills、interfaces、commands、schema ids、typed exits、consumer routes；
- Requirements / Design / Test / Architecture identity 与 locator；
- Finish、archive、journal/workspace、cleanup 和 history/query capability。

投影使用排序后的结构化集合；完整扫描数据停留在临时目录，任务只保留人类可审查结论和下游直接消费字段。

### 3.2 Canonical migration

1. 在 canonical manifest 与 installer contract 中更新 official Trellis target。
2. 运行 upstream `0.6.15` 迁移行为探针，确认 upgrade/update 对 workflow、template hashes、managed files 与 local edits 的真实处理。
3. 针对发现的正常兼容缺口修改 canonical workflow/preset/overlay/package/runtime/tests。
4. 运行 preset apply 同步 dogfood 与所有平台投影。
5. 处理每个 `.new` / `.bak`，随后执行 recursive zero-sidecar check、ownership check、mode check 和 overlay drift check。

语义合同变化由 owner Skill 处理。若 finding 指向 #263/#264/#265 semantic contract，本任务不改该合同并返回原 owner；若 finding 只属于 version binding、installer、migration、projection 或 compatibility runtime，则由 #260 处理。

### 3.3 Matrix runner

矩阵维度为：

```text
live selected platform × {clean, existing} × {install, workflow, preset, runtime, inventory}
```

每个 cell 具有独立临时 Git repository、独立 npm cache 前缀、独立 Trellis home/config 与显式 source ref。runner 输出固定摘要：platform、scenario、source commit、before version、after version、command phase、exit、sidecar count、inventory comparison、installed smoke result。secret、本机用户配置与绝对临时路径不得进入摘要。

clean cell：official `0.6.15` init -> Guru workflow marketplace install -> preset initial apply -> installed smoke -> inventory compare。

existing cell：从 `v0.6.5-guru.10` 构建业务 repo -> official upgrade -> update dry-run -> 仅按 `MIGRATION REQUIRED` 分支执行 migrate -> workflow preview/switch -> preset reapply -> installed smoke -> inventory compare。

失败 cell 保留隔离临时 repo供当前调试阶段读取；结论生成后清除。一个 cell 失败不会复用另一 cell 的 runtime 或 evidence。

## 4. capability comparison

before/after 投影采用五组键：

1. `distribution`: managed paths、overlays、modes、hash ownership、platform routes。
2. `skill_api`: active ids、interfaces、commands、public inputs、typed outputs、consumers。
3. `workflow`: mandatory invocation、phase route、planning/check/review/publication/merge/finish/cleanup exits。
4. `task_data`: task/index/history/query/finish-summary/archive/journal/workspace contracts。
5. `docs_authority`: Requirements / Design / Test / Architecture locators、traceability、minimal spec projection。

比较器先给出 exact set diff，再由 AI 对每个差异分类：`version_binding`、`reviewed_migration_mapping`、`owner_route_migration`、`blocking_loss`。前三类必须绑定实施变更与验证；`blocking_loss` 阻塞 Phase 2。

## 5. dogfood 设计

dogfood 先以 clean primary checkout 验证 base，再在 #260 task branch执行受控迁移。official update 的 preview、实际动作与 preset reapply 分段执行，每段记录 pre/post Git diff、template hash 和 sidecar 结果。apply 后必须完成：

- canonical/package/source checks；
- installed package checks；
- upstream ownership check；
- managed Python routing check；
- dogfood overlay drift check；
- executable and managed mode check；
- recursive `.new` / `.bak` zero check。

发现 local edit preservation 结果不确定时停止后续写动作，审查 exact preimage、official output 与 sidecar，再选择迁移修复；禁止覆盖式清理。

## 6. A/B business lifecycle 设计

### 6.1 拓扑

- 生成一个 clean seed repository 和固定 base commit。
- 从 seed 创建两个 clone，隔离 Git worktree registry 与 runtime root。
- A clone 配置 `workspace_mode=worktree`，连接经单独副作用确认的 dedicated disposable GitHub test repository，执行真实 `github_pr` Finish entry。
- B clone 配置 `workspace_mode=current`，执行 `none` Finish entry。
- 两个 task 使用不同 issue/task/branch/worktree/archive locator，不读取 source repository 的 active task 状态。

### 6.2 生命周期断言

每个 task 执行 Phase 0、Planning、activation、implementation、Phase 2、semantic commit、independent Branch Review、publication、acceptance、Finish、archive 与 cleanup。fixture 业务改动限定在 task-local 独立文件，Guru metadata assertion 检查完整 tracked diff。

### 6.3 route 与失败隔离

- A 的 dedicated test remote 只接受 A branch 和 A PR identity；repo create、push、PR、merge 与 cleanup 分别受当前 workflow 的 exact side-effect confirmation 约束。缺少授权 target 时阻塞 A 场景，不降级成 mock 结论。
- B 的 `none` route 拒绝任何 PR read/create call。
- 在 Finish、provider、cleanup 三个明确注入点分别制造一次普通失败，再按 owner 提供的 typed recovery route 恢复。
- recovery 断言 task identity、phase resume target、remaining bookkeeping 与另一 task 的零读写。

### 6.4 commit reachability

对 A -> B 和 B -> A 两种合并顺序构造 commit topology，验证第二次合并无 Guru metadata conflict。cleanup 前记录 exact retained refs 和 `merge-base --is-ancestor` 结果；cleanup 后重跑 reachability，证明 task work、archive 与 Finish/bookkeeping commits 未被错误删除。

## 7. #263/#264/#265/#266 保护设计

每个 matrix cell 在 install/reapply 后运行：

- `guru-maintain-requirements-design-test-ssot` package discovery 与代表性 profile smoke；
- `guru-maintain-architecture-baseline` package discovery 与代表性 profile smoke；
- `guru-bootstrap-repository-ssot` 的 `new_repository`、`existing_repository`、`repair` profile smoke；
- upstream `trellis-spec-bootstrap` ownership、Guru orchestration boundary 与 source/installed/platform equality check；
- docs authority locator、traceability 和 `.trellis/spec` projection assertion。

smoke 使用受支持 normal scenario，semantic owner 产生判断，recorder/checker 只验证结构与 live facts。

## 8. compatibility finding route

对缺失的 `.agents/.../preview-change-context-history.sh` 先读取 interface、managed inventory、package install projection 和平台 adapter contract。归属判定只有两个结果：

- `declared_asset_missing`：在 canonical projection 补齐并纳入 source/installed/platform tests；
- `not_a_public_asset`：保留现状，并以 interface/inventory 证明 `.agents` 只提供 `invoke.sh` public entry。

该判定在 implementation discovery 完成，未得出结果时阻塞 Phase 2。

## 9. Docs SSOT 与版本 identity

RDT 与 Architecture owner 先执行 `task_impact_sync`。本迁移预期返回 `sync_required`，随后写 task contribution，并通过 `promotion` 形成新的 current-main version locator。locator 由 post-migration canonical extension version 与 current-main 状态构成；#267 后续将其映射到 stable release，不在本任务预建 tag identity。

`.trellis/spec/docs/requirements-design-test-ssot.md` 与 `.trellis/spec/architecture/baseline-usage.md` 只同步 current identity、locator、route 与 freshness 摘要，正文留在 versioned docs。

## 10. 失败、回滚与证据边界

- 修改前保存 Git diff 与 exact HEAD；回滚单位是当前 task branch 中的单个 migration step，不 reset 或覆盖用户并行改动。
- throwaway cell 失败通过删除该隔离 repo并从 frozen input 重建；不得把失败 repo当成下一 cell 起点。
- dogfood update 失败保留 worktree和 sidecar用于审查，修复 canonical 后重新从 clean candidate 运行完整 dogfood route。
- capability loss、authority drift、未处理 sidecar、platform cell failure、A/B cross-task write、unreachable bookkeeping commit 均阻塞通过。
- 完整 stdout、临时路径、owner-private gate evidence 不进入 Git；durable docs 只保存结论、identity、矩阵范围和未验证边界。

## 11. 权衡

- 每个平台使用两个独立 repo，执行成本高于共享 repo；该隔离直接证明平台与 clean/existing 状态不互相污染。
- B 使用独立 clone 的 `current` mode，避免与 A 共用 Git worktree registry，同时覆盖第二种受支持 workspace mode。
- #260 不发布 release，使 current-main compatibility 与 stable release mutation 分离；#267 必须重新验证 exact merged main 后再发布。
