# #311 修复 installed Finalizer provenance source/target checkout 混淆

## 1. Goal

修复 `guru-finalize-task` 的 pre-PR provenance metadata-tail producer，使安装在业务仓库中的
Finalizer 从当前安装 manifest 解析并检出精确 Guru Trellis extension source，同时在业务仓库的
reviewed checkout 中执行 preset apply、校验唯一 metadata-tail 并继续 ordinary publication。

Live authority：<https://github.com/castbox/guru-trellis/issues/311>。

## 2. Confirmed Facts

- 本 task 基于 `main@d907fcc5e17f23b6499648e5e9a208457f2d6f8b` 创建；branch 为
  `fix/311-finalizer-provenance-source-checkout`。
- `castbox/playable-ads-guru` 安装 `v0.6.15-guru.1` 后，Publication checker 与 public invoke
  返回唯一 `ready`，Finalizer preview 返回 `reprepare_required`；executor 随后报
  `Canonical preset apply entry is unavailable for provenance preparation.`。
- `prepare_provenance_metadata_tail()` 目前从业务仓库的 `reviewed_content_head` 创建 detached
  checkout，并在同一 checkout 内查找 canonical
  `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`。业务仓库不携带该
  source-only 路径。
- 上述错误字符串只记录 current failure evidence，不定义 target contract。
- installer 写入的 `.trellis/guru-team/extension.json` 已拥有 extension source 的
  `repo/ref/commit/tree_state/is_mutable_ref`。正式 Git 安装的 `ref` 与 `commit` 为完整 commit OID。
- 现有 verifier 已证明 manifest-bound source 解析、canonical GitHub locator、exact-OID fetch、
  detached checkout 与 HEAD 校验可行；Finalizer 不调用 verifier lifecycle，也不读取 verifier
  owner state。
- 现有 provenance validator 强制 `source.ref == source.commit == reviewed_content_head`。该规则只
  适用于 Guru Trellis self-hosted target，不适用于 extension source 与 target repository 分离的
  installed business target。
- current Requirements/Design/Test 与 Architecture authority 为
  `current-main-0.6.5-guru.40`。本 task 不把 task 三件套当作 repository shared authority。
- #267 独占 release-wide exact-candidate matrix、tag 与 Release；本 task 只承担 #311 修复与精确
  回归证据。
- current clean candidate `cdc55ca93bc28934bfaa1c4ba48aeef83baf3277` 的第 3 次且最后一次
  standalone throwaway 已越过 caller inventory 并进入 default compatibility matrix，但 outer verifier
  只保留整段 stdout/stderr hash 与 size；matrix 临时目录清理后，失败 cell、stage、command 与 error
  tail 均不可恢复。对该 candidate 禁止第 4 次完整 throwaway。

## 3. Requirements

### R1. 两个 checkout、两个身份

- provenance 准备必须建立 `target_reviewed_checkout` 与 `extension_source_checkout` 两个独立
  checkout。
- `target_reviewed_checkout` 属于业务 task repository，`HEAD` 必须是
  `reviewed_content_head`；preset apply 的 `--repo` 与 metadata-tail commit 只能作用于该 checkout。
- `extension_source_checkout` 只提供 canonical preset implementation；它不得接收业务 task 内容、
  task artifact、Finalizer state 或 publication mutation。
- 两个 checkout 的 repository identity、commit identity、clean state 与用途必须分别校验；不得用
  路径存在性或本机隐藏 checkout 推断 source。

### R2. Extension source binding

- Finalizer 必须从 `target_reviewed_checkout` 的当前 installed manifest 读取 source
  `repo/ref/commit/tree_state/is_mutable_ref`，并拒绝缺失、malformed、dirty、mutable 或 commit
  非完整 OID 的 source identity。
- installed business target 中，`extension_source_checkout` 必须从 manifest 的 canonical source
  repository 按 exact commit OID 获取，配置 canonical `origin`，detached checkout 后验证
  `HEAD == manifest source.commit` 且 worktree clean。
- self-hosted Guru Trellis target 中，extension source 与 target repository identity 一致；source
  checkout 必须绑定 `reviewed_content_head`，保持 #191 的 self-hosted 行为。
- Finalizer 必须在 package-local runtime 内拥有 source binding 与 checkout helper；不得调用
  `guru-verify-extension-installation` 的 profile、gate、transaction、artifact 或 typed exit。

### R3. Binding-aware metadata-tail contract

