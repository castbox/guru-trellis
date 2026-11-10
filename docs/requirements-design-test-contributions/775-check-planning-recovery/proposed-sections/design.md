## D713：原owner公开执行承接

**D713-01 / CON713-CONTRACT** 承接R713-01：每个原Skill拥有适用profile的执行正文；Interface、commands/help、schema和正常示例指向同一输入域和authoring/结果边界。creation复用shared task-creation source/target定义，保留原执行器和public局部约束。命令dispatcher仅展示声明合同与载体，不按语义猜profile；当前入口不能误选历史示例。

**D713-02 / CON713-CANDIDATE** 承接R713-02：原delivery_projection只读CLI经安装的construct-delivery-candidate.sh返回既有完整Git Candidate。输入来自真实Task/Delivery与AI选择的B/HEAD/paths，复用原content_base/candidate；同Delivery candidate的B优先，再用实际前序delivered或显式development baseline/唯一merge-base。新桥接仅Git checkout/C4/当前pull_request，原上游git_free入口保持原consumer边界。原Delivery begin-check/rework继续消费完整operation，保持owner/phase/freshness；构造器不写阶段或作语义判断。

**D713-03 / CON713-DIAGNOSTIC** 承接R713-03：原schema/error owner输出具体字段与合同，不回显敏感原值；普通修正或stale指原profile/producer，内部故障保持非零和已确认范围。调用者完整捕获原exit及双输出后才解析中间result、真实artifact/checker receipt和正式typed exit，不能使用外层成功或截断显示构造缺失字段。原恢复或re-entry保留身份/B与适用结果，不创建第二consumer/状态。

原 C4 discovery 公开 Closure 必需的真实 binding 引用，resolver 保持唯一事实 authority。原 Check 按 AI 已作出的路线判断交接：reapprove_plan 的范围内规划修复向既有 Author 传递具体 revision_actions，包含已记录 current_scope 的情形；真实范围变化以 proposal_refs 交原 Clarify。原 scope_decisions 保留，不将其非空与否作为新需求选择或省略动作的依据。Check 在执行其阶段 operation 前验证完整公开输出，普通装配错误不先改变阶段。legacy finalize 在重执行命令前校验其既有 REVIEW 必需字段，保留原观察比较和额外 caller 字段。精确字段、载体、Planning freshness 配方和 profile 仍由各原 package 单写；匹配采用及原结果恢复见 [MIGRATION-713](../../../trellis/presets/guru-team/MIGRATION-713.md)。

首次 planning_stale 的原 recorder 在既有私有 6.0 结果中派生最小 rollback_binding，保存回退后不可重新推导且同 owner 恢复必需的原 key、scope/plan、Planning result、候选及三份规划 evidence。原正常语义 authoring 保持 11 字段。原 Check 的声明恢复 profile 使用独立的已回退前置，核原绑定与当前同对象、内容、scope/plan及规划 evidence，不能走依赖已清 Planning 的普通入口或 checker。恢复及合法纠正只返回原规划交接，不再 rework、record_gate 或覆盖 candidate；原结果字节保留。

旧无绑定结果由同 owner 从实际保留的原 public query，或精确原 Git Task 对象经原公共 parser，取得原 Planning、candidate、scope/plan 及 evidence；不得从当前状态补成旧绑定。缺原因果来源明确阻塞，并给原 Planning/Clarify 重新判断入口。matching package、workflow/router 与受控 consumer 直接成套演进，退出旧非空 refs→Author 路径；不增加历史 parser、第二 checkpoint 或长期双写。精确字段和操作由原 Check 合同及 [MIGRATION-775](../../../trellis/presets/guru-team/MIGRATION-775.md) 单写。

旧现场采用先从目标checkout之外的完整matching provider，通过其公开Check wrapper的既有--root参数对未变目标恢复。provider提供当前执行合同和runtime，目标已安装且兼容的Task2/Delivery API1提供唯一身份和状态authority；缺API或身份/选择前置时按原诊断停止，不调用provider私有Task实现替代。原consumer承接公开输出后，在不再复用旧结果时由原tools owner合法采用新工具，后续绑定真实after候选。先升级tracked目标工具导致原内容变化的现场回原owner，不能豁免旧token。

**D713-04 / CON713-EVAL** 承接 R713-04/05：测试辅助与生产能力逐职责对照。当前 profile 导航归原生产合同，完整 Candidate 归原公开构造，私有 recorder 身份不由 eval 补给模型。既有 isolated owner tests 保留合法历史 fixture/透明运输及其证明边界；它们不证明 N1 首次正确或完整模型生命周期。当前 owner 核对已有 source、组件、原命令、consumer、安装、synthetic 与局部 native 结果的实际适用性；缺失或变化只补命中检查。真实 Agent 的当前语义前提仍由实际原 owner 完成，host 仅承担合法环境、provider/transport 与观测。取消 #713 追加 N1/N3 原生链、非等价 native 代表、旧 fixture 接续及 R5 模型方法补证；保留首次失败、部分成功、污染、未知退出码和方法证据不足，不将取消项改记为 passed。

**D713-05 / CON713-ADOPTION** 承接 R713-05：原 tools owner 维护已有 Task/session 的本仓 dogfood，原 installer 维护 matching 安装、reapply、冲突与 mode。固定 B 的 43/127/180 声明清单、当前候选差额和 F1–F13 证据对应留在原规划/验证位置，不生成公共 DTO 或独立长期 manifest。采用完整且仍匹配的既有安装/投影、reapply/drift/sidecar/mode 实绩，仅刷新实际变更依赖；不为取消项再次安装、恢复损坏 clean 或准备环境。旧成功 consumer 保留既有合同；成功语义变化先显式迁移，无 consumer 的 deprecated 资产经原 owner 核实后退出。RDT/Architecture 完整隔离拟写先经候选 Check，再各原 owner final_integration/readback；实际 after 重绑后执行最终 Check、TaskCommit、完整 committed Review、Delivery Review/readiness、发布/交付及 Completion/Closure/Finish。合并前保留 fresh merge gate；本项取消验收不新增必需后续切片或 native 支线。

这些职责沿既有D531/ADR-028及#710 recorder决定，不修改官方Trellis、全局包或node_modules实现。精确argv/profile/schema仍由canonical原package/step单写；此单元不复制私有算法或测试expected输出。
