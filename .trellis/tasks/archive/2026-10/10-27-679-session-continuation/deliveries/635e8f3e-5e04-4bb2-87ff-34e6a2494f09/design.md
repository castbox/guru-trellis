# D1 跨会话接续、首失败诊断与请求身份投影设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 [本批 PRD](prd.md) 的 R1–R4、S1–S9 和 AC1–AC6，承担整体 Task 的全部当前范围。目标是让明确接收同一 Task/Delivery 的会话自行补齐缺失的原绑定与选择，再继续实际未完义务；同时修复首失败诊断、standalone 请求构造说明及文档展示调用。没有前序 Delivery。

固定内容基线 B 为 `e6c3b8276d62ac174ab42cba5bca4d5784be2ca3`。原 `DeliveryProjection.content_base(key, development_base=B, observed_target=B)` 已返回同一完整 OID：当前没有既有 candidate 或前序 delivered head，来源是明确选定的开发基线。Planning H0 也是该 OID，仅为当前观察；实施 H 由实际内容确定。后续内容范围为固定 B 到实际 H 加当前 dirty 差额；PR 集成目标为 `main`，不把浮动 `origin/main` 当内容基线。

本阶段采用 `docs/architecture/README.md`（`guru-trellis-architecture`）、`00-foundation/design-constitution.md`（`guru-trellis-design-constitution-v1`）和 `06-governance/change-contract.md`。独立 Architecture 已对同一 key、六项实际候选返回 `baseline_current / candidate_assessment / no_architecture_impact`：修复位于原 caller、owner 校验和 producer 投影职责内，不引入新 state、writer、owner 或决定。本设计仍须在 Wording 后接受独立 `final_plan`，候选结论不代表最终规划或实现通过。

## 2. 当前系统、边界与目标差额

`runtime/delivery_projection/adapter.py` 已正确区分有 context 的本会话 current 与无 context 的 explicit-task。原 Identity、Ensure、Bind 和 `guru-create-delivery:delivery_selection` 已可恢复明确对象；现有缺口是接收者进入阶段前没有完整执行这些前置步骤。显式 key 不会绑定调用会话，换 Author profile 不能补齐事实。

Author `runtime/invoke.py` 与 Architecture `runtime/invoke.py` 把多种失败合并成 `stale_identity / delivery_key`。Wording、Approval 同样有 current 保护，Activation 已有单独选择检查。五个消费者都必须经过原 caller 的接收前置检查；runtime 的防错校验继续保留。

Readiness `normalize_target` 已正确拒绝 standalone 的错误 request_id。其 `references/contract.md` 当前可执行 recipe 只构造 proposed_draft，未提供 standalone 的完整身份映射。`adapters/eval/formal_exit_boundary.py` 的 readiness 回放提示也固定为 proposed_draft。

workflow 的 Human artifacts 展示命令没有传 resolver 实际必填的 `--delivery-key`，正常运行已返回 `invalid_arguments / arguments`。显式传真实 key 后原 resolver 可返回本批三文档路径。本批修正调用说明与命中测试，不修改 resolver API。

这些现场与原 Architecture 子会话人工恢复只证明缺口及原能力可恢复，不是 R1 修复后的原生验收。没有业务仓、生产、部署或 Release 变化；无数据库或外部数据迁移。

## 3. 来源设计处置（唯一）

Issue #679 不提供独立详细设计，但其中明确约定的机制边界构成本批规范性约束。以下为唯一处置矩阵，PRD 和 implement 不另复制。

| 来源与原承诺 | 处置、具体落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| #679 R1；现行 D531-02：有 context 必须读自身选择，仅真正无 context 可 explicit-task | retain；第4、6节。adapter 的 current/select 边界保持 | 防止显式 key 隐藏缺绑定或冲突；无需改变原 adapter 公共合同 |
| #679 R1/R2：原 Identity/Ensure/Bind/Selection 补缺，同对象、原 phase/profile/purpose 接续 | retain；第4–6节。workflow 编排，原 step-local 合同拥有内部操作 | 不继承父会话、不新建 writer，不重置规划；不同选择回原 owner |
| #679 R1；现行 D657-01/02：created 只服务原创建区间，续接按实际未完义务 | retain；第6节。只对初始需求调用 initial Author | 绑定不是阶段 pass；旧进度和真实 producer 输出按适用性消费 |
| #679 R2：首失败可定位，保留校验强度及兼容说明 | retain；第5、7节。拆 Author/Architecture 复合诊断，原 caller 覆盖五消费者 | 保留 code、DTO、typed exit；field_path/remediation 的诊断细化在 MIGRATION-679 明示 |
| #679 R3：standalone profile 与 mode 独立，保留真实 producer、合法不同 caller_locator 和 normalization | retain；第5、6节。原 recipe 补变体，原 runner 补真实 profile | 错误输入被拒不是 normalization bug；不改正向 runtime 或另造身份 |
| #679 R4：真实 key 展示，Task-only 只根 PRD，归档保留 archive ref/key | retain；第5、6节。原 Human artifacts 调用及原 package-owned 测试 | 不猜选、不伪造 key、不创建空切片；不新增展示 API |
| #679 AC1–AC6；现行 T531-07：分层真实验证、匹配安装及旧能力兼容 | retain；第8节及 implement 第3节 | package、installed、原生各自证明；一代表 clean，不承担完整矩阵 |

