# 跨环境生命周期基础 D1 实施与验证计划

## 1. 输入与引用

输入为同Task整体accepted_scope、本批`prd.md`全部要求、`design.md`第3节唯一来源设计处置、第5–9节机制、接口与迁移，以及原Architecture实际candidate_assessment。后者返回`baseline_current / architecture_impact / legacy_boundary_convergence`，只允许继续方案规划；不是final_plan、Approval、Activation或实现证明。

实施前按I01–I08命中文件完整读取原package合同、当前canonical代码、`.trellis/spec/`命中规范、Author planning-body/templates、current knowledge及候选适用性合同。实际原scope仍为R1–R5/V1–V8。上游正式API已通过PR #55合并。精确matching构建及canonical source采用已通过；当前完整适配方案及真实贡献/ADR已形成；仍需当前Wording、Architecture final_plan和Approval。目标安装/原生验证按下文在实施阶段执行，不能把未来验收当作规划前置。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner与实际文件范围 | 产物与完成观察 |
| --- | --- | --- |
| P0 provider采用 | 原source owner；已合并Trellis PR #55，不重复上游实现 | 精确merge/parents/tree/main CI、matching Core/CLI build与真实capability；canonical lock及文档成套采用，目标投影和原生消费另行验证 |
| P1 完成Planning | 原Author，在当前D1规划目录；真实依赖到达后补design接口、迁移和本计划命中命令；原RDT/Architecture准备隔离贡献及必要ADR | 全部当前要求、真实上游I/O、唯一consumer与context充分；原Wording→Architecture final_plan→Approval→当前计划接受→Activation，未到此不实施 |
| P2 逐项状态归属 | 当前Task checkout，`trellis/skills/guru-team/packages/`全链原owners、`runtime/task_lifecycle/`及`runtime/delivery_projection/` | 对design第4节每行实际读写/producer/direct consumer/生命周期/缺失入口作完整审查，选择已证实必要修改，原owner判断后记录最小事实；不按目录推断或留下R1阻塞后关闭 |
| P3 共享Finish/Reactivate及旧格式 | 原Finish/Reactivate/legacy maintenance语义与确定性适配，命中原package的SKILL/references/schema/runtime/tests | 精确历史终态独立于本机seal/Cleanup；当前Task2沿公共reopen；指定旧格式调用P0真实能力；后继复用、generation一次、新key交原环境owners及next owner |
| P4 活动与副作用恢复 | 原Identity/Establish/Ensure/Bind/continuation、Publish/Merge/Closure及其原tests | 明确ref/commit上的同Task/Delivery续接；Open Draft/Ready、MERGED、exact-source disposition分别零重复恢复。保持#636/637/638，必要输入真缺时具体阻塞 |
| P5 资源与正常并行 | 原common-dir branch/resource ledger及Cleanup package | 旧代资源责任不跨common-dir/Task冒领；推进remote ref保留新提交；正常双Task不互设准入；无锁/租约/压力扩张 |
| P6 matching分发与知识候选 | canonical workflow/preset/spec/overlay/packages；原Author选择官方implement/check context；原RDT/Architecture写隔离完整proposal | 完整consumer迁移/legacy删除条件、声明平台与dogfood一致；没有只改安装副本；source lock正式采用与源码状态分开 |
| P7 候选质量与最终整合 | 原implementation、独立Architecture、原Check与原知识owners | 固定B/实际HEAD/全部paths candidate→独立Architecture phase2→candidate Check→合法rework→原final_integration写/readback→刷新candidate→最终Architecture/Check |
| P8 提交到终态 | 原Commit/Branch Review/Delivery Review/Publication/Merge，再whole Completion/Closure/Finish/Cleanup | 按实际候选精确提交、完整committed独立Review、真实readiness和expected-head；全部satisfying PR合入main后仍独立审整体完成及精确资源责任 |

P0 source采用已经完成；P1继续当前规划评审。P2–P8在原计划接受/Activation后执行；真实转换调用还必须核目标已采用matching capability。上述执行次序不授权任何Git/GitHub mutation，也不为绕过P0拆出fallback-only交付。

### P0 精确采用与本轮接续

采用目标唯一见design第5.1节。公共能力与merge CI已可核验；旧7f050 lock、现有stale dist和此前86de配对安装均不能当作精确merge已采用。A1–A3现已执行，仅证明source层采用。目标安装没有执行。

