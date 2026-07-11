# Issue #105 技术设计

## 1. 设计原则

1. Markdown workflow/skill/prompt 负责 scope、readiness、review 与 publish 充分性判断。
2. Python 只实现 plan builder、validator、recorder、Git/GitHub executor 与确定性状态恢复。
3. archive 是最后一个 repo mutation transaction，不再充当流水线中点。
4. draft PR 在 archive 前提供稳定 PR identity；ready 状态只在最终 remote identity 校验后切换。
5. #97 finish-summary schema 与 #98 PR 检索合同保持兼容。
6. 官方 `task.py archive` 保持原样，Guru Team 在其外部组织投影、allowlist 和恢复状态机。

## 2. 现状证据

当前 `cmd_finish_work()` 的正式顺序是:

1. 验证 gate、dirty paths、index 与 PR body。
2. 写 active task `pr-readiness.json`。
3. 调用 `task.py archive`。
4. 在 archived task 构建 initial empty-URL `finish-summary.json`。
5. 迁移 gate path、提交 metadata。
6. 调用 `cmd_publish_pr()` push、verifier、PR create、summary URL rewrite、summary tail commit/push。

当前 `cmd_publish_pr()` 同时承载 normal publish 与 `--recovery-after-finish-work`，`cmd_finish_work()` 又通过 `--skip-archive` 暴露另一个恢复分支。职责交叉导致调用者必须判断失败阶段。

## 3. 目标状态机

| 状态 | task path | PR 状态 | 可执行动作 | 禁止动作 |
| --- | --- | --- | --- | --- |
| `prepared` | active | none | push reviewed content | archive、PR create |
| `content_pushed` | active | none | verifier 与 evidence/readiness commit | archive |
| `evidence_pushed` | active | none | create/reuse draft PR | archive |
| `draft_bound` | active | draft | build/validate final archive projection | ready |
| `projection_validated` | active | draft | archive metadata transaction | 重跑 verifier |
| `archive_moved` | archive | draft | exact metadata commit/push recovery | artifact build/rewrite |
| `archive_pushed` | archive | draft | local/remote/PR head check | commit、push |
| `ready` | archive | ready | return success | repo mutation |

状态不写独立 runtime marker。executor 从 immutable readiness、plan digest、task active/archive locator、Git history、remote HEAD 与 open PR identity确定当前状态。无法形成唯一状态时 fail closed。

## 4. Immutable closeout plan

### 4.1 数据结构

新增 `closeout-plan.schema.json`，schema version 固定为 `1`。plan 包含:

- `task`: portable task id、active locator、archive locator、source issue。
- `git`: repo、remote、base branch、head branch、reviewed work HEAD。
- `inputs`: task context、task、gate、ledger、PR body、finish-summary index、relevant config 的 SHA-256。
- `review`: gate reviewed HEAD、changed paths、close issue coverage。
- `publish`: exact title、body SHA、draft-to-ready 策略、unique PR match identity。
- `marketplace`: required flag、pending machine object template、verifier artifact locator。
- `projection`: active-to-archive mapping、final artifact locator、metadata path allowlist。
- `transitions`: 固定状态序列与每段 executor 名称。
- `plan_digest`: canonical JSON 在排除本字段后的 SHA-256。

plan 中不保存 token、环境变量、绝对 worktree path、PR URL、verifier 输出或 archive commit SHA。task-local artifact 固定命名为 `closeout-plan.json`。

### 4.2 Digest handshake

- `prepare_closeout()` 是 dry-run 与 formal 的共享入口，返回 schema-valid plan。
- dry-run 输出完整 plan 与 `plan_digest`，不调用 write、Git mutation 或 GitHub mutation helper。
- finish skill 从 dry-run 输出取得 digest，并在 formal 命令传入 `--expected-plan-digest <sha>`。
- formal 重新执行 `prepare_closeout()`。digest 不相同则返回 exit 2，payload 指明漂移的 artifact key，不执行 push。
- 首次 formal 把 canonical plan 原样写入 `closeout-plan.json`，把 digest 写入 `pr-readiness.json.publish_inputs.closeout_plan_digest`。两个 artifact 进入同一个 pre-draft metadata commit。
- 后续重试从 committed plan 与 readiness 读取初始输入和 digest，验证当前事实只能匹配 plan 声明的后继状态；不得用 passed ledger 反向重建初始 plan，不接受 title/body/base/draft/digest 覆盖。

