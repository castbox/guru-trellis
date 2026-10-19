# D1 提前 Draft 实施与验证计划

## 1. 输入与引用

读取整体 `../../prd.md`、本批 `prd.md` 和完整 `design.md`。design第3节是唯一来源设计处置；§1给出固定B、H0和PR目标；§5-7拥有本批接口、顺序和迁移差额。D1无前序，整体范围保持AC636-01..10。

必要canonical输入为 `trellis/workflows/guru-team/workflow.md` 的Phase2/3、Continuation与typed consumer，原TaskCommit/Publication/BranchReview/Check/DeliveryReview/Merge package的完整当前SKILL与contract、实际interface/schemas/consumer，以及`runtime/delivery_projection`与`.trellis/delivery-contract.md`的原API边界。不得从摘要或旧安装推断当前行为。

读取 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 的身份、固定候选、质量、发布、Refs-only及整体收尾；Architecture `.103`、constitution v1、change contract v1、ADR-024/028/030和本批真实contribution/ADR候选。工程约束读取 `.trellis/spec/workflow/companion-scripts.md`、`quality-guidelines.md`的Validation Scope Ownership与Test And Validation Value、`skill-package-contract.md`的Public Skill I/O And Private State、`subtraction-first-compatibility.md`和完整写作规范。上下文manifest只定位这些实际文件，不复制规则。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原责任 | 实际文件/改动与完成观察 |
| --- | --- | --- |
| I636-01 | 当前Planning经Wording、fresh final_plan、Approval及当次计划接受/Activation | 原Author完成本planning_root三份正文和official implement/check JSONL；唯一D1被激活，保留整体accepted_scope |
| I636-02 | I01；独立implementation子Agent负责canonical TaskCommit | `trellis/skills/guru-team/packages/guru-create-task-commit/`：新早期独立闭合profile/输出、candidate2.0与原精确executor/receipt投影；现有最终Check路径保持。受影响tests覆盖无Check真实commit、精确stage、clean恢复及不冒充最终committed |
| I636-03 | I02的早期DTO；同implementation owner负责原Publication | `guru-publish-task-delivery/`：Draft publish、return-to-Draft、原same-plan恢复和新2.0事务；ensure_draft在push前，Draft终态不写PublicationFact，Ready仍current gates；旧事务一次性迁移不执行remote动作 |
| I636-04 | I02/03接口明确；同implementation owner负责原审核/编排 | `guru-review-branch/`早期profile；`guru-check-task/`、`guru-review-task-delivery/`、`guru-merge-task-delivery/`只同步实际命中的契约/consumer与验证对象，不重构未受影响逻辑。canonical workflow显式调用和唯一feedback router；continuation/rework保持各phase原owner |
| I636-05 | I02-04；原RDT/Architecture作者按各自范围写入 | `trellis/presets/guru-team/MIGRATION-636.md`、两个workflow/preset README、根导航中实际命中说明、RDT task-owned contribution及必要canonical delta、Architecture task-owned contribution/ADR候选。完整拟晋升内容进入独立Phase2评估，shared-current只由原owner写，不提前实现#638 |
| I636-06 | 可审查candidate已形成且最小自检完成 | 经原TaskCommit准备具体早期提交计划，得到当次确认后提交；原Publication展示确切remote计划，确认后创建真实Draft。不得直接git commit/push或gh创建PR，不能为本仓尚未安装的新入口伪造pass |
| I636-07 | I06 Draft存在 | 独立早期内容审核子Agent与风险验证并行，在同固定B/H产出分离结果；有finding回原implementation修复，同PR Draft更新；Ready往返及输出恢复按具体真实副作用边界执行 |
| I636-08 | 实际源码/文档候选完整；原Architecture/RDT维护 | 完整preset同步dogfood：`trellis/presets/guru-team/scripts/bash/apply.sh --repo .`，逐项处理sidecar；独立Phase2 Architecture评估拟写内容，原owner晋升/判断实际写入，随后独立Check覆盖最终候选和全部AC |
| I636-09 | I08正式Check；原最终提交/Review/Delivery/Publish/Merge | 必要最终commit后依原router取得当前Check，fresh独立committed Architecture与完整BranchReview；readiness/Ready；具体Merge gate后另请合并授权。合并后整体Completion、Closure、Finish、适用Cleanup；不启动#637/#638 |

