# #177 Implementation Plan

## 1. 执行约束

- 只在 `codex/177-content-identity-boundary` worktree 修改。
- 先修订本文件的测试矩阵，再修改测试实现；本文件是本迭代的测试计划 SSOT。
- canonical source 先改，dogfood/platform copies 由 preset installer 同步。
- 不创建 commit、push、PR、Issue mutation、Finalizer transaction 或 cleanup；执行这些副作用前另行取得独立确认。

## 2. 实现步骤

- [x] I1. 在 shared runtime 实现 `guru-reviewed-content-1.0` path classifier、tree/worktree overlay 和 canonical identity。
- [x] I2. 将 Phase 2 private checkpoint 升级为 current-only schema 4.0，使用 `reviewed_content_sha256` 与 `phase2_capture_commit`。
- [x] I3. 升级 Phase 2/Task Commit public schema，以 `phase2_commit_anchor` 承接当前 Git anchor；metadata-only descendant 使用当前 HEAD 作为 commit parent，同时重验内容 identity。
- [x] I4. 将 Branch Review private gate 升级为 current-only schema 3.0，使用 `review_commit`，删除 metadata-descendant allowlist 与旧 gate 分支。
- [x] I5. 升级 Branch Review/Publication/Finalizer public schema，以 `branch_review_commit` 承接当前 Git anchor，并让所有 freshness owner 使用统一 identity。
- [x] I6. 增加 scope-only Ledger 2.0 schema、生成器、current-only loader 与 publish validator。
- [x] I7. 移除 Finalizer 向 Ledger 注入 marketplace pending/passed evidence 的 active 路径，改为独立 artifact binding。
- [x] I8. 删除受影响 Skill/workflow/preset/overlay/script/schema/example/eval/test/docs 中的旧 reader、projection、re-entry、allowlist、alias、fixture 和 compatibility 文案，更新 current-only package contract 与 breaking schema ids。
- [x] I9. 运行 preset installer 同步 dogfood/platform copies，处理 `.new`、`.bak`，验证 overlay drift。
- [x] I10. 执行完整测试矩阵并修复 current-scope finding。
- [x] I11. 修复 Branch Review `BR-177-F001`：删除 `task-start-context.json` 兼容 resolver、配置/schema/Skill/文档与专用测试，当前 identity 只由 `task.json`、runtime mapping 和 live Git worktree facts 建立。
- [x] I12. 修复 `BR-177-F002` / `BR-177-F003`：删除 finish-summary backfill 与 frozen Stage 0 migration 的 wrapper、dispatch、manifest、schema、example/eval、测试及文档，不保留替代入口。
- [x] I13. 修复 `BR-177-F004`：删除 43-path ownership tombstone 与 payload migration executor/inventory/fixture/test/docs，preset 只验证和安装 current Guru-owned claims/assets；非 current manifest/input 统一 fail closed。
- [x] I14. 收敛 canonical manifest、workflow/spec/README、throwaway verifier，并通过 preset installer 重新同步 dogfood 与全平台副本，处理全部 `.new` / `.bak`。
- [x] I15. 对 finding-fix 后的完整 dirty reviewed content 重新执行 Phase 2，并记录 current-only `guru-phase2-check-4.0` private checkpoint。
- [x] I16. 修复 `BR-177-F005`，并让 `check-review-gate` owner checker 接受内容等价
  descendant、拒绝 reviewed-content descendant。该轮未完整覆盖 Branch Review public
  wrapper；提交 `8473503` 后的独立 closure 证明 `BR-177-F006` 仍开放。
- [x] I17. 修复 `BR-177-F006` / `BR-177-F007`：完整 public wrapper 对 metadata-only
  descendant 返回 `passed`、对 reviewed-content descendant 返回 `blocked`；删除
  `task_local_pr_readiness_path`、`build_pr_readiness_snapshot`、
  `read_pr_readiness_publish_inputs`、仅供这些 helper 使用的常量，以及专用测试和 mock。
  canonical 修改后通过 preset installer 同步 dogfood/platform copies，并重新执行完整
  current-only Phase 2。
- [ ] I18. Phase 2 通过后另行确认新的 finding-fix commit；提交完成后再由原 finding
  owner 完成 F006/F007 transient closure，并由 distinct reviewer 完成 fresh-final Branch
  Review。

## 3. 测试计划

