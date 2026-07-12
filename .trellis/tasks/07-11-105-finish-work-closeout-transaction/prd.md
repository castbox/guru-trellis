# Issue #105: 重构 Guru Team finish-work 收尾事务

## 1. 来源与目标

- Source issue: <https://github.com/castbox/guru-trellis/issues/105>
- 前置 issue: #97 与 #100 已关闭并合入 `main`。
- 后续 issue: #98、#99、#101 保持独立交付，不进入本任务关闭范围。
- 目标: 把 Guru Team closeout 从 archive 中途发生的多段流水线，重构为 archive 前完成全部可预见验证、用 draft PR 固化 PR identity、用单一入口恢复任意中断的事务状态机。

## 2. 当前问题

当前 `finish-work` 在正式路径中先写 `pr-readiness.json`，再调用官方 `task.py archive`，随后才构建和校验 `finish-summary.json`、迁移 review gate、提交 metadata、push、执行 marketplace verifier、创建 PR、回写 PR URL 并再次提交和 push。

这条顺序形成五个缺陷:

1. dry-run 与正式路径没有复用同一个完整 prepare/validate 管线，dry-run 通过不证明正式路径中的 ledger、remote evidence、archive path mapping 和 publish identity 合法。
2. task 已进入 archive 后仍会触发本地合同错误、GitHub auth 错误、远端 verifier 错误和 PR create 错误。
3. `remote_marketplace_verification` pending 对象由 AI 手写，机器字段与人类说明混在一个逐字 identity 合同中。
4. 正常路径生成 empty-URL initial summary、archive metadata commit、PR URL summary tail，形成多个 closeout metadata commit。
5. `--skip-archive` 与 `--recovery-after-finish-work` 暴露内部阶段，调用者必须自行判断中断点。

## 3. 功能需求

### R1. Canonical closeout plan

- 新增 schema-valid immutable closeout plan，固定记录 task/repo/base/head identity、Branch Review Gate、Issue Scope Ledger、PR title/body/draft-to-ready 策略、finish-summary index、marketplace requirement、active/archive path mapping、metadata allowlist 与输入 artifact SHA-256。
- plan 的 canonical JSON digest 固定为 `closeout_plan_digest`。dry-run 与正式 finish 必须调用同一个 prepare/validate 函数并产生相同 digest。
- dry-run 只输出 plan、digest 和预期动作，不写 task、Git、GitHub 或 runtime 状态。
- 正式 finish 必须接收 dry-run 返回的 expected digest，在首个副作用前重建 plan 并逐字比较 digest。输入漂移必须失败并保持 task active。
- 首次 formal digest 匹配后必须把同一份 plan 写为 task-local `closeout-plan.json`，并与 immutable readiness 一起提交。后续重试只读取已提交 plan，不从已推进到 passed 的 ledger 反向重建初始输入。
- PR number、PR URL、verifier 输出和 archive commit SHA 属于阶段运行事实，不进入 immutable input digest；它们必须受 plan 中的 repo/base/head、artifact locator、状态转换和 allowlist 约束。

### R2. Archive 前本地完整验证

- prepare 必须验证 workspace boundary、task identity、review gate、ledger close/ref/follow-up 互斥、close issue acceptance evidence、PR body/readiness、finish-summary index、repo/base/head、marketplace requirement、active/archive mapping、schema 和 metadata allowlist。
- prepare 必须在内存或隔离临时目录构建 future archived task 投影，并对最终路径、artifact existence、review gate locator、ledger、readiness 和 summary 执行完整验证。
- malformed pending evidence、缺 acceptance evidence、close/ref 重叠、gate 未覆盖 #105、body/readiness 缺失、summary/path 错误必须让 dry-run 与 formal 返回同类错误。
- 正式 finish 在 archive 前完成全部本地 artifact build、schema validation、path mapping validation 和 immutable input validation。

### R3. Deterministic marketplace evidence

- AI 继续负责 `close_issues`、`related_issues`、`followup_issues`、acceptance evidence 和 PR readiness 充分性判断。
- recorder 从 plan 中的 machine facts 生成 pending marketplace evidence。AI 不再手写 status、required、artifact locator、HEAD 或 digest 字段。
- reviewed content push 成功后，recorder 必须把 pending evidence 写入 active ledger；verifier 成功后只能把该 machine object 替换为 passed。两个状态都必须匹配 plan 声明的 canonical machine identity。
- 人类 reason 不参与 machine evidence identity。修改 reason 不得改变 pending machine identity；缺失或篡改 machine 字段必须 fail closed。
- required verifier 必须针对已 push 的 reviewed content HEAD 执行，生成 `marketplace-verification.json`，并把 primary/close issue evidence 更新为 passed。
- verifier artifact、ledger passed evidence 和 immutable readiness 必须在 draft PR 创建前提交、push 并通过 remote HEAD 校验。

### R4. Draft PR identity handshake

