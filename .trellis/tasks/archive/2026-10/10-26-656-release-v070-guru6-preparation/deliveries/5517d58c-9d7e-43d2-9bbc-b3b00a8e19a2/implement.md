# D1：v0.7.0-guru.6 发布准备实施与验证计划

## 1. 输入与引用

整体范围使用 [Task PRD](../../prd.md) 的R1–R8/AC1–AC6；本批需求使用 [D1 PRD](./prd.md)，实际方案和唯一来源处置使用 [design第3节](./design.md#3-来源设计处置唯一)。首次D1没有前序Delivery。固定内容B为 `abe3701acbd278a10f6c6ebbdc5bbe19a938916b`，PR target为main；后续H由真实实现/提交产生。

实施前实际读取：私有release contract的Stage1/Stage2/freshness/禁止持久化；原Check的candidate/final区分；TaskCommit的early/final和精确提交；BranchReview的独立完整审查与正式结果；current-knowledge的完整单元和final integration；当前lock/manifest、三README、public-docs及必要历史Test。正文模板和本方案引用通过原 `task.py add-context` 写入本D1官方implement/check JSONL。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原责任owner | 实际改动／可审核完成观察 |
| --- | --- | --- |
| I1 | 当前Planning激活后，原RDT/Architecture owners读取完整适用authority | RDT判断本批真实知识差额；无差额返回no-change，有差额在本Task隔离拟写完整目标。Architecture无新决策不造贡献/ADR；真实扩张回原owner。 |
| I2 | I1边界明确，实施owner | 修改canonical manifest version；upgrade-installation/runtime/owner.py两TARGET；package public output、package consumer、shared production consumer const；两个当前示例及必要current fixture。完整保留Fork lock、历史来源和旧行为fixture。 |
| I3 | 版本映射明确，文档owner | 修订README.md、workflow/preset README、唯一tracked public-docs的稳定.5/候选.6、当前79a97ed/CI39905440951及知识入口。保留真实历史和验证层次；provider同ref，候选由操作时实际SHA核验，不写未来自引用。 |
| I4 | canonical候选完整、V3b执行目标经原owners审查且独立副作用边界已满足，原preset/质量owners | 在唯一受控完整source repository执行真实首装及自有三平台full reapply，核对实际installed `.6`与完整投影；作者source/私有Skill parity单独检查。冻结及结束比较、变化失效、ordinary guard、sidecar沿第3/4节；不迁移作者历史或其它checkout。 |
| I5 | 实现及所有拟写完整，原独立Architecture/Check | 实施按固定B/真实HEAD/完整dirty begin_check；完成完整candidate Check；合法返回implementing后交原TaskCommit预览early提交。 |
| I6 | 精确提交另行确认并形成H，原独立Review owner | 审完整B..H、拟写、未改consumer和验证；首次只作为#656晋升前完整独立正式Review恢复承接，当前对话消费，不写公共Check/full_review。findings未清或缺必需证据不进入晋升。 |
| I7 | I6完成且内容/证据仍当前，原implementation/Architecture/Check/maintenance | 提交后的实际H重新candidate/begin_check及适用candidate评估/Check；原Architecture/RDT串行final_integration与读回。no-change不造空写。实施重绑所有actual after。 |
| I8 | 实际after重绑，原最终质量owners | 最终Architecture/Check→原TaskCommit必要dirty或clean reentry→提交后适用刷新→第二次完整独立Architecture/BranchReview。必须有真实checker/public wrapper passed，不能复用首次恢复结论。 |
| I9 | I8真实结果，原Delivery至Cleanup owners | publication/Delivery Review生成中文Refs-only payload；独立边界Publish/Ready/Merge；整体Completion→Closure no_mutation→acceptance-finish→Finish各独立动作和精确Cleanup。 |

各Git/GitHub动作的精确路径、ref/HEAD、命令/消息/payload和预期结果由原owner在该动作前展示并独立确认。此稳定计划不预授权commit、push、PR、merge、tag、Release或cleanup。

## 3. 验证入口、输入与预期观察

以下为本批计划，不能写成已经通过。依赖缺失记为实际FAIL/SKIP并停止真正依赖项。

| ID | 入口与输入 | 预期观察／对应AC |
| --- | --- | --- |
| V1a | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-upgrade-installation/tests -p 'test_*.py'`；tools受影响tests同原package入口 | 原正式来源/输出schema/consumer、迁移恢复和旧来源语义一致；当前fixture随目标，历史fixture不批量替换；AC1。 |
| V1b | quality-guidelines的in-memory Python Syntax Check；changed JSON以`python3 -m json.tool`解析；现有public-doc/README/版本断言按实际依赖选择 | 无语法错误、版本目标错配或无依据新测试；AC1/AC2。 |
| V2 | 独立核对三README/public-docs全文差额，`git show v0.7.0-guru.5:trellis/guru-team-extension.json`与同树lock，当前manifest/lock | 稳定.5自身CLI.4、候选.6自身CLI.5分开；同ref provider与真实SHA核验步骤完整；#630/#649/#669失败与未验证保留；AC2。 |
| V3a | 在作者 checkout执行原 source validator；V3b安装后在受控source执行 `./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`，分别加四个`--platform-root` | 作者 canonical有效；受控Shared/Codex/Claude/Cursor源码投影有效，并和实际installed bytes/modes一致；每项明确执行根，只证明对应分发层；AC3。 |
| V3b | 在下述唯一受控source根执行原 ownership；作者完整source的原preset首装后，从受控根运行 `./trellis/presets/guru-team/scripts/bash/apply.sh --repo . --platform claude --platform codex --platform cursor`、`./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json`、原 `check-dogfood-overlay-drift.sh --repo .` | 同一完整冻结源实际首装和full reapply完成；actual manifest `.6`、受影响runtime/schema及全部受管投影bytes/modes匹配，无drift或未处置sidecar；原guard不绕过，作者原apply失败不改写；AC3。 |
| V3c | 作者checkout四平台私有release Skill的SKILL/contract逐字比较；受控source全部受管mode及递归sidecar/residue检查 | 私有skill不进入公共inventory；受控对象Shared/三平台及完整受管mode匹配；作者与受控残留各自报告，既有未知资源不擅删；AC3/AC6。 |
| V4 | I5–I8原入口的实际语义结果、真实提交B/H、完整diff及maintenance读回 | 两轮完整独立Review，各自零开放P0–P3；实际after最终公共Check/full_review齐备；AC4。 |
| V5 | 原Delivery/Completion/Closure/Finish/Cleanup及live PR/Issue/Git | Refs-only准备与bookkeeping合并；Task正常归档；Closure no_mutation；AC5。 |
| V6 | `git diff --check`；`python3 .trellis/scripts/task.py validate <本TaskRef>`；完整dirty/untracked范围和Task正文审查 | 无未知差额、动态发布状态、body handoff或授权持久化；AC6。 |

V3b固定一个新建受控根 `/private/tmp/guru656-d1-controlled-source`，执行前确认不存在，不复用旧fixture或复制作者`.git`、Task、archives、session/runtime。只复制作者完整`trellis/`及其原modes；用`79a97ed`真实匹配build执行三平台 `init -y --workflow native-delivery-v1 --no-monorepo`，不靠手改Task/`.version`使预检通过。沿既有local_sample复制冻结Guru workflow，作者原preset对该根首装后，再从该根自身full reapply。原installer拥有生成的manifest、Python pointer、Shared和三平台公共资产；不手写安装receipt或fixture pass。

完整冻结以本轮内存中的paths/bytes/modes集合供复制前后比较，不生成tracked审计文件。首装与reapply期间作者canonical保持同一内容；结束时再次与作者比较。新差额、工具链/环境或必需义务变化交原owners判定失效与补验范围，组合影响不明则完整重验V3；没有变化不无因重跑其它已证命令。操作前必须成功fresh读取live #656及comments，核验相同source lock与匹配build，并展示完整目标/写集及原命令；本稳定计划不提前执行创建或安装。

升级包测试需要其真实依赖和Node；环境不满足不记通过。实际测试选择由原Check审其价值和归属；版本fixture修订不能顺便扩大迁移范围。官方工具源码未改，不重复专项平台/runtime/性能评测。Stage1不执行完整累计多平台throwaway矩阵。

tools的`test_native_install.py`是需原writer旧fixture及matching maintenance pair的opt-in组合用例。本批不改tools运行行为，其缺fixture不单独形成#656必过gate；实际SKIP及其未验证层次如实保留，不称通过。后续若原Check发现真实受影响义务，再按原owner选择匹配fixture补跑；该组合用例及其tools-only reapply都不替代V3b的普通完整reapply或Stage2。

Stage2精确candidate的source/installed/parity、ownership/reapply、focused Codex安装、真实前驱existing upgrade/退休资产、secret scanner、residue、完整独立发布审核和tag-pinned smoke由私有release合同原稳定入口拥有。准备验证不替代这些后续验收。

## 4. 停止条件与适用回退点

版本或源码锁冲突回原维护/Architecture；需求来源改变回Clarify/Author；实现/断言错误回实施/Check。实际候选或拟写变更时刷新受影响Architecture/Check/Review，工程事实仅经当前适用判断复用。

作者普通apply被旧archive校验拒绝时保留首次错误，按design第7节由原owners判断验证对象；不自动迁移历史Task或其它registered roots。受控目标的普通apply前置、完整安装、reapply或installed `.6`任一失败仍停止V3b，回原安装维护owner；不绕前置、不强写版本，不把作者旧安装validator或tools-only当本候选采用证据。存在用户修改或sidecar时沿原hash/冲突机制处理，不覆盖或删除无关文件。首次恢复Review与最终公共gate不能互相补造。

提交前失败保留真实working tree；提交后的恢复由原TaskCommit读实际commit/receipt，不重复提交。晋升partial/output-loss由原maintenance读回同意图，不重放已完成写入。没有业务数据库和生产部署，故没有数据/生产回滚协议；所有后续发布副作用仍在独立边界。

## 5. Delivery Policy（唯一）

Policy为full：D1覆盖整体准备范围AC1–AC6，没有预定延期切片。完成条件是版本/maintenance/文档/投影与必要知识差额一致，两次完整独立正式Review各覆盖其真实内容，最终公共质量链、准备合并及整体Completion/Closure/Finish/Cleanup正常完成。no-change不免除完整质量职责，也不制造空贡献或空提交。

Stage2不是本Task内延期阶段；它由#656在准备和bookkeeping合并后独立承担。本Task完成不代表软件发布完成，也不关闭#656。不得把未验证完整矩阵、业务升级、native-host、生产或live模型行为记为准备失败的扩展任务或已通过结论。

## 6. Docs SSOT Plan（唯一）

strategy选择delta_first。公开版本映射由实现/文档owner先在三README及本仓public-docs候选中展开；必要的当前知识定义由原RDT writer在Task隔离贡献中提供完整proposed targets，原Check/Review为直接consumer。原RDT task_impact_sync读取真实完整命中单元，判断addition/modification或no-change；不因发版强制全局知识升版，不复制未变单元。

命中引用为RDT-REQ-KNOWLEDGE的R331/R638/R648、RDT-DES-KNOWLEDGE的D638/D648、RDT-TST-KNOWLEDGE的T638/T648，以及Architecture change-contract/ARCH-GOV-008和distribution来源/分发边界。软件常量和来源说明变化不改变这些知识行为；若其定义无差额，原owner明确no-change即可，不建空贡献。真实过期的当前定义由原writer拟写，历史原始结果/失败不回写。

所有真实delta必须先通过晋升前完整独立Review，再由原Architecture/RDT串行final_integration合成、写入并读回，随后在最终Phase2前完成actual after重绑。Architecture没有真实decision差额时无贡献/ADR；扩大scope/owner/知识职责回原评估，不由本计划预批。导航只随真实关系变化维护，稳定authority identities保持。
