# 阶段成果收敛与完成证据一致性：D1 实施与验证计划

## 1. 输入与引用

本批为 full D1，读取 Task root `prd.md` 的 AC649-01..07、本 Delivery `prd.md` 的完整行为与本 Delivery `design.md`。规范性来源设计只由 design 第3节处置；本文件不建立第二矩阵。起点 B/H0=`319202beab79c7666ecdb855291bf117e43d407e`，没有本 Task 前序 Delivery。实际 DeliveryKey 为 `649-stage-result-convergence / 0 / 244a5d53-0d81-4d1b-aebf-a6a56bf54e0d`。

实施前完整加载 live #649、必要 #648 实际结果、原 Author planning-body/authoring 和 Delivery 模板；阶段状态的三层 `docs/*/current/task-delivery-lifecycle.md`、`completion-closure.md`、`knowledge-maintenance.md` 及其必要关联条件；Architecture baseline/constitution/change-contract。设计中的 candidate_assessment 仅是当前方案输入，后续新判断使用其原阶段入口。

命中的 Skill contract、公共 Skill I/O/private-state 规范、causal-completion-semantics、quality-guidelines 的 Test And Validation Value／Validation Scope Ownership、workflow-contract 的 Candidate Applicability And Coverage 由各原 owner 在写入／审核前读取。官方 Trellis workflow/spec marketplace 扩展文档约束分发方式；不修改上游、node_modules 或 hook 实现语义。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 依赖与原 owner | 文件及实际动作 | 可审核完成观察 |
| --- | --- | --- | --- |
| I649-01 | Planning 当前已接受并由原 Activation 激活后，实施 owner | 冻结 B 匹配包和设计第8节样本；重读 #648 Test、archive 与原公开结果；盘点 canonical/dogfood 与测试 transport 接口 | before 方法可重建，#648 有效观察／失败／未证分开，不写授权记录 |
| I649-02 | I01，实施 owner／design 第4节逐一列明的原方法 owner | 修改 design 第4节列明的原 step-local Markdown、Delivery implement 模板及必要既有示例；补六维、四类缺口、限制解除与 cutoff 规则 | 逐场景能定位原 owner 正向行为和 gate；无新 public API/state/exit/reviewer；global 只保留原编排 |
| I649-03 | I01，可与 I02 按实际文件独立推进；实施 owner | `adapters/eval/stage_result_authoring.py` 及现有 native adapter/staging/constants/runner 的必要测试接线；原 Check/Delivery Review/Completion/task-free evals 与对应定向测试 | current Task/Delivery 事实从原 API 产生；Agent 写实际 result 并调原 wrapper；不从 expected 表生成答案；legacy runner 不冒充 current |
| I649-04 | I02/03，实施及原测试审核 | 按 V02/03/04 跑 before/new 独立样本，逐次人工语义审核实际读取、判断、原因、owner route 和 wrapper stdout；失败保留并修命中方法/transport | 测试支持与产品语义分开；错误出口期待、执行错误、无评分、真实漏检分别记录；无答案泄漏 |
| I649-05 | I02 和实际新事实，原 RDT owner；Architecture 独立判断 | 在 `docs/requirements-design-test-contributions/649-stage-result-convergence/` 形成真实贡献、完整 proposed targets、trace 与实际 Test；准备 #637 有限修正 | 当前定义完整，历史保留；每个 proposed target 有实际差额；no-impact 不造 Architecture contribution／ADR |
| I649-06 | I02/03，实施 owner | 完整 canonical apply/reapply 同步 dogfood；一个代表 clean matching 安装，命中 installed source/native 入口及平台/mode/drift/sidecar 检查 | 方法、引用和脚本安装可用；用户内容保留；零未处理 .new/.bak；不扩完整矩阵 |
| I649-07 | I04/06、#648 匹配前置，原各 owner | 在 V06 同一实际 Task D1 partial 合同→D2 实施中执行真实原 API、原 wrappers、本地 commit/merge、约束冲突和合法修订、候选及最终链 | 逐个连续结果来自实际前序 stdout；current 文档／断言收敛；四类缺口／六维与整体剩余边界正确；受控 provider 证据限定测试层 |
| I649-08 | I04..07，implementation／独立 Architecture／原 Check | 固定 B 及完整差额 candidate/begin_check→candidate Check；原 RDT/Architecture final_integration 实际整合读回；同 B 实际 after 重绑→final Check | shared current 实际写入纳入新 content_ref；candidate pass 不当 final pass；适用事实可复用而当前语义新判 |
| I649-09 | I08，原 Commit／独立 Review／Delivery Review／Publication／Merge | 精确当前文件 TaskCommit、完整 committed B..H Review、readiness、真实 PR/merge；每项 Git/GitHub 副作用由原 owner 展示后按当时授权执行 | 中文 PR 真实描述验证与边界；scope/关闭语义正确，merge 可达 live main，不夹带无关改动 |
| I649-10 | I09，原 Completion／Closure／Finish／Cleanup | 审全范围及全部实际 Delivery，再按原终态／归档／bookkeeping／清理入口承接 | satisfying PR、main ancestry、Issue CLOSED/COMPLETED 与各原结果分别真实；共享 Docs 不由终态 owner 补写 |

