# D1：固定 Fork 来源并验证 Guru context/tools 采用——实施与验证计划

## 1. 输入与引用

整体来源为 Task 根 `prd.md` 的当前 accepted_scope；本批为同目录 `prd.md` 的 R1—R6/AC1—AC5。设计与唯一来源设计处置见 `design.md`，特别是§3、§5 lock、§6提交与正式采用顺序、§8验证设计。首次 Delivery 无前序业务结果；Fork PR #68/#69 和 e379 是跨仓前置，不是 Guru 已采用证明。

实施前实际加载：`trellis/presets/guru-team/README.md` 的构建、tools-only和官方投影检查；`guru-upgrade-tools` 完整 Skill/contract/Interface 与对应 public schemas；官方 workflow marketplace 安装文档；`quality-guidelines.md` 的 Test And Validation Value、Validation Scope Ownership；原 Architecture runtime-location、constitution/change contract，以及 `docs/{requirements,design,test}/current/runtime-location.md` 的完整相关条件。正式 source要求以 `guru-upgrade-installation/runtime/owner.py:formal_guru_source` 与 `guru-upgrade-tools/runtime/tools_owner.py` 实际检查为准。

B/H0 为 `ce4644392d1ed9815d59071388b9bff9978d1cee`。执行位置为本 Task checkout `codex/814-context-validation`；e943和Fork保留工作区只读。当前 Planning 尚未激活，本文全部执行步骤均为计划，不能将本文件的存在当作安装或验收成功。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原 owner | 文件、动作与可审核观察 |
| --- | --- | --- |
| I1 激活后核起点 | 原 Activation 已真实完成；实施 owner 加载 trellis-before-dev | 每批写入前执行原 checkout-boundary；核当前key/phase/B、源/目标、未终结重叠操作与并行状态。没有来源变化才继续。 |
| I2 精确构建 | 原source采用职责；确认新build目录/副作用 | 在独立 `/Users/wumengye/Documents/GoProjects/Trellis-builds/guru-814-e3793251` 从Fork e379构建，保留原Fork worktree。核Git identity、pnpm10.32.1、CLI/Core产物及public API1.0；成功后写原source marker。可审核产物为真实build/package identity与执行结果。 |
| I3 canonical采用 | I2匹配；实施 owner | 更新 `trellis/presets/guru-team/source/trellis-source.json` 到design§5组合，版本不变。需要的源码说明仅在现有README/source说明处更新。不开新Skill/schema或在Guru重写context。 |
| I4 开发工具同步 | 原 `guru-upgrade-tools`，完整本Task Guru source + I2匹配包 | 用显式Task checkout与 `local_candidate` 做read-only preview，检查实际受管写集、平台、AGENTS、冲突/sidecar；在原gate展示精确副作用，确认后一次prepare并冻结invoke。由原owner同步官方脚本/hash/version、Guru managed资产/receipt/lock与声明平台。真实tools_upgraded保留formal_fork_source_lock未验证标记。 |
| I5 定向工程验证 | I4原操作实际终结；实施/验证 owner | 按§3 V1—V5执行实际目标原生/计时/恢复/保持与投影。Task-owned临时driver只在确有缺口时创建，显式source/target，合法writer生成fixture；历史archive不改。可复用现有tools tests，不造通用框架。 |
| I6 知识整合与固定提交 | I5工程结果；原RDT owner及TaskCommit | 按§6唯一Docs Plan维护必要delta，原owner提交前整合/readback；无Architecture contribution。原TaskCommit审查完整真实差额并展示精确stage/commit范围，形成实际Guru H。Planning不执行此步骤。 |
| I7 正式H采用 | I4原操作终结；真实H、canonical trellis clean；原tools owner | 从完整H重新preview，以 `source_locked`、source_ref=实际H、workflow provider固定H，对显式Task checkout新建操作。重新审查实际写集后一次prepare/invoke；目标自身验证、同ref读回和保持满足才记录正式结果。不能修改旧local_candidate ref或把旧结果改为formal。 |
| I8 committed候选与独立审核 | I7结果与最终实际提交；原实施/TaskCommit/Review | 如正式采用产生实际内容差额，原owner纳入真实candidate并刷新受影响证据；保留source H和最终HEAD的区别。原constructor依据固定B和真实文件形成candidate，实施owner执行begin_check；一次独立committed Review审查完整范围和真实结果。PR/merge仍是另一个边界。 |

