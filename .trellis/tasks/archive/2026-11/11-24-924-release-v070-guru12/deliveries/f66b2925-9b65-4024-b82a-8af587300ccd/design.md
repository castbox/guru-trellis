# D3 实际 dogfood 工具采用设计

## 1. 目标与基线

本批对应 AC02。固定内容基线 B 与规划 HEAD 为前序已交付的 `b77923c4ea1756386000bc0450985273c14a7261`。目标 `castbox/guru-trellis:main`。候选架构结论 `no_architecture_impact`，相关责任见 ARCH-INT-008、014、015。

## 2. 当前边界与差额

#925 和 #926 已合并，完整干净源码采用前序已交付提交 `b77923c4`。准备目标仍安装 .11。实际只读预览已返回当前的 source 和目标工具清单。待采用 .12 并交付已安装受管内容。

## 3. 来源设计处置

| 来源承诺 | 处置与落点 | 理由 |
| --- | --- | --- |
| 发布合同先交付干净源码，再实际采用 | retain，第4、6节 | #926 已合并且树一致 |
| 原 tools owner 独占预览、准备、写入和同事务恢复 | retain，第4、6、7节 | 工具数据源、备份及受管范围继续由已有入口核对 |
| 验证目标真实工具、保留用户和同级状态 | retain，第5、8节 | 原入口提供实际文件和本地状态证据 |

## 4. 模块与取舍

从独立干净已交付 checkout 运行 canonical `guru-upgrade-tools`。匹配 Fork 以 source lock 中 `e3793251fad8bd261d0c370d408c7675b9f6a140` 的 .6 构建为准。目标绑定现有 #924 注册 worktree。原官方 SDK 管理 Trellis workflow 和工具，原 preset 管理 Guru 资产。沿用既有单 checkout 安装协议。

## 5. 接口与数据

使用 `install` 的 `source_locked`、绝对目标位置、已交付 source ref、原公共工具计划。workflow 使用 reviewed canonical 内容及对应 immutable provider。预览中可选的 `.trellis/config.yaml` 来源差异按用户配置保留。`AGENTS.md` 使用原文件内容作为 custom 输入，工具 owner 仅渲染其管理块。保留其余合法原设置、Task 与会话状态。

## 6. 顺序和失败流程

刷新目标预览并核对写集，使用原 owner 单次准备并读回冻结计划，执行写入。若原 owner 返回 `resume_required`，使用同源、同目标和原恢复引用。冲突、缺匹配来源或校验失败停在实际 owner。执行后核对目标安装、受管范围和保留。将真实安装结果作为 D3 交付。

## 7. 恢复、兼容与集成

源固定为已交付 `b77923c4`。工具 reader 与 source lock 对应。安装范围是单 checkout，保留同级工作区、Task、会话、归档和用户配置。合并后的实际准备结果由 Completion 读取，正式发布使用准备归档合入后的 main。

## 8. 验证设计

V1 原 tools owner 对实际准备 worktree 返回 `tools_upgraded`，无法读取目标本身时不能判定通过。V2 读目标的 installed manifest、CLI、锁及 managed source，实际跑 installed validator、ownership、drift、当前 native continuation，核对所有预期字节差异和用户预像。V3 核对 sidecar、diff 及实际安装来源为前序已交付 commit。保留本地 user config 和 Task 状态。

## 9. Canonical 引用与差额

ARCH-INT-008、014、015 定义源、官方与 Guru tools 的分工。现有 `guru-upgrade-tools` 合同继续拥有采用行为和验证。当前仅实现版本投影采用，没有新的业务合同或未决项。
