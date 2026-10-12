# #532 验证策略与实际结果

source binding 与晋升状态见 [manifest](manifest.yaml)，需求和设计分别由 [requirement](requirement.md)、[design](design.md)拥有。

| Test identity | 原入口和观察 | 当前结果 |
| --- | --- | --- |
| T532-01 | 原 schema/生产 validator 接受 []；非数组/真实 refs 校验保持 | passed：package 全套 38 tests，最终合同 12 tests、执行消费 8 tests；空数组、非数组与 finding/scope refs 均覆盖。 |
| T532-02 | 完整真实零候选 AI review → 原 recorder/checker/public initial_check | passed：一个实际 Codex installed task 完成九维，[] 正式 passed；Check checkpoint 保留，完成的 Activation checkpoint 退役。 |
| T532-03 | 实际非空候选经适用资格判断全部 rejected | passed：具体上端点 concern 经原 Normal/Solution 拒绝；Root 无 eligible refs 未调用；保留一条分类、无 finding，九维及原公开链返回 passed。 |
| T532-04 | 当前有效 finding 完整资格/refs 后走原修正/回程 | passed：真实上端点 off-by-one 的两项 tests 失败，Normal/Solution qualified_current、Root not_incident_applicable；原公开链返回 implementation_required 和真实 finding。planning_stale 由 package/profile 定向测试证明，非实际规划变更声明。 |
| T532-05 | 正常 missing Architecture 与 recorder 后内容变化不因 [] 通过 | passed：新等价正确 predicate 的两项 tests 通过，当前 Phase2 Architecture 尚未执行；[] 九维后正式 blocked。旧证据保留但不适用新内容；内容漂移由 package 原 recorder/checker 测试证明。 |
| T532-06 | 四 public profiles 与 Check/Task Commit/reconciliation/execution checkpoint 消费 | passed：package/profile/execution tests 与共享 production fixture direct-consumer test；四个 post_owner routing 场景实际出口正确。fixture 只证明确定性消费。 |
| T532-07 | canonical/dogfood/一个 Codex installed 的原真实入口 | passed：Fork 0.7.0-castbox.3 锁定 frozen install/build、marketplace init 与完整候选 preset；installed 校验 36 packages/109 commands、Codex managed 投影、sidecar/conflict 为零；8项关键 source/installed 字节一致。 |
| T532-08 | preset apply/reapply、overlay drift 与 .new/.bak 结果 | passed：dogfood apply/reapply 与 drift rc0/status ok；首次冲突及34份旧 preimage backup 经逐项核对和重应用处理，剩余 .new/.bak 为零；clean installed reapply rc0，无 new copy。 |

实际安装态四轮均由 AI 先完成适用审查，再走原 recorder/checker/public wrapper；无空 qualifier 调用或虚构 no-defect 候选。implementation_required 与 blocked 退役 Check checkpoint，passed 保留供 Task Commit 使用。不得以 DTO fixture 或命令绿灯替代这些语义判断。

额外共享 runtime 全套 64 tests：58 passed、5 discovery errors、1 discovery failure。相同六处 version_state_mismatch 在未修改 main、同一 Python 3.12 下复现，涉及已有接口版本注册，不是本任务回归。定向 direct-consumer test passed；不扩大修复范围。

post_owner passed-initial 的确定性断言正确，但其整体 evaluation_failed 因缺少外部 semantic grader；新增 native semantic-authoring corpus 未执行完整模型 eval。以上实际 AI installed 执行是独立证据，不能冒充全 corpus 评分通过。

首次使用 PATH 的旧 0.6.17 CLI 安装因缺 Guru marker 被拒绝，属于 setup failure；改用准确锁定 Fork 后干净安装成功。只将后者计为一个代表性 clean Codex 安装。

完整多平台升级/Release matrix、#292 原会话实际恢复、#530/#531 验收、正式版本与业务部署保持外部 unverified 边界，不属于本 Issue 的失败。临时 runtime 输出不进入长期文档；这里只保留直接验收所需的实际结果和边界。