- formal finish 必须先 push reviewed content，并校验 local/remote branch、repo、base 与 head identity。
- formal finish 必须创建 draft PR，不得直接创建 ready PR。
- 同一 repo/head/base 已存在唯一 open PR 时必须复用；不存在时创建一个 draft PR；存在多个匹配 PR 时必须 fail closed。
- canonical PR number/URL 必须写入最终 `finish-summary.json.github.pr_url`，`index.search_terms.pr_refs` 必须保留唯一 `PR #<number>`。
- draft 创建后到 archive transaction 完成前发生失败时，PR 必须保持 draft，task 必须保持 active；同一 `trellis-finish-work` 入口重试时必须复用该 PR。

### R5. Final archive projection

- 取得 canonical PR identity 后，formal finish 必须在 active task 中构建一次最终 `finish-summary.json`，内容按 future archive path 投影并通过 #97 schema/validator。
- final projection 必须重新验证 ledger passed evidence、readiness、review gate、artifact links、changed paths 与 exact metadata allowlist。
- final projection 通过前不得调用 `task.py archive`。
- final summary 必须保留 #97 的安全 path 过滤合同、canonical PR URL 和 #98 `--pr` 精确检索所需的唯一 PR ref。
- 正常成功路径不得生成 empty-URL initial summary，不得生成 post-PR summary tail commit。

### R6. Archive metadata transaction

- archive transaction 必须调用未修改的官方 `task.py archive`，把 active task metadata 与已验证的 final summary 移到预期 archive path。
- archive commit 必须只包含当前 task 的 active-to-archive metadata move、最终 task status 和 final summary。代码、workflow、preset、schema、docs、tests、CI/CD、部署、migration 与 Makefile 路径必须触发 fail closed。
- transaction 必须 push archive commit，并校验 local HEAD、remote branch HEAD 和 draft PR head 三者相同。
- archive move、commit 或 push 中断后，调用者继续使用同一个 `trellis-finish-work` 入口。入口必须识别已持久化的 plan/readiness/draft PR 和 active/archive 状态，恢复精确 transaction；不得要求 `--skip-archive`。
- archive transaction 完成后不得再构建、校验或改写 repo artifact，不得新增 commit，不得再次 push branch。

### R7. Draft-to-ready publish

- archive transaction 完成且三方 HEAD 相同后，executor 才能把 draft PR 转为 ready。
- draft-to-ready 失败时，final remote HEAD 与 draft PR 必须保留。重试同一入口时只能重新执行 remote identity check 和 draft-to-ready，不得重新 verifier、archive、改写 artifact、commit 或 push。
- `publish-pr` 仅保留无条件兼容性阻断入口，不再是 executor；publish 与 recovery 只由 `trellis-finish-work` 执行。
- `--skip-archive` 与面向用户的 `--recovery-after-finish-work` 必须退出正常合同。兼容入口若保留，必须 fail closed 并指向同一状态感知入口。

### R8. Canonical、dogfood 与平台一致性

- canonical workflow、finish skill/command/prompt、preset、overlay、README、durable specs、schema、companion scripts 与 tests 必须同步同一事务顺序。
- `.trellis/workflow.md` 与 `.trellis/guru-team/**` dogfood installed copy 必须由 canonical source/preset apply 同步，不得成为唯一源头。
- Claude、Codex、Cursor 已声明平台的 finish entry 文案必须一致，不得继续展示旧 archive-first、empty summary tail 或内部 recovery flag。
- preset apply 后必须处理全部 `.new` / `.bak`，overlay drift 必须为零。

### R9. 单一实现与减法收敛

- `trellis-finish-work` 必须是 closeout publish/recovery 的唯一生产实现；不得同时保留另一套可执行的 PR publish、summary tail、marketplace evidence 或 recovery pipeline。
- `publish-pr.sh` 作为既有公共路径只保留兼容性阻断入口，必须 fail closed 并指向 `trellis-finish-work`；不得保留无生产调用者的完整 executor 实现。
- 新增 production top-level function 必须存在真实生产调用者，或本身是 `main()` 可达的显式 CLI handler；只有测试调用的 helper 必须删除。
- 测试必须经过真实 CLI parser 或真实 `finish-work` production entry；不得通过手工构造 parser 不可能产生的 `argparse.Namespace` 来证明 dormant 路径正确。
- clean throwaway initial/update installed closeout smoke 属于本 issue 明确验收面，必须保留；减法不得以删除开箱即用验证换取行数下降。
- 本轮只删除重复实现、死代码和对应自证测试，不新增通用 resolver、通用 symlink、remote transport framework、索引格式、schema 或时间框架。

## 4. 非目标

- 不删除或放宽 #97 `finish-summary.schema.json` 的 PR URL、PR ref、path safety 和 retrieval text 合同。
- 不降低 #98 `--pr` 精确匹配、候选 PR URL 输出或解决 PR 读取能力。
- 不实现 #98、#99 或 #101。
- 不创建 repo 级 committed archive index。
- 不修改 Trellis upstream、全局 npm、`node_modules`、官方 `task.py archive` 或官方 task lifecycle。
- 不恢复 `.trellis/workspace/**`、`add_session.py` 或 developer journal。
- 不把 issue scope、PR readiness、review finding 或 publish 充分性判断写入 Python/shell。
- 不以兼容名义保留第二套 publish/recovery 业务实现；兼容入口只允许确定性拒绝。

