# #600：架构晋升前移与最终结果承接

本迁移改变晋升入口和直接 consumer 的合同。它不改变公共 Task schema 2.0、Delivery API 1.0、TaskId/DeliveryKey、既有阶段或其 owners。软件发布、业务安装和实际采用仍需各自的证据。

## 匹配版本

Architecture Planning 3.0 及其 Delivery Planning 投影保持原职责。非 Planning `task_impact_sync` 与 `promotion` 使用 4.0；对应 `delivery_task_impact_sync` 与 `delivery_promotion` 使用 `delivery-2.0`。新当前 selector 不把旧的 nonplanning2.0/delivery1.0 或 committed-range promotion 输入转换为新通过；历史 schema 只供固定旧安装或验证资产使用。bootstrap/repair 保持其原意义。

新非 Planning输入的 `before_authority` 定位可重读的晋升前 Git authority，`candidate` 绑定实际完整候选。promotion 固定在 `phase2`、`promotion_required`：移除尚未发生的 `committed_range` 前置，显式绑定写前 expected-current 与后继 baseline。完整拟写目标、独立评估和实际写入适用性留在原 Architecture owner 当前调用。脚本只执行 recorder/validator；它不判断充分性、不授予语义通过。

`baseline_current` 的匹配后继输出将 `before_authority`、`candidate` 交原 current router。该 router 薄承接到原 Architecture 的实际写入适用性或匹配阶段 consumer，最终 Check 读取同一晋升前 authority 并核对实际完整候选。此结果不能冒充尚未发生的 committed 独立判断。

Branch Review 增加 `delivery_promotion_reference_alignment` 输入 profile。它接收原真实 `passed` DTO、原固定 base、最终 HEAD 和当前 Check；全部差额由 Git 原受审 HEAD 到最终 HEAD 重读。原 owner 审查完整差额和依赖后，经原 recorder/checker 产生新的正式 `passed`，唯一 consumer 仍为 Delivery Review。它不读取已退休私有 checkpoint，也不要求原公共 full_review slot 在合法 rework 后仍存在。普通 Git continuity 继续只拥有真实整合的有界判断。

## 正常执行

Planning → 可审查完整实现与 Docs reconciliation → 现有 Phase2 独立 Architecture 评估及拟晋升审查 → 原 owner expected-current 分支内晋升 → 实际写入及结论适用性 → 最终 Check → Task Commit → committed 独立 Architecture 与完整 Branch Review → Delivery。

候选语义、依赖和检查义务未变且实际写入等于受审内容时，由原 owner 核验适用性；不因 baseline 身份变化重新派发同内容评估。最终 Check 仍覆盖实际完整候选。committed 阶段重新独立判断晋升前后变化、贡献、晋升文件及未修改消费者，不能以新 CURRENT 自证符合原 authority。

Task Commit 的提交后合法绑定刷新保留。无架构影响走原 no-change，不创建贡献或 ADR。多个 Delivery 各有自己的完整内容范围；“一次完整 Review”只约束稳定通过且无后续实质修订的正常候选。

## 三类在途 Delivery

| 安装切换时的真实状态 | 原 owner 的接续 |
| --- | --- |
| 尚未晋升 | 读取实际完整候选、拟写差额和原 authority，完成本次独立评估后晋升，再进入最终 Check。 |
| 已晋升、最终 Review 未完成 | 读回原意图、实际写入及原 authority。保留适用的完成事实，只补真正缺失的判断和最终门禁；不创建第二个后继版本。 |
| 最终 Review 已完成 | 保留真实完整 Review 和晋升事实，核对其当前适用性后继续。若仅需本次晋升引用/状态对齐，使用窄 profile；否则按真实变化回原受影响 owner。 |

旧结果缺失、过期或不能证明适用时回原恢复或补审路径，不从版本号、同一路径、phase 或旧 passed 推导新通过。安装升级本身不触发重复晋升。

晋升后的 finding 修复改变贡献、架构判断或 baseline 陈述时，原 owner 更新受影响内容并完成必要评估，返回适用当前候选的正式结果。架构内容未变时，不因 HEAD 改变重复晋升。finding owner closure、真实未完成后的 replacement 和 distinct fresh-final 保持原合同；协调会话切换不改变职责。

## partial write 与输出丢失

原 Architecture owner 读回原意图和实际文件，区分已完成、未完成、冲突。意图可唯一恢复且无冲突时，仅补未完成内容，核验完整后才返回成功；已完成内容及后继版本不重复创建。意图无法唯一恢复或有冲突时停止写入，沿原阻塞处置，不猜目标或覆盖冲突。超出原受审内容的恢复返回受影响架构评估。

expected-current 不匹配时先判断真实差额和依赖，不覆盖新的 current，也不因版本前进重跑无关业务验证。不引入长期审查日志、授权记录、锁协议或第二状态机。

## 完整安装与验证边界

canonical workflow、Skill packages、runtime、schemas、consumer 和声明平台投影必须来自匹配的完整版本。已有项目按原官方 workflow preview/apply 与完整 preset reapply 路径更新；旧版本状态转换由原安装 owner 处理，不热替换活跃任务的少数受管文件。保留用户本地内容，逐项处理 `.new`/`.bak`，完成 installed/platform/reapply/drift 验证后才使用新入口。

源码仓库的 dogfood 同步不自动证明业务项目已升级。结构/schema/预填 DTO 只提供客观合同证据；实际 AI 读取、独立判断、写入、Check、完整 Review 和 consumer 接续单独观察。完整累计多平台 Upgrade/Release 矩阵不属于本 Issue；实际结果与未验证项由本次唯一 Test 文档记录。
