# #260 Trellis v0.6.15 兼容基线

## 目标

在 #266 已激活的 Requirements / Design / Test 双 SSOT 与 Architecture Baseline 上，把 Guru Team 的官方 Trellis 目标从 `0.6.5` 迁移到 `0.6.15`，并以 live manifest 派生的全平台业务仓库矩阵证明安装态、升级态、运行态、并行 Finish、acceptance 与 cleanup 合同保持完整。

GitHub Issue：https://github.com/castbox/guru-trellis/issues/260

## 当前权威与真实 before-state

- 当前 base、`origin/main` 与 live remote `main`：`5c059f4943edad7dfe25182a78af94759d41f9a1`。
- replacement release：annotated tag `v0.6.5-guru.10`，tag object `b5fd47e9dc45ca4d6950f87f38d495776ce676ce`，peeled commit `5c059f4943edad7dfe25182a78af94759d41f9a1`。
- 当前 canonical extension revision：`0.6.5-guru.36`；`target_trellis_cli`、`requires.trellis_cli` 与 `tested.trellis_cli` 仍绑定 `0.6.5`。
- Issue 正文中的 `v0.6.5-guru.9`、`56b5f411...` 与旧 extension revision 只保留历史语境；本任务的迁移输入以 `v0.6.5-guru.10` 和上述 live main 为准。
- 官方目标包：`@mindfoldhq/trellis@0.6.15`；`0.7.0-beta` 不进入本任务。
- 当前 live installed manifest 的平台集合为 `claude`、`codex`、`cursor`；执行矩阵前必须由 `.trellis/guru-team/extension.json`、`trellis/guru-team-extension.json`、`trellis/skills/guru-team/registry.json`、package interfaces、installed manifest 与 `trellis/presets/guru-team/ownership/upstream-ownership.json` 重新派生，禁止依赖本段静态枚举跳过新入口。
- #263 的 Requirements / Design / Test Skill、#264 的 Architecture Baseline Skill、#265 的 Bootstrap `new_repository` / `existing_repository` / `repair` profiles 与 #266 的 current authority 已进入 live main，构成迁移前合同。

## 第一性约束

1. 本任务证明升级兼容，不以删除 Guru 能力换取 Trellis `0.6.15` 运行成功。
2. canonical source 是长期源头；dogfood、installed package 与平台副本必须由 canonical source 同步并通过 drift 检查。
3. 兼容结论必须绑定 exact source HEAD、official Trellis 版本、平台 inventory、命令 route 与可复核结果。
4. GitHub Release、stable tag 和 #267 生命周期不属于本任务。
5. 业务并行验证只覆盖 honest normal path、普通失败恢复与 Issue 已列出的 provider / Finish / cleanup failure；锁、TOCTOU、压力竞态、攻击输入、生产变更不进入范围。

## 需求

### R260-01 版本与迁移合同

- 将 canonical manifest、dogfood manifest、installed manifest、README 版本矩阵和 verifier 绑定迁移到实际通过的 official Trellis `0.6.15`。
- existing 场景从 replacement release `v0.6.5-guru.10` 构建，先运行 official `trellis upgrade`，再运行 `trellis update --dry-run`。
- `trellis update --dry-run` 明确输出 `MIGRATION REQUIRED` 时执行 `trellis update --migrate`；未出现该文本时禁止执行 migrate。
- 更新后的 `target_trellis_cli`、`requires` 与 `tested` 只记录矩阵真实通过的版本。

### R260-02 live-manifest-derived 全平台 Throwaway 矩阵

对执行时派生出的每个声明平台创建隔离业务仓库，并覆盖两个独立场景：

| 场景 | Trellis 起点 | Guru 起点 | 必测路径 |
| --- | --- | --- | --- |
| clean | official `0.6.15` | 当前 #260 candidate exact HEAD | marketplace init、workflow install、preset initial apply、installed runtime |
| existing | official `0.6.5` + official migration route | `v0.6.5-guru.10` | upgrade、update dry-run、条件式 migrate、workflow preview/switch、preset reapply、installed runtime |

每个 repo 检查 `trellis/index.json`、workflow id/path/type、managed paths、hooks、skills、commands、prompts、schemas、scripts、executable mode、managed mode、`.trellis/.template-hashes.json`、`.new` / `.bak`、overlay sidecars、source/installed package identity与最终 recursive sidecar scan。每个场景使用独立临时目录，不读取本机隐藏安装状态。

