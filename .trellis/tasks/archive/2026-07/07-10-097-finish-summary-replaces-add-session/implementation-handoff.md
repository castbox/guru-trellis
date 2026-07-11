# Issue #97 Branch Review round 1 闭环与 round 2 P2 修复实现交接

## 完成状态

- 状态：`round2_fix_complete_pending_fresh_phase2_check`。
- 本轮已修复 `round-001-replacement-finding.md` 的 5 个 current-scope finding。
- 已修复 `round-002-closure.md` 的唯一 P2：snapshot-unavailable 固定事实与批准设计不一致。
- 未修改已批准的 `prd.md`、`design.md`、`implement.md` 或 `planning-approval.json`。
- 未写入 `phase2-check.json`、`agent-assignment.json`、`review.md`、`reviews/*.md`、`review-gate.json`。
- 未 stage、commit、push、创建 PR、关闭 issue 或调用 finish-work。
- source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 保持干净；所有写入都位于 task worktree。

## Branch Review round 2 P2 修复

- canonical `FINISH_SUMMARY_PATH_SNAPSHOT_UNAVAILABLE_CONTRACT` 已与批准版 `design.md` 4.4 完整一致：

```json
{
  "contract": "finish-summary git path snapshot unavailable",
  "before": "Git 变更路径快照未成功完成。",
  "after": "完成摘要已使用空路径集合，未写入未验证路径。",
  "source_artifact": ""
}
```

- 初始 `git diff` 失败、初始 `git ls-files --others` 失败、final/recovery `git diff` 失败均直接驱动真实 snapshot 分支，不再只 mock 已完成的 snapshot tuple。
- 三类 failure 共用对象级断言：完整 unavailable fact 与批准对象相等且恰好一次，两个 path 数组同时为空，protected-filtering fact 不存在，`retrieval_text` 从最终 index 重派生。
- 三类 failure 均验证 partial stdout path、受保护 path basename、stderr 与 secret ref 不进入最终 summary；注入 workspace path 后，`git.changed_paths` 与 `index.search_terms.paths` 两个 validator 继续 fail closed。
- 已通过 all-platform preset apply 同步 dogfood companion。生成 backup 的 SHA 与 apply 前 Git blob 一致，内容差异仅为上述两行 fixed fact；backup 已清理，extension 安装运行态字段未纳入本 finding diff。

## Round 2 修复验证

- canonical companion full suite：`302 tests` PASS。
- preset installer full suite：`36 tests` PASS。
- `FinishSummaryContractTests`：`31 tests` PASS，包含三类 snapshot failure 的完整对象、空 paths、无泄露、重派生与 fail-closed 断言。
- Python compile：canonical/dogfood companion、canonical tests、preset installer/tests PASS。
- all-platform preset apply：PASS；dogfood companion 与 canonical byte-equal。
- `check-dogfood-overlay-drift.sh`：PASS。
- recursive `.new` / `.bak` sidecar scan：空。
- 旧 snapshot-unavailable 文案定向扫描：canonical/dogfood companion 中无命中。
- task validation、planning approval、workspace boundary、source checkout clean、`git diff --check`：PASS。
- 未执行独立 Phase 2 check；必须由新的阶段二检查代理重跑并重写 `phase2-check.json` 后，才能追加 work commit 和进入下一 closure round。

## Docs SSOT 执行

- plan strategy：`ssot_first`。
- durable docs 输入：官方 Trellis custom workflow/spec marketplace 文档、canonical Guru Team workflow、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、README 与 `docs/requirements/**`。
- confirmed task delta 输入：重新批准的 `prd.md`、`design.md`、`implement.md`，以及 `research/current-finish-publish-contract.md` 中的 5 个 Branch Review finding。
- durable docs 同步结果：已把 no-workspace context、immutable readiness、Git path snapshot failure、0/1/>1 recovery、throwaway sidecar cleanup 写回 canonical workflow、spec、README、requirements 与 overlays。
- task delta 合并：5 个 finding 的长期合同已全部合并到 durable docs；task artifacts 不作为长期 SSOT。
- task-history-only：round 1 finding 证据、旧 planning blocker、sub-agent replacement/liveness、post-planning approval 过程和本实现交接只保留在 task archive。
- 无更新理由：不适用；本轮长期 workflow/publish/context/test 合同发生变化，durable docs 已实际更新。
- 后续限制：#98 搜索命令、#100 backfill CLI、#99 developer identity 不属于 #97；真实 remote marketplace verifier、finish/publish 副作用留给通过 fresh Phase 2 check 和 Branch Review Gate 后的 finish-work。

