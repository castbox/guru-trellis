# #184 修复扩展安装验证的目标仓库与扩展源身份混淆

## Goal

修复 `guru-verify-extension-installation` 的单 checkout 身份模型，使业务目标仓库与
Guru Team 扩展源仓库分别解析、检出、校验和记录，并恢复跨仓库 task-bearing 安装验证。

## Authority And Current Baseline

- 需求权威：live `castbox/guru-trellis#184`，读取时间为 2026-08-06。
- 实现基线：`main@804419859abd1b6004abb2dcabf236a1a84fee19`。
- 当前缺陷已在 `castbox/guru_ai_roleplay` 的正常 task-bearing 路径复现：目标 ref 与
  checkout 校验成功，但 runtime 在目标仓库中寻找 `guru-trellis` installer，最终返回
  `installation_contract_unavailable` 和 `blocked`。
- `codex/extension-installation-source-contract` dirty worktree 仅提供候选设计与测试思路；
  本 task 不复用其 task 状态、旧基线、`.bak`、本地验证或发布证据。

## Requirements

### R1. 双身份与双 checkout

- `target_repository` 仅拥有目标 repo/remote/ref/HEAD、Branch Review continuity 与
  target reviewed-content identity。
- `extension_source` 仅拥有 installed manifest 指定的 source repo/ref/commit、installer、
  canonical assets、ownership 与 sidecar facts。
- Executor 必须建立隔离的 `target_checkout` 与 `extension_source_checkout`；任一身份不得
  覆盖另一方，source asset 读取不得回退到 target checkout。

### R2. Manifest provenance 与 ref resolution

- Task-bearing workflow 和带 task 的 standalone 调用必须从目标 checkout 的
  `.trellis/guru-team/extension.json` 解析 source provenance。
- Annotated tag 使用 peeled commit；branch 与 lightweight tag 使用 direct commit。
- Resolved source commit 必须与 manifest `source.commit` 完全一致；manifest 缺失、损坏、
  source drift、ref/commit 不一致或 source checkout HEAD mismatch 均 fail closed。

### R3. Standalone fallback

- Taskless standalone 只有在 caller 明确验证 source repository 且 installed manifest
  不可用时，才使用 public repo/remote/ref locator。
- Fallback 必须记录 `manifest_provenance=not_available`，并执行与 manifest 路径相同的
  ref resolution、checkout HEAD、installer、asset、ownership、sidecar 与 redaction 校验。
- Malformed manifest 不是 absent manifest，不得触发 fallback。

### R4. Evidence 与 public API

- Private/execution evidence 升级为能完整表达 target/source 双身份的 current-only schema；
  旧 shape 不保留兼容 reader。
- Target reviewed-content digest 只能从 current task root 或 target checkout 计算。
- Installer、canonical workflow/runtime/schema/package assets、ownership 与 sidecars 只能从
  extension source checkout 计算。
- 四个 public typed exit 与 downstream consumer 保持最小 DTO，不暴露 private source
  inventory、完整 command facts 或 machine-local path。

### R5. Locator 与语义门禁

- Source locator 只接受 credentials-safe canonical GitHub URL；credential-bearing URL 在
  clone 与 artifact write 前阻断，错误输出不得反射敏感 locator。
- Command exit 0、空 findings、checker success、production eval 或 dirty local fixture 均不
  单独产生 `verified`；AI 继续拥有 applicability、adequacy、finding 与 route 判断。

### R6. Canonical、安装副本与文档

- 更新 canonical runtime、schemas、package contract、examples/evals、tests、extension
  manifest inventory、durable specs 与 public README。
- 通过 preset apply 同步 `.trellis/guru-team` 与 Agents/Codex/Claude/Cursor 声明副本；不得
  手工维护漂移副本。
- 验证 source/installed closure、canonical/platform equality、ownership、overlay drift、
  update/reapply 与 recursive zero-sidecar。

## Acceptance Criteria

- [ ] AC1：业务 target 与 `castbox/guru-trellis` source 在 execution/private evidence 中以
      两套独立 identity 存在，Afizzy task-bearing 路径从 installed manifest 选择 source。
- [ ] AC2：`v0.6.5-guru.3` annotated tag 的 direct object 与 peeled commit 被分别解析；
      peeled commit 与 manifest commit 完全相同时才能进入 source checkout。
- [ ] AC3：删除 target fixture 中的 `verify-throwaway-install.sh` 不影响合法 source checkout
      成功；source installer 缺失必须在 source 边界失败。
- [ ] AC4：manifest 缺失/损坏、source drift、source/target checkout mismatch 与 target
      reviewed-content mismatch 均 fail closed，且不产生 `verified`。
- [ ] AC5：taskless source fallback 明确记录 `manifest_provenance=not_available`；带 task 的
      调用不使用 fallback。
- [ ] AC6：credential locator 与 stale evidence 有独立回归；输出和 artifact 不含敏感 URL。
- [ ] AC7：source/installed package closure、canonical/dogfood/platform equality、ownership、
      overlay drift、clean install/update/reapply 与 recursive zero-sidecar 全部通过。
- [ ] AC8：完整当前 diff 通过 Phase 2 check 与独立 Branch Review，无未关闭 P0-P3 finding。
- [ ] AC9：本地实现与验证不会被表述成新的 immutable release 或 Afizzy 重跑证据；远端
      release、安装与 Afizzy verifier 重跑留在后续独立副作用边界。

## Out Of Scope

- 不修改 Afizzy 产品代码、canonical 文档或 closeout plan，不复制 installer 到业务仓库。
- 不把 required verification 改为 `not_required`，不修改 public exit consumer 语义。
- 不修改 Trellis upstream、全局 npm 或 `node_modules`。
- 不实施恶意 actor、对抗输入、并发竞态、锁、TOCTOU、额外 fault injection 或跨 OS
  crash consistency。
- 不直接复用、清理或提交旧 dirty candidate worktree。
- 不在本 task 自动 commit、push、创建 PR、merge、tag、release、安装到目标仓库或清理。

## Open Questions

无阻塞产品问题。Schema 的精确字段布局由 design 约束，实施中不得改变上述身份边界、
fallback 条件、public DTO 或非目标。
