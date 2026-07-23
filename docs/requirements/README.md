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
- 后续维护补充：active issue #112 已把 task workspace mutation 收敛为
  `guru-create-task-workspace`；`prepare-task` 仅保留 query-only compatibility。#60
  已沉淀为 workspace boundary 事实层与 task artifact 写入边界；#76 正在沉淀为
  sub-agent liveness、status request、stale cutover 与 completed-only recovery
  gate。合并后应随对应 PR 更新到历史索引。
- #112 的失败恢复补充要求 reviewed-draft 创建前执行 exact open-issue 0/1/>1
  恢复判定，完整 Intake 重入携带 checker-passed created-issue result；首次业务 mutation
  前还必须重跑 shared base sync，remote 前进时刷新 base 后返回 `refresh_review`。
- Active issue #129 把 Phase 1 planning approval 收敛为 active semantic Skill
  `guru-approve-task-plan`。它是 `planning-approval.json` 唯一 semantic owner，固定消费
  current wording evidence、审查 planning adequacy/provenance/unusual proposals、取得所需
  confirmation，并通过四个 typed exits 交回 global workflow；shared runtime 只录制和校验
  deterministic facts。
- Issue #144 建立 interface 1.2/1.3 共存、registry 1.1 exact migration
  state、minimal public input/per-exit output/consumer projection/private artifact 与
  `discover-skill-contract` 基础设施。#144 交付时，九个 production Skills 仍使用 1.2
  `legacy`，1.3 representative fixture 仅用于测试；随后 #145 已把六个 Stage 0 Skills
  及其 24 exits 原子迁移到 `1.3+minimal_handoff`；#146 再以独立
  `production-minimal-handoff-v1` 把 planning/check/commit 三包、十个 profiles 与 11 exits
  原子迁移到 1.3。当前 live closure 为 9 Skills / 35 exits，Stage 0 的 6/24 identity 保持不变。

## 扩展重要性分层

| 层级 | 类别 | 历史来源 | 说明 |
| --- | --- | --- | --- |
| P0 | Workflow 主合同与日常入口 | #1, #2, #57, #64, #65, #66, #78, #130 | `guru-team` marketplace workflow 定义 Phase 0-3、auto-bootstrap 日常入口、业务项目中文文档默认规则、知识门禁和 Docs SSOT；Phase 1 规划策略后由 active `guru-check-task` 独占 Phase 2 scope/adequacy/finding loop、`guru-phase2-check-2.0` 与四出口，official `trellis-check` 只提供 evidence；Phase 3 final review 只验证不补救、finish-work 不首次 merge docs；Branch Review `reviews/*.md` / `review.md` 也继承中文 human-readable artifact 规则。 |
| P0 | Intake / base sync / change-context / task workspace / no_task / workspace boundary 副作用边界 | #6, #15, #26, #51, #54, #60, #96, #99, #110, #111, #112 | repo-changing intake mandatory invoke `guru-sync-base -> guru-discover-change-context -> guru-clarify-requirements -> guru-review-contract-wording -> guru-review-change-request -> guru-create-task-workspace`。最后一个 active semantic Skill 是 issue/branch/worktree/task 唯一 mutation owner；reviewed draft 只创建 exact issue 后返回 `refresh_review`，open issue 另行取得 workspace/task confirmation 后才创建 workspace。它固定解析 assignee、通过隔离 adapter 调用 official `common.task_store.cmd_create`，仅在该 handler 调用内禁用 developer accessor，使 `creator=assignee=reviewed login`；同时写四个 portable task-local Intake artifacts，并只把本机 mapping 写到 ignored `.trellis/.runtime/guru-team/**`。Guru preset/executor 不读取、不创建、不恢复 `.trellis/.developer` 或 `.trellis/workspace/**`，existing identity bytes 保持不变；官方 Trellis identity/journal 支持仍保留。 |
| P0 | Planning / check / task work commit / Branch Review Gate 证据链 | #5, #8, #20, #44, #62, #72, #76, #78, #122, #125, #129 | `guru-approve-task-plan` 独占 Phase 1 planning adequacy、四类 provenance、implementation choice、unusual proposal、AI Gate、confirmation 与 `approved` / `revision_required` / `clarify_scope` / `blocked` 路由，并写 schema 2.0 唯一 `planning-approval.json`；runtime 只验证 deterministic facts、closed union 与 freshness。后续 phase2 check、`guru-create-task-commit`、独立 review、中文 raw/rollup review report、review report digest、任意 finding 阻断、fresh 最终放行审查、sub-agent liveness / status request / stale cutover / completed-only recovery chain 继续形成可审计链路；`workflow` 与 `standalone` 只区分 global routing 与 direct discovery，两者都依赖完整 Guru Team runtime，package wrapper 统一经 `run-skill-command` fail closed；默认 sub-agent mode 下 implement、check、Branch Review 都必须有真实 sub-agent evidence。 |
| P0 | Finish / publish / PR readiness | #7, #17, #18, #27, #66 | PR 发布只能在 finish-work 后发生，且必须有 AI 审查过的 reviewer-facing body 与 readiness evidence；PR body 必须说明 Docs SSOT / 文档同步处理结果。 |
| P1 | Preset installer 与平台 overlay | #9, #11 | preset 安装 companion assets 与平台入口，支持 overlay 选择，并保持 canonical / dogfood 同步。 |
| P1 | 安装、升级、开箱验证 | #10, #27 | README 非交互安装、throwaway install、dry-run readiness 和 Codex 默认 sub-agent 让新项目可开箱使用。 |
| P2 | Docs / spec / knowledge 协同 | #1, #9, #10, #57 | task artifact、durable docs、`.trellis/spec/`、中台知识引用、业务项目中文语言规则和公开安装文档协同。 |