## 实现结果

### 1. No-workspace startup/context

- shared `trellis-start` 固定运行 phase、packages、`task.py current --source` 与 Git facts，不再运行 bare `get_context.py`。
- canonical Codex/Cursor SessionStart overlays 删除 `get_active_journal_file`、`count_lines` 的 import/fallback/call 和 `Journal:` 输出。
- fresh preset install sentinel 测试在 `.trellis/workspace/**` 放置带秘密 basename/content 的 journal，并对 `Path.read_text` / `Path.iterdir` 加 access guard；hook 构建上下文时不得读取或枚举 workspace，输出不得包含 path、basename、content 或 line count。
- 独立 Phase 2 check 又把 shared start sentinel 纳入真实 throwaway：Python audit hook 阻断 `open` / `os.listdir` / `os.scandir` workspace 访问，实际执行 phase、packages、current-task 三条 Python context 命令并检查输出不含 sentinel/journal/line count。
- 未修改 upstream `.trellis/scripts/common/session_context.py`、全局 npm 或 `node_modules`。

### 2. Immutable PR recovery inputs

- `finish-work` 在 archive 前从 task-local `pr-body.md` 构建 `pr-readiness.json.publish_inputs`，固定 repo、base/head branch、reviewed HEAD SHA、exact title、body source/SHA-256、draft、reviewed source 和 canonical snapshot SHA-256。
- readiness/body 随 archive metadata commit 在首次 PR create 前提交；formal publish 只接受 task-local readiness snapshot。
- publish/recovery 在 PR query/create 前验证 artifact/body dirty/staged、当前 HEAD Git blob、readiness 单次提交历史、snapshot/body digest、review gate HEAD/ancestor、repo/base/head identity 与 current/remote HEAD。
- recovery command 只携带 archived readiness artifact 与 task/repo/remote locator，不携带 title/body/draft/base/validation override。
- mutation tests 覆盖 body、title、draft、repo、base、head、reviewed HEAD、reviewed source、snapshot digest 和 committed readiness rewrite；全部在 PR resolution 前 fail closed。

### 3. Git path snapshot failure

- `finish_summary_git_path_snapshot()` 统一返回 safe paths、filtered flag 与 unavailable flag。
- initial diff、initial `ls-files --others`、final/recovery diff 任一失败时返回 `([], false, true)`，不保留 partial path，也不传播 stderr/ref。
- initial/final recorder 同时清空 `git.changed_paths` 与 `index.search_terms.paths`，移除 protected-filtering fact，只追加一次固定 `finish-summary git path snapshot unavailable` fact，并重新派生 `retrieval_text`。
- schema/path validator 未放宽，所有 path surface 继续拒绝 workspace/runtime/absolute/parent/backslash/CRLF 路径。

### 4. Durable full-flow document

- `docs/requirements/guru-team-trellis-flow.md` 已修订分层职责、全链路总图、finish 图、dry-run、PR readiness、Artifact 责任图与讲解主线。
- 新主线为 AI index -> initial summary -> immutable readiness -> metadata commit -> marketplace verifier -> open PR 0/1/>1 -> PR URL/ref/safe-path metadata tail。
- Guru Team 的旧 archive+journal/add_session finish 描述已移除；官方 Trellis 自身仍保留 workspace journal 扩展能力的背景说明。

### 5. Throwaway sidecar gate

- `verify-throwaway-install.sh` 校验预期 workflow preview `.new` 后立即删除并确认不存在。
- verifier 随后执行 workflow switch、`trellis update --force`、workflow reapply、preset reapply，并在成功退出前递归扫描 `.new/.bak`；任何残留 sidecar 都会输出路径并失败。
- 独立 Phase 2 check 发现官方 update 会把 active workflow 恢复成 upstream 默认值；本轮补充 update 后的 marketplace workflow reapply，并让 preset 单元测试校验 preview cleanup -> initial switch -> update -> workflow reapply -> preset reapply -> final scan 的固定顺序。

## 主要改动文件

