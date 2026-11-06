# D1 实施与验证计划

## 1. 输入与引用

实际读取整体 ../../prd.md、本批 prd.md、design.md 第3节唯一来源设计处置及第4–8节。研究 ../../research/compact-formal-reactivation.md 定位当前代码。实施前读 .trellis/spec/workflow 的 workflow-contract、companion-scripts、data-contracts、skill-package-contract、quality-guidelines、subtraction-first-compatibility 与 cross-layer guide；公共机制从固定成对包读取。原 #635/#669 历史结果只在仍适用范围采用。

## 2. 有依赖顺序的步骤与文件责任

- I1：实现 owner 修改 canonical Reactivate shared_finish.py/invoke.py、shared runtime identity.py 及必要 transport/installed-loader。先检查实际 API，接通 public family/key/native relation，不复制 parser。不直接修改 dogfood。
- I2：同 owner 扩展 formal archive 回归及最小 native setup helper。保留原样 compact bytes，覆盖 public operation/recovery/后继/再次归档读取，旧 families 保持回归。
- I3：原 Reactivate Markdown owner 更新 Skill/必要 README 的家族准入边界。RDT owner 为 completion-closure 三层准备并整合真实 delta，证据正文只记录实际结果。
- I4：原 guru-upgrade-tools owner 同步此工作树 dogfood 和代表目标的工具；按目标完整 source/build/API 核采用和 sidecar，不迁移本 Task 或无关历史。
- I5：实际 AI 执行 V4 的 installed 原 owners，分别记录真实 stdout 与 scope 消费。实施/check agent 进行完整候选检查，main 协调原正式 Check、commit、独立 committed Review 与交付闭环。

文件责任限上述 runtime/package/tests、原技能/README、受影响三层 RDT、必要安装投影及 Task 文档；不改公共上游源码/global npm/node_modules。代码 Agent 与其他 owners 并行时不撤销他人编辑。

## 3. 验证入口、输入与预期观察

先用固定候选 record 生成 TRELLIS_MAINTENANCE_CANDIDATE 的调用期输入，GURU_UPSTREAM_DELIVERY_SCRIPTS 指向匹配包模板。通过源 managed Python resolver 执行 Reactivate tests/test_formal_archive_reactivate.py、test_delivery_reactivate.py、test_existing_implementation.py 以及受影响 task_lifecycle identity/archive_resume tests；V1/V2/V3 对应结果见 design 第8节。

V4 仅一个必要 clean throwaway，用固定 CLI init、完整 Guru preset 和原 tools owner 更新后，由 AI 读客观前史与原历史合同，真正调用 installed wrapper、Identity/Ensure/Bind、get_context.py --mode continuation 和原 Clarify scope continuation。后继再次归档采用代表性合法状态定向 native TS/Python/Guru 检查，不重复整个生命周期。

V5 使用 check-dogfood-overlay-drift.sh、相关 package/interface/installed 定向检查、Python in-memory syntax、Task validate 和 git diff --check；检查 .new/.bak。完整多平台 installer/upgrade/Release 矩阵不属于本批。每次有写入先检查本 Task checkout boundary。

长期回归只保留能检测 accepted 行为违例的断言；安装临时路径、语义输入与原始 stdout 为外部临时诊断材料，不新增 tracked 授权、资格台账或逐测试证明文件。

## 4. 停止条件与适用回退点

公共 family/target native 不匹配时在转换前停于原 tools/source owner；source/历史资格缺口回原 Reactivate/source；真实 scope 改变回 Clarify，机制扩大回 Architecture。普通实现或测试失败在本 D1 修复，不新建切片掩盖。pending/绑定中断按原 operation 恢复，保留原档和其他任务。

无生产部署或业务数据迁移，本地可逆源码改动不需要额外发布回滚协议。保留并行改动；设施连续失败重评复现入口或明确证据缺口，不宣称依赖验收通过。所选证据充分后停止追加矩阵。

## 5. Delivery Policy（唯一）

full：D1 覆盖整体 R1–R7/AC1–AC6，交付完整 Guru 下游集成、目标 native 联合验证及必要文档同步。无延期实现切片。完整公共转换、控制/续接、scope 消费及再次归档读取均满足后才可请求 Delivery readiness；D1 merge 后仍独立 Completion→Closure→Finish，不从合并推断 Task 已完成。

隔离 local_candidate 只验证开发集成，formal_fork_source_lock、真实业务恢复和完整 Release 矩阵是本批明示边界，不能被本地成功覆盖；这些不是未交付的 accepted 业务范围。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原 guru-maintain-requirements-design-test-ssot 拥有 docs/requirements/current/completion-closure.md、docs/design/current/completion-closure.md、docs/test/current/completion-closure.md 的完整单元；consumer 为 Reactivate/Completion 及后续实现审核。delta 增补 explicit compact 正式家族、公共解释与 native consumer/验证，保留原 #635/#669 和人工/未完边界，在最终 Phase2 前整合并读回。实际结果写本主题 contribution/test，而非伪造历史 pass。

canonical Reactivate Skill 与 preset README 由本 package owner 同步；managed copies 由原 tools owner 生成。Architecture candidate_assessment 为 no_architecture_impact，不新建空 contribution/ADR 或共享导航；后续真实影响重入原 owner。历史正文/原始证据不改写为本次结果。
