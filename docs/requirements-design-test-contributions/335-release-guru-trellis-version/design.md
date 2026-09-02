# #335 Repository-private release orchestration Design contribution

## Private Skill boundary

- `D335-01`：`.agents/skills/release-guru-trellis-version/` 是仓库私有语义定义；Codex、Claude、
  Cursor 目录保存 Agent 可发现且与共享定义一致的 project-local projection。Skill 不声明公共
  `interface.json`、schema、runtime、typed exit 或 installer inventory。
- `D335-02`：Skill 使用 Markdown 定义 release-specific preflight、stage classification、owner
  composition、freshness route 和副作用边界；确定性 Git/GitHub mutation 仍由既有 owner 与工具
  执行，不新增 tracked 状态机或 companion script 代替 AI 判断。
- `D335-03`：invocation-local identity 聚合六项最小输入与 fresh live facts。缺失、歧义或不一致
  只产生 fail-closed stop；恢复时重新读取 live authority，并只消费仍满足既有 freshness 合同的
  owner-private checkpoint。

## Two-stage composition

- `D335-04`：preparation 按 standard intake 建立稳定 planning，随后依次调用现有 Phase 2、Task
  Commit、Branch Review、Publication、Finalizer 与 Merge owners。每个 owner 独占自身判断、
  typed exits、recorder/validator、确认和副作用。
- `D335-05`：最终 delivery content commit 后只执行一次覆盖完整 `origin/<base>...HEAD` 的独立
  Branch Review。Publication 和 Finalizer 只消费其现有最小 handoff；允许的 lifecycle-only
  metadata 不回写 delivery content，因此不触发第二次完整 Review。
- `D335-06`：merge 后重新 fetch `origin/main`，从 live merge/base facts 建立 invocation-local exact
  candidate。preparation branch identity、旧 gates 和旧 release evidence 不作为 candidate authority，
  cross-SHA 或 lineage gap 直接停止。
- `D335-07`：post-merge gate 将 Issue 要求的最小 release checks 绑定同一 candidate，并明确把完整
  累计多平台矩阵留给专门 Release Gate owner。任一 required check 为 FAIL、SKIP 或 stale 时不得
  进入 mutation。

## Payload, freshness and side effects

- `D335-08`：Publication 在 PR 动作前即时生成并审查 PR payload；Release boundary 在 GitHub
  Release 动作前即时生成并审查 Release payload。payload 只存在于当前 owner handoff 或调用，
  不写 task-local release notes/body/status 文件。
- `D335-09`：reviewed-content classification 包含实际交付、Skill、durable docs、配置、schema、
  scripts 和 tests；这些 bytes 变化使相关 gates stale。既有 allowlist 内 owner-private checkpoint
  与 lifecycle metadata 不进入该 identity，consumer 完成后按 owner 合同退休。
- `D335-10`：merge、tag、tag-pinned smoke、GitHub Release、Issue closure 与 cleanup 是独立
  confirmation transactions。Skill 只路由到下一动作，不保存授权、阶段或动作结果；unsupported
  exit 没有 fallback。
- `D335-11`：contract tests 校验四投影 parity、public inventory 零泄漏、forbidden tracked artifact
  为零、独立确认和 fail-closed wording；honest-path fixture 证明稳定计划到 Finalizer 的单次 Review
  路径，以及 delivery drift 与 lifecycle metadata 的不同 freshness 结果。
- `D335-12`：RDT 与 Architecture 仅写 task-owned contribution；shared current 是否 promotion 由
  `guru-maintain-requirements-design-test-ssot` 与 `guru-maintain-architecture-baseline` 串行决定，
  本 contribution 不拥有 promotion 或 current 声明。
