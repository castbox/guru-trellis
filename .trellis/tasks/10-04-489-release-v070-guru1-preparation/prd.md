# #489：v0.7.0-guru.1 发布准备

## 需求来源与交付边界

来源为 castbox/guru-trellis#489，relation 为 `reference_only`。本任务只交付该 Issue 的 Stage 1 发布准备；Stage 2 从 Delivery 与 Finish 归档合并后的 fresh remote main 冻结唯一候选，独立承担 exact-candidate、tag、smoke、Release 与 Issue closure。本任务 Completion 不包含 Stage 2，Closure 不关闭 #489。

## 需求与验收

- R489-P1：根 README、workflow/preset README 与 public-docs spec 的目标仓库 tag 均为 `v0.7.0-guru.1`，extension 为 `0.7.0-guru.1`，CLI/core 为 `0.7.0-castbox.1`；predecessor 为已发布 `v0.6.17-guru.2`。版本轴独立，准备文本不声明目标已发布。
- R489-P2：公开安装文本对齐 #490 采用的 canonical Fork source lock，workflow 与 preset 使用同一 immutable release tag；未发布验证使用可寻址完整 candidate SHA。旧 `0.6.17` 安装明确拒绝 update，数据保留；不承诺原地升级、双读或自动迁移。
- R489-P3：只修改当前发布身份文本及其 project-local projection。canonical extension 版本已经正确时保持不变；历史 versions、任务、归档、已发布 manifest 与 source pin 不改写。当前 package/ownership/dogfood drift 验证通过，全部 Markdown 引用与命令保持可执行结构。
- R489-P4：RDT 与 Architecture owners 判断当前文档变化的影响；若无行为/owner/API/GAP 改变，则正式返回 current/no-change，不创建空 contribution 或空 promotion。若存在本范围要求的 shared-current promotion，则仅由对应 owner 执行，并对新增 diff 重跑 Phase 2、commit、完整独立 Branch Review。

## Delivery policy

task_scope / delivery_slice：R489-P1 至 R489-P4；本准备任务无剩余业务工作。独立可用条件为目标发布身份与兼容边界在 main 上一致，即使 Stage 2 尚未发布。验证边界为 current 文本、package/source/installed/platform/ownership/drift 定向证据；Stage 2 的 immutable remote provider、focused install/update/reapply、旧安装拒绝、secret scan、tag/Release 由 #489 发布流程承担。完整多平台/native-host 矩阵与业务仓生产安装不在本任务范围。

## 排除范围

不改变 #454 生命周期 owner，不复活 #481 人员接口，不改变公共 Skill I/O，不安装依赖、重新构建或修改既有上游 checkout。不得创建 tracked release progress、release notes、PR/Release body handoff 或动态 implement checklist。
