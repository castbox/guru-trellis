# #861 gen2 D2：正式采用实施与验证计划

## 1. 输入与引用

完整读取根../../prd.md、本批prd.md及design.md；唯一规范性来源设计处置为design§3。Task/gen2/D2 key、scope/root来自原public current。固定B/H0=343bc3100ea8f157bfd20d7a6a226455dbe482f4；source M=2938801829c8b8862e71d522891c79e8efb2d47a，不能互换。

实施前加载Author planning-body及design/implement模板、quality Test And Validation Value/Validation Scope Ownership、workflow Candidate Applicability And Coverage、原tools完整Skill/contract/install输入/private-prepare与actual public maintenance协议、原Sync、private release Stage1/真实采用/独立确认及Stage2。设计§9定位RDT/Architecture完整必要单元，before-dev加载受影响包规范。所有Python禁bytecode；每批Task写前fresh checkout boundary。本轮仅完成规划审核并展示，停Activation前。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 原owner、动作及完成观察 |
| --- | --- |
| I1 规划 | Author三正文/context→独立candidate/final Architecture→Approval→展示计划。本轮停点；不执行后续写入 |
| I2 来源 | 未来原Activation后，原Sync对clean primary main fetch/ff-only取得完整M。核实际HEAD/source/lock，primary仅供应源，不安装。main超M先评差额刷新来源 |
| I3 只读计划 | 从完整M canonical launcher preview，核Fork/API/target/peer、相交事务、managed edits、actual inspection；不猜hashes或旧dispatcher |
| I4 正式采用 | tools prepare一次，读完整result.plan；展示真实写删/保留及invoke命令，取得该安装独立确认再执行。实际写入仅原writer，原operation恢复，不重prepare |
| I5 目标验证 | 原tools/实施owner执行V2/V3，核全部installed after、native/保留、真实same-operation reapply/drift和零sidecar；失败原ref处理 |
| I6 兼容 | 实际M采用后执行V4一个完整.9→M Codex existing及aggregate；不预设需改driver，不用focused/tools exit替代 |
| I7 知识/交付 | 原RDT/Architecture对真实after复核，必要完整整合/readback；原TaskCommit另确认后固定完整B..H，新的独立完整Check/Branch Review、readiness、Refs-only Publish/Merge，分别保原边界 |
| I8 整体后继 | 实际delivered交原Completion判断所有准备责任；reference-only Closure/Finish及Stage2仍各归原owner，本轮不执行 |

预计产品差额是四处受管Discovery commands.json及installer产生的provenance/投影after；实际完整文件集以I4原plan和Git after为准，不人为限制为四文件、不纳入并行改动。canonical生产机制/测试/manifest定义当前无变更计划。历史资料不回写为新pass。

## 3. 验证入口、输入与预期观察

### V1 clean source与一次tools计划（A-AC1）

原Sync public invocation为operation=sync、base_branch=main，使用唯一clean注册primary authority，读取其完整当前合同再调用。目标source取得后必须HEAD==M且canonical clean；不一致先由原来源owner判断，不用M的source_ref执行新HEAD。完整source为/Users/wumengye/Documents/GoProjects/guru-trellis；tools target是gen2 checkout；Fork为/Users/wumengye/Documents/GoProjects/Trellis，HEAD e3793251fad8bd261d0c370d408c7675b9f6a140，CLI/Core .6。匹配build marker、锁定包byte identity和maintenance capability必须实际核实，路径或版本号不证明匹配。

TOOLS_INPUT为design§5的完整install/source_locked对象。UPSTREAM_SOURCE由原transport实际inspection形成，PRIVATE_PREPARE按原schema及真实public prepareToolsInstallation输入组装。使用完整M source公开入口：

    bash "$SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/preview.sh" --root "$TARGET" --input "$TOOLS_INPUT" --upstream-source "$UPSTREAM_SOURCE"
    bash "$SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/prepare.sh" --root "$TARGET" --input "$TOOLS_INPUT" --plan "$PRIVATE_PREPARE"

各JSON可用本owner临时regular UTF-8文件；不放Task。preview/prepare原stdout是intermediate receipt，完整捕获exit/stdout/stderr后投影result。保prepare唯一result.plan为FROZEN_PLAN，不重构或二次prepare。workflow canonical全文、immutable M provider、ownership=custom；AGENTS恰一custom、actual source snapshot和原全文base交原renderer，核renderer-idempotent。平台来自target的Claude/Codex/Cursor；config原bytes preserve。逐路径Guru决定与public required/skip/user-edit规则按inspection，完整写删集不得触及Task/archive/workspace/session/config/peer/common。缺能力、相交事务或unknown编辑沿原owner，不转full migration。

