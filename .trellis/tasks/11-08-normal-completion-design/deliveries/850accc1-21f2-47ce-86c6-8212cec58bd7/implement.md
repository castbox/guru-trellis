# 正常完成路径与协调成本：D1 实施与验证计划

## 1. 输入与引用

读取根PRD完整范围、本批PRD、design全篇及第3节唯一来源设计处置；消费实际独立candidate_assessment。原方法由canonical Architecture contract Adopted-mechanism review、Root Cause Protection、Author Requirements and candidate before substantive solution writing承接。Test And Validation Value决定当前验证层级与停止条件。

本批无前序交付；固定B/H0为`80fc24eed3d4deb2dd0fc63126c0affb9789d365`。当前未实现、未验证、未激活，不能从文件存在推断阶段成功。

## 2. 有依赖顺序的步骤与文件责任

1. 原实现owner在Architecture原段整合design§4完整方法，保留已有文档优先、适用性、正常请求、旧决定及typed出口。可审核产物为单一连贯方法，不追加第二检查表。
2. 同owner修Root Cause Protection与Author原引用段，仅明确资格/准入及路径先行；检查Approval、Check、Branch Review、独立Review既有引用，只有证实漏读/冲突才修必要导航。
3. 原RDT owner对R-MECH/D-MECH/T-MECH准备完整隔离拟写与必要追踪，将本批承诺和证据边界接回原单元，保留历史。shared current暂不写；Architecture不制造空贡献。
4. 按§3完成定向语义及机械验证，原公开constructor纳入完整真实内容并begin_check；原候选质量门禁后，由RDT原final_integration实际整合/读回，再由implementation同B重绑全部after，最终质量检查覆盖真实内容。
5. 当前本地边界完成后报告源码和检查状态及未执行的安装/业务效果；后续Git/GitHub交付保留原owner边界，不提前标记Completion。

没有本批新增临时运行限制、数据迁移或前后Delivery接口；无需制造解除清单。

## 3. 验证入口、输入与预期观察

- **V1**：独立语义审核读取实际改后方法，以共享配置写、慢I/O持锁、批次等待和必要原子性/局部容量/缺证/已最小方案作对照；预期拒绝可避免成本且保留真实必要约束。临时案例可沿当前已读样例推导，不建立永久矩阵，不声明生产或统计改善。
- **V2**：`git diff -- <三处canonical路径及本批真实RDT路径>`，逐段审唯一正文和实际消费；限定`rg`定位现有引用后读完整必要上下文。预期无复制准入规则、公共字段或非必要入口改动。
- **V3**：在repo root执行 `python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/tests -p test_contract.py`，并按相同入口分别运行 `guru-qualify-root-cause/tests`、`guru-author-task-plan/tests` 的 `test_contract.py`；执行 `git diff --check`。这些只证明命中合同/格式边界；若现有suite明确带来无关安装/环境或整套CI动作则停在原验证owner收窄实际测试，不间接运行完整流水线。
- **V4**：RDT owner比较拟写与原完整单元，候选Check检查规范承诺/追踪/历史与真实测试报告；最终integration后同B的完整actual-after再检查。

只用必要已有测试，不写锁定新文案的自证测试。不主动CI、镜像、生产压测或安装更新；未执行项明确报告，不记通过。

## 4. 停止条件与适用回退点

实际范围/机制/authority变化回原Clarify/Author/Architecture；候选不成立则修本批机制，保留接受范围。格式、引用或合同测试失败按实际根因修复，设施失败不能冒充产品缺陷。本节所列证据充分后停止追加实验；重复设施失败时换有依据观察方式或如实保留缺口。

本地文档修订可在精确本批范围内恢复，保留并行改动，不reset工作树。本批无部署或生产写，因此无数据/发布回滚协议。shared current只由原知识owner在合法final_integration写，冲突不擅自覆盖。

## 5. Delivery Policy（唯一）

**full**：本批完整覆盖NC-R1—R7和NC-AC1—AC4，不按三个Skill拆Delivery。独立可交付结果为唯一方法、必要消费、RDT一致性及风险匹配检查；本批无延期的规范承诺。

剩余安装采用、backend技术规则/业务投影及原业务修复由各原owner负责，不是本批独立完成的循环前提。本地检查不替代后续formal Check、committed Review或整项Completion；本次不创建commit/push/PR。

## 6. Docs SSOT Plan（唯一）

**strategy：delta_first**。原RDT owner读取 `docs/requirements/current/knowledge-maintenance.md` R-MECH、同名Design D-MECH、同名Test T-MECH的完整单元，在 `docs/requirements-design-test-contributions/normal-completion-design/` 准备完整proposed及本批必要trace/test事实。候选只承接正常最终完成、主动尝试替代、协调默认不准入、Protection与Architecture分工、当前定向验证及证据边界；不复制方法正文或扩大历史native安排。

直接consumer为原Planning/implementation/Check/Review及当前RDT读者。原RDT owner先接受独立Architecture当前结论和完整candidate Check，再在原final_integration重读真实target整合、实际写入及读回；实施owner纳入全部actual-after重绑，最终Phase2前完成reconciliation。Test结果只记录实际观察，未执行的安装采用和业务效果保留未知。

Architecture当前constitution/change-contract委托已有效，独立candidate_assessment为no_architecture_impact，故无Architecture贡献/ADR、共享导航、版本或ownership索引差额。.trellis/spec与安装副本只属原受管投影，本批不手改或更新安装；公开源码与目标采用分别报告。
