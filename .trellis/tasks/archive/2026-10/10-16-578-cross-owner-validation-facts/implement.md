# #578 实施计划

## Delivery Policy
policy=full。task_scope=AC1..AC6；delivery_slice=AC1..AC6；remaining_work=[]。
本次交付的独立可用条件：三个原 owner 和直接派发合同统一、定向真实行为与当前绑定验证通过、架构/RDT 已审晋升、完整安装说明可供采用。最终 Completion 覆盖全部 AC，不等待 #421/#607 消费结果。
validation_boundaries：小型正常 fixture、受影响 package/runtime、匹配 installed 公开链路与声明平台/reapply/drift；完整多平台 Release/Upgrade matrix、业务仓全量构建/部署/生产不在任务内。无后端 API，新接口分阶段要求不适用。

## 执行顺序和写集
1. 完成 Wording、final_plan Architecture、Planning Approval，由原 Activate owner 进入实施。
2. implement worker 读取 PRD/design/spec/当前文件，仅修改三个 canonical Skill 的 SKILL.md/references/contract.md、直接派发的现有 workflow 文案、现有 quality-guidelines 执行事实段落、必要 stale 提示。不得改变 phase、owner、typed route、schema/公共DTO或 CI/CD。必要提示改动先证明由原 freshness 错配正常触发；保持检查条件。
3. 基于现有 local-revision-facts fixture 和 eval carrier补足跨 reviewer/阶段事实采用场景；不写自动 semantic classifier、不预填 owner pass、不新增测试平台。只有真实缺口才扩展 fixture 的正常动作。
4. main/RDT writer 写唯一 docs/requirements-design-test-contributions/578-cross-owner-validation-facts/ 增量；写 MIGRATION-578 与现有 README 导航；维护 task-owned Architecture contribution/ADR。
5. 完整匹配 source dogfood 运行现有 apply/reapply/drift、安装/平台/sidecar/mode定向验证；开发Task不热更新。变更 overlays 时从该匹配 source dogfood 自身运行 apply.sh --repo .；逐项处理安装器本次 .new/.bak，不清理无关资源。
6. fresh 独立 Architecture 后完整 Phase2；精确 staging/TaskCommit；fresh 独立完整 committed BranchReview。其后原 owners 执行架构/RDT promotion，新差额再次 Phase2/Commit/独立完整Review。
7. 原 Delivery Review/Publish/Merge 交付 main；原 Completion 判断全scope；Closure 处理 #578；Finish 的独立 bookkeeping PR归档并验证 main，最后原 Cleanup 只清本任务资源。

## 最小验证集合
| 场景 | 观察 |
| --- | --- |
| 原执行者产生 A/B 真实结果，文档只对齐已有行为，换 fresh reviewer/阶段 | owner 完整当前判断；A/B 命令计数不增加；summary 真实注明采用与来源 |
| 文档改变 B 行为合同/测试期望、共享依赖改变、新增C | 执行 B/实际消费者或C；不能用相同代码 tree 跳过 |
| 定义/版本、工具链、参数或环境改变；原始B结果缺失 | 执行受影响项，A依赖不变且事实可用时保持A计数 |
| commit/promotion身份变化且工程依赖仍适用 | 当前结果重新绑定；旧 token 不充当当前结果；不因身份单独全量 |
| 原始事实仍可查但旧owner私有checkpoint已退休 | 只用合法原始结果；不打开/重建退休checkpoint |
| package/runtime/installed/projection | 原current identity、typed routes不退化；source/installed公开调用、声明平台一致、reapply/drift及sidecar/mode通过 |

真实行为由 native/current AI读取合同、候选和事实后选择命令并形成当前结果，独立观察实际调用；文本匹配或DTO绿色单独不充当行为证明。已经执行的原始结果保持原对象，不改写成新候选记录。
唯一 Test 文档单写命令、层次、首次失败/修复与未验证边界；本文件不重复执行日志。

