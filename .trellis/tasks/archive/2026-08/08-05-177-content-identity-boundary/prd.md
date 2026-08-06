# #177 隔离 reviewed content identity 与 task/publication metadata

## 1. Authority 与目标

- Live authority：<https://github.com/castbox/guru-trellis/issues/177>。
- Breaking scope authority：<https://github.com/castbox/guru-trellis/issues/177#issuecomment-5189559933>。
- 已完成前置：Issue #174。
- 独立后续：Issue #180，不进入本 task。
- 目标：使用一个可重复计算的 reviewed-content identity 区分交付内容与 task、publication、finalization metadata，使 metadata 变化不再令 Phase 2、Branch Review 或内容验证 stale。

## 2. Reviewed Content 定义

### 2.1 纳入内容

除第 2.2 节固定排除路径外，当前仓库中的 Git tracked 文件、当前 worktree 的未提交修改、删除和非 ignored 新文件均属于 reviewed content。该集合覆盖：

- 实现与测试；
- `.trellis/spec/**`、README、workflow 文档和 durable engineering docs；
- canonical workflow、Skill、preset、overlay、schema、companion script；
- dogfood 与受支持平台的已安装交付副本；
- 影响安装、更新、升级行为的仓库文件。

### 2.2 排除内容

以下路径只承载任务运行态、任务归档或本机状态，不属于 reviewed content：

- `.trellis/tasks/**`；
- `.trellis/workspace/**`；
- `.trellis/.runtime/**`；
- 已有 AI-first OS noise 分类器识别的文件。

排除规则按完整仓库相对路径判定，不使用提交消息、作者、时间或可扩张 basename allowlist 推断。

### 2.3 Identity 合同

- 算法 id 固定为 `guru-reviewed-content-1.0`。
- 输入是 `HEAD` 完整 tree，并叠加当前 worktree 的修改、删除、重命名、复制和非 ignored 新文件。
- 每个纳入条目绑定仓库相对路径、Git mode 和 Git object id；条目按 UTF-8 path 排序后进行 canonical JSON SHA-256。
- 同一内容在未提交、提交后和 metadata-only descendant 三种状态下产生相同 identity。
- 纳入路径的内容、mode、路径、删除状态或 gitlink HEAD 改变时 identity 必须改变。
- Git 状态、对象、symlink、gitlink 或路径无法确定时 fail closed。

## 3. 功能需求

### R1. Phase 2 freshness

- `guru-check-task` 私有 checkpoint 记录 `reviewed_content_sha256`。
- Phase 2 checker 重新计算 identity，不再要求 commit anchor 与当前 HEAD 完全一致才能判定内容 fresh。
- private checkpoint 使用新的 current-only schema 和 `phase2_capture_commit`；不保留 `checked_head` 字段或旧 schema reader。
- 当前 dirty reviewed-content 路径仍须完全包含在 AI 的 `reviewed_paths` 中。
- 仅 task/runtime metadata 改变时 checkpoint 保持 fresh；任一 reviewed-content 改变时返回 stale。

### R2. Task Commit 承接

- `guru-check-task` passed DTO 与 `guru-create-task-commit` input 使用新的 public schema 和 `phase2_commit_anchor`，只承担当前流程的 Git ancestry/capture 定位。
- Phase 2 checkpoint、当前 worktree identity 和当前 commit parent 均须在执行前重读。
- `phase2_commit_anchor` 到当前 HEAD 之间只有排除路径变化时，commit 仍以当前 HEAD 为 parent；reviewed-content 漂移时 fail closed。

### R3. Branch Review freshness

- `guru-review-branch` 私有 gate 使用新的 current-only schema，记录 `reviewed_content_sha256` 和 `review_commit`。
- 完整 review range 仍为 `origin/<base>...<reviewed commit>`。
- 后续 freshness 只使用统一 identity 比较；删除 metadata descendant allowlist 及其分支。
- finding 的 Git ancestry 仍使用真实 commit anchor，不使用内容 digest 替代 Git 因果关系。

### R4. Publication 与 Finalizer freshness

- Publication 每次进入时从 Branch Review `passed` DTO 消费
  `branch_review_commit`，重算当前 reviewed-content identity，并校验 live content
  continuity；不得读取、解释或删除 Branch Review 私有 gate。
- Finalizer 初次进入时消费 Publication `ready` DTO 的
  `branch_review_commit`，re-entry/recovery 时消费 immutable existing plan 中的同一
  anchor；每次都重算当前 reviewed-content identity，不得读取 Branch Review 私有
  gate。无 DTO 且无 plan 时 fail closed。