没有 change/reject 来源承诺，也没有需要原需求 owner 决定的技术偏离。

## 4. 模块、职责与设计取舍

| 原模块或 owner | 输入、实际改动与输出边界 |
| --- | --- |
| canonical `trellis/workflows/guru-team/workflow.md` | 在原 created consumer、唯一 continuation 与 Planning 编排处，mandatory 调用原 Identity/Ensure/Bind/Selection。明确接收者自己的前置检查；保留原 profile/purpose 和唯一出口 consumer。这里仅拥有跨 Skill 路由，不复制 Bind 内部步骤。 |
| 五个 Planning owner 的现有 SKILL/references | Author、Wording、Architecture、Approval、Activation 的 entry 分别指向并履行自身前置要求；缺本会话事实回原 owner，重读后再执行原步骤。Architecture 保持独立与 baseline-first。修正命中合同，不新建通用恢复 Skill。 |
| Author、Architecture 的现有 runtime 校验 | 在原 planning guard 内按第5节检查首失败，只返回客观错误。不能自行 bind/select、推断语义 route、写 pass 或放宽 phase/scope。 |
| Readiness 原 `references/contract.md` | 完整 recipe 增 standalone_request 分支及普通 request_id 错误恢复。真实 completed_review 仍由 AI 完成十维判断；transport 只构造 envelope 和消费真实 receipt。 |
| 原 eval fixtures 与回放入口 | 复用 create/Binding/Planning fixtures、ReadinessAdapterTests、formal_exit_boundary。补受支持初始状态与 profile 参数；runner 不提供恢复步骤或 expected pass，不代 Agent 填映射。 |
| 原 Human artifacts 合同与 Approval package 的 artifacts 测试 | 展示明确对象并实际执行 resolver；测试检查真实路径及文件缺失，不以文本相等代替行为。 |
| 原 preset installer/平台入口 | 同步 `.trellis/workflow.md`、package 安装及声明投影；入口只加载、路由，不拥有另一份恢复流程。 |

不采用在 adapter 自动绑定的方案，因为它将 caller 的语义目标与 writer 副作用藏进事实读取。也不采用统一 stale 后重跑初始规划，因为会丢失原义务、不能诊断首失败。复用现有 package 测试和 runner，避免新增通用框架。Readiness 保持原 normalization，只有合法输入仍失败的实际证据才触发候选重审。

## 5. 接口与数据

### 5.1 接收身份与原 owner 链

原 producer 提供 TaskId、generation、DeliveryKey、TaskRef、planning_root 和实际前序输出；这些不是授权或 pass。接收者先经原 Identity/Ensure 核定同 Task 当前 generation、唯一注册 checkout 和真实 Git 关系，再读取本会话公共 current。缺 Task 只进入原 Bind；缺选择只进入 `guru-create-delivery` 的原 selection profile。匹配事实直接复核复用。之后重读 current 的 key、phase、scope 和公共 root，与输入核对，再调用原 Author/Wording/Architecture/Approval/Activation。

不新增 input/output schema、public typed exit、session store 或 GateResult 字段。原公共解析器继续验证 opaque key；调用方不通过目录、唯一 inventory、working directory 或父会话选择身份。

### 5.2 首失败诊断合同

Author/Architecture 在原复合 guard 位置按实际可得事实逐项验证：公共 current kind → 已选 key → 当前 generation → 适用 phase → scope authority 及其内容校验。原 resolve 若先返回客观 generation/身份错误，保留该首失败，不用后续推测覆盖。多项失配每次只报告首先失败的一项，修复后重新读取全部条件。

| 条件 | 诊断指向与原 owner |
| --- | --- |
| `no_current_task` | 指出当前调用会话未绑定；原 Identity/Ensure/Bind，不能暗示 design 过期 |
| 同 Task `no_current_delivery` | 指出缺 selection；原 `guru-create-delivery:delivery_selection`，不能新建切片 |
| `terminal_delivery` | 指出终态及原 terminal/release owner；不能当作可补缺选择 |
| `error` 或 API/checkout/绑定读取失败 | 保留实际 code/condition/原错误信息与责任 owner；不得归为无 Task |
| `current` 但 key 不同 | 指出当前 selection 冲突；交原选择/生命周期 owner，不能覆盖 |
| generation、phase、scope 真实失配 | 分别定位实际字段；按原身份、stage rework 或 scope owner 恢复；原拒绝强度保持 |

