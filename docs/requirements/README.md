# Guru Team Trellis Extensions

本目录说明本仓库已经建设的 `guru-team` Trellis 扩展能力。

这些文档不是通用产品需求模板，也不绑定 Codex、Claude、Cursor 或任何单一 AI coding
harness。它们用于回答一个问题：Guru Team 已经在官方 Trellis 之上扩展了什么能力，
这些能力如何分类、哪些最关键、哪些是安装与维护支撑。

## 文档

| 文档 | 内容 |
| --- | --- |
| [requirement-main.md](./requirement-main.md) | 基于本 repo 全量 issue / PR 历史整理的已实现 Trellis 扩展总览。 |
| [guru-team-trellis-flow.md](./guru-team-trellis-flow.md) | 面向演示的 Guru Team Trellis 全流程图：从 Codex prompt hook 触发 pre-task intake 到 `trellis-finish-work` closeout，并用颜色区分官方 Trellis 原生机制、Guru Team 扩展、平台入口和 companion scripts。 |

## 历史扫描范围

本轮整理已扫描 `castbox/guru-trellis` 的 GitHub issue 和 PR 历史，包括 closed / merged
记录：

- Issues：15 个，全部 closed。
- PRs：15 个，其中 14 个 merged，1 个 closed 未合并。
- Comments / reviews：基本没有额外决策；issue #6 有 `closed by #9` 补充，PR review
  comments 为空。主要产品决策和验收信息来自 issue body 与 PR body。
- 后续维护补充：active issue #51 已沉淀为 `prepare-task` 命名质量门禁能力，#60
  已沉淀为 workspace boundary 事实层与 task artifact 写入边界；#76 正在沉淀为
  sub-agent liveness、status request、stale cutover 与 completed-only recovery
  gate。合并后应随对应 PR 更新到历史索引。

## 扩展重要性分层

| 层级 | 类别 | 历史来源 | 说明 |
| --- | --- | --- | --- |
| P0 | Workflow 主合同与日常入口 | #1, #2, #57, #64, #65, #66, #78 | `guru-team` marketplace workflow 定义 Phase 0-3、auto-bootstrap 日常入口、业务项目中文文档默认规则、知识门禁和 Docs SSOT；Phase 1 规划策略、Phase 2 执行/检查、Phase 3 final review 只验证不补救、finish-work 不首次 merge docs；Branch Review `reviews/*.md` / `review.md` 也继承中文 human-readable artifact 规则。 |
| P0 | Intake / base sync / worktree / no_task / workspace boundary 副作用边界 | #6, #15, #26, #51, #60, #96, #110 | repo-changing intake 在任何 issue、Docs、代码、测试或历史语义读取前 mandatory invoke `guru-sync-base`；caller-side AI 只做 tool-free route classification，deterministic Skill 直接执行 digest-bound fetch / ff-only，并以 decision checkout、local base、remote base 三方 SHA equality 放行，不增加 selected-base 或 post-execution AI Gate。之后创建 issue、worktree、branch、task 或当前 checkout 直改仍必须有 AI/human handoff、用户授权和语义命名门禁；tracked `task-start-context.json` 只保存 portable workspace identifiers，worktree mode 下 task artifact / review artifact 写入前必须通过当前 checkout、`.trellis/.runtime/guru-team/**`、`git worktree list` 与 `check-workspace-boundary.sh --task` 推导并校验 actual repo root。 |
| P0 | Planning / check / task work commit / Branch Review Gate 证据链 | #5, #8, #20, #44, #62, #72, #76, #78, #122, #125 | planning、phase2 check、`guru-create-task-commit`、独立 review、中文 raw/rollup review report、review report digest、任意 finding 阻断、fresh 最终放行审查、sub-agent liveness / status request / stale cutover / completed-only recovery chain 和 schema 1.2 append-only provenance correction/recovery link 形成可审计链路；task work commit 由可重复进入的公共 closed-loop skill 绑定 exact paths、统一消息 parser、普通 Git operation state、ordinary SHA-256/mode/delete、gitlink worktree HEAD/OID 与 candidate deterministic bytes，在 isolated index/detached HEAD 上执行 hook/commit；snapshot 以 `renamed_from` / `copied_from` 显式区分 rename 与 copy，只有 rename source 继承 destination 的删除/exact-stage authority，copy source 绝不因关系自动入 stage，若自身 dirty 则必须独立分类；真实 `index.lock` 作为 sentinel 持有到 transaction 结束，独立 final-index temp 在 sentinel 下发布，最终 candidate identity read 是线性化点，read 前并发 C 触发 ref/index rollback 并保留 C，read 后 C 作为 later operation 保留且 commit blob/result digest 仍为 committed authority；`workflow` 与 `standalone` 只区分 global routing 与 direct discovery，两者都依赖完整 Guru Team runtime，package wrapper 统一经 `run-skill-command` fail closed；默认 sub-agent mode 下 implement、check、Branch Review 都必须有真实 sub-agent evidence。 |
| P0 | Finish / publish / PR readiness | #7, #17, #18, #27, #66 | PR 发布只能在 finish-work 后发生，且必须有 AI 审查过的 reviewer-facing body 与 readiness evidence；PR body 必须说明 Docs SSOT / 文档同步处理结果。 |
| P1 | Preset installer 与平台 overlay | #9, #11 | preset 安装 companion assets 与平台入口，支持 overlay 选择，并保持 canonical / dogfood 同步。 |
| P1 | 安装、升级、开箱验证 | #10, #27 | README 非交互安装、throwaway install、dry-run readiness 和 Codex 默认 sub-agent 让新项目可开箱使用。 |
| P2 | Docs / spec / knowledge 协同 | #1, #9, #10, #57 | task artifact、durable docs、`.trellis/spec/`、中台知识引用、业务项目中文语言规则和公开安装文档协同。 |