步骤依赖是执行顺序，不是新增流程 stage。没有实现授权前只完成本轮规划与原规划 gates。实现过程的普通技术返工自动返回原 owner，不创建其它 Task/Issue 或提前清理工作区。

## 3. 验证入口、输入与预期观察

全部验证对照 design 第8节 V649-01..08，不预填结果。使用仓库匹配 managed Python resolver 运行所需 unittest／runtime；不把系统 Python 缺依赖记为产品通过。

| 入口 | 输入、用途和预期观察 |
| --- | --- |
| `trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill <原 skill id> --adapter codex --case <设计第8节样本> --run-root <repo外目录> --current-package <new包> --comparison-package <B包>` | V02/03/04。双方提供相同测试 corpus/transport，生产方法分别是 B 与 new；原框架的 host-only semantic-grading 在实际执行后逐次填写。禁止先填评分再宣称真实判断正确；模型沿同一实际配置，不锁死版本常量 |
| 同一原 runner 的 `--mode installed`，并使用原 installed package | V07 的命中代表，核安装方法与新测试支持实际可运行；source 结果不替代 installed |
| 命中 package 的原 tests：Author planning chain、Check、Delivery Review、Completion contract、task-free；`trellis/skills/guru-team/tests` 中实际 adapter/runner/distribution tests | V01：实际调用对应逻辑和原 wrapper，观察输入传递、正常失败及 current Delivery 接续；只跑本次差额涉及的模块，不以全文固定字串保护实现 |
| V06 连续样本入口：现有 native transport 的 command-forwarding，新增私有测试 driver 只调用原 Task/Delivery、原 executor 与各原 wrapper | 输入是 design 第8节冻结的 D1/D2 场景及其实际前序 stdout；host 不预写 semantic gate/DeliveryFact。实际本地 Git 与 promotion/重绑/最终Check/committed Review、Delivery Review/Completion 全部发生。driver 不新增生产 API |
| `gh pr view 644 --repo castbox/guru-trellis --json state,headRefOid,mergeCommit,mergedAt`；原 #637 archive 与 `git merge-base --is-ancestor <实际merge> <实际main>` | V05：只核可证后续事实及 ancestry；逐项比对原“尚未验证”，有限修正当前 cutoff／引用，保留真实未证项和历史 |
| `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`；`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`；原 package source/installed checker 与平台投影／权限检查 | V07：canonical/dogfood/installed、声明平台、mode、reapply、sidecars；按原脚本帮助选择定向参数。只做一个代表 clean，后续普通 fixture 复用匹配安装副本，不伪称新增矩阵 |
| 原 candidate/begin_check、Check、maintenance final_integration、实际 after 重绑、final Check、TaskCommit、完整 committed Review 及本 Task GitHub/终态入口 | V08：实际内容／范围／原结果可核，不以本计划或测试 exit 代替真实 gate；完整多平台升级／Release、业务采用与生产 E2E 继续未验证 |

测试私有 driver 的具体文件落在 Completion 原 tests 或共享 eval 测试支持目录，按实际共用职责选择一个位置；测试指令和参数须由实际接口核实后写入唯一 Test 结果。这个实现细节不改变冻结场景、原 owner、原接口或证据层次。测试支持若必须改公共生产契约才可运行，停止而不是静默扩大范围。

## 4. 停止条件与适用回退点

- Task/generation/key、registered checkout、source 或 accepted_scope 不匹配：停止写入，回原 identity/checkout/scope owner，不重建资源。普通输出丢失沿原 producer 重读恢复。
- 约束／前提与候选冲突：暂停受影响 operation；机制错误回原 Author／Architecture，真实来源或 scope 变化回 Clarify，实现／断言错误回 implementation/Check。无冲突工作只按真实依赖继续。合法修订后刷新受影响规划、判断与实际候选再恢复。
- 必要事实或外部证据缺失：明确对象、依赖 operation 和原 evidence owner；只停止依赖声明，不抹去已成立其它维度。无关未知保持边界，不制造 blocker。
- native transport 调用失败或缺必要依赖：保留首次 execution_error/no-grade，在原测试支持范围修复；不能记成语义通过或通过修改期待值掩盖错误。被测 Agent 接收 host 答案时该观察无效，修复隔离后重新执行该同口径样本。
- final_integration 或实际 rebind 后内容变化：按原 candidate applicability 重审实际受影响覆盖；不能用旧 pass 或追记结果豁免。无变化工程事实可按定义、参数、环境、工具链及预期适用性复用。
- 无生产或 DB 写入，本批不建立生产回滚协议。普通文件修复只改本次明确范围；不 revert／清理无关 dirty、worktree 或旧证据。Commit/push/PR/merge/closure/finish/cleanup 分别按原 owner 当前具体计划处理。

