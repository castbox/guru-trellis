# 组合交付源采用与完整 existing 设计

## 1. 设计目标、需求承接与内容基线

本批承接PRD A-R1–6、A1–6、A-AC1–5，选中整体R3/R4/R5/R11、AC2/AC3/AC7/AC9；不改变整体收尾责任。目标是repair真实采用与原完整existing，并修原verifier必要的阶段前像承接及直接回归；不改变受分发工具行为。

development B固定为前序实际delivered head `f09afb891cfae105ee808c137301e182804b6092`，它是当前HEAD的唯一最近前序delivered head；Planning H0同B。前序merge `79c25b5eaafdbcf415393535a16a7b1c0d281284` 是本次采用源C，包含main #868/#872；C不是替换B的理由。PR目标main与固定内容范围分开；原constructor后续保持前序B并包含全部真实after。需要base整合时只走原Reconcile，不能reset/rebase缩范围。

baseline/constitution/change-contract为 `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md`。本批独立candidate_assessment实际返回baseline_current/no_architecture_impact：复用现有Sync/tools/Fork/installer/verifier，无新owner/状态/架构决定，无contribution/ADR；该结果不替代final_plan。

## 2. 当前系统、边界与目标差额

首次规划观察的repair installed版本为`.10`、来源为gen0 `b3525d4b052f79f7d9cb4a18f827ff7c990f1983 / dirty`，该原安装登记216项输入；canonical本轮退出11项，原exact gate核实际集合。版本相等不证明采用。目标exact selection为Claude/Codex/Cursor，Codex使用共享`.agents/skills`。source manifest/Schema历史/selector/Fork lock保持前序已审语义。

主目录 `/Users/wumengye/Documents/GoProjects/guru-trellis` 在首次规划时clean、HEAD `434b207fe2d5df75a75ed9552cf17c02a9504527`，仅作后续干净源位置。该起点不代替后续live事实。未执行的来源操作在计划接受后由原Sync取得main；只有实际HEAD为C，才以source_ref=C进入正式tools。目标仍repair，主目录与peer不进行tools安装。

本批实际写入由原tools完整计划确定，主要是`.trellis/guru-team/**`、managed spec、shared/Claude/Cursor Skills及平台overlay、workflow和checkout-local Python pointer。同步C的#868/#872合同/投影与本manifest修正一并采用，不只手改11项。用户配置及Task/session/peer保持。新增canonical改动仅为 `trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py` 与 `test_verify_trellis_upgrade_contract.py`；二者不在本次managed projection中。原C安装资产及provenance不因driver修复改变。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置与落点 | 理由/影响及原owner |
| --- | --- | --- |
| release Complete Source Before Actual Adoption：完整source delivered后才建后继 | retain；§1/2/6 | #871已delivered，Completion/Creation已按顺序产生本key，不拿未交付源或样本代替 |
| release/tools：正式source_locked、完整matching Guru/Fork/CLI/Core | retain；§4/5/8 | C完整组合源及其自身lock，原tools验证，不降local_candidate |
| tools Forward behavior：target selection、workflow custom、AGENTS custom renderer、prepare一次 | retain；§4/6 | 原public maintenance与Guru installer单写，不复制executor或renderer |
| tools保留/冲突/恢复：Task/session/user/peer/common隔离，固定ref/preimages | retain；§4/7 | 原preview核真实目标，部分失败原操作恢复，不绕历史guard |
| root R11/AC7/AC9与前序Policy：新清单实际采用并完成真实`.9→.10 existing` | retain；§6/8 | 当前是未实施工作，完整existing不能由tools_upgraded/focused替代 |
| #868责任边界/证据去重规则 | retain；§8及implement验证 | 只证明本批原承诺；采用/existing由root明确要求，不新增客户端或业务E2E |
| #872线索与draft绑定指引 | retain；§2/4 | 作为完整C已有正文/投影采用，不改检索/schema，也不重做其验收 |
| 整体R9/AC7、A-R5/A6：维护后baseline对应真实阶段前像 | retain；§4.4/8 | 修原verifier承接，不改hash、renderer、用户正文或未知漂移拒绝 |
| release Whole Completion/Stage2/独立副作用 | retain；§6/7 | 本批交付后才整体Completion，正式发布仍最新main；Refs-only，不关闭#861 |

