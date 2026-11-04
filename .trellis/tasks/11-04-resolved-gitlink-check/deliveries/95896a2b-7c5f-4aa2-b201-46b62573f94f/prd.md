# D1 resolved gitlink Check 需求

## 1. 整体来源与术语

整体 authority 为本 Task `prd.md` 的公共 accepted_scope，本批 scope_ref 选择 R1—R4、AC1—AC4。来源、resolved merge 与 stage-0 gitlink 定义读取整体PRD第1节；本批不改变这些定义。canonical Check common/record/check/delivery 是当前实现证据，Reconcile execute 是现有精确提交责任。完整来源已读；没有来自 Issue 的规范性设计方案。

## 2. 整体与本批目标、非目标

当前普通 HEAD 绑定把合法 resolved stage-0 子模块更新拒绝，阻断精确整合。D1完整修复这一缺口及正式命令组合，保留普通 Check、child root/clean/OID 和候选变化检查。非目标为业务导航、release/tag、恶意输入、并发压力与完整多平台矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首次D1，无前序Delivery。开发基线、content base B 与当前H0均为 main `b78edbbdc32e77392bc3775366473971050ccb4b`。交付目标 main，profile=pull_request。源码、dogfood、完整source调用及target既有API/consumer兼容验证属于本批；源码merge后原调用方真实候选复跑由原Check/Reconcile owner承接，整体Completion须核该结果。不得把工具PR合并解释为调用方已恢复。

## 4. 本批调用方、场景与流程

- DS1（S1）：调用方保留合并前HEAD和单一MERGE_HEAD，正常解决冲突、stage-0包含新gitlink，child clean且HEAD匹配stage-0。专用resolved入口依次record/check/invoke/project，原Reconcile执行精确tree/parents/message提交，随后真实新HEAD进入普通Check/fullReview。
- DS2（S2、S3）：普通入口面对暂存但未提交的gitlink差异仍拒绝；任何入口发现child dirty/HEAD不匹配、未解决冲突或被审候选变化时阻断过期结果。
- DS3（S4）：原调用方从clean且完整matching reviewed source运行原wrapper --root target。source runtime只提供原Check；target公共API与原Reconcile继续各自职责。必须证明该组合兼容；不复制runtime、不更换Task、不混合安装、不排除路径。兼容不能成立时返回原安装owner。

## 5. 完整行为、条件与约束

- DR1（R1）：只有专用resolved profile采用stage-0 gitlink目标，并固定HEAD、单一MERGE_HEAD、stage-0 tree/index与完整被审内容。
- DR2（R2）：普通capture身份算法保持；子模块exact root/clean/OID和正常候选变化继续校验。typed_exit文字不能开启resolved路径。未解决冲突、未暂存内容不能通过。
- DR3（R3）：record/check/invoke/project使用同一候选语义；原Reconcile独占精确提交。拒绝先commit绕Check。完成后新HEAD仍需fresh Check/fullReview。
- DR4（R4）：canonical修复经原受支持完整source入口或原安装owner恢复；公共输出及consumer compatibility必须一致，不引入业务资料到公共模板。

## 6. 本批验收、验证方式与未决项

- DAC1（AC1）：正常Git merge fixture包含合法staged gitlink，真实record→check→invoke→projection→原Reconcile成功，核提交tree/parents/message。
- DAC2（AC2）：普通入口staged差异仍拒；child dirty/HEAD不匹配、unmerged与capture后候选变化返回原诊断，不将失败样本排除。
- DAC3（AC3）：无gitlink、普通gitlink、resolvedgitlink和wrapper实参组合回归通过；测试不得仅mock身份函数或预填通过。
- DAC4（AC4）：canonical/dogfood一致，clean完整source --root 与target已安装API/原Reconcile消费组合验证通过；merge后原业务owner复跑真实候选。源码单测不替代该复跑。

需求没有待用户决定的问题；具体candidate进入独立Architecture前只保留Author的最小方案事实。当前未实施、未验收。

## 7. Canonical 引用与本轮差额

- 行为/设计合同：`trellis/skills/guru-team/packages/guru-check-task/references/contract.md` 与原Reconcile合同；本轮专用resolved capture差额必须同步，普通入口保持。
- Test：原Check package tests 与Reconcile真实组合；新增正常fixture，保留既有普通语义。
- Architecture：`docs/architecture/README.md` 的角色与晋升边界；`00-foundation/design-constitution.md` 的职责内聚、最小复杂度；`06-governance/change-contract.md` 的九concerns和candidate/final独立评估。本轮是既有owner内的target_native修复，不预写shared CURRENT；独立Architecture判定实际影响后由原owner维护必要差额。
