# Issue #97 Branch Review Round 4 最终放行审查

## 审查身份

| 字段 | 值 |
| --- | --- |
| `logical_role` | `最终放行审查代理` |
| `agent_id` | `/root/issue97_final_round4` |
| `reviewed_head` | `017b9f351bfbb90fcfca3a3935a9167de645b97c` |
| `round` | `4` |
| `reuse_decision` | `new-agent` |
| `findings_count` | `0` |

本技术身份未参与 Round 1、Round 2 或 Round 3，也不是任何 earlier finding owner、替换审查代理或闭环审查代理。本轮只执行最终独立审查，不修改实现、测试、durable docs、规划、Phase 2、assignment、review rollup 或 Gate artifact，也未运行任何 recorder/Gate 命令。

## 固定审查范围

- Repository：`castbox/guru-trellis`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/097-finish-summary-replaces-add-session`。
- Intake base：`ff8c03abb259c2a048626ea72e0bf57138db2c14`，对应 `origin/main`。
- Reviewed HEAD：`017b9f351bfbb90fcfca3a3935a9167de645b97c`。
- 完整 diff：`origin/main...HEAD`，62 个 tracked 文件，6726 insertions、2200 deletions。
- 工作树边界：除 task-local 未跟踪 Trellis 审查/检查/发布准备 metadata 外无 reviewed HEAD 后的实现漂移；source checkout 为 clean。
- Live scope：GitHub Issue #97 当前为 OPEN；只完成 task-local `finish-summary.json` 对 workspace journal/add_session 的替换，#100 backfill、#98 历史发现、#99 developer identity 保持非目标。

## 完整分支审查

### 需求、设计与实现

- `prd.md`、`design.md`、`implement.md` 已通过 schema `1.2`、`explicit-post-planning-review` 与 ambiguity review 的 post-planning approval；当前 planning validator 通过。
- Canonical workflow、companion、finish-summary schema、preset installer、platform overlays、dogfood copies、requirements、README 与 specs 对同一行为收敛：Guru Team finish 不调用 `add_session.py`，完成摘要归属当前 archived task，workspace journal 不作为 finish/readiness/context 证据。
- `finish-summary-index.json` 只承载 AI 审查判断；脚本只收集 Git、task、issue、artifact、时间、branch/path/ref 等确定性事实并执行 validator，未把产品判断转移到脚本。
- 正常 finish 写 initial summary，固定空 `pr_url`/`pr_refs`；PR 创建或恢复后只回写 archived task 的 summary URL/ref/safe paths，并以精确 metadata-only tail 提交、push、核对 remote SHA。
- `pr-readiness.json.publish_inputs` 固定 repo/base/head/reviewed HEAD/title/task-local body source/body SHA-256/draft/reviewed source，并以 canonical digest、Git blob、单次 artifact history、Gate HEAD 与祖先关系约束。Recovery command 只引用 archived readiness artifact，不重新接受 title/body/draft/base/validation override。
- Recovery 在 PR query/create 前重验 current branch、base、repo、current/remote HEAD、review gate、body/readiness 和 required marketplace evidence；随后严格执行 1 个 open PR 复用、0 个同参数仅创建一次、多个 fail closed。单次 create retry 再失败时保留 initial summary 并返回同一 recovery command。
- Git path snapshot 对 initial diff、initial untracked 与 final/recovery diff 失败统一写双空 paths，只追加一次批准的 fixed unavailable fact，移除 protected-filtering fact并重新派生 `retrieval_text`；错误输出、ref、路径与 basename 不进入摘要，path validator 继续 fail closed。
- raw paths 正常分支先排序去重，再过滤 `.trellis/workspace/**` 与 `.trellis/.runtime/**`；安全集合同时写入 `git.changed_paths` 与 `index.search_terms.paths`，固定 filtering fact 不披露具体路径或数量。

### Canonical、安装副本与升级门禁

- Canonical/dogfood companion、workflow、finish-summary schema、shared start、Codex hook 与 Cursor hook 均 byte-equal；overlay drift 检查通过。
- Shared `trellis-start` 只组合 phase、packages、active task 与 Git facts；Codex/Cursor session hooks 已删除 journal helper import/call。单元和 throwaway access guard 覆盖 workspace sentinel，不是读取后过滤。
- Throwaway 顺序固定为 preview 内容校验及 sidecar cleanup、initial switch、`trellis update --force`、marketplace workflow reapply、preset reapply、no-workspace sentinel、最终递归 `.new/.bak` gate；public-main sampling 已实际通过。
- Preset 写入 `.trellis/workspace/` ignore 与顶层 `session_auto_commit: false`，不再扫描/改写 workspace index 文案；官方 `task.py archive`、`add_session.py` 与 upstream 文件未修改。
- `git ls-files '.trellis/workspace/**'` 为空；完整 raw diff 保留 `.trellis/workspace/index.md`、`.trellis/workspace/wumengye/index.md`、`.trellis/workspace/wumengye/journal-1.md` 三条预期删除记录。

### 提交与发布准备

- 三条 work commit 均为中文 issue-bearing Conventional Commit，包含实质性的背景、变更、边界、验证与 `Refs #97`，未使用 close keyword：`53f265f`、`0abdc0f`、`017b9f3`。
- `issue-scope-ledger.json` 只把 #97 列为 close issue；#53、#96、#100 为 related，#98、#99 为 follow-up。`pr-body.md` 只使用 `Closes #97`，分类与 live issue scope 一致。
- PR body 如实记录 302/36/79/31+1、public-main throwaway、workspace tracking、Docs SSOT、安全与部署结论，没有把 current-ref remote verifier 写成已完成。

## 前序问题闭环复核

### Round 1 五项

1. No-workspace context：已通过 shared/Codex/Cursor canonical overlay、fresh sentinel 与 access guard 闭环；未发现 journal open/enumerate/read/count/output 回归。
2. Immutable publish inputs：已由 committed `pr-readiness.json.publish_inputs`、digest/blob/history/Gate/remote validators 与跨调用 mutation tests 闭环。
3. Snapshot failure：已实现双空 paths、唯一 fixed unavailable fact、不披露、retrieval 重派生及 path fail closed；Round 2 发现的精确文案偏差也已在 Round 3 关闭。
4. Durable flow Docs SSOT：`guru-team-trellis-flow.md` 已完整表达 AI index、initial summary、marketplace verifier、0/1/>1 recovery、PR URL metadata tail 和 no-workspace context，不再把 Guru Team finish 描述为 archive+journal/add_session。
5. Throwaway sidecar：preview sidecar 显式清理，switch/update/workflow reapply/preset reapply 后执行最终递归 `.new/.bak` scan，已闭环。

### Phase 2 两项 P3

- Update 后 marketplace workflow reapply 已加入实际脚本顺序并由 preset regression/public-main throwaway锁定。
- Public-surface test 已排除 `__pycache__`/`.pyc`；Phase 2 在 compile 后重跑 canonical 302 与 preset 36 仍通过。

### Round 2 P2

- `FINISH_SUMMARY_PATH_SNAPSHOT_UNAVAILABLE_CONTRACT` 逐字段等于批准的 `design.md` 4.4 对象，canonical/dogfood companion byte-equal。
- Initial diff、initial `git ls-files --others`、final/recovery diff 三类真实失败 fixture 均断言完整对象、双空 paths、无 filtering fact、不披露、retrieval 全值相等及受保护路径 fail closed。
- Round 3 由同一 finding owner 以 `reuse-for-closure` 完成闭环，当前完整分支无该问题回归。

## Findings

无 P0、P1、P2 或 P3 finding。

`findings_count=0`。

## 观察项

- 当前分支尚未 push；默认 pinned `v0.6.5-guru.3` 的远端 tag 查询无结果。真实 current-ref remote marketplace verifier 必须在正式 publish push 后运行，并把 ledger 中 pending evidence 替换为 passed evidence；本地和 public-main sampling 不替代该发布门禁。
- Task-local `review.md` 与旧 `review-gate.json` 在本轮开始时仍反映 final pending/earlier findings，这是 Branch Review Gate recorder 尚未执行的预期前置状态，不是实现缺陷。本报告只提供 final AI judgment，后续应由主会话登记 Round 4、更新 rollup，再运行 assignment/Gate validator。
- `phase2-check.json.head` 为提交前 HEAD `0abdc0f`，其 `dirty_paths` 精确覆盖随后提交 `017b9f3` 的三个 tracked 路径和 task metadata；这是 post-commit audit 语义。Fresh Phase 2 及 Round 3 已重新验证第三个 commit，无 stale gap。

## 后续候选

- #100：为既有 archived tasks 回填 finish-summary，保持 related/non-close。
- #98：消费 finish-summary 做历史上下文分级发现，保持 follow-up。
- #99：取消 developer identity 前置，保持 follow-up。
- 未发现需要新增 issue 的 current-scope 缺陷或独立后续项。

## Docs SSOT 判断

结论：`PASS`。

- Live #97、approved task design、canonical workflow、finish-summary schema、workflow/data/companion/preset specs、root/workflow/preset README、`requirement-main.md`、`guru-team-trellis-flow.md`、platform entries 与 dogfood copies表达同一 finish-summary/no-workspace/immutable recovery/snapshot failure/throwaway 合同。
- 官方 Trellis 文档确认 custom workflow 行为由 `.trellis/workflow.md` 的 Markdown runtime contract承载，spec marketplace 不应承载 active task/runtime 私有状态；当前实现使用官方 extension surface，未 fork upstream。
- Task artifacts 只保留规划、审批、实现交接、Phase 2 与 review evidence，不替代 durable docs。

## 部署与安全判断

- 完整 diff 未修改 GitHub Actions/CI/CD、Dockerfile/Compose、Kubernetes/Kustomize、Helm、数据库 migration/seed/backfill 或 Makefile，也未新增 API、服务、worker、定时任务、队列、数据库结构或业务运行时部署入口。
- 变更影响 Guru Team workflow/preset 安装、session-start context 与 finish/publish metadata 控制面；需要在 publish 时执行真实 current-ref remote marketplace verifier，但不需要业务部署、数据库迁移或 release tag。
- Added-line secret scan 只命中测试 sentinel、变量名和负向检查文本；未发现 token、真实 secret、private key、签名 URL、`.env`、数据库 URL、客户数据或 workspace journal 内容迁移。
- 三个 workspace 文件仅从 Git tracking 删除；摘要过滤合同不披露被过滤路径 basename、数量或内容。

## 独立验证

- `gh issue view 97 --repo castbox/guru-trellis --comments --json ...`：live issue OPEN，scope、字段合同、recovery、snapshot failure 与 acceptance criteria 已复读。
- Trellis 官方 `index.md`、`advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`：扩展边界与本实现一致。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：302 tests PASS。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：36 tests PASS。
- `PublishBoundaryTest + FinishSummaryContractTests`：79 tests PASS。
- `python3 -S FinishSummaryContractTests`：31 PASS，1 项仅因 optional `jsonschema` 不可用而 skip。
- `check-planning-approval.sh`：PASS；`check-workspace-boundary.sh`：PASS，source checkout 无可疑 task artifact。
- `check-dogfood-overlay-drift.sh`：PASS；六组关键 canonical/dogfood `cmp`：PASS。
- 全部 tracked Bash `bash -n`、repository JSON `jq empty`、`git diff --check origin/main...HEAD`：PASS。
- Recursive `.new/.bak` scan：空；workspace Git index：空；base-to-HEAD workspace diff：三条预期 `D`。
- 远端 `v0.6.5-guru.3` tag：不存在，符合 PR body 的 publish 前 pending 风险说明。

## 结论

最终放行审查：`PASS`，`findings_count=0`，reviewed HEAD 为 `017b9f351bfbb90fcfca3a3935a9167de645b97c`。

本轮覆盖 live Issue #97、post-planning-approved task contracts、完整 `origin/main...HEAD`、canonical/preset/overlay/dogfood、companion/schema、tests、durable Docs SSOT、三条 commit、前序 finding lifecycle、Phase 2 evidence、workspace tracking、close/ref/follow-up 语义以及部署与安全影响。全部 current-scope finding 已闭环且独立验证无新回归，因此证据足以由主会话登记 Round 4 并记录 Branch Review Gate；真实 current-ref remote marketplace verification 仍按设计留在 push 后、PR create 前的 fail-closed publish gate。