现有 `stale_identity` code 与公共 exit/DTO 形状保持；field_path/remediation 从泛化 delivery_key 细化为实际条件。精确命名由原错误目录及现有字段组合确定，并在同批 MIGRATION-679 列出前后映射；不新增第二状态模型。五个 caller 共同按这张事实分流表恢复。Wording/Approval/Activation 的既有独立 guard 和失败合同先保持，只有正常入口实测命中未覆盖的差额才由原 owner 重新资格并扩展当前候选，不自动复制一套 runtime helper。

### 5.3 standalone consumer envelope

`profile=standalone_request` 的 `public_input.target_locator` 来自实际 Wording `transition.target_locator`；source 的 `draft_id` 与 authored `target.request_id` 都等于该实际请求身份。`target.caller_locator` 是真实非空调用方定位，可以不同于请求身份。public_input、owner_result 的 mode 均来自真实 transition.mode，保持 workflow/standalone 两个合法值；continuation 不重造。

`source_request_sha256` 仍是当前 draft authority projection 的 digest，包含原合同定义的 kind/repo/issue_number/url/state/updated_at/body_sha256；不改成 body SHA。recipe 复用原计算及 recorder 派生，不填写私有 Gate linkage。record 成功后完整替换 owner_result 为 receipt.result；check 成功后只取真实 receipt.result.validation_receipt；invoke 的实际 ready 才进入唯一 consumer。最小 completed_review 必须包含 AI 真实十维、scope conclusion、findings 和最小 Gate，不预置 pass。

### 5.4 Human artifacts

明确选定 Delivery 时，原命令为 `resolve-human-artifacts.sh --json --task <实际 TaskRef> --delivery-key <实际完整 DeliveryKey JSON>`。使用公共结果中的实际 paths；缺失文件只报告存在的结果和缺口。尚无或没有当前 Delivery 的 Task-only 停点，直接展示该精确 TaskRef 内存在的根 `prd.md`；不调用要求 key 的切片 resolver。明确归档切片传实际 archive TaskRef 与该 key。原 helper API 不变，调用说明不得宣称无 key 可解析切片。

## 6. 状态、顺序、正常与失败流程

1. 接收真实输出或恢复明确原对象，读取安装合同和当前请求。原 Architecture 接收仍先读完整 baseline/constitution/change-contract，不接收 PRD/验收或旧 pass 叙事作前置答案。
2. 由原 Identity/Ensure 核定目标，公共 current 检查调用者自身事实。仅对确实缺失项调用原 Bind/Selection；没有 context 走已有 explicit-task，不写 session。不同选择、终态、error 停在原 owner。
3. 恢复后重读 current/key/generation/phase/scope/root。匹配时保留全部规划及适用前序，执行唯一 continuation 的原未完义务。初始 requirements 才到 initial Author；已有方案回适用 Author/Wording/Architecture/Approval，当前 approved 回 Activation 展示边界。
4. 真实前序输出缺失或过期，回原 producer 刷新受影响义务；不从文件/phase 猜 pass。普通同范围恢复自动衔接，不重复要求用户手动绑定或确认继续。
5. standalone 构造错误时，原 Agent 先读错误、当前 source 和实际 producer，再完整重建 consumer 并重审十维，经原 record/check/invoke。producer 不变；source/body/authority 真变或 producer 失效则回原 producer，不伪造 linkage/receipt。
6. 在正常展示停点按第5.4节取实际文档。R4 不改变任何业务 phase，也不为展示建立 Delivery。

所有补绑定与选择只写各自原 owner 允许的本会话状态；不改变 Delivery phase、不清空原 gate、不产生 Planning 通过。错误后的实际合法 rework 仍由当前 stage owner 执行。

## 7. 恢复、兼容、迁移与集成

MIGRATION-679 明确成套采用范围：matching workflow、受影响五 Planning packages、Readiness recipe、原 eval/installer 及 dogfood 投影。旧完整安装固定旧版本；显式采用时用官方 marketplace workflow 预览 `.new`、核本地修改后显式应用，并 reapply 完整匹配 preset。不得只复制一段提示或修改全局/npm/hook。诊断 field_path/remediation 的前后差额单列；code、现有 schema/exit/opaque key 与 helper 参数 API 保持。

在途同 Task/key 原阶段恢复，不换身份、不改 context 环境，不转换旧 semantic pass。缺失输出回原 producer；已发生的合法 Git/GitHub 事实保留。无需数据格式迁移或双读：没有持久 schema 变化。新行为没有临时 feature switch、compatibility store 或退出账本。