### V2 正式写入与目标证据（A-AC2/3）

原tools owner审实际source、target、所有写删/保留、pointer、sidecar和完整plan，展示精确invoke后取得本次写入确认。未来执行：

    bash "$SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/invoke.sh" --root "$TARGET" --input "$TOOLS_INPUT" --plan "$FROZEN_PLAN"

预期tools_upgraded、installed_version .10、unverified无formal_fork_source_lock；结果单独不证明内容充分。原installer生成实际manifest，核source repo/ref/commit=M、clean immutable来源，extension/CLI/source lock、完整current inventory与所有受管投影。不得手改manifest/hash或恢复历史schema为current。

原operation在安装区间保留Task/archive/workspace/session/public/private control、config、peer tools及common/peer pointers；只允许目标自身checkout-local runtime pointer与原recovery变化。原tools保存事实只供其直接consumer短期使用，不另写ledger。目标配置核原bytes；AGENTS核原renderer结果及区块外保留，不把它当raw模板。

目标自身runtime/resolve-python.sh运行解释器probe、installed package validator：
    bash "$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" --root "$TARGET" --mode installed --json

以目标解释器执行目标.trellis/scripts/get_context.py --mode continuation及public Delivery current/Identity/Ensure入口，观察同Task/gen2/D2在合法implementing阶段可继续原owner。source resolver不能冒充target执行，不能借其它session身份或更改环境identity。旧历史Task仍按维护合同诊断，不转换以换验证通过。

### V3 全量投影、四help、真实reapply/drift（A-AC3/4）

使用M原installer managed_source_projections形成全部预期映射；比较完整集合、每个文件bytes与可执行位（此前集合10,002条，仅为起点统计，不硬编码正确数量）。逐域核runtime/packages、shared/.agents及Claude/Cursor、overlay、workflow、spec和lock；config/AGENTS/manifest等生成或preserve对象按其定义独立验证。无未声明公共投影、旧受管.codex/skills/guru-*、私有runtime/tests泄漏或未处理sidecar。

运行installed Discovery四个实际command help：record-context-discovery、check-context-discovery、invoke-guru-discover-change-context、read-change-context-source。从实际帮助取得声明schema，对requirements/wording_only两个context_request正常输入与该包issue_readiness_supplement1.0分别验证；按D1现有test_runtime.py同一正常样本方式执行原issue_review.invoke，观察context返回identity和supplemented身份不丢失。完整保留原public input、声明、输出；不mock被测返回，不把此受控入口证据说成live GitHub/客户端业务成功。

真实reapply使用同frozen source/plan/recovery_ref，复用原tools tests/test_native_install.py的已有install_assets路径。只有同operation owner读取自己的actual checkpoint upstream_ref，原值传入tools_maintenance。调用M原installer：
install_assets(M/trellis/workflows/guru-team, TARGET/.trellis/guru-team, TARGET, set(frozen selected_platforms), python=目标实际resolved解释器, checkout_local=True, tools_only=True, tools_maintenance={source:原upstream_source, plan:原upstream_plan, recovery_ref:actual upstream_ref})。
若原operation包含preserve/retirement决定，沿其实际参数保持；不新wrapper、复制算法、刷新checkpoint或prepare。观察skill_installed_validation.returncode=0、package/overlay status及所有保存项。complete后resume只验证，不能用它充作reapply；无法合法完成则保具体gap回tools owner。

原dogfood脚本的--repo同时选择canonical与installed根。因此先证明target canonical受管来源与M全部相关bytes/modes一致，再执行 bash "$TARGET/trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh" --repo "$TARGET"；它实际读取target自身canonical与installed。另重核M到target完整mapping，不用本地同源推断取代M绑定。若canonical实变，保原drift输出并回原owner，不修改canonical或副本制造同源。递归扫描.new/.bak/__pycache__/.pyc/.pyo；原owner逐个处理真实sidecar，不直接删未知文件制造pass。target native/installed及preservation再次核。

### V4 一个完整前驱existing（A-AC4）