没有change/reject设计承诺，无新增compatibility parser或双写。

## 4. 模块、职责与设计取舍

### 4.1 完整源与单目标

原 `guru-sync-base(operation=sync, base_branch=main)` 仅在唯一clean primary注册checkout执行fetch/ff-only，使实际source root到C；不切换repair分支、不重置其元数据。实际main若超C，先检查C到新HEAD的完整source/消费者差额，原Author/Architecture刷新受影响判断与source_ref，不能用C标签运行新HEAD。当前方案不预先授权未知源变更。

选择复用现有clean primary作为源，避免额外source分支/worktree。Git source同步不是primary tools采用；它的实际Git副作用在执行前展示。若primary dirty或无法唯一解析，原Sync停止，不改用较低优先checkout或临时复制代码。原tools从source的完整 `trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/` 运行，`--root`指repair，不能用repair旧dispatcher安装自己。

Fork复用 `/Users/wumengye/Documents/GoProjects/Trellis@e3793251fad8bd261d0c370d408c7675b9f6a140` 现有clean build；CLI/Core均`.6`，tree/CI/marker/package bytes/modes由原transport核对。若缺构建，按该源声明正常pnpm构建，不固定执行pnpm版本或改packageManager。

### 4.2 原tools维护

preview读取实际旧manifest/managed hashes、平台、peer/common观察、公共维护inspection与相交未完成事务。以其实际snapshot构造public tools_input：workflow install/custom，template guru-team，provider `gh:castbox/guru-trellis/trellis#C`及C完整workflow；恰一AGENTS action=custom，以目标原全文为base交原renderer，只更新Guru block。public config按真实inspection保留；`.trellis/guru-team/config.yml`依原非受管用户配置规则保持。未知managed edits逐路径在原owner审查preserve/replace，不先覆盖再消除差额。

prepare一次后完整消费result.plan，不修改public operation/plan。确认AGENTS目标renderer幂等、write/delete不触及Task/archive/workspace/session/user/peer/common，显示精确写集后另确认invoke。已成功的原prepare/invoke沿其真实frozen输入、plan与ref消费，不生成第二计划；未执行的新安装须先展示其真实写集。正式输入不接受local_candidate替代；manifest由原installer产生，不手工修改。

### 4.3 完整existing

用§4.4绑定的C产品资产与修复driver从真实tag `.9` 安装开始，执行完整单Codex existing。已读前驱tag peeled commit `ac1c823857ad6695c106daeedd25aafce4c50934`；其manifest target CLI与lock CLI均`.6`、Fork均e379325，可复用同一匹配build。仍由原入口实际建立before状态/安装/原tools升级/全部validate_cell，不从手工fixture生成升级结果。临时target与repair正式采用分开。

### 4.4 verifier 阶段前像与完整执行源

保留init后由 `_capture_agents_preimage` 验过hash的前像。existing在原 `_upgrade_bootstrap_fixture` 前另读取当时真实AGENTS bytes；这是前驱preset后、tools维护前的文件，不提前称为当前baseline对应前像。仅当实际维护结果为 `tools_upgraded` 时，将该维护前像交最终 `validate_cell`；其它既有维护分支仍保init前像。`_known_agents_projection` 继续要求前像SHA256等于实际当前template baseline、磁盘after精确等于原renderer输出。不得改hash、补写after、从after反推前像、忽略unknown drift或跳过失败。

