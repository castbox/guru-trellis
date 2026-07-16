# #111 `guru-discover-change-context` 实现交接

## 1. 当前状态

- 实现代理：`/root/issue111_scope_impl`。
- 状态：`Implementation Complete`，等待新的独立 `trellis-check` 执行 Phase 2
  语义复核。
- Docs SSOT strategy：`ssot_first`。
- 当前范围权威：live issue #111 的 2026-07-16“场景范围控制”。
- 当前 HEAD：`94d6126d75d7419e79a142f45d92b07dc8922241`；base：
  `origin/main@3395fad2a4049a33c4c679cd05452cfa45a85b92`。
- 未 commit、未 push、未创建 PR、未写 Phase 2 / Branch Review recorder，也未修改
  `agent-assignment.json`、`review.md`、`reviews/**` 或 `review-gate.json`。

本文只交接实现与验证事实，不声明 Phase 2、Branch Review 或发布门禁通过。

## 2. Scope 收敛

本轮对 `origin/main...HEAD` 与 working tree 中的 change-context 资产做了完整减法，
不是继续修补旧加固模型。

已删除：

- duplicate candidate 的 post-review GitHub 二次读取，以及 cross-repo、closed-after-review、
  unreadable 和伪造类矩阵；
- refresh 的 prior snapshot / receipt CLI、外部 ancestry 证明与写后外部证据重读；
- 整份 payload 的 machine-path / signed-query 扫描；
- archive symlink/unreadable-subtree walker、query symlink walk；
- recorder target 的 symlink/FIFO/special-file 矩阵与 post-write mutation hook；
- 对应 schema、interface、runtime、tests、throwaway 和 durable docs 承诺。

保留的普通 correctness/reproducibility 合同：

- workflow/standalone fresh-base parity 与 stale-before-semantic-read；
- current-state-before-history 固定顺序；
- 一次 open duplicate search 返回字段的 repo/number/identity/URL/open/update-time 投影重算
  与 `facts_sha256`，不执行第二次 search/re-read；
- query/manifest/preview/snapshot digest、score v1、固定 sort/limit/projection；
- 普通 non-file/read/JSON/index-shape invalid isolation 与 lexical path boundary；
- zero candidate、AI 1-3 candidate selection、source-specific deep read 与 mem insufficiency gate；
- `typed_exit=blocked` 当且仅当 AI Review Gate blocked；
- 当前 stale codes、superseded query/snapshot digests、reason、detection time 驱动的
  `refresh_base` 整步 re-entry；
- task-local same-snapshot persistence、单次 exact-byte readback 与 Git trackability；
- no-workspace/no-runtime/no-repo-cache/no-shared-write。

## 3. 实现与分发

- Canonical runtime：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Canonical package：
  `trellis/skills/guru-team/packages/guru-discover-change-context/**`，包含 semantic
  `SKILL.md`、interface 1.2、`guru-context-discovery-1.0` schema、contract、
  dispatcher wrappers、example 与 package tests。
- Runtime commands：
  `preview-change-context-history`、`record-context-discovery`、
  `check-context-discovery`。
- Stable exits：
  `context_ready -> guru-clarify-requirements`、
  `refresh_base -> guru-sync-base`、`blocked -> change-context-blocked`。
- Extension version：`0.6.5-guru.11`。
- Canonical preset apply 已同步 `.trellis/guru-team/**`、shared、Codex、Cursor、Claude
  package copies；installed manifest 为 `status=ok`、3 个 active skills、9 个 exit
  markers、128 个 managed files、0 conflict、0 sidecar。
- Transitional legacy overlay 与 43 条 frozen ownership baseline 未修改。

## 4. Docs SSOT Reconciliation

本轮先更新 durable docs，再以同一合同复核 package/schema/runtime/tests：

- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `docs/requirements/README.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/docs/public-docs.md`

上述 durable sources 已删除旧 ancestor/receipt、二次 candidate live read、跨字段扫描、
archive special-input 与 recorder special-target 合同，并统一到第 2 节的正常调查路径。
Task 中旧 review/finding 只属于历史记录，不再作为当前 acceptance 或实现依据。

## 5. 验证证据

- Targeted：
  `python3 -m unittest trellis.skills.guru-team.packages.guru-discover-change-context.tests.test_contract trellis.workflows.guru-team.scripts.python.test_guru_team_trellis.ChangeContextDiscoveryTests`
  -> `Ran 29 tests ... OK`。
- Full suite：
  `python3 -m unittest ...test_contract.py ...test_skill_packages.py ...test_guru_team_trellis.py ...test_apply_guru_team_trellis_preset.py ...test_upstream_ownership.py`
  -> `Ran 589 tests in 176.285s ... OK`。
- `python3 -m py_compile` 覆盖 runtime、preset installer、ownership validator -> passed。
- `bash -n` 覆盖三个 discovery wrappers、preset apply、throwaway script -> passed。
- `apply.sh --repo . --all-platforms`：首轮按 managed upgrade 生成 26 个已知
  `.bak`；逐项确认目标等于 canonical bytes 后清理；第二轮 `status=ok`、
  source/installed package 均 passed、sidecar_count=0。
- `check-upstream-ownership.sh` -> 43 active、0 removed、13 managed claims；
  `check-dogfood-overlay-drift.sh` -> canonical/dogfood match。
- Workspace boundary、planning approval、task validate、`git diff --check`、scope
  regression audit、zero `.new/.bak` -> passed。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh` -> `exit=0`；
  覆盖 clean init、workflow preview/switch、local preset install、direct discovery、
  record/check、`trellis update`、preset reapply、ownership 与 zero sidecar。

Throwaway 限制：远端不存在
`feat/111-guru-discover-change-context`，且当前阶段禁止 push，因此未验证“从当前分支
exact GitHub ref 安装 marketplace workflow”。公共 `#main` marketplace 只作为脚本明确
标记的 public sample；本地 canonical preset/package/runtime 使用当前 worktree bytes。
后续分支 push 后必须由 publish/remote verifier 使用 exact ref 补齐，不得把本轮 public
sample 记为 current-branch marketplace pass。

## 6. Task-History-Only 内容

以下内容只保留在 task 目录：

- #111 intake、规划确认、scope change、agent assignment 与历史 review 轮次；
- 旧加固 findings 及其撤销原因；
- 本机 throwaway 临时仓库、模拟 issue/PR、临时 SHA 与运行时间；
- 本交接中的一次性测试计数和未推送分支限制。

当前 durable docs、package、schema、runtime、tests 与 throwaway 已使用同一 scope。
下一位 Phase 2 checker 必须先绑定 live #111 的场景范围；被明确排除的场景不得升级为
finding 或重新派发实现。