## Canonical Source

公共 closed-loop workflow skill 的唯一 canonical root 是
`trellis/skills/guru-team/`。其中 registry 区分只占用 id、不可安装和路由的
`reserved`，以及具备完整 package/interface/schema/validator/test/route
证据的 `active`。workflow marketplace 只安装 `.trellis/workflow.md`；完整
extension 必须再应用 Guru Team preset，由 preset 安装 audited runtime copy、
selected platform discovery copy 和逐文件 managed-hash provenance。

Active package 的 `SKILL.md` frontmatter 只允许 stable id `name` 与非空
`description`，并与 registry/interface 精确一致；`tests[]` 只能引用 package-local
`tests/<file>` regular file，禁止标签、虚构路径、越界路径或 symlink evidence。

Interface schema 1.2 为每个 mode 固定 `routing`，新增必填 `judgment_mode`，并声明
`runtime_dependency` 与 validator `runtime_command`。`semantic` 使用五阶段，
`deterministic` 使用三阶段；`standalone` 只表示平台可脱离
global workflow routing 直接发现 Skill，不表示单目录 self-contained/portable；两种
mode 均依赖完整且兼容的 Guru Team preset、installed extension manifest、shared
dispatcher、companion scripts 与 managed package inventory。缺失或不兼容时必须在业务
副作用前失败并提示完整安装或升级 preset，禁止回退到旧 companion command。

Skill id、external exit id、schema/interface id、stable script command 和
registry lifecycle 都是公共 API；破坏性变更必须新建 id 或给出迁移合同。
`guru-create-work-commit` 保留为 reserved tombstone；正式 active 入口是
`guru-create-task-commit`，不得重新解释旧 id。

Phase 0 base freshness 的正式 active 入口是 `guru-sync-base`。它固定使用
explicit base、non-empty scalar `base_branch`、ordered `base_branch_candidates` 中首个
existing ref（缺省 `dev -> develop -> main -> master`）、候选均不存在时的 remote default
四级解析，禁止 current branch implicit fallback；多个候选同时存在按配置顺序选择，
不是歧义。外部出口固定为 `synced`、`skipped`、
`blocked`。`sync-base` 与 `check-base-sync` 是共享 deterministic runtime command，
`guru-base-sync-result-1.0` 是结果 schema id。`prepare-task` 复用同一 resolver/sync core，
不能另维护 planner/executor base 语义。Resolution/result facts 只经 stdout 传递；
planner 与各 mutation guard 接收 expected digest，并在各自边界重跑 shared core。
Skill 不创建 repo-external evidence file、lease、release 或 cleanup API。

本仓库的扩展长期源头位于：

- `trellis/index.json`
- `trellis/workflows/guru-team/`
- `trellis/presets/guru-team/`
- `trellis/presets/guru-team/overlays/`
- `.trellis/spec/`
- `README.md`

`.trellis/workflow.md`、`.agents/skills/`、`.codex/prompts/`、`.codex/skills/`
等 dogfood 文件是本仓库安装后的运行副本；维护时应从 canonical source 同步，而不是把
dogfood 副本当成唯一来源。

## GitHub 历史索引

| 主题 | Issues | Merged PRs |
| --- | --- | --- |
| 中台知识门禁与 Docs SSOT | #1, #64, #65, #66 | #4；#64/#65/#66 对应 hardening PR |
| Trellis auto-bootstrap 日常入口 | #2 | #3 |
| AI review prompt 与 Branch Review Gate | #5, #20, #44 | #12, #22 |
| prepare-task 无副作用 planner 与命名质量门禁 | #6, #51 | #14；#51 对应 PR 待发布 |
| Phase 0 selected-base resolve / sync closed loop | #110 | 当前实现分支；#111 仅负责后续 context discovery Skill 化 |
| Workspace boundary 与 source checkout 误写防护 | #60 | 当前 PR 待发布；为 #76 liveness checker 提供 source/task 双侧事实层 |
| Sub-agent liveness / stale cutover 状态机 | #76 | 当前 PR 待发布 |
| PR readiness 与 PR body 质量 | #7, #17 | #23, #24 |
| Planning / phase2 可审计证据 | #8 | #25 |
| Dogfood overlay 同步 | #9 | #13 |
| README 非交互安装与开箱验证 | #10 | 历史合并已体现在 README / validation 脚本中 |
| Preset 平台选择 | #11 | #30 |
| no_task 直接编辑审批 | #15 | #16 |
| publish 只能发生在 finish-work 后 | #18 | #19 |
| Worktree developer identity | #26 | #28 |
| finish-work dry-run readiness / Codex dispatch | #27 | #29 |

Closed but unmerged PR：

- PR #21：`#20` 的早期实现尝试，已关闭并由 PR #22 替代。