| 子步骤 | 原owner、实际范围 | 完成观察与边界 |
| --- | --- | --- |
| A1 matching source build | 复用已在准确merge且tracked干净的既有Fork checkout；该checkout自身`node_modules/`、`packages/core/dist/`、`packages/cli/dist/`及CLI build-origin标记；正常prepare还会生成ignored `.husky/_/`并设置本仓`core.hooksPath=.husky/_` | 使用`pnpm@10.32.1`和冻结lockfile；正常Core→CLI build成功后才记HEAD；不移动branch/HEAD、不创建Task或checkout，不改源码/全局npm |
| A2 canonical source采用 | 本Guru checkout的`trellis/presets/guru-team/source/trellis-source.json`、根`README.md`、`trellis/workflows/guru-team/README.md`及`trellis/presets/guru-team/README.md` | 写准确merge、有序parents/tree、main CI与既有版本/manager；文档说明新增capability及未验证目标边界，保留稳定tag/历史source的原身份 |
| A3 source定向核验 | 原`verify_trellis_compatibility_matrix.py validate-source`，不是matrix run；source准备与三份README一致性定向测试 | readback精确HEAD/build-origin/模板bytes、matching Core/CLI、实际capability及精确merge CI；只证明source采用，不报告目标安装或V1–V8通过 |
| A4 原D1 Author续写 | 同planning_root三文档及官方JSONL；原独立Architecture owner | 用真实API和matching source事实刷新原candidate_assessment，完成全链owner输入/输出、贡献/必要ADR和V1–V8可执行计划，继续原Wording→final_plan→Approval→计划接受/Activation；原blocked规划无自动批准效果 |

A1–A3是已完成的source采用动作。该批不运行full preset、不调用Reactivate、不改变任务/会话/资源、不会写Task/Delivery gate。A4的规划写作继续原Task，不新建D2或替代Task。所有commit/push/PR及生命周期副作用保留原独立边界。

以下命令已按README在精确source执行；canonical lock与三份README同步采用。未来重入仍须先核准确source/干净状态与版本：

```sh
set -e
# FORK_SOURCE指向现有、准确merge且干净的Fork；先核pnpm为10.32.1。
cd "$FORK_SOURCE"
test "$(pnpm --version)" = "10.32.1"
pnpm install --frozen-lockfile
pnpm build
# 仅在上面构建成功后生成此标记；不为通过validator单独补标记。
git rev-parse HEAD > packages/cli/dist/.guru-source-commit
node packages/cli/bin/trellis.js --version
node packages/cli/bin/trellis.js maintain contract --json

# 按design第5.1节采用canonical lock并同步三份README后：
cd "$GURU_SOURCE"
PYTHONDONTWRITEBYTECODE=1 python3 trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py \
  validate-source --repo-root . --fork-source "$FORK_SOURCE"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s trellis/presets/guru-team/scripts/python -p test_fork_preparation.py
git diff --check
```

实际结果：Core→CLI build成功后写来源标记；source validator通过（212个template，精确merge/main CI匹配），4项source准备测试通过，git diff --check通过。新SDK对真实#503固定archive的只读inspect返回successor absent，调用前后仓库状态一致；未prepare/apply，未作Guru正式终态资格判断。上述结果不替代原生Reactivate或V1/V7。

### P6 安装、分发及迁移范围

A1–A3不等于目标采用。P6应在完整Guru机制与迁移合同就绪后执行下列成套动作，不在旧规划上直接安装半套能力：

1. canonical adapter修改归原`runtime/maintenance_transport.py`方法allowlist/capability检查，Reactivate package的SKILL/references/独立输入输出schema/runtime/tests及命中环境/Continuation owners。public DTO只投影实际key/ref和唯一consumer需要的身份；实施前由完整owner审查决定是否保留ID增量兼容或新ID/显式迁移，不能靠新增nullable字段绕过契约。
2. 原RDT/Architecture维护隔离完整delta与必要ADR，命中shared Finish、local资源责任、正常跨clone活动/已发生副作用恢复及旧schema1单次收敛。迁移说明落在canonical preset `MIGRATION-635.md`，明确两仓配对、旧安装路线、在途事务处置及退出条件；不修改稳定tag历史或批量旧归档。
3. Trellis-owned模板更新由matching官方工具owner执行，先看实际update dry-run/维护preview；保留用户修改、原Task/D1与本机资源。上游新reader在`common/task_utils.py`，不得通过Guru preset复制补丁或仅改`.version`。官方hash、更新冲突及真实sidecar逐项审查，生成文件集以该次preview为准。
4. Guru canonical workflow/完整preset/packages/overlays/spec由原installer投影；`source/trellis-source.json`只投影到`.trellis/guru-team/trellis-source.json`，后者不是第二authority。dogfood及声明平台使用同一complete source；不手写projection或绕过旧归档迁移前置。若full apply仍被旧记录阻塞，沿原安装/维护owner具体处理，不迁移无关档案制造成功。
5. 运行`apply.sh --repo .`、`check-dogfood-overlay-drift.sh`及`verify_dogfood_upstream_projection.py --repo-root . --fork-source <matching source> --json`；分别报告Guru与Trellis投影。source-only采用不冒充这三项通过。
6. 同一Guru candidate配对matching Fork，最多一个代表安装profile。此前上游packed样本只证明公共/native层；Guru V1两条再次Finish、V2活动ref、V3三类副作用、V4/V6隔离、V5缺失、V7真实旧样本与V8分发仍需本D1实际证据。独立common-dir运行样本可以多个场景，不能扩成全平台installer矩阵。

