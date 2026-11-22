# D1 设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 Delivery PRD 的 D1-S1–S5 和整体 AC01–AC03。开发基线 B 和规划起点 H0 均为从 origin/main 取得的 `61da60132bd0f6b64ab8626ac3158093481cd21e`。未来 PR 目标是 castbox/guru-trellis 的 main。独立候选评估为 architecture_impact / target_native，引用 ADR-ISSUE-REVIEW-INTAKE、ADR-005、ADR-009。项目 Baseline、constitution 和 change contract 均使用现有 authority。

## 2. 当前系统、边界与目标差额

只建单从 Sync、Discovery、Clarify 和 Readiness 取得已审目标，再由 Create Issue 写入。独立需求审核先请求 Discovery 上下文。独立就绪审核可从 Sync 后的已知 Issue 进入按缺口补审。D1 在三个实际入口先按目的和实际证据决定启动的工作。开工请求继续走既有正式 Issue 入口。本批没有前序 Delivery。

## 3. 来源设计处置

#887 的方案是候选，未给出规范性接口。行为、兼容、正文与验收源于 #887 及现有内容和开工约束。第 4–8 节展开本批方案。

## 4. 模块、职责与设计取舍

- workflow 选择用户要求的创建、需求审核、开工就绪审核或正式开工入口。只读结果由该入口的专属 stop 返回。只有用户请求开始工作时，建单成功才把正式 Issue 交给 Sync 和既有开工就绪流程。
- Create Issue 为资料充分的只建单提供直接语义路径。Agent 读取当前仓库身份、查重和相关来源。完整采纳共同 Issue 内容方法，保留 Clarify 的正文责任及 Readiness 的交付单位判断。若出现真实需求、范围或交付依赖缺口，调用原 owner 补查。必要完整链仍使用原交接。
- Clarify 和 Readiness 分别拥有独立只读入口。开始时读取当前 Issue 及有效讨论。Clarify 判断目标、边界、条件、来源承诺和可观察验收。Readiness 还判断独立交付与依赖。原 owner 按问题选证据，必要时进入原定向补查或完整链。
- 在当前对话采用仍适用的原调查事实和已审结论。没有可读的原证据时，重新执行本轮结论需要的最小调查。完整链适合跨来源冲突和影响范围无法界定的情形。无条件跑完整链会重复已完成工作。增加长期复审台账会引入额外写入和复审状态。

## 5. 接口与数据

独立只读入口各使用独立 profile 及当前 Issue 快照。正式 invoke 进行一次 repo-bound 只读核对后返回已完成审核或原 blocked。结果包含可显示的实际覆盖、结论和未决事项。消费方只呈现回复。就绪报告中的 ready 是语义结论，不能变成正式开工 gate 的 ready 出口。旧 standalone_review 和 existing_issue_intake 的 wire 可供当前已进入的原调用继续消费。

在直接建单语义审查完成后，Create Issue 的预备命令从 draft_id、已审内容、实际查重时间及评论正文生成 issue_creation_direct 输入。该 profile 沿用现有 executor 的字段和操作。调用方使用完整 stdout result。直接入口若在实际写入前检测到过期或内容不匹配，返回 direct_review_refresh 及原 reason_code，由 workflow 交回同一个 Create owner。它按实际原因刷新查重或受影响的审查。旧 issue_creation 的 refresh_review 及原 consumer 保持原义。预备命令只做客观输入校验、转换和内容绑定。

## 6. 状态、顺序、正常与失败流程

新建单顺序为读来源和查重、审完整标题正文和评论、预备准确 payload、展示后取得一次写入确认、调用既有 writer、两对象回读。查重超过当前执行时限时，在 provider 写入前重新核对。仅查重过期时保留适用正文审核和对同一可见 payload 的确认。若目标、查重处分、正文、标签、评论或实质依据变化，重新审核受影响内容。确切可见写入计划变化时重新展示。

独立复审首先比较对象、正文、影响结论的讨论和原依据。若只有无关内容变化，沿用原结论所需的有效证据。若影响能够界定，则只重看受影响判断和必要上下文。不可读或影响无法界定时说明缺口，保持原 owner 的补查与停止规则。命令失败保留原失败、错误字段及同 owner 重试入口。

## 7. 恢复、兼容、迁移与集成

只在原动作确定尚未写入时才可重新预备。输出丢失、provider 结果未知或创建后回读失败均恢复原操作，并重用原 reviewed_at 和内容。原执行器先定位 Issue，再找原评论，只补确实未完成的评论。旧调用、旧 typed exit 含义和已有尝试均按原工作流恢复。匹配完整 workflow 和 preset 成套采用。当前任务和用户文件通过既有 tools owner 保护。

## 8. 验证设计

- V1 对照同一材料的真实 Codex Agent 运行。记录进入步骤、实际命令失败和重试、首个可审阅结果墙钟时间，等待确认单列。验收以确切减少交接或重复调查和实质输出完整为准。
- V2 使用正常缺口、实质变化和仅查重过期材料验证原 owner 分流及变化影响。观察只读结果和 Scope 之外零写入。已建立的正式开工补查工程测试继续覆盖旧 wire。
- V3 使用现有状态化 GitHub CLI 测试替身，执行正式 Create 包装器以及实际 stdout 驱动的恢复，确认一次创建、一次评论与两次对象回读。捕获真实 Agent 的只写预览及请求开工后的实际路由。外部替身结果限于已声明边界。
- V4 运行源、受管投影、安装包、回执路由和 reapply/drift 定向检查。需干净安装时运行一个代表样本。无发布矩阵。

## 9. Canonical 引用、本轮差额与实际未决项

现行职责定位为 `docs/architecture/03-domains/issue-review-intake.md` 及 `docs/{requirements,design,test}/current/issue-content.md`，隔离 Architecture 贡献与 ADR-887-ISSUE-ENTRY-STREAMLINE 定义当前责任及窄替代。implementation 完成后原 Architecture 和 RDT owner 执行 final_integration，独立 committed Review 再审核真实 after。当前无需求未决项。
