# Issue #105 Branch Review Round 20 最终放行审查报告

## 审查身份

- 逻辑角色：最终放行审查代理
- technical agent：`/root/final_release_review_105_round20`
- 独立性：未参与实现、Phase 2 或 Round 1-19
- reviewed_head：`46c7ee508ef648c71214ed68593af302d56b0dfe`
- base：`3dec302206783fe4ac1296066e9a1789c995d58b`
- reuse_decision：`new-agent`
- findings_count：`2`
- 结论：`fail`

## 审查范围

只读审查了 live GitHub Issue #105、规划三件套及 planning approval、Phase 2、Issue Scope Ledger、agent assignment、Round 1-19 raw reports，以及完整 `base...HEAD` 的 60 文件、13 commits、13421 insertions、1250 deletions。

覆盖 canonical/dogfood workflow、companion、schema、preset、overlay、平台入口、installed smoke、durable docs、closeout plan、remote/PR identity、archive/recovery、resolver、hook、跨月、history rewrite、CI/CD、容器、K8s、migration、Makefile、安全与部署影响。

未修改文件，未运行 recorder/gate，未 commit、push、创建 PR 或关闭 issue。

## 最终审查

### P1：initial archive destination collision 未在 prepare/dry-run 阶段拒绝

证据：

- `build_closeout_plan()` 仅拼接 `.trellis/tasks/archive/YYYY-MM/<task>` locator，没有检查初始目标是否已存在：`guru_team_trellis.py:11455-11479`。
- `prepare_closeout()` 没有补充目标冲突校验。
- 目标冲突直到 evidence metadata 已 commit/push 后，才由 `ensure_closeout_draft_pr()` 调用 `closeout_task_dir_from_plan()` 发现：`guru_team_trellis.py:12126-12135`、`:12235-12240`、`:13356-13370`。
- 当前测试没有覆盖 archive destination collision 的 dry-run/formal 等价失败。
- PRD R2 明确要求 prepare 完整验证 active/archive mapping、最终路径及 path error，并要求 dry-run 与 formal 返回同类错误：`prd.md:33-38`、`:99-102`。

影响：

legacy、手工恢复或部分状态中若 planned archive locator 已存在，dry-run 会错误通过；formal 随后可能已经 push reviewed content、执行 verifier、生成并 push evidence commit，才暴露纯本地路径错误。虽然 task 尚未 archive、PR 尚未创建，但已违反 immutable prepare 的无副作用完整预检合同。

修复要求：

- 在 initial prepare 阶段检查 planned archive locator 必须不存在。
- 该检查必须发生在 Git/GitHub/recorder 副作用之前。
- 增加 production case，断言 dry-run 与 formal 均 fail closed，task active，local/remote HEAD、PR、ledger、plan/readiness 均无变化。

### P2：parent task 的 children 门禁误伤官方正常生命周期

证据：

- `prepare_closeout()` 对任何非空 `children` list 一律拒绝，但错误文案声称只禁止 active child mutation：`guru_team_trellis.py:11715-11721`。
- 官方 `task.py archive` 会保留 archived child 在 parent 的 children list；归档 parent 时，只修改仍能在 active tasks directory 找到的 child：`.trellis/scripts/common/task_store.py:414-431`。
- 因此先正常归档 children、再归档 parent 时，官方 archive 不会产生额外 child path mutation，但 Guru finish-work 仍永久阻塞 parent。
- 非-list 的 malformed `children` 又未被该门禁结构化拒绝，判断边界与官方消费语义不一致。
- 当前测试没有 archived-child parent success、active-child failure 或 malformed children case。

影响：

Trellis 官方支持的 parent/child 正常完成路径在 Guru Team workflow 中不可闭环。该限制未进入 PRD、design 或 durable workflow contract，属于公开 lifecycle 兼容性回退；它 fail closed，不会错误发布，因此定为 P2。

修复要求：

