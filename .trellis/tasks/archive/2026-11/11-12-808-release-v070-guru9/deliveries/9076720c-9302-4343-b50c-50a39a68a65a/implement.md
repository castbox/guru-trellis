# Gen2 采用切片实施与验证计划

## 1. 输入与引用

读取[整体PRD](../../prd.md) §3.3/5.4/5.5/7、[本批PRD](prd.md)全稿及[design](design.md)九节，唯一来源设计处置在design§3。实际输入是PR844的delivered结果、reviewed H `3f7099b9db78700d03a29b2c825e84280f5b6821`及其完整干净provider。内容B同该head，PR目标main，不追浮动main。

工程Agent实际完整读取安装的Author planning-body、当前三模板、clear-technical-writing、quality的Test And Validation Value/Validation Scope Ownership，以及原tools SKILL/contract/interface/public install schema。MIGRATION794§1/4/5、私有发布合同Complete Source Before Actual Adoption/Whole Preparation Completion与design§3必要条件共同约束本批。引用不是阅读或验收证明。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原责任、文件和完成观察 |
| --- | --- |
| I1 取得匹配来源 | Activation后，原source/tools owner读取PR844公共结果与实际Git，取得完整干净H；按源自己的lock复核已有Fork及CLI/Core build/API。外部临时source checkout仅provider，不写Task workspace映射 |
| I2 原tools正式采用 | I1成立；原owner核未完事务、目标/peer/shared路径、旧manifest/managed编辑和平台；preview→AI完整审write/delete/preserve、AGENTS/workflow及public capability→prepare一次→审实际冻结plan→展示→invoke。原installer生成所有目标受管after和manifest，不手写managed文件 |
| I3 目标工程验证 | 实际执行terminal后，原implement/check agents完成V1～V5，运行目标自己的resolver/installed/native，核完整集合/安装mode/三平台/workflow/lock、preservation、sidecar/drift。发现计划外候选先停改并交原coordinator，不自修扩scope |
| I4 知识整合 | 原RDT执行本Docs Plan，原Architecture判断必要after；无变化返回原no_change，有真实差额先由原writer完成整合/readback。安装结果不替独立语义质量 |
| I5 固定完整候选 | I3/I4充分后，原TaskCommit展示全部实际安装/规划/必要文档路径，精确本地提交；原constructor固定B与实际H、完整paths，再公开begin_check。配置工程agents不写正式gate |
| I6 独立质量与交付 | 新的未实现候选reviewer独立Architecture before/after及完整九维/fullrange，正式check/full_review两槽。当前passed后publication Architecture、Delivery readiness、中文Refs-only载荷、Publication和expected-head Merge；合并后原Completion判断全Task |

每批source/test/Task写入前调用原check-task-checkout-boundary，编辑限定当前已核Task checkout。工具的checkout-local runtime更新留原tools write set；Task/jsonl只由原Author或公共lifecycle API写。没有其他源码、README、共享index或发布ledger写作任务。

## 3. 验证入口、输入与预期观察

| 验证 | 命令/输入与预期结果；对应design§8 |
| --- | --- |
| V1 | repo-bound gh读PR844及public Delivery facts，Git head/status、源trellis-source lock及既有matching Fork/build/API；目标与源配对明确、clean且已delivered |
| V2 | 源tools scripts/preview.sh、prepare.sh及invoke.sh，source_ref=实际H、dependency_mode=source_locked、checkout=当前Task；实际tools_upgraded、unverified=[]，extension .9/CLI .6/clean source/原postvalidation |
| V3 | 目标resolver、`./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`、`./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json`、`python3 .trellis/scripts/get_context.py --mode continuation`及public current；新runtime真实可达、同key继续原owner |
| V4 | 对全部managed mapping与manifest实际path set核字节/安装mode、三公共root source validator、workflow/lock、check-upstream-ownership.sh、check-dogfood-overlay-drift.sh、sidecar/bytecode、原preservation；缺失/差异/未处理sidecar为空，peer/common及Task/user内容保持 |
| V5 | 核H0已审Sync16/read3/Issue2及临时完整分发的适用性；在实际目标原Sync公开wrapper调用无Git副作用bare skipped输入，期待exit0/skipped。不要在真实target测试默认sync去推进primary。旧组合fixture失败不改成pass，不扩修其他Issue |
| V6 | 原RDT/Architecture真实after、diff-check、TaskCommit/完整constructor候选与新独立Review、原readiness/Publication/Merge；所有after进本批质量链，Refs #808，不宣称Task或Release完成 |

使用已匹配toolchain与managed Python，Python设PYTHONDONTWRITEBYTECODE=1。source/installed/Agent/GitHub分层报告；目标native不能用源命令或临时fixture代替。临时原始命令日志可留外部temp，不创建task-local状态或证明账本。预期不是已执行结果。

## 4. 停止条件与适用回退点

来源未交付/不clean、lock/build/API缺失、目标不唯一或重叠未完事务，停原tools/source owner。普通参数错误按原诊断纠正；旧事务按同source/plan/ref完成，不能新prepare替换。真实scope/authority/机制变化返回原Author/Clarify/Architecture适用路由，刷新受影响门禁后再实施。

未知owned编辑需原owner明确preserve/replace；sidecar、完整集合不匹配、preservation或target native失败均保实际失败并恢复，不报成功。rollback沿原owner单独审写集、先公共兼容校验再restore，不reset Git、不删历史/无关改动。没有数据库、生产部署或远端发布变更，不制造这三类回滚协议。

具体验证缺口才追加能回答该问题的实验；证据充分后停止。设施反复失败重评复现方法并保缺口，不无限修fixture或把未证验收记pass。提交、push/PR、merge、终态/cleanup和后置发布各保持原独立边界。

## 5. Delivery Policy（唯一）

Policy=`full`，仅指本批选择的AC04及自身适用AC01/03/05/06全部覆盖。独立交付条件是完整干净已交付来源的真实source_locked采用、完整目标工程/preservation/native验证、必要知识after、精确本地提交和本批独立完整质量/Refs-only交付均成立；没有延期的本批安装或来源缺陷。

来源与采用之间的临时限制在本批实际成功后解除；历史失败与前序正文保持原观察。没有新机制或当前规范限制需要另建退出协议。整个Task仍需原Completion核所有准备要求/五个实际Delivery及证据；合并不自行完成Task。之后Closure no_mutation、acceptance-finish Architecture、Finish和精确Cleanup仍待原owners。Stage2全部候选gate、tag/smoke/Release、eafc/primary收敛和最终关闭#808不在本批或准备业务Completion内。

## 6. Docs SSOT Plan（唯一）

strategy=`no_docs_update_needed`。本批只安装已交付的相同规范/源码；不新增业务行为、公共接口、架构决策或支持限制。三个README已有真实版本和发布条件，不追写当前安装/最终pass；原失败日志和贡献cutoff保持。命中的完整authority为PRD§7所列R794/R649（生命周期/Completion）、配对D/T、ARCH-DOM-010/ARCH-INT-015及原tools合同；无需新共享导航、contribution或ADR。

原writer为guru-maintain-requirements-design-test-ssot及必要guru-maintain-architecture-baseline；它们在实际after阶段亲自核是否确无差额，直接consumer为TaskCommit及本批独立完整Review。若发现真实需要修订的当前定义，先返回原Author更新Docs Plan，原maintenance完整整合/readback后再TaskCommit；不由worker手改共享authority或追记结果。独立提交后Review判断实际after；no_docs_update_needed不是预填其通过。
