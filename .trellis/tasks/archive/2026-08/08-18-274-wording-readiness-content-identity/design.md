# #274 技术设计

## 1. Owner 与数据流

修复点保留在 producer package：

```text
checked wording owner scope
  -> package-local unique title/body resolver
  -> canonical title+body digest
  -> wording_current.target_content_sha256
  -> readiness normalize_prerequisites
  -> existing normalize_target content identity
```

`guru-review-contract-wording` 拥有 wording public projection；`guru-review-change-request` 继续拥有 readiness target normalization。两者只通过 public transition 与 consumer-owned prerequisites 交互，生产代码之间不存在 private runtime import。

## 2. Package-local resolver

在 `guru-review-contract-wording/runtime/common.py` 增加一个窄 helper，输入 checked scope，输出 canonical target content digest：

1. 收集 `field=title` 的全部 item。
2. 收集 `field=body` 的全部 item。
3. 两组数量必须各为一；否则抛出 `CommandError("stale_identity", "owner_result.scope", ...)`。
4. 使用现有 `digest()` 对固定 key 的二字段对象计算摘要。

`runtime/invoke.py` 只调用该 helper 一次，并把结果写入顶层和内嵌 wording projection。Helper 不读 GitHub、不修改 scope、不重新 hash 原文，也不接受 caller 提供的预期 digest。

## 3. Consumer 与兼容边界

- `guru-review-change-request/runtime/common.py::normalize_target()` 不改。
- Public output 字段、schema、Interface、typed exit 和 consumer mapping 不改。
- Draft 与 live Issue 使用同一 title/body scope 合同。
- `explicit_paths` 与 `planning_artifacts` profile 不生成 Stage 0 target projection，行为保持不变。
- 旧 body-only transition 不能继续消费；fresh Intake 会重新运行 wording 并生成 current identity。

## 4. 验证设计

### 4.1 Package tests

在 wording package test 中构造 schema-valid checked owner 与 `clarity_current`：

- positive：title/body 唯一，验证 canonical digest、顶层/内嵌一致和 transition id 派生；
- structure negative：分别删除 title、删除 body、复制 title、复制 body，验证稳定 error code 与 field path；
- profile isolation：现有 explicit-path pass 继续保持无 Stage 0 transition。

### 4.2 Cross-package Stage 0

修改 installed Phase 0 transcript 的 readiness owner builder：

- 从实际 `wording_current` transition 读取内容身份；
- 禁止从 wording owner scope 再次重算；
- 用该值投影 clarity/wording prerequisites；
- 继续调用 production readiness recorder、checker 和 public invoke。

在同一真实链路增加 title-only 与 body-only 漂移断言。每个负例使用旧 wording transition 配合只变更一个字段的 current source，预期 readiness recorder/checker 因内容身份不匹配而 fail closed。

### 4.3 Distribution

先改 canonical package、canonical preset spec 和 transcript verifier，再运行 preset apply。Installed dogfood 获得完整 package；Shared/Codex/Claude/Cursor 只获得 manifest allowlist 内的 public files。Source/installed validator、package inventory test 和 dogfood drift 证明无漏同步或 private runtime 泄漏。

## 5. 方案取舍

### 保持 consumer 接受 body-only

拒绝。该方案会让 title 漂移绕过内容身份，并削弱 #101 的 canonical target authority。

### Caller 手工 canonical rebind

拒绝。当前 transcript 的手工重算已经证明这会掩盖 producer 缺陷，也会让普通调用方承担 package owner 职责。

### 跨 package 共享 private helper

拒绝。两个 package 维持独立 runtime；相同 canonical JSON 形状通过 public contract 对齐，不通过 private import 耦合。

### 升级 schema 或新增字段

拒绝。现有字段语义已经是 target content identity，本 task 只纠正 producer value，不引入兼容面。

## 6. Docs SSOT Plan

- Strategy：`ssot_first`。
- Durable behavior owner：`trellis/skills/guru-team/packages/guru-review-contract-wording/references/contract.md` 定义 change-request public projection 的唯一 title/body 与 canonical digest；`trellis/presets/guru-team/spec/workflow/data-contracts.md` 定义 `wording_current` 到 readiness 的 consumer-facing identity。
- Implementation owner：`trellis/skills/guru-team/packages/guru-review-contract-wording/runtime/`；readiness runtime 仅作为不变 consumer 证据。
- Verification owner：wording package tests 与 `trellis/presets/guru-team/scripts/python/verify_installed_phase0_transcript.py`。
- Derived copies：`.trellis/guru-team/**`、`.trellis/spec/**`、`.agents/skills/**`、`.codex/skills/**`、`.claude/skills/**`、`.cursor/skills/**` 仅由 preset apply 同步，禁止手工形成平行定义。
- Task delta：本目录三份 planning 文件与 ledger 只记录 #274 的交付历史，不成为长期 Stage 0 合同。
- Reconciliation：Phase 2 必须先更新 durable owner，再同步 derived copies；Phase 3 检查 canonical、dogfood、平台投影和 task history 一致。
- Follow-up：累计 release/完整 throwaway 矩阵留给 release-owned task，本 task PR 仅披露未执行边界。

## 7. 回滚与风险

本修复没有持久状态迁移。回滚一个 task commit 即恢复旧 projection，但会重新暴露 readiness 阻塞。主要风险是同步遗漏、测试仍从 owner scope重算、错误地修改 consumer 或把 private runtime投影到平台目录；对应门禁分别是 preset apply、raw transition cross-package test、full diff review 与 platform inventory validation。