### P2–P8 可执行文件责任

| 实施ID | canonical文件/原owner | 必须完成的实际工作与前置 |
| --- | --- | --- |
| I01 / D635-01 | `packages/guru-reactivate-task/{SKILL.md,references/,interface.json,schemas/,runtime/invoke.py,runtime/shared_finish.py,tests/}` | 定义新闭合shared archive入口、准确历史Git/PR资格与后继优先查询；退役shared admission中的seal/manual Cleanup依赖。Task2仍公共reopen，正式schema1沿matching SDK；无旧C/C/gate制造 |
| I02 / provider | `runtime/maintenance_transport.py`及对应tests | 加两个正式SDK方法和明确capability检查，复用source_locked匹配与既有事务executor；不新增CLI wrapper、第二resolver或converter |
| I03 / D635-02 | `packages/guru-complete-task-closure/{SKILL.md,references/,interface.json,schemas/,runtime/invoke.py,tests/}`、`runtime/task_lifecycle/closure_result.py`、Finish命中的contract/tests | 实现最小共享载体、原public evidence关联、准确result/Completion/source读取及零provider恢复profile。旧已完成archive不补载体；source/provider漂移回原Closure；载体不能恢复授权或证明terminal |
| I04 / D635-03 | `packages/guru-publish-task-delivery/{SKILL.md,references/,interface.json,schemas/,runtime/owner.py,runtime/draft.py,runtime/remote_recovery.py,tests/}` | 两个独立精确PR恢复profile，复用原push/bind/metadata/Ready writer；显式remote ref与本地binding分离，零重复create/已完成动作。保留普通本地profile、#636 Draft先于新候选push、当前readiness原owner判断 |
| I05 / R1/R3 | `trellis/workflows/guru-team/workflow.md`及原Identity/Establish/Ensure/Bind、Continuation、Check/Review/Completion各自的SKILL/references | 全局只加必要新profile路由/唯一consumer，step-local明确public共享事实、必须重审、local责任和真缺输入四类。复用#454和当前evidence-refresh/manual Merge；原实现正确处保留代码，用实际caller/测试证明，不重写所有owner |
| I06 / R4 | 原Reactivate释放/收购责任适配、`runtime/task_lifecycle/resource_ledger.py`及Cleanup命中tests | 仅删除旧资源待处置对不同合法新资源的准入依赖；同资源冲突、unknown ownership、精确remote ref/expected head和generation不放宽。实测双common-dir同名local branch及双Task；未发现缺陷的ledger/Cleanup实现保持 |
| I07 / V8 | `MIGRATION-635.md`、canonical workflow/preset/spec/overlays/packages与声明平台生成副本 | 新profiles/schema/consumer和旧入口退役显式列清；source、官方native与Guru完整packages同源采用。原tools-only维护owner保持旧Task/session，代表支持目标验证full preset/reapply，逐个处理sidecar，不批量转换无关旧档 |
| I08 / Docs与最终链 | 本D1真实Architecture贡献/ADR、`docs/architecture/contributions/635-portable-lifecycle/proposed/`及`docs/requirements-design-test-contributions/635-portable-lifecycle/` | 原RDT/Architecture owners形成命中完整单元proposed，不预建空文件。独立Architecture→candidate Check→合法回implementation→原final_integration→实际readback→重新candidate/begin_check→最终Architecture/Check；然后精确commit、完整committed Review及readiness/交付 |

I01/I03/I04先完成各自闭合接口与直接consumer，I02与I01组成实际可用formal路径；I05/I06对完整组合核验，I07在matching完整候选就绪后执行。任何真实范围/机制/依赖变化回原Author/Architecture，不默默加共享字段或借新profile放松旧正常路径。

### 安装验证的唯一代表profile

