## T713：公开执行合同与定向交付验收

| Test → requirement/design | 正常输入与原入口 | 必须观察及限制 |
| --- | --- | --- |
| T713-01 → R713-01/D713-01 | 原 creation 合法 Issue/no_issue 及已观察 relation 误填；当前多 profile/真实旧 consumer | 原正向执行及字段错误的定向证据，具体 field/contract/恢复，导航与 authoring 边界一致；仅 schema 拒绝不证明模型首次能力 |
| T713-02 → R713-02/D713-02 | 原 construct 完整 Candidate→公开 begin-check/rework；同 D1 恢复、实际 delivered 及真实编辑的已有证据 | Git/C4/current 前置、完整 B..H/dirty、固定 B 和合法 stale；git_free 保持上游原 consumer 边界；不追加完整 native 恢复链 |
| T713-03 → R713-03/D713-03 | 原命令 exit/stdout/stderr、record/check/invoke、普通错误或实际内部故障；C4 binding 引用→Closure、Check 无 scope 或 current_scope 范围内返工→Author、真实范围变化→Clarify、已回退原结果恢复/纠正、legacy finalize 既有 REVIEW | receipt.result/checker/typed exit 分清；原 consumer 消费最小引用与具体动作，普通形状错误在对应 transition/重执行前诊断，旧合法成功域及恢复保持；不加无范围 fault injection |
| T713-04 / N1 → R713-04/D713-04 | C1 / AC5：新增 preTask→Finish 首次正确完整 native 链验收取消 | 保留原首装配失败与纠正后实际生命周期结果；取消/未验证不得记为全链 passed，不追加新 run 或必需补证支线 |
| T713-05 / N2 → R713-03/04、D713-03/04 | 已有普通字段、authoring/result 或 receipt 误用与公开纠正 | 按实际层级采用原结果，首失败与纠正分开；不计 N1 首次正确，不为本项重新准备独立案例 |
| T713-06 / N3 → R713-02/03/04、D713-02/03/04 | 缩减 AC6：已有真实编辑/stale、合法推进、结果丢失/恢复的定向或局部命令证据 | 原 key/B/适用证据保持；C2 取消新增独立 public-only native 恢复链及旧 fixture 接续，保留 N3 不充分与原 finding/证据不足 |
| T713-07 → R713-01/05、D713-01/04/05 | 缩减 AC7：固定 B 及当前差额的 43 active packages / 127 commands / 180 structured profiles；F1–F13 与 mode/profile/consumer | 完整导航、输入/输出与 consumer 核对；已有结构、命令、安装、synthetic、局部 native 各按其层采用。C3 取消 F10 及其余非等价 family/profile/caller/goal 追加 native 代表，未验证行为明确保留，不扩 #712 |
| T713-08 → R713-04/05、D713-04 | 缩减 AC8：R5 owner_schema/public_reads、native 提示、observe_candidate 的生产职责对照与原入口模块回归 | 生产知识/事实由原公开 owner 提供，eval 不保第二调用实现，合法 fixture/观测保持。C4 取消完整方法加载、Planning→同 fixture Activation/resume 与 Drift 新模型补证，保留方法不足、execution_error 与 fitness_regression |
| T713-09 → R713-05/D713-05 | 当前 canonical/dogfood/平台/代表 matching 安装、reapply/drift/sidecar/mode 与原 consumer 恢复的已有实绩 | 核仍匹配的实际结果，仅刷新真实变更依赖。C5 取消为追加 native 重复环境准备、损坏 clean 恢复与再次安装；source、installed、native/provider 分层，完整 Release 矩阵、部署及业务采用不由此推定 |

T713-03 的 #775 差额复用同组生产 Check fixture：从正常 current_scope + reapprove_plan 语义输入调用实际 recorder/checker/invoke，将实际 planning_stale stdout 按正式薄投影交真实 Author 输入 schema，并断言具体修复动作保持。由原公开流程实际回退、清除 Planning 后，从目标外完整provider wrapper用既有--root调用声明恢复/纠正入口，观察同 key、candidate 与业务内容保持，无第二次 rework、Planning/Check pass 或旧结果字节改写。旧无绑定转换只覆盖新增入口或转换实际改变部分，并消费真实既有原因果来源；真实 scope/plan/内容变化与来源缺失保留原 owner 停点。

两项共享已有前置与证据，受影响无 scope、真实范围变化、成功 Check 以及 canonical/dogfood/consumer/drift 采用命中回归。该验证证明框架公开入口及消费者合同，不要求完整 Author 写作、业务历史重演、完整 Intake/native Agent 全链、多平台或 Release 矩阵。具体执行结果由当前 Task 原质量 owners 实际给出，此处不预填通过。

本节定义 #713 当前保留验收，不预填本轮通过。观察截止于已有原命令/run 的实际记录及本 Task 验证结果，后续正式结果由原 owner 输出承接。原首输入、命令/退出状态/双输出、读取、消费与出口保持在原记录；最终 typed exit 或 no-source-read 断言单独不证明模型行为。源码工程诊断和 #710 旧 native 不计本轮正常入口通过；新修正不改写旧失败。

N1 首装配失败、N3 public-only 不充分、F10/H2 非通过、R5 方法不足/resume execution_error/Drift fitness_regression，以及污染、未知退出码和部分成功均保留原边界。R3 仅 runtime 准备通过，未启动 native；旧 clean 后续损坏不证明 installer 缺陷，也不证明当前可用。取消或缺失的 native 不记为 passed，不再作为本项必须补跑的验收。已知正确性缺陷仍须修复，当前范围仍须完成完整候选 Check、原知识 final integration/readback、after 重绑后的最终 Check、TaskCommit、完整 committed Review、Delivery Review/readiness、发布/交付和 Completion/Closure/Finish，合并前保留 fresh merge gate。受控 GitHub 替身只证明本地层次，不证明真实 GitHub 发布、部署或业务生产效果。
