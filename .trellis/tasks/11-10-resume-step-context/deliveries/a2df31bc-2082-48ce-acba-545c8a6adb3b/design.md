# D1 正常续接与实际出口查询设计

## 1. 设计目标、需求承接与内容基线

本批覆盖整体 PRD R1–R9、AC1–AC7 和 D1 PRD 的全部场景；没有前序 Delivery。development baseline B 改为整合提交 `26630149070e2988ad08102679931468b3535ef8`，来源为 D1 PRD 第1节的冻结基线补充。本轮 Planning H0 同值；原 H0 `43d8f713865a7d621d838cf851bc358c34d29f29` 保留为历史。整合保留 main 更新并继承 journey `f4a3da407bae582088c80213ddbf721e9b38a537` 的完整历史。后续 PR 目标仍为 main，不替代 B。

独立 candidate_assessment 已由原 Architecture 在合法 receiving-session 恢复后返回 `baseline_current`：baseline=`guru-trellis-architecture`，constitution=`guru-trellis-design-constitution-v1`，impact=`architecture_impact`，path=`target_native`。消费本轮 `/tmp/resume-step-context-architecture-candidate-reentry-public.json`，不消费前轮更改 context 环境后产生的结果。该候选结论只允许编写方案，最终设计仍须 Wording、独立 final_plan 和 Approval。

本次仅修订基线与对照条件，第4–7节的两项查询机制和整体行为要求不变，原 candidate 机制事实仍适用。此前针对旧正文的 Wording、final_plan 与 approved 结果不用于当前新输入；本轮不声明它们已经刷新，也不据旧批准激活。

## 2. 当前系统、边界与目标差额

`task.py current --json` 已提供当前身份、workspace 和完整 current_delivery。原 `guru-ensure-task-checkout/runtime/invoke.py` 按显式身份校验 C4 branch binding、C5 ownership、唯一 registered checkout 和 live Task。新增的是同入口的组合查询，不能重建 resolver。上游 current_delivery 包含完整 results/candidate 树，本批只投影直接 consumer 所需字段。

`runtime/discovery.py` 已定位完整 Skill 合同；`runtime/installed.py` 的 `MARKER_PATTERNS/workflow_facts` 已解析 workflow 标记。新增的是原 `discover-skill-contract.sh --exit` 的选定出口查询。上游 `trellis-start` 仍强制 default get_context；本批不修改它，也不承诺消除全部启动读取或历史警告。

## 3. 来源设计处置（唯一）

| 来源与承诺 | 处置与设计落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| 冻结请求「实施约束」：复用公开 current、原身份/ownership 校验 | retain；第4–6节同 Ensure 新 profile | 无第二 resolver；原显式接口兼容，无偏离 |
| 同来源：同 discover 扩展、复用原 marker/parser | retain；第4–5节共享解析和 --exit | workflow/Interface 保持唯一 authority，无偏离 |
| 同来源：动态 profile 由实际 payload 决定 | retain；只返回原 profile_selector | 不增加第二 profile 导航，无偏离 |
| 同来源及整体 R2：输出最小身份/checkout/key/phase/planning | retain；第5节字段白名单 | 不输出完整结果树、candidate 或审计包，无偏离 |
| 同来源及整体 R6–R8：完整加载、canonical、原安装、只读边界 | retain；第6–8节 | 不改 upstream/start/launcher；cache 刷新单列，无偏离 |
| 当前补充：无 context key 与有 context 无绑定不同 | retain；第5–6节独立出口 | 采用公开 resolver/诊断，不能伪装 no_current_task；是现有诊断完整性细化 |
| 整体 R9：保留首次原生结果、成本及不利观察 | retain；第8节 V4 | 不把前置修正算方法收益，不作产品质量推断 |
| D1 PRD 第1节冻结基线补充：继承旅程方法、重取同条件控制组 | retain；第1、8节 | 实施 B 改为 `26630149`；旧原始结果不覆盖、不混作控制组；整体要求不变 |

## 4. 模块、职责与设计取舍

在 canonical `trellis/skills/guru-team/packages/guru-ensure-task-checkout/` 增 `delivery_current_task` profile。复用上游 current 读取和原 Ensure 身份/ownership/checkout 校验。两个 profile 共用的校验若仍内嵌原 invoke，则提取为内部共享函数。原 `delivery_active_task` 输入、输出、错误和 consumer 不变。session context 是否存在沿上游公开 `active_task.resolve_context_key` 及既有 session adapter 判断，不能删改环境变量、借别的 session 或从路径猜身份。

在 `runtime/installed.py` 提取现有 marker 解析结果供 `workflow_facts` 和 `runtime/discovery.py` 共用；保留既有全局校验。后者只扩展 `discover`/CLI 可选 exit，原 shell 入口透传。同步原 package Interface/schema/example、公开 help、workflow exit markers 和原 current checkout router；不新增 Skill、wrapper、路由表或长期缓存。目标动态 profile 不在 discovery 中求值。

## 5. 接口与数据

Ensure 新输入为 `{profile: delivery_current_task, mode: workflow|standalone}`，不接受推测身份。成功 `current_context_ready` 仅含 `task_id/task_ref/lifecycle_generation/checkout_path`；`current_delivery` 存在时仅含 `delivery_key/phase/planning_root`，无 Delivery 时省略。四个 Task 字段沿原 Ensure 校验，Delivery 三字段来自上游公共 current 并核同 Task/generation；关系不一致返回原诊断。

