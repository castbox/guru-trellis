# #575 S2 来源准备执行计划

本文定义稳定执行顺序。整体根 PRD 拥有 accepted scope，当前 PRD 拥有来源切片要求，唯一 source-design matrix 位于 `design.md` D2。实际命令结果只写原 RDT 贡献的 Test。

## P1. 唯一 Delivery Policy

策略为 staged。整体 R575-01..07/A575-01..08 不变，有序阶段为 S1 来源采用→M 独立维护→S2 来源准备→S3 完整投影与验证→Whole Completion/Closure/Finish。发布 Issue Stage 2 不作为准备 Task 的未完成实现。

当前 S2 入口：原 Check 合法返工到同一 Delivery 的 planning；原 Author完成来源切片要求，candidate Architecture→solution planning→Wording→final Architecture→Planning Approval，展示新三文档后由原 Activation 接受当前计划。

S2 独立出口：canonical .4 版本消费者、公开源码映射、原已采用 .3 基础工具及 Task2/session3、当前来源定向验证和 isolated RDT contribution经本切片 Check/TaskCommit/完整独立 Review后 refs-only交付，形成实际 clean committed .4 source。该出口可检查并由下一安装操作直接消费，不要求执行尚依赖该提交的 .4 正式安装。

S3 保留完整 .4 packages/runtime/schema/四平台投影、三平台 reapply/drift、正式 clean/predecessor/maintenance/native/恢复证明、完整 contribution 收敛与共享晋升。S3 由实际下一切片 Creation取得新 key/root；不提前写未来规划或制造空 Delivery。Whole Completion检查所有准备阶段和实际证据，不能从 S2 合并推导完成。

## P2. 唯一 Docs SSOT Plan

策略为 delta_first。唯一 writer 为 guru-maintain-requirements-design-test-ssot，贡献根 `docs/requirements-design-test-contributions/575-release-preparation/` 使用 manifest.yaml、requirements.md、design.md、test.md、traceability.md。来源为 Task整体要求和当前 S2 PRD；requirement→design→test双向 trace分别承接当前来源切片与 S3剩余义务。

S2 final Phase2前由原 owner完成当前delta reconciliation。贡献保持draft，不提前改变shared current；Test区分现存.3真实维护、canonical .4模块结果及尚未执行的.4正式安装。S3补齐最终证据后，在首次完整committed Review通过后按fresh expected-current串行晋升；晋升差额fresh Check/TaskCommit/另一轮完整独立Review。Architecture由独立owner判断，无impact时不建贡献或ADR。

## P3. 当前来源切片的实施顺序

1. 完成当前同-key重规划和全部规划门禁；新方案展示并接受后才重新 Activation。根PRD和历史Delivery规划不覆盖。
2. Trellis implement agent按当前source/consumer合同完成canonical .4版本、生产输出/消费者/fixtures与managed interpreter修复。Main按D3修订四处当前源码公开映射，稳定.3事实保持原归属。只处理已接受要求；新候选先原资格审查，owner/API/authority扩大回原规划。
3. 保留并审查M原.3基础工具/原生采用的全部受管差额。核对当前receipt、native、ownership、workflow、四平台入口和配置/Task/session/common/peer状态；不手工同步.4生成副本、不运行需要clean .4来源的新工具操作。
4. 原RDT owner收敛当前contribution及trace，执行V1/V2/V4/V5/V7的S2范围。fresh独立Architecture phase2后，由完整Trellis check评估当前切片、code/docs subtraction、测试价值和全部已披露边界；只有实际guru-check-task:passed才进入TaskCommit。
5. 原TaskCommit展示精确staging/commit清单并独立确认。固定B→实际H，由不同独立Review评估全部实际committed差额和PR diff；新finding回其原owner，内容变化刷新受影响门禁。原publication Architecture/Delivery Review检查source切片和剩余S3责任，不声称.4全安装或whole completion。
6. Publish/merge各自展示远端对象、head和Refs-only中文payload，分别确认后执行。S2实际Delivery结果进入Whole Completion的剩余工作判断；S3原Creation取得key后，从clean committed .4来源启动其新操作。当前计划不预授权这些Git/GitHub副作用。

## P4. 最小可靠验证与归属

Python走执行source/target自身managed resolver，不用外部source代跑目标native。

| 编号 | 原入口与S2检查对象 | S3或发布阶段保留项 |
| --- | --- | --- |
| V1 | verify_trellis_compatibility_matrix.py validate-source，exact-built Fork 2a6f10b的commit/tree/parents/CI、CLI/Core/pnpm/build/template检查 | 新 .4 tools操作的formal clean Guru source/API检查在真实提交后执行。 |
| V2 | 原test_contract、test_resume_source_update、具备真实CLI env的test_delivery_upgrade和test_fork_preparation；生产结果→schema/consumer、合法旧族、source mismatch/dirty、Plan2/resume/rollback | 既有fixture/preset替身不替代正式 .4 installed/native维护。无新依赖变化不重复无关检查。 |
| V3 | S2只保留M原 .3 tools/selected Task的真实分层事实与原备份 | S3原tools preview/prepare/invoke和所选Task apply/observe/finalize，必须目标native与下一实际owner通过；同操作恢复不reprepare换identity。 |
| V4 | 原check-skill-packages source/四平台发现投影；现存.3 installed/receipt检查；私有release Skill合同四份byte parity | 最终.4 installed和全部版本相关bytes parity由S3检查，不能用现存.3结构通过替代。 |
| V5 | 原Fork dogfood native projection、ownership、现存workflow/spec/platform投影及其已采用来源；全部受管差额进入Review | S3新.4原tools-only安装后做三平台apply/reapply/drift、权限、sidecar和退休资产检查；旧归档guard不放宽。 |
| V6 | S2不从dirty source执行正式.4安装 | S3一个focused Codex clean/local-workflow和真实stable.3 predecessor维护样本；最终remote immutable provider、predecessor和tag smoke归发布Stage2重跑。 |
| V7 | 完整来源/基础图差额的diff hygiene、真实secret scanner、权限、递归bytecode/sidecar/residue；上游生成文本例外只按现有provenance合同判断 | 任何后续新bytes刷新受影响检查；缺scanner、漏扫、未审查告警、FAIL或SKIP不计通过。 |

所有结果由原Test准确记录source与验证层次。失败先判断当前回归、不可分前置、环境或不相关历史问题；不通过改timeout、缩窄样本或放宽guard追求全绿。不执行累计多平台/native-host矩阵、真实业务安装或生产验证。

## P5. 整体终态与交互边界

S2准备来源、S3完整安装证明和最终Docs收敛全部完成后，原Completion判断整个准备Task。reference-only Closure保持#575 OPEN，Finish另行archive/bookkeeping；之后发布Stage2对最终main candidate执行正式门禁。commit、push/PR、merge、Finish、tag/Release、Issue closure和cleanup各沿原owner的精确副作用边界。

本计划不记录授权、gate进度、发布checklist或逐轮状态，不创建第二规划writer、兼容reader、恢复框架或跨仓实现。历史归属、Task/source/session身份和无关工作保持。
