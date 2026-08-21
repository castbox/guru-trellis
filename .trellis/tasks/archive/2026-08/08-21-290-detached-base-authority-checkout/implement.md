# #290 实施计划

## 1. 建立 task-owned Docs delta

- Planning 已创建 Architecture contribution `docs/architecture/contributions/290-detached-base-authority-checkout.md` 和 ADR candidate `docs/architecture/adr/006-base-authority-checkout-routing.md`，供 Planning Architecture gate 绑定。
- Phase 2 创建 RDT contribution `docs/requirements-design-test-contributions/290-detached-base-authority-checkout/`，包含 `manifest.yaml`、`requirements.md`、`design.md`、`test.md`、`traceability.md`。
- 所有 contribution 绑定 current `current-main-0.6.5-guru.38`、design constitution `guru-trellis-design-constitution-v1`、change contract `guru-trellis-architecture-change-contract-v1` 和 Issue #290；不直接改 shared current。

## 2. 重构 base selection 与 authority binding

- 在 canonical `guru-sync-base/runtime/common.py` 中保持现有 selection precedence，并新增单一 authority checkout resolver。
- worktree inventory 只在 selected base 已确定后读取；仅接受同一 common-dir 下绑定 `refs/heads/<selected_base>` 的 checkout。
- authority checkout 校验 root、branch、HEAD/ref 和 clean；提供 missing、dirty、identity mismatch 的稳定错误定位。
- internal resolution digest 绑定 authority checkout 的 branch/head/clean identity，同时保持 result/public closed schema。

## 3. 让 execute/check/public handoff 使用 authority checkout

- executor 在 authority checkout 上执行 explicit refspec fetch 与 `merge --ff-only`，并从同一 resolver 重建 pre-sync identity。
- checker 的 `--root` 指向 authority checkout，验证 clean 与三向 equality。
- public invoke 将实际 authority checkout 写入现有 `handoff_repo_locator` 和 `transition.repo_locator`；base transition、typed exits 与 consumer 不变。
- `guru-create-task-workspace.reviewed_base_freshness` 用 `base()` 返回的完整 current
  candidates exact revalidate `transition.base.ordered_candidates`，保持 ordered candidate
  provenance 可被下游正常消费。
- current selected-base checkout 场景保持原有成功行为；detached session 不再因 symbolic branch 缺失失败。

## 4. 扩充测试与 eval

- package tests：显式/config base 不因 clean `main` checkout 回退；ordered `dev` 缺 checkout blocked；detached session + clean authority success；missing/dirty/mismatch blocked；current checkout success；behind fast-forward only。
- contract/schema tests：result/public schema、three exits、digest/freshness、repo locator 和 consumer 兼容。
- cross-package tests：workspace package 覆盖 ordered `dev -> main` provenance；sync-base
  detached ordered fixture 直接调用 downstream freshness consumer 并断言 fresh/equality。
- eval/production corpus：更新 synced/blocked 正常场景，包含 detached shell 到 selected-base authority 的一个真实 wrapper 路径。
- 代表性 Codex detached worktree：从 detached session 调用 installed public wrapper，证明输出 authority locator 和 fresh equality；不执行 #267 完整矩阵。

## 5. 同步 canonical、dogfood 与平台投影

- 修改 canonical contract/interface/runtime/tests/evals 与必要 README。
- 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`。
- 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`，检查 canonical/installed/Shared/Codex/Claude/Cursor bytes 和 executable modes。
- 递归检查 `.new`、`.bak` 与 unknown sidecar 为零。

## 6. Phase 2 验证

- 先运行 workspace boundary 与 task/package targeted tests。
- 运行 guru-sync-base package contract/runtime/eval 测试及受影响的 dispatcher/schema/manifest regression。
- 运行 preset reapply/drift 和 Issue-required representative detached validation。
- 根据 `.trellis/spec/workflow/quality-guidelines.md` 报告 package、installed、platform、representative throwaway 各自证据；未运行的 #267 release matrix 明确为 follow-up boundary。
- 完成 Architecture `task_impact_sync(stage=phase2)` 和 RDT task delta reconciliation，再进入 `guru-check-task`。

## 7. Review 与 promotion

- Phase 2 通过后创建 exact task commit，独立 Branch Review 覆盖 `origin/main...HEAD` 完整 committed diff。
- Architecture/RDT contribution 经独立 review 后分别执行 serialized promotion；promotion 产生的 shared-current diff 重新进入 Phase 2、task commit 和 Branch Review。
- Publication/Finalizer 只能消费 fresh promoted/current evidence；`#267`、tag、Release 始终不进入本 task。

