# D1：固定 Fork 来源并验证 Guru context/tools 采用——设计

## 1. 设计目标、需求承接与内容基线

本批承接本目录 PRD 的 D1-R1—R6、D1-S1—S5、D1-AC1—AC5。目标是采用已交付的 Fork 原生修复，并证明 Guru 的实际工具目标可用。没有前序业务 Delivery。Task 整体 R7/AC6 由后续 Completion、Closure、Finish 承担，不能由本批技术证据替代。

固定 development baseline B 为 `ce4644392d1ed9815d59071388b9bff9978d1cee`，来自本 Task 创建时选定的 `origin/main` 固定对象；Planning H0 同为该对象。未来内容范围由原 constructor 依据 B、实际 HEAD 及本批真实文件产生。未来 PR 目标是 `castbox/guru-trellis:main`；main 后续前进不自动改变 B。H 指未来真实 Guru 内容提交，不是当前 H0，也不是 Fork commit。

Architecture authority 为 `docs/architecture/README.md`、`docs/architecture/01-current/runtime-location.md`，constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `docs/architecture/06-governance/change-contract.md`。独立原 Architecture owner 的当前 `candidate_assessment` 已返回 `baseline_current / no_architecture_impact`：只在既有 lock 和单 checkout tools owner 内采用修复，没有新 Guru authority、持久状态或公共接口。该结果只允许方案展开，不能替代 Wording 后的 `final_plan` 或最终实现审核。

## 2. 当前系统、边界与目标差额

canonical `trellis/presets/guru-team/source/trellis-source.json` 与 installed `.trellis/guru-team/trellis-source.json` 当前均锁定 Fork `aa898d090fc27c9ce6145cfa3c787a6f400da4e2`。Fork 已交付原生 `RepositoryFacts` 内的成功观测复用、合并 Git 查询、既有分支拓扑筛选与安全 probe 诊断。Guru 不复制这些官方实现。

本批 canonical 差额首先是 lock 的 commit、parents、tree、CI identity。官方模板脚本、hash、版本、Guru lock/manifest 和实际声明平台的安装差额由原安装 owner 生成。实施时以真实 preview 为准列明每个写入、删除、保留、冲突及 sidecar，规划不伪造 manifest 或固定文件数量。CLI/Core `0.7.0-castbox.6`、pnpm `10.32.1` 不变，版本号相同不能证明来源相同。

原 `guru-upgrade-tools` 持有完整 source/target、冻结 public plan、operation/ref、preimages 与目标验证职责。`formal_guru_source` 要求 source_ref 解到实际 source HEAD，且 `trellis/` canonical clean，并检查该 HEAD 的 manifest/version 与完整 Skill。普通 `.trellis/tasks/` 规划元数据不在这项 canonical clean 检查范围内。原 Task/Delivery/session、peer/common pointer、历史维护和回滚模型保持；不新增 Guru 持久缓存、锁、schema、恢复 authority 或通用诊断框架。

## 3. 来源设计处置（唯一）