只选一个Codex/native代表安装profile，沿已建立的上游样本环境/工具前缀更新到当前精确matching source并承接Guru完整安装；不分别再跑一套全新clean/多平台安装。独立common-dir A/B及双Task场景从该受审tracked工具/Task/Git内容合法clone，不复制.git、ignored runtime、session或原机ledger，不把clone动作当第二installer矩阵。

该profile内由实际AI owner从原native入口完成必要语义判断和正式调用；测试driver可负责真实Git/受控provider输入、命令及客观观察，不能替AI写semantic pass。A的completed/archive必须由原Completion/Closure/Finish生成，bookkeeping合入所选测试target；不能手写completed/seal替代。受控provider fixture只证明其集成层；真实GitHub样本/当前provider事实单独标明，不声称生产或完整Release。若环境不能完成该真实native链，保留具体SKIP/缺口，不能由unit结果宣称V1通过。

source仓库现有旧归档会命中`delivery_installation.py`的全量inventory前置；`validate_applied_tools_operation`和原`guru-upgrade-tools`已有不解析旧Task的tools-only合同。因此dogfood先由原工具维护owner保留Task/session完成成套工具投影；按AGENTS实际调用plain apply并保留其真实结果，不能把拒绝记作成功。完整preset apply/reapply在上述唯一受支持代表目标证明；不以迁移全部历史档案解除source仓库的前置。不修改preflight或强制写`.version`作为捷径。

## 3. 验证入口、输入与预期观察

| 验证 | 原生入口/实际输入与测试落点 | 预期结果及AC |
| --- | --- | --- |
| T01 当前Task2共享终态 | `guru-reactivate-task/tests/test_delivery_reactivate.py`扩真实Git/独立clone；实际原owner产生Task2 C/C/archive、bookkeeping merge；target再正常前进 | B无A seal/退出/Cleanup仍核准确历史；后继优先、同Task一次增代；未合入target不正式完成。V1/V4/V5 |
| T02 正式旧schema1 | `test_reactivate_contract.py`及拟新增`test_formal_archive_reactivate.py`；固定Guru .3/#503原样本与其准确PR505 merge，matching formal SDK input | 原archive/history不变，公共一次g+1，无旧C/C/gate/空Delivery；原Establish→Ensure→Bind/Continuation及真实下一owner消费。人工历史/未完closeout分别原路线。V7/V8 |
| T03 共享Closure | 拟新增`guru-complete-task-closure/tests/test_shared_result_recovery.py`及`task_lifecycle/tests/test_closure_result_portability.py`；正常close/retain/no-close、混合集与无Issue | 原owner产生载体/public结果，再正常clone无private；精确读取原动作集和result，Finish真实逐Issue状态核验。projection丢失恢复零close，drift回原owner；不把CLOSED当归属。V3/V5 |
| T04 Open Draft/Ready恢复 | 拟新增`guru-publish-task-delivery/tests/test_remote_recovery.py`并保留`test_early_draft.py`/`test_transaction.py`；明确source commit/同key与原PR，B本地branch不同 | Draft/metadata未完只补剩余动作；Ready已发生只恢复事实并重判适用性，无create/重复push/edit/Ready。保留新未审修订先退Draft、当前真实readiness。V2/V3 |
| T05 MERGED恢复与Completion | 复用`guru-merge-task-delivery/tests/`对应manual merged recovery、Completion既有无Delivery profiles | actual双亲PR/public Publication唯一关联；public结果丢失恢复零merge。actual差额及CI状态进入原Completion，不推导whole completed。V3 |
| T06 活动ref与正常并行 | 原Identity/Bind/C4/Continuation tests及`test_delivery_family_integration.py`；Task/Delivery/代码在明确可获取但未入main的ref；两独立common-dir、两个Task | 同身份/实际Delivery接续；仅重审/补跑命中项，不重开Intake/Planning或造替代Task；另一Task runtime缺失/cleanup pending不互改。V2/V6 |
| T07 资源隔离与缺失 | 原Cleanup contract、resource ledger、`test_finish_family_integration.py`；旧pending、同名local branches、正常推进remote head及新generation | 不跨common-dir认领，不用旧receipt删除新代/新head；unknown保留；不可获取ref/代码/真正必要输入及归属冲突具体返回原owner。V4/V5/V6 |
| T08 原native完整两条再次Finish | 唯一代表profile中实际AI owner按public输入调用原Reactivate和后续owners；A正式归档→B clone：一条新Delivery，另一条仅补验证 | 分别真实Delivery→Completion/Closure/Finish和evidence-refresh→Completion/Closure/Finish；无空Delivery、旧pass或A私有状态。逐项观察原失败阶段/最终结果，不能由fixture摘要代替。V1/V7 |
| T09 分发与迁移 | 原source/installed package validator、官方projection checker、Guru apply/reapply/drift及定向安装/平台投影tests | source/installed/Guru/官方native分别通过；模式/sidecar正确，旧安装沿匹配维护路线保留原数据；仅一代表profile，不泛化Release矩阵。V8 |