- metadata-tail commit 的 parent 必须是 target `reviewed_content_head`，且 changed path 仍只有
  `.trellis/guru-team/extension.json`。
- post-apply manifest 的 source `repo/ref/commit/tree_state/is_mutable_ref` 必须绑定本次
  `extension_source_checkout`，不得绑定 installed business repository HEAD。
- self-hosted mode 的 post-apply `source.ref/source.commit` 必须是 `reviewed_content_head`。
- installed mode 的 post-apply `source.ref/source.commit` 必须是 manifest-bound immutable extension
  source commit；`source.repo` 必须保持同一 canonical repository identity。
- 现有 allowlist 继续限制 `installed_at`、声明的 managed hash 与四个 source 状态字段；额外
  managed byte、task content、config、sidecar 或 manifest field 变化必须 fail closed。
- 每个 reviewed head 只能形成一个校验通过的 metadata-tail child；`publication_head` 必须是该
  child，`reviewed_content_head` 保持不变。

### R4. Finalizer routing 与 recovery 不变

- `reprepare_required`、`reprepare_preview`、ordinary publication transaction、Draft PR、archive、
  Ready 与 terminal `ready_for_merge` 的 public ids、consumer 与顺序保持不变。
- post-bind existing-PR recovery 必须继续先于 pre-PR provenance inference；匹配 transaction 不得
  回退到 source resolution 或 fresh reprepare。
- remote/head/PR/Issue scope、Publication title/body、plan digest、archive 与 terminal freshness gate
  不得放宽。
- source resolution、fetch、checkout、apply 或 validation 失败时，Finalizer 必须在 PR、archive、
  Ready 与 Issue mutation 前停止，并返回精确错误原因。

### R5. Canonical 与安装投影

- semantic source 只在 `trellis/**` canonical package、preset、workflow/spec 与 README 中修改。
- preset apply 必须同步 dogfood installed package、Shared/Codex/Claude/Cursor projection；生成副本
  不得反向成为 source。
- source/installed package graph、interface/schema/command、mode、managed provenance、reapply、
  drift 与 sidecar-zero 必须保持一致。
- installed package contract tests 必须只从当前 package/shared installed runtime 推导依赖路径，不得
  读取业务 target 不存在的 canonical `trellis/**` source tree。

### R6. 回归覆盖

- focused tests 必须覆盖 self-hosted target 与 installed business target 两种 binding。
- installed fixture 的 target repository 不得含 `trellis/presets/guru-team/**`，source 只能来自
  manifest-bound exact extension commit。
- missing/malformed repo、非完整 commit、dirty/mutable identity、exact-OID fetch mismatch、source
  checkout dirty、canonical apply entry missing、额外 target diff、managed-byte drift 与 sidecar
  必须 fail closed。
- 一个代表性 clean throwaway business closeout 必须覆盖 Publication `ready`、Finalizer preview、
  `reprepare_required`、execute、`reprepare_preview`、Draft PR、archive、Ready 与 archive 后
  `ready_for_merge`；任何 GitHub mutation 使用独立的当前对话授权。

### R7. Standalone verifier failure evidence

- standalone extension verification 失败时必须在临时目录清理前保留受控、schema-valid 的失败阶段、
  matrix cell（若已进入 cell）、稳定 command label、exit code 与 bounded error tail；现有 hash/size
  继续保留。
- credential、token、带认证 remote 与环境 secret 不得进入诊断字段；无法解析的 failure output 必须
  显式分类，不得静默退化为只有 hash/size。
- 诊断字段只属于 `guru-verify-extension-installation` standalone evidence owner，不得进入 Finalizer
  profile、transaction、gate、publication 或 Merge handoff。它只支持 #311 normal closeout 诊断，
  不把本 task 扩张为 #267 release-wide acceptance。

## 4. Acceptance Criteria

- [ ] A1 / R1-R2：installed business target 的 reviewed checkout 不含 canonical preset source tree，
  Finalizer 仍从 manifest 精确检出 clean detached extension source checkout。
- [ ] A2 / R2：source checkout 配置 canonical `origin`，exact-OID fetch 后
  `HEAD == source.commit`；repo/ref/commit 或 clean/mutable mismatch 在 apply 前阻断。
- [ ] A3 / R3：preset implementation 从 extension source checkout 执行，`--repo` 精确指向 target
  reviewed checkout；两个 checkout 的写入边界无交叉。
