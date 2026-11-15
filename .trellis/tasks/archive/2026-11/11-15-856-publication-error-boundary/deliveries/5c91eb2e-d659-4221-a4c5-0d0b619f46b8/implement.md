# D1：实施与验证计划

## 1. 输入与引用

输入为根accepted_scope AC856-01至06、本批prd.md D1-R1至06、design.md第1至9节，规范性来源处置唯一见design第3节。实际candidate_assessment为baseline_current/no_architecture_impact；不是实施或final_plan通过。B固定4f3d9069e0720ec94e39d1079154d2f7a7058935，当前H0同B，无前序Delivery。

实施先完整读clear-technical-writing、companion-scripts的Python Runtime Constraints／Error Handling／JSON carriers／Intermediate Command Stdout、quality-guidelines的Test And Validation Value／Validation Scope Ownership、subtraction-first-compatibility、current-knowledge，以及原Publish owner与command/io和所有实际entry。不得从测试或旧摘要反推要求。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 责任、前置与实际文件 | 行为与完成观察 |
| --- | --- | --- |
| P856-1 | implementation；Planning正式接受/激活后；package tests | 在新test_public_errors.py建立真实wrapper缺字段/closing两例与invalid_json对照，明确副作用前拒绝；复用原fixture，不连接真实GitHub |
| P856-2 | implementation；P1；runtime/owner.py、errors/catalog.json、commands.json | 原WorkflowError兼容接CommandError，静态安全code/field/remediation/exit，保构造/内部payload；补真实现存未声明code及直接命令声明，定点标readiness_result_id/pr_body |
| P856-3 | implementation；P2；runtime/owner.py、invoke.py、check.py、record.py、execute.py、recover.py、migration.py | 五entry引用单一package私有unknown边界；保原CommandError，unknown静态70；migration去str(exc)/fixed3但不改route/事务。shared command/io不改 |
| P856-4 | implementation；P2/3；package全套tests与runtime定向tests | 补migration错误码、安全unknown、内部route、同事务动作和既有合法恢复覆盖；按实际consumer检出缺口，执行第3节集合 |
| P856-5 | 原RDT owner；真实工程结果与第6节完整拟写 | 在隔离贡献准备实际差额，final_integration合完整current并读回，不直接逐Issue登记README；原Architecture按无影响轻量route确认，无空ADR |
| P856-6 | 原guru-upgrade-tools；完整matching canonical及其public source pair；当前专用checkout | preview→AI gate→精确写集展示/必要确认→prepare一次→invoke同plan→target原生/source-installed/drift验证。保Task/session/peer；不得手抄受管副本 |
| P856-7 | implementation及原quality owners；上述工程/知识/安装结果完成 | 重读全部after，TaskCommit前展示真实提交范围并按原边界执行；固定完整B..H和dirty增量，committed candidate/begin_check后一次独立完整Review。未授予commit/push/PR权限 |

每批写前运行 `bash .trellis/guru-team/scripts/bash/check-task-checkout-boundary.sh --json --task .trellis/tasks/11-15-856-publication-error-boundary`，保持并行内容。单一source文件不超过3000行；本次原owner约816行，仍需核最终实际长度。不存在需额外维护的临时功能限制。

## 3. 验证入口、输入与预期观察

以下均为计划，不预填pass。工作目录为本Task checkout，产品Python测试通过已安装managed resolver，不以PATH Python依赖结果充证据。

```bash
PYTHONPATH=trellis/skills/guru-team bash .trellis/guru-team/runtime/resolve-python.sh "$PWD" "$PWD/.trellis/guru-team/runtime" -m unittest discover -s trellis/skills/guru-team/packages/guru-publish-task-delivery/tests -p 'test_*.py'
PYTHONPATH=trellis/skills/guru-team bash .trellis/guru-team/runtime/resolve-python.sh "$PWD" "$PWD/.trellis/guru-team/runtime" -m unittest discover -s trellis/skills/guru-team/runtime/tests -p test_io.py
PYTHONPATH=trellis/skills/guru-team bash .trellis/guru-team/runtime/resolve-python.sh "$PWD" "$PWD/.trellis/guru-team/runtime" -m unittest discover -s trellis/skills/guru-team/runtime/tests -p test_command_receipts.py
bash .trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
bash .trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
git diff --check
```

V856-1至4按design第8节建立长期独立行为断言：正式invoke分别缺readiness_result_id与Closes #435→2/3和原定位；JSON `{`→invalid_json/input/2；适用direct entry、migration／legacy错误边界、known external4和unknown70→安全三字段；原stateful正常发布、same-plan恢复、typed exits及输出丢失→零重复动作。原test_transaction、test_early_draft、test_remote_recovery、test_delivery_migration、test_current_transaction_migration、test_json_carriers与test_legacy_maintenance均在package集合，不能以两例替代。