以下为实施后最低定向命令；现阶段只有P0 source采用项已执行。运行前原implement/check读取各package当前测试与环境合同，命令失败如实归因，不擅自扩大suite或改期望：

```sh
# canonical package校验，不把validator成功当semantic pass
PYTHONDONTWRITEBYTECODE=1 bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-reactivate-task/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-complete-task-closure/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-finish-task/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-publish-task-delivery/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/runtime/task_lifecycle/tests -p 'test_*.py'
# 现有Merge/Completion/资源/跨family命中项及新transport测试由上述T05-T07责任选择。
# T08由实际owner逐步执行，不用一个脚本--pass生成所有gate。
# source dogfood按原tools维护结果再核两类projection；plain apply真实结果单列。
bash trellis/presets/guru-team/scripts/bash/apply.sh --repo .
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
PYTHONDONTWRITEBYTECODE=1 python3 trellis/presets/guru-team/scripts/python/verify_dogfood_upstream_projection.py --repo-root . --fork-source "$FORK_SOURCE" --json
git diff --check
```

实际新增测试归其被测package，复用真实Git/public-bin/native helpers，避免重复纯Core断言或镜像实现。P0的4项source准备测试和SDK inspect不替代T01–T09。所有V1–V8仍待实施，结果由原Check/RDT唯一test正文记录实际层次和未验证边界，不制造全链审计历史。

## 4. 停止条件与适用回退点

P0公共能力/I/O、matching build及Guru canonical source采用已经完成，旧provider缺失停点已解除。当前原Author可交plan_ready，之后仍由当前Wording→Architecture final_plan→Approval判断。未取得计划接受/Activation前不实施；真实转换前目标必须已采用matching capability。目标安装未执行不要求Author返回blocked，也不证明转换可用。不在Guru补公共writer或造旧C/C；仅登记依赖不是完成。

真实scope/authority变化回原Clarify，机制/依赖变化回原Author及独立Architecture；普通mapped re-entry自动承接。语义结果、文件或原source缺失不补造pass。实际API到达后必须核字段/版本/恢复/consumer差额，不能直接把当前候选评估重标为final_plan。

原owner各自恢复同操作，只补未完成动作；未知输入/归属冲突停止该owner，不覆盖并行修改。迁移回退以正式上游维护合同、原preimage及数据兼容为准；当前没有已执行迁移需回退。Git/PR/Issue/资源删除保留实际对话副作用边界，不记录授权、不批量清理。

## 5. Delivery Policy（唯一）

Policy为`full`。D1承担整个R1–R5/AC-V1–V8，不把正式旧格式、独立clone原native再次完成或其它全链缺口分给未获接受的后续Delivery。全部行为、验证、matching迁移、真实最终质量门禁和交付事实满足后，才能报告该Delivery已交付；whole Completion仍独立审所有责任。

P0 source采用是已完成前置，目标迁移与全部V1–V8仍为本D1实施责任，不是partial/staged完成理由。当前D1仍planning，未Activation、未交付；也不能因Architecture候选方向通过就关闭Issue或触发Finish/Cleanup。

## 6. Docs SSOT Plan（唯一）

strategy选择`delta_first`。原RDT owner为生命周期及completion-closure的R/D/T完整单元准备隔离delta；原Architecture owner为共享终态/本机资源责任、正式旧格式单次收敛及ADR-027/ARCH-DOM-032窄替代准备真实贡献和必要ADR。直接consumer分别是原Planning/implementation/Check/Review和后续Continuation/Completion，不能以审计方便扩大DTO或新建全链台账。

原Architecture实际候选路径是`legacy_boundary_convergence`，decision refs为ADR-024/027、ARCH-DOM-032/054、ARCH-GOV-009。真实接口、具体贡献/必要ADR候选已在本D1 architecture-contribution.md与adr-portable-lifecycle.md形成；原Architecture final_plan尚待实际独立审查，候选文件不能冒充已通过。

shared CURRENT保持原值。先独立Architecture和candidate Check覆盖完整implementation/proposal，原owners在P7 final_integration合成完整有效定义、readback并判适用性，实施刷新全candidate，最终Architecture/Check/commit/committed Review覆盖实际晋升内容。source、dogfood或导航更改不代表目标安装已采用，P6/T09分别证明真实分发边界。
