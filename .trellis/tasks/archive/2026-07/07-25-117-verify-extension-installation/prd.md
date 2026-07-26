# #117：实现 `guru-verify-extension-installation` 闭环 Skill

## 1. 目标

为 Guru Team extension 提供一个可独立调用、可被未来
`guru-finalize-task` 消费的 semantic closed-loop Skill：
`guru-verify-extension-installation`。

该 Skill 针对已推送的 remote ref，验证 workflow marketplace、preset、
overlay、installer、schema、公共 Skill contract 和平台入口能否按真实用户路径完成
clean install、update 与 preset reapply。最终路由由 AI 对适用性、验证 profile 和
adequacy 的审查结论决定；deterministic runtime 只执行命令、记录事实、校验
schema、identity 与 freshness。

## 2. 权威与交付边界

- 当前需求权威是 GitHub Issue #117 正文与
  `issuecomment-5045035361` 的 additive `accepted_current` 修订。
- 本 task 唯一 `close_issue` 是 #117。
- #115、#109、#116、#144、#146 仅提供前置合同或上下文。
- #81、#118、#119、#132 保持 follow-up；本 task 不实现、不关闭这些 Issue。
- #117 先拥有 #118 `verification_required` target 的 package-local input
  schema、example、fixture 与 public-wrapper eval；不激活 #118 producer edge。
- 本 task 不 push 分支、不创建 PR、不归档 task；这些副作用仍由后续 workflow
  阶段拥有。

## 3. 功能需求

### 3.1 Skill 与模式

- 新增 public Skill id `guru-verify-extension-installation`，状态为 `active`，
  `judgment_mode=semantic`，Interface 版本为 `1.3`。
- `workflow` 与 `standalone` 使用两个结构不同的 public input profile。
- Workflow seed 固定为 `task_ref`、`plan_ref`、`repo_ref`、
  `reviewed_head`、`verification_target`。
- Standalone input 明确携带 repository、remote、ref 与 caller intent；调用方不负责
  构造 verification profile、命令矩阵、remote facts 或 installed asset inventory。
- 无 task 的 standalone 调用只返回本次会话报告，不创建 repo-level cache、latest
  pointer、index 或 tracked artifact。

### 3.2 Semantic closed loop

- AI 读取 target、reviewed diff、extension contract、安装文档和当前 ownership
  inventory 后判断 applicability。
- AI 为本次变更选择一个确定的 verification profile，并说明该 profile 对本次变更面的
  覆盖关系。
- AI 在 executor 完成后审查命令事实、安装资产、redaction 与覆盖面，形成 adequacy、
  findings 和 route。
- `exit code 0`、空 findings 或 deterministic checker pass 均不得替代 semantic
  `verified` 结论。
- `marketplace_verification_required()` 的路径事实只能作为 AI 输入，不得继续拥有
  applicability 路由权。

### 3.3 Deterministic runtime

- Validator 校验 repo、remote、credentials-safe URL、ref、remote HEAD、reviewed
  HEAD、plan identity、task/worktree 和 invocation freshness。
- Executor 在临时 clean repo 中执行 marketplace index、new repo init、existing repo
  preview/switch、preset apply/reapply、Trellis update、managed ownership、
  `.new/.bak` 和平台分发检查。
- Recorder 将 AI 已完成的 applicability、profile、adequacy、findings 与 route，连同
  deterministic command facts、digests、sizes、asset inventory 和 remote identity
  写入唯一 private artifact。
- Checker 只校验 artifact schema、route 形状、remote/ref/HEAD binding、task binding、
  redaction、consumer mapping 与 freshness，不重新作 semantic 判断。
- Public wrapper 只从 checker-passed owner result 派生实际 `exit_id`，再按该 exit 的
  schema 输出最小 DTO。

### 3.4 Private evidence 与 public I/O

- `{TASK_DIR}/marketplace-verification.json` 是有 task 调用的唯一 task-local private
  evidence。
- Verification profile、适用性理由、adequacy、findings、command、exit code、
  stdout/stderr digest/size、installed asset digests、remote facts 与 temporary repo
  facts 全部保留在 owner-private evidence。
- 四个 public output 均以 `exit_id` 为 discriminator：
  `verified`、`not_required`、`return_to_task_work`、`blocked`。
- `verified` 只向 #118 传递 `task_ref`、`plan_ref`、`reviewed_head` 与 opaque
  `verification_ref`。
- `not_required` 只向 #118 传递 task/plan/HEAD identity；适用性理由留在 private
  evidence。
- `return_to_task_work` 向 `trellis-continue` 传递 task、finding refs 与确定的
  resume target。
- `blocked` 向 stop consumer 传递 stable reason code 与 remediation。
- #118 不解析 `marketplace-verification.json`。

### 3.5 安装、升级与 ownership 验证

- 真实验证必须从 remote ref 获取 source，不以当前 worktree 文件替代远端安装。
- 验证面固定包含：
  - `trellis/index.json` 中 `guru-team` workflow id/path/type；
  - new repo workflow init/install；
  - existing repo workflow preview/switch；
  - preset initial apply 与 reapply；
  - Skill package、registry、schema、config、scripts 和 executable modes；
  - Shared、Codex、Claude、Cursor 分发副本；
  - `trellis update` 后的保留、冲突与再次 apply；
  - `.new/.bak`、managed hashes、canonical/dogfood drift；
  - README 中公开安装命令。
