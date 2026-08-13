# #217 Branch Review Gate 持久化需求

## 目标

修复 `guru-review-branch` recorder 只返回 gate JSON、却不写入 owner-private `review-gate.json` 的 package-local runtime 缺口，使 checker 和 public invocation 能在正常公开 wrapper 路径中完成 `record -> check -> invoke -> retire/retain` 生命周期，无需 Agent 手工复制 recorder stdout。

## 需求权威与当前事实

- Live authority：`castbox/guru-trellis#217`，2026-08-14 读取时为 open、无评论、唯一 assignee 为 `wesleywu`。
- 固定顺序为 `#219 -> #217 -> #218 -> #222`。#219 已由 PR #224 合并到 `main@d930d2df9bd89dc8016b44963e4e63e712b2969e`，正式 resolver 已使用受管 runtime `62965e65ece1b5add2408027` 通过固定依赖版本与 Draft 2020-12 probe。
- 当前 canonical `runtime/record.py` 只 `return validate_gate(...)`，不写 checkpoint；`runtime/check.py` 从调用者给定的 JSON locator 读取；`runtime/invoke.py` 直接消费 envelope 中的 `owner_result`，不退休 checkpoint。
- 当前 package test 在测试代码中执行 `self.write("gate.json", gate)`，并把 recorder 返回对象直接放入 invoke envelope，掩盖了公开 wrapper 的真实生命周期缺口。
- 本 task 只实现并关闭 #217。#219 是已合并前置；#218 与 #222 保持后续范围，本 task 不启动。

## 功能需求

### R1 Recorder 持久化合同

- `review-branch` 在 AI semantic review 完成并通过 current gate schema 校验后，把 compact gate 写入该 task/owner 的精确 gitignored runtime checkpoint。
- checkpoint 必须是 regular JSON file，路径由 package runtime 的单一 owner-private path resolver 决定，并绑定 task、base、HEAD/review commit、profile/review intent、typed exit 与 `reviewed_content_sha256`。
- recorder stdout 仍只输出一个最小 JSON 结果，供 caller 获取 checkpoint identity；checkpoint 不进入跨 Skill public DTO。
- 不持久化用户授权、reviewer process transcript、完整 Git/GitHub scan、无 consumer 的 hash bundle或 tracked `review.md`/handoff。

### R2 Checker 与 Invocation 生命周期

- `check-review-gate` 必须直接消费 recorder 写入的精确 checkpoint，不要求 Agent 写入或复制 recorder stdout。
- public `invoke-guru-review-branch` 必须在内部重新执行现有 objective checker，再投影唯一 typed output；caller 不得注入 checker-passed owner result绕过 checkpoint。
- terminal `passed` 成功投影后退休 checkpoint；至少一个非终态 route 按现有 re-entry consumer 需要保留 checkpoint，且重复调用行为必须确定、可测试。
- 已退休 checkpoint 的 check/invoke 必须 fail closed；失败 checker 或无效 projection 保留 checkpoint供同 owner修复。

### R3 Freshness 与路径安全

- normal recovery 只接受同 owner、同 task、同 base、同 reviewed content 的精确 checkpoint。
- stale content、错误 task/base/head、unsafe path、symlink checkpoint或祖先路径、重复调用和已退休 checkpoint均使用稳定错误 fail closed。
- 只覆盖 honest-but-fallible 正常路径，不扩展恶意伪造、锁、并发竞态、TOCTOU、fault injection、crash consistency或跨 OS 原子性。

### R4 Package 与投影一致性

- 修改 canonical `guru-review-branch` package 的 runtime、wrappers、commands/interface/schema/tests及必要合同文档；不得改变 semantic ownership、finding qualification、severity、五个现行 external exits或 consumer mapping。
- 通过 preset apply/reapply同步 installed runtime、Shared、Codex、Claude、Cursor projection与 managed inventory。
- canonical/installed package与各 public projection必须 byte-equal；dogfood drift、managed inventory和递归未知 `.new`/`.bak` sidecar必须为零。

### R5 快速发布验证边界

- 必须完成真实 wrapper-level `record -> check -> invoke -> retire/retain` 测试，测试不得手工写 recorder返回值。
- 必须覆盖 `passed`、至少一个非终态 route、stale content、错误 task/base/head、unsafe/symlink path、重复调用和已退休 checkpoint。
- 必须运行 package/runtime tests、canonical/installed equality、Shared/Codex/Claude/Cursor projection equality、targeted preset apply/reapply、managed inventory、dogfood drift和零未知 sidecar。
- 不运行完整 12-capability `guru-verify-extension-installation`；不重复完整 marketplace、official Trellis update、全平台 throwaway或业务仓库 upgrade smoke。

## 验收标准

- AC1：真实公开 recorder wrapper 成功后，精确 owner-private `review-gate.json` 自动存在且符合 current schema；测试未手工写该文件或 recorder stdout。
- AC2：真实 checker wrapper从该 checkpoint通过；public invoke内部复检并为 `passed` 输出现行最小 DTO，随后 checkpoint不存在。
- AC3：至少一个非终态 route通过真实 wrappers输出正确 DTO并按明确合同保留 checkpoint；重复 invoke不产生第二份或漂移状态。
- AC4：stale content、错误 task/base/head、unsafe/symlink path和已退休 checkpoint全部 fail closed；失败路径不错误退休有效 checkpoint。
- AC5：现行五 exits、consumer mapping、semantic review ownership、current gate schema与 public DTO字段保持兼容。
- AC6：canonical/installed runtime及Shared/Codex/Claude/Cursor投影一致，targeted apply/reapply幂等，managed inventory与dogfood drift通过，未知 sidecar为零。
- AC7：package/runtime及直接相关 integration tests通过；测试证据明确区分本 task targeted correctness与 #222累计发布充分性。

## 非目标

- 不修改 #218 Finalizer/Merge终态输出与恢复，不启动 #222累计发布门禁。
- 不改变 Branch Review finding流程、severity、review scope、typed exits或下游 publication consumer。
- 不重新引入 tracked `review.md`、`implementation-handoff.md`或公共 gate handoff。
- 不创建 tag/Release，不声称当前 `main` 已可发布或供业务仓库安装。
- 不运行完整 marketplace、official Trellis update、完整全平台 throwaway、业务仓库 upgrade smoke或完整 12-capability verifier。

## Docs SSOT Plan

- `trellis/skills/guru-team/packages/guru-review-branch/SKILL.md` 与 `references/contract.md`：Branch Review owner-private checkpoint、checker输入、invoke退休/保留行为的 step-local SSOT。
- `trellis/presets/guru-team/spec/workflow/skill-package-contract.md`：仅在需要澄清公共 Skill private state生命周期的通用规则时更新；不复制 Branch Review内部步骤。
- `trellis/presets/guru-team/spec/workflow/companion-scripts.md` 与 `quality-guidelines.md`：仅记录有直接复用价值的 recorder/checker路径边界与 targeted验证门禁；通过 preset apply同步 `.trellis/spec/workflow/**` dogfood副本。
- `commands.json`、interface/schema 与 package runtime是机器可执行合同；README不复制完整内部字段。
