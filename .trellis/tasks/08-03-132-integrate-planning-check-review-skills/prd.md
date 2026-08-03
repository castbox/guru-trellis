# #132 集成 Guru planning/check/review Skills 并收敛 preset upstream overlays

## 目标

在不改写 #161 已合并 Skill 内部 semantic/runtime 合同的前提下，完成 Guru Team 全链路的最终集成：将 global workflow 收敛为 mandatory Skill invocation、typed exit、唯一 consumer 与 fail-closed stop；将 producer output 到 consumer input 收敛为唯一薄 projection；停止 preset 安装或 managed-upgrade Trellis upstream-owned 入口；以可追溯 tombstone、provenance-safe migration 和真实跨平台安装验收完成 #132 combined acceptance。

## Authority 与执行顺序

- GitHub Issue #132 正文是当前唯一需求 authority；历史评论只作定位，不增加独立条款。
- PR #167 已于 2026-08-02 合并主体 AI-first contracts；PR #168 已于 2026-08-03 合并最终 Trellis template provenance 修复，merge commit 为 `c8cdd9e7fbb73687cd700c1dbbb7a5907307476f`。Issue #161 已按 COMPLETED 关闭；当前执行顺序保持 `#161 -> #132 -> #81`。
- 本任务当前 live base、`origin/main` 与 worktree HEAD 均为 `c8cdd9e7fbb73687cd700c1dbbb7a5907307476f`。
- 本任务只消费 #161 最终 public contracts。若发现 owner Skill public contract 本身存在可复现缺陷，停止对应 #132 补丁并回到 #161；projection、platform entry、installer、ownership、update/upgrade 或 reapply 问题留在 #132。
- Close scope 仅为 #132、#127、#98、#53；#81、#108、#106 保持 follow-up，不得关闭。

## 已确认事实

1. Current main 的 source 与 installed Skill package 校验均通过：13 个 active `guru-*` Skills、51 个 external exits、13 个 workflow invoke markers、28 个 workflow targets；不存在 active legacy Skill id。
2. Canonical `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md` 当前字节一致。
3. Ownership inventory 当前保留 43 个 `transitional_legacy/active` 记录；overlay tree 当前为 43 个 legacy payload 加 3 个 Guru-owned additive entry。
4. Extension manifest 当前有 16 个 managed-path claims，其中 9 个是 Guru-owned，7 个仍覆盖 upstream namespace；这 7 个 claim 必须在本任务删除或收窄。
5. 当前 ownership validator、source/installed package validator 与 dogfood overlay drift 均通过；这些结果证明迁移前基线一致，不证明 #132 已完成。
6. Shared、Codex、Claude、Cursor 的 `guru-*` package discovery copies 已存在；current acceptance 必须在 clean throwaway 中实际安装和发现，不能只依赖分发单元测试。
7. 当前 worktree 没有 `.trellis/.developer`；执行 `get_context.py` 时，该命令以退出码 0 返回 developer 未初始化提示，而 `task.py current --source` 与 workspace-boundary validator 仍能精确定位本任务。该现象作为平台入口/安装验收事实处理，不改写 #161 owner semantics。
8. 当前 task 状态为 `in_progress`，task 目录没有 tracked `planning-approval.json`。#161 schema 3.0 contract 将 Planning owner checkpoint 放在 ignored runtime，并在 public typed output 投影后删除；因此缺少 tracked artifact 不是 bypass 证据。由于 live base 已由 PR #168 更新，本次继续执行会对当前三份 planning 文档重跑 wording owner 与 Planning owner，再消费当前 typed exit。

## 需求

### R1 Thin global workflow

- Canonical 与 dogfood workflow 必须只拥有全局 phase 顺序、stable Skill id 的 mandatory invocation、typed exits、唯一 consumers、薄 caller-owned projection 和 fail-closed stops。
- Workflow 必须删除 Planning、Phase 2、Task Commit、Branch Review、Publication、Finalizer 以及 Intake owner 的内部 checklist、finding lifecycle、confirmation 算法、recorder/checker 命令、private schema、digest/freshness/recovery 教程。
- Missing mandatory Skill、unknown/multiple/unmapped exit、consumer mismatch 或非唯一 consumer 必须 fail closed。
- Global-only 合同仍保留：workspace boundary、task activation、Docs SSOT、Issue Scope Ledger、human Markdown artifact 解析、交互预算和发布副作用边界。

### R2 唯一 public I/O projection

- 完整 producer-output -> consumer-input graph 必须覆盖 Stage 0、Planning、Phase 2、Task Commit、Branch Review、Publication、Extension Verification 与 Finalization。
- 每个 structurally distinct exit 使用独立 output schema；每个 output 字段必须有直接 consumer。
- Projection 只能执行 direct pass-through、字段选择、重命名或确定性规范化；不得读取 producer private artifact、owner checkpoint 或 runtime source 来重建 semantic intent。
- Target-owned authoring partition 必须保持唯一，不能由 workflow/platform wrapper 补写或覆盖。

### R3 Upstream ownership 收敛

- 43 个 frozen inventory entry 必须全部从 `transitional_legacy/active` 迁移为 `upstream_owned/removed`，同时保留 path、baseline hash、replacement owners、blocking/removal history、upstream producer、current Guru behavior 与 update/upgrade conflict 审计事实。
- Removed entry 不得保留 `current_payload_sha256`，不得有 canonical overlay payload，且不得被 extension manifest 或 installer 继续声明为 managed path。
- Overlay tree 最终只保留明确 Guru namespace 的 additive entry；ownership inventory 和 managed claims 中不得存在 `transitional_legacy` 或 `unclassified`。
- Trellis-generated Skill、Agent、Command、Prompt、Hook、runtime agent 回归 `trellis init/update/upgrade` ownership。