## 预期修改范围

- `trellis/skills/guru-team/packages/guru-sync-base/**`
- `trellis/skills/guru-team/packages/guru-create-task-workspace/runtime/prepare.py` 与
  `tests/test_runtime.py`
- `trellis/presets/guru-team/**` 中该 package 的 managed inventory、必要 README/验证入口
- dogfood/installed 与声明平台的 generated projection
- `docs/architecture/contributions/290-detached-base-authority-checkout.md`
- `docs/architecture/adr/006-base-authority-checkout-routing.md`
- `docs/requirements-design-test-contributions/290-detached-base-authority-checkout/**`
- `.trellis/tasks/08-21-290-detached-base-authority-checkout/**`

超出上述范围的新需求、其他 Issue、业务仓库、Release Gate、tag/Release 或完整多平台发布矩阵必须停止并重新进入 owning route。

## Phase 2 implementation evidence (2026-08-21)

### Implemented candidate

- `guru-sync-base` 现按 selection -> authority binding 两阶段运行；session checkout 可
  detached，authority 只接受 same common-dir、exact selected branch、registered、clean、
  branch/HEAD/ref identity 一致的唯一 checkout。
- resolve/execute/check/invoke 复用同一 binder；fetch、ancestor probe、可选
  `merge --ff-only` 与三向 equality 均在 authority checkout，public 既有 locator 字段
  指向 authority。closed result/public schemas、Interface、README 与三个 typed exits 未改。
- canonical Skill/contract/evals、package tests、dogfood/Shared/Codex/Claude/Cursor
  projection 与 task-owned RDT contribution 已同步。shared current RDT/Architecture 未改。

### Commands and results

- `python3 -m unittest trellis.skills.guru-team.packages.guru-sync-base.tests.test_contract`
  -> `15 tests`, `OK`。覆盖 explicit/config/ordered precedence、missing 不回退、
  porcelain-z 三 record、detached authority、dirty/mismatch、current checkout 与 behind
  fast-forward。
- `python3 -m unittest trellis.skills.guru-team.tests.test_skill_packages`
  -> `8 tests`, `OK`。
- `python3 -m unittest ...SharedRuntimeTests.test_platform_projection_routes_to_installed_package ...test_source_and_installed_layouts ...test_compat_dispatch_resolves_validator_metadata`
  -> `3 tests`, `OK`。
- `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`
  -> `status=passed`, `active_packages=21`, `commands=72`。
- `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json`
  -> `status=passed`, `selected_platforms=[claude,codex,cursor]`, `sidecar_count=0`,
  `conflict_count=0`, `removal_count=0`。
- source/installed `discover-skill-contract` 与 `discover-skill-evals` for
  `guru-sync-base` -> `status=ok`；三个 eval case 与 synced/skipped/blocked output schemas
  均被 current Interface 1.4 发现。
- `.codex/skills/guru-sync-base/scripts/invoke.sh --json --invocation -` against detached
  installed fixture `/tmp/guru-290-installed-codex.pQRuE0` -> `exit_id=synced`，session
  detached，authority clean，handoff/transition locator 指向 authority，
  `HEAD == refs/heads/main == refs/remotes/origin/main`，post-sync digest
  `f00075321aea70285230a67b742ee900833cbca1409dee098fbe61247eddae92`。
- `ruby` YAML parse、R290/D290/T290/AC trace scan、
  `python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-21-290-detached-base-authority-checkout`
  -> passed；`implement.jsonl` / `check.jsonl` absent 按轻量 task 合同 skipped。
- canonical vs installed runtime/tests and canonical vs Shared/Codex/Claude/Cursor changed
  public files `cmp` -> all match。schema/interface/README/shared-current diff -> none。
- runtime `py_compile`、eval/facts `json.tool`、`git diff --check` -> passed。

### Preset and drift evidence