- [ ] A4 / R3：metadata-tail commit 只有 extension manifest 一个 changed path，字段 diff 位于现有
  allowlist，parent 为 target reviewed head，publication head 为唯一 child。
- [ ] A5 / R3：self-hosted post-apply source commit 绑定 reviewed head；installed post-apply source
  commit 绑定 immutable Guru Trellis commit，且不被业务 repository HEAD 覆盖。
- [ ] A6 / R4：post-bind recovery、remote/PR/Issue scope、payload、plan、archive、Ready 与 terminal
  freshness regression 全部通过，Finalizer 仍不调用 verifier。
- [ ] A7 / R5：canonical、dogfood、installed、Shared/Codex/Claude/Cursor bytes/modes/graph 一致，
  preset reapply 与 drift 通过，`.new`、`.bak`、unknown sidecar 为零。
- [ ] A8 / R6：focused package、installer、installed runtime 与 source-resolution negative fixtures
  通过。
- [ ] A9 / R6：代表性 clean throwaway business closeout 完成完整 #311 路径；结果明确区别于 #267
  release-wide matrix。
- [ ] A10：fresh committed `origin/main...HEAD` Branch Review 无 P0-P3 open finding；PR 只关闭 #311。
- [ ] A11：reviewed merge identity 到达 live `main` 且 Issue #311 closed 后停止；不启动 #267 或修改
  playable-ads-guru #29。
- [ ] A12 / R7：focused fixtures 证明 pre-matrix、matrix-cell 与 post-matrix failure 在 cleanup 后仍有
  schema-valid bounded evidence，且不执行完整 live matrix、不对 `cdc55ca9` 做第 4 次 throwaway。

## 5. Docs SSOT Plan

Strategy：`delta_first`。

- Planning 已创建 task-owned Architecture contribution：
  `docs/architecture/contributions/311-finalizer-provenance-source-checkout.md`，change path 为
  `target_native`，以及 ADR candidate：
  `docs/architecture/adr/007-finalizer-extension-source-target-binding.md`。
- Phase 2 写 task-owned RDT contribution：
  `docs/requirements-design-test-contributions/311-finalizer-provenance-source-checkout/`，包含
  `manifest.yaml`、`requirements.md`、`design.md`、`test.md` 与 `traceability.md`。
- Phase 2 持续维护上述 Architecture contribution 与 ADR candidate。该 ADR 拥有
  self-hosted/installed source binding、两个 checkout owner 与 metadata-tail parent/source 双身份
  决策。
- 更新 `.trellis/spec/workflow/{data-contracts,companion-scripts,skill-package-contract,quality-guidelines}.md`、
  `.trellis/spec/preset/installer.md` 与 `.trellis/spec/docs/public-docs.md` 中直接拥有 source/target、
  installed manifest、Finalizer tail 与验证边界的条款。
- 更新 canonical Finalizer contract、preset README 与 workflow README 的 operator-visible 说明；
  不修改 typed exit graph。
- independent committed full-diff review 通过后，RDT 与 Architecture promotion owner 按 expected
  `.40` 执行 serialized promotion；promotion delta 重新进入 Phase 2、task commit 与 Branch Review。
- task-local planning 文档不替代 shared current Requirements/Design/Test/Architecture authority。

## 6. Out Of Scope

- 不修改 `castbox/playable-ads-guru` 的 task、branch、Issue #29、PR、runtime 或 Finalizer state。
- 不重开、编辑或关闭 #191、#195、#267、#275。
- Finalizer 不调用 standalone extension verifier，不恢复 Finalizer verification route，不新增
  cross-Skill private-state dependency；本 task 的 standalone verifier 变更仅增强其自身 failure evidence。
- 不改变 Finalizer public profile、typed exit、transaction state、Merge contract 或 Issue close
  ownership。
- 不执行 #267 release-wide exact-candidate matrix、tag、GitHub Release、版本晋升或历史 tag 改写。
- 不引入恶意 actor、伪造/篡改防御、TOCTOU、锁、并发压力、fault injection、crash consistency 或
  跨 OS 原子性加固。
- 不修改 Trellis upstream、global npm、global Python 或 `node_modules`。

## 7. Open Questions

无。Live Issue、current implementation、#184/#191/#195/#275 history、current RDT/Architecture
authority 与 installed manifest contract 已确定产品、scope、compatibility、risk 与 acceptance
边界。
