# D1 提交后一次独立完整语义审查：实施与验证计划

## 1. 输入与引用

本批完整承担根 `prd.md` R1–R7 与本批 PRD D1-R1–R7；没有前序 Delivery。固定 B/H0 为 `4d565c97b5abf634d76ede2d18eed0a57f13bb76`，PR target 为 main。唯一来源设计处置位于 design 第3节；本文件不复制。实际 candidate_assessment 为 architecture_impact/target_native，最终方案仍须经 Wording、独立 final_plan 和 Approval。本轮停在规划，以下均为后续执行计划。

实施前完整加载以下输入及关联条件：design 第4–7节的 owner/I/O/状态/迁移；`.trellis/delivery-contract.md` 的 roles、Candidate、result/rework/recovery；原 Author 的固定区间合同；Architecture contribution 与必要 ADR 候选；`.trellis/spec/workflow/workflow-contract.md` 的 Candidate Applicability And Coverage；`quality-guidelines.md` 的 Test And Validation Value/Validation Scope Ownership；`subtraction-first-compatibility.md`；各命中原 Skill 的完整当前合同、interface 及 consumer。安装正文 `clear-technical-writing.md` 适用于实现说明与全部新文本。

官方参考为 `https://docs.trytrellis.app/index.md`、`https://docs.trytrellis.app/advanced/custom-workflow.md`、`https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`。沿 Markdown/workflow/preset 扩展，不改上游源码、npm 全局安装或 hooks。原 `trellis-meta`、`trellis-before-dev` 与 package spec 在实现开始时加载；规划不代替实施入口。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 依赖、原责任与具体文件 | 行为、可审核产物与完成观察 |
| --- | --- | --- |
| I1 合同切换与退休边界 | 已激活本批 Planning；Author/原 workflow owner；`trellis/workflows/guru-team/{workflow.md,references/routing.md}`、`trellis/presets/guru-team/MIGRATION-794.md`、design第5节各 package interfaces | 在 Markdown 明确新顺序、双role同owner、原typed consumers和旧profiles退出；列出当前全部Check/Review/early Draft实际consumer、匹配版本、已执行/pending处置；不先改狗食或公共Task记录。完成后每个真实出口有唯一consumer，版本无碰撞 |
| I2 精确待审提交 | I1；原 `guru-create-task-commit/{references,runtime,schemas,examples,interface.json,commands.json}` | 新pre-review commit/clean reentry和最小output；复用exact executor/hook/路径与同提交恢复；移除Check和early Publication前置/consumer。V1/V4证明无先验Check可产生真实待审commit且clean reentry无新提交 |
| I3 提交前知识整合 | I1；原 Architecture/RDT packages；`runtime/invoke.py`及promotion/target读回实现、schemas、contracts；共享current-knowledge | 新版本移除独立candidate Check/phase2 Architecture先决，保留Planning/工程/完整targets/expected-current/readback；新增明确pending-review事实；不将未审内容标成reviewed_promoted。V5证明合法整合后可提交、冲突仍回原owner |
| I4 单一完整独立审核 | I1–I3；原 `guru-review-branch`、`runtime/delivery_projection/gates.py`及必要adapter；原 `guru-check-task`当前开发职责 | 迁移九维、qualifier适用性、Architecture authority-first、工程采用、full range、findings、scope/planning回程；一次判断顺序record真实check/full_review，同候选缺步恢复；当前Check开发profiles和重复checkpoint退出。通过V1/V3/V4和原回归；不造pass、账本或reviewer流程字段 |
| I5 全体后继与Reconcile | I4；原 `guru-reconcile-task-base/runtime/{project,execute}.py`、Review continuity/alignment、Delivery Review的readiness producer、Publication的draft/migration及ready/readiness consumer、Merge/Completion/Finish实际命中contracts | require_current_check/phase2 anchor迁到新candidate语义；不缩B..H，覆盖冲突及未改consumer；Delivery Review记录readiness，Publication只消费并发布；early Draft pending远端动作回当前审核/readiness，已完成动作准确恢复；保留#775 rollback和终态结果。V2–V4与完整graph无旧强制前置 |
| I6 完整知识候选与文案 | I4/I5实际差额明确；原RDT/Architecture writers；第6节列明targets和本Task隔离proposed | 把当前活动定义与本次新规则整合成完整单元，准备ADR窄替代和引用；保留历史原观察，不逐Issue登记共享根或索引。此处准备完整拟写，真实晋升沿当前合法owner边界，不能用源码变更强行让本Task旧阶段通过 |
| I7 matching采用和行为证据 | I2–I6定向行为通过；原 `guru-upgrade-tools`；canonical overlays、README、受管inventory/mode/sidecar配置 | 先按MIGRATION-794判断本Task实际旧阶段，沿原工具完整更新保留全部Task/session/journal/用户内容，逐个处置sidecar；验证source/installed、Codex/Claude及命中平台、重应用与drift。V6实际新reviewer及后继行为另做，不以静态投影替代 |
| I8 工程自检与正式交付停点 | I1–I7；原实现协调者及当前适用workflow owners | 汇总真实工程结果、docs实际after和未验证范围。按本Task实际所选完整provider完成合法审核/本地提交边界。Git/GitHub副作用沿原owner的具体对话边界执行，merge交协调者处理。不得修改其他Task或主checkout的#796工作 |