保留 #548 有/无 context transport、#443 会话隔离和 #396 proposed_draft recipe/恢复。main 无关前进不重新选 B；真实 conflict/必要依赖才按原 Reconcile。没有前后 Delivery 接口迁移，本 D1 的真实结果之后交整体 Completion。受影响共享 RDT 当前正文按 implement Docs Plan 在候选 Check 后由原 owner 最终整合；Architecture 无 impact，不创建 contribution/ADR。

## 8. 验证设计

| ID、对应范围 | 层次、入口与正常输入 | 必须观察及证据限制 |
| --- | --- | --- |
| V1：R1/AC1，S1/S2 | 正常 writer 创建隔离 Task/D1；真实主接收会话与 fresh Architecture 子会话初始未绑定/未选，分别读安装入口 | 自行经原 owners 恢复同对象并到 Author requirements_ready、Architecture candidate_assessment 正式出口；保留修复前首失败对照。提示只给事实/目标/边界，不给恢复步骤、预期 pass。人工恢复不算通过。 |
| V2：R1/R2/AC2，S3–S6 | 原 fixtures 和至少一原生已有进度样本；按原正常 Bind/Selection/phase/scope 操作形成各状态 | 覆盖 current 五种 kind、不同选择、真实 generation/phase/scope 变化、API/读取 error、无 context；指出首失败/原 owner，同对象/规划/Git/并行会话保持，原未完义务继续，不重跑初始规划。不能靠手改 session/artifact 造样本。 |
| V3：R3/AC3，S7/S8 | ReadinessAdapterTests 执行公开 recipe；workflow/standalone 合法及 mode 失配；原 runner 做一条真实 mode 的原生错误恢复 | 实际 producer 身份、不同 caller_locator 正常到 ready；错误 request_id 拒绝后 Agent 从未改 producer 完整重建 consumer 到正式 ready。helper 不代映射；package 双 mode 不冒称原生双 mode。 |
| V4：R1/R2/AC4 | 五个直接消费者原 tests/entry；原 creation chain、bind runtime/portable、projection fixtures | 逐边核 mandatory 接续和正向/失配；保留 #548/#443/#396。fixture gate 只是 transport，不能替代 V1/V3 原生。 |
| V5：R4/AC4/AC5，S9 | 原 Approval artifacts 测试执行文档展示命令；选定 D1、缺文件、Task-only、archive | 带真实 key 返回同切片实际路径；缺文件准确报告；Task-only 只根 PRD且没有选择/创建副作用；archive 使用原 ref/key。文本 parity 只补充分发。 |
| V6：AC5/AC6 | 一个代表 clean 安装、完整 reapply、drift、可执行 mode、声明平台和 sidecar 定向检查 | matching canonical/dogfood/installed 实际调用与本地用户内容保持；逐个核 `.new/.bak`。不承担完整多平台 Release/Upgrade 或业务安装升级。 |
| V7：R1–R4/AC5 | 原 Check/独立 Architecture、完整 B..H Review 与 RDT proposed/current 链 | 对应历史边界→首失败→机制→正向/失配→实际证据；缺原生、环境或安装结果明确未验证，不用静态检查闭合。 |

具体命令、依赖顺序与停点在 implement 第3、4节。所有项目目前为计划，没有预填通过。

## 9. Canonical 引用、本轮差额与实际未决项

- Requirements：`docs/requirements/current/task-delivery-lifecycle.md` 的身份/Planning/跨环境接续，补本会话前置事实、首失败和展示场景；Readiness 原 package 合同补 standalone 映射。
- Design：`docs/design/current/task-delivery-lifecycle.md` 的 Authority、Creation/Author/Activation、恢复，补明确接收者与原 owners 的 mandatory 衔接；本设计第3节是唯一来源设计处置。
- Test：`docs/test/current/task-delivery-lifecycle.md` 的 T531/T657 与当前场景，补 V1–V6；原 #548/#396 历史贡献保留旧观察。新结果在本 Task 的 RDT contribution test 正文逐项维护，不复制日志。
- Architecture：第1节三个 authority 及其必要关系。已消费候选 no-impact；Wording 后 final_plan、实施 Phase2 与 committed 阶段仍由独立原 owner 判断实际变化。当前不创建 Architecture contribution、ADR 或空 project-check。
- 公共精确规格：原五 Planning packages、Bind/Selection、Readiness Interface/schema、delivery_projection、原 package artifacts resolver；不把本设计当第二公共 API。

当前没有未决产品选择或设计阻塞。实施中出现的新正常路径问题先由原 owner 核定必要性与最小范围，直接影响本链路的差额按 R4 纳入；机制变化刷新受影响资格/Architecture/Planning，不能只记范围外后绕过。实际原生执行与安装环境尚未验证，其缺口将保留到原 Check/Completion。
