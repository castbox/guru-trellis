# D1 正常续接与实际出口查询实施与验证计划

## 1. 输入与引用

输入为整体 PRD 的 accepted scope、本批 PRD AC1–4、design 第3节唯一来源设计处置和本轮合法 candidate_assessment。无前序实现。实施前加载 design 第9节命中的完整 authority 和必要关联条件、原两个入口 Interface/schema、`.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value、clear-technical-writing 和当前 package 编码规格。原始请求冻结，技术约束不构成新产品选择。

基线与取证输入另读 D1 PRD 第1节的冻结 `resume-step-context-baseline-adjustment.md`。实施从 `26630149070e2988ad08102679931468b3535ef8` 及其已同步工具起步，PR目标仍为 main。root 的 `43d8` 调查叙述和 accepted_scope 原字节保留。旧 approved 只属于原输入，不用于本轮激活；本次停在修订后的规划，受影响正式门禁待原owner承接。

## 2. 有依赖顺序的步骤与文件责任

1. I1：实施 owner 修改 `trellis/skills/guru-team/packages/guru-ensure-task-checkout/` 的原 runtime、Interface、schema/example/help 与 tests；新增明确 current profile，复用公开 current 和原 Guru 校验，区分无 key/无绑定，白名单投影。保留显式旧 profile。产物须让 V1 经真实入口观察到行为。
2. I2：同 owner 修改 `trellis/skills/guru-team/runtime/installed.py`、`discovery.py` 和原 workflow shell 入口；抽取原 marker 解析，新增 --exit 及 V2 定向用例。保留无 exit 行为及动态 selector。不得新增平行 wrapper 或硬编码路由。
3. I3：在 canonical workflow、原 Ensure Skill/Interface 及 companion-scripts discovery 文档接入新查询；只修改相邻 consumer 必要差额，明确原合同完整加载和上游 start 边界。按 V1/V2 检查出口图与兼容。原 RDT/Architecture owners 准备完整隔离拟写差额，不直接改共享 authority。
4. I4：原 `guru-upgrade-tools` 按 local_candidate 合同同步当前 checkout 的受管工具投影，保留 Task/session 和并行改动，处理原 owner 报出的冲突；执行一次 V3。完成后在原生固定输入下执行 V4，原始首次结果与成本留外部 evidence，不复制协议进产品。
5. I5：原 implementation candidate/begin_check、独立 Architecture/Check 审完整实现及隔离拟写；合法回程后由原 RDT/Architecture final_integration 晋升/readback，再重绑 after 候选并走最终 Check。发布、提交和 Task Completion 各保原 owner，不由本计划或安装检查替代。

## 3. 验证入口、输入与预期观察

V1 使用原 package `tests/test_contract.py` 和真实 invoke，覆盖 design §8 列出的不同状态，额外大 results 树用于验证最小投影不泄出；比较前后 Task/Delivery/session/Git 状态。V2 在既有 `test_skill_packages.py`、`test_delivery_contract_graph.py` 与必要 discovery runtime tests 中执行实际 parser/CLI，局部 fixture 构造普通声明差错。两者均使用仓库 managed Python 解析入口及源 PYTHONPATH，不改全局运行时。

V3 运行 canonical `check-skill-packages.sh`、`check-dogfood-overlay-drift.sh` 与受影响 contract graph；通过原升级入口读回新 profile/--exit，再调用旧显式 profile 和无 exit 查询。仅一次代表性安装投影；完整多平台 clean/update/release 矩阵不属于本批。

V4 执行外部冻结 bound/unbound prompt；执行者只读 prompt 和正常入口，不读验收协议。控制组与实验组共用 `26630149` 旅程方法及 main 更新；重取控制组首次结果另存，实验候选仅增加两项查询。准备 context/fixture 与待测查询分计。无 key 如实报告设施边界；支持显式测试 context 的绑定观测单列，不冒充生产会话。旧 `43d8/unbound` 的214.97秒保留为历史成本，不采用为新控制组，不与新候选计算节省比例，也不因载体前置修正声称减负。每组原生执行总预算为10分钟；历史成本仍列入总推进成本。原生对照、机械正确性、安装投影分别报告。当前已验证的是基线安装准备；新查询用例、查询安装后的可用性和效果仍待验证。

## 4. 停止条件与适用回退点

真实身份/选择冲突交原 owner；不删改 context 环境，不从 inventory 选 Task。来源/范围改变回 Clarify，机制冲突回 Architecture，普通实现失败在当前 owner 修复。必要断言或安装失败时停止相关验收，保留真实诊断。证据已充分且无新变化时停止重复测试。设施反复失败则重评复现层级并报告具体缺证。

只回退本批可证明所属的 path/hunk，保留并行修改与旧 Task。没有业务数据迁移或部署，故无新增数据/发布回滚协议。不得为验证覆盖生产绑定或提交新切片。

## 5. Delivery Policy（唯一）

策略为 full：唯一 D1 覆盖整体 R1–R9/AC1–AC7。独立交付条件是两项查询、旧兼容、原入口完整消费、受管分发和规定验证全部有真实结果。没有延期 D2；剩余实施、V1–V4、正式质量链及整体 Completion 由各原 owner 承担。规划通过或单个 Delivery 交付不证明整体完成。上游 start 读取成本是明确非目标，不是本 Task 待解除的临时限制。

## 6. Docs SSOT Plan（唯一）

策略为 delta_first。原 RDT writer 在实施中维护命中的 requirement/behavior、design、test 完整单元，差额限 design §5–8 的公开查询、失败映射与验证边界；导航只按原发现合同定位，不向根列表重复登记。原 Architecture writer 维护本批真实 contribution，按 ownership/change-contract 保留单 writer、target_native 与原动态路由 authority。当前无需新 ADR、缓存或台账。

直接 consumers 是后续实施、独立 Check/Architecture、最终 Branch Review 与 Completion。共享晋升在候选检查后的原 final_integration/readback，最终 Phase 2 前完成 reconciliation；规划阶段不写共享 README/index/baseline，不把未实施目标标成 CURRENT。历史失败及旧基线证据保持原观察。
