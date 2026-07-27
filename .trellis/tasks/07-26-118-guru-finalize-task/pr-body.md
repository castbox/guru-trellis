## 变更摘要

- 新增公共 semantic closed-loop Skill `guru-finalize-task`，统一拥有 immutable closeout plan、精确人类 digest 确认、content push、verification routing、唯一 Draft PR identity、final projection、单次 archive metadata transaction、三方 HEAD equality、draft-to-ready 与封闭 recovery state machine。
- 建立 Interface 1.3 distinct public inputs 与六个使用 `exit_id` 的最小 outputs；`reprepare_required` 通过 target-owned `skill_input_authoring_seed` 分离 producer seed 与 fresh AI intent/context authoring fields。
- 复用既有 closeout transaction engine，增加 exact one-time、same-month、plan-bound legacy partial-plan takeover，保持既有事务顺序、generic recovery 与 cross-month reprepare 语义不变。
- 将 closeout plan、readiness、verification、PR/archive/recovery facts 和内部 transaction states 保留在 owner-private checkpoints；跨 Skill 只投影 named consumer 直接消费的最小 identity。
- 补齐真实 public wrapper production eval、per-exit actual schema selection、六 exits corpus，以及 Shared、Codex、Claude、Cursor byte-identical 分发和平台协议验证。
- 同步 canonical package、dogfood runtime、registry、extension manifest、preset installer、schemas、examples、tests 与 durable Docs SSOT；未修改 global workflow route 或 upstream `trellis-finish-work` family。

## 影响范围

本变更影响 Guru Team finalization Skill package、deterministic runtime、private gate/plan schemas、consumer projections、production eval adapter、extension registry、preset additive distribution、四个平台副本和相关 Docs SSOT。AI 继续独占 plan、scope、readiness、recovery route 与 confirmation 判断；脚本只执行、校验和记录客观事实。

现有 task publication 与 extension verification Skill 仅通过各自最小 DTO 接入 finalizer。全局 Finish family workflow/platform routing 仍由后续集成任务负责，upstream overlay 清理也保持独立；本变更不修改 upstream Trellis Skill、Command、Prompt、官方 archive 脚本、全局 npm 包或 `node_modules`。

## 验证结果

- Post-finding Phase 2：runtime 615 passed、13 skipped；Skill packages 178 passed；preset 45 passed；finalizer package 4 passed；ownership 9 passed；installed real-wrapper production eval 8/8 passed。
- Final Branch Review：focused legacy takeover/cross-month 6/6 passed；closeout transaction matrix 93/93 passed；finalizer package 4/4、installed wrapper 8/8、platform protocol 2/2 passed。
- Source/installed validators、canonical/dogfood runtime identity、Shared/Codex/Claude/Cursor package byte/mode identity、dogfood overlay drift、task artifact validation、Bash/Python/JSON checks、`git diff --check` 与 cache/sidecar hygiene 均通过。
- Clean throwaway exit 0，覆盖 workflow marketplace discovery、preset initial install/reapply、official update、managed hashes、`.new/.bak` recovery、all-platform distribution、真实 wrappers/evals 与 installed closeout recovery。
- 当前通过的是 local unpublished source throwaway。真实 pushed feature-ref verification 仍是 finalization 的 mandatory post-push gate；在它通过前不得创建 Draft PR 或 archive task。

## Review Gate

Branch Review 覆盖完整 `origin/main...4847bfb` 的 467-path committed range。历史 P1 `F-FINAL-LEGACY-01` 已由 exact one-time、same-month、plan-bound takeover 修复，并由原 finding owner 的 fresh replacement closure 与随后独立 final reviewer 复核。

最终 Round 6 为最后、current、zero-finding 的 fresh final review；P0/P1/P2/P3 均为 0，旧候选因当前正常路径证据已反证而保留为 `rejected_candidate`。正式 Branch Review recorder、checker 与 public wrapper 均返回 `passed`。

## Issue 关闭范围

Closes #118

Related #81, #115

Follow-up #119, #132

#118 的 Skill、runtime、schemas、examples、tests、eval、distribution 与 durable contracts 已由完整 diff、Phase 2 和 Branch Review 覆盖。#115 是 umbrella，由 #119 的 combined acceptance 负责关闭；#119 继续拥有 Finish family integration，#132 继续拥有 upstream overlay 清理。本 PR 不关闭或改写这些独立范围，也不改变已完成 #105 的事务语义。

## 安全说明

Public DTO 不携带 closeout plan、readiness、verification、PR/archive/recovery facts 或内部 transaction state。Task-local 与 runtime evidence 只记录去敏 repository identity、digest、HEAD、path/blob/mode 与状态事实；未发现 token、credential、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始记录进入候选变更。

本变更不新增恶意 actor、伪造 artifact、攻击模型、并发 finalizer、锁、TOCTOU、额外 fault injection、偶发 crash consistency 或跨 OS 原子性范围。没有 dependency、CI/CD、container、Compose、Kubernetes、Helm/Kustomize、DB migration、Makefile、服务部署或 production data write 变化；无需数据库迁移、配置变更、服务重启或生产回滚。

## Docs SSOT

- Strategy：`ssot_first`。
- Durable docs：finalizer step-local contract、Skill I/O、workflow ownership、companion scripts、quality、preset installer/upstream ownership、public docs 与 repository/workflow/preset README 已同步。
- Merged delta：semantic owner、single transaction engine、distinct profiles、six `exit_id` outputs、owner-private state、verification/PR/archive/recovery ordering、production eval、distribution 和 update/reapply 规则均已写入对应 durable owners。
- Task history：planning provenance、实现轮次、Phase 2 command evidence、historical finding lifecycle 与 raw Branch Review reports 仅保留在 task-local artifacts，不承担长期流程定义。
- Follow-up / limitation：global Finish family activation 与 combined acceptance 由 #119 负责，upstream overlay cleanup 由 #132 负责；exact pushed feature-ref verification 是后续 finalization 的 mandatory gate，当前 local throwaway pass 不替代该证据。
