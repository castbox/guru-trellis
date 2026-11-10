# #773 D1：Task 诊断与同身份关联恢复设计

## 1. 设计目标、需求承接与内容基线

本批完整实现 Delivery PRD 的 R1/R2、D1-S1–S3 和 AC1–AC4。Task 整体范围见根 `prd.md`；没有前序 Delivery。固定 development baseline B 和 Planning H0 均为 `313d80215f65777fc70893a90c6d8dce8005d6dd`，来源为本批选定的 origin/main。后续内容范围为 B 到实际候选 HEAD 及所选工作区内容；PR 目标为 main，目标前进不自动替换 B。

Architecture authority 为 `docs/architecture/README.md` 的 `guru-trellis-architecture`，constitution 为 `docs/architecture/00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1`，change contract 为 `docs/architecture/06-governance/change-contract.md`。实际 candidate_assessment 返回 `baseline_current`、`architecture_impact`、`target_native`，decision refs 为 `ADR-PORTABLE-SHARED-LIFECYCLE` 和候选 `ADR-TASK-RECOVERY-ASSOCIATION`。它仅认可候选边界，不代表最终方案批准、实现或安装通过。

## 2. 当前系统、边界与目标差额

Branch 包位于 `trellis/skills/guru-team/packages/guru-establish-task-branch-binding/`。其 `runtime/invoke.py` 的正式 invoke 已转换生命周期错误；discovery 和 plan recorder 共用的 `run()` 分支在候选枚举前直接解析 Task，遗漏转换。目标是在这一共用边界返回既有 `stale_identity` 诊断，保留原错误 code 和 TaskRef 定位。

`runtime/task_lifecycle/branch_resolution.py` 已拥有候选发现、C4/C5 匹配检查、建立事务和结果恢复。未绑定候选用 HEAD 树验证 Task，已绑定的同分支可读工作区 Task。恢复未跟踪目录后，Identity 可读而普通初次候选仍不成立。现有 Rebind 又要求已有绑定及 clean/base-contained，因此不能承接首次关联。

本批在原 Branch 内新增一个明确选择的恢复 profile，直接验证当前注册 checkout 的工作区原身份，复用原 C4/C5 建立事务。普通候选枚举、排序、HEAD 检查、Rebind、Creation 限制和既有输出不改变。没有新 owner、持久状态、授权记录或恢复账本。

## 3. 来源设计处置（唯一）

| 来源／原承诺 | 处置与正文落点 | 理由、影响及上游处置 |
| --- | --- | --- |
| #773 R1：复用生命周期错误到命令诊断的转换；保持拒绝 | retain；第4、5节 | 共用解析边界处理，不建设异常框架。无需改变来源。 |
| #773 R2：固定载体，核原身份、完整规划和历史缺口后恢复 | retain；第6节 | Markdown 判断充分性；Git 仅恢复精确已审路径。 |
| #773 R2：目标基线、文件恢复、资源关联、聊天绑定分别表达结果 | retain；第4、6节 | `task.py set-base-branch`、Git、Branch、Bind 各保原 writer。 |
| #773 R2：工作区／HEAD 前提不同；不改枚举排序，不隐含提交 | retain；第2、5节 | 新 profile 显式承接工作区，普通入口保持原行为。 |
| #773 R2：优先公开能力，仅补具体缺口的最小动作 | retain；第2、4、5节 | 首次 C4/C5 关联是已核缺口；仅在原 owner 增加 profile。 |
| #773 非目标：不补历史 gates、不重建身份或空 Delivery | retain；第6、7节 | 关联动作不写 Task、Delivery 或 gate；无上游偏离。 |
| #773 最小验收：定向诊断；动作变化时一条代表恢复；受管同步 | retain；第8节 | 验证新增边界和直接消费者，保留原证据限制。 |

## 4. 模块、职责与设计取舍

- Branch `SKILL.md` 拥有恢复条件、语义审查、必要副作用计划、调用和 typed exits。`interface.json`、schemas、commands、examples 描述同一公开能力；`runtime/invoke.py` 只做客观校验及执行。新的 `references/task-carrier-recovery.md` 由此原 owner 提供完整可执行顺序，其他 owners 只描述自身职责并引用它。
- 共享 `branch_resolution.py` 增加窄的工作区恢复准入，复用或提取 `establish_branch_binding` 现有 snapshot/write/readback/rollback 事务代码。C4 继续通过 `OwnershipPort` 调 C5，不读取 ledger 内部结构。只填缺失控制；原有效 ownership 保留，不能改成 caller-owned 覆盖既有权属。
- Identity `SKILL.md` 说明缺载体时的诊断和固定 Git 来源核验。Ensure `SKILL.md` 说明缺关联交回 Branch，成功后重读唯一 checkout。Bind `SKILL.md` 说明建立关联后由接收聊天自身绑定，再读取原生 current/continuation；不得借用来源聊天身份。
- 原生 Git 负责 `git restore --source <fixed-commit> --worktree -- <exact-reviewed-paths>`。原生 `.trellis/scripts/task.py set-base-branch <TaskRef> <branch>` 负责已选择基线。两者不迁移身份或补 gate。