职责仍为public tools写baseline、preset写Guru block、verifier核真实更新阶段的输入/输出。只改原coordinator传递与直接回归，不新增API、字段、状态或通用前像框架。组件回归可隔离外部maintenance，但须观察真实 `_run_cell` 的阶段传递及原hash/renderer gate；真实完整existing另用原writer，不能由fixture代替。

完整执行使用repair修复driver的原公开 `run --mode existing` CLI，显式 `--repo-root` 指完整clean primary C。产品资产、Fork/lock、immutable provider、前驱、tools launcher、source state及完整 `_run_cell/validate_cell` 均从C原入口取得；driver字节明确来自repair候选，不称C旧driver通过。原C shell的bootstrap/routing/inventory前置仅在输入仍适用时采用；完整cell后执行原aggregate，不能以局部validate/focused替代。

driver及其子进程必须继承原C完整shell已生成的 `source-managed-python-path/python3` bridge：读取真实work root，核可执行文件正文仍绑定C原resolver/root/runtime，实际probe落到原hash-locked解释器，再将该目录置于PATH首位并设置 `TRELLIS_PYTHON_CMD=python3`。不能只指定父Python而让子进程回到系统Python。bridge来自原shell正常producer，不手写替代wrapper；缺失或来源不符先停原环境owner，重新取得原shell前置后再执行。aggregate使用相同环境。

实施前逐项核driver命中依赖与C的bytes/mode：SCRIPT_ROOT errors/support/platform/native helpers、fork_session_probe、renderer installer及imports、`__file__.parents[5]/trellis/skills/guru-team/runtime/installed.py`。差额仅允许本批verifier/test；其它不等价回Author。原CLI已支持显式repo-root，不新增launcher、monkeypatch、复制算法、临时source commit或worktree。此方案保持C干净和repair fixed B；Stage2仍待修复合入后以最新main完整wrapper重验，当前driver证据不代替它。

原dogfood drift脚本在repair内比较的是repair的H canonical与已采用C的managed副本。保留其真实差额输出，不将其改报通过；本次采用的drift判定以完整C expected map对目标的集合、bytes/mode、hash/provenance为准。不得为消除此源版本差额而同步repair HEAD、修改canonical或手修副本。Stage2最终main自身的dogfood门禁仍单独执行。

## 5. 接口与数据

无新公共字段/schema/Skill/exit/数据库或持久模型。tools install输入是source_ref=C、dependency_mode=source_locked、checkout=repair绝对路径。upstream_source绑定实际CLI/Core package roots与身份及source roots；private-prepare包含该descriptor、selected_platforms、guru_decisions和原tools_input。原preview/prepare receipt.result不是semantic pass；invoke原tools_upgraded只是目标工具结果，不是Delivery/Task完成。

current清单按C active Interface exact规则；历史schema及Sync3.0→2.0分支原字节保留。fixedB、sourceC、workflow provider、目标installed provenance各归原consumer，不互换。Task规划只保存稳定方案，不保存授权/事务审计或动态pass。

## 6. 状态、顺序、正常与失败流程

1. 当前需求→独立candidate→Author方案/context→独立final_plan→Approval。展示本轮修复完整方案；原Activation只接受当前方案，已成功来源/tools不重复。
2. 计划接受后原Activation，再按单独展示的Git来源同步取得完整C；复核source/目标/Fork/事务，原tools只读preview。
3. 已成功原操作只消费实际结果及仍适用证据，不重复prepare或安装；尚未执行者核实际路径决定，prepare一次；完整读取frozen plan并显示目标/source/写删集/命令，独立确认后invoke。缺前置/未知编辑先停，不普通apply或转installation migration。
4. 实际工具usable后核目标自身入口、完整资产/保留、同operation reapply/drift；按§4.4先完成必要driver修复，再执行完整existing。第一真实失败保留，source缺陷回原writer，不用reapply或工具exit0掩盖。
5. 原RDT/Architecture复核真实after，必要整合/readback；TaskCommit另确认，constructor/begin_check保B，新独立Review审完整B..H。readiness/Publish/Merge各原边界；实际delivered后Completion重评全Task。