I02-05的执行由独立implementation子Agent承接，主Agent协调原owners；独立Check、Architecture和BranchReview不能由implementer自报通过。各子Agent先完整读写作规范和自己实际context，保留其他人的修改。官方context validator已指出写作规范、workflow及三份长spec会超过注入上限；dispatch必须要求子Agent自行完整读取写作规范和任务命中的条款及关联条件，不能把被截断注入当作完整加载，也不修改全局注入配置。新增/实改非generated代码文件不得超过3000行；若命中则在当前责任范围机械拆分，不顺手重构。

本批新公共能力必须先在隔离matching安装里验证；用于本Task真实早期提交/发布时，必须按原升级/重apply owner把完整匹配源码安装到选定Task checkout并核对新入口。这个本地安装不能替代正式Planning、Check或remote授权。若无法合法获得matching安装，则停在I06明确前提，不绕过公共owner。

## 3. 验证入口、输入与预期观察

所有命令从注册worktree运行。原owner按当前受影响文件选定测试，不跑完整Release矩阵。具体新增测试名由implementation写入真实结果；不能把下列计划当已执行。

| 验证 | 入口/输入 | 预期观察及对象 |
| --- | --- | --- |
| V636-01 | 最小自检：`git diff --check`；实际命中Python文件`python3 -m py_compile <files>`、JSON/schema验证；TaskCommit/Publication新早期入口定向tests | 无完整Check候选被原早期owner真实提交；无敏感内容、精确paths、实际HEAD和中文消息明确。正文列完整质量待完成 |
| V636-02/03 | `python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task-commit/tests`；Publication同路径的`tests`；新增正常Draft/Ready事务与stdout-loss恢复cases | early/final两种输入闭合；同commit/PR恢复，Draft前置push顺序与状态读回，旧gate不放行new HEAD；失败不假通过 |
| V636-04 | BranchReview/Check/DeliveryReview/Merge命中tests；`runtime/delivery_projection/tests`；固定B/H独立Agent与HEAD验证并行，fixture target前进/冲突/无merge ref/CI未触发 | 内容审核和HEAD命中检查推进；HEAD H、target T、组合M分别呈现，组合失败/SKIP/未执行有具体条件。正式full_review仍真实Check predecessor |
| V636-05/07 | family/public-contract-graph与旧事务迁移tests；`python3 -m unittest discover -s trellis/skills/guru-team/tests`，再运行受影响owner migration tests | refs-only、完整gate/最终public fact保持；在途各phase及成功历史保留，无runtime双读、伪造gate或重复mutation |
| V636-06 | `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`；`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`；preset中platform inventory、runtime native compatibility、installer/reapply/managed text与本次命中sidecar tests | canonical/installed/dogfood和声明平台入口一致；`.new/.bak`逐个给出处置及actual安装结果，不以源码同步声称业务链通过 |
| V636-01..04实际链 | 受支持公共TaskCommit和Publication wrapper；同一`castbox/guru-trellis` Task/Delivery/PR，按每次展示计划授权；独立Agent经实际BranchReview早期入口和命中HEAD命令 | 首次真实Draft先于完整审核/重型检查；同PR真实修订、Ready→Draft→Ready及正常输出丢失恢复分别记实际结果。未能真实执行的条款必须标未验证，不能仅用fixture闭环 |
| V636-09最终质量 | 官方 `task.py validate <task_ref>`；原Check、fresh committed Architecture、完整B..H BranchReview、readiness/Publication/Merge与整体收尾公共入口 | 全部适用证据覆盖实际候选；无P0-P3未解finding；真实live结果与静态结果区分；最后整体Closure而非PR body关闭#636 |