- Ownership 检查必须证明 Trellis upstream Skill、Agent、Command、Prompt、Hook 与
  runtime agent 在 update/upgrade 后保持官方版本，preset reapply 只恢复 Guru
  assets。
- #132 关闭前，只接受 #128 inventory 已冻结的 `transitional_legacy` 集合；新增
  legacy owner 必须使验证失败。
- Production eval 与真实 remote-ref clean installation 是两个独立验收面，任一通过
  均不能替代另一验收面。

### 3.6 Retry、stale 与失败路由

- 相同 plan/ref/HEAD 下的 auth、network 或临时外部失败可重新进入完整 Skill。
- Task code/docs/tests 发生修复后，旧 verification evidence 立即 stale；必须重新完成
  publication review、closeout prepare、push 与 extension verification。
- Remote ref 或 HEAD 改变后不得复用旧 evidence。
- 安装失败、覆盖缺口或 task 内可修复 finding 返回 `return_to_task_work`。
- Auth、network、remote unavailable 或当前 task 外部依赖导致无法继续时返回
  `blocked`。
- Verifier 失败不得创建 PR、archive task 或产生第二个持久化 verification artifact。

### 3.7 Redaction

- Artifact、console summary、fixture、eval trace 和临时日志不得持久化 token、secret、
  private key、credential URL、signed URL 或敏感原始输出。
- Command evidence 只保留去敏后的 argv、exit code、digest 与 size；remote URL 在
  evidence 中使用安全 locator 或占位符。
- 测试 fixture 使用合成 repository、路径、SHA、token marker 与输出内容。

## 4. 非功能与兼容要求

- Markdown workflow、Skill 与 contract 负责流程和 AI 判断；Python/shell 只承担
  executor、recorder、validator。
- 不修改 Trellis upstream source、全局 npm 安装或 `node_modules`。
- Canonical source、dogfood installed copy、Shared/Codex/Claude/Cursor package copy
  必须 byte-identical。
- Public Skill id、schema id、exit id、target id 与 runtime command 是公共 API；本
  task 使用新增 id，不静默改变既有 Skill 的 public I/O。
- 不新增通用 CI framework、任意软件安装框架或 repository 自身 CI 的替代品。
- 不承担 Issue closure、PR readiness、Docs SSOT 充分性、finish summary 或 branch
  review 语义。
- 中台 SDK 知识门禁不适用：本 task 只修改 Guru Trellis extension workflow/runtime
  contract，不使用 `go-guru`、Unity Guru SDK 或 Flutter Guru SDK。

## 5. 明确排除

- #118 `guru-finalize-task` 的实现与 producer output。
- #119 finish family 的全局集成与完整 route activation。
- #132 的全部 legacy overlay 清理。
- Malicious actor、对抗性输入、故意伪造或篡改 artifact/hash/state。
- TOCTOU、锁、竞态压力、额外 fault injection、crash consistency 与跨 OS 原子性。
- 未经 exact proposal 专用确认的新验收场景。

## 6. 验收标准

- [ ] Source 和 installed registry 都把 `guru-verify-extension-installation` 识别为
      active Interface 1.3 semantic package，package discovery 无 drift。
- [ ] Workflow 与 standalone 两个 input profile 都有独立 schema、完整 example 和
      real-wrapper eval；profile 结构不互相兼容。
- [ ] `verification_required` target bootstrap 精确包含五个固定 seed 字段，且未激活
      #118 producer edge。
- [ ] 四个 `exit_id` 均有独立 output schema、完整 example、唯一 consumer 与
      checker-passed real-wrapper eval。
- [ ] Public DTO 不包含 verification profile、adequacy、command/log/digest inventory
      或 private artifact body。
- [ ] `marketplace-verification.json` 是 task 调用的唯一持久化 verification evidence；
      无 task standalone 调用后 repository tracked/ignored artifact inventory不新增
      verification cache/index。
- [ ] Applicability、profile 与 adequacy 由 AI-authored evidence 驱动；deterministic
      runtime 不以 changed-path 命中或 command exit code 决定 `verified`。
- [ ] Retry、stale、remote HEAD drift、task-fix re-entry 与四条 route 均有正常路径测试。
- [ ] Redaction 测试证明 secret marker 与 credential URL 不出现在 artifact、wrapper
      stdout、eval trace 和保留日志。
- [ ] Package-local production corpus 覆盖 workflow/standalone、applicability、四 exits、
      retry/unavailable；Shared/Codex/Claude/Cursor 使用 byte-identical corpus。
- [ ] 从真实 remote ref 执行 clean throwaway，new install、preview/switch、preset
      reapply、update、ownership、`.new/.bak` 与 README command 全部通过。
- [ ] `apply.sh --repo .` 后 dogfood 副本同步，`check-dogfood-overlay-drift.sh` 返回通过，
      且没有未处理的 `.new/.bak`。
- [ ] Canonical/installed package tests、runtime tests、manifest/schema validation、
      workflow graph validation 与 throwaway update/reapply regression 全部通过。

## 7. 文档状态

仓库已有 workflow、Skill package、companion script 与 durable requirements 文档，
但尚未定义 #117 semantic owner 和四出口合同，因此 docs state 为
`partial_docs`。唯一 Docs SSOT Plan 位于 `design.md` 的“Docs SSOT Plan”章节；本文件
只记录需求影响，不复制该计划。