- Canonical code/tests：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、`test_guru_team_trellis.py`。
- Canonical overlays/tests：`trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`、Codex/Cursor SessionStart、continue overlays、preset tests。
- Installer verifier：`trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`。
- Durable SSOT：canonical/dogfood workflow、workflow/preset specs、root/workflow README、`requirement-main.md`、`guru-team-trellis-flow.md`。
- Dogfood copies：`.trellis/guru-team/scripts/python/guru_team_trellis.py`、`.agents/skills/trellis-start`、Codex/Cursor hooks、continue entries。

## 已运行验证

- planning approval validator：PASS，approved HEAD `53f265f3949ca8374c7b534da309a4c924325450`。
- workspace boundary：PASS；source checkout 无状态变化。
- canonical companion suite：`302 tests` PASS。
- preset installer suite：`36 tests` PASS。
- `PublishBoundaryTest`：immutable readiness 与 recovery 定向 suite PASS。
- `FinishSummaryContractTests`：path failure 与固定 fact 定向 suite PASS。
- Python compile：canonical/installed companion、preset installer 与两组 tests PASS。
- Bash syntax：`verify-throwaway-install.sh` PASS。
- `apply.sh --repo . --all-platforms --json`：PASS；预期 managed `.bak` 已核对并删除。
- `check-dogfood-overlay-drift.sh`：PASS。
- byte equality：canonical/dogfood workflow、companion、shared start、Codex hook、Cursor hook PASS。
- recursive `.new/.bak` scan：空。
- `git diff --check`：PASS。

## 独立 Phase 2 check 修复

- 检查中真实运行 throwaway 后发现：`trellis update --force` 会把 active workflow 恢复为 upstream 默认 workflow，原 verifier 随后只 reapply preset，最终 workflow 断言失败且无法到达 sidecar gate。
- 已把 verifier 顺序修为 preview cleanup -> initial workflow switch -> update -> workflow reapply -> preset reapply -> final assertions/sidecar scan；preset test 固定验证两次 workflow switch 的顺序。
- public-main sampling throwaway 已完整通过；fresh repo 中的 shared start sentinel 由 Python audit hook 阻断 workspace `open` / `os.listdir` / `os.scandir`，实际 phase/packages/current-task 命令未触发专用退出码，且输出未披露 sentinel、journal 或 line count。
- 完整回归在先执行 `py_compile` 后发现 public-surface 测试会把 ignored `__pycache__/*.pyc` 当 UTF-8 文档读取；测试现明确排除 Python bytecode/cache，保证 compile 后重复运行 canonical suite 仍稳定。
- 默认 pinned `v0.6.5-guru.3` 因 release tag 尚未发布而在 marketplace init 阶段失败；本任务规划明确不创建 tag，current-ref remote verifier 必须在分支 push 后由正式 publish gate 执行，因此该项保留为发布前门禁，不视为本地 current-scope 实现通过证据。

## 剩余风险与未执行项

- 本实现代理未执行完整独立 Phase 2 check，也未运行真实 remote throwaway marketplace verification；后者要求 branch push 后由正式 verifier 执行。
- 本实现代理未运行真实 finish/archive/metadata commit/push/PR create/recovery；相关副作用只允许 finish-work 在 gate 通过后执行。
- readiness 的 exact Git blob/history 校验已由真实临时 Git repo mutation tests 覆盖，但仍需 Phase 2 check 复核跨层调用顺序与所有旧 tests 的最新结果。
- 旧 `phase2-check.json` 早于 round 1 findings，不得复用。

## Phase 2 check 重点

1. 复核 formal finish 是否在 archive metadata commit 前生成 readiness，并确保首次 create 前 artifact/body 已提交且 recovery command 只引用 archived readiness。
2. 复核 mutation、dirty/staged、Git blob/history、gate ancestor、repo/base/head/current/remote 检查都发生在 PR query/create 前。
3. 复核 initial diff、initial untracked、final/recovery diff failure 都得到相同空 paths/unavailable fact/retrieval 行为，且无 stderr/ref/partial path 泄露。
4. 以 fresh install sentinel 复核 shared/Codex/Cursor context 不打开、不枚举、不输出 workspace journal/path/basename/content/line count。
5. 复核完整流程 durable doc 与代码/测试一致，并确认所有 canonical/dogfood copies byte-equal、`.new/.bak` 为空。
6. 运行完整 canonical/preset/compile/shell/JSON/task/planning/boundary/drift/equality/diff 与可行的 throwaway/update/reapply smoke，生成新的 Phase 2 结论。

# Formal finish 路径身份回归修复交接