### R260-03 dogfood 迁移

- 在当前 Guru dogfood repository 上执行 official `0.6.5 -> 0.6.15` upgrade/update route、workflow preview/switch、preset reapply、ownership 检查和 overlay drift 检查。
- 逐项审查 update 产生的 template hash、`.new`、`.bak` 和 local edit preservation 结果；未处理 sidecar 阻塞通过。
- canonical、dogfood、installed 与三平台副本的 package/interface/schema/exit/mode 必须一致。

### R260-04 完整 capability inventory 保留

迁移前后均从 live canonical inventory 生成机器可比投影，覆盖：

- active Skill ids、package interfaces、public input schemas、typed output schemas、private schemas、commands、consumers 与 workflow routes；
- task create/index/update/query、history discovery、finish summary/archive；
- semantic task/branch/worktree naming、`worktree` / `current` workspace modes、boundary validator 与 recovery；
- normal-scenario qualification、base sync/reconciliation、Planning approval、Phase 2、Branch Review；
- semantic commit、Docs SSOT Plan、`.trellis/spec` sync、Publication Review、push、PR、Ready、merge；
- provider recovery、acceptance、Finish、cleanup、preset/reapply、workflow preview/switch 与 multi-platform entry。

版本绑定、已审查 migration mapping 与 owner/route migration 之外的集合或语义差异一律阻塞。Skill、schema、typed exit、history/index/query、naming、Docs SSOT、Finish、cleanup 或平台入口缺失时，不得以测试通过替代能力保留结论。

### R260-05 installed contracts 与双 SSOT 权威保护

- 在每个平台的 clean 与 existing 场景中执行 #263、#264、#265 的 source/installed/package/platform contract smoke。
- 验证 Bootstrap 三个 profile 与 upstream `trellis-spec-bootstrap` ownership 未回退。
- 验证 `docs/requirements/**`、`docs/design/**`、`docs/test/**`、`docs/architecture/**` 未被 update 覆盖或删除。
- 验证 `.trellis/spec` 仍是双 SSOT 的概要/index projection，不形成第三正文权威。
- migration finding 若要求改变 #263/#264/#265 的 semantic contract，本任务停止该改动并返回原 owner；不得在 #260 内隐式重写。

### R260-06 两个独立 business task 场景

从同一 clean base 建立 A/B 两个独立 task：

- A 使用 `workspace_mode=worktree` 与 Finish entry `github_pr`，目标是后续单独确认的 dedicated disposable GitHub test repository；创建 repo、push、PR、merge 或 cleanup 前均展示 exact target/ref/action 并取得当前对话确认。未取得可用 test target 时 A 矩阵 fail closed，不以 provider mock 替代真实 PR 行为。
- B 使用 `workspace_mode=current` 与 Finish entry `none`，位于另一个隔离 clone，保证 current checkout 不与 A 共用 Git worktree registry。
- A/B 均完成 Intake、Planning、implementation、Check、semantic commit、独立 Branch Review、publication route、acceptance、Finish 与 cleanup 验证。
- A 的 route 只能创建和读取 A 的 PR；B 的 route 不创建 PR，也不读取 A 的 PR。
- A/B tracked diff 禁止出现 fixed handoff、`.trellis/workspace/**`、shared index、shared runtime cache 或跨 task metadata。
- Finish 不得修改 parent/child 或另一 task 的 `task.json`；archive 只移动 exact task-local path。
- A/B 不互相 merge bookkeeping commit；两种提交合并顺序均验证 Guru metadata path intersection 为空。
- Finish failure、provider failure 与 cleanup failure 只恢复原 task owner 的剩余 bookkeeping，不返回 Phase 0，不重建另一 task。
- cleanup 前验证 task、archive、reviewed-content、Finish/bookkeeping commit 的 retained ref 与 reachability；cleanup 后验证受保护 commit 仍可达。

### R260-07 当前 compatibility discovery finding

`.agents/skills/guru-discover-change-context/scripts/preview-change-context-history.sh` 当前缺失，而 canonical 与 installed package 内存在同名 wrapper。该事实不阻塞 Phase 1；实施矩阵必须依据 live interface 与 managed inventory完成一次归属判定：若 `.agents` public package 合同声明该 wrapper，则补齐 canonical projection 和全量分发检查；若合同未声明，则记录证明该路径不属于 public installed asset。禁止静默忽略。

### R260-08 最小下游合同