## 7. 恢复、兼容、迁移与集成

本批不转换历史Task或重写gen0。source repair与#868/#872共存是完整已交付C，原组合审核不代替本目标采用。当前旧installed可继续支撑规划，解除条件是本批正式source_locked和目标验收，不是修改版本号。

相交未完成操作先回原Skill/provider/ref，不读他人private checkpoint。新operation部分失败按原resume_required和相同source/plan/ref续接，不重新prepare、扩preimages或吸收后来工作；rollback另审兼容与写集，不reset Git。源码/计划实变回原受影响owner。

原tools-only reapply须消费同一次public source/plan/recovery_ref，保持tools_only=true；不能用普通full apply绕历史Task guard。无法合法执行则保具体验证缺口，不预称通过。PR/交付后的whole Completion、Closure/Finish与Stage2仍独立，当前禁止收尾/正式发布。

具体重投影沿原 `guru-upgrade-tools/tests/test_native_install.py` 的同操作入口：同一tools owner读取自己当前operation的实际public upstream ref，使用冻结plan的upstream_source/upstream_plan及selected_platforms，经原source installer `install_assets(source/trellis/workflows/guru-team, target/.trellis/guru-team, target, selected_platforms, python=目标已解析解释器, checkout_local=True, tools_only=True, tools_maintenance={source,plan,recovery_ref})`。真实preserve/retirement参数沿该operation决定保留；调用原函数，不复制安装算法，不改checkpoint，不新prepare。原函数在写前验证实际已applied public operation。`resume`在complete阶段只做postvalidation，不是该reapply入口。

## 8. 验证设计

| 验证 | 对应/层级与入口 | 观察与边界 |
| --- | --- | --- |
| V1 | A-R1/A-AC1；原Sync、source_locked preview/prepare | source实际HEAD/完整canonical==C，含三项交付；Fork build/API/modes、目标平台/冲突/保留和frozen写集。preview不是安装 |
| V2 | A-R2/3/4、AC2/3；原invoke与目标自身入口 | tools_upgraded/unverified无formal-source缺口，目标resolver/installed/native及完整expected bytes/modes/current API/workflow/lock/provenance、Task/session/user/peer保持，零sidecar |
| V3 | A-R3/4；同operation原tools-only reapply、drift | 不重prepare，不回full apply；完整受管内容与保留关系稳定，未处理冲突不算通过 |
| V4 | A-R5/A6/AC4；§4.4原完整existing CLI及aggregate；真实.9、C产品资产、修复driver | 完整真实before升级结果、退役资产、AGENTS精确hash变换、平台规则、零sidecar；不替代repair采用/真实Agent/Release |
| V5 | A-R6/AC5；原知识/TaskCommit/完整Review/交付 | 全部实际after进入B..H，Refs #861；实际delivered后才能whole Completion，不预称发布通过 |

前序source回归与三平台临时安装facts只在输入/依赖/定义/预期仍适用时采用。本批不重跑完整175项历史suite，不因stage变化重复source验证；完整C加入#868/#872的实际目标资产必须比对，不能仅用旧H样本证明。本轮直接回归覆盖真实阶段错配，不扩同质长期tests；本批临时实验止于明确责任边界，已有外沿证据充分时不重复内部层级。必要目标验证和existing不能省略。

## 9. Canonical 引用、本轮差额与实际未决项

同PRD§7的R724/R630/data-contracts/MIGRATION-861与ARCH-INT-006/014/015；本批实际采用和验证不改变这些定义。原RDT/Architecture实施后核真正知识差额；无变化不建空contribution/ADR/导航。新知识差额先更新本唯一Docs策略，再原owner整合/readback。

没有未决产品选择。必要driver修复及其C资产绑定按§4.4实施；完整existing仍须实际通过。新方案仍需final_plan、Approval及规划接受后再实施，不预填成功。