每步只修改本Issue直接影响文件。任何命中非生成源码超过3000行时，先由原 owner 判断机械拆分或小型解耦，不把上限当截断功能理由。脚本执行事实，不决定scope、pass、route或Issue关闭。无授权信息写入tracked或runtime状态。

## 3. 验证入口、输入与预期观察

V1–V7 的行为条件、输入、断言和证据限制在 design 第8节。本节安排实际入口与顺序；所有结果均待执行，未预填pass。

1. V1/V4：用受管Python运行 `trellis/skills/guru-team/packages/guru-create-task-commit/tests/` 的happy path、committed reentry、early draft/migration与新pre-review cases；Review的runtime、tree identity、candidate reuse及新双结果缺步恢复cases。测试须调用新公开invoke/原executor并读取真实Git/API结果，不能先注入新Check来让链通过。
2. V5：运行原 `guru-maintain-architecture-baseline/tests/test_promotion.py`、`test_contract.py` 与 RDT `tests/test_contract.py` 的受影响覆盖，并补新integration pending-review和committed before/after。由正常recorder/executor产生targets与gate事实，核实before/after真实读取和未审发布阻塞。
3. V2/V3/V4：运行原 `guru-reconcile-task-base/tests/{test_runtime.py,joint_resolved_flow.py}` 与 Review candidate reuse/continuity、Publication draft/migration/runtime和Delivery Review受影响tests。外部GitHub边界用可观察的调用替身；无需实际push/PR即能证明本地gate是否阻止远端executor。不能将替身结果写成真实外部完成。
4. V7：运行 `trellis/skills/guru-team/tests/test_delivery_contract_graph.py`、`test_delivery_family_integration.py` 和命中packages的contract/eval。用matching provider的 `discover-skill-contract.sh --root . --mode source --skill <实际producer> --exit <实际exit> --json` 及installed模式取得真实consumer，核对新投影、旧路径退出和 unknown/unmapped正常错误。按实际差额执行Python语法/静态检查和 `git diff --check`。
5. V6：原workflow/Review owner用新公开入口在隔离throwaway执行真实提交对象审查：首次新独立reviewer；真实finding修复后的同reviewer后继；影响无法界定或原覆盖不可得的补足路径。base冲突/消费者缺口验证复用同一场景时，必须具有独立检测价值。记录真实读取/判断/原stdout和未覆盖边界于当前会话及唯一Test贡献，不建立通用Agent评测器、固定审查轮数或数量门槛。只在发生机制实质变化时刷新受影响qualification/Architecture。
6. V7：已有checkout使用原 `guru-upgrade-tools` 完整源合同，不直接运行会破坏任务前提的apply。安装后运行 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`，以及原owner指定的定向mode、sidecar/reapply、source/installed/platform检查。若受影响clean安装路径尚无可靠证据且本次accepted scope依赖该证据，最多补一个代表性clean throwaway；不做全平台矩阵。

实际Python命令从对应package README/commands或原受管runtime入口确定，执行前读取参数。现有测试仍适用则采用；补新增行为和失效前置，不为锁定常量、文案或fixture新增重复断言。测试先后由风险和成本决定；无需固定红绿、回退旧版重复或完整无关生命周期重放。

## 4. 停止条件与适用回退点

- 缺上游公开能力、固定B/当前key不一致、来源实质变化：停止依赖步骤，回原Identity/Ensure/Clarify/Author。不能改Task身份或手填候选摘要解阻。
- 新机制偏离candidate_assessment：回Author形成当前候选并刷新受影响Architecture/qualifier；普通实现细化不重复访谈。
- 旧事务待执行动作或旧gate缺必要语义：按design第7节回原producer/迁移owner，保留真实已执行事实；不重复远端动作、不跨读旧private状态、不转换pass。
- 当前expected-current或sidecar冲突：原维护/安装owner重读和判断，不能覆盖用户/其他Task内容；部分操作按同intent仅补未冲突pending。没有新的数据库或服务迁移，因此不新增数据回滚协议。
- 验证失败：判断是否到达声明行为，再修复实现或测试设施；设施反复失败时缩到能回答同一问题的入口，或明确未验证缺口。必要验收缺口未解决不得通过。达到V1–V7所需充分证据及受影响回归后停止追加实验。
- 不revert并行改动、不清理共享journal或其他Task资源。规划不建立Activation、实现或交付结果。

## 5. Delivery Policy（唯一）

策略为 `full`。本D1交付根R1–R7全部能力：新链、完整职责、知识/提交/上游双结果、后继/base、early Draft和旧gate迁移、真实consumers及受管采用。没有延期必需实现，没有前序输入，也不预留本Scope内的后继Delivery。

独立交付条件：V1–V7覆盖的真实公开入口可运行；当前安装图无重复Check或审核前发布边；旧支持域有明确恢复/处置；当前文档与代码/测试一致，必要dogfood/platform采用有证据。未执行完整多平台升级/Release矩阵是本Task明确边界，不是隐藏实现延期。

当前剩余工作是本计划全部实现、验证和原交付阶段；本轮没有完成这些事实。D1 merge不等于Task完成。Task整体Completion还须核完整accepted scope和全部真实结果，随后原Closure/Finish完成终态。原Task owner持续承担剩余责任；任何merge交协调者处理。

## 6. Docs SSOT Plan（唯一）

strategy=`delta_first`。先在本Task隔离贡献准备完整proposed targets，由原RDT/Architecture owners在本Task实际适用provider的合法integration边界分别晋升/readback，再使真实after进入候选与完整审核。若采用新链，提交前整合为pending-review，提交后一次独立审核才形成真正通过；本Task自举不能直接借新文案豁免旧安装的门禁。

| 权威/实际target | 本轮差额 | 原writer、直接consumer和时点 |
| --- | --- | --- |
| `docs/requirements/current/task-delivery-lifecycle.md` | 保留身份/范围/终态；窄替代重复Check和早期发布，定义R794与正常迁移/覆盖行为 | 原RDT writer；Author/Review/Delivery Review/Completion消费完整当前定义；最终实现提交前合法整合 |
| `docs/design/current/task-delivery-lifecycle.md` | 原Review双role、真实双结果、提交/integration/reconcile/recovery与新版本projection | 原RDT writer；实现/审核/发布consumers；与requirements/test同批readback |
| `docs/test/current/task-delivery-lifecycle.md` | 现有T530/531/600/636/637/638/713真实替代边界和T794行为入口；唯一承载V1–V7实际观察及缺口 | 原RDT writer；原Review/Completion按实际结果采用，不复制pass表到其他文档 |
| `docs/{requirements,design,test}/current/knowledge-maintenance.md` 中实际命中单元 | 去除提交前独立candidate Check循环；保留完整拟写、原writer、expected-current/readback和历史边界；R710正常语义authoring、完整结果消费/恢复及R711完整单元/局部导航义务迁入实际新消费者 | 原RDT writer；知识maintenance与Review；实施前读取完整命中单元并核target集合；历史专项次数不变为本批验收 |
| `docs/architecture/06-governance/change-contract.md`、实际命中的DOMAIN/GOVERNANCE完整单元、根README自身维护时机段 | 新时机、两role同owner、pending与真实review状态、范围/恢复、early Draft退出；九concerns/descriptor identities保留 | 原Architecture owner；Planning/Review/Publication/Finish；本Task贡献准备完整拟写后沿原promotion入口整合 |
| `docs/architecture/adr/postcommit-independent-review.md` | 从本Task真实ADR候选晋升，窄替代ADR-KNOWLEDGE-FINAL-INTEGRATION/033，保留028/034 | 原Architecture owner；当前change-contract和受影响引用直接消费；不逐项更新共享ADR index |
| `trellis/presets/guru-team/spec/workflow/{workflow-contract,quality-guidelines,companion-scripts,skill-package-contract}.md` 的真实命中条款；workflow/preset READMEs、MIGRATION-794 | 删除活动重复门禁、旧Check producer与早期发布边，写新版本/恢复及验证界限 | 各canonical原owner；runtime/AI/installer消费者；canonical改后由原tools owner同步dogfood/平台 |

没有无内容贡献、共享导航登记、全局版本递增或授权记录。共享入口只在自身合同确实变化时维护；历史归档、原始日志与已封存证据不重写。正式审核判断实际完整定义、代码/测试及采用证据；不能从文件存在推定晋升、安装或业务效果。
