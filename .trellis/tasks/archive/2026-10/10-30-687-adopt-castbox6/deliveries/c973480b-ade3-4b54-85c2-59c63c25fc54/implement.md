# D1 固定来源采用实施计划

## 1. 输入与引用

整体Task `prd.md` 的AC1–AC5、本批PRD DR1–DR5、design第3节唯一来源设计处置是本批范围。内容基线B=7718d129bcb2055d77c7f43d0e4edca9aee313ea，无前序Delivery。本批design第9节所列完整canonical/spec合同由实施和审核实际读取；原维护Skill拥有严格来源与恢复，不能由测试driver替代其判断。

## 2. 有依赖顺序的步骤与文件责任

1. I1 source/implementation owner：核对已发布17015f98/.6的merge、parents/tree/mainCI40882919377及四附件；更新canonical lock、manifest target/requires/tested、原upgrade runtime三处精确pin及其原测试预期。修改前执行checkout boundary。
2. I2 同owner：更新README、preset README、workflow README中的当前来源段落，保留历史已发布Guru .6的.5配对。通过原installer/合法tools-only投影同步dogfood与selected平台，检查每个sidecar，保留历史Task和无关文件。
3. I3 RDT原owner：按第6节写687贡献与三个完整proposed当前单元。实际Test观察在I4完成后补齐；不预填通过，不写shared CURRENT。
4. I4 implementation owner：在隔离Git源码checkout精确Fork17015f98，正常pnpm frozen install/build，成功后写原source marker；从当前候选生成干净已提交Guru snapshot并核对canonical bytes/mode；运行原validate-source。在一个隔离已有目标通过原tools-only维护公开入口完成采用，比较Task/session/用户内容/peer。维护后执行installed Core/Python stop与重试/保留性断言、reapply/drift/sidecar和原定向回归。临时driver仅执行/记录事实，不写语义gate。
5. I5 原Architecture/RDT/Check owners：候选Architecture phase2与RDT task_impact_sync→candidate Check→原RDT final_integration晋升；Architecture原owner同步687贡献中三处完整当前定义；两知识owner写后均读回并确认实际适用性。implementation重建完整candidate/begin_check→实际final Architecture/Check→TaskCommit→独立完整固定B..HEAD BranchReview→DeliveryReview/Publish/Merge。
6. I6 原Completion/Closure/Finish owners：核对全部AC和真实Delivery事实，完成Issue处置、归档与独立bookkeeping；不以Delivery合并替代整体完成。

## 3. 验证入口、输入与预期观察

- V1：Git/GitHub读取精确source/CI/Release，附件SHA256和CLI/Core精确依赖。pnpm@10.32.1正常build，输出与来源lock一致。
- V2：原source/installed package checker、upstream ownership、dogfood drift；核对canonical lock和目标投影，当前.6和历史.5分开。
- V3：原`verify_trellis_compatibility_matrix.py validate-source --repo-root <clean-guru> --fork-source <clean-fork>`；原`_upgrade_native_bootstrap_tools`调用公开preview/prepare/invoke，要求tools_upgraded和unverified=[]。独立比较维护前后保留对象bytes/mode及真实installed包。
- V4：实际installed Core SDK与Python `delivery.py`公开stop，对两种旧profile的合法保留样本检查stop/retry、peer/history/selection和无Completion/Closure。使用原合法历史构建/maintenance生成输入，不手改真实业务Task或扩大workflow profiles冒充修复。
- V5：原`test_tools_only_installer.py`、`test_verify_trellis_upgrade_contract.py`与受影响maintenance package测试；原reapply/drift、ownership、递归sidecar检查。根据实际改动执行最小可靠集，不新增只固定版本字符串的测试。

V1–V5对应design同ID和DAC1–DAC5。工程命令与实际安装证据分别记录来源/环境/结果；没有本轮真实业务升级、全平台累计矩阵或新Guru软件Release。

## 4. 停止条件与适用回退点

缺完整匹配来源、CI/附件身份或严格入口失败时，保留第一失败并回原owner恢复。发现范围、owner、状态authority、机制或验收责任扩张时，在写入前返回原qualification/Author/Architecture。仅隔离目标允许原maintenance rollback/recovery；不改真实业务状态，不批量迁移历史Task。保留无关dirty、已有stash和其它worktree。

## 5. Delivery Policy（唯一）

policy=full。本批承担整体R1–R5及AC1–AC5；没有当前范围内延期责任。独立交付条件是唯一来源与精确pin已采用，代表性实际source_locked维护、两profile停止和保留性定向验证满足，原Docs差额完成晋升，完整质量门禁通过。合并后整体Completion仍由原owner依据全部AC和真实证据判断。范围外累计矩阵、软件Release与业务安装不作为本批通过依据，也不因未执行它们宣称整体功能已生产采用。无新增临时能力限制。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原`guru-maintain-requirements-design-test-ssot` writer拥有`docs/requirements-design-test-contributions/687-adopt-castbox6/`的最小需求/设计/测试/追踪与manifest，以及`docs/{requirements,design,test}/current/native-compatibility.md`完整proposed单元；承接R630-05/D630-05/T630-06的当前.6采用关系，保留#630历史.5观察。实际执行Test不回写原历史记录。当前生命周期R657-03/D657-03/T657-05的stop/release原则保持，只补本次installed回归引用。

直接consumer是候选Check、原RDT final_integration晋升、最终Check和后续Completion；晋升在candidate_checked之后、最终Phase2之前发生。README当前来源由implementation owner同步。Architecture candidate_assessment为architecture_impact/target_native。本Author拥有 `docs/architecture/contributions/687-adopt-castbox6.md` 与配套manifest、三份完整proposed正文；原Architecture owner在candidate_checked后final_integration晋升三处当前定义，保留#630历史边界。final_plan/phase2/committedReview/下游仍由原owner执行；无需新ADR，不改全局版本入口。没有owner以记录最终pass/HEAD为由额外追加文档提交。
