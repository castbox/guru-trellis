# D1：活动任务续接与迁移残余合同收敛实施计划

## 1. 输入与引用

整体Task根prd.md与本Delivery prd.md承载完整F1–F6/R1–R7/V1–V12。实施先读design第3节唯一来源设计处置及第4–8节实际行为，不复制处置矩阵。已取得真实Architecture candidate_assessment：target_native / architecture_impact / baseline_current；后续仍须Wording-current final_plan与Approval/Activation。

必要来源为canonical workflow的Bound formal continuation、created consumer、scope clear-router和Workspace boundary；Creation/Discovery/Review/verifier/Clarify的当前Interface/Skill/reference；shared composition的初始恢复；Author planning-body及本批design/implement模板；current RDT生命周期完整单元；Architecture constitution、change-contract、ADR-011/023/024与本批真实contribution/ADR候选。关联条件须实际读取，context链接不能替代加载。

本批起点为main `319202beab79c7666ecdb855291bf117e43d407e`；D1无前序。固定Trellis source-lock `e9fb95fd2eb0fb8441153e77384a9dfd3ea3358f`，其matching实际Core/CLI来源、构建和运行版本须在native样本现场核验，不能从旧日志推定。B与PR目标分开，采用design第1节固定B。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 依赖／owner | 实际文件与行为 | 完成观察 |
| --- | --- | --- | --- |
| I1 | 当前Planning/Approval/Activation完成后，实施owner | 每批先check-task-checkout-boundary；读当前canonical和必要official扩展文档，保留并行dirty | 当前Task/gen/binding/cwd真实一致；不凭旧created取得准入 |
| I2 | I1；workflow/原Skill owner | 修改trellis/workflows/guru-team/workflow.md的普遍created、created consumer、scope旧clear路径；同步原create-delivery Interface/Skill/reference对consumer实际阶段的说明和明确matching迁移 | initial/current边界与pre/post scope分开；created wire及初始validator不变 |
| I3 | I2；各原package owner | Discovery Skill/reference及managed skill-package-contract身份/status段；Review Interface；verifier Skill/reference诊断；workflow/data/companion spec旧scope段 | F1–F6的current指令同义，pinned-old明确版本，原validator严格条件保留 |
| I4 | I2–I3；测试owner | 在原Creation、shared lifecycle、Discovery、Review、verifier、Clarify scope测试扩展正常场景；记录完整caller→consumer→owner输入与观察 | V4–V6、V8–V12确定性层可定位；不造伪造artifact负例，不用exit名代替行为 |
| I5 | I2–I4；原生测试执行owner | 使用下节一个matching installed/native样本，真实Agent做clone续接、正式rebind>0、原阶段写入、selection和scope消费 | V1/V2/V7及V11/V12实际Agent层独立成立或准确blocked；fixture不冒充 |
| I6 | I2–I5；分发owner | 通过canonical preset apply/reapply同步dogfood、platform及managed spec，核ownership、drift、mode和sidecar | source/installed内容与声明一致，所有.new/.bak逐项处理；不改业务现场 |
| I7 | 完整实现/隔离proposed targets；原Architecture/RDT owner | 在原docs贡献目录形成完整requirement/design/test/traceability及Architecture命中完整单元，独立candidate Check后final_integration/readback | 不在Planning直接写shared current；真实新增after回implementation重新candidate/begin_check |
| I8 | I7；原Check/TaskCommit/Review/Completion | 最终Architecture/Check覆盖实际candidate，后续精确提交和完整独立Review、Delivery与Task Completion各按正式合同 | 当前证据绑定真实内容，未验证边界分层报告；合并不等于整体完成 |

I7的RDT贡献由原RDT writer拥有；Architecture贡献及必要ADR已是非空task-owned候选。正式共享ADR编号与目标由原Architecture owner查重选择。任何额外Git/GitHub副作用仍按当前明确边界处理。

## 3. 验证入口、输入与预期观察

