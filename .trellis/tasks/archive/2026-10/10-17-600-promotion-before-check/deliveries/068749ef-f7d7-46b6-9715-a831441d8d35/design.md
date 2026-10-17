# #600 D1 设计：最终 Check 前晋升架构

## D600-01 边界与固定候选

本 Delivery 的开发基线和完整内容比较起点均为 `main@ab854ef29448910c332faadeec3c1a5dd810901d`，来源为用户明确选择的 main。PR target 为 main；远端 target 后续推进不改变这个内容比较起点。Architecture 的适用起点为该 Git 对象中的 `docs/architecture/`、`current-main-0.6.17-guru.95`、constitution v1 和 change-contract v1。RDT 起点为 `.103`。源码接受、本地验证、合入、部署和采用分别表述。

原 Architecture、Check、Task Commit、Branch Review、Delivery、Completion 和 Finish owners 保持。脚本只执行或校验真实候选、文件内容、Git、版本和公共结果关系。没有新审批阶段、审查账本、通用增量平台或第二生命周期。

EVO-001..007 的目标身份和范围不变；本次承接已有流程连续性、架构感知和官方安装投影目标，不实施 Evolution 重构。

## D600-02 独立评估、拟写差额与晋升入口

现有 Phase2 Architecture reviewer 先读晋升前 authority，再读完整 tracked/untracked 候选、受影响未修改消费者和拟写架构正文。形成判断后才核对贡献及必要 ADR。拟写内容是草稿，其他任务不能把它当作已接受 CURRENT。

直接演进原 `delivery_promotion` / `promotion` 边界，选择显式后继 schema 与匹配 Interface；旧 committed-range promotion 输入只保留为固定旧安装的历史验证资产，不在新图中双读。Planning 3.0 的 candidate/final 职责保持。需要调整非 Planning impact/public consumer 时，使用明确版本和迁移说明，同批迁移受控调用方。

晋升调用必须定位四类真实对象：

- 晋升前 baseline/constitution/change-contract 的可重读 Git 版本及本次写前 expected-current。
- 本次独立评估的实际完整 worktree 候选，包含实现、测试、文档和 RDT reconciliation；不制造未来提交范围。
- 本次拟写差额的完整目标文件和确定内容；普通内容 checksum 只服务一致性校验。
- 本轮已执行的独立评估与原 owner 的当前适用性判断。

这些对象由原 owner 的当前输入和最小私有结果承接。public DTO 仅投影下一步直接需要的 Task/Delivery、实际候选与 authority identity；完整拟写正文、文件摘要和恢复信息留在原 owner 当前调用，只有确实存在恢复 consumer 时才保留短生命周期 checkpoint。不得持久化用户授权或 reviewer 过程。

原 Architecture owner 重读 expected-current，先判断真实差额、冲突和依赖，再按受审内容写当前执行分支。分支内晋升不写目标分支。实际写入一致且语义、依赖、验证义务未变时，原 owner 核验适用性并产出绑定实际晋升后候选的正式结果，交最终 Check；不重新派发同内容独立 Architecture 评估。超出受审内容或出现新架构事实时，返回受影响架构评估。

## D600-03 比较、结果与修复

最终 Phase2 Check 覆盖实际晋升后的完整候选。committed Architecture 与完整 Branch Review 重新独立判断固定 base-to-HEAD，包含贡献、晋升文件、前后职责变化与未修改消费者。新 CURRENT 自身是受审变更，不能反向成为实现符合原约束的证据。真实决策演进必须由当前需求和必要 ADR 支持。

Task Commit 的 dirty 事务、提交后合法 Check 刷新和 clean committed re-entry 保留。不同提交或阶段不自动否定仍适用的工程命令事实；原 reviewer 先判断当前检查集合，再决定采用或补跑。旧 semantic pass、旧 project-check token 不能替代本轮判断。

晋升后的 finding 修复按实际影响回程。职责、行为、兼容、实现或验证义务改变时返回最早受影响 owner。贡献或基线陈述改变时，更新受影响内容并完成架构评估，产生适用当前候选的正式结果；旧 reviewed_promoted 不为新内容放行。未变化的贡献和已经完成的晋升不重复执行。仅 HEAD 改变而架构内容未变时不重复晋升。

无架构影响继续原 no-change 路径；不创建贡献、ADR、晋升写入或额外阶段。多个合法 Delivery 分别使用自身正常路径。

## D600-04 完整 Review 后的窄修订

在原 Branch Review package 内建立独立输入 profile，限于本次晋升的来源引用或状态表述对齐。它不使用 `delivery_base_continuity`，也不创建通用文档增量平台。