业务Mongo/Redis/race/全量编译不是本repo新增工具义务，也不是所有Draft统一前置。本Task完整命中验证仍须Draft后完成。BackendCI入口缺失不能伪装成功；本项提供明确HEAD调用/候选合同，不改业务CI。只有确需证明clean安装且定向验证不足时，最多增加一个代表性clean throwaway，原owner先说明触发依据；不扩展全平台/Release矩阵。

## 4. 停止条件与适用回退点

- 缺current Task/Delivery、accepted Planning、固定B或原owner合法phase：回原identity/binding/Planning/phase owner；不创建替代Task或直接改task.json。
- 实际机制改变、出现scope/authority冲突：停止受影响写入，回Author/Architecture或Clarify；不以旧candidate评估放行新机制。
- 定向测试失败、敏感内容、未分类paths或HEAD变化：由原implementation/TaskCommit修复和fresh prepare；保留无关dirty，不reset/stash/amend掩盖结果。
- 远端副作用成功但输出丢失：原Publication先回读原事务实际状态；不重复PR、空提交或强推。新动作变更先fresh preview；历史成功不证明当前gate。
- matching install、官方API或真实外部入口不足：保留源码与证据，报告精确缺口和依赖；不改Trellis上游/全局包、不另开故障Issue、不绕过公共owner。
- preset产生sidecar：停在该文件原安装/冲突处理责任，不覆盖用户内容。迁移前保留原owner有界backup；恢复/回退只针对本次安装的精确write set。

本批不改数据库或部署，无生产回滚协议。GitHub Draft/Ready的正常恢复按design §6；PR关闭、branch/worktree删除和merge各保留独立具体边界。

## 5. Delivery Policy（唯一）

`full`。唯一D1完整覆盖R636-01..07和AC636-01..10；没有预先延期的#636责任，没有待#637/#638实现才能交付的接口。完成条件是原owners承接的早期真实Draft、同PR更新与状态往返/恢复、分离的审核/验证对象、最终完整gates以及迁移/分发证据全部成立。没有延期项不表示验收已通过。

本Delivery合并后仍须整体Completion逐项核对全部Task要求及实际证据，再Closure/Finish/适用Cleanup。真实验收缺口必须回原Completion/implementation补齐，不能用一次Merge或测试数量代替。用户当前只处理#636，本项结束后由用户决定后续工作。

## 6. Docs SSOT Plan（唯一）

strategy=`delta_first`。原RDT维护owner承接本Task隔离贡献，完整差额覆盖早期commit/Draft入口、原final gates、Refs-only/Closure、候选对象、同操作恢复与matching迁移。命中canonical为 `docs/requirements/current/task-delivery-lifecycle.md`、`docs/design/current/task-delivery-lifecycle.md`、`docs/test/current/task-delivery-lifecycle.md`；版本导航/索引只由原owner按实际完整targets推进。Test唯一记录命令、真实Agent/GitHub结果和未验证边界，不在三处复制测试结果。

Architecture原owner消费本planning_root真实contribution与ADR候选，原独立Phase2评估完整拟晋升内容；原owner依据写前live expected-current晋升并判断实际写入适用性，再进入最终Check。ADR候选只窄替代ADR-024/current流程中“所有提交和Publication必须在最终Check/readiness之后”的时机片段，保留上游身份/phase/full_review predecessor、ADR-028/030和整体Closure职责。不能通过本批提前实施#638。

直接consumer为独立Check、committed Architecture/BranchReview、DeliveryReview、Completion和Finish。canonical workflow/preset/package合同同步后经完整preset reapply，installed/dogfood只作为投影。旧时机文本若失去唯一current consumer，在本Task删除/替换并从current导航退出；不可变历史ADR/归档保留来源说明，不能成为current fallback。所有delta在最终Phase2前reconciliation/promotion，无后置“补文档commit”循环。
