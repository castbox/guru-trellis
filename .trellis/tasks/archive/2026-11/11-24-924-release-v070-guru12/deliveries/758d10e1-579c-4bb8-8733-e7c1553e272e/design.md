# D2 升级候选版本同步设计

## 1. 目标与基线

本批承接 AC02a。开发基线 B 和规划 HEAD 为 `168e4389040e79c746878de11293d103c2ca7328`。它是前序 PR #925 已合并的候选 head。PR 目标为 `castbox/guru-trellis:main`。当前架构评估为 `no_architecture_impact`，受 ARCH-INT-009、014、015 约束。

## 2. 当前边界与目标差额

已交付 .12 扩展清单。现有工具安装在 `source_locked` 预览期间调用升级实现的 `formal_guru_source`。该函数期望 .11 并拒绝真实的 .12 源码。需同步该值及现有升级成功结果和消费者。

## 3. 来源设计处置

| 来源与约定 | 处置与落点 | 理由与影响 |
| --- | --- | --- |
| 发布合同 Stage 1 先交付干净源码，再真正采用 | retain，第6、7节 | 避免以临时验证替代采用 |
| 升级合同核对正式源码与结果的版本绑定 | retain，第4、5节 | 同步本次版本，不改判定和职责 |
| 发布合同 Fork 依赖单独锁定 | retain，第5、8节 | 保持匹配的 .6 构建和已审锁定 |

## 4. 模块与取舍

在 canonical `guru-upgrade-installation` 包中调整 `runtime/owner.py`、现有 `public-upgraded-output` schema、包内出口消费者投影及示例。在共享 `consumers/stop/production` 中同步消费 schema。采用与上一版发布相同的版本映射更新方式，避免为本次发行引入新版本协商机制。

## 5. 接口与数据

源码 manifest 的 `version=0.7.0-guru.12` 对应现有 `TARGET_GURU` 和两个 consumer、一个公开结果 schema 中的 `installed_version`。CLI 和 source lock 值保持现状。沿用现有检查命令、结果字段、分支及旧版本固定 provider 恢复。

## 6. 正常和失败流程

执行本批版本同步。用隔离测试工作区的相同源码增量构造干净测试提交，验证正式源码预览。临时安装只证明该增量可安装。正式 D2 候选经完整独立审核、Publication 和 Merge 交付。当前预览或测试失败时在本批修正并验证。

## 7. 兼容、恢复与集成

旧版已开始的操作沿其匹配 source provider 恢复。后继 Delivery 读取实际 D2 交付的干净完整源码后，在任务工作区执行真实 `source_locked` 安装。已安装工具更新不混入本批。

## 8. 验证设计

V1 运行现有安装升级合同测试、canonical 源码包校验和 diff 检查。V2 在临时安装里校验 .12 的实际平台投影。V3 使用实际匹配 Fork 和包含本批变更的干净测试源码运行只读 tools preview，确认取得可用目标预览。临时测试提交只支持该验证。正式分支提交和实际目标采用分别履行其门禁。

## 9. Canonical 引用与未决项

架构分发边界见 `docs/architecture/04-integrations/distribution.md`。安装升级语义沿用原 Skill。此次改动仅同步既有版本参数，不改变 RDT 或 Architecture 当前定义。无待决需求。