以下均为计划，未预填pass。测试owner以当时真实匹配环境执行并保留首次失败与原结果。

### 3.1 原package/runtime定向入口

- `python3 trellis/skills/guru-team/packages/guru-create-delivery/tests/test_contract.py`：正式create/select/输出丢失、四个已前进phase、planning对照；必须让真实consumer后续交原owner，不能只assert created。
- `PYTHONPATH=trellis/skills/guru-team python3 -m unittest discover -s trellis/skills/guru-team/runtime/task_lifecycle/tests -p 'test_composition.py'`：V6初始Creation精确恢复及V5合法mismatch。若该入口需要现有managed interpreter，先用原resolve-python，不改产品来迁就系统Python。
- `python3 trellis/skills/guru-team/packages/guru-clarify-requirements/tests/test_delivery_scope.py`：V3/V12 pre/post scope_ready2.0、真实AuthorityRef、三种scope_action、有/无current Delivery及stage合法操作。
- 原Discovery、Delivery Review与verifier目录的现行`tests/test_contract.py`或声明runtime测试：分别V8真实active绑定/上下文、V9真实Review candidate及readiness refresh、V10旧输入诊断和合法standalone输入。不因本任务跑完整verifier矩阵。
- 对新增/实际修改模块执行其原contract/interface/schema消费者检查。只扩展与本次变更相关suite，失败缺依赖记环境blocked，不算pass。

可复用的现有正式样本入口还包括Bind `tests/test_portable_recovery.py`、Author `tests/test_planning_chain.py`、Check `tests/test_delivery_flow.py`；按当时真实目录执行。Completion旧native runner为schema1，不作为当前schema2原生样本入口。

V11至少一个原consumer→实际阶段owner隔离链；V12至少一个完整scope owner隔离闭环，三种disposition另有定向对照。V4无scope变化保留实际适用结果；V5通过正常ref不可取、正式binding/checkout错误或stale操作触发，不手改digest/authority伪造失败。

### 3.2 一个matching installed/native独立clone样本（V1/V2/V7）

1. 在临时本地测试repo A使用固定source-lock的matching实际CLI/Core和完整Guru apply，声明Codex入口。真实Agent通过正式入口形成schema2 Task/Delivery与可获取规划；只在测试repo内提交样本和tracked工具基线。该样本不发布远端，也不进入业务数据。
2. A的本地测试main须真实包含样本tracked基线，活动branch从同HEAD分出，使后续Rebind满足原prepare要求的current HEAD为selected base ancestor。不能对未入main的活动commit强行rebind落后main，也不能为了测试放宽validator。
3. `git clone --no-local --branch <明确活动ref> <A> <B>`形成独立common-dir。B只有tracked输入，不复制A的`.git`、私有runtime、session、ledger或created DTO。核实际CLI/Core/Guru来源、版本和安装指针，以同一个代表目标复用后继场景，至多一次代表性clean安装。
4. B真实Identity `delivery_active_task`解析明确TaskId/generation/source；Establish `action=establish`形成合法rev0及caller_owned ledger；由原Rebind record-plan生成真实`same_checkout_new_ref`方案，再执行同plan得到revision1。Ensure核唯一checkout，Bind `delivery_rebind_missing_session`或合法explicit-task入口继续。
5. 真实Agent读取current public phase及原合同，由实际Author或实施owner完成一次合法规划/实施写入。核同TaskId/generation/source/Delivery、revision>0、原历史/业务内容保存。缺created不阻塞；身份或phase本身不冒充semantic gate。
6. 在该matching安装复用明确已有Delivery selection及输出丢失入口，让created真实consumer读取phase后进入原owner；再用受控公开scope修订，经原Clarify→Author根PRD→Clarify acceptance→post结果→原stage合法rework/stop。实施阶段的scope修订由原`delivery_scope_revision`承接，implementing使用原`DeliveryProjection.revise_implementation_scope`后交同Delivery Author重新规划；其它阶段保留其原合法profile。原生样本至少覆盖真实消费，其余phase和disposition由上述定向fixture补齐并分别报告。

