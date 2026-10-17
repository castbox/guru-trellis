# #600 D1 需求

来源：https://github.com/castbox/guru-trellis/issues/600；整体 authority：../../prd.md。D1 完整承接整体 AC1..AC8，无剩余切片。

## 要求

1. 现有独立 Phase2 Architecture 审查完整候选及拟晋升差额，原 owner 核对 expected-current 后在当前执行分支晋升，最终 Check 包含实际晋升内容。
2. 候选及写入一致时仅核验适用性，不因 baseline 身份变化重复同内容独立评估。committed Architecture 与完整 Branch Review 仍独立覆盖最终完整范围、受影响未修改消费者及晋升前后比较。
3. 变化按职责/行为/兼容/验证义务返回最早受影响 owner；finding 修复同步受影响贡献、基线及正式结果。无架构影响走 no-change，不新增贡献或 ADR。
4. 完整审查后的窄路径只修正晋升来源引用或状态表述，承接原完整 Review 和全部差额；不得新增事实主张或借用 Git continuity。
5. partial write/输出丢失由原 owner 读回，在原意图唯一且无冲突时完成未写内容；否则停止写入。不重复版本或覆盖冲突。
6. 明确三类在途 Delivery、公共版本及完整安装迁移，保留适用事实并补齐缺失审查，不重写旧 pass。
7. 同步 canonical/dogfood/声明平台/安装投影；实际独立行为及 consumer 接续与客观 tests 分开验证。

## 验收与边界

验收逐项使用整体 PRD 的 AC1..AC8，最终 Test 文档逐项列证据和未验证边界。保留原 finding closure/replacement/fresh-final 合同。无业务仓、生产环境、完整累计 Release 矩阵、新审批链、审查账本或通用增量审查平台。