规范性来源为 PRD 第1节原选定的 [Fork PR #68](https://github.com/castbox/Trellis/pull/68) 与 [固定合入 e379](https://github.com/castbox/Trellis/commit/e3793251fad8bd261d0c370d408c7675b9f6a140)。逐项处置如下。PRD 与 implement 引用本节，不另建矩阵。

| 来源条款与原承诺 | 处置 | 本批落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- |
| e379 实际 commit、parents、tree、main CI identity | retain | §5 lock 采用精确组合；§6 从该对象构建，避免同版本错源。 | 原合入已核；没有偏离。 |
| PR #68 改动：一次解析内合并 toplevel/common-dir 查询，复用已成功检查事实 | retain | §4 官方来源负责；只在同一个 RepositoryFacts 同步解析内复用，不提升成跨调用缓存。 | 直接消费已交付实现。 |
| PR #68 改动：所有 eligible peer 仍校验，保留精确 prunable 例外 | retain | §8 V2/V3 实际入口检查合法拓扑及必要拒绝；不只测选中目录。 | 不削减校验。 |
| PR #68 改动：既有分支拓扑缩小候选，选中分支仍独立查询 | retain | §4/§8 V2 采用原实现并观察 Git 来源与正确 checkout。 | 不新增猜测或 fallback。 |
| PR #68 验证：真实 native probes；两个10000ms预算不变 | retain | §6/§8 V2/V4 到达实际 installed/native/public probes，不以 PATH 调整或无界等待替代。 | 没有预算变更。 |
| PR #68 安全与部署影响：诊断只含安全必要字段 | retain | §8 V3/V4 检查实际诊断；保留失败类别，不复制敏感原始 stderr。 | 原诊断合同保持。 |
| PR #68 验证与边界：同候选 public tools apply/recover/resume 保留原 ref/plan/preimages，跨候选拒绝 | retain | §6/§7 分开 local_candidate 与正式 H 操作，原操作完成后才能改变 source 身份。 | 不改旧事务，不放宽 candidate_mismatch。 |
| PR #68 证据边界：受控169/小拓扑结果不证明所有机器耗时，旧内部超时未自然重现 | retain | §8 分别报告 Guru 新观察、Fork 历史和未复现边界；无额外 fault injection。 | 不将历史失败改为已修复旧事务。 |
| PR #68 兼容边界：不改公共 API/schema/state/version/dependency | retain | §2/§5 仅来源采用与原 owner 分发；Task/会话和持久接口无迁移。 | 本批不引入新兼容层。 |

## 4. 模块、职责与设计取舍

| 模块或 owner | 输入、行为、输出与边界 |
| --- | --- |
| canonical source lock | 实施 owner 校对 e379 的真实 commit/parents/tree/CI 后更新 lock；输出完整 Guru source 的依赖选择。只改存在真实差额的字段。 |
| 精确 Fork build | 独立目录从 e379 构建 CLI/Core，核 pnpm 与 package/source identity；成功构建后才写原 `.guru-source-commit` 标记。保留 ESM、workspace 布局和 mode。 |
| 原 `guru-upgrade-tools` | 从完整 Guru source 读取自身 lock，消费匹配 CLI/Core public maintenance API1.0；preview、一次 prepare、冻结 invoke；由原 installer 生成目标 projection/receipt。 |
| 原生 context/session | 来自 Fork；原 Task/C4/session 身份与唯一位置保持，实际目标入口返回合法解析或必要拒绝。Guru 无平行身份 parser。 |
| 原验证 owner | 真实源/目标、native、计时/Git来源、恢复和保持观察分别取证；原 Check/Review 判断充分性。工具退出不代替语义判断。 |
| 原 RDT/Architecture owners | RDT 在合法阶段维护 runtime-location 必要采用/验证差额；Architecture 最终规划及提交后 Review 仍由原 owner 承担。 |

选择原 tools owner 是因为目标为已有 Task checkout 的工具更新，并须保留 Task/session。普通 apply 的历史 Task 阻塞不能变成迁移授权。正式 source_locked 绑定真实 H；提交前采用 local_candidate 只能证明开发可用性，不解除正式来源边界。

## 5. 接口与数据

新 lock 的完整目标值为：

```json
{"schema_version":"1.0","repository":"https://github.com/castbox/Trellis.git","commit":"e3793251fad8bd261d0c370d408c7675b9f6a140","parents":["7a9c62e842001b1d91d6b7feeed36ddd38370da7","cd1d5064f3ec8f97c19cf61f2193694edd4c3ba0"],"tree":"8d7d0c3fe28a3464d92f723539a63da241e5485e","ci_run_id":43341080020,"cli_version":"0.7.0-castbox.6","package_manager":"pnpm@10.32.1"}
```

沿原 public input `profile=install, source_ref=<实际source HEAD>, dependency_mode=local_candidate|source_locked, checkout=<显式单目标>`。CLI/Core 来源描述及 file decisions 由匹配 public inspection 和真实 preview 提供。正式 workflow install 使用 `provider=gh:castbox/guru-trellis/trellis#H`、`template_id=guru-team`、`ownership=custom` 与 H 的 canonical workflow bytes。原 AGENTS custom decision 先由 AI 审查用户正文，再由原 renderer 更新 Guru block；不复制 updater 或伪填 bundled ownership。

`prepare.sh` 只调用一次原 public prepare，返回原 plan/operation facts；`invoke.sh` 消费同一 plan。`resume_required` 只薄投影 `profile=resume,recovery_ref` 回原 owner；实际 `tools_upgraded` 才证明该目标工具验收。local_candidate 必须保留 `unverified=[formal_fork_source_lock]`。不增加公共字段，完整规格由原 package Interface/schema 独占。

## 6. 状态、顺序、正常与失败流程

1. 当前 Planning 完成 Wording→独立 final_plan→Approval，呈现后停在 Activation 前。后续只有原 Activation 才改变 Delivery phase。
2. 获准实施后，核源/目标及任何与拟写集重叠的未终结操作。重叠操作先回原 owning Skill 的原 source/ref 处理，不能新 prepare 覆盖。
3. 构建精确 Fork，更新 canonical lock。先执行来源/官方投影的定向检查；从完整本 Task Guru source 对显式目标做 read-only preview。开发采用以真实 H0 为 source_ref，dependency_mode=local_candidate；canonical dirty 只允许原开发合同。
4. 对实际 preview 的完整写集完成原 tools gate 和必要副作用确认，然后一次 prepare、冻结 invoke。未知等待结果先读原执行 handle/PID/operation，跟随原 executor；实际需要恢复才消费原 ref。完成目标 resolver/installed/native 和保持验证后，读回真实 tools_upgraded。不得在这个操作尚未终结时更改 source HEAD 或 canonical bytes。
5. 完成工程验证及原 RDT 整合/readback，再由原 TaskCommit 在其独立边界形成真实 H。TaskCommit 前的证据只能是开发证据，不能要求尚未存在的 H。提交集覆盖 lock、原 owner 生成的受管差额、必要文档及本批规划，精确 stage/commit 集在该边界重新展示。
6. H 形成后，确认 canonical `trellis/` clean，重新读取 H 的 lock，从完整 H source 对同一显式 Task checkout preview。新建一个独立的 source_locked 操作，其 workflow provider 固定 H。这不是继续旧 local_candidate 的 ref。沿同样的原 tools gate/prepare/invoke/目标验证完成正式采用。
7. 正式采用若产生需纳入内容的真实差额，由原实施/TaskCommit 处理并重新固定实际候选；受影响来源和证据刷新。不能手改 receipt 来保持 H。source_locked 安装结果与它实际使用的 source H 分开标明；不要求 receipt 自包含自己未来 commit，原合同未要求所有文件全树 clean。
8. 原 constructor 固定 B 至最终实际 HEAD 的内容，实施 owner 检查已提交范围及实际证据后 begin_check，再进入一次独立 committed Review。阶段失败回最早受影响原 owner，不把 tools exit 当作 Review。

## 7. 恢复、兼容、迁移与集成

源绝对路径、HEAD 与 canonical source_tree_token 都属于原操作的匹配条件。local_candidate 操作必须先实际完成再形成 H；不能将其 ref、plan、source 或 preimages 改成正式 H。已完成同候选 operation 的 output loss 可由原 public recovery 读回；正常恢复、仍运行 executor 与旧历史超时分别报告，不制造中断来满足测试。

普通 source/path/candidate/owned freshness 失配保留原阻塞，cross-candidate candidate_mismatch 不放宽。若真实操作需 rollback，原 owner 单独审查固定 preimages，先 public compatibility 后恢复 Guru assets/pointer，再验证旧目标入口；不使用 Git reset、分支删除或后续业务回退。没有 Task/session 数据迁移、公共 schema 迁移或数据库发布。

单目标更新保留 Task/planning/archive/workspace/session 和实际合法选择。所有原 peer/common 观测逐项同值；新增合法 peer 仍按原物理隔离规则，不冻结正常注册数。仅更新明确 Task checkout，不写 e943、保留 Fork worktree或其他业务仓。安装的冲突与 `.new/.bak` 交原 owner 逐项处理；没有 unresolved sidecar 才能报告成功。与后续 Delivery 没有新的数据接口，剩余整体验收直接进入原 Completion。

## 8. 验证设计

采用 Fork 已有因果观察和现有工具测试设施，填补 Guru 实际采用缺口。先取得可执行来源再测真实目标，不惯例要求回退旧实现重跑。临时计时 driver 只回答本批来源在正常拓扑的开销和身份问题；长期回归优先复用既有 tests。

| ID / 对应 | 层与入口、输入 | 独立可观察结果及边界 |
| --- | --- | --- |
| V1 / R1、AC1、S1 | 精确 e379 build 与真实 source/ref/lock；原 public maintenance contract；正式 H 的 canonical clean | commit/parents/tree/CI 与实际包来源一致，API1.0可用。版本字符串一致或 marker 自比不能单独证明包来源。H 前不宣称正式来源。 |
| V2 / R2/R3、AC2、S2 | 约169合法工作区及小拓扑，从实际 installed `get_context.py` 当前会话、显式 Task 和公开 tools probes | 正确 owner/Task/唯一 checkout，必要 peer 检查与选中分支独立查询；记录每类 Git 调用来源、数量、耗时及原预算内结果。与历史可比条件分开，不硬编码旧调用数或全机延迟保证。 |
| V3 / R2/R5、AC3、S3 | 原正常入口制造支持的 stale/conflict/非唯一关系，使用合法原 writer 和正常分支/会话操作 | 必要拒绝与安全诊断，不借用别的会话；前后独立读取 Task/session/peer/common 的字节、mode和合法选择。禁止手改 artifact/hash 造负例。 |
| V4 / R3/R4/R5、AC4、S4 | 实际 tools public plan/apply/recover/resume；原 executor/ref；新固定候选 | 原10秒 probes可用，同候选原ref/plan/preimages和operation不替换；真实 output-loss读回。没有自然旧内部超时就报告未复现，不把新操作说成恢复旧#793。 |
| V5 / R6、AC5、S5 | 原 tools 目标 resolver、installed/native；官方 projection checker及tests；实际Claude/Codex/Cursor投影/drift与必要reapply/sidecar | 工具来源、可执行模式、官方hash和生成receipt一致，目标自身可运行、用户改动保留，peer/common保持。源成功不替代目标；skip不算pass。 |

V2 的临时 fixture 必须通过原公开 Task/Delivery/C4/session writers 生成合法关系，采用显式 source/target 参数。可复用 Fork 历史测量 technique，不能直接运行会改 archive-relative 状态的历史 `measure-context.py`，也不能手工 seed C4。调用来源观测不能改变被测入口或用 mock 结果定义预期。V3 只补真实未覆盖的必要边界，不枚举全部状态。V4 优先采用现有 `test_native_install.py` 设施；opt-in环境满足才算已执行，不新增权限中断或 fault injection 要求。

V1—V5足以支持本批语义判断后停止追加实验。只有实际剩余因果或覆盖问题才增加诊断，并说明该问题及结果如何改变判断。完整多平台 throwaway/Release矩阵不属于#814；Fork未变化的广泛套件不机械重跑。

## 9. Canonical 引用、本轮差额与实际未决项

`docs/requirements/current/runtime-location.md`（RDT-REQ-RUNTIME-LOCATION）的 R718/R769 来源、单目标与恢复职责继续；本批只维护 context 正常规模采用及证据边界。`docs/design/current/runtime-location.md`（RDT-DES-RUNTIME-LOCATION）的 D718-03/06/07、D769 不改，补精确来源及原工具采用顺序。`docs/test/current/runtime-location.md`（RDT-TST-RUNTIME-LOCATION）原 T718/T769 设施继续，补当前真实来源、目标、规模和恢复观察；不覆盖旧观察截止。唯一 Docs Plan 见 implement §6。

Architecture 当前无影响，不创建空 contribution 或 ADR。原 final_plan 必须在完整当前设计经 Wording 后重审；后续实际机制变化仍回原 owner。必要工程事实（真实 H、真实 preview 写集、包路径、实际计时）须在对应步骤产生，不是当前需求歧义；目前没有需要用户决策的未决项。缺失依赖或不一致按 implement §4 停在相应依赖处。
