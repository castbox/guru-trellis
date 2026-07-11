# Issue #97 Branch Review Round 2 问题闭环审查

## 审查身份

| 字段 | 值 |
| --- | --- |
| `logical_role` | `问题闭环审查代理` |
| `agent_id` | `/root/issue97_closure_round2` |
| `reviewed_head` | `0abdc0f97911c28b96439f2ba2c1dd3c1aa5bfaf` |
| Diff 范围 | `origin/main...HEAD` |
| `round` | `2` |
| `from_round` | `1` |
| `reuse_decision` | `new-agent` |
| `findings_count` | `1` |

本代理未参与 earlier review rounds。`agent-assignment.json.reuse_decisions[]` 已记录从 round 1 到 round 2 的 `new-agent` 关系、相同 reviewed HEAD 与非空原因。本轮只负责验证 round 1 finding 的闭环，不具备 `最终放行审查代理` 身份；由于本轮仍有 finding，本轮同时成为新的 finding owner，后续必须先由新的 closure round 显式闭环，不能直接派发 final reviewer。

## 审查范围

- 复核 live GitHub issue #97、官方 Trellis custom workflow 与 spec marketplace 文档、仓库 `AGENTS.md` 和 `.trellis/workflow.md` Branch Review Gate 合同。
- 读取 `prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`implementation-handoff.md`、`phase2-check.json`、`issue-scope-ledger.json`、`pr-body.md`、research、durable specs、round 1 raw report 与 `review.md`。
- 审查 base `origin/main` 到固定 HEAD 的完整 diff、两个 commits、metadata-only working tree，以及 workflow、companion、schema、preset、overlay、平台入口、requirements、README、测试、配置和 workspace 删除记录。
- 复核 CI/CD、Docker/Compose、Kubernetes/Kustomize、Helm、数据库 migration、Makefile、运行时配置、发布与安全影响。

## Round 1 问题闭环状态

### 1. Shared/Codex/Cursor 启动上下文读取 workspace journal

状态：已闭环。

- shared `trellis-start` 只列出 phase、packages、current task 与 Git facts，明确禁止 bare `get_context.py` 及任何 workspace journal 打开、枚举、读取、计数和输出。
- canonical/dogfood Codex 与 Cursor SessionStart overlay 已删除 `get_active_journal_file`、`count_lines` 与 `Journal:` 分支；canonical 与 dogfood 副本 byte-equal。
- preset 测试在 fresh 临时仓库写入带秘密 basename/content 的 workspace sentinel，以 `Path.read_text` / `Path.iterdir` guard 执行 Codex/Cursor compact context builder；输出不含 sentinel、内容或旧 line-count 信号。
- throwaway verifier 通过 Python audit hook 阻断 `open`、`os.listdir`、`os.scandir` 对 workspace 的访问，并实际执行 shared phase/packages/current-task 命令。审查代理另以 audit hook 执行完整 Codex/Cursor hook 入口，两个入口均无 workspace access event，也无 `Journal:` 输出。

### 2. Recovery 未绑定不可变 PR publish inputs

状态：已闭环。

- `pr-readiness.json.publish_inputs` 固定 repo/base/head/reviewed HEAD/title/body source/body SHA-256/draft/reviewed source，并以 canonical JSON SHA-256 绑定 object。
- normal publish 与 recovery 在任何 PR query/create 前校验 task-local path、完整 keys、snapshot/body digest、dirty/staged、当前 HEAD Git blob、单次 artifact commit history、review gate HEAD 及祖先关系、task repo/base/head identity 和 current/remote HEAD。
- recovery command 只携带 archived readiness artifact 与固定 task/repo/remote locator；CLI title/body/draft/base/validation override 在 PR query 前 fail closed。
- 0/1/>1 query-first、单次 same-input create、已有 PR 复用、多个 PR fail closed、verifier evidence 只校验复用，以及 retry failure 保留 initial summary 均有定向测试。

### 3. Git path snapshot 失败合同

状态：未完全闭环，见本报告 P2 finding。

- initial diff、initial `git ls-files --others`、final/recovery diff 返回非零时，代码已经返回空路径集合和 `snapshot_unavailable=true`；initial/final summary 同步写空 `git.changed_paths` 与 `index.search_terms.paths`，移除 filtering fact，并重新派生 `retrieval_text`。
- schema 与 Python validator 对 path 继续 fail closed，错误 stdout/stderr/ref 不进入 summary。
- 但是 recorder 写入的固定 unavailable fact 文本与用户重新批准的 `design.md` 精确合同不一致，测试也没有锁定完整对象，因此该 round 1 finding 不能判定为闭环。

### 4. `guru-team-trellis-flow.md` Durable Docs SSOT

状态：实现主线已闭环，但整体 Docs SSOT 因 finding 3 的 task-design/code 冲突仍为 FAIL。

- `docs/requirements/guru-team-trellis-flow.md` 已重写总图、finish/publish 时序、dry-run、Artifact 责任、companion 边界与讲解主线，包含 AI index、initial finish-summary、immutable readiness、marketplace verifier、0/1/>1 recovery、PR URL metadata tail 和 no-workspace 启动上下文。
- `requirement-main.md`、README、workflow/data/companion/preset specs 与 canonical workflow 使用相同主线；未发现仍把 Guru Team finish 描述为 archive 后调用 `add_session.py` 的 durable 文档。

### 5. Throwaway preview/switch/update/reapply sidecar 门禁

状态：已闭环。

- verifier 校验预期 `.trellis/workflow.md.new` 后显式删除，随后执行 initial switch、`trellis update --force`、marketplace workflow reapply、preset reapply，最后递归扫描全部 `.new` / `.bak`。
- Phase 2 发现 update 后 workflow 未重新应用的 P3 已修复；public-main sampling throwaway 实际到达最终 sidecar gate并通过。当前 worktree 递归 sidecar 扫描为空。

## Phase 2 新增问题复核

- update 后未重新应用 marketplace workflow：已闭环。脚本顺序固定为 update -> workflow reapply -> preset reapply -> final sidecar scan，preset regression test 锁定该顺序。
- public-surface test 误读 `__pycache__/*.pyc`：已闭环。扫描排除 Python bytecode/cache；审查代理重跑 canonical suite 为 302 tests PASS。

## Findings

### P2 - Snapshot-unavailable 固定事实偏离批准版精确合同

- 路径与行号：`.trellis/tasks/07-10-097-finish-summary-replaces-add-session/design.md:107`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:177`、`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:9447`。
- 批准合同：`design.md` 明确要求唯一 fixed fact 的 `before` 为 `Git 变更路径快照未成功完成。`，`after` 为 `完成摘要已使用空路径集合，未写入未验证路径。`。
- 当前实现：canonical constant 使用 `Git path snapshot was unavailable.` 与 `完成摘要未记录 path 字段；其它合同与检索字段保持可验证。`。这不是文案格式差异，而是 recorder 对外持久化 contract fact 的值与 post-planning approval 精确 schema 行为合同不一致；dogfood companion byte equality 会同步复制同一偏差。
- 测试缺口：initial/final unavailable tests 只断言 contract 名称出现一次、filtering fact 不存在和 retrieval text 重新派生，没有把完整 unavailable fact 与批准对象做相等断言，因此 302 tests PASS 无法证明该固定合同一致。
- 影响：Git path snapshot 失败时产出的 `finish-summary.json` 不符合本任务的批准 design 与 task-scoped Docs SSOT；后续 #98/#100 可能看到未被批准的固定检索文本。当前 scope 的设计、实现和测试不一致，Branch Review Gate 必须阻断。
- 修复要求：把 canonical constant 改为批准版完整对象，同步 dogfood companion，并为 initial diff、initial untracked、final/recovery 三类失败路径增加完整 fact 相等断言；完成独立 Phase 2 check、追加 commit 和新的 closure round。

## 观察项

- `phase2-check.json` 记录 HEAD `53f265f`，其 `dirty_paths` 覆盖后续 fix commit 的 37 个 non-metadata paths；这符合 workflow 的 post-commit audit 语义。除本报告发现的批准合同漂移外，302 canonical、36 preset、79 PublishBoundary + FinishSummary、31 + 1 optional skip、compile、Bash、260 JSON、planning/boundary/drift/equality/sidecar/diff 证据完整。
- 两个 work commits 均为中文 issue-bearing Conventional Commit，body 包含背景、变更、边界、验证和 `Refs #97`；未使用 close keyword。
- `git ls-files '.trellis/workspace/**'` 为空，`origin/main...HEAD` 保留三个预期 `D`；ignore 与 `session_auto_commit: false` 已物化。
- issue ledger 仅将 #97 放入 close scope；#53/#96/#100 为 related，#98/#99 为 follow-up；`pr-body.md` 的 `Closes #97` 与 ledger 一致。
- current branch 尚未 push，真实 current-ref remote marketplace verification 仍为 pending；这是 `gh pr create` 前的 fail-closed publish gate，不由本地/public-main sampling 替代。默认 pinned `v0.6.5-guru.3` 当前远端不存在，且在本任务基线已如此；PR body 已明确本任务不创建 tag，正式 publish 必须使用已 push current-ref，此项不降级为当前 #97 finding。

## 后续候选

- #98、#99、#100 保持 live #97 已定义的非目标，不并入本轮修复。
- 未发现需要新增 issue 的独立范围；本报告 P2 属于 #97 当前 close scope，必须在同一分支闭环。

## Docs SSOT 判断

- 结论：`FAIL`。
- Durable requirements、workflow/spec/README 的流程主线已收敛，round 1 的旧 `add_session.py` 流程文档 finding 已修复。
- 但重新批准的 task `design.md` 是当前实现的精确输入合同，canonical recorder 与其 fixed unavailable fact 不一致，且测试未锁定该对象；这属于 current-scope Docs SSOT inconsistency，不能记录为 observation。

## 部署与安全判断

- 完整 diff 未修改 GitHub Actions/CI/CD、Dockerfile/Compose、Kubernetes/Kustomize、Helm、数据库 migration/seed/backfill 或 Makefile，也未新增 API、服务、worker、定时任务、队列、数据库结构或业务运行时部署入口。
- 变更影响 Guru Team workflow/preset 安装、SessionStart 上下文和 finish/publish metadata 控制面；真实 remote verifier 继续在 publish 前 fail closed。
- 未发现新增 token、secret、private key、签名 URL、`.env`、数据库 URL或客户数据。workspace journal 内容没有迁移到新 artifact；本报告不复述已删除 journal 内容。
- 当前 P2 只要求修正 fixed fact 与测试，不需要业务部署资产、配置迁移或 release tag。

## 独立验证

- `gh issue view 97 --repo castbox/guru-trellis --json ...`：live issue OPEN，0/1/>1 recovery、snapshot failure、workspace non-read 与验收合同已复读。
- 官方 `custom-workflow.md`：确认 workflow 行为由 Markdown runtime contract 定义，不 fork upstream。
- 官方 `custom-spec-template-marketplace.md`：确认 marketplace spec 不承载 active task/runtime 私有状态。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：302 tests PASS。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：36 tests PASS。
- 完整 Codex/Cursor hook audit：两个入口均无 workspace `open` / `os.listdir` / `os.scandir` event，无 `Journal:` 输出。
- canonical/dogfood workflow、companion、schema、shared start、Codex hook、Cursor hook：byte-equal。
- `git diff --check origin/main...HEAD`：PASS；recursive `.new/.bak` 扫描为空。
- workspace tracking audit：Git index 为空，base-to-HEAD 保留三个删除记录。
- source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis`：仍为 `ff8c03a` 且 clean。

## 结论

Round 2 closure：`FAIL`，`findings_count=1`。Round 1 finding 1、2、4、5 与 Phase 2 新增两个 P3 已闭环；finding 3 因 fixed unavailable fact 与批准 `design.md` 不一致而未闭环。当前 HEAD 不得进入 `最终放行审查代理`、Branch Review Gate PASS 或 `trellis-finish-work`。修复并重新完成 Phase 2/commit 后，必须由后续 `问题闭环审查代理` 显式关闭本轮 finding；本代理不得转任 final reviewer。