Phase 0 change-context 的 duplicate evidence 使用 repo/number/`#number` identity/canonical
URL/open state/update time 的 deterministic digest projection，并从同一次 open search 返回
字段重算 identity、URL 与 digest；record/check 不进行第二次 search 或 candidate re-read。
同一 result contract 双向绑定 `typed_exit=blocked` 与 blocked AI Review Gate。
Active-task context re-entry 由 validated task/snapshot locators 绑定 owner
checker；private `task_worktree_state` 覆盖除 fixed snapshot/runtime 外的完整 dirty
worktree。Different-byte fixed snapshot 仅在 regular/trackable prior、exact expected
prior digest 与完整 new/live validation 全部通过后 formal replace，并记录
`superseded_snapshot_sha256`；失败保持 prior bytes，same-byte retry 幂等。

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

Interface schema 1.2 为已发布 legacy contract；interface 1.3 是新建或实质修改 public
I/O 的 independent target。Registry 1.1 的每个 active row 必须 exact 选择
`interface_schema_id` 和 `legacy|minimal_handoff`，不得从 optional 字段猜版本。
当前 `stage0-minimal-handoff-v1` 原子单元中的六个 Stage 0 production rows 与独立
`production-minimal-handoff-v1` 中 planning/check/commit 三个 rows 均使用
`1.3+minimal_handoff`，active `legacy_skill_ids=[]`。两版均为每个 mode 固定 `routing`，
声明 `judgment_mode`、`runtime_dependency` 与 validator `runtime_command`。`semantic` 使用五阶段，
`deterministic` 使用三阶段；`standalone` 只表示平台可脱离
global workflow routing 直接发现 Skill，不表示单目录 self-contained/portable；两种
mode 均依赖完整且兼容的 Guru Team preset、installed extension manifest、shared
dispatcher、companion scripts 与 managed package inventory。缺失或不兼容时必须在业务
副作用前失败并提示完整安装或升级 preset，禁止回退到旧 companion command。

Skill id、external exit id、schema/interface id、stable script command 和
registry lifecycle 都是公共 API；破坏性变更必须新建 id 或给出迁移合同。
`guru-create-work-commit` 保留为 reserved tombstone；正式 active 入口是
`guru-create-task-commit`，不得重新解释旧 id。

Interface 1.3 的 `public_contracts` 独立声明 caller-owned structured/scalar input、
exact package invocation、per-exit schema/example、Skill/workflow/stop consumer input、
direct/select/rename/closed normalize projection 和 runtime checkpoint/gate evidence
private artifact。所有 public output 字段必须有直接 consumer use，public/private
schema 互斥。稳定命令 `discover-skill-contract` 返回 closed legacy/minimal variant；
失败携带 stable code、repo-relative field path 与 remediation。Mixed fixture 不进入
production registry、manifest、platform inventory 或 mandatory route。

Stage 0 migration manifest 精确绑定六包、24 exits、全部 public input
profiles/signature、per-exit output/example、consumer/projection、private artifact 与 eval case。
Registry、Interface、workflow markers、extension inventories、manifest、canonical/installed
packages 和 selected platform copies 必须双向集合相等；任何 missing/extra/duplicate/renamed/
unknown 或 mixed 1.2/1.3 Stage 0 graph 均失败关闭。Preset 以一次完整 staging transaction
安装该单元，upgrade/update/reapply 后仍须得到同一 graph、同一 corpus bytes/modes 与零
`.new`/`.bak` sidecar。

Production manifest 精确绑定 planning/check/commit 的十个 structured profiles、11 exits、
per-exit output/example、consumer/projection、private artifact 与 eval cases；两个 manifests
合并后形成当前 9/35 closure。`committed` DTO 只含 `exit_id`、`task_ref`、`base_ref`、
`committed_head`，继续由 `branch-review-or-finding-closure` 消费，#146 不提前激活 #131。
Commit candidate builder 只物化 private plan并复用既有 validator/executor transaction。