### 4.3 阶段事实

PR identity、verifier digest、evidence commit SHA 和 archive commit SHA 作为 stage facts 进入 executor payload 或既有 artifact，不修改 immutable input digest。每段 transition 必须验证前段固定输出的 facts 与 plan identity 一致。

## 5. Shared prepare/validate pipeline

`prepare_closeout()` 依次执行:

1. resolve task 与 workspace boundary。
2. validate gate、dirty path class、ledger semantic scope、#105 acceptance evidence。
3. validate PR body/readiness judgment source与 finish-summary index。
4. resolve repo/base/head/remote 和 marketplace requirement。
5. recorder 构建 pending marketplace machine object与投影后ledger digest；reason 保留在semantic ledger区域，不参与machine identity。
6. build active/archive mapping 和 metadata allowlist。
7. 在 temporary projection root 中复制 task-local artifact bytes，按 archive locator 改写确定性 path fields。
8. 验证 projected ledger、gate、readiness、artifact links 与 summary skeleton。
9. build canonical plan、schema validate、计算 digest。

dry-run 与 formal 只能在第 9 步完成后分叉。formal 分支不得拥有 dry-run 未执行的本地 validator。

## 6. Formal executor

### 6.1 Push reviewed content

- 调用 `require_gh_auth()` 后 push reviewed work HEAD。
- 校验 repo、base、head branch、local HEAD、remote branch HEAD。
- 失败时 task active、PR 不存在，重试仍从 digest handshake 开始。

### 6.2 Marketplace verification 与 readiness

reviewed content push和remote HEAD校验完成后，recorder先把canonical pending machine object写入active ledger。required分支针对reviewed work HEAD运行verifier，成功后只把pending object替换为passed。recorder同时写:

- `closeout-plan.json` canonical plan artifact。
- `marketplace-verification.json` passed artifact。
- ledger 中 primary/close issue passed machine evidence。
- `pr-readiness.json`，包含 plan digest、exact publish inputs与 stage identity。

plan、readiness、verifier artifact与passed ledger进入一个exact allowlist metadata commit并push。not-required分支写/提交plan与readiness。push后校验remote HEAD。

verifier失败时task保持active，ledger保留recorder生成的pending object，PR不存在。同一entry重试必须校验或重建完全相同的pending machine bytes。这样AI不编辑固定对象，reason变化不改变machine identity，passed evidence仍有完整verifier provenance。

### 6.3 Draft PR handshake

- 查询 `repo + head + base` 的 open PR。
- 0 个: 使用 plan 固定 title/body创建 draft PR。
- 1 个: repo/head/base必须完全一致且 PR 必须保持 draft；复用 canonical URL。
- 多个: fail closed。
- 已存在 ready PR 只在状态机确认 archive transaction已完成且 head一致时视为 `ready`；其它组合 fail closed。

### 6.4 Final projection

取得 PR URL 后，builder 使用 reviewed HEAD、最终 metadata path snapshot、ledger passed evidence与 active-to-archive mapping构建 final summary。active task中的临时 `finish-summary.json` 保存 future archive identity，并在 temporary archive projection中执行:

- #97 schema与 Python validator。
- canonical PR URL和唯一 PR ref检查。
- path safety、artifact existence和 retrieval derivation检查。
- ledger、gate、readiness、marketplace evidence cross-validation。
- exact archive diff allowlist检查。

任一失败时 task仍 active、PR保持 draft。重试能覆盖 active task中的 recorder产物，但不得改变 plan protected inputs。

### 6.5 Archive metadata transaction

final projection通过后调用官方 `task.py archive`。active task中的 final summary随目录移动到 archive终态，避免 archive后重新 build/rewrite。

executor随后只执行:

1. 核对 staged/unstaged paths属于 prevalidated exact allowlist。
2. 创建单个 `chore(trellis): #105 固化任务收尾元数据` commit。
3. push同一 branch。
4. 读取 local HEAD、remote branch HEAD与draft PR head并要求三者相同。

archive move后不得调用 schema builder、ledger validator、body validator、summary rewrite或 verifier。若 move/commit/push中断，同一入口从 committed readiness、已存在 draft PR、active/archive locator与Git状态恢复 transaction；恢复路径不接受 `--skip-archive`。

### 6.6 Publish ready

三方 HEAD相同后调用GitHub draft-to-ready操作。失败时返回固定 stage `draft-to-ready` 和同一 finish entry命令。重试只执行 PR identity/HEAD校验与 ready切换。

