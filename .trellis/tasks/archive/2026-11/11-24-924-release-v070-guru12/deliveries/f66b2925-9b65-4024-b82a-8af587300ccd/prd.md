# D3 实际 dogfood 工具采用

## 1. 整体来源与术语

Task 根 PRD 是整体要求，本批只选择 AC02。发布来源为 [#924](https://github.com/castbox/guru-trellis/issues/924) 和私有发布合同 Stage 1。`source_locked` 将干净已交付 Guru 源码与匹配 Fork 源码和构建绑定。

## 2. 整体与本批目标、非目标

真实更新准备工作区至 Guru .12，并把应交付的实际受管安装结果合入 main。整体准备归档与正式 tag、Release、Issue 关闭在本批之后执行。

## 3. 起点、前序结果、依赖与剩余责任

PR #925 已交付 .12 分发源码。PR #926 已交付版本修正，合并提交 `01cd18e3fa2b331dfa4f5c95c5c32d6f59923d10` 与审核提交 `b77923c4ea1756386000bc0450985273c14a7261` 的树相同。使用后者的干净独立 checkout 和匹配 Fork .6 构建。当前准备目标仍安装 .11。

## 4. 调用方、场景与流程

维护者预览当前目标，审核工具、workflow、受管写入及用户文件的保留策略。原 tools owner 冻结并执行安装。维护者在实际目标读回版本、来源及受管入口，再交付安装结果。

## 5. 行为、条件与约束

更新保留 Task、archive、workspace、session、用户配置、同级工作区及共用 runtime 指针。必要安装入口、source lock、模式及匹配投影由原 owner 验证。未知冲突或未消除 sidecar 阻塞。相同操作通过其原恢复引用接续。来源设计处置见 design 第3节。

## 6. 验收与未决项

AC02 要求目标中的 manifest、CLI、source lock、实际文件、原生入口及受管所有权与 .12 来源相符。检查保留边界、drift、sidecar 和 Git 差异。确认实际安装合入 main 后，准备 Task 进入 Completion。无产品未决项。

## 7. Canonical 引用与差额

ARCH-INT-008、014、015 和原 tools owner 定义既有安装责任。本批更新现有工具的实际受管投影。版本来源为已交付 #926 的完整源码。