V856-5的installed校验与drift在实际tools同步后执行；source先证明canonical结构。核code与commands/catalog闭合、平台投影bytes/mode、受影响文件可执行位、递归.new/.bak及原owner disposition。原命令首个失败、exit/stdout/stderr和后续纠正分别报告，不把receipt运输成功当semantic pass。

工具同步的完整源入口为 `trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/{preview,prepare,invoke}.sh`。install输入明确profile=install、实际source_ref、dependency_mode=local_candidate、checkout=本专用worktree；source_ref在执行时固定当前完整canonical HEAD，dirty增量保持原owner的isolated local_candidate边界及unverified=[formal_fork_source_lock]。从该完整源的Fork lock取得真实CLI/Core package roots与public maintenance API，不伪填路径/版本。preview传 `--root . --input <实际install JSON> --upstream-source <实际matching source JSON>`；AI核未完操作、peer/指针、全部managed差额及AGENTS custom决定后，prepare一次冻结原public plan；invoke使用同input和 `--plan <原frozen public plan>`。未知preimage先由原owner解决；不使用apply的legacy blocker扩大迁移，不手改manifest/hash/pointer。

由于冻结写集和运行时差额只能由届时preview产生，当前不虚构其operation ID、per-path决定或授权。执行前原tools owner必须展示实际目标/源/命令/写删除集并取得该实际写入所需确认；这是原工具副作用边界，不是Planning形式化确认。target resolver、installed/native entry、peer/common指针和Task/session保留都需真实验证。仅当实际修改需要证明当前版本可干净安装时，执行最多一个代表性clean throwaway；否则以本checkout的定向tools同步/reapply验证，不执行clean throwaway。本Task不执行完整多平台Release矩阵。

## 4. 停止条件与适用回退点

- source、scope、key/phase/root或有据机制改变时回原Clarify/Author/Architecture；不重建Task/Delivery或改B追赶无关main。
- 已知code缺少consumer依据、真unknown被错误归类、内部route被提前截断、敏感sentinel回显、退出码不符或副作用重复时停止，回本package implementation修复；不降低断言。
- tools无matching public API、未完重叠事务、managed冲突/.new/.bak、peer改变或source不符时由原tools owner处理同操作恢复，不自行重prepare、手改checkpoint或运行全迁移。
- 保留用户与其他Agent改动，不用reset/revert整体回退。无本Task数据库/数据迁移或真实发布动作，故无新增业务回滚协议；已有发布未知结果仍由原owner先回读同事务。
- 足够工程/范围证据后停止追加可选实验。设施反复失败先重评复现入口并保具体缺口，不无限修设施、重复红绿或声称覆盖目标行为。

## 5. Delivery Policy（唯一）

**full**：D1承担根accepted_scope AC856-01至06、本批D1-R1至06全部责任，包括known分类、全部实际直接入口的最小覆盖、内部typed recovery、同事务零重复、unknown70/脱敏、catalog一致及实际定向分发。没有已知延期到D2的实现范围。

本批完成条件是原Delivery门禁与实际交付事实均成立；Task Completion另外比较全scope和真实证据，不因full、合并或fixture绿色直接完成。历史G10首次异常、旧Draft及真实业务生产效果的未验证边界保留，不制造真实重放义务。新scope或独立延期须回Clarify和Creation原路径，不能只改Policy标签。

## 6. Docs SSOT Plan（唯一）

strategy为 **delta_first**。原writer是guru-maintain-requirements-design-test-ssot，直接consumer为实施/独立committed Review及后续Readiness/Completion。隔离贡献位置为 `docs/requirements-design-test-contributions/856-publication-error-boundary/`，只在原owner确认实际知识差额后写真实内容，不先建空manifest或第二current。

命中单元是RDT-REQ-LIFECYCLE／R713-03和R531-05、RDT-DES-LIFECYCLE／D713-03及Delivery Review/Publish/Merge、RDT-TST-LIFECYCLE／T713-03和T531-05。补Publish具体已分类错误/安全unknown、同事务恢复与定向公共入口验收；保原source/typed exit/Refs-only/Closure和历史观察。JSON-input R695/D695/T695保持既有读取合同，只引用，不无因扩改。具体canonical路径见prd第7节。

原RDT owner按完整current-knowledge读取真实current及仍有效关系，在实施和工程自检后、TaskCommit前final_integration整合完整定义并实际readback；TaskCommit纳入全部after，独立committed Review验证真实before/after。方案规划不先写共享current/README或贡献链审计。Architecture候选为no-impact，故无空贡献/ADR；若实际shared协议/owner/状态变化则回原Architecture重新评估，不沿用该结论。