### T1. Identity 单元测试

- 相同 reviewed content：dirty candidate、提交状态、task metadata commit 后 identity 相同。
- included file 的内容、mode、rename、delete、untracked add 改变 identity。
- `.trellis/tasks/**`、`.trellis/workspace/**`、`.trellis/.runtime/**` 与 OS noise 不改变 identity。
- `.trellis/workflow.md`、`.trellis/spec/**`、canonical Skill/preset/script/schema 改变 identity。
- symlink 与 clean gitlink identity 稳定；dirty/unavailable gitlink fail closed。

### T2. Phase 2 与 Task Commit

- metadata-only HEAD/status 变化后 Phase 2 checker pass。
- reviewed-content HEAD/status 变化后 Phase 2 checker stale。
- Task Commit 在 metadata descendant 后以 current HEAD 为 parent。
- Task Commit 在内容 identity drift 后 blocked。

### T3. Branch Review

- schema 3.0 gate 记录 digest；metadata commit 与 dirty task metadata 保持 pass。
- 非 task 内容 commit、dirty content、mode/path 变化触发 stale。
- finding ancestry 继续使用 commit anchor。
- `check-review-gate` 对 content-equivalent descendant 保持 pass，对
  reviewed-content descendant 保持 stale；初始 recorder/public invocation 仍要求
  `branch_review_commit == current HEAD`。
- 完整 Branch Review public wrapper 对 metadata-only descendant 序列化 `passed` DTO，
  对 reviewed-content descendant 序列化 `blocked` DTO；不得仅以 owner checker 直测
  代替 wrapper 回归。
- Branch Review `passed` public wrapper 在 output schema 通过后删除自己的 checkpoint，
  随后的 Publication entry 不依赖该文件。

### T4. Ledger 与 Verification

- 新 task 只生成 Ledger 2.0 固定字段。
- Ledger schema 拒绝 `acceptance_evidence`、`verification`、proposal digest、comment checksum、rules 和未知字段。
- loader 只接受 Ledger 2.0，不存在旧 Ledger projection、migration 或专用 re-entry。
- Marketplace required/not-required 流程均不修改 Ledger bytes；verification artifact 单独校验。

### T5. Finish Family Integration

- Branch pass -> wrapper 删除 Branch Review checkpoint -> Publication ready ->
  Finalizer preflight 在 metadata tail 后保持 fresh。
- Finalizer 初次 preflight 使用 Publication DTO，re-entry/recovery 使用 immutable
  existing plan；两条路径都不读取 Branch Review checkpoint，无 DTO 且无 plan 时
  fail closed。
- current runtime 不保留 task-local PR-readiness snapshot/recovery helper、其 publish-input
  常量、专用测试或 mock；Finalizer 只使用 Publication DTO 或 immutable plan。
- reviewed-content drift 返回 task-work/stale route。
- marketplace verification、closeout plan、archive projection 不依赖 Ledger evidence augmentation。
- #180 的 transaction compression 不被提前实现。

### T6. 分发、安装与升级

- canonical package contract tests。
- source 与 installed Skill package closure。
- preset Python tests、shell syntax、Python compile。
- `apply.sh --repo .` 后 dogfood overlay drift 为零。
- clean throwaway workflow/preset install。
- existing-project workflow preview/switch、preset update/reapply、`.new/.bak` 行为。
- Codex、Claude、Cursor 平台入口和 shared Skill bytes 一致。
- 受影响 active contracts 只包含 current schema/id/field，不存在旧 reader、projection、re-entry、allowlist、alias、fixture、eval 或专用测试。

### T7. Breaking current-contract-only 回归

- current runtime、Skill package、extension manifest、preset ownership 与安装副本中不存在 `task-start-context` reader/schema/config、finish-summary backfill、Stage 0 migration manifest/schema 或 ownership tombstone migration。
- current canonical/dogfood runtime 与测试中不存在
  `task_local_pr_readiness_path`、`build_pr_readiness_snapshot`、
  `read_pr_readiness_publish_inputs`、`PR_READINESS_PUBLISH_INPUT_KEYS` 或
  `PR_READINESS_CLOSEOUT_INPUT_KEYS`。