I2预计命令为克隆固定repository、`git checkout --detach e3793251fad8bd261d0c370d408c7675b9f6a140`、`pnpm install --frozen-lockfile`、`pnpm build`；全部成功后才执行 `git rev-parse HEAD > packages/cli/dist/.guru-source-commit`。产物布局不足时沿原README/packed protocol构建CLI/Core成对包，使用实际pack输出，不硬编码tarball名或文件数。

I4/I7均从完整source的 `trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/` 运行 `preview.sh`、`prepare.sh`、`invoke.sh`，参数由原schema与真实inspection提供；`--root`不改成执行旧目标dispatcher。公开 `tools_input`、upstream_source、platform/file decisions来自实际匹配API，不预写未来plan。每次新操作前检查现存未终结操作，恢复只用原plan/ref/preimages。

## 3. 验证入口、输入与预期观察

V1—V5与design§8逐项对应。顺序为来源可用性→实际开发同步→目标原生与保持/恢复→投影→文档/readback→H→正式source_locked目标证明。下面的命令是入口，实际执行状态届时分别记录。

- **V1**：在精确build目录读取 `git rev-parse HEAD HEAD^{tree}`、parents及实际CI；核package.json、成功build marker和真实CLI/Core根；运行public `getMaintenanceContract`/inspection，观察匹配来源与API1.0。H后执行原正式source校验；不以marker或版本互相比对代替来源链。
- **V2**：在Task-owned临时合法fixture的169规模及小拓扑执行实际installed `python3 .trellis/scripts/get_context.py --mode runtime-contract`、`--mode continuation` 和当前安装公开支持的显式Task入口，参数以该目标实际 `--help` 为准。经公开tools原probes观察10秒内真实结果。外部观测Git调用来源、次数和耗时；独立核Task/checkout/owner及必要peer查询，禁止从fixture自身期望值算出“正确结果”。
- **V3**：复用真实native/tools身份测试设施，覆盖实际缺口中的正常stale、conflict和非唯一拒绝，使用原公开writer/正常Git操作。读回安全diagnostic，核合法路径仍成功；测试不手改内部state/hash。保持比较从操作前独立快照到操作后读取实际Task/session/peer/common内容、mode与resolver选择。
- **V4**：复用 `trellis/skills/guru-team/packages/guru-upgrade-tools/tests/test_native_install.py` 真实wrapper/SDK和same-ref基础设施。先读其当前opt-in环境要求，提供真实匹配包；缺依赖记SKIP。实际prepare一次、apply原plan、使用原public recover/resume读回同operation；输出丢失时从同ref恢复结果。外层超时先查executor；没有自然内部超时则明确未复现，不新造权限中断/fault injection或重复prepare。
- **V5**：开发同步与正式同步分别跑目标自身resolver、installed package validation和native入口，读取actual public tools postvalidation。执行下列官方投影检查及drift检查，检查实际Claude/Codex/Cursor声明投影、mode、receipt、必要reapply与sidecar结果。源侧检查不替代目标检查。

```sh
python3 trellis/presets/guru-team/scripts/python/verify_dogfood_upstream_projection.py --repo-root . --fork-source /Users/wumengye/Documents/GoProjects/Trellis-builds/guru-814-e3793251 --json
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_verify_dogfood_upstream_projection.py
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
```

现有长期tests检测原工具/native保持与投影回归；临时driver仅定位当前正常规模开销。无需因Guru采用重新跑Fork未变的全部广泛测试，无需完整多平台throwaway/Release矩阵。任何新增实验必须回答真实剩余问题，不以测试数量证明充分性。#793首次失败、Fork受控结果、本次开发结果、正式H/目标结果与未验证项分别保留。

## 4. 停止条件与适用回退点