Planning revision self-reentry、check passed 到 initial commit、commit revision self-reentry
三条 edge 使用 target-owned `skill_input_authoring_seed`。Producer 只投影 minimal seed，
caller AI 编写其余 required semantic fields；validator 证明字段分区无交集且完整、merge 无
覆盖并通过完整 target schema。该 consumer kind 不新增 projection operation，也不允许
private lookup、default 或 runtime semantic reconstruction。

`guru-sync-base` 保持 scalar CLI；其余五包以 closed discriminator profiles 表达 pre-task、
re-entry、target、scope-change 与 mutation initial/recovery。Agent 先在 owner loop 中完成
semantic Gate 与 recorder/checker，再向 public wrapper 提交 caller-owned input 和
repo-relative owner-result/supporting locators。Runtime 重跑现有 checker，并且只从
checker-passed owner result 推导 typed route；调用方不得传 expected exit，public output
example 也不是生产输入。每次 invocation 只返回一个 declared typed-exit DTO，normal Agent
不读取/import `guru_team_trellis.py` 或 private artifact body。Existing active task 通过 owner
profile re-entry，archived 1.2 artifacts 按旧 schema 只读且不回写。

Interface 1.3 scalar argument 的 `required` 是显式 boolean；只有 `required=false` 可省略。
`guru-sync-base --base-branch` 省略时复用 formal owner resolver，不在 wrapper 复制 fallback。
Active-task scope-change clear 的 null disposition 固定投影为 `retained`，initial/standalone
null 仍失败关闭。Production semantic eval 使用 repo-local checker-passed owner result；actual
exit 选择 schema 后才比较 expected exit，四平台不接收 expected-exit oracle。

Phase 0 base freshness 的正式 active 入口是 `guru-sync-base`。它固定使用
explicit base、non-empty scalar `base_branch`、ordered `base_branch_candidates` 中首个
existing ref（缺省 `dev -> develop -> main -> master`）、候选均不存在时的 remote default
四级解析，禁止 current branch implicit fallback；多个候选同时存在按配置顺序选择，
不是歧义。外部出口固定为 `synced`、`skipped`、
`blocked`。`sync-base` 与 `check-base-sync` 是共享 deterministic runtime command，
`guru-base-sync-result-1.0` 是结果 schema id。`prepare-task` 复用同一 resolver/sync core，
不能另维护 planner/executor base 语义。Resolution/result facts 只经 stdout 传递；
query 接收 current expected digest 并在读取前重跑 shared core；workspace mutation
freshness 由 `guru-create-task-workspace` 在自身边界独立重验。
Skill 不创建 repo-external evidence file、lease、release 或 cleanup API。
Workspace plan 绑定 initial `post_sync_resolution_sha256`；executor 首次 mutation 前实际
fetch/sync，fresh identity 改变时不创建 issue/workspace/task并回到完整 Intake。

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
| Phase 0 selected-base resolve / sync closed loop | #110 | 已实现；`synced` 的唯一 consumer 是 #111 的 active context discovery Skill |
| Phase 0 change-context semantic closed loop | #111 | active `guru-discover-change-context`；current-state-first、finish-summary index preview、same-snapshot task-local persistence、current stale-code/superseded-digest refresh re-entry、Git-trackable task target |
| Phase 0 change-request readiness semantic closed loop | #101, #112 | active `guru-review-change-request`；三类 target、current context/clarity/wording linkage、十项 AI review dimensions、五出口、stdout-only record/check；`ready` 唯一进入 active `guru-create-task-workspace` |
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

## Skill 行为评测基础设施（#147）

#147 建立 Interface 1.3 package-local `evals/evals.json`、closed schema、真实
public-wrapper runner、deterministic/external-semantic/human 三边界，以及
shared/Codex/Claude/Cursor 四个薄 adapter。#147 交付时，九个 production Skills 仍保持
Interface 1.2 legacy；随后 #145 已迁移六个 Stage 0 production corpora 并完成其 24 exits
coverage；#146 已完成 planning/check/commit 三包的 11-exit coverage 与 9/35 closure。
四个 descriptor 必须绑定真实可执行 wrapper，并由 wrapper 从 `PATH` 检测 documented native
command、组装平台 argv、加载 exact Skill/prompt/files、收集 public output/trace；隐藏
executable 环境变量不能替代该公开安装路径。
Runner 在 native execution 外读取 canonical corpus；CLI 只收到 repo/package 外 public-only
projection、case workdir 与不含 canonical package/corpus/private runtime locator 的最小 request。
Native trace 使用 closed `guru-team-skill-eval-native-trace-1.0` receipt：CLI 必须通过
repo 外 helper 读取 projected exact `SKILL.md` 并调用 exact public wrapper，receipt 与 request、
projection、Skill/wrapper digest、wrapper result 和返回 DTO 不匹配或缺失时为
`execution_error`。四平台直接读取 projection 内 eval/private runtime 必须真实失败，不能靠提示词。
