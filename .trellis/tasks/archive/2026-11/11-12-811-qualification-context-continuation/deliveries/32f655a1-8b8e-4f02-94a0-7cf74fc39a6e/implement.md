# D1 资格确认 context 接续实施与验证计划

## 1. 输入与引用

本批是全量D1，key为 `811-qualification-context-continuation/gen0/32f655a1-8b8e-4f02-94a0-7cf74fc39a6e`。
实际 planning_root 由原公共 current 解析。输入为根PRD的accepted scope、本批完整PRD和design；
来源设计处置只由design第3节维护。固定B/H0为 `ca0b21f0dfc754a6979f919be14deee696719a4b`，PR目标main。
本Task没有前序Delivery；#812结果已在B内，不重复实施显式key入口。

实施前加载以下完整适用条款和关联条件：

- live #811全文与本批PRD第4..7节：真实入口、三类context、两类确认、本项独立正常 Task/Delivery 验收和交付边界。
- design第4..7节，含第5.4节：模块职责、版本、producer→consumer投影、mutation refresh、共享Interface与迁移。
- `.trellis/spec/workflow/skill-package-contract.md`：Public Skill I/O And Private State、版本迁移、consumer/projection与分发。
- 五个受影响package的完整Skill/contract/Interface及shared消费者：原语义owner和公开调用，不能从测试fixture推断合同。
- `.trellis/spec/workflow/{workflow-contract,quality-guidelines,subtraction-first-compatibility,causal-completion-semantics}.md`
  的当前候选适用、Test And Validation Value、Validation Scope Ownership、直接演进和因果完成边界。
- `guru-upgrade-tools/references/contract.md`：完整source、preview/prepare、精确写集、副作用、同操作恢复及目标自身验证。
- `docs/{requirements,design,test}/current/{qualifier-applicability,local-fix-intake}.md` 与design第9节Architecture引用：
  原current关系及本轮差额；根PRD、历史ADR和前序观察不改成当前pass。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、原责任与文件 | 行为及完成观察 |
| --- | --- | --- |
| I811-01 | 已批准并接受的本规划；实施owner；五package/tests、shared消费者测试 | 先补V811-01..03中可廉价表达的身份/路由断言；建立Task/Delivery和受控外部gh边界，不预填qualifier/context/clear输出。审查实际entry/setup/observation以确认到达缺陷 |
| I811-02 | I01；normal/solution package runtime/common.py、schema、Interface、examples、原caller | 从已验证target投影确认output3；Task-bound携实际task_ref/key，非Task独立分支；classified/root输出不扩张；旧输入校验复用 |
| I811-03 | I02；Clarify/Discovery/Sync canonical runtime、schema、Interface、consumer/projection | 实现design第5、6节全部边，含bootstrap、authority/target分离、authority_duplicate_snapshot供原disposition、真实Issue mutation→refresh→Sync read→Discovery返回和独立clear；保事实校验、不创建语义脚本 |
| I811-03a | I03；shared schema及原runtime/installer/eval owners | 按design5.4新增普通Interface1.10、registry1.5、production manifest6、ordinary run5；Clarify/Discovery/Sync及registry、extension public_api/current manifest成套切换。discovery/validate解析consumer自有call-local声明及唯一authoring profile，installed保公开示例，installer复制新schema；ordinary runner/receipt consumers切5。无独立resolver，旧schema字节及qualification run3/4保持 |
| I811-04 | I03；各原Markdown writer；packages/SKILL.md/references、trellis/workflows/guru-team/workflow.md与references/routing.md、实际命中overlay、README | 更新mandatory路由和step-local合同，保持唯一consumer；补MIGRATION-811及新版示例；旧资产保字节、退出current引用，不建双reader |
| I811-05 | I02..04，含03a；实施owner | 执行V811-01..03、07及source package/graph检查；修复当前scope缺陷，检查每个改动非生成code文件≤3000行，超限按原规则机械拆分 |
| I811-06 | 当前完整canonical source与原tools前置；guru-upgrade-tools | 只读preview/prepare后展示本checkout精确source/target/命令/写删集；按原边界执行matching工具更新，保Task/session/peer；跑V811-04，逐个处理实际sidecar，不手抄受管副本 |
| I811-07 | 当前范围与有效公共链覆盖；原实施/caller owner | 按V811-05复核本项独立正常Task/Delivery的真实公共调用和后续消费；采用仍适用的原入口、日志和代码观察，只补实际未覆盖分支。不指定外部发布Task，不制造未决范围，不预填producer输出 |
| I811-08 | 当前完整实施与真实工程结果；原RDT/Architecture maintenance owners | 原RDT按当前范围刷新phase2影响判断，消费真实完整拟写；两owner在提交前final_integration核live expected-current、分别整合/readback。只到integrated_pending_review，不制造candidate Check或预提交独立实施审核 |
| I811-09 | I08及本次TaskCommit明确副作用边界；原TaskCommit/implementation/独立Review owners | 展示stage/commit准确文件后由原owner形成固定本地候选；原constructor覆盖完整B..H与实际路径，再begin_check。新独立reviewer同次审核Architecture before/after及九维完整区间，不让实现自审代替 |
| I811-10 | 当前Check/full_review和证据；原Delivery Review/readiness/Publication/merge及整体owners | 每个Git/GitHub副作用先展示精确计划；每次merge交协调方。业务交付后整体Completion/Closure/Finish、必要归档merge及live main可达性和资源disposition仍须实际完成 |