- current loaders 只接受当前 schema/manifest；其它 shape 通过通用 current-contract 校验 fail closed，不增加版本识别、迁移分支或版本专用 fixture/test。
- ownership validator 只证明 current Guru-owned claims、三处 additive finish entry、managed asset/package closure 与 source/installed 一致，不保留历史 path/payload 数量、digest 或迁移状态。
- throwaway fresh install 与 update/reapply 从当前资产开始，验证不安装、不发布、不调用已删除入口，最终递归零 `.new` / `.bak`。

## 4. 验证命令

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/skills/guru-team/packages/guru-check-task/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-create-task-workspace/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-review-branch/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-review-task-publication/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/tests/test_finish_family_integration.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-05-177-content-identity-boundary
git diff --check
```

集成与 throwaway 验证串行执行。任何因网络、CLI 或外部 marketplace 状态无法执行的命令单独记录为未验证，不折算为通过。

## 5. 实现与验证结果

### 5.1 当前实现

- `guru-reviewed-content-1.0` 由 shared runtime 单点实现，完整 tree 与 worktree overlay 使用同一 canonical identity。
- Phase 2、Task Commit、Branch Review、Publication、Finalizer 已切换到 breaking current-only schema 与新的 commit anchor 字段。
- `issue-scope-ledger.json` 只保留 Ledger 2.0 scope 字段；marketplace verification 使用独立 artifact，不再写 Ledger。
- 受影响 active package 不再包含旧 reader、旧 schema projection、版本兼容 re-entry、metadata allowlist、alias、legacy fixture/eval 或专用兼容测试。
- canonical source 已同步到 `.trellis/guru-team/**`、`.agents/skills/**`、`.codex/skills/**`、`.claude/skills/**`、`.cursor/skills/**` 与三处 finish overlay。

### 5.2 已通过证据

- shared runtime 全量：382/382 passed；完整 13 个 Skill package 合同：130/130 passed；六个直接相关 Skill 合同：61/61 passed；Finish-family source 与 installed 各 11/11 passed；preset Python tests：45/45 passed。runtime 数量较上一轮减少 1 项，来源是按 F007 删除的 obsolete PR-readiness helper 专用测试。
- source/installed package closure 均通过：13 active Skills、51 exits、28 workflow targets；installed manifest 管理 2612 个文件，removal/conflict/sidecar 均为 0。
- ownership current-only schema 3.0 通过：11 条 anchored Guru-owned rules、9 个 managed claims、3 个 additive overlays、53 个 current managed assets；dogfood overlay drift 为零。
- current-only 扫描未发现 `task-start-context` reader/config/schema、finish-summary backfill、Stage 0 migration manifest/schema、ownership tombstone/payload migration、旧 Phase 2/Branch Review 字段或 schema、Ledger 1.0、`trellis_cli_compatibility`、已删除 wrapper/脚本入口。所有删除路径均不存在。
- canonical workflow、runtime、finish-summary schema 与 dogfood copy byte-identical；13 个 canonical package 与 installed/shared/Codex/Claude/Cursor 副本由 installed closure 验证为一致。
- preset `apply.sh --repo . --all-platforms` 最终全量 unchanged；此前两份 sidecar 继续保留在仓库外恢复目录 `issue177-preset-sidecars-recovery.Mq9A40/` 且本轮未访问。本轮首次同步产生的一份新 `.bak` 已确认逐字节等于当前 Git 中同步前 dogfood runtime 后删除；复跑三平台 installer 后 removal/conflict/sidecar 均为 0，递归 `.new` / `.bak` 为零。
- clean throwaway 首次因当前 branch 未发布而正确 fail closed；设置 `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 后，public marketplace discovery + 当前本地 unpublished workflow sample 的 fresh install、existing-project preview/switch、官方 Trellis 0.6.5 `update --force`、workflow/preset reapply、两轮 installed wrapper/Finish-family/closeout/workspace 验证、无 developer identity 与 identity-preservation 两条路径、最终递归零 `.new`/`.bak` 均通过。
- shell `bash -n`、Python compile、changed/untracked JSON parse、task validate、`git diff --check` 均通过；用户 `.trellis/guru-team/config.yml` hash 保持 `647facdebec4c04c97a65c64a5e5cde37252f1a3db6c96eeb112c60576262988`。

### 5.3 Phase 2 finding 与修复

- `P1`：reviewed-content identity 原实现只校验 `git status` overlay 中出现的 gitlink。正常执行 `git submodule deinit` 后 status 为空，未初始化 gitlink 被错误接受且 identity 保持不变。修复后会校验最终 tree 中全部 gitlink worktree，未初始化或 dirty 均 fail closed；新增 included symlink、clean/advanced/dirty/uninitialized gitlink 直接测试。
- `P3`：preset README 曾同时声明 `install.managed_assets` 为 58 和 60。已改为由测试约束 README 声明必须等于 current manifest；后续删除兼容资产后，当前两者均为 53。
- `P3`：提交前按 live `quality-guidelines.md` 执行 Task Commit 审读时，发现 Branch Review 清单仍把 `guru-check-task` owner checkpoint 写成 schema 3.0。已修正为 current-only schema 4.0，并扩展自然语言版本残留检查。
- 三项 finding 修复后已重跑对应全量矩阵与直接依赖检查，当前无未关闭 P0-P3 finding。

### 5.4 尚未声称的外部证据

- 当前 branch 尚未 push，因此没有从 exact remote branch/ref 安装当前 marketplace workflow；throwaway 证据是 public marketplace discovery 加当前 worktree 的 local unpublished workflow sample，不替代 push 后远端门禁。
- extension manifest 仍以 Trellis CLI `0.6.5` 为 target/tested version；已验证该目标版本的 `trellis update --force` 与 reapply，不声称已验证 npm `0.6.12` 的跨版本 upgrade。

### 5.5 Branch Review finding-fix 状态

- 独立 Branch Review 对 `origin/main...b04a6b1` 返回 `implementation_required`，开放 `BR-177-F001` 至 `BR-177-F004` 四个 `P1 normal_required_behavior` finding。
- `BR-177-F001` 的 `task-start-context.json` reader/config/schema/Skill/docs/tests 已删除；当前 task identity 只来自 `task.json`、ignored runtime mapping、current checkout 和 live Git worktree facts。
- `BR-177-F002` / `BR-177-F003` 的 finish-summary backfill、Stage 0 frozen migration wrapper/dispatch/manifest/schema/example/eval/tests/docs 已删除，不存在替代入口；`finish-summary.schema.json` 只接受正常 current `guru-team.finish-work` generator。
- `BR-177-F004` 的 43-path tombstone、payload migration executor/inventory/fixtures/tests/docs 已删除；ownership schema 3.0 只描述和验证 current claims/assets。
- finding-fix 后的上一轮 Phase 2 semantic check 已通过：`guru-phase2-check-4.0` recorder/checker 绑定 `b04a6b191e1f1fd94d4001b363f356a456e8c3d4` 与当时 reviewed-content identity，public wrapper 返回唯一 `passed` DTO；该证据早于 F006/F007 修复，不能复用于本轮。
- finding closure 尚未完成。F005 已由原 finding owner 关闭；F006/F007 的实现、验证矩阵与 fresh current-only Phase 2 已完成，但仍须另行确认 finding-fix commit，再完成原 owner transient closure 与 distinct fresh-final Branch Review。

### 5.6 I16 提交后的独立 closure 结果

- `BR-177-F005` 已修复：Branch Review `passed` wrapper 删除 private checkpoint 后，
  Publication 只校验 `passed` DTO 的 `branch_review_commit` 与 live reviewed-content
  continuity；Finalizer 初次进入只消费 Publication DTO，re-entry/recovery 只消费
  immutable existing plan。两条路径均不读取 Branch Review private checkpoint；无 DTO
  且无 plan 时 fail closed。
- `BR-177-F006` 仍开放：`cmd_check_review_gate` 已显式使用
  `require_current_head=False`，但 `production_owner_result` 的 Branch Review public
  wrapper 路径再次调用 `review_branch_entry_precondition_errors` 时仍使用默认 `True`；
  metadata-only descendant 因此会被错误序列化为 `blocked`。现有回归只覆盖 checker，
  未覆盖完整 public wrapper。
- `BR-177-F007` 为新增 `P1 explicit_nonstandard_requirement` finding：canonical 与
  dogfood runtime 仍保留三个无 active caller 的旧 task-local PR-readiness
  snapshot/recovery helper，reader 还消费 Branch Review gate；这违反 breaking
  current-contract-only 与用户明确的“不保留向前兼容内容”要求。
- 本节此前记录的 I16 测试和 Phase 2 结果只证明 `8473503` 提交前的候选状态，不能作为
  F006/F007 修复后的 pass 证据。完成 I17 后必须重跑受影响矩阵、全量分发/安装门禁和
  fresh current-only Phase 2。

### 5.7 I17 修复与当前验证结果

- `BR-177-F006` 已在 canonical runtime 修复：`production_owner_result` 的完整 Branch
  Review public wrapper 以 `require_current_head=False` 重验 task commit 与
  reviewed-content continuity。回归测试通过真实 wrapper 证明 metadata-only descendant
  序列化 `passed` 最小 DTO 并消费 private gate；随后重建 gate 后，reviewed-content
  descendant 序列化 `blocked`。
- `BR-177-F007` 已按 breaking current-contract-only 删除
  `task_local_pr_readiness_path`、`build_pr_readiness_snapshot`、
  `read_pr_readiness_publish_inputs`、两个仅供这些 helper 使用的 publish-input 常量、
  readiness builder/reader 专用测试及两个 obsolete mock；canonical、dogfood、Skill、
  preset 与 Codex/Claude/Cursor 安装副本扫描均为零残留。
- current 验证通过：runtime 382/382、13 个 Skill package 合同 130/130、六个直接相关
  Skill 合同 61/61、Finish-family source/installed 各 11/11、preset 45/45、
  source/installed package closure、ownership schema 3.0、dogfood drift、Python/shell
  syntax、JSON parse、task JSONL validate、`git diff --check` 与配置 hash 保持。
- clean throwaway 首次因当前 branch 未发布而按设计 fail closed；启用明确的 local
  unpublished workflow sample 后，fresh install、Trellis 0.6.5 update、workflow/preset
  reapply、两轮 installed wrapper/Finish-family/closeout/workspace 与最终零 sidecar 均
  通过。exact remote branch marketplace install 仍未验证，不折算为通过。
- fresh current-only Phase 2 已在全部 F006/F007 修复与验证完成后执行，结果见 5.8；
  F006/F007 closure、finding-fix commit 与 fresh-final Branch Review 仍未完成。

### 5.8 Fresh current-only Phase 2

- AI semantic round 重新读取 live Issue #177 及 breaking current-contract-only comment、
  #174/#180 状态、scope-only Ledger、三份 planning、完整 `origin/main...HEAD`、当前
  staged/unstaged/untracked 与 durable Docs SSOT；#180 明确保持 `out_of_scope`。
- candidate hygiene 覆盖 1009 个 committed candidate path、4 个 dirty reviewed-content
  path 和 7 个仅 task-local untracked path，结果 `passed`、`errors=[]`。
- 本轮重跑 runtime 382/382、全部 13 个 Skill package contract 130/130、
  Finish-family source/installed 各 11/11、preset 45/45，并通过 source/installed package
  closure、ownership schema 3.0、dogfood drift、Python/shell syntax、JSON/JSONL parse、
  task validate、`git diff --check`、canonical/dogfood parity、配置 hash 与零 sidecar 门禁。
- `guru-phase2-check-4.0` recorder 绑定
  `phase2_capture_commit=84735037ce3154b7782ba51b0e45915d748ed065`、
  `reviewed_content_sha256=e20074f5c7ad3e52c87b9207006de80a854331986b8860a8d1cbe9f6d40eb357`、
  1009 个 reviewed paths、九个 passed adequacy dimensions、`findings=[]` 与
  `consumer=guru-create-task-commit`。
- checker 返回 `status=ok`，public wrapper 返回唯一 DTO：
  `passed(task_ref=.trellis/tasks/08-05-177-content-identity-boundary,
  phase2_commit_anchor=84735037ce3154b7782ba51b0e45915d748ed065)`。
- exact remote branch marketplace install 因分支尚未 push 保持
  `blocking=false` 未验证项；不折算为通过，也不阻塞本次 pre-commit Phase 2。
- 本节不声称 commit、F006/F007 transient closure、fresh-final Branch Review、push、PR、
  finalization 或 cleanup 已完成。

## 6. Review Gate

- Phase 2 `guru-check-task` 必须覆盖完整 dirty path 与本测试计划。
- 最后一次 reviewed-content commit 后只运行一次完整 Branch Review。
- Branch Review 之后的 task/publication/finalization metadata 不触发 Phase 2 或 Branch Review 重跑。
- commit、push、PR、finalization 与 cleanup 均在当前实现验证完成后另行取得独立副作用确认。