## 5. 验收标准

- [ ] dry-run 与 formal 共用 prepare/validate 函数，并输出相同 canonical plan digest。
- [ ] 首次 formal 提交的 `closeout-plan.json` bytes 与 dry-run plan canonical bytes 一致；后续重试只消费已提交 plan 与 readiness。
- [ ] formal expected digest 与重建 digest 不同、任一 protected input SHA 漂移或 repo/base/head identity 漂移时，在首个副作用前失败。
- [ ] ledger、gate、body、readiness、summary、artifact、path mapping 的本地错误在 archive 前失败，task 保持 active。
- [ ] pending marketplace evidence 由 recorder 生成；reason 变化不改变 machine identity，machine 字段缺失或篡改被拒绝。
- [ ] required verifier 在 archive 前执行；passed artifact/ledger/readiness commit 已 push，remote HEAD 已校验，再进入 draft PR 阶段。
- [ ] formal 创建或复用唯一 draft PR；多个匹配 PR 被拒绝；重试不创建重复 PR。
- [ ] final summary 一次生成，包含 canonical PR URL 和唯一 `PR #<number>`，不存在 empty-URL initial summary 或 post-PR summary tail。
- [ ] final archive projection 在 active task 中通过完整 schema、artifact、ledger、gate、readiness、path 和 allowlist 校验。
- [ ] archive commit 只包含当前 task metadata transaction；push 后 local、remote、draft PR head 相同。
- [ ] PR 转 ready 后 branch 不新增 commit，工作树干净，PR 非 draft。
- [ ] failure injection 覆盖 prepare、content push、verifier、evidence commit/push、draft PR create、final projection、archive move/commit/push、remote HEAD check 和 draft-to-ready。
- [ ] 每个 injection 断言 task active/archive path、PR draft/state、local/remote HEAD、dirty paths 和唯一合法下一动作。
- [ ] 2026-07-03 identity failure、2026-07-04 dry-run/archive failure与 #100 pending marketplace evidence failure均有回归测试。
- [ ] 同一 `trellis-finish-work` 入口恢复所有阶段，不要求调用者理解 `--skip-archive` 或 publish recovery。
- [ ] canonical Python/preset tests、compile、shell syntax、JSON/schema、task validation、overlay drift、canonical/dogfood equality 和 `git diff --check` 全部通过。
- [ ] clean throwaway repo 完成 workflow/preset 安装、dry-run digest、formal draft handshake、archive metadata、PR ready 路径。
- [ ] throwaway repo 完成 workflow preview/switch、`trellis update`、preset reapply 与递归 sidecar 空扫描，事务语义不漂移。
- [ ] `cmd_publish_pr` 不再承载 publish/recovery 行为；其专属 production call graph 已删除，`publish-pr.sh` 仅验证兼容性拒绝。
- [ ] production AST/call graph 不存在只有测试调用的新增 top-level function，已删除 `resolve_closeout_state()` 和审计识别的全部无生产调用代码。
- [ ] 删除直接测试 dormant publish executor 的用例，只保留真实 parser/CLI 兼容拒绝测试；canonical closeout failure matrix 与 installed smoke 继续通过。
- [ ] 相对当前 reviewed HEAD，减法修复删除目标不低于约 900 行 production dormant code 与约 1300 行自证测试；最终以职责唯一性和调用可达性为门禁，不以机械行数替代审查。

### Round 18 边界收敛

- 用户于 2026-07-12 明确确认本任务继续修复 Round 18 当前范围 finding，但不得扩展为通用 hook 或时间迁移能力。
- archive destination 月份与 immutable plan 不一致时，必须在 official move 前失败并保持 task active；同一 `trellis-finish-work` 入口必须生成新 digest 并重新 prepare，不实现跨月 archive 迁移或通用时钟框架。
- `.trellis/config.yaml` 存在非空、不可确定验证或不可解析的 `after_archive` hook 时，必须在 archive 前 fail closed；本任务不执行、不分析、不支持 hook transaction。
- 上述两项只用于守住“archive 后不再出现本地可预见失败”的现有验收合同，不新增 Trellis upstream 修改或新的平台能力。

## 6. Docs SSOT 状态

- 状态: `complete_docs`，现有 durable docs 已覆盖旧 finish-summary/publish 流程，但本任务必须以新事务合同替换旧顺序。
- 产品范围 SSOT: GitHub issue #105。
- 流程 SSOT: `trellis/workflows/guru-team/workflow.md`。
- 机器合同 SSOT: `trellis/workflows/guru-team/schemas/` 与 canonical Python validator。
- companion 合同 SSOT: `.trellis/spec/workflow/companion-scripts.md`。
- data 合同 SSOT: `.trellis/spec/workflow/data-contracts.md`。
- task 文档只保存本次决策、执行步骤和 gate 证据，不替代 durable SSOT。