## 5. Delivery Policy（唯一）

选择 **full**。本 D1 完整覆盖 AC649-01..07：原 step-local 方法、模板／示例、必要 native 支持和独立实际 Agent 评测、六维与 task-free、#648 自身证明承接及真实 D1/D2 组合、#637 有限修正、RDT 当前知识、定向安装分发、最终质量链、真实 GitHub 交付及整体终态。组合样本内 D1 partial/D2 implementation 是测试事实，不把本 Task 改成 staged 或 partial。

本批真实临时边界是：Planning 尚未接受，方法、样本和当前知识仍未实施，所有本项验证与终态均未完成。原因是当前仍在规划阶段；解除条件是依次完成本文件步骤和真实证据。后继责任分别由实施／RDT、原 Check／Review、Publication／Merge 和 Completion／Closure／Finish／Cleanup 承担。源码更新、安装通过、Delivery 合并任一项都不能代替其它阶段。

没有延期给 #651 或其它 Issue 的 accepted scope。整体 Completion 仍须本项独立评测与组合分别完成，#648 必要前置有效，本批所有真实 Delivery 和 satisfying PR 可核且合入可达 main，当前知识真实维护。Release 完整矩阵、业务安装采用与生产效果是范围边界，不伪装成延期实施工作。本 Task 的真实终态由最后原 owners 返回，不要求受审正文回填自己的最终 pass 或最终 HEAD。

## 6. Docs SSOT Plan（唯一）

选择 **delta_first**。原 RDT owner 以本设计、批准 delta 和实际 implementation/eval 观察写本 Task 隔离 contribution，准备完整 proposed targets；candidate Check 后由原 `final_integration` 写共享 current 并读回，再以实际 after 重绑、final Check 和完整 committed Review。Planning 不写 shared README/index/manifest 或预建空 contribution。

| 真实差额与 canonical 目标 | 原 writer／直接 consumer／晋升时点 |
| --- | --- |
| `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`：阶段限制、当前说明／断言、Delivery 状态与候选覆盖 | 原 RDT；后续 Author、实施、Check、Delivery Review；本批 final_integration |
| 同三层 `completion-closure.md`：六维、四类缺口、late facts 与终态 owner 边界 | 原 RDT；原 Completion/Closure/Finish 及其审核；同一次实际最终整合 |
| 同三层 `knowledge-maintenance.md`：完整当前定义收敛、cutoff、原结果准确引用及单写职责 | 原 RDT；知识维护和各阶段当前查询；不改变原 authority identity 或无关知识单元 |
| `docs/requirements-design-test-contributions/649-stage-result-convergence/{manifest.json,requirements.md,design.md,test.md,traceability.md}` 及原合同要求的完整 proposed targets | 原 RDT；candidate/final owners 和后续结果查询。实际 test.md 区分合同、确定性、真实 Agent、安装、GitHub 与外部边界，并写观察截止点；不追自身最终 pass |
| #637 contribution Test 当前状态／尚未验证的有限描述及必要当前 Test 引用 | 原 RDT；当前结果入口读者。只修可证过期项，保留原命令、旧失败与未知；纳入本批实际候选和最终覆盖 |
| `trellis/presets/guru-team/spec/workflow/{quality-guidelines,workflow-contract}.md` 的命中最小 projection，apply 后 `.trellis/spec/` | 原 RDT 与现有 package/spec 分发职责；原阶段 owner。只定位新增原 owner 方法，不复制 step-local 内部流程或新增阶段 |
| Architecture baseline/constitution/change-contract/current system | 原 Architecture 独立判断；当前 no-impact 保持 no_change，不造 contribution/ADR。后续真实变化回原 owner，不由 RDT 越界写入 |

导航仅在实际 locator/关系/状态变化时由原 owner 修改。结果说明以候选、观察截止点和正式结果引用承接；Closure/Finish 不补写共享文档。source/dogfood/installed 的真实分发和未验证业务采用分别报告。