输入定位原完整 Review 的实际正式结果及其已审 HEAD/固定 base，以及最终已提交候选和当前 Check。原完整 Review 必须可恢复；可消费其实际公共输出、公共 result 或可重读事实，不能读取已退休私有 checkpoint。全部最终差额由 Git 原受审 HEAD 到最终 HEAD 识别，不能由 caller 只挑部分路径。必要 identity 只用于本次原 owner 的直接消费，不建立长期历史。

原 owner 先核对原完整范围及结果，再语义审查全部差额与受影响依赖。必须证明差额只对齐已有可核验事实，未新增架构接受、验证通过、部署完成或采用等主张，且未改变职责、行为、兼容、实现或验证义务。路径后缀、代码 tree 相同和旧 passed 均不构成充分依据。

满足条件后，原 recorder/checker 和正式 `passed` 出口绑定最终候选，明确承接原完整 Review 与已审差额；唯一 consumer 仍为 Delivery Review。当前公共 full_review 结果覆盖最终候选和当前 Check。原结果无法恢复或任一条件不成立时，返回既有恢复或受影响完整审查路径；不得把旧结果改标为新 HEAD 通过。finding closure、真实未完成 replacement 与 distinct fresh-final 合同保持。

## D600-05 恢复与安装迁移

partial write 或输出丢失后，原 Architecture owner 读回原意图与实际状态，将每个受审目标区分为已完成、未完成或冲突。原意图可唯一恢复且无冲突时，仅完成尚未完成的写入并核验最终结果。冲突或不能唯一恢复时停止写入，沿原阻塞处置；不猜内容、不覆盖冲突、不重复后继版本、不把部分写入报为成功。超出原受审内容则返回架构评估。

匹配的 MIGRATION-600 明确三类在途 Delivery：

| 状态 | 接续 |
| --- | --- |
| 尚未晋升 | 在最终 Check 前执行本次完整候选和拟晋升差额的独立 Architecture 评估，再由原 owner 晋升。 |
| 已晋升、最终 Review 未完成 | 核对已完成写入、晋升前 authority 与仍适用事实；补齐真正缺失的评估或最终 Check/committed Review，不重复晋升。 |
| 最终 Review 已完成 | 保留实际完整 Review 与晋升事实；只有需要本 Issue 受界定的引用/状态对齐才走窄修订，否则继续原下游 eligibility。缺失事实回原 owner，不能改标旧 pass。 |

canonical、workflow、完整 preset/runtime、公共 schema/Interface 和 consumer 同批安装。使用官方 workflow preview/apply 及完整 preset reapply；不热换活跃 Task 的少数受管文件。旧输入在新边界明确拒绝并给出原 owner re-entry；需要继续旧图的任务固定使用旧完整安装。没有兼容 fallback、dual parser 或第二 authority。

本 Task 在尚未晋升的 Planning/实现状态完成匹配完整安装后才采用新合同。canonical/dogfood 同步、声明平台和 reapply/drift/sidecar 验证由现有 installer 执行。公共 Task/Delivery API、身份、阶段和历史事实不迁移或伪造。

## D600-06 唯一来源与原约束处分

| 来源 | 原约束 | 处置与落点 |
| --- | --- | --- |
| #600 §2/3、AC1/4 | 原 owner，独立评估前移；完整最终 Review；no-change 与多 Delivery | retain；D600-01/02/03，canonical workflow 与原 packages |
| #600 §4.1、AC2 | 保留晋升前后比较，不能自证符合原约束 | retain；D600-02/03，Architecture project-check 与 committed Review |
| #600 §4.2、AC3/5 | 先判断真实变化，再选择受影响回程 | retain；D600-02/03/05，原 owner 适用性合同 |
| #600 §4.3、AC5 | 窄引用/状态修订必须有明确输入、绑定及唯一正式 consumer | retain；D600-04，Branch Review 窄 profile 与原 passed consumer |
| #600 §5、AC3/7 | 同操作恢复、三类在途迁移、真实独立性与 finding lifecycle | retain；D600-04/05，MIGRATION-600 |
| #600 §6、AC6/8 | Markdown 判断、版本迁移、完整投影、真实行为证据，无循环文档提交 | retain；D600-01..05，implement 的验证计划与唯一 Test |

原文没有被改为 advisory 的规范约束。ADR-005 的 committed-review-first 片段由本次 task-owned ADR 后继决定替代；ADR-019/028/029 的独立输入、阶段适用性和工程事实合同保持。必要来源可定位，但架构正文不补写最终 Branch Review pass 或最终 SHA。