- Branch Review、Publication 与 Finalizer 的 public input/output 使用新的 schema 和 `branch_review_commit`；该字段只承担当前流程的 Git ancestry、review range 和 remote verification 定位，不是 freshness authority。
- task/publication/finalization metadata 写入或提交不得触发完整 Phase 2 或 Branch Review 重跑。
- reviewed-content 改变必须返回现有 task-work 或 stale 路由并 fail closed。

### R5. Scope-only Ledger

- 新写入的 `issue-scope-ledger.json` 使用 schema `2.0`。
- 顶层只保留 `schema_version`、`primary_issue`、`close_issues`、`related_issues`、`followup_issues`。
- issue entry 只保留 `number`、`url`、`title`、`reason`。
- Ledger 禁止 `acceptance_evidence`、`verification`、proposal digest、GitHub comment checksum、review metadata、process metadata 和 rules 文本。
- loader、writer、schema、example、eval 与测试只接受 schema `2.0`；不保留 schema `1.0` 投影、迁移或专用 re-entry。

### R6. Verification ownership

- Marketplace 机器验证只写 `marketplace-verification.json` 及 owner-private verification result。
- Finalizer 不再向 Ledger 注入 pending 或 passed verification evidence。
- 发布校验分别读取 scope Ledger、Phase 2/Branch Review/Publication gate 和 marketplace verification artifact；不得用 Ledger 中的复合 evidence 替代这些 owner。

### R7. Canonical 与分发一致性

- canonical runtime、Skill package、schema、example、eval、workflow docs 和 preset source 同步修改。
- 受影响合同只保留 current schema/id/field；Skill、workflow、preset/overlay、脚本、文档和测试不得保留旧 reader、projection、re-entry、allowlist、alias、fixture 或 compatibility 文案。
- 通过 preset installer 生成 dogfood 与平台副本，不把生成副本作为唯一源头。
- 安装后 source/installed package closure、overlay drift 和支持平台语义保持一致。

### R8. 正常路径边界

- 覆盖正常 honest-but-fallible 路径、普通 stale/mismatch、遗漏和实现错误。
- 不增加恶意篡改、对抗输入、竞态压力、锁、TOCTOU、fault injection、crash consistency 或跨 OS 原子性机制。

## 4. Acceptance Criteria

- [ ] `guru-reviewed-content-1.0` 在 canonical runtime 中只有一个实现和一组固定 metadata path 规则。
- [ ] 未提交 reviewed content、提交后的相同内容和 metadata-only descendant 产生同一 identity。
- [ ] 修改实现、测试、durable docs、workflow、Skill、preset、overlay、schema 或 script 后 identity 改变。
- [ ] Phase 2 在 metadata-only HEAD/status 变化后保持 fresh，在 reviewed-content 变化后 stale。
- [ ] Branch Review 在 metadata-only commit 后保持 fresh，在 reviewed-content commit 或 dirty change 后 stale。
- [ ] Branch Review `passed` wrapper 删除自己的 checkpoint 后，Publication/Finalizer
  仍只凭最小 DTO、immutable plan 与 live facts 在 metadata tail 后继续工作；
  reviewed-content drift 仍 fail closed。
- [ ] 新 Ledger 符合 scope-only schema 2.0，且不包含 verification 或 process 字段。
- [ ] Marketplace verification 不再修改 Ledger。
- [ ] 受影响 public/private contract 使用新的 current-only schema/id/field，旧 artifact 直接按无效输入 fail closed，仓库中不存在其 reader、projection、re-entry、allowlist、alias、fixture、eval 或专用测试。
- [ ] `checked_head`、`reviewed_content_head`、旧 Phase 2/Branch Review schema 和 Ledger 1.0 不再出现在本次受影响的 active Skill、workflow、preset、脚本、schema、example、eval 或测试合同中。
- [ ] canonical、dogfood、preset/overlay、schema、example、eval、README 与 durable spec 一致。
- [ ] targeted unit、package contract、finish-family integration、dogfood drift、clean throwaway install、update/reapply 与平台入口验证通过。
- [ ] 当前完整 diff 的独立 semantic review 无未关闭 P0-P3 finding。

## 5. 非目标

- 不删除或重构完整 `context-discovery.json` 生命周期。
- 不压缩 Finalizer transaction、PR merge/ready 流程或用户确认次数；这些由 Issue #180 负责。
- 不修改 Trellis upstream、全局 npm 或 `node_modules`。
- 不为本 task 制造 handoff 或 metadata-only commit。