canonical package根为 `trellis/skills/guru-team/packages/`；shared consumers/runtime根为
`trellis/skills/guru-team/`，preset/overlay/spec根为 `trellis/presets/guru-team/`。
本checkout的installed/dogfood只由原tools owner更新。I811-01..06已有实施和定向工程事实，具体结果由配对 Test 单写；
本轮只刷新验收与依赖，不重做未变实现或重放已完成tools采用。真实内容变化后才由原owner判断受影响验证。
当前规划不执行commit/push/PR/merge；每项Git/GitHub副作用仍须展示精确计划。

## 3. 验证入口、输入与预期观察

按design第8节V811-01..07执行。下面给出入口、观察和证据边界；既有结果按当前适用性采用，正式完整验收由原质量owner判断。

1. **V811-01/02**：在原 normal、solution、Clarify、Discovery、Sync 的 `tests/` 中维护长期回归，
   用 `python3 -m unittest discover -s <实际package/tests> -p 'test_*.py'` 逐包执行。
   新完整链回归置于 `guru-discover-change-context/tests/test_qualification_context_chain.py`，
   真实调用各原 `scripts/invoke.sh`；fixture只准备boundary外状态，外部gh替身不替代包内producer。
   六类profile/context差异及两个mutation refresh分别观察完整返回identity、最新authority与原caller消费。
   mutation输入中的disposition必须取自真实Discovery公开authority_duplicate_snapshot；断言snapshot与实际authority及原duplicate事实匹配，
   source普通更新后旧snapshot拒绝并经原producer刷新；不能在fixture手填该被测producer应生成的snapshot。
   独立expected来源是#811行为，不能调用被测实现重复计算expected。证据限确定性public链，不称真实Agent/远端验收。
2. **V811-03**：采用各package现有 `test_contract.py/test_runtime.py`、Sync `test_read_baseline_chain.py`
   的适用覆盖，增加实际受影响旧四类、Task/no_issue/非Task与普通stale/mismatch。
   旧active Task-status路径保pinned-old验证语义，不恢复为current入口。以固定B原字节检查旧发布schema/example，
   current selectors只选新合同；不是为保持旧runtime添加compat reader。
