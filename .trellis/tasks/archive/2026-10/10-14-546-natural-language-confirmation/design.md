# #546 交互合同设计

## D546-01 公共交互语义

唯一正文位置为 `trellis/presets/guru-team/spec/workflow/workflow-contract.md#interaction-budget`，安装后的 locator 为 `.trellis/spec/workflow/workflow-contract.md#interaction-budget`。保留现有 Interaction Budget 的询问条件与副作用集合，补充：

- 确认、真实选择和必要澄清默认普通聊天；提问工具可用不等于必须使用。遵守已表达的 prompt 偏好。
- 唯一当前已展示动作接受明确自然语言肯定；精确动作已经请求或确认时沿原 owner 承接，不切换渠道重复确认，不要求身份复述或固定句式。
- 结构化提问仅在用户主动要求或平台上位约束强制要求时使用，并满足工具自身允许用途。默认预选、未回答与等待时间不是授权。
- 文字及按钮答案先对应原问题和原计划；迟到或重复答案不重放已经承接的动作，不把旧答案绑定到新问题。判断在当前对话中完成，不增加持久状态。优先只留下一个待回答入口。
- Agent 主动提问与平台命令权限、沙箱或外部审批区分；真正强制审批说明其来源和动作，不承诺绕过。

该正文只定义渠道和答案承接，不修改准备、提交、发布、合并等独立授权边界；既有 mapped transition、re-entry 与后置校验照原合同自动继续。

## D546-02 引用与平台分发

`trellis/workflows/guru-team/workflow.md` 的全局合同与 Interaction and side effects 指向该唯一正文；不复制新规则到 phase/breadcrumb，不增加路由。

审查 `trellis/skills/guru-team/packages/*` 的现有确认入口：创建、Clarify、Planning、Commit、Publish、Merge、Closure、Finish、Cleanup 等需要交互的 owner 在其现有入口加载公共 Interaction Budget，仍独占动作计划、确认必要性和执行回程。仅补薄引用，不改 public I/O、registry、schema、runtime 或 typed exits。

`trellis/presets/guru-team/overlays/**/guru-finish-work*` 是现有平台入口源；声明平台采用同一薄加载指令，覆盖 Codex、Claude、Cursor 及同源派生入口。JSON/TOML 平台保持有效格式。通过现有 package projection 分发公共 Skill，不另造平台专属交互正文或 wrapper。preset/workflow README 只给出公共 locator 与静态/实际验证边界。

## D546-03 安装边界

本任务通过完整 installed legacy Task graph 执行，canonical 已是 #531 Task/Delivery 候选。公开 apply 要求匹配的完整安装；本任务不调用 apply 更新旧 dogfood，不手改 manifest，不修改 `.trellis/workflow.md`、installed package 或平台运行副本。

依照 Direct Source 补充评论，当前交付仅 canonical 合同及平台投影源；旧 dogfood 同步由原安装/迁移 owner 在合格完整迁移后进行。旧版本漂移单列为既有边界，不用局部 backport 或新 updater 消除它。source 验证不等于 installed、native、upgrade 或 Release 证明。

## D546-04 来源设计处置矩阵

| 来源/原承诺 | 处置与落点 | 理由、影响及上游承接 |
| --- | --- | --- |
| #546 目标1/验收1-2：自然语言确认 | retain → D546-01公共正文、D546-02原owner薄引用 | 渠道中立承接；原授权边界不变 |
| #546 目标2/验收4：选择澄清及渠道偏好 | retain → D546-01 | 工具可用性不能替代意图；不改客户端 |
| #546 目标3/验收3：迟到重复答案 | retain → D546-01 | 当前对话对应原问题，无授权存储或重复执行 |
| #546 目标4/验收5：mapped接续 | retain → D546-01/02 | 不调整拆分合并、executor或validator |
| #546 目标5/验收6：强制平台审批 | retain → D546-01 | 说明真实来源，遵守上位约束 |
| #546 目标6及平台验收：SSOT/平台一致 | retain → D546-02 | 原公共Markdown和已有平台源承接，无新API |
| #546 正文dogfood同步和installed/reapply/drift要求 | change → D546-03 | 同Issue评论6159835923明确延后；旧完整安装迁移仍由原owner承担，不宣称同步通过 |
| canonical workflow Candidate migration boundary；preset README MIGRATION-531 | retain → D546-03 | 不把canonical改动当作开发任务runtime迁移 |
| Trellis官方 custom-workflow/custom-spec-template-marketplace | retain → D546-01/02 | 使用workflow/skill/overlay/spec官方扩展面，不改hook、上游或全局包 |

Issue未引入额外规范性方案；以上既有公共合同是保留约束。当前独立 candidate_assessment 返回 `no_architecture_impact`，没有新增 Architecture decision、GAP、contribution 或 ADR；final_plan 仍需独立审核。

## D546-05 Docs 与验证承接

RDT采用 `ssot_first`：由原 `guru-maintain-requirements-design-test-ssot:task_impact_sync` 评估增量，默认写 `docs/requirements-design-test-contributions/546-natural-language-confirmation/` 的最小requirements/design/test/traceability和manifest；唯一Test持有实际结果与未验证边界，不复制公共Interaction Budget正文。共享current晋升只经原RDT owner。

R546-01..06 → D546-01..05 → S546-01..06；具体验证计划由 implement.md 拥有。人工语义检查证明合同完整性，现有source/package/projection检查证明结构及分发源，不将文字断言当实际Agent行为测试。