新出口 `no_current_task` 只表示已确定真实 context 且没有绑定；`context_unavailable` 含原 `context_key_unavailable` 原因，表示载体无 key。这两者都交原 `guru-current-task-checkout-router` 报告事实，不能启动 Intake 或写 selection。已知 Task 的 `binding_required/checkout_required/invalid_task_state` 沿原输出和原恢复 owner；上游实际错误保留原 code、field_path 和 remediation，不能按非零退出码一概判无 Task。成功出口也只定位 owner，不代表语义通过。

Discovery 保留无 --exit 的原输出。`--skill <id> --exit <actual_exit>` 校验 Interface 声明与唯一 workflow marker 一致，返回 `skill_id/exit_id/consumer`、选定出口 output contract、consumer input/projection 定位和原入口定位。Skill consumer 返回其公开入口及输入合同；workflow/stop consumer 返回原 workflow target 定位。存在动态 selector 时返回原 `profile_selector`，不返回猜测的 profile。未知 exit、缺失映射、多重映射或 Interface 不一致返回明确非零诊断，不任选候选。字段使用原 Interface locator，不携带完整合同正文。没有持久化数据或数据库迁移。

## 6. 状态、顺序、正常与失败流程

current 查询先确定原 context 是否可用，再读上游 current；无 context 立即报告设施事实。有绑定时核身份及 workspace，然后执行原 Guru 校验，最后投影最小字段。terminal、stale、冲突和读取错误沿原 owner 停止；没有 Delivery 不制造选择。查询全过程不改变 Task/Delivery、session、Git 或业务状态。

出口查询先按原 discovery 验安装/source 合同，再核 exit 声明和唯一 marker，最后定位 consumer 原合同。caller 取得定位后完整读取当前适用条件及必要依赖，才调用原 owner；查询不执行下一业务步骤。原 managed Python launcher 可能刷新 ignored selection cache，该事实单列，不属于 Task/session 变更。

## 7. 恢复、兼容、迁移与集成

原显式 Ensure 和无 --exit discovery 保持兼容；新增调用必须显式选 profile/exit。普通缺失由 Identity、Bind、branch binding 或 checkout 原 owner 恢复，再重查；查询不承担修复。source 与 installed 模式使用同解析逻辑，各自定位本环境真实合同。受管副本由原 `guru-upgrade-tools` 同步并保留 Task/session、并行修改及冲突处理。无新持久状态，故无数据迁移、dual-read 或新恢复事务。

## 8. 验证设计

| ID | 条件、入口与独立观察 | 层级和边界 |
| --- | --- | --- |
| V1 / AC1、2、5 | 真实 Ensure invoke：合法绑定有/无 Delivery、无 key、真实 context 无绑定、正常 stale/ownership/checkout mismatch；断言最小输出及原错误路由，查询前后原状态相同 | package/runtime 长期回归；fixture 可准备前置身份，不能替查询生成校验结果；保留旧显式用例 |
| V2 / AC3–5 | 真实 discovery CLI：Skill/workflow/stop、动态 selector、unknown/multiple/unmapped/不一致局部 fixture；观察唯一原 locator、selector 保留和明确失败 | 长期解析/导航回归；不以字符串自比较代替实际路由；不改生产状态构造错误 |
| V3 / AC6 | 相关 package、contract graph、canonical/dogfood drift 及一次原 owner 代表性安装投影；核新入口可用与旧调用兼容 | 安装/分发证据；不扩成全平台 Release 矩阵 |
| V4 / AC7 | 冻结 bound/unbound 原生 prompt，两组共用 `26630149` 方法及匹配安装；同模型/输入/环境，记录首次结果、重复查询、装配错误、读取量与人工介入 | 临时行为对照；新控制组另存首次结果，实验候选只增加当前查询差额；执行者不读验收 protocol；准备查询与待测查询分计，cache 刷新单列 |

先完成 V1/V2 的实际缺口和相关回归，再 V3/V4；采用仍适用的已有覆盖，不要求惯例回退重跑。无 context 载体只能证明真实 unavailable/explicit 模式；bound 使用受支持显式测试 context 的独立 fixture，标为测试输入。旧 `43d8/unbound` 退出0、214.97秒，仅是原环境历史观察，不作为新控制组，不计算与新候选的节省比例；原文件及不利结果保留。新两组各自原生执行总预算为10分钟；旧运行成本仍计入已发生的总推进成本，不挪入新组或删去。原工具owner已完成本整合基线的安装投影、目标native及installed/drift验证，这只证明实施准备；两项新查询的 V1–V4 仍待执行。必要观察充分后停止；设施反复失败时重评方法并保留缺证，不编通过。

## 9. Canonical 引用、本轮差额与实际未决项

需求 authority：整体/D1 PRD；共享行为定位 `docs/requirements/current/task-delivery-lifecycle.md` 的 current、ownership、Delivery 关系。设计沿 `docs/design/README.md` 发现原查询完整单元，测试沿 `docs/test/README.md` 定位必要断言；本批差额是两查询及原入口读取。Architecture 依据 `docs/architecture/README.md`、`03-domains/ownership.md`、`06-governance/change-contract.md` 及 candidate 的 ARCH-DOM-016/019/024/025/038/043。具体真实 contribution 见同目录 `architecture-contribution.md`；不新增 owner/状态体系，无新原则性 ADR 必要性。贡献由独立 final_plan 审核，shared-current 仅由原 Architecture 在合法 final_integration 晋升。无待用户回答的产品问题；实现和效果尚未验证。
