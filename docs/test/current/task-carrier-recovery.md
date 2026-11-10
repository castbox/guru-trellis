# Task 载体恢复的验证策略与观察边界

知识单元：`RDT-TST-TASK-CARRIER-RECOVERY`；别名：T773 / V773。
状态：current；authority：`guru-trellis-rdt`；原 owner：
`guru-maintain-requirements-design-test-ssot`。来源为 [R773](../../requirements/current/task-carrier-recovery.md)
和 [D773](../../design/current/task-carrier-recovery.md)。固定适用 before 为 Git
`313d80215f65777fc70893a90c6d8dce8005d6dd` 的
[`RDT-TST-LIFECYCLE`](task-delivery-lifecycle.md)。本文件定义本能力验证策略，
其 current 状态仅在原 RDT final_integration 实际晋升后生效；隔离 proposed 文件不改变共享 authority。实际观察见下文。

## 行为、入口与独立观察

| Test → requirement / design | 条件、动作与观察 | 层次及限制 |
| --- | --- | --- |
| T773-01 / V1 → R773-01 / D773-01 | 正常缺失的规范 TaskRef 分别进入公开 discover-candidates.sh、record-plan.sh；两者拒绝、退出3，既有诊断含 task_not_found、实际 TaskRef 和原恢复处理，不能返回成功空候选。复用原成功/只读回归。 | package 公共 wrapper 及共用解析边界。断言源于要求，不用错误包装自身计算预期，不另建完整诊断链。 |
| T773-02 / V2 → R773-02/03 / D773-02/03 | 一条去敏 Git carrier 含合法原 schema2 Task/Delivery、完整计划及真实缺失 gates；目标 HEAD 无该 Task。Git 恢复未提交 workspace 后实际 invoke 新 profile，再由原 Bind 观察同身份结果。比较 Task/Delivery/规划及 Publication/Delivery/full_review/readiness 缺口保留。 | 新 association producer 必须真实执行，fixture 只能建立其边界前的合法历史。下游未变外部依赖可隔离，但必须报告实际组件层，不声称 native Agent、真实聊天或业务全链。 |
| T773-03 / V3 → R773-03 / D773-03 | 匹配 C4/C5 复用不写；缺一项只补该项；正常 branch/HEAD/身份/控制失配拒绝。以实际 primary/linked 拓扑观察 not_applicable/caller_owned，既有 ownership 保持。 | 原 Branch/shared substrate 定向回归；只增加能检测不同必要行为的用例，不枚举伪造/攻击、锁、压力或 crash。 |
| T773-04 / V4 → R773-02/03 / D773-02/03 | AI 将完整指引与公开 schema/commands、Git/task.py/Identity/Ensure/Bind/current/continuation 对照；核参数可用阶段、原 writer、顺序、写集、stop、HEAD/workspace 差异及历史保留。 | 语义与调用核对。链接存在、文本扫描或 schema 通过不能证明 Agent 已完成恢复。#773 正文的 #223 结果是历史事实，不重操作该业务仓库。 |
| T773-05 / V5 → R773-04 / D773-04 | 原 tools owner 同步 matching source/installed/受管声明投影，运行受影响 package/runtime 和 distribution/drift/sidecar/mode 检查，读回同 Task/session/key/phase。 | 只采用仍适用工程事实并补变化命中项。source、installed、native、远端和生产分别报告；不扩大为多平台安装/Upgrade/Release 矩阵。 |

## 执行方法与充分性

遵循安装的 Test And Validation Value 和 Validation Scope Ownership。V1 是长期
缺陷回归；新关联的 V2/V3 是长期行为回归。指引核对、当前投影/sidecar 检查形成
本次证据。先完成清晰且廉价的诊断观察，再验证新准入和代表恢复，最后跑受影响
旧覆盖与投影。必要观察充分后停止追加实验；新失败或明确因果疑问才增加检查。

测试必须到达所声明边界，不能用预写 C4/C5、fixture 自动修复 Task、手填 Bind
成功或复制实现计算预期来证明新 producer。基础设施/装配失败不算产品缺陷；
反复失败时重评方法或保留证据缺口，不更改行为断言制造通过。原 #223 事实支持
历史背景，不能替代当前新增动作的代表验证。

## 当前观察截止点

观察截止于本 D1 完成定向 source 验证和原 tools 同步之后、正式 candidate Check
之前。以下为实际执行或明确采用的工程事实；不声明最终 Check、Review、PR、
业务恢复、生产或 Release 通过。