前驱tag v0.7.0-guru.9 peeled ac1c823857ad6695c106daeedd25aafce4c50934；前驱manifest/lock均CLI .6、Fork e379325，运行时重新核。新源已实际采用后，从完整clean M执行原shell，显式提供新临时WORK_DIR以保留完整结果；PATH选择已验证的Python3.12供最初bootstrap，后续由原shell的source-managed bridge/resolver负责，不手写bridge：

    PYTHONDONTWRITEBYTECODE=1 TRELLIS_FORK_SOURCE="$FORK" TRELLIS_PREDECESSOR_SOURCE="$FORK" TRELLIS_PREDECESSOR_COMMIT=e3793251fad8bd261d0c370d408c7675b9f6a140 TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#2938801829c8b8862e71d522891c79e8efb2d47a bash "$SOURCE/trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh" "$WORK_DIR" --mode existing --platform codex --before-tag v0.7.0-guru.9 --before-cli 0.7.0-castbox.6

该原shell实际执行bootstrap/routing inventory、完整run_existing及aggregate，原结果JSON为WORK_DIR/matrix-existing-codex.json。确认driver真实init、前驱preset、source_locked升级、reapply、全部validate_cell、AGENTS维护前像、source/Fork前后检查及aggregate，而非仅局部validate或tools_upgraded。M已包含前序driver修复，当前不计划再改；若失败保首个真实结果，原owner判断环境/源缺陷及最早返工点，不预设重复gen1修复。不得以旧driver/修复后driver混报，或只用父Python绕过子进程路由。只有完整cell和aggregate通过才满足本承诺；Stage2仍对最新候选重新执行原门禁。

### V5 工程事实采用及完整交付（A-AC5）

D1 V1四例、Discovery12例、source42packages/123commands、三平台临时完整安装/reapply、完整map及三OS CI是各自原对象事实，不自动给D2通过。可核验且输入/依赖/工具链/参数/检查定义/期望保持时采用，不因Delivery/reviewer变化重跑无关175suite；新target及existing必须当前执行。语法仅对真实新增Python用内存compile；git diff --check和实际受管范围检查仍执行。

I7由原owners亲自完成知识判断及完整交付，不用几条命令代替Check或把安装exit当Completion。独立Review涵盖全部fixed B..H、必要未改consumer及保留/验证边界。当前无tag/Release/真实客户端Agent全链/生产/累计矩阵通过声明。

## 4. 停止条件与适用回退点

identity/checkout/selection/scope不符回原owner；source HEAD/clean/M、Fork build/API/lock不符停来源步骤；相交事务、unknown edits、sidecar、保存项差异、target不可用或必要验证失败停tools/验证owner。真实机制变化回Author/Architecture，scope选择回Clarify。main推进不自行改变fixed B或重复D1。

原same-operation ref恢复不新增prepare/plan；bounded rollback另由原tools评估public兼容及精确写集，不reset/rebase或覆盖后续业务/历史。无需数据库/生产回滚协议。设施失败重新选择能命中同承诺的真实复现方法，不能无止境修设施或声称缺口已过。证据足够后停止可选实验；必要验收未满足保留为缺口。Git/GitHub动作仍各按原边界，当前不执行。

## 5. Delivery Policy（唯一）

选择full，指当前选定正式采用切片全部责任：A-R1–6/A-AC1–5，含真实source_locked、完整target/preservation/native、同操作reapply/drift及一个existing、必要知识及actual delivered，不再把采用推给“补证据”。进入需本批Planning/独立candidate/final/Approval、当前计划接受和原Activation；tools安装仍需实际冻结写集的独立确认。完成需全部验证及本批原完整质量交付链。

前序“完整源未交付不得正式采用”的局部限制已由D1 actual delivered解除来源交付前置；实际安装尚未发生，目标旧installed差额只在本批真实after验证后解除。Task其余整体Completion/Closure no_mutation/Finish终态归档由原owner执行，不因full标签或merge自动完成。Stage2最新main候选、tag/smoke/Release及primary发布后收敛另有原边界。没有其它Issue状态前置。

## 6. Docs SSOT Plan（唯一）

strategy=no_docs_update_needed。命中docs/{requirements,design,test}/current/codex-skill-distribution.md的R724/D724/T724及ARCH-INT-001/006/014/015；它们与原tools/private release现行合同已定义完整匹配采用、单writer、状态保留和证据分层。本批只完成已有工具采用，不改变当前公共语义、API或架构；不新增版本/ledger/贡献/ADR/导航，历史结果保持原截止点。

原writer为guru-maintain-requirements-design-test-ssot及guru-maintain-architecture-baseline；直接consumer为实际实施、独立Review及整体Completion。真实after与工程结果若揭示当前规范/指南差额，先由Author刷新本唯一策略和受影响规划，再由原owner提交前完整final_integration/readback，TaskCommit纳全部after，之后同一次独立committed Review审before/after。当前无差额不造空整合产物。

