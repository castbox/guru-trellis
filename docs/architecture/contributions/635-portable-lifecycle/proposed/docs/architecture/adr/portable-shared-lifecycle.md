# ADR-PORTABLE-SHARED-LIFECYCLE：共享生命周期与本机责任分离

状态：accepted target；来源：castbox/guru-trellis#635，固定 before 为 `7a7b60743499653ffeb81f6b31e627a02c33f579:docs/architecture/`。本完整目标正文仅在原 Architecture final_integration 实际晋升后生效；隔离 proposed 文件不改变共享 authority。

## 背景与决定

原共享 Finish 准入依赖本机 seal/manual Cleanup；原 Closure 完整动作集只在私有事务；原 Open PR 恢复依赖原 transaction 和本地 branch。独立 clone 可取得相同 Task/Git/远端事实却无法接续，搬运 runtime 不能满足原机不可用的正常场景。

公共 Trellis 继续单写 Task/Delivery/session/binding、公共 parser/store、转换及恢复。Guru 原 Identity、环境、阶段、Publish/Merge、Completion/Closure/Finish/Cleanup/Reactivate owners 各自拥有原语义和确定性适配；不建第二模型、跨 owner ledger 或审批链。共享事实、当前语义判断、工程命令事实与本机资源责任分别解释。

原 Reactivate 依据准确 archive commit、TaskId/generation/source/scope、该版本终态关系、summary/archive 一致性和实际 bookkeeping PR/target 判断共享 Finish。Task2 必须有真实 Completion→Closure；指定正式 schema1 按固定前驱合同核历史，不制造旧结果。先继续可获取匹配后继，无后继才公共 reopen 或 formal operation 严格增代一次。历史 target 后续前进不否定已成立终态；未入 target 的唯一未完 closeout 才回原 Finish。人工历史保留原 legacy owner，不泛化旧格式双读。

仅对无法由现有公共结果重新推导的完整 Closure 动作集合，原 Closure 单写最小 task-local 载体并以公共 Closure evidence/AuthorityRef 关联。直接 consumers 只有原 Closure recovery 与 Finish。精确 result/key、Completion/scope/source 和 live required states 均须校验；载体不授予权限、不断言 terminal，不记授权/逐轮审计。共享恢复零 provider close，剩余真实动作回正常 Closure 当前边界。旧已完成 history 不强补 carrier，未发布必要输入准确报告缺口。

原 Publish 精确选择已有 Open PR 与 source_commit，核同 key、Planning、候选和 repo/base/head/owner；远端 full ref 不等于 B 本地 binding。只补未完成 Draft/metadata/Ready 动作，绝不创建第二 PR；当前 Readiness 必须实际适用。新的未审修订先退 Draft，早期反馈不写最终 PublicationFact。原 Merge 对 MERGED 仅恢复 Delivery fact，Completion 独立审整个 scope/actual 差额/CI；不重复 merge 或从远端状态补造 pass。

共享 Finish 成立后，本机 seal、binding 退出和 Cleanup pending 仍由原资源 owner 处理，不能阻塞不同合法新资源。local 责任限定 common-dir/generation；remote ref 按 repository/fullref/expected head 核验。旧 receipt 不删除新代或推进 ref，同资源未完责任、未知 ownership 和 caller/peer 内容继续保留。

## 具名窄替代与有效前驱

本决定保留 ADR-024 的公共模型 authority、所有原语义 owners、Refs-only/Closure、整体 Completion 和无空 Delivery；将其私有事务恢复描述补全为原 owner 可从充分共享输入恢复既成事实，历史不变成当前 gate。保留 ADR-027 的独立 tools/selected legacy 维护、完整 Plan2、公共 writer、native/下一真实 owner、回退与旧 consumer 退出；只解除其对明确支持正式 schema1 已完成归档的普通拒绝，允许原 Reactivate 调用正式公共单次增代能力。

本决定窄替代 ARCH-DOM-030/ARCH-INT-033 的 cleaned receipt 跨环境准入、ARCH-DOM-032 对指定正式旧归档仅只读拒绝，以及原 shared Finish 必须先本机 seal/Cleanup 的片段。保留 DOM028/043/044/054 的原 owners、公共结果关系和逐 Issue 核验，GOV009 的独立全链与当前副作用资格。完整新职责由 DOMAIN/INTEGRATION/GOVERNANCE 正文直接表达，旧 ADR/Git 仅保留其历史意义，不要求普通 reader 回放 override 链。

ADR-028 固定 B/阶段适用性、ADR-033 Draft 与最终 Ready 区分、ADR-034 原覆盖适用性和 ADR-KNOWLEDGE-FINAL-INTEGRATION 的最终整合顺序保持。没有宪法例外，不关闭 ARCH-GAP-006/008，不改变软件版本轴或扩大 Release 矩阵。

## 比较、迁移与退出

为已完成旧归档保代 resume 再产生新 Completion/Closure/Finish 可以形成合法新结果，但会新增旧代 bookkeeping、archive 和既有资源责任冲突。正式公共一次增代更直接；原 raw/history 只读，后续使用 current 公共模型。扩 Core Closure 模型、全局恢复台账或搬隐藏 runtime 均无必要。

新 profiles/schema/consumers、matching Fork/native 与 Guru canonical/workflow/preset/声明平台按 MIGRATION-635 成套采用。旧完整安装固定或由原工具/安装 owners 维护；不热迁移既有安装、不绕 preflight、不批量迁移无关旧档。legacy-only入口在真实旧 consumer 退出后的显式迁移删除，历史 Git/raw 与原本机资源责任保留。

完整实现与隔离 proposed targets 先由独立 Architecture 和 candidate Check 审查，再原 owners final_integration 写/readback，implementation 重建 candidate/begin_check，最终 Check、commit、独立完整 committed Review 和 readiness 覆盖真实 after。实际 V1–V8、安装、provider/Agent 层次与缺口只由唯一 Test 说明；本决定及知识晋升不证明它们通过。