- key/generation/checkout/phase不匹配，停止写入并回原Identity/Ensure/Bind/Selection。每次写入前重新过boundary，不使用e943代写。
- 精确Fork源码、构建、Core/CLI、API1.0、真实source H或原owner能力缺失，停止依赖它的采用/验收；不改PATH遮蔽、不只改.version、不手抄managed副本、不降级validator。
- source/path/candidate/owned freshness或原peer/common观测变化，回原tools owner检查原操作；不换ref、plan或preimages，不把正常新增隔离peer当作全局冻结理由。旧操作未终结前不能形成H或重写source。
- 真实范围/来源承诺变化回原Clarify/Author；机制变化回原Architecture candidate assessment并刷新受影响规划。普通实现缺陷和缺证据留原实施/验证职责，不新造scope确认。
- 预算内失败、身份错误、保持变化、projection/drift或sidecar未解决，保留首次失败并停止相应验收。反复设施失败先缩到真实入口和依赖重评；未解决不能预填通过。未知旧超时因果不阻止有依据的开销修复，但必须保持未复现边界。
- rollback只由原owner依据固定preimages和public兼容条件处理，先public后Guru，保留后续业务和并行改动。没有数据库或服务部署迁移，不新增发布回滚协议，不reset/rebase/删除工作区。

选定验收和必要回归已充分时停止追加验证。没有新问题不重复counterfactual、整套矩阵或人工故障；skip、源码通过、安装通过、实际恢复分别标明。当前停点仍是Planning审核后、Activation前；本文不授权工具安装、build、commit、push或PR。

## 5. Delivery Policy（唯一）

**policy=full（针对选定本批范围）**。本批完整交付R1—R6/AC1—AC5：精确Fork来源、canonical与managed采用、正常规模native性能/身份、原预算、安全诊断、同候选原ref接续与Task/session/peer/common保持，以及必要RDT差额。没有延期的技术子能力，不用额外空Delivery承载bookkeeping。

本批完成条件是：真实H及匹配source_locked目标结果、V1—V5足够证据、必要文档整合/readback、完整committed Review/readiness和后续原Delivery结果。开发local_candidate的formal_fork_source_lock限制只在真实H新操作成功后解除；它是该开发证据的限制，不是整个Task冻结。旧内部超时未自然复现仍是证据边界，不能由新操作成功抹去。

整体R7/AC6由原Completion确认所有accepted scope和实际交付，再由Closure/Finish处理Issue与归档，并核live main可达。Delivery合并不等于Task完成；完整Release矩阵及其他业务仓采用不由本批承诺。没有跨Delivery新数据合同或未分配的实施责任。

## 6. Docs SSOT Plan（唯一）

**strategy=delta_first**。原writer为 `guru-maintain-requirements-design-test-ssot` 的适用task-impact/integration profiles。命中完整单元为：`docs/requirements/current/runtime-location.md` / RDT-REQ-RUNTIME-LOCATION，`docs/design/current/runtime-location.md` / RDT-DES-RUNTIME-LOCATION，`docs/test/current/runtime-location.md` / RDT-TST-RUNTIME-LOCATION。保留现有source/target、R718/D718/T718、R769/D769/T769语义和各历史观察截止。

真实delta限定为本次context正常规模来源采用、原预算/身份/同操作保持合同的必要承接，以及实际工程观察与正式来源尚未/已经验证的边界。Requirements只补真正缺失的长期行为，Design只补原owner采用顺序与精确来源职责，Test记录必要验证策略及有截止的实际观察；不为凑三层同时改写未变正文，不把某一次计时固化为全机器SLA。完整规范处置见design§3。

直接consumer为本批实施/验证、提交后的独立Review，以及Task Completion的真实证据判断。实施后由原RDT owner形成非空真实delta，在本地TaskCommit前final_integration并readback，状态仅为integrated_pending_review；同一committed Review审核before/after。若H之后有正式验证新结果，原owner按实际差额维护并刷新必要提交/Review，不预填未来成功或自指最终HEAD。

Architecture引用 `docs/architecture/01-current/runtime-location.md`、constitution和change contract。当前候选no_architecture_impact，不建contribution/ADR；final_plan或实施出现真实影响再回原owner。Planning仅写本Delivery正文及必要official JSONL，不写共享current/index/manifest或空proposal。历史Fork archive与#793观察保留原样。若本批真实delta改变原维护合同要求的导航或spec投影内容，由原维护owner同步这些受影响项；内容未变则保持。不新建平行ledger。