主会话在用户对两个精确 temp sidecar 目录的额外授权后执行
`trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`，结果
`status=ok`，source/installed validation passed，sidecars/conflicts zero；随后
`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 返回 `status=ok`
且 copies match。其组合 shell 的最终 exit 1 仅来自后续 `find` 访问已删除 temp 路径，
不是 apply/drift/package validator 失败。本阶段未再次执行 apply 或 cleanup。

### Explicit boundary

未运行 #267 release matrix、tag-pinned matrix、tag、GitHub Release 或多平台累计 Release
Gate；未 commit、push、创建 PR、merge 或清理 task/worktree。installed detached fixture
保留供复核。

## Phase 2 finding fix evidence (2026-08-21)

### Finding and fix

- Finding：remote-ahead 正常路径完成 `merge --ff-only` 后，checker 已验证 authority
  checkout 的 post-sync HEAD，但 public transition 仍从 pre-sync resolution 投影
  `base.decision_head`。因此 `decision_head != local_base_head == remote_base_head`，下游
  `reviewed_base_freshness` 会把刚完成的同步判为 stale。
- Fix：canonical `runtime/invoke.py` 改为从 checker 返回的 `checked["head"]` 投影
  `decision_head`。未修改 schema、Interface、typed exit 或 transition shape。
- Regression：既有 detached remote-ahead fixture 现断言
  `decision_head == local_base_head == remote_base_head == remote_head`，并把真实
  `transition.base` 交给 `guru-create-task-workspace` 的
  `reviewed_base_freshness`，结果 `fresh=true`、`three_way_equal=true`。

### Commands and results

- `python3 -m unittest trellis/skills/guru-team/packages/guru-sync-base/tests/test_contract.py`
  -> `15 tests`, `OK`（canonical edit 后和最终 reapply 后各通过一次）。
- 首次 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`
  -> `status=conflict`, exit `2`；仅产生预期的
  `.trellis/guru-team/skills/packages/guru-sync-base/runtime/invoke.py.bak` 与
  `.trellis/guru-team/skills/packages/guru-sync-base/tests/test_contract.py.bak`。
- apply 前 canonical/installed pre-fix SHA-256 分别为
  `c024a36884362bde28549090e3e94a219acf62fc35dbbdb2688b6ce2c3d900dc` 与
  `cd3a709b668a8844b5d47bdc2f04eebcff1e36972be30b54aea82e1709804c3c`；两个
  `.bak` 分别精确匹配这些 managed bytes。删除且仅删除这两个已核对 backup。
