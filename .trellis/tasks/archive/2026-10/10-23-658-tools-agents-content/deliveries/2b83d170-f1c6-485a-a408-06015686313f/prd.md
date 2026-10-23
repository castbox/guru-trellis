# D1：AGENTS 最终内容准备与维护闭环

## 1. 整体来源与术语

本批属于 Task 658-tools-agents-content 的首个 Delivery。整体权威为 ../../prd.md 的 R1–R8、AC01–AC07，通过公共 accepted_scope 与本 Delivery scope_ref 绑定；本批 planning_root 为当前 deliveries/2b83d170-f1c6-485a-a408-06015686313f。

Direct Source：https://github.com/castbox/guru-trellis/issues/658 全文及验收1–9。必要依赖：https://github.com/castbox/Trellis/issues/57；来源采用约束：https://github.com/castbox/guru-trellis/issues/656。公共 operation 指 Fork 维护操作，Guru recovery_ref 指原 Guru 资产恢复引用，两者不合并为新模型。

## 2. 整体与本批目标、非目标

本批完整覆盖整体 R1–R8：公共 prepare 从开始即接受最终 AGENTS 内容，preset 对其幂等，恢复/回滚保留原内容与后续编辑保护，工具升级保持业务数据和非目标指针不变。交付 Guru 适配、合同和安装说明、固定依赖采用与完整定向验证；使用真实原writer生成的独立代表性旧安装核验完整维护及目标自身运行时。

本批不转换 Task/session，不同步其它 checkout，不修改已发布制品，不承担完整平台发布矩阵、业务功能改动或通用扩展框架。不以升级guru_ai_roleplay_dev作为验收，不对其原仓库做后续实质修改、安装、恢复写入或创建PR。必要时可单独clone验证，但不强制新增业务clone或外部验收门槛。

## 3. 本批起点、前序结果、依赖与剩余责任

没有前序 Delivery。当前 Guru 在公共 prepare 后修改 target，被 Fork 候选重算拒绝；后置 preset 写入又使公共恢复/回滚误判。Fork #57 提供公开准备自定义 AGENTS 内容的必要能力；依赖源码交付与 CI/source lock 未完成前，本地候选仅作开发验证。

本批交付后整体仍需 Completion 审核全部验收及独立安装证据；PR 合并不能代替该判断，正式 Release 仍归 #656。原业务失败操作已在范围调整前由未变的原来源合法回退，仅保留为历史事实，不再要求业务仓库后续操作。独立样本的恢复仍不能由新源码接管旧checkpoint。

## 4. 本批调用方、场景与流程

- DS1：Guru tools owner 选择固定来源和目标，准备完整 AGENTS 最终内容及工具计划；公共 prepare 不写目标，后续 apply 与已审查内容相同。
- DS2：带旧 Guru 块和块外项目正文的旧安装执行公共维护与 preset；块更新、正文保留、权限正确，重复应用不产生额外变化。
- DS3：公共维护或 preset 的正常执行中断后，原 owner 使用原引用恢复；完成后的内容与 DS2 一致。存在后续编辑时停止，不吸收该编辑。
- DS4：兼容且没有后续工作时原 owner 回滚组合工具写入，恢复原始字节及权限；真实用户后续编辑阻止覆盖。
- DS5：从固定匹配来源在真实原writer独立旧安装执行完整工具维护，由该目标自身runtime验证；已有符合输入和来源的fixture可作主体证据。原业务失败及合法回退仅作历史，不使用业务升级或源runtime冒充验收。

## 5. 完整行为、条件与约束

准备阶段明确上游模板处置与 Guru 块变更，保留公共 preserve/replace 等旧语义；不在 prepare 后改冻结 target、guard 或 checkpoint 规避校验。最终公共 API 方案由 design 第3节处置，需求不要求保留现有 helper。

Guru 块外的项目自定义正文和原权限保持。preset 对正确的最终块幂等；公共恢复、回滚与后续编辑保护保持原职责。工具写集不包含 Task、规划、归档、workspace/session 或其它 checkout/common 指针。

缺少公共依赖能力时在写入前给出明确前置诊断，不 fallback 至后置双写。旧 recovery 保留原来源身份；独立样本重新准备前合法处置原操作。canonical 合同与实现同时更新并通过既有机制同步受影响投影，不另建审批或持久化证明。原业务仓库后续只读，无业务PR。

## 6. 本批验收、验证方式与未决项

| AC | 整体对应 | 入口、输入与预期 |
| --- | --- | --- |
| DAC01 | AC01/AC02 | 真实 CLI/Core，旧块+块外正文+非默认权限样本：准备无写入，apply正确，preset重应用幂等 |
| DAC02 | AC03 | 公共维护与preset组合的原引用恢复及回滚；恢复原字节/权限，真实后续编辑被保护 |
| DAC03 | AC04 | 操作前后Task/workspace/session与其它指针快照一致 |
| DAC04 | AC05 | 固定匹配来源的完整独立安装与目标自身installed/native有实际结果；旧业务回退仅历史，不以业务dev升级为门槛，不对原业务仓库做后续实质修改或创建PR |
| DAC05 | AC06/AC07 | canonical/installed投影、reapply/drift/sidecar定向验证，证据层级明确 |

需求无待产品选择项。Fork来源交付及#656来源约束协调是固定来源验证的前置；不以本地API样本代替完整独立安装，也不把业务仓库升级新增为完成条件。

## 7. Canonical 引用与本轮差额

- docs/requirements-design-test-contributions/566-single-checkout-upgrade/design.md 的 D566-01/D566-06：保持原工具语义owner及两层恢复职责；本次消除准备后变更target的机制冲突。
- docs/architecture/03-domains/ownership.md 的 ARCH-DOM-047：Trellis单写公共模板/维护恢复，Guru只编排自身规则与资产，不复制公共算法。
- trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md 的 Forward behavior、Same-operation resume and rollback：受影响的当前步骤须与最终实现一致。
- .trellis/spec/preset/installer.md、upstream-ownership.md：保留上游入口归属、业务数据隔离及原安装投影机制。
- .trellis/spec/workflow/quality-guidelines.md 的 Validation Scope Ownership：定向验证，不扩张为完整发布矩阵。
