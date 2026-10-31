# #693：合同承接与验证证据方法

Task `693-contract-evidence-adoption` / generation `0`，Delivery `e20f478c-2398-40ad-a438-c493eef0506a`。来源为 [#693](https://github.com/castbox/guru-trellis/issues/693)。本贡献供本批 final_plan、完整候选 Architecture/Check、原 final_integration 和 committed Review 消费。当前为完整实施与拟写候选，不表示共享晋升或后端目标安装已完成。

## 适用 authority、起点与真实差额

固定 before 为 Git `e514770dfa03711a4606046232593b9bf782695a:docs/architecture/`。baseline identity 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`，change-contract 为 `guru-trellis-architecture-change-contract-v1`。原独立 candidate_assessment 返回 `architecture_impact / target_native`，decision refs 为 ADR-034、ADR-KNOWLEDGE-FINAL-INTEGRATION。该结果只供 Author 形成方案，不代替后续当前评估。

原共享覆盖规则已经要求实际未改消费者、旧工程事实适用性及当前独立判断。原测试价值规则已经拒绝绕过被测入口的证明。原机制方法覆盖对象、时序及采用适用性。本项保留这些能力，补齐其执行动作：沿生产者输出和持久完成状态追踪消费者使用前提；在新调用条件下核对复用参数的对象、存在阶段、状态和顺序；对照测试声明边界与正式路径，区分合法边界前 fixture 和边界内代产出。

完整方法分别由 canonical `workflow-contract.md#candidate-applicability-and-coverage` 和 `quality-guidelines.md#test-and-validation-value` 单写。原 Author、Architecture、Check、Branch Review 和 Delivery 判断只加载并消费同一方法。本项目 change-contract 补消费定位，RDT 原 owner 在 knowledge-maintenance 完整单元承接行为、职责及测试关系。项目指导不复制业务字段、领域成功条件或另一套方法正文。

## 必要性、替代与兼容

具体差额服务本次明确要求的合同追踪与证据判断。仅增加原则不能说明实际检查动作；新 Skill、阶段、schema、脚本 reviewer 或永久证据台账没有额外直接 consumer。选择原正文和原职责内的最小修订。

本项不改变 runtime、public I/O、typed exits、九 concerns、descriptor/check/result identity 或最终质量顺序。旧完整安装在正式采用前保持其实际合同；公共源码、dogfood 与后端采用分别报告。后端领域整改、业务回归、部署和 QA 均不由本贡献承担。

没有长期 owner、GAP 生命周期、compatibility exit、架构决定或原则例外变更，因此当前候选不新增 ADR。若 final_plan 或实施评估发现这些事实变化，由原 Architecture owner 重新判断。

## 九 concerns

| Concern | 适用性、理由与本批承接 |
| --- | --- |
| authority-binding | applicable；同 Task/Delivery 的原 Planning purpose 与 before authority 保持，候选和最终结果各消费其实际对象。 |
| constitution-binding | applicable；完整五原则约束采用方法和维护面，不建立原则评分或第二 authority。 |
| boundary-and-decision | applicable；共享方法与项目消费分工明确，业务定义仍由所属 authority 单写。 |
| owner-and-single-writer | applicable；原语义 owners 各自判断，RDT/Architecture 各自写完整隔离候选及最终共享正文。 |
| compatibility-and-exit | applicable；没有 public 格式或旧 reader 迁移，正式安装沿完整匹配源与原 Upgrade owner 承接。 |
| gap-and-deviation | applicable；不新增或关闭无关 GAP，不以方法修订声称历史漏检理由已确认或业务事故已修复。 |
| parallel-scope | applicable；Planning 只写本 Task 规划、贡献和完整拟写；共享 current 等待原 final_integration，保留并行内容。 |
| evidence-and-freshness | applicable；实际候选、原证据与当前判断分开，工程执行、语义判断、分发及外部采用各限于真实证明范围。 |
| review-and-promotion | applicable；完整实施及所有 proposed targets 先由独立 Architecture/候选 Check 审核，原 owners 最终写入读回，再覆盖 actual after 和完整 committed range。 |

## 完整目标与原晋升

完整项目拟写为 [change-contract proposed target](./693-contract-evidence-adoption/proposed/docs/architecture/06-governance/change-contract.md)。内部引用按最终目标路径解释。拟写保留 before 的全部现行内容，只在“候选适用性与独立职责”增加共享方法及测试边界消费定位。

原 RDT owner 在实施期准备配对三层完整 knowledge-maintenance 候选及 R693/BEH693、D693/CON693、T693 关系。它不写本项目 Architecture 正文；本贡献不替代 RDT 定义。

项目检查继续使用 `guru-trellis-architecture-convergence:repository:1`、`guru-trellis-architecture-convergence@1` 和 `guru-project-architecture-check-result-2.0`。原独立 Architecture 对当轮完整对象亲自判断，不预填未来 pass。Planning 不晋升 shared current；候选 Check 后才由原 owner 执行 final_integration/readback，implementation 以同 B 和全部实际 after 重绑，最终 Check 与完整 committed Review 覆盖真实写入。

## 证据与剩余责任

历史固定源码、当时规则、公开计划/阶段事实及原命令用于只读分析。源码失配支持具体合同分析，不证明历史 reviewer 的思路；缺失理由保持未知，不重建其他 owner 的 private state。本贡献不包含现场业务标识或敏感记录。

初次 Planning 拟写时尚未实施或运行工程检查。D1 的计划验证见所选 Delivery design 第8节；后续实际源码、同 checkout 工具同步、分发检查与未知项由 [Test contribution](../../requirements-design-test-contributions/693-contract-evidence-adoption/test.md) 承接。本贡献不追写自身最终 pass。D1 只交付 AC693-01..04。公共交付后，AC693-05 的后端正式安装和适用项目指导采用由原 Upgrade/项目 authority owners 查实并执行；未采用前 #693 整体责任尚未完成。
