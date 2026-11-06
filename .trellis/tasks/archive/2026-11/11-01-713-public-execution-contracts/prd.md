# 统一 Guru 公开执行合同与定向交付验收：整体需求

## 1. 来源与术语

Direct Source 为 [Issue #713](https://github.com/castbox/guru-trellis/issues/713)。S1–S3、S4 的生产/eval 职责边界、S5 及修订后的 AC 是当前交付要求；原首次完整链与扩展 native 计划作为取消验收和历史证据保留。固定 B 为 `8378b8d500a974ae1c01bd0571f30149f56541b0`，包含 #710 的实际前置交付。
公开资料包括 workflow、Skill/引用正文、Interface、commands/help、profile schema、正常 authoring 示例、错误恢复及 producer→consumer 投影。结构、命令、安装、局部 native 和完整行为证据分别报告；取消验收或未验证不等于通过。
[原 Check checkpoint](../../.runtime/guru-team/owner-checkpoints/11-01-713-public-execution-contracts/phase2-check.json) 与原命令/run 是已有结果来源，不用历史结果替代当前范围的完整判断。

## 2. 背景与问题

本项修复 R1 输入域、R2 当前/旧导航、R3 原 candidate/阶段执行入口、R4 错误与结果消费，以及 R5 经逐项对照确认的生产/eval 职责差额。代码、合同、consumer 和安装已有真实定向结果；模型首次装配、方法加载和历史 fixture 接续仍存在反复未通过边界。
当前交付采用可核验的定向结果并保留这些边界，不继续为扩展 native 验收准备环境、恢复旧状态或循环重跑。不据单次 caller 偏差新增产品机制；真实正确性缺陷继续归原 owner 修复。

## 3. 目标与非目标

交付当前公开合同、原生产确定性能力、错误/恢复/结果承接、eval 职责收敛和匹配分发。Task 713-public-execution-contracts/g0 与 D1 a163bca1-b051-4f04-b5aa-2727a4e7abb2 保持不变，不新增切片。
固定声明仍为 43 active packages、127 commands、180 structured profiles，F1–F13 用于导航和证据对应，不撤销公开支持域。
取消的新 native、旧 fixture 接续及重复安装见第5节；它们不构成必需后续工作。#711 布局迁移、#712 新 legacy 家族、#363 遥测、业务 #994 代码/状态/生产、Trellis 上游/global/node_modules、攻击/伪造、压力/锁/TOCTOU/crash 加固、完整发布矩阵、部署和外部采用仍非目标。

## 4. 真实调用方、场景与流程

| 场景 | 前置、动作与观察 |
| --- | --- |
| SC1 原公开步骤承接 | 正式安装和真实原 owner 前置下，核公开输入、原命令、producer 输出及 consumer；采用已发生的定向结果，不要求新的 preTask→Finish native 链 |
| SC2 普通错误 | 使用已有 relation/disposition、authoring/result、receipt 等实际错误及公开纠正结果，保留原失败 |
| SC3 变化与恢复 | 采用已有真实 candidate/stale/同结果恢复证据，检查 key/B/适用结果不被覆盖；取消追加完整 native 恢复链 |
| SC4 固定调用族 | 核 F1–F13、mode/profile、当前/旧合同及 consumer，逐项标记现有证据和未验证行为，不追加非等价 native 场景 |
| SC5 执行器真实故障 | 保留 exit/stdout/stderr 和确认范围，已知正确性缺陷交原维护 owner，不将 caller 错误改判产品缺陷 |
| SC6 分发与兼容 | 复用仍匹配的 source/dogfood/平台/代表安装、mode/sidecar/reapply/drift 及旧 consumer 事实，仅刷新真实变更依赖 |

## 5. 行为要求

S1：原 schema/正文承接现有成功域，Issue/no_issue 正向输入明确；当前/旧、多 profile 导航一致，AI 作者、公共 producer 身份和 recorder 字段分清，真实兼容域保持。
S2：AI 选择 scope/B/路径/阶段，原 executor 计算 candidate/身份并执行阶段操作；公开 CLI/dispatcher 与原 owner 优先，不新增第二算法、workflow、wrapper Skill 或状态台账。
S3：机器可判定错误给字段/约束/合同和原恢复入口；stale 与内部故障保留语义。完整捕获 exit/stdout/stderr，区分 receipt.result、checker 和正式 typed exit，不用截断显示重建结果。
S4：逐项对照 R5 三辅助，必需生产知识和事实由原 owner 提供，eval 复用；保留合法 fixture/环境/观测。当前验证采用源实现、公开原命令、定向测试、consumer 与匹配安装结果；真实 Agent 必读与语义职责不变。
S5：canonical、dogfood、声明平台和代表安装成套匹配，沿原 owner 保留 mode、sidecar、Task/session、旧成功域与恢复；不因本项重复安装或扩大发布矩阵。

| 取消项 | 范围 | 结果口径 |
| --- | --- | --- |
| C1 / AC5 | 新的 preTask→Finish 首次正确完整 native 链 | 取消本批验收；已有首装配失败与后续生命周期事实保留，不记全链通过。 |
| C2 / AC6 | 新的独立 N3 public-only 变化/结果恢复链及旧 fixture 接续 | 取消追加 native 和历史状态恢复；已有普通错误、stale、同结果恢复按实际层级采用。 |
| C3 / AC7 | F10、其余非等价 family/profile/caller/goal 的追加 native 代表 | 取消追加模型验收；保留 43/127/180 声明、导航与 consumer 映射和已有定向结果，未验证行为明确列出。 |
| C4 / AC8 | R5 完整方法加载、Planning→同 fixture Activation/resume、Drift 的模型方法补证 | 取消补证及重跑；保留职责对照、生产入口、alias/consumer 模块结果，以及 execution_error、fitness_regression 和方法证据不足。 |
| C5 / AC9 | 为补上述 native 而重复准备环境、恢复损坏 clean 或再次安装 | 取消重复准备与安装；复用完整且仍匹配的安装/投影、reapply/drift/sidecar/mode 实绩。 |

取消项的原失败、部分成功、污染、未知退出码和当前 H2 终态保持；不清理、回滚、续跑或改写为通过。不为取消项新建 Issue、交付支线、native 或环境。

## 6. 约束与依赖

AI/脚本边界、公共 API/typed exit、兼容迁移、最小状态、无授权持久化规则保持。当前模型、主 worktree、Task/Delivery、固定 B 与 main 目标不变。
相同且未受影响的命令和 gate 只作适用性采用；已知正确性缺陷必须修复，范围改变后的完整语义门禁仍须执行。范围以当前 Direct Source 与公共 accepted_scope 承载，不以文件存在替代范围接受。
主 Task 的候选 Check→原知识 final integration/readback→最终 Check→TaskCommit→完整 committed Review→Delivery Review/readiness→发布/交付→Completion/Closure/Finish 保持；实际 merge 前保留 fresh merge gate。没有自动关闭 Issue 或绕过 Git/GitHub 副作用边界。

## 7. 可观察验收与验证方式

| AC | 要求 | 保留的可观察验收 |
| --- | --- | --- |
| AC1 | S1/S3 | 原 creation Issue/no_issue 正向调用与已观察字段错误的定向证据；公开 schema、例子及诊断与实际入口一致。 |
| AC2 | S1 | 固定 B 和本项差额的 43 active packages、127 commands、180 structured profiles 完成导航、输入/输出及 consumer 核对；保留真实兼容域。 |
| AC3 | S2 | 原 construct/candidate、阶段与恢复入口的定向执行和真实 consumer 结果；公共 token 原样承接，不复制私有算法。 |
| AC4 | S3 | 原命令 exit/stdout/stderr、receipt.result、checker receipt、typed exit 的定向检查和真实错误事实；不吞掉 stale 或已确认故障。 |
| AC5（取消） | S4 | 取消新的首次正确完整 native 链验收；原失败、纠正后结果与未验证范围保留，不作为通过项。 |
| AC6（缩减） | S3/S4 | 复用普通错误、真实 stale、结果丢失/恢复的现有定向或局部命令证据；取消新的独立 native 恢复链及旧 fixture 状态接续。 |
| AC7（缩减） | S1/S4 | 保留 F1–F13 的声明语义和证据层级对应；采用现有结构、命令、安装、synthetic 与局部 native 结果，不再要求追加非等价 native 代表。 |
| AC8（缩减） | S4 | 保留 R5 三辅助职责对照、生产能力归原 owner、合法 fixture 与原入口模块回归；取消 R5 模型方法加载及特殊接续的新增行为补证。 |
| AC9 | S5 | 采用当前匹配 canonical/dogfood/平台/代表安装及兼容恢复的现有实绩；只刷新实际变更依赖，不重复安装或完整矩阵。 |

当前保留验收为 AC1–AC4、缩减后的 AC6–AC8 与 AC9；AC5 是取消项。全量声明及 source/组件/consumer/安装证据由原 Check 按当前适用性采用，取消或缺失的 native 不能填入 passed。

## 8. 实际未决项

没有未决产品范围选择。原 full gates、知识最终整合和交付仍须按当前范围实际完成。
原 N1 首装配失败、N3 public-only 不充分、F10/H2 非通过、R5 方法不足/resume execution_error/Drift fitness_regression，以及旧 clean 的后续损坏均保留为取消/未验证边界。完整模型生命周期、全部声明模式实际模型行为和 R5 方法不作已验证声明。