只写指引无法跨过已核首次关联缺口；要求先提交引入无必要 Git 副作用；放宽普通 HEAD 候选会改变所有 discovery 调用的准入。显式 profile 把新准入限定在同身份恢复，复用原事务和 consumers，代价是一个有当前调用方及验收的输入分支。详细取舍见本目录 `architecture/adr-task-recovery-association.md`，仍为 proposed。

## 5. 接口与数据

新输入 profile 定名 `delivery_restored_checkout`。公开入口仍为 Branch `scripts/invoke.sh --root <registered-checkout> --input -`。输入只含 `profile`、`mode`、`task_id`、`task_ref`、`lifecycle_generation`、`branch_name`、`expected_head`。`mode` 保持 workflow/standalone，HEAD 为完整40位 Git SHA。没有 action、路径清单、源载体、审查结论或授权字段；载体和写集由 Markdown 与 Git 恢复边界承接，不成为长期关联 authority。

新增独立 schema `public-delivery-restored-checkout-input.schema.json`，identity `guru-establish-task-branch-binding-input-delivery-restored-checkout-1.0`。aggregate 改为明确的两个 profile union 并使用新的 `guru-establish-task-branch-binding-input-delivery-2.0` identity；原 active-task profile schema、字段及语义保持。Interface、command schema bindings、examples 和受管分发成套更新。公开迁移说明明确新调用需要完整 matching package/runtime；旧安装不支持新 profile，沿原 tools owner 升级，不能把它重解释成旧 establish 或 recover。

新 profile 在 invoke 内验证：工作区 Task 是 schema2 active，TaskId/generation 匹配；root 是同 common-dir 的当前注册 checkout；注册分支、实际分支、输入 branch_name 和 HEAD 相符。primary 与 linked 都受支持，不继承 Creation 的 non-base／非 primary 限制。读取 C4/C5：已有项必须同 key、branch、revision；另一 Task 占用或未解决 incarnation 冲突停止；只有缺失项才建立。初次无控制项使用原 revision 0；仅一项存在时沿其 revision 补另一项。

完全匹配已有 C4/C5 时复用并验证当前 checkout；缺 C5 时新 branch ownership 为 caller_owned，primary worktree 为 not_applicable，linked 为 caller_owned。现存权属不改。成功仍输出 `binding_established` 的原 TaskKey，交原 established router → Ensure；身份问题用原 `invalid_task_state`，控制/checkout/HEAD 矛盾用原 `blocked`。不新增 exit、public output 或 store。

普通 discovery 和 recorder 仍只接受 `delivery_active_task/action=establish`。共用 `resolve_task_ref` 捕获 `LifecycleContractError` 并抛 `CommandError("stale_identity", exc.field_path, "<原code>: <原诊断及恢复提示>", 3)`。`task_not_found` 的 field_path 保留实际 TaskRef，提示先由 Identity 核固定载体，再由 Branch 原恢复指引建立关联。错误 DTO 结构不变；拒绝不变，原误报 internal_error 改为已声明的 stale_identity。

## 6. 状态、顺序、正常与失败流程

1. AI 固定可获取的原 Git commit，完整读取原 Task、Delivery、规划以及该 Task 的 Publication/Delivery/full_review/readiness 历史，核唯一 TaskId/generation/source/scope 及真实缺口。来源不唯一或 schema 不受支持时停在 Identity／原迁移 owner，不创建替代身份。
2. AI 明确目标基线、当前目标分支／checkout 和精确写集，核对现有本地改动。沿原交互边界展示真实副作用；同目标已授权范围内自动接续，目标或写集变化回原选择。
3. 使用 Git 恢复已核路径；若目标基线改变，使用原生 set-base-branch。重读恢复文件，确认仅发生已审变化，完整规划和历史 Publication/Delivery/full_review/readiness 缺口仍如实保留。
4. Identity 核工作区原 Task。有效 C4/C5 直接复用并由 Ensure 验证；普通 HEAD 候选可成立时继续原 establish。仅当工作区已恢复而 HEAD 不含原 Task、需要首次或缺失控制关联时，AI 审查后调用新 profile。
5. 新 profile 完成上述客观准入后，只补缺失 C4/C5，事务回读一致才返回原成功出口。普通错误或控制矛盾保持现场并回原 owner；不扫描重试来代替恢复，不要求提交。
6. Ensure 重读唯一 checkout；Bind 使用接收聊天自己的原 resume/rebind profile，原生 `task.py current --json` 及 continuation 读取真实结果。若 no_current_delivery，按实际需求回原 continuation，不自动新建 Delivery。文件、关联和 session 成功均不构成规划／交付成功。