## 真实故障与副作用边界

- `trellis-finish-work` dry-run 已通过；formal finish 在 archive 后构建 initial `finish-summary.json` 时失败：`index.search_terms.paths[53] duplicates index.search_terms.paths[17] after normalization.`
- 碰撞输入为 `.trellis/guru-team/extension.json` 与 `trellis/guru-team-extension.json`。两者是不同、合法且都必须保留的 Git 路径；失败前的 `git.changed_paths` 已按精确字符串排序去重。
- 本轮开始时主会话已确认失败没有生成 `finish-summary.json`、新 commit、push、远端 branch 或 PR，并已把 task 恢复到 active / `in_progress`。本实现代理未运行 finish-work、Phase 2 recorder、Branch Review Gate recorder、commit、push、归档或 PR 操作。

## 根因与修复

- 根因为通用 `finish_summary_string_array_errors()` 把面向自然语言/搜索 token 的去空白、去标点归一化重复检查无差别应用到 `index.search_terms.paths`。上述两个路径归一化后相同，导致合法 path identity 被错误折叠。
- canonical validator 新增精确字符串 duplicate 检查，并让所有 path-bearing arrays 使用该身份合同：`index.search_terms.paths`、`index.affected_surfaces[].paths`、`backfill.source_artifacts`；`git.changed_paths` 保持既有 `sorted(set(paths))` 与 sorted/unique validator。
- `affected_surfaces` 和 `contract_changes` 的对象级 fingerprint 只归一化语义文本；`paths` 与 `source_artifact` 在复合对象中保持精确值，避免路径数组修复后又被外层对象 fingerprint 误判。
- 非路径语义/搜索字符串继续执行 normalized duplicate 检查；clean relative path、protected prefix、绝对/parent/backslash/CRLF 拒绝规则未放宽。
- 回归覆盖 initial summary build 和 final validator 同时精确保留两条真实碰撞路径、affected surface 外层 fingerprint、exact duplicate 拒绝、generator exact dedup、backfill source artifacts，以及 changed behavior / phrases normalized duplicate 继续拒绝。

## Docs SSOT 对账

- Docs SSOT strategy 延续已批准的 `ssot_first`；本次根因属于 finish-summary 数据合同歧义，不是 task-local 临时例外。
- `trellis/workflows/guru-team/schemas/finish-summary.schema.json` 的 `uniqueItems` 本来就是精确 JSON 值身份，无需修改 schema。
- `.trellis/spec/workflow/data-contracts.md` 已补充 domain-specific duplicate identity：所有路径数组按精确字符串识别，Git path generator 精确排序去重，非路径语义/搜索字符串继续归一化去重。
- formal finish 的失败现场、task 恢复过程、本轮代理执行边界与验证数字只作为 task-history-only 证据保留在本交接；长期合同已合并到 durable spec、canonical companion 和测试。

## 本轮修改文件

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`（preset apply 同步的 dogfood installed companion）
- `.trellis/spec/workflow/data-contracts.md`
- 本 `implementation-handoff.md`（task metadata，不进入 work commit）

## 本轮验证

- `FinishSummaryContractTests`：`34 tests` PASS；`python3 -S` 为 `34 tests` PASS、`1` 个 optional `jsonschema` skip。
- canonical companion full suite：`305 tests` PASS。
- preset installer full suite：`36 tests` PASS。
- canonical/dogfood companion SHA-256 byte-equal；`check-dogfood-overlay-drift.sh` PASS；recursive `.new` / `.bak` scan 为空。
- Python compile、tracked Bash syntax、`251` 个 tracked JSON parse、task validation、planning approval、workspace boundary、`git diff --check` PASS。
- preset apply 生成的 managed backup 已与 apply 前 HEAD blob 做 SHA-256 等值核对后清理；apply 刷新的 extension provenance 已恢复，未纳入本轮 diff。

## 剩余门禁

- 这次代码修改发生在旧 Phase 2 与 Branch Review Gate 之后；旧 `phase2-check.json`、`review-gate.json` 不得作为新 HEAD 的放行证据。
- 主会话必须在提交前派发新的独立 Phase 2 check，并在 work commit 后重新完成 Branch Review Gate；通过后才能再次运行 formal finish。
- 默认 pinned `v0.6.5-guru.3` 尚未发布；current-ref remote marketplace verifier 仍留在正式 publish push 后执行。