#260 完成时向 #248、#252 与 #267 提供一个最小、可确定性检查的兼容结论，字段仅含：

- exact source commit、verified Trellis/project version、installed workflow/preset identity；
- exact Finish entry profile、archive locator 规则、journal/workspace tracked-write 结论；
- bookkeeping commit ref 与 reachability 结论；
- A/B 结果、平台矩阵结果、未验证边界。

该结论不包含用户授权、完整命令日志、review 历史、本机绝对路径、mtime 或完整 hash bundle。

## Docs SSOT Plan

- `strategy`: `sync_required`。
- `authoritative_sources`: live Issue #260、#263/#264/#265/#266/#275 archive summaries、`docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md`、`docs/architecture/README.md`、current versioned docs、live manifest/inventory/interface 与 official Trellis 文档。
- `durable_update`: 通过 `guru-maintain-requirements-design-test-ssot:task_impact_sync` 与 `guru-maintain-architecture-baseline:task_impact_sync` 建立 task contribution，再由各自 `promotion` 更新 versioned current Requirements / Design / Test、Architecture current/evidence、四个 README locator 和最小 `.trellis/spec` projection。
- `durable_content`: 记录 official `0.6.15` 版本绑定、矩阵范围、能力清单迁移结果、installed contract 结果、A/B Finish/cleanup 结论、known gaps 与 #267 消费边界。
- `task_history_only`: 临时 repo locator、完整 stdout/stderr、命令逐行日志、owner-private checkpoint 与中间 hash 只存在运行期，不进入 durable docs。
- `merged_delta`: 合并前必须能从 versioned docs 与 manifest 直接判断 current main 已通过的 Trellis 版本、平台范围、能力保留状态和未验证边界。
- `release_boundary`: 本任务只建立 current-main compatibility authority；stable tag、GitHub Release、release notes 发布与 release smoke 由 #267 执行。

## 验收标准

- [x] AC-01：执行前 inventory 投影绑定 exact main/candidate HEAD、replacement tag、official package versions 与派生平台集合；执行后不存在 identity drift。
- [x] AC-02：每个派生平台的 clean 与 existing repo 均完成 R260-02 全路径，全部 mandatory check 为 PASS，最终 recursive `.new` / `.bak` 计数为 `0`。
- [x] AC-03：dogfood 完成 official upgrade/update、preview/switch、reapply、ownership 与 drift 检查；未处理 sidecar 计数为 `0`。
- [x] AC-04：迁移前后 capability projection 符合 R260-04；每个差异均属于版本绑定、已审查 migration mapping 或 owner/route migration。
- [x] AC-05：#263/#264/#265 installed contracts 在每个平台两类场景均 PASS；#266 docs 与 Architecture authority 未丢失，`.trellis/spec` 未成为第三正文权威。
- [x] AC-06：A/B 均完成各自生命周期；A route 只绑定 A PR，B route 的 PR 创建数为 `0`，两者不存在 shared tracked metadata path。
- [x] AC-07：A/B 两种 merge 顺序无 Guru metadata conflict；Finish/provider/cleanup failure 只恢复原 owner；cleanup 前后 retained ref/reachability 断言通过。
- [x] AC-08：R260-07 finding 已按 live interface 得出唯一归属结论，并纳入 source/installed/platform distribution check。
- [x] AC-09：Docs SSOT Plan 已完成 promotion，current docs、Architecture evidence、manifest 与最小 projection 语义一致。
- [ ] AC-10：Phase 2、独立 Branch Review、PR readiness、merge-head identity、Finish/archive/history/cleanup gate 均通过；PR 只关闭 #260。
- [x] AC-11：未创建 stable tag 或 GitHub Release，未开始 #267，未修改其它 Issue 正文，未创建 repair Issue。

## 非目标

- 不修改 Trellis upstream source、全局 npm 包或 `node_modules`。
- 不吸收 broad Phase-owner refactor、#248、#252、#247、#249、#250、#261 的实现。
- 不修改业务生产环境、数据、部署或组织级配置。
- 不把 guru-trellis source repository 的 canonical 集成冲突误判为已关闭 #53 的业务并行失败。
- 不新增锁、TOCTOU、压力竞态、攻击模型或 hostile-input 防御。

## 阻塞问题

无。live Issue、依赖 completion authority、current manifests、双 SSOT、Architecture Baseline 与 replacement release 已提供完整产品意图和范围。