- 再次 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`
  -> `status=ok`, exit `0`；source/installed validation passed，sidecars、conflicts、
  removals 均为 `0`。
- `PYTHONPATH=.trellis/guru-team python3 .trellis/guru-team/skills/packages/guru-sync-base/tests/test_contract.py`
  -> `15 tests`, `OK`。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
  -> `status=ok`，dogfood workflow 与 overlay copies match canonical sources。
- canonical/installed `runtime/invoke.py` 与 `tests/test_contract.py` 的 `cmp`
  -> exit `0`；全仓 `.bak`/`.new` zero check -> exit `0`；`git diff --check`
  -> exit `0`。

### Boundary

未修改 schema、Interface、README、RDT、Architecture、shared current 或其他 Issue；
未运行 #267 matrix，未 commit、push、创建 PR 或 merge。

## Cross-package finding fix evidence (2026-08-21)

### Finding and fix

- Finding：`guru-sync-base` 的 config-candidate transition 正确保留完整
  `ordered_candidates`，但 `guru-create-task-workspace.reviewed_base_freshness` 丢弃
  `base()` 返回的 current candidates，并硬要求 provenance 等于 `[selected_base]`；合法
  ordered `dev -> main` 因此在 downstream freshness consumer 被误判 stale。
- Fix：consumer 现在保留 `base()` 返回的 `current_candidates`，并要求
  `resolved == selected` 且 provenance `ordered_candidates == current_candidates`。没有修改
  schema、Interface、public DTO 或 Architecture decision。
- Coverage：workspace package 独立覆盖 ordered `dev -> main` normal path；sync-base
  detached ordered fixture 将真实 transition provenance 直接传入该 consumer，结果
  `fresh=true`、`three_way_equal=true`。

### Commands and results

- canonical workspace tests：
  `python3 trellis/skills/guru-team/packages/guru-create-task-workspace/tests/test_runtime.py`
  -> `6 tests`, `OK`。
- canonical sync-base tests：
  `python3 -m unittest trellis/skills/guru-team/packages/guru-sync-base/tests/test_contract.py`
  -> `15 tests`, `OK`。
- `python3 trellis/skills/guru-team/tests/test_skill_packages.py`
  -> `8 tests`, `OK`；source package validator -> `status=passed`, `21 packages`,
  `72 commands`。
- 首次 `apply.sh --repo . --all-platforms` -> `status=conflict`, exit `2`，仅产生三个
  预期 backups。其 SHA-256 分别精确匹配 apply 前 managed bytes：
  `prepare.py.bak=a95a0c7f13d40f42093c1d0e9449cdd19dd3c9e2e05dabed55f6e57d829989b8`、
  `test_runtime.py.bak=a0bb63919af9c60cf7025e4f96a7d87d8e04b4ce1f8c5f2aeb63d241f98dc2ba`、
  `test_contract.py.bak=a2096b85339886d2654b024860f2c43838757433abdf86b2a62989ce8de73b2d`。
  删除且仅删除这三个已核对 backup。
- 第二次 `apply.sh --repo . --all-platforms` -> `status=ok`, exit `0`；source/installed
  validation passed，sidecars/conflicts/removals 均为 `0`。
- installed workspace tests -> `6 tests`, `OK`；installed sync-base tests ->
  `15 tests`, `OK`；installed package validator -> `status=passed`，sidecar/conflict/
  removal count 均为 `0`。
- `check-dogfood-overlay-drift.sh` -> `status=ok`，copies match；三个 canonical/installed
  managed files `cmp` -> exit `0`；全仓 `.bak`/`.new` zero check 与
  `git diff --check` -> exit `0`。

### Boundary

未修改 schema、Interface、README、shared current、ADR 或其他 Issue；Architecture
contribution 仅补充受影响 consumer/evidence。未运行 #267 matrix，未 commit、push、创建
PR、merge 或清理其他路径。

## Cross-package source provenance finding (2026-08-21)

### Qualification and Architecture gate

- Fresh Phase 2 observation：合法 explicit override 与 remote-default producer transition
  仍会被 `guru-create-task-workspace` 拒绝；前者被 config-only `base()` 重选覆盖，后者
  因 consumer 不实现 remote-default 而报 `Could not resolve a configured base branch.`。
- `guru-qualify-normal-scenario:phase2_candidate_set` 对两个候选均返回
  `qualified_current`，typed exit 为 `classified`；live #290 明确拥有四级 selection 和
  downstream freshness compatibility，正常路径无需伪造、攻击或流程绕过。
- fresh Architecture `task_impact_sync(stage=implementation_discovery)` 返回
  `baseline_current` / `architecture_impact` / `target_native` /
  `reviewed_candidate`。consumer 修复仍在既有 affected boundary 内，不新增 public
  resolver、private-runtime import、owner、DTO、持久化或 shared-current write。

### Approved implementation

- workspace freshness 按 provenance source 对 explicit/config/config-candidate/
  remote-default 做 package-local live revalidation；source、selected base 与完整 candidates
  必须 exact 匹配。
- `prepare()` 只消费 freshness gate 已验证的 selected base/candidates，不再在 gate 前
  执行 config-only resolution。
- regression 覆盖 config 与 explicit 冲突时 explicit 保持优先，以及 configured
  candidates 均不存在时 remote HEAD 驱动 remote-default continuity。

### Fix and fresh evidence

- canonical workspace consumer 新增 package-local `live_base()`，按
  `explicit -> config -> config-candidate -> remote-default` 重建 current source/base/
  candidates；freshness 要求三者 exact 等于 producer provenance。`prepare()` 改为消费
  freshness 返回值，不再执行 gate 前 config-only resolution。
- canonical 与 installed workspace tests 均为 `6 tests, OK`；canonical 与 installed
  sync-base tests 均为 `15 tests, OK`；package integration 为 `8 tests, OK`。
- source/installed package validator 均 passed（21 packages / 72 commands）；installed
  sidecar/conflict/removal count 均为 `0`；dogfood overlay drift `status=ok`。
- 首次 reapply 仅生成三个预期 `.bak`，SHA-256 分别精确匹配 apply 前 managed bytes：
  `256b52d61d1e152118393456402a98910b1ab8fdeb127f6035f348bc346a87d6`、
  `d74379eefe7d45585eef8c483d333278eac970dcb7f7c9eb3c536a95767c95a0`、
  `02df54c39620533a78c1a87d063e37e74933d20986d66c553bf164b907295e84`。
  仅删除这三个已授权 backup 后，第二次 reapply 返回 `status=ok`，全仓
  `.bak/.new` 为零，canonical/installed 三文件 byte-equal。
- fresh independent `trellis-check` 重读 live #290、planning、完整 current diff、
  canonical/installed producer 与 consumer 后结论为 P0-P3 无 findings；observations
  01/02/03 均不再复现。

### Boundary

未运行 #267 Release Gate、多平台累计发布矩阵、tag 或 Release；未 commit、push、创建
PR、merge、promotion shared current 或清理 task/worktree。此前代表性 installed Codex
detached wrapper 证据继续只证明 #290 normal path，不冒充 release-wide compatibility。
