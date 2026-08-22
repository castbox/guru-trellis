# #295 修复 Phase 0 Sync 到 Discovery public handoff 断链

## 1. Goal

修复 `guru-sync-base:synced` 到 mandatory
`guru-discover-change-context:pre_task` 的 public handoff，使 honest caller 仅用 Sync
public output 的 `base_current` 即可进入 Discovery semantic owner，并保持所有 private Sync
result、digest 与执行事实留在 Sync owner 内部。

Live authority：<https://github.com/castbox/guru-trellis/issues/295>。

## 2. Confirmed Facts

- 本 task 基于 clean `main` commit
  `e7df696ac3ce8365046c47bffc6059ed39ca752e` 创建；branch 为
  `fix/295-sync-discovery-public-handoff`。
- fresh `guru-sync-base` public invocation 已返回 `synced`，其 public transition 为
  `guru-stage0-transition-base-current-1.0`；完整 `guru-base-sync-result-1.0` 未进入
  public DTO。
- Discovery current owner-result schema 2.0、identity builder 与 checker仍读取
  `base_evidence.sync_result`、`base_sync_facts_sha256` 和 Sync private digest，honest
  public caller无法构造合法 owner invocation。
- `verify_installed_phase0_transcript.py` 的 `base_sync_payload()` 从
  `base_current` 反向构造 private Sync payload；当前 transcript PASS 不证明真实 public edge。
- `base_current` 已包含 Discovery live freshness 所需的 repository locator、resolution
  source、selected base、remote、ordered candidates、decision/local/remote HEAD 与
  post-sync resolution identity。
- current RDT/Architecture authority 为 `current-main-0.6.5-guru.39`；普通 task 使用
  task-owned contribution，shared current 仅在 committed independent review 后 serialized
  promotion。
- 官方 Trellis workflow 扩展合同以 Markdown 为行为入口；本 task 不修改 Trellis upstream、
  global npm 或 `node_modules`。

## 3. Requirements

### R1. Sync public contract保持单一 transition

- `guru-sync-base:synced` 继续使用现有 synced 2.0 output 和 `base_current` 1.0 transition。
- `base_current` 是 Sync 到 Discovery 的唯一 public transition。
- Sync public DTO 不增加 `guru-base-sync-result-1.0`、`facts_sha256`、完整 Git snapshot、
  private artifact locator、review history 或 authorization。
- Sync wrapper继续在 owner内部完成 resolve、execute、private check，再投影并校验
  `base_current`。

### R2. Discovery versioned public input migration

- 新增 `guru-stage0-discover-change-context-input-pre-task-2.0`，旧 1.0 schema id与
  legacy schema bytes保留为历史兼容资产，不静默复用旧 id表达新语义。
- 2.0 public input只携带 Discovery caller-owned profile、source exit、mode、change clues与
  continuation identity；repository/base authority来自独立 `base_current` transition。
- Interface、consumer input、projection、schema、example、eval与 checker全部切换到同一
  active 2.0 contract。
- Sync `project_synced` projection必须由真实 stdout确定性生成 Discovery input和独立
  `base_current`，不得要求 caller理解 Sync private runtime。

### R3. Discovery-owned base observation

- 新增 `guru-change-context-owner-result-3.0`，旧 owner-result 2.0 schema id与 legacy schema
  bytes保留为历史资产。
- 3.0 用 Discovery-owned `base_observation` 取代 `base_evidence.sync_result`；该 observation
  仅记录 Discovery live读取并直接消费的 repo、selected base、remote、authority branch、
  decision/local/remote HEAD 与 clean/current 判定。
- owner identity、recorder与 checker删除 `base_sync_facts_sha256`、private Sync schema
  definitions、private Sync result digest和同义字段。
- `base_observation` 是 Discovery owner-private gate evidence，不进入下游 public DTO。

### R4. Live authority与 typed exits

- Discovery checker按 `base_current.repo_locator`、selected base、remote与 public HEAD
  identity现场读取 authority checkout、local ref和remote-tracking ref。
- `base_current` 与 live authority一致时继续 current-state、duplicate、Docs/code/test/history
  semantic discovery，并可返回 `context_ready`。
- normal base advance、public HEAD变化或 transition freshness变化返回 `refresh_base`，唯一
  consumer 为 `guru-sync-base`。
- dirty authority、wrong branch/ref、missing或ambiguous authority、repo mismatch、结构错误
  返回 `blocked`。
- base precondition在 Issue、Docs、code、test与history读取之前判定；Discovery不执行 fetch、
  fast-forward、checkout、reset、stash或 shared authority写入。

### R5. 真实 public wrapper chain

- installed Phase 0 transcript删除 `base_sync_payload()` 及所有同义 private reconstruction。
- end-to-end fixture调用真实 Sync public wrapper，按 interface声明的薄投影构造 Discovery
  public invocation，再把真实 Discovery `context_ready` 投影到 Clarification input。
- fixture不调用 Sync low-level executor、不读取 private stdout transport、不伪造 digest、
  不 import private package runtime构造 consumer input。
