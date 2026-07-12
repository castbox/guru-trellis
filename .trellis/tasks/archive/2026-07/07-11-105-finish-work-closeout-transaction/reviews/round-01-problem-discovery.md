# Issue #105 Branch Review 原始报告

## 审查身份

- 逻辑角色：问题发现审查代理
- 技术身份：`/root/branch_review_105_round1`
- 审查方式：独立只读 Branch Review
- reviewed_head：`b900a3c63be150246146ef0d7d22b12822c5324a`
- diff_range：`origin/main...HEAD`
- base：`3dec302206783fe4ac1296066e9a1789c995d58b`
- findings_count：`4`
- 结论：`fail`

## 范围与方法

已读取 live GitHub issue #105、`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`phase2-check.json`、`issue-scope-ledger.json`、HEAD 版本 `agent-assignment.json`，并审核完整 47 文件 diff。

覆盖 closeout plan、dry-run/formal digest、marketplace evidence、draft PR、final projection、archive transaction、active/archive recovery、三方 HEAD、#97/#98 兼容、失败矩阵、canonical/dogfood、workflow/spec/docs/platform entry、schema 与测试。未修改文件，未运行 recorder/review-gate companion 命令。

## 发现项

### P0：0

### P1：4

#### P1-1：draft PR 复用与转 ready 没有绑定 immutable title/body 和最终 summary PR identity