- 先验证 `children` 必须为 `list[str]`。
- 按官方 lookup 语义区分 archived children 与仍会被修改的 active children。
- 仅对会产生 transaction 外路径 mutation 的 active child fail closed，或明确设计兼容的受控 transaction。
- 增加 archived-child parent success、active-child side-effect-free failure、malformed type failure 测试，并同步 durable contract。

## 问题生命周期

Round 1-18 的既有 findings、Round 18 六项 P1 和 Phase 2 stale manifest P2 未发现代码级回退：

- lifecycle heads 已重锚到当前可达提交；19 份 raw report digest/size 与 assignment 一致。
- archived exact recovery 统一从 current commit blob 读取 plan。
- formal 入口均携带 expected digest。
- pre-move tracked mode/blob、dirty/staged/untracked、月份和 empty hook 门禁已实现。
- 跨月仅使用 active plan/readiness supersession。
- `after_archive` 仅 preflight rejection，不执行或分析。
- locator、remote、fork、raw body、summary PR identity 和 installed smoke 既有闭环保持有效。

本轮两项是 fresh full-diff review 新发现，属于 #105 当前 prepare/archive lifecycle，不得降级为观察项或 follow-up。

## 通过证据

- canonical suite：`411/411`，OK
- preset suite：`36/36`，OK
- post-commit Phase 2 audit：`errors=[]`
- Phase 2 的 28 个 dirty paths 与 `d8bde83..46c7ee5` 提交路径集合及 digest 精确一致
- planning approval、agent assignment validator：通过
- commit message contract：`13/13 errors=[]`
- Round 1-19 report digest：`19/19` 一致
- overlay drift、canonical/dogfood Python/workflow/schema/config/平台入口 equality：通过
- manifest：71 assets，排序唯一且存在，`managed_backups=[]`、`new_copies=[]`
- `.new/.bak`：0
- `git diff --check`：通过
- 官方 Trellis workflow 文档确认 Markdown workflow 是正确扩展面；未修改 upstream、全局 npm 或 `node_modules`

上述绿灯没有覆盖本轮 archive collision 和 parent-with-archived-children 两个场景。

## Docs SSOT

现有 durable docs 对 Round 18 修复已同步，但没有表达：

- initial archive destination 必须在 prepare 阶段不存在；
- parent task 的 children 兼容边界。

代码实际行为与 R2 完整路径预检合同、官方 parent/child lifecycle 不一致。Docs SSOT 结论：`fail`。

## Ledger 与范围

分类正确：

- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`

primary 与 close acceptance evidence 一致。两项 finding 均直接影响 #105 的 prepare/archive transaction，不能拆到 #98、#99 或 #101。

## 安全与部署

- 未修改 CI/CD、Docker、Compose、K8s/Kustomize、Helm、migration 或 Makefile。
- 未发现真实 token、secret、private key、`.env`、数据库 URL、客户数据或签名 URL。
- credential/userinfo 字符串仅存在于拒绝测试 fixture。
- 不需要应用部署、数据迁移或运行配置变更。

## 观察项

- 远端不存在 `v0.6.5-guru.3`，不得声称 stable-tag 安装已验证。
- 远端尚无当前工作分支。
- current-branch remote marketplace 与真实 GitHub E2E 仍须由 publish-time fail-closed verifier 完成。
- standalone pre-commit `check-phase2-check.sh` 在 post-commit 状态报告旧 HEAD/dirty metadata 属预期；Branch Review 使用的 post-commit audit 路径已确认 `errors=[]`。
- 当前工作树仅有 task metadata/reviews tail，无 non-metadata drift。

## 后续候选

0。两项 finding 都属于 #105 当前事务合同。

## 结论

Round 20 最终放行不通过。

- P0：`0`
- P1：`1`
- P2：`1`
- P3：`0`
- findings_count：`2`
- reuse_decision：`new-agent`

必须先修复 archive destination prepare 门禁和 parent/child lifecycle 兼容问题，补齐 production 测试与 durable contract，重新执行 Phase 2；本 agent 之后只能作为 finding owner 执行 closure，不能再次担任最终放行 reviewer。
