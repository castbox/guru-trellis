# Issue #97 Branch Review Round 5 最终放行审查

## 审查身份

| 字段 | 值 |
| --- | --- |
| `logical_role` | `最终放行审查代理` |
| `agent_id` | `/root/issue97_final_round5` |
| `reviewed_head` | `fd310e15b08a2a29d253a1308b38816db7bc005d` |
| `round` | `5` |
| `reuse_decision` | `new-agent` |
| `findings_count` | `0` |

本技术身份未参与 Round 1 至 Round 4，也不是任何前序 finding owner、闭环代理或旧 final reviewer。本轮只执行独立最终审查；未修改实现、测试、spec、规划、Phase 2、assignment、review rollup、Gate、finish-summary index、PR body 或 readiness，未运行 recorder、Gate、finish、archive、commit、push 或 PR 命令。

## 固定审查范围

- Repository：`castbox/guru-trellis`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/097-finish-summary-replaces-add-session`。
- Intake base：`ff8c03abb259c2a048626ea72e0bf57138db2c14`，本地 `origin/main` 与该 SHA 一致。
- Reviewed HEAD：`fd310e15b08a2a29d253a1308b38816db7bc005d`。
- 完整范围：`origin/main...HEAD`，62 个 tracked 文件，6872 insertions、2200 deletions，4 条 work commit。
- Live scope：GitHub Issue #97 为 OPEN；只完成 task-local `finish-summary.json` 对 workspace journal / `add_session.py` 的替换。#100 backfill CLI、#98 历史发现、#99 developer identity 解耦保持非目标。
- 工作树边界：除 task-local 未跟踪 Trellis evidence 外，无 reviewed HEAD 后的 tracked/implementation drift；Git index 为空，source checkout 无 task artifact 漂移。

## Post-Gate P1 闭环复核

Formal finish 暴露的 P1 根因成立：合法路径 `.trellis/guru-team/extension.json` 与 `trellis/guru-team-extension.json` 经删除标点的通用文本规范化后身份相同，旧 validator 因而把两个不同 Git path 误判为 duplicate，阻断 initial `finish-summary.json`。

修复在 `fd310e1` 中完整承接该根因：

- `finish_summary_string_array_errors(..., exact_identity=True)` 只对 path-bearing arrays 使用 exact string identity；`index.search_terms.paths` 与 `backfill.source_artifacts` 已接入。
- `git.changed_paths` 继续通过 `sorted(set(...))` 执行 exact string 排序去重；最终 validator 要求 `index.search_terms.paths` 与其完全相等。
- `index.affected_surfaces[].paths` 使用 exact duplicate validator；surface composite fingerprint 对 `kind`、`name`、`change` 保留 normalized semantic identity，对 `paths` 保留 exact list identity。
- Contract composite fingerprint 对 `contract`、`before`、`after` 保留 normalized semantic identity，对 `source_artifact` 保留 exact path identity。
- 非路径 `changed_behavior`、commands/config/schema/symbol/phrases 等 semantic/search-token arrays 仍使用 normalized duplicate 门禁，没有因 P1 修复放宽。
- JSON Schema 原有 `uniqueItems: true` 使用 exact JSON value identity，与修复后的 Python validator 同构，无需 schema 结构变更。

独立构造验证把上述两条真实 collision paths 同时写入 `git.changed_paths` 与 `index.search_terms.paths`，并拆成两个除 path 外语义相同的 affected surfaces：Python validator 为 0 errors，Draft 2020-12 JSON Schema 为 0 errors，两个字段均逐字保留两条路径。进一步验证：

- 两个只在 `source_artifact` 路径上不同、其余语义等价的 contract 不被 composite fingerprint 折叠；完全相同 contract 仍被拒绝。
- `backfill.source_artifacts` 接受上述两个 exact-distinct paths；完全相同 path 同时被 Python 与 JSON Schema 拒绝。
- path/search/surface exact duplicate 被拒绝；`重复行为。` 与 `重复 行为!` 这类非路径 normalized duplicate 仍被拒绝。

因此 formal finish P1 的生成路径、Python validator、JSON Schema、surface/contract composite identity 与 backfill 分支均已闭环，未发现旁路或兼容性回归。

## 完整分支审查

### Finish-summary 与 no-workspace 合同

- Canonical schema 同时覆盖 normal `guru-team.finish-work` 与 #100 `guru-team.finish-summary-backfill` 数据分支；Python validator 校验字段集合、类型、长度、数量、枚举、SHA/issue/PR、path 净化、duplicate、artifact link 与 derived facts。
- `finish-summary-index.json` 只承载 AI 已审查的 problem/outcome/behavior/surface/contract/search judgment；companion 只注入 task、Git、issue ledger、artifact、UTC、branch/path/ref 等确定性事实并派生 `retrieval_text`。
- Guru Team formal finish 使用官方未修改的 `task.py archive`，在 archived task 写 initial summary；未修改官方 `.trellis/scripts/task.py` 或 `.trellis/scripts/add_session.py`，Guru Team companion 中不存在 `add_session.py` 调用。
- Shared `trellis-start` 只读取 phase、packages、active task 与 Git facts；Codex/Cursor session hook 已删除 workspace journal helper 的 import/call。单元测试和 throwaway audit hook 均从 open/listdir/scandir 层阻断 workspace access，证明不是读取后过滤。
- `.gitignore`、`.trellis/.gitignore` 与 preset installer 均固定 workspace ignore；`.trellis/config.yaml` 与 preset materialization 固定顶层 `session_auto_commit: false`。Preset 不再扫描或改写 workspace index。
- `git ls-files '.trellis/workspace/**'` 为空；raw base-to-HEAD diff 精确保留三个预期删除记录，未迁移 journal 内容。

### 路径过滤与 snapshot-unavailable

- 正常路径 snapshot 先按 exact path 排序去重，再过滤 `.trellis/workspace/**` 和 `.trellis/.runtime/**`；安全集合同时写入 `git.changed_paths` 与 search paths。
- 发生过滤时只追加一个固定 `finish-summary protected path filtering` fact，内容不披露 path、basename、数量或 stderr；无过滤时该 fact 不存在。
- Initial diff、initial untracked enumeration、final/recovery diff 任一失败时，两个 path arrays 同时为 `[]`，过滤 fact 被移除，只保留一次批准的固定 unavailable fact，并重新派生 `retrieval_text`。
- Schema 与 Python validator 在正常、过滤和 unavailable 分支均继续拒绝绝对路径、parent segment、反斜杠、CR/LF、workspace/runtime protected prefixes，没有降级例外。

### Immutable publish 与 recovery

- `pr-readiness.json.publish_inputs` 固定 repo、base/head branch、Gate reviewed HEAD、exact title、task-local body source/body SHA-256、draft、reviewed source 与 canonical snapshot digest；formal publish/recovery 校验 committed blob、单次 artifact history、snapshot/body digest、Gate ancestor、repo/base/head/current/remote identity。
- Recovery command 只接受 archived readiness artifact 与 task/repo/remote locator；title/body/draft/base/validation override 在 PR query 前失败。
- Open PR 状态机固定为：1 个复用；0 个用 immutable inputs 仅 create 一次；多个 fail closed。客户端失败但服务端已创建的 race 通过 query-first 复用；单次 retry 再失败时保持 initial empty URL/ref 并返回同一 recovery command。
- PR URL/ref/safe paths rewrite 后只允许当前 archived task 的 `finish-summary.json` metadata tail；代码、配置、schema、workflow、preset、docs、test、CI/CD、部署、migration 与 Makefile 路径均不能进入该提交。
- Marketplace-required 正常 publish 在 push 后执行 remote verifier；recovery 只验证并复用既有 passed artifact/ledger/HEAD/Gate evidence，不能重跑 verifier。

### Marketplace、升级与安装

- Canonical workflow、companion、finish-summary schema、shared start、Codex hook、Cursor hook 与 dogfood copies 六组逐字相等；overlay drift 为零，递归 `.new/.bak` 扫描为空。
- 独立 public-main sampling throwaway 实际完成：fresh init、local preset install、preview sidecar 内容校验与删除、initial workflow switch、`trellis update --force`、marketplace workflow reapply、preset reapply、no-workspace access audit、final sidecar gate。
- Throwaway 中 `finish-work` direct call 与 `publish-pr` direct call 均在副作用前阻塞；安装产物含 schema、companion、ignore、`session_auto_commit: false` 与 public extension contract。
- 当前分支尚未 push，故 public-main sampling 不是 current-ref remote marketplace evidence；正式 publish 仍必须在 push 后运行 current-ref verifier并把 ledger pending evidence替换为 passed evidence。

### 提交、发布说明与 issue scope

- 四条 commit `53f265f`、`0abdc0f`、`017b9f3`、`fd310e1` 均通过 issue-bearing Chinese Conventional Commit validator，无 close keyword。
- `issue-scope-ledger.json` 只把 #97 列为 `close_issues`；#53、#96、#100 为 related；#98、#99 为 follow-up。`pr-body.md` 只写 `Closes #97`，与 live scope 一致。
- PR body 的 305 canonical、36 preset、82 targeted、`python3 -S` 34 + 1 optional skip、251 tracked JSON 数字均由本轮独立重跑或计数确认；remote verifier 明确写为 pending，没有虚报。

## 前序问题生命周期

| 来源 | 问题 | 当前状态 | 本轮证据 |
| --- | --- | --- | --- |
| Round 1 | no-workspace context | 已关闭 | shared/Codex/Cursor no-read 实现、access guard、throwaway PASS |
| Round 1 | immutable publish inputs | 已关闭 | readiness blob/history/digest/identity 与 mutation tests PASS |
| Round 1 | snapshot failure 合同 | 已关闭 | 双空 paths、固定 fact、不披露、retrieval 重派生 tests PASS |
| Round 1 | durable flow Docs SSOT | 已关闭 | requirements/workflow/spec/README/canonical/dogfood 一致 |
| Round 1 | throwaway sidecar 遗留 | 已关闭 | preview cleanup 与 final recursive gate PASS |
| Phase 2 | update 后未重应用 workflow | 已关闭 | 固定 update -> workflow reapply -> preset reapply 顺序 PASS |
| Phase 2 | `__pycache__` public-surface 漂移 | 已关闭 | compile 后 canonical 305 再次 PASS |
| Round 2 | unavailable fixed fact 文本偏差 | 已关闭 | `017b9f3`、Round 3 closure 与三类 failure tests PASS |
| Round 4 | 仅覆盖旧 HEAD `017b9f3` | 已失效 | 本 Round 5 完整覆盖 `origin/main...fd310e1` |
| Formal finish | normalized path collision P1 | 已关闭 | exact identity code、真实 collision Python/Schema 与 full regression PASS |

前序 raw reports：

- [Round 1 replacement finding](./round-001-replacement-finding.md)
- [Round 2 closure](./round-002-closure.md)
- [Round 3 closure](./round-003-closure.md)
- [Round 4 old-HEAD final](./round-004-final.md)

## Findings

无 P0、P1、P2 或 P3 finding。

`findings_count=0`。

## 观察项

- 旧 `review-gate.json` 与 `pr-readiness.json` 绑定 `017b9f3`，且 readiness 中 body digest 与当前 `pr-body.md` bytes 不同；它们在当前 HEAD 下是预期 stale evidence，不能直接发布。主会话必须先登记 Round 5、重录 current-HEAD Branch Review Gate；normal closeout 随后重建 current readiness snapshot。
- Latest fresh `phase2-check.json.head` 为 `017b9f3`，其 `dirty_paths` 精确覆盖第四个 commit 的 4 个 tracked paths；checker `/root/issue97_phase2_path_collision` 对这些 bytes 与完整 #97 范围给出 P0/P1/P2/P3=0。该结构符合 workflow 的 post-commit audit 合同，本轮又独立重跑关键验证。
- 默认 pinned `v0.6.5-guru.3` 尚未发布且不属于本任务创建范围；正式 publish 必须使用已 push current ref 的 remote verifier，不能用本轮 public-main sampling 替代。

## 后续候选

- #100：既有 archived tasks 的 finish-summary backfill CLI，保持 related/non-close。
- #98：基于 finish-summary 的历史上下文分级发现，保持 follow-up。
- #99：developer identity 前置解耦，保持 follow-up。
- 未发现需要新增 issue 的 current-scope 缺陷。

## Docs SSOT 判断

结论：`PASS`。

- 新增 `.trellis/spec/workflow/data-contracts.md` 的 domain-specific duplicate identity 合同与 canonical/dogfood companion、JSON Schema、tests、PR body、finish-summary index、implementation handoff 一致。
- `docs/requirements/guru-team-trellis-flow.md`、`requirement-main.md`、workflow/spec/README/platform entries 已收敛 finish-summary、no-workspace、immutable recovery、snapshot failure、marketplace/update/reapply 合同。
- 官方 custom workflow 文档确认 workflow Markdown 是运行时流程控制面；官方 spec template marketplace 文档禁止 active task、workspace/runtime 私有状态与平台 prompt 进入 reusable spec template。当前实现使用官方扩展面，未 fork upstream。
- Formal finish 失败现场、task 恢复、旧 review/Gate 和验证数字只保留为 task history；长期 exact path identity 规则已合并到 durable spec、canonical companion 与 tests，没有让 task artifact 成为平行 SSOT。

## 部署与安全判断

- 完整 diff 未触碰 GitHub Actions/CI/CD、Dockerfile/Compose、Kubernetes/Kustomize、Helm、数据库 migration/seed/backfill 或 Makefile；未新增 API、服务、worker、cron、queue、数据库结构或业务部署入口。
- 影响范围是 Guru Team workflow/preset 安装、session-start context 与 finish/publish metadata 控制面；无需业务部署、数据库迁移或 release tag，但 publish 前必须完成 current-ref remote verifier。
- Added-line secret review 的命中均为测试 sentinel、变量名、固定禁止词或负向安全断言；未发现 token、真实 secret、private key、签名 URL、`.env` 内容、数据库 URL、客户数据或 workspace journal 内容迁移。
- Protected/snapshot fixed facts 不披露被过滤 path、basename、数量、stderr 或 ref。

## 独立验证

- Live `gh issue view 97`：Issue OPEN；方案 A、0/1/>1 recovery、snapshot failure、workspace tracking 与非目标边界一致。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：305 PASS；`py_compile` 后再次 305 PASS。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：36 PASS。
- `PublishBoundaryTest + FinishSummaryContractTests`：82 PASS。
- `python3 -S FinishSummaryContractTests`：34 PASS，1 个 optional `jsonschema` skip。
- 真实 collision direct check：Python validator、Draft 2020-12 JSON Schema、surface/contract/backfill exact identity、exact duplicate rejection、semantic normalized duplicate rejection 全部 PASS。
- Python compile、全部 tracked Bash syntax、251 个 tracked JSON 与 task-local JSON：PASS。
- Planning approval、workspace boundary、commit message、overlay drift、六组 canonical/dogfood byte equality、recursive sidecar、`git diff --check`、workspace tracking：PASS。
- Public-main sampling throwaway：preview cleanup、switch、update、workflow reapply、preset reapply、no-workspace access audit、final sidecar gate PASS。
- Source checkout 无可疑 task artifact；review worktree 无 tracked/staged drift。

## 结论

最终放行审查：`PASS`，`findings_count=0`，reviewed HEAD 为 `fd310e15b08a2a29d253a1308b38816db7bc005d`。

本轮完整覆盖 formal finish 暴露的 exact path identity P1、live Issue #97、approved planning contracts、`origin/main...HEAD` 全量 diff、canonical/preset/overlay/dogfood、schema/companion/tests、no-workspace context、immutable publish/recovery、protected/snapshot paths、marketplace/update/install、Docs SSOT、四条 commit、issue scope、部署与安全。P1 与所有前序 finding 均已闭环，独立验证未发现新的 P0-P3，因此当前 HEAD 足以由主会话登记 Round 5 并重录 Branch Review Gate；旧 Gate/readiness 不得复用，真实 current-ref remote marketplace verification 仍保留在正式 push 后、PR create 前的 fail-closed publish gate。
