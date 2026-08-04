# #174 修复 #132 合并候选的 thin workflow 420 行预算并补齐 current-HEAD 回归

## 1. 目标

在创建任务时绑定的 `main` current HEAD 上，修复 Guru Team thin workflow 超出既有
420 行预算的问题，并证明本次压缩没有改变 #132/#161 已确定的公共 workflow graph。

## 2. 权威与基线

- Live Issue：<https://github.com/castbox/guru-trellis/issues/174>
- 任务基线：`main` / `origin/main`，HEAD `ecb2e918627dd3513976dd1dd52d9af461375c9d`。
- 实现目标：`trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`。
- 当前事实：两份 workflow 字节一致但各为 427 行；两个现有回归断言均要求不超过
  420 行。
- Issue 创建证据中记录的 README 基线失败、#132 历史 combined acceptance 以及此前
  未提交压缩尝试不属于本任务的新验收证明。

## 3. 范围

### 3.1 In scope

1. 从当前 canonical workflow 独立删减 7 行或更多，使 canonical 与 dogfood copy 均不超过
   420 行。
2. 只压缩重复的全局说明、边界说明或 Markdown 排版；保留 global workflow 必须拥有的
   phase/status route、mandatory invocation、typed exits、唯一 consumer、28 targets、
   stop graph、human artifact、Docs SSOT、Issue Scope Ledger、interaction 与
   platform-ownership 边界。
3. 保持两份 workflow 字节一致，并验证 `get_context.py` 的 phase parser 仍能读取
   Phase Index 与实现、检查、Branch Review、Finish 入口。
4. 在 current HEAD 重跑 runtime workflow suite、aggregate Skill package suite、
   source/installed graph、ownership、dogfood drift、managed installation/update/reapply
   和 `git diff --check`。
5. 对完整 current-HEAD diff 做独立语义 review；报告 P0-P3 findings、未覆盖边界以及
   本 Issue 新验证与 #132 历史验证的区别。

### 3.2 Out of scope

- 不放宽、删除或改写任何 420 行预算 assertion。
- 不修改 Skill package、interface/schema、companion runtime、preset installer、
  upstream-owned overlay、平台入口、Trellis upstream、全局 npm 或 `node_modules`。
- 不重新实施 #132 的 installer、ownership、platform discovery 或 combined acceptance。
- 不实现 #108、#106、#81，也不关闭 #132 或其它 Issue。
- 不处理恶意 actor、对抗输入、竞态、锁、TOCTOU、额外 fault injection、跨 OS
  crash-consistency 或其它 Issue 未要求的非正常路径。

## 4. 功能要求

- R1：canonical 与 dogfood workflow 字节一致，且各自 `splitlines()` 数量 `<= 420`。
- R2：13 个 active Skill invocation、51 个 exit、28 个 workflow/stop target、每个
  exit 的唯一 consumer 以及 fail-closed 规则与当前 graph 完全一致。
- R3：#161 stale re-entry public contract、Phase 1 activation、Phase 2 check、Branch
  Review、Publication/Finalization 的 global boundary 不因压缩而回归为 step-local 实现。
- R4：当前 workflow 仍可被 Trellis parser 读取；canonical/dogfood、source/installed
  package 和 managed install 结果没有漂移或 unresolved `.new`/`.bak`。
- R5：验证输出必须区分本 Issue 重新执行的 current-HEAD 证据、README 基线失败和
  #132 已有历史 acceptance，不得用历史结果替代本 Issue 验证。

## 5. 验收标准

- [ ] canonical 与 dogfood workflow 字节一致且不超过 420 行。
- [ ] 两个 line-budget regression 与完整 aggregate Skill package suite 通过；任何
      README 基线失败单独记录，不改变本 Issue 结论。
- [ ] 13 Skills、51 exits、28 targets、mandatory invocation、唯一 consumer 与 stop
      graph 保持一致。
- [ ] Phase parser、source/installed graph、ownership、dogfood drift、managed install
      与 update/reapply checks 通过。
- [ ] `git diff --check` 通过，且无超出本任务范围的产品、测试或 preset 改动。
- [ ] 独立 current-HEAD semantic review 无未关闭 P0-P3 finding。
- [ ] PR/最终说明只关闭 #174，并诚实区分新验证与 #132 历史 combined acceptance。

## 6. 变更授权边界

当前确认只覆盖规划、实现和验证。commit、push、PR、Issue close、archive、cleanup
或其它外部副作用必须在各自动作前重新获得明确授权。