- no-impact、existing Issue、proposed draft、zero-history、refresh与blocked路径保持覆盖。
- pre-task正常路由不写 tracked handoff、journal、shared cache、task、branch、worktree或
  cross-Skill checkpoint。

### R6. Managed Python dependency/runtime contract

- 所有 Python package/runtime tests通过 checkout-local `resolve-python.sh`、现有 managed
  test wrapper或 public package wrapper运行；bare PATH `python3` 的 import结果不作为产品
  dependency结论。
- PATH Python不能 import `jsonschema` 时，真实 Sync/Discovery public wrappers和targeted tests
  仍由 managed interpreter通过。
- managed runtime pointer缺失、过期、identity mismatch或 interpreter缺失时返回精确稳定
  runtime error，不得误报 test通过。
- 本 task不修改 global Python、global npm、Trellis upstream或 `node_modules`。

### R7. Canonical、投影与抗漂移闭环

- 同步 canonical package、workflow consumer contracts、registry/interface、schemas、examples、
  tests、evals、migration/activation inventory与sidecar检查。
- 通过 preset apply同步 dogfood installed package及 Shared/Codex/Claude/Cursor selected
  projections；生成副本不成为语义 source。
- 更新 workflow/spec、preset/installer与对应 README，使 public edge、managed Python和
  version migration叙述一致。
- reapply、update、dogfood drift、installed validation与 recursive zero-sidecar均通过。
- 执行一个代表性 clean throwaway，证明真实 installed Sync-to-Discovery-to-Clarify edge。

## 4. Acceptance Criteria

- [ ] A1 / R1：detached invocation通过真实 Sync public wrapper绑定 clean `main` authority并
  返回 `synced`；public shape仍为 synced 2.0 + base-current 1.0。
- [ ] A2 / R1-R2：Sync actual stdout经interface薄投影成为Discovery 2.0 public input和
  独立 `base_current`，零private result reconstruction。
- [ ] A3 / R3-R4：Discovery 3.0 owner result由live `base_observation`支撑，真实wrapper返回
  `context_ready`并继续投影到Clarify input。
- [ ] A4 / R4：normal base advance稳定返回`refresh_base`；dirty、wrong、missing、mismatch、
  ambiguous authority稳定返回`blocked`，且均不先读取后续authority。
- [ ] A5 / R4-R5：no-impact、existing Issue、proposed draft与zero-history路径无回退。
- [ ] A6 / R5：transcript verifier不存在`base_sync_payload`或同义private reconstruction；
  tests不触达Sync private runtime或low-level executor。
- [ ] A7 / R1-R3：public DTO不存在private result、完整Git snapshot、review history、
  authorization或checkpoint locator。
- [ ] A8 / R5：pre-task wrapper chain对tracked handoff、journal、shared cache、task、branch、
  worktree与cross-Skill checkpoint均为零写入。
- [ ] A9 / R6：PATH Python缺少`jsonschema`时真实wrappers和targeted tests仍通过managed
  interpreter；缺失或stale pointer返回声明的runtime error。
- [ ] A10 / R7：canonical/dogfood/installed/platform/preset parity、reapply/update/drift、
  sidecar-zero和一个代表性clean throwaway全部通过。
- [ ] A11：fresh committed `origin/main...HEAD` Branch Review无P0-P3 open finding；PR只关闭
  #295。
- [ ] A12：reviewed merge identity到达live main且Issue #295 closed后停止；不开始#286。

## 5. Docs SSOT Plan

Strategy：`delta_first`。

- 实现阶段先写task-owned RDT contribution：
  `docs/requirements-design-test-contributions/295-sync-discovery-public-handoff/`，包含
  requirements、design、test、traceability与manifest。
- 同步写task-owned Architecture contribution：
  `docs/architecture/contributions/295-sync-discovery-public-handoff.md`；change path固定为
  `target_native`，不新增ADR，因为public/private owner原则未改变，只修复现有contract断链。
- 更新`.trellis/spec/workflow/`与`.trellis/spec/preset/`中直接拥有当前行为、public I/O、
  managed runtime和验证范围的文档。
- independent committed full-diff review通过后，RDT与Architecture promotion owner按expected
  `.39` serialized promotion激活successor current；promotion delta重新进入Phase 2、commit
  与Branch Review。
- task-local planning文档不替代repository RDT/Architecture authority。

## 6. Out Of Scope

- #286 temporary-object lifecycle、#287 preset staging、#250 final Phase 0 owner graph。
- #247、#249、#261、#248、#252及任何后续Issue；#267 chain-end verification继续独立拥有。
- 业务仓库Git cleanup、第二个#295 task/worktree/branch/PR。
- Discovery history/search扩张、shared journal/cache/ledger、tracked pre-task handoff。
- 攻击模型、恶意伪造、锁、压力竞态、TOCTOU、fault injection、crash consistency与跨OS
  原子性加固。
- Trellis upstream、global npm、`node_modules`、tag、GitHub Release或开始#286。

## 7. Open Questions

无。Live Issue、fresh public wrapper输出、current code/tests、RDT/Architecture authority与官方
Trellis扩展文档已确定本task的产品、scope、compatibility、risk与acceptance边界。