## 7. 恢复、兼容、迁移与集成

普通 active profile 的 discover/record/establish/recover 和输出 consumers 保持；新 profile 是 additive 受支持能力，aggregate identity 变更显式记在 `trellis/presets/guru-team/MIGRATION-773.md`，不静默复用旧 schema identity。实际是否需要修改通用分发登记由现有 Interface 发现规则决定，不另建 registry。

输出丢失时先用原 discovery 检查 `already_established`／binding_ref，再用原 recover-result 的 exact revision/branch/HEAD 只读恢复；已绑定分支的工作区校验支持该路径。不要从输出丢失推断执行失败而再次建控制。恢复之前仅一项控制存在时只补缺项，事务普通异常沿原 rollback；不新增锁、crash 或原子写协议。

不迁移 Task/Delivery schema，不填历史 result，不改真实聊天或 #223 资源。安装由 `guru-upgrade-tools` 按完整源升级受影响工具，保留当前 Task/session，并处理真实 sidecar；不能手抄受管文件。RDT 与 Architecture 先准备隔离正文，独立 candidate Check 后才原 owners 晋升，再重绑实际 after 走最终质量链。

## 8. 验证设计

| ID／验收 | 层级、入口与输入 | 独立预期观察与限制 |
| --- | --- | --- |
| V1／AC1 | Branch 包公开 discover-candidates.sh 和 record-plan.sh；临时仓库中规范 TaskRef 正常缺文件 | 两入口拒绝且退出3，既有诊断 DTO 含 task_not_found、实际 TaskRef 和原恢复指引。不得返回成功空候选；复用原成功/只读用例。 |
| V2／AC2–AC3 | 一条去敏代表恢复：固定 Git 原载体含真实有效 schema2 Task、Delivery、完整计划；目标 HEAD 不含 Task，Git 精确恢复工作区，调用新 Branch invoke | 无需 commit，建立同 Task/generation 的 C4/C5；原 Task/Delivery、规划和历史缺口不被修改。后续原 Bind 公共入口读取相同身份；current/continuation 观察限定实际运行层，不冒称 native Agent 全链。 |
| V3／AC2–AC3 | 原 Branch/shared tests 中直接覆盖新准入边界 | 匹配复用不写，缺一项只补一项；普通分支/HEAD/身份/既有关联失配拒绝。primary 的 not_applicable 和 linked caller_owned 采用实际拓扑，必要 fixture 可隔离未变外部依赖；不制造攻击测试。 |
| V4／AC2 | AI 对照完整指引、公开 schema/commands、原 Git/task.py/Bind/continuation 调用 | 核顺序、输入可用阶段、写集、停止条件和历史缺口；文本扫描只辅助，不证明 Agent 行为。 |
| V5／AC4 | 受影响包验证、runtime unittest、source/installed/distribution、声明 dogfood/drift/sidecar/mode 定向检查 | 通过结论只覆盖实际运行入口；tools owner 同步后验证 Task/session 保留。无 full installer 或 Release 矩阵。 |

V1 是长期缺陷回归；V2/V3 的新行为断言是长期恢复回归。指引核对与当前 sidecar 检查是本次证据。先写清晰且廉价的诊断用例，再实现新准入及代表恢复，随后跑受影响原覆盖和投影验证。测试从需求条件、动作和观察推导，不固定可变配置或只比较自身 fixture。若入口未到达所测逻辑，先修复或更换有界观察；不把基础设施失败称为产品缺陷。必需验收与回归足够后停止追加实验；只为真实未决因果问题追加检查。

## 9. Canonical 引用、本轮差额与实际未决项

R/D/T 当前基线分别为 `docs/requirements/current/task-delivery-lifecycle.md`、`docs/design/current/task-delivery-lifecycle.md`、`docs/test/current/task-delivery-lifecycle.md`；本批用独立 `task-carrier-recovery.md` 叶子承接完整新规则，不向根或共享索引登记。Architecture 真实关系落点为 `docs/architecture/03-domains/ownership.md` 的 C4/C5 关系，以及新 `docs/architecture/adr/task-recovery-association.md`，原 portable ADR 保持有效。

本目录 `architecture/contribution.md` 和 ADR 是真实 task-local 候选，由原 Author 写作，独立 Architecture 评估。实施阶段在这里准备完整拟晋升 targets；candidate Architecture/Check 之后由原 Architecture final_integration，RDT 原 owner 同步三层 authority。当前无用户范围未决项；所有实现、代表恢复、安装投影及最终 gates 尚未验证，不得提前标通过。
