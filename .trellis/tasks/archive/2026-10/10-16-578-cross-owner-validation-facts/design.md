# #578 设计：独立判断与工程执行事实

## D578-01 三种对象
当前候选的完整语义判断、工程命令的原始执行事实、当前 owner 的结果绑定分别承接。第一种由本轮 owner 独立完成；第二种在真实依赖仍适用且合法可核查时采用；第三种由本轮真实判断完成后经过既有 recorder/checker 创建。旧 semantic pass、旧 freshness token、retired private checkpoint 均不充当第二种对象。
先确定当前完整范围、风险、消费者和适用检查集合，再查看原始结果，避免旧结果缩窄第一轮判断。工程事实采用不声称当前 reviewer 执行过原命令。

## D578-02 原 owner 最小修补
- Check：直接演进 Dependency-Scoped Validation，去除 same-owner-only 条件，补齐参数、测试期望与原始结果来源。现有 validation summary 记录实跑/采用及适用理由。
- Architecture：独立评估仍由 fresh generic reviewer 按原读取顺序执行；在本轮适用 project check 中区分语义检查和工程命令事实。project check 必须绑定当前 invocation，原始命令事实是否仍适用由本轮 reviewer 判断，不能复制旧 project-check token。
- BranchReview：当前独立完整 committed range 审查不省略；其 Architecture 前置及自身检查按真实依赖采用工程事实。修改直接冲突的派发文案，不能把重跑转给另一个阶段。
- shared engineering convention：在现有 quality-guidelines 的执行事实验证段落定义跨 owner 采用条件与验收边界；step-local 顺序和路由继续由各 Skill 独占。无新 spec/Skill/exit/DTO/状态机。

## D578-03 失效与来源
检查定义/版本、真实依赖、工具链、参数、环境、测试期望任一改变或无法判断，执行受影响检查。原始结果缺失只补该检查，新检查执行；文档改变行为合同或引入新风险时重新确定消费者及义务。文档路径或代码 tree 相同不自行证明适用。
原始事实通过合法可访问的实际命令结果、已有 summary/evidence locator 和 Git 检查对象核对。不读取其它 owner 私有状态，不为提高命中保留已退休 checkpoint，不新增账本/缓存/长期日志。无因全量与一次后永不重跑均不成立。

## D578-04 安装与迁移
公共 I/O 不变，原 token 的当前绑定校验保持；如有误导性 stale 提示，仅把“再次执行命令”收敛为“重新判断并绑定当前结果”，不放宽 validator。
产品 canonical 通过完整 preset 安装。当前开发 Task 保持原完整安装；使用包含完整候选 source 与匹配 runtime 的独立 source dogfood 执行 apply/reapply/drift、声明平台投影及一份代表性 installed 公开调用。不得热替换活跃 Task 的少数受管文件。
MIGRATION-578 只说明采用边界和旧任务完整安装路径，不引入兼容 reader；未验证完整 Release/Upgrade matrix、业务仓采用或生产效果不声称通过。

## Architecture
采用实际 candidate_assessment 的 architecture_impact/target_native。task-owned architecture-contribution.md 与 architecture-adr.md 拥有本次架构增量。ADR-019 的独立语义评估和 ADR-028 的阶段适用性继承；窄 successor 只澄清工程命令事实。首次独立 committed Review 后由原 Architecture owner 按当时 expected-current 晋升，晋升差额重经 Check/Commit/独立完整 Review。

## 原始来源约束处分
| Source | 原约束 | Disposition / landing |
| --- | --- | --- |
| #578 范围1/2 | 完整语义范围与命令范围分离；先独立判断 | retain；D578-01/02 与三个原 owner 合同 |
| #578 范围3/4 | 依赖适用且结果可核查才采用；变化/未知/缺失补跑 | retain；D578-03 与原 validation summary |
| #578 范围5 | 当前绑定、promotion、reviewer切换不能替代当前判断 | retain；D578-01/02 与现有 recorder/checker |
| #578 范围6 | 结果来源真实，私有状态消费/退休不绕过 | retain；D578-03；无新存储 |
| #578 范围7 | canonical投影与完整安装迁移 | retain；D578-04 与 MIGRATION-578 |
| #578 关联边界 | 复用#464/#567；业务项目和Release各自负责 | retain；PRD非目标与 implement 验证边界 |
来源已包含规范性机制约束，以上全部保留；未改变或拒绝来源承诺。

## Docs SSOT Plan
strategy=delta_first。唯一长期增量位于 docs/requirements-design-test-contributions/578-cross-owner-validation-facts/，由原 RDT writer 在实施中写 requirement/design/test/traceability/manifest；最终 Phase2 前完成 reconciliation。Requirement 只引用 AC1..6；Design 承接 D578-01..04；Test 单写实际证据与未验证边界。首次独立 committed Review 后原 RDT/Architecture owners 串行 promotion，后继差额重新门禁。
回滚为撤回本次 canonical/doc 变更并完整 reapply；无数据、容器或 CI/CD 迁移。