实际Agent不应接收预写通过结论。若缺匹配build、模型/CLI或正式owner执行能力，暂停对应层并报告准确输入/环境缺口，不以stub、手拼DTO、静态scanner或fixture补齐native要求。独立clone不要求再次完整发布/Finish。

### 3.3 分发与最终完整候选

运行`bash trellis/presets/guru-team/scripts/bash/apply.sh --repo .`，读实际.new/.bak/hash冲突后按原机制处理，再reapply检查幂等。运行`bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`、`bash trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh`及`git diff --check`；核声明平台投影、interface/唯一consumer/schema、wrapper执行mode和零未处理sidecar。只对本次受影响package/runtime/managed资产定向验证，不执行全平台Release矩阵。

原candidate Check和final_integration后，必须将真实共享targets、关系和导航差额纳入新的implementation candidate/begin_check，再final Check/完整committed Review。唯一Test记录source、deterministic、actual Agent、installed和外部层；规划时的命令、历史结果或知识晋升都不证明这些层通过。

## 4. 停止条件与适用回退点

必要ref/代码不可获取、Task/generation/binding/checkout不唯一或不匹配，停在原identity/checkout owner且写前不继续。原source selection丢失回Clarify，普通semantic输出丢失fresh重入原owner；已成功mutation输出丢失只由原producer恢复同一结果。

真实source/scope变化回Clarify→scope-only Author→acceptance；机制改变重入candidate assessment；Wording等义改动只刷新受影响门禁。native环境缺失保留实际验证缺口，不能删验收或补造pass。完整candidate/最终Check失败按原owner修复，未通过不晋升或Ready。

本批没有DB/业务数据迁移、远端发布或生产写入，故无新数据/发布回滚协议。源码退回仅处理本次明确文件，保留并行dirty；安装冲突沿原sidecar/旧版本原owner处置，不能reset或覆盖用户修改。初始Creation恢复validator不放宽。

## 5. Delivery Policy（唯一）

采用full。D1完整承担R1–R7/F1–F6及V1–V12，含actual installed/native独立clone、选择与scope消费，不把关键验证留给后续空Delivery。本批完整实现、分发、证据和RDT/Architecture实际差额通过原质量链后，才具备本Delivery交付条件。

当前没有独立延期的必要实现范围。未完成的native/环境证据仍是本批真实待完成项；不得改写为已经通过。Task Completion另审整个accepted scope、全部Delivery历史及外部边界，Delivery合并不自动完成Task。完整多平台Release、#649、业务现场采用不在本批范围。

## 6. Docs SSOT Plan（唯一）

采用delta_first。原RDT writer在`docs/requirements-design-test-contributions/657-workflow-continuation-conflicts/`维护真实完整requirement/design/test/traceability拟写单元，直接consumer为原RDT评估及最终整合；命中current生命周期requirement/design/test，补充created准入、phase consumer与scope两段的实际要求、机制、验证策略。实际结果由唯一test单写，不复制本方案为通过证明。

原Architecture writer消费本批`657-workflow-continuation-conflicts.md`及`657-workflow-continuation-routing-adr.md`真实候选，在原shared current命中单元及必要正式ADR中收敛011/023/024窄片段与旧Current Planning scope说明。constitution不变、既有GAP状态保留；没有空贡献、无consumer审计数据或无因全局版本递增。

Planning只写Delivery规划和task-owned贡献。implementation完成全部拟写正文后，原独立Architecture/Check先审完整隔离候选；由原owners在final_integration按live expected-current写共享完整targets并读回，implementation重绑全部actual after，随后最终Check/commit/完整Review。源workflow/package/spec及投影归各自canonical owner，不在共享导航复制step-local合同。最终报告明确工程、native、安装和未验证范围，不把当前源码采用推广为业务部署或Release通过。
