# #187 修复 schema 2.0 Finalizer 迁移归档兼容性

## 目标

修复 schema 2.0 Finalizer 对迁移 active task 的归档兼容性，使已经完成语义审核、已有 Draft PR 的任务能够基于当前 Git index 和精确内容绑定继续同一条 closeout transaction，避免重复 PR 或重新进入 Branch Review。

## 权威来源

- 主需求：[castbox/guru-trellis#187](https://github.com/castbox/guru-trellis/issues/187)。
- Consumer 现场仅用于复现场景与验收边界：`castbox/guru_ai_roleplay#30`、Draft PR `#38`。
- 当前 Finalizer 合同：`trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`。
- 当前 deterministic engine：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。

## 当前缺陷

1. 已存在 schema 2.0 closeout plan 时，`build_closeout_plan` 沿用历史 `tracked_move_paths` 与 `untracked_archive_outputs`，不会根据当前 Git index 重新分类。
2. 迁移 task 中已 tracked 的 legacy `closeout-plan.json` 因而可能仍被列为 untracked output；`finish-summary.json` 才是真正的 untracked archive output。
3. 归档前连续性校验当前只接受 transaction-parent blob 或少量固定 `inputs` 内容，无法接受已经由当前 Finalizer 语义审核、但在 metadata tail 中更新的 tracked task artifact。
4. verification 网络 fallback 只把 untracked outputs 计入 plan-owned dirty set，导致已精确审核的 tracked metadata 被误判为超出 output set。
5. public wrapper 重新构造 checker 上下文时可能遮蔽 direct checker 已确认的 `blocked` / `evidence_ready` 状态，退化成 `owner_result_not_checked`。

## 功能需求

### R1 Git index 分类

- 每次准备或恢复 closeout plan 时，必须从当前 Git index 重新计算 task 内 `tracked_move_paths`。
- `untracked_archive_outputs` 必须由 `move_paths - tracked_move_paths` 推导，不复用历史失真分类。
- tracked legacy `closeout-plan.json` 在 plan、validation 和 archive transaction 中必须始终走 tracked 路径。

### R2 Reviewed tracked metadata 绑定

- 凡是偏离 transaction-parent blob 的 reviewed tracked task artifact，immutable plan 都必须保存其 task-relative path、Git mode 和当前内容 SHA-256。
- 绑定集合只能来自当前 task 的 tracked move paths 和当前工作树事实；任意未绑定内容变化继续 fail closed。
- 被最终裁剪的 metadata intermediate 也必须先经过同一精确绑定与连续性校验，再由既有 archive pruning 规则显式移除，不得静默忽略。

### R3 一致的直接 consumer

- pre-move continuity 使用精确绑定判断 reviewed tracked metadata 是否仍为 plan-reviewed bytes。
- verification fallback 的 expected dirty set 包含当前仍存在且匹配绑定的 tracked metadata，以及真实 untracked outputs 和 verification artifact。
- archive transaction 继续使用同一个 plan projection，不建立第二套 tracked/untracked 判定。

### R4 Finalizer 恢复语义

- 已有唯一 Draft PR 的迁移 task 从当前 Finalizer 恢复；复用该 Draft PR，不创建重复 PR。
- 恢复不要求重新执行 Branch Review；current reviewed-content identity 仍按既有规则验证。
- direct checker 和 public wrapper 对同一 checker-passed blocked/evidence-ready gate 输出一致的 `blocked` typed exit。
- 保留 `guru-finalize-task` 现有六个 public typed exits、consumer mapping 和 Interface 1.3 形态。

### R5 分发一致性

- canonical runtime、schema、Finalizer contract 和测试为修改源头。
- 通过 preset installer 同步 dogfood runtime、shared/Codex/Claude/Cursor Skill 副本。
- 不直接修改 Trellis 上游源码、全局 npm 包、`node_modules` 或 consumer repo。

## 范围外

- 恶意 artifact/hash/state 伪造或人为绕过流程。
- 并发 Finalizer、锁、TOCTOU、压力测试、跨 OS 原子性和额外 crash-consistency 加固。
- Finalizer 公共 API 重设计、新 typed exit 或无关 closeout 功能。
- 修改 `castbox/guru_ai_roleplay` 或其 Issue/PR 状态。

## 验收标准

- [ ] migrated active task 中 tracked legacy `closeout-plan.json` 被当前 Git index 归入 `tracked_move_paths`，不再出现在 `untracked_archive_outputs`。
- [ ] `finish-summary.json` 保持真实 untracked archive output 分类。
- [ ] 每个可变化的 reviewed tracked artifact 都有 path、mode、SHA-256 精确绑定；未绑定或内容/mode 漂移继续阻塞。
- [ ] dirty `prd.md`、`design.md`、`implement.md` 及可裁剪 metadata intermediate 可在绑定匹配时通过 pre-move continuity。
- [ ] verification 网络失败 fallback 不再把已绑定 tracked metadata 错判为超出 plan output set。
- [ ] direct checker 与 public wrapper 对 blocked/evidence-ready fixture 都输出 `blocked`，不出现 `owner_result_not_checked`。
- [ ] existing Draft PR resume 复用唯一 Draft PR、完成 archive 路径且不触发 Branch Review replay。
- [ ] migrated active task 回归覆盖 tracked legacy plan、dirty reviewed metadata tail、network fallback、existing Draft PR resume 四类场景。
- [ ] canonical/installed/platform package bytes 同步，dogfood drift 检查通过。
- [ ] clean throwaway 安装验证 marketplace、preset、Finalizer wrapper 和基础入口可运行；若环境限制未完成，最终报告明确列出缺口。

## 风险与约束

- 归档仍保持 fail closed；修复只接受 plan 精确绑定的正常 metadata tail。
- closeout plan 内容变化会改变 plan digest，迁移规范化必须由同一 Finalizer owner 显式识别并保持现有恢复路由，不得伪装为普通相同字节计划。
- 已有 Draft PR 的 repo/head/base/number/URL/Draft 唯一性验证保持不变。