证据：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:11109` 的 PR 查询只读取 `number,url,headRefName,baseRefName,headRefOid,isDraft`，没有读取 `title`、`body`。
- 同文件 `:11144` 的 `ensure_closeout_draft_pr()` 对唯一 draft 直接复用，只检查 draft/head/base。
- 同文件 `:11392` 的 `ensure_closeout_pr_ready()` 只检查 local/remote/PR HEAD 与 draft 状态，没有比对 plan/readiness 的 title/body digest，也没有比对 archived `finish-summary.json.github.pr_url` 指向同一 PR number。
- `test_guru_team_trellis.py:9344` 只覆盖多 PR 与提前 ready，未覆盖 title/body 被改写、旧 draft 内容不匹配、原 draft 被关闭后同分支新建另一 PR。

影响：

手工或外部修改 draft title/body 后，流程仍可把未审核内容转 ready；同 head/base 的既有无关 draft 也会被接管。archive 后若原 PR 被替换为另一 open draft，新 PR 可被转 ready，但 immutable summary 仍指向旧 PR，破坏 #97/#98 的准确 PR identity。

建议：

PR 查询加入 title/body；复用、final projection、archived recovery和转 ready 前均校验 title、body SHA、repo/head/base/draft。archive 后还必须从 final summary 解析 PR number/URL，并要求与当前唯一 PR 完全一致。补充上述篡改与替换场景测试。

#### P1-2：archive transaction 只绑定路径集合，没有绑定 evidence commit 到 archive commit 的文件内容

证据：

- `guru_team_trellis.py:11252` 的 archive 校验只比较路径集合。
- 同文件 `:11330` 的 archive layout 只比较文件名，并仅深验 summary、ledger/marketplace；未校验 `pr-body.md`、review gate、review reports、readiness 等文件内容。
- 同文件 `:11418` 的恢复路径会接受完整 dirty path set 并直接提交，没有比较 archived blob 与 evidence commit 中 active blob。
- `test_guru_team_trellis.py:9080` 的 real-Git fixture 只断言 parent/path；`:9168` 还 mock 掉 archive layout 校验。

影响：

`task.py archive` 已移动但尚未提交时，修改任一原本已 dirty 的归档文件不会改变 path set。恢复流程会把被改写的 `pr-body.md`、review evidence 或 readiness 一并提交、push并转 ready，绕过已验证 final projection 和 immutable evidence。

建议：

对所有 `tracked_move_paths` 比较 evidence commit active blob 与 archive commit archive blob。除 `task.json` 外必须 byte-for-byte 相同；`task.json` 仅允许官方 archive 的确定性状态字段变化。为 summary 保留现有模板 digest。增加真实 Git tamper recovery 用例。

#### P1-3：durable Docs SSOT 和 canonical/dogfood workflow 仍保留旧 archive-first 合同

证据：

- `.trellis/spec/workflow/data-contracts.md:110` 仍写 initial empty PR summary、archive 后创建、PR 后重写；`:126` 紧接着又写新的一次性 final summary，单一文档自相矛盾。
- `.trellis/spec/workflow/companion-scripts.md:165` 仍允许 archive 后 rewrite gate 路径；`:427` 仍允许 post-PR archived summary tail。
- `.trellis/spec/workflow/workflow-contract.md:489` 仍规定 evidence commit 只有 verifier artifact + ledger，和新 plan/readiness/evidence allowlist 冲突。
- `trellis/workflows/guru-team/workflow.md:317`、`:929`、`:942` 仍称 PR publish 在 archive 和 initial summary 后触发，与同文件 `:1361` 的新事务顺序冲突；dogfood `.trellis/workflow.md` 同步复制了该冲突。

影响：

这些 Markdown 是 AI 运行时流程合同。canonical/dogfood byte equality 虽通过，但只是同步了同一组冲突；不同入口可能继续执行旧 archive-first、empty-summary、post-PR tail 语义，Docs SSOT 不能判定为通过。

建议：

从 durable specs 和 canonical workflow 中删除或改写全部旧合同，不要在后文追加第二套规则。增加旧术语/旧顺序负向扫描测试，并同步 dogfood。

#### P1-4：12 阶段 failure injection 主要断言 mock 自建状态，不能证明生产状态机满足验收

证据：

- `test_guru_team_trellis.py:9584` 定义预期状态。
- `:9623` 至 `:9682` 的 mock 自行更新同一 `state`。
- `:9693` 至 `:9727` mock 掉 prepare、identity、verifier、evidence commit、draft、projection、archive、ready 等生产边界。
- `:9740` 最终比较的是 mock 写入的 state，而不是实际 task locator、Git index、remote 或 PR 状态。

影响：

即使生产函数未正确更新 task status、dirty/staged paths、HEAD 或恢复动作，该矩阵仍可通过。Phase 2 中“P1-3 已闭环”的证据不足，issue #105 明确要求的逐阶段真实失败状态没有完整验证。

建议：

使用临时真实 Git repo/bare remote 和可控 fake `gh`/verifier，在生产 `cmd_finish_work()` 入口注入失败；只 mock 外部响应，不 mock 被审查的 transition 函数。逐阶段从文件系统、Git index/log/remote 和 fake PR store 读取状态断言。

### P2：0

### P3：0

## Docs SSOT 判断

`fail`。新事务合同已经写入主要章节，但旧合同仍在同一 durable spec 与 canonical workflow 中生效，不能认定 SSOT 收敛。

## 部署与安全判断

- 未变更 CI/CD、Docker/Compose、K8s/Kustomize、数据库 migration、Makefile 或部署资产。
- `publish.draft` 配置变化属于 workflow 发布行为，不涉及服务部署。
- 未发现 token、secret、私钥、`.env`、客户数据或签名 URL 泄露。
- 但 P1-1 可发布未审核 PR 内容，P1-2 可把篡改后的审查/发布 artifact 纳入 archive commit，因此发布安全门禁未通过。

## 验证证据

独立执行并通过：

- canonical Python：`359/359`
- preset Python：`36/36`
- Draft 2020-12 三个变更 schema：通过
- `git diff --check origin/main...HEAD`：通过
- canonical/dogfood Python、workflow、schema 与五个平台入口 byte equality：通过

Phase 2 artifact 另记录 targeted `25/25`、throwaway init/preview/switch/update/reapply 通过。上述通过结果未覆盖四项 finding。

Issue Scope Ledger 分类正确：仅关闭 #105；#53/#96/#97/#100 为 related；#98/#99/#101 为 follow-up。

## 观察项

- worktree 当前仅有审查调度造成的 `agent-assignment.json` 未提交变化；本报告严格以 HEAD 版本审查。
- 远端尚无 `v0.6.5-guru.3` tag，当前分支 remote marketplace 和真实 GitHub closeout E2E 尚未执行；不得声称稳定 tag 路径已验证。

## 后续候选

0。四项均属于 #105 当前范围，不能转为 observation 或 follow-up。

## 结论

Branch Review Gate 不通过。必须修复四项 P1、补真实测试、清理 Docs SSOT 冲突并形成新提交，再由问题闭环审查代理复核完整 `origin/main...HEAD`。