## 7. AI 与脚本边界

| AI 主会话职责 | Companion 职责 |
| --- | --- |
| close/ref/follow-up issue分类 | 校验数组互斥与固定字段 |
| acceptance evidence充分性判断 | 记录与校验artifact digest |
| Branch Review finding闭环判断 | 校验gate HEAD与覆盖字段 |
| PR title/body/readiness真实性判断 | 固化title/body digest与GitHub调用 |
| Docs SSOT与安全/部署影响判断 | 执行schema/path/HEAD/allowlist检查 |
| 是否进入finish-work的最终决定 | 构建plan、projection与状态恢复 |

脚本不得从 changed files 推导 close issue，不得生成 reviewer-facing 论证，不得把 verifier exit 0替代 AI readiness。

## 8. 代码结构

canonical Python新增或重构为以下逻辑单元:

- `build_closeout_plan()` / `closeout_plan_errors()` / `validate_closeout_plan()` / `load_committed_closeout_plan()`。
- `prepare_closeout()`，供 dry-run和formal复用。
- `record_marketplace_machine_evidence()`，分离semantic reason与machine identity。
- `resolve_closeout_state()`，从tracked/remote facts识别唯一状态。
- `ensure_content_pushed()`、`ensure_marketplace_evidence_pushed()`、`ensure_draft_pr()`。
- `build_final_archive_projection()`、`execute_archive_metadata_transaction()`、`ensure_pr_ready()`。
- `cmd_finish_work()`只做阶段编排和结构化错误包装。
- `cmd_publish_pr()`保留内部低层executor语义，移除用户恢复决策。

Bash wrapper继续只转发参数，不承载状态判断。

## 9. Failure injection 设计

测试以fake Git/GitHub operation adapter或现有subprocess mock注入每段失败。每个case断言:

- task locator是active或archive。
- PR不存在、draft或ready。
- local/remote/PR head值。
- dirty/staged path精确集合。
- recorder artifact是否存在且digest是否匹配。
- next action固定为同一finish entry中的哪个transition。

历史回归固定覆盖:

- 2026-07-03: archive后developer identity/journal失败。新链路不调用journal，identity错误在prepare失败。
- 2026-07-04: dry-run通过但formal archive后失败。新链路共享prepare，formal digest漂移在archive前失败。
- #100: pending marketplace evidence不满足publish validator。新链路由recorder生成machine object并在archive前完成passed evidence。

## 10. Docs SSOT Plan

- state: `complete_docs`。
- strategy: `ssot_first`，因为任务重写public finish-work lifecycle与recovery合同。
- 先更新 `.trellis/spec/workflow/companion-scripts.md`、`data-contracts.md`、`workflow-contract.md` 与需要的 quality/preset contract。
- 再更新 canonical `workflow.md`、workflow README、preset README、`docs/requirements/guru-team-trellis-flow.md`、finish skill/commands/prompts与schema说明。
- canonical实现完成后运行preset apply同步dogfood `.trellis/workflow.md`、`.trellis/guru-team/**`和平台installed entries。
- task-local failure matrix、测试日志、review findings只保留在task artifacts，不复制到marketplace template。
- Phase 2 check前必须验证durable docs与最终代码阶段名、flags、artifact和恢复语义一致。

## 11. 安装、升级与回滚

- clean throwaway repo从remote branch安装workflow marketplace和preset，执行完整closeout smoke。
- 已有项目执行workflow preview/switch、`trellis update`、preset reapply；确认custom workflow保留，新schema/script/overlay恢复。
- 每轮apply后递归扫描 `.new` / `.bak`并处理，运行dogfood overlay drift。
- 回滚代码时同时回滚schema、workflow、skill、overlay、preset、docs与tests。
- 已创建draft PR但archive前回滚时保持draft并由维护者关闭；不得伪造ready或删除远端审计事实。

## 12. 安全与部署影响

- plan、错误payload和test fixture不得输出token、secret、`.env`、签名URL或Git credential。
- closeout plan只保存repo-relative locator与digest，不保存本机绝对worktree path。
- 本任务不增加服务、端口、配置项、数据库migration、容器或Kubernetes资源。
- Dockerfile、Docker Compose、GitHub Actions、Kubernetes/Kustomize、database migration和Makefile无需修改；原因是变更只作用于Guru Team本地workflow/preset/companion closeout控制面。
