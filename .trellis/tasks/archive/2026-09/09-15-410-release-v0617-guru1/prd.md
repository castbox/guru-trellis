# #410 发布 v0.6.17-guru.1 并提升 Guru Team extension 至 0.6.17-guru.42

## 目标与价值

按仓库私有的两阶段 Release Contract，基于 Issue #410 交付一个可追溯、可复现、可回滚的 Guru Trellis 正式版本。发布结果必须区分仓库发布 tag、Guru Team extension revision、官方 Trellis CLI/core 版本和 framework source lock。

## 已确认事实

- 仓库：`castbox/guru-trellis`；Issue：[#410](https://github.com/castbox/guru-trellis/issues/410)，为本次发布的唯一外部工作项。
- 基线：`main` 与 `origin/main` 一致，当前基线 HEAD 为 `0cedf4fb80fa80f8540652cab464454605ee122e`。
- 目标版本轴：仓库 tag/Release `v0.6.17-guru.1`；Guru Team extension `0.6.17-guru.42`；官方 Trellis CLI/core 保持 `0.6.17`。
- 前序版本轴：仓库 tag/Release `v0.6.16-guru.1`；Guru Team extension `0.6.16-guru.41`。
- 当前任务隔离在 branch `chore/410-release-v0617-guru1`、worktree `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/410-release-v0617-guru1`，task ref 为 `410-release-v0617-guru1`。
- 发布 Skill 是仓库私有编排，不进入 Guru Team 公共 Skill registry、extension manifest、preset、marketplace 或业务仓库安装包。

## 需求

### R410-01 两阶段发布生命周期

Stage 1 必须经过 planning、前置交付变更、第一次 Phase 2、task commit、完整独立 Branch Review；随后串行完成 Architecture/RDT promotion，并对 promotion 产生的 diff 重新执行 Phase 2、task commit 和完整 Branch Review。只有第二次 Branch Review 通过后，才进入 Publication、Finalizer 和 preparation PR。Stage 1 PR 使用 `Refs #410`，不得提前关闭 Issue。

Stage 2 必须在 preparation PR 合并后从 fresh `origin/main` 冻结唯一 exact candidate commit/tree；丢弃 Stage 1 的发布证据，不以 preparation branch HEAD 代替 candidate。所有 release gate、tag、tag-pinned smoke、GitHub Release 和 Issue close 都绑定同一 candidate。

### R410-02 版本与文档一致性

候选 commit 中的 manifest、根 README、workflow README、preset README 和 Docs SSOT 必须一致表达四条版本轴，并明确当前 source lock、CLI/core、extension revision 与历史 stable release 的关系。不得创建 task-local release notes、PR/Release body handoff 或动态发布 checklist。

### R410-03 目标候选验证

在 tag mutation 前，针对 `v0.6.16-guru.1` 到 exact candidate 的完整 diff 执行 Issue 规定的 lineage、版本映射、source/installed validator、Shared/Codex/Claude/Cursor parity、ownership/preset/dogfood drift、focused install/update/reapply、secret scan 和 residue/diff hygiene gate。任一 `FAIL`、`SKIP`、候选跨 SHA、身份不匹配或未能解释的 sidecar 都必须 fail closed。

### R410-04 发布与关闭边界

准备 PR 合并、annotated tag 创建/推送、tag-pinned smoke、GitHub Release 创建、Issue 关闭、branch/worktree/task cleanup 均是独立副作用边界，分别展示精确目标和 live facts，并取得当前对话中的独立确认。任何一次确认不得预授权或复用到其它动作。

## 验收标准

1. Stage 1 的 planning、两次 Phase 2/task commit、两次完整 Branch Review、Architecture/RDT promotion、Publication、Finalizer、preparation PR merge 均由对应 owner 完成，且新鲜证据没有 P0-P3 finding；PR 为 reference-only 并使用 `Refs #410`。
2. Stage 2 只使用从 fresh `origin/main` 得到的一个 exact candidate；前序 tag 可证明是 candidate 的祖先，候选树、diff、validator 输出和后续 tag target 全部绑定该 candidate。
3. 候选的四条版本轴、public release text、source lock、生成的 installed projection 和四平台 Skill package parity 通过当前合同；preset reapply 不产生未解释的内容、`.new` 或 `.bak`。
4. focused throwaway install/update/reapply 与 source/installed/ownership/drift 检查完成并可复现；本 Issue 不冒充专门 Release Gate Issue 所拥有的完整累计多平台 matrix。
5. tag、smoke、GitHub Release 和 Issue close 的 live GitHub 结果逐项核验；最终报告分开说明代码/测试、静态证据、live GitHub 证据和未验证边界。
6. 任何发布失败都保留可定位的失败事实，并按合同停止，不通过替换 ref、全局 CLI、mutable latest、重写历史或 metadata commit 绕过。

## 明确排除

- 不在本 Issue 内执行完整累计多平台 Throwaway installer Release Gate matrix；其结果由专门 owner 承担。
- 不修改 Trellis 上游源码、全局 npm 包、`node_modules` 或业务仓库。
- 不新增 release status artifact、恢复 Skill、公共 schema/exit、task-local release notes 或动态 checklist。
- 不把 Issue 关闭、tag/Release 成功、远端发布成功或真实业务仓库安装成功从静态检查推断出来。

## 未决项

没有阻塞规划的用户决策。具体变更文件、Docs SSOT contribution 路径和每个 owner 的输入/出口由 `design.md` 与 `implement.md` 固化；实际 live GitHub mutation 仍需在对应边界逐项确认。