3. **V811-04**：从原 `check-skill-packages.sh` source/installed公开入口验证受影响包、共享consumer及projection，
   通过 `discover-skill-contract.sh --root . --mode source|installed --skill <实际producer> --exit <实际出口> --json`
   证明唯一consumer及matching合同可定位；命令格式以当前原help为准。运行
   `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
   原tools操作之后跑目标自己的resolver、installed验证和实际native/public入口；验证实际声明的平台资产、mode及sidecar。
   源脚本运行成功不能代替目标可用；tools-only local_candidate必须报告formal_fork_source_lock未验证。
4. **V811-05**：使用本项现有 `test_qualification_context_chain.py` 的独立正常 Task/Delivery 场景，
   复核其原 Creation/Identity/Ensure/Bind/Selection 前置与真实 normal/solution qualifier→Clarify→Sync/Discovery→正式clear→原caller消费。
   观察场景内同一 Task/generation/Delivery、候选、target、mode、continuation/resume 及当前来源关系。
   fixture 的显式语义输入只证明测试声明层；不预置被测 producer 结果，不捏造用户未决范围，不指定发布 Task/版本/时点。
   复用仍适用的完整链及定向结果，由原 Check 判断组合覆盖是否充分；实际缺口只补对应观察，不另加实际 Agent/远端证明前置。
5. **V811-06**：原knowledge readback、固定已提交候选和独立Review使用各原公开入口及其当前合同。
   整体交付后的GitHub关闭/merge与main可达性用authenticated repo-bound gh和Git实际核对；
   业务PR与归档PR分别说明结果，不拿计划或本地测试当已交付。
6. **V811-07**：扩展原 `tests/test_skill_packages.py`、`tests/test_delivery_contract_graph.py`、
   `runtime/tests/test_runtime.py` 及直接installer/adapter测试，不新增通用测试框架。
   通过原source/installed `discover-skill-contract.sh` 查询Discovery context_ready、Clarify refresh_context和
   Sync baseline_ready，实际观察context4及consumer自有call-local schema可定位。
   从真实Sync baseline_ready两种输出选择authoring_profiles，校seed/AI字段互斥、原字段投影及唯一profile；
   原AI提供change_input和pre_task的clarify_profile，reviewed-plan另提供source_locators，再由真实Discovery input校验。
   ordinary eval沿原 `run-skill-evals.sh` 的实际help选择一个1.10包及足以到达原调用的现有case，
   不替代被测wrapper；输出由新run5 schema和原receipt reader消费。若设施未到达调用，保诊断，不能算行为证据。
   run2/3/4旧资产按B保字节，qualification生产矩阵不重跑；本项不新增模型、评分或生产验收合同。

执行顺序采用低成本行为明确的回归优先；当前已有完整实现与工具采用事实，先判断覆盖适用性，再补真实缺口。
单元/contract、公共链、installed、实际Agent与外部lifecycle证据分别报告。
已有结果只在其前提仍适用时采用；仅stage或caller改变不要求重复实验。
临时诊断须回答一个未解问题，足够支持下一判断即停止；无固定反复red/rollback义务。
本项不执行完整多平台Throwaway/升级/Release矩阵或生产观察。
此前公共链整包初试失败及修正后定向通过由配对 Test 单写，不把定向结果称为新的整包全绿。
metadata/authoring与实际安装均已有定向工程结果；本轮规划刷新本身不产生额外通过结论，也不要求无关重复实验。

## 4. 停止条件与适用回退点

- 每次Task/source/test写前运行原 `check-task-checkout-boundary.sh --json --task <本TaskRef>`。
  Task/key/phase/checkout不符回原Identity/Ensure/Bind/Selection，不借其他chat binding。
- 缺必要authority或source内容回原Discovery/Clarify；scope变化先根requirements acceptance与原Delivery rework。
  新机制、owner或支持边界实质变化回Author与Architecture，不在实施中扩张本设计。
- public invoke错误保实际diagnostic，修正真实输入或由原producer重取context；record/check不冒充出口，旧transition不修补。
  mutation已生效时按live事实刷新，不重放副作用。未解决选择不进入clear。
- tools更新前的源/API/锁/unfinished operation缺口回原tools owner；未完成工具操作用同ref/frozen plan恢复。
  rollback是原owner另行审查的准确写集，不重新prepare、不改checkpoint、不覆盖后来业务dirty。
- 公共链失败先判断是否到达声明行为；设施反复失败后修设施、改有界观察或保明确gap。
  独立公共链真实缺口回原实施/质量owner；不能以schema或record/check替代被测producer及正式clear。
- 没有业务数据/DB迁移或服务部署，故不新增数据库或发布回滚协议。未授权Git/GitHub动作和资源清理保持停点。
  验证已足够且必要回归完成后停止追加实验；完整矩阵不在本Task的失败集合。

## 5. Delivery Policy（唯一）

**full**。D1覆盖全部R811-01..07和AC811-01..08的当前实现与证据责任，不留D2实现清单。
独立可交付条件是：完整两类公共链及mutation刷新、旧支持行为、共享metadata/AI authoring和ordinary receipt可消费、matching受管采用、本项独立正常Task/Delivery的同工作公共链接续、
完整知识整合/readback、固定已提交独立Check/full_review和当前readiness成立。
不保留指定发布Task、版本或时点依赖，不以另建同名对象替代场景内身份保持。fixture语义输入与实际公共产物分层，原Check按live验收判断充分性。

业务交付后才能成立的整体Completion、Issue正确关闭、必要Finish归档、归档merge/main可达性和资源disposition，
仍由本Task原owners继续完成，不是业务PR创建前必须预先完成的循环前置。
Delivery合并不代表Task完成。没有其他延期能力、临时产品限制或具名后继Delivery。
本地candidate的正式Fork lock和完整矩阵/生产效果未验证，不改写成#811功能失败或release pass。

## 6. Docs SSOT Plan（唯一）

**strategy=delta_first**。真实delta是design第5..7节的确认I/O、Task/authority关系、mutation刷新、
共享Interface/consumer及AI authoring、旧边界退出和matching采用；本轮另同步独立正常Task/Delivery验收及外部依赖退出。
原RDT writer为 `guru-maintain-requirements-design-test-ssot`，直接consumer是本批实施、Check/Review和整体Completion。
本地隔离R/D/T delta置于 `docs/requirements-design-test-contributions/811-qualification-context-continuation/`
的requirement.md、design.md、test.md；只在内容实质形成时写，不建空文件或资格ledger。

| authority/现有单元 | 本批真实差额与原writer |
| --- | --- |
| docs/{requirements,design,test}/current/qualifier-applicability.md | 各层新增完整REQ/DES/TST-811、两类/三context及mutation返回、最小对象和版本关系；原RDT writer分别维护，测试单元单写实际结果与未验证边界 |
| 同三层current/local-fix-intake.md | 只修命中的context target/authority与原producer恢复适用关系，链接上行#811定义；不扩张其他诊断或重写历史 |
| docs/architecture/03-domains/qualifier-applicability.md、workflow-context.md | 原Architecture writer承接确认对象、原graph、Sync事实角色、共享metadata、AI authoring与分发；保其他职责和历史观察 |
| docs/architecture/adr/qualification-context-continuation.md | 原Architecture writer从同名隔离ADR候选整合；只窄替代#812两确认output不带key片段，其余决策保持 |
| trellis/presets/guru-team/MIGRATION-811.md、命中README/Skill/spec投影 | 各原源码writer按design5.3/5.4记录current Interface/registry/manifest/run、profile authoring、pending重装/固定旧provider恢复及matching reader/installer采用；原tools owner安装投影 |

真实隔离Architecture贡献和ADR见design第9节。实施与工程结果齐全后，原两maintenance owners分别在提交前
final_integration核live expected-current、整合完整current正文并readback，再纳入TaskCommit。
独立已提交Review审核实际before/after及三层与Architecture关系；Planning、schema或recorder通过不能代替晋升与Review。
保持原root/system/ownership/index和未命中规范；出现确实需要的共享关系变更时回各原owner，不直接登记第二current。
