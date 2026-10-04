# #490 Guru reference-only 创建与上游采用

## Authority 与目标

唯一需求来源：castbox/guru-trellis#490。先决上游 castbox/Trellis#25 已由 PR #26 合并；本任务解决 Guru 正式创建入口的 source disposition 限制，并采用该已合并的官方 Fork。#489 发布准备仍是独立 reference-only 任务。

## Accepted scope

- R1：现有 guru-create-task C6 input 接受 Issue source 的 exact_source 与 reference_only；正式调用现有上游 task creator，保存原 disposition，result recovery 和 source identity 与创建结果一致。
- R2：采用 castbox/Trellis@9c36002a324c16a09a85b6aa5a380b74aabf801f，main CI 37179218822 success，CLI/core 0.7.0-castbox.1。更新 source lock、正常官方模板生成、preset、dogfood、installed provenance、create-task/source current README/spec/tests。
- R3：保持 no_issue/exact_source、TaskId/generation、session、branch/checkout/resource ownership 与 Closure 行为；新增 reference-only 创建不授予关闭来源 Issue 的效果。
- R4：定向 package/runtime、官方 source projection、canonical/dogfood/installed/platform validator，加一个代表性 clean install/update/reapply、sidecar/drift 检查。旧 0.6.17 数据拒绝升级及完整发布矩阵由 #489 验证。

## 验收场景

AC1：通过正式 guru-create-task 入口创建 reference_only fixture，task.json 保存相同 repo/number/disposition；recover_creation 返回同一 TaskId/generation/TaskRef。
AC2：正式 no_issue 与 exact_source 创建仍通过；source reader、session/branch 和 Closure 的现有回归通过。
AC3：正常支持输入 follow_up/parent 不作为新创建能力；现有创建 schema 保持拒绝。不为人为伪造 artifact 增加测试。
AC4：来源 checker 确认真实 source commit/tree/parents/CI 与 build marker；官方生成及 preset apply 后，声明平台投影和 dogfood drift 无未处理差异。
AC5：代表性 throwaway clean init、preset install、当前 0.7.0 update/reapply 与正常 .new/.bak 处理通过，记录实际范围和完整矩阵未验证边界。

## 排除与交付

不新增 source writer、source 概念或公共 Skill id；不支持 follow_up/parent 创建、不迁移历史任务、不改历史版本文档；不承担 #489 Stage 1/tag/Release/closure 或 native-host 全矩阵。R1-R4 作为一个独立 Delivery 完整交付；后续发布由 #489 owner 承接。