| 观察 | 实际结果与证据边界 |
| --- | --- |
| V1 原失败与修复 | 实施 Agent 在临时真实 Git 仓库，以正常缺失的 `.trellis/tasks/missing-demo` 分别调用原 discover-candidates.sh 和 record-plan.sh。旧代码均为 internal_error、field_path=runtime、exit2。修复后的长期用例实际走两个 wrapper，要求 exit3、stale_identity、实际 TaskRef、task_not_found 和原恢复指引，并保持无成功候选及无 C4/C5 写入。 |
| V1–V3 package | 下列 Branch 命令实际 9 tests、exit0；shared 命令实际 43 tests、exit0。代表恢复的首次新 Branch 与 Bind 调用是真实公开 wrapper，依赖真实 installed native API，Git 恢复原 fixture Task/Delivery 及三份规划文件的完整字节。当前为 no_current_delivery，同身份、原 Delivery、未变 HEAD 与历史 null gates 保持。不是 native Agent 语义审核全链，也不是原业务聊天重放。 |
| 代表用例修订 | 首次测试曾错误假设普通 discovery 全局无候选；原 carrier 本地分支仍是合法候选。改为独立检查选定 main 候选的 task_artifact_mismatch 后通过，没有为此修改生产行为。一次并行 managed Python 启动报 runtime_dependency_missing/exit2，串行重试后通过；这次设施失败不算产品诊断缺陷。 |
| V4 指引核对 | 原文档 writer 核 canonical 相对链接及 Bash 代码块语法，原实施/Check coordinator 亲自对照完整指引、当前公开输入和实际 consumer 顺序。固定 carrier、身份/完整规划/历史核对、Git/set-base、Branch、Ensure、接收聊天 Bind/current/continuation、匹配复用和冲突停止均有原 owner；没有私有调用、隐含 commit 或历史 gate 补造。 |
| V5 source | source package 合同 validator exit0/status=passed；其 package_test_count=159 是测试文件发现计数，未执行159项测试。原 coordinator 实际完成390个Python文件内存compile、marketplace JSON、Bash语法、Delivery context及diff检查。context的长文件注入和代码引用告警已观察；Agent另行读取完整必要正文，未以截断注入代替加载。 |
| V5 tools/installed | 原 guru-upgrade-tools 以同一冻结操作实际返回 tools_upgraded/exit0，版本0.7.0-guru.8；完整重装9183个受管文件，最终42个内容投影字节/模式匹配，原writer更新manifest，受管sidecar=0，drift exit0。配置、Task/session、peer/common指针按原保留检查保持；当前运行指针为checkout-local schema3 selection-v3.json，legacy active.json保持缺失。 |
| V5 root native | 本聊天实际 task.py current --json 为 stale=false、同 Task/generation/Delivery、implementing及原planning接受结果；get_context.py --mode continuation exit0。两个已安装missing诊断入口各exit3、定位原TaskRef及恢复指引，stderr空。installed discover-skill-contract实际提供aggregate2.0及两个profile。这些读取验证目标可用性，不增加新关联或补 gate。 |

上述成功 source 测试命令在仓库根执行，使用匹配 managed Python 和当前已审核
`.trellis/scripts`；后继 owner 根据真实 source/依赖/环境判断采用，不从计数推定充分性。

```bash
GURU_UPSTREAM_DELIVERY_SCRIPTS="$PWD/.trellis/scripts" bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/packages/guru-establish-task-branch-binding/tests -p test_contract.py
GURU_UPSTREAM_DELIVERY_SCRIPTS="$PWD/.trellis/scripts" bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/runtime/task_lifecycle/tests -p test_branch_substrate.py
bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

本次 tools 采用 dirty Guru development source 的 local_candidate 模式。正式
formal_fork_source_lock 仍未验证；精确 Fork CLI/Core 构建匹配不消除该 Guru 来源
边界。完整多平台安装/Upgrade/Release 矩阵、native Agent 全链、真实 GitHub/backend
恢复和生产效果均未执行，不属于本项验收。#773 正文中的 #223 结果仅作适用历史
事实；未重新操作该业务仓库。独立 Architecture、candidate Check、原 owners 最终
整合/readback、after重绑和最终质量结果仍由各原 owner 分别形成。

## 关系

原阶段和证据消费仍读 [Task/Delivery lifecycle 测试](task-delivery-lifecycle.md)。
本叶只拥有 Task carrier recovery 的策略与实际观察边界；整体 Completion、
Closure、Finish、Release 和原业务恢复由各自原 owner 判断。