### R4 Installer migration 与 provenance 安全

- Fresh apply/reapply 不得写入或 managed-upgrade removed upstream paths。
- Existing repository migration 必须区分：clean upstream bytes、已知旧 Guru-managed bytes、缺失 path、以及未知/本地修改 bytes。
- Clean upstream bytes 必须保持不变；已知 legacy-only managed entry 必须按 reviewed migration 删除；仍为旧 Guru payload 的 upstream-generated entry 必须 fail closed 并要求先完成官方 `trellis update/upgrade`，不得由 preset 猜测或合成 upstream bytes。
- 未知或本地修改必须原地保留，并以 `.new` remediation sidecar 或明确 conflict 阻塞；不得静默覆盖或删除。
- Installed manifest、managed hashes、removals/conflicts/sidecars 与 reapply recovery 必须反映新的 ownership，不得把 removed upstream path 继续记为 Guru managed asset。

### R5 平台 discovery 与入口

- Shared、Codex、Claude、Cursor 必须实际发现 byte-identical 的 active `guru-*` packages 与 public contracts。
- Preset 不得覆盖 `trellis-start`、`trellis-continue`、`trellis-finish-work` 或 upstream sub-agent/hook/runtime-agent 文件来实现 Guru 分叉。
- 必须保留的显式入口只能使用 Guru namespace，并且只负责加载 workflow/Skill、调用和路由，不能复制 step-local 合同。
- Tool-free route 与平台 entry 必须显式到达 mandatory `guru-*` Skills；frontmatter auto-match 不能成为 mandatory invocation 的唯一保证。

### R6 Update、upgrade 与 reapply

- Clean init、workflow preview/switch、preset initial apply/reapply、`trellis update` 和版本升级后，upstream files 必须保持官方版本，Guru assets 必须由 preset 恢复且无 ownership 交叉。
- `.trellis/.template-hashes.json`、installed extension provenance、`.new/.bak` 与 legacy cleanup 必须有可执行验证。
- Dogfood canonical/installed copies 必须同步，overlay drift 为零，递归 sidecar 扫描不得遗留未处理项。

### R7 文档与验收

- 更新 canonical/dogfood workflow、ownership specs、installer/overlay specs、三个公共 README、extension manifest、schema、tests 和 throwaway verifier，使其只描述最终 ownership 与 public graph。
- README 中的 marketplace init、preview/switch、preset apply/reapply、update/upgrade 命令必须真实可执行。
- Final review 必须基于独立 current HEAD 完整 diff，覆盖 workflow thinness、public I/O、private evidence ownership、runtime-source independence、platform equality 与 upstream migration。
- Remote branch marketplace verification 与 package-local production eval 是独立证据；只有 pushed ref 验证成功才能声明 remote acceptance 通过。

## 验收标准

- [ ] Canonical 与 dogfood workflow 的 mandatory Skill markers、typed exits、consumer targets 完整且唯一；step-local internal prose 已移除。
- [ ] Source/installed Skill package validator 通过，完整 public I/O graph 无 private-artifact dependency。
- [ ] Ownership validator 报告 43 个 removed、0 个 active legacy、0 个 unclassified；overlay tree 只剩 3 个 Guru-owned additive entry。
- [ ] Extension manifest 不再包含任何 upstream namespace managed claim。
- [ ] Installer 对 clean upstream、known legacy、missing、unknown local edit 四类 migration case 按 R4 行为执行。
- [ ] Clean marketplace init、workflow preview/switch、preset initial apply/reapply 全部通过。
- [ ] `trellis update` 与版本升级后 upstream/Guru ownership、managed hashes、`.new/.bak` 和 legacy cleanup 全部通过。
- [ ] Shared、Codex、Claude、Cursor 在真实 clean install 中完成 discovery；声明平台入口语义一致。
- [ ] README 命令、dogfood canonical equality、overlay drift、可执行位和递归 sidecar 扫描全部通过。
- [ ] #112、#119、#144-#146、#131 evidence 与 current HEAD/schema/installed copies 仍一致；#161 private contracts 未被本任务改写。
- [ ] 独立 current-HEAD semantic Branch Review 无未关闭 P0-P3 finding。
- [ ] PR close keywords 仅包含 #132、#127、#98、#53；不关闭 #81、#108、#106。

## 非目标

- 不修改 Trellis upstream 源码、全局 npm 包或 `node_modules`。
- 不重写或补丁式修复 Planning、Phase 2、Task Commit、Branch Review、Publication、Finalizer 的内部 semantic/runtime 合同。
- 不实现 #108 subtraction 或 #106 merge executor，不创建 release tag，不关闭 #81。
- 不扩展恶意 actor、伪造/篡改、对抗输入、竞态、锁、TOCTOU、额外 fault injection 或跨 OS crash consistency。
- 不把 digest、private checkpoint、review history 或用户授权过程扩展为 public workflow authority。

## Docs 状态

- 状态：`stale_docs`。
- 证据：`.trellis/spec/preset/upstream-ownership.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/quality-guidelines.md`、`.trellis/spec/docs/public-docs.md` 以及三个公共 README 仍描述 43 个 active legacy overlays 和兼容 router。
- 需求影响：本任务必须先将 durable specs 收敛为最终 thin graph 与 removed ownership，再让代码、schema、installer 和验收实现与之一致。

## 中台知识 Gate

不适用。本任务修改 Trellis extension workflow/preset/platform integration，不涉及 `go-guru`、`proto-guru`、Unity Guru SDK 或 Flutter Guru SDK 合同。
