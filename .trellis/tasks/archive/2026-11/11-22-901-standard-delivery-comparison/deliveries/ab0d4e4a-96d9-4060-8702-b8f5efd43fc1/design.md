# 标准 Delivery 发布版对照设计

## 1. 设计目标、需求承接与内容基线

以同一小型 CLI 变更承接本批 R1–R3、AC1–AC3。正式工作 development baseline B 和规划时 HEAD 均为 `f06eddb6ccf97ddd2d1a41c117692f5957cb2dc7`，来源为只读 Intake 固定的 `origin/main`。交付内容范围由原 Candidate owner 在实际待交付文件上固定。PR 目标为 `castbox/guru-trellis:main`。实验版本独立固定如下。

| 发布版 | Guru 提交 | Fork 源码锁 |
| --- | --- | --- |
| v0.7.0-guru.8 | `2ab135ed2d3908966785bb23ad42ada0790f0c81` | `ca0e8b931d19ccb87802d6866abd2113a6f707c0` |
| v0.7.0-guru.9 | `ac1c823857ad6695c106daeedd25aafce4c50934` | `e3793251fad8bd261d0c370d408c7675b9f6a140` |

两侧均声明 CLI `0.7.0-castbox.6` 和 pnpm `10.32.1`。按各 tag 自身源码锁构建，记录实际运行版本。Architecture 依据为 `docs/architecture/README.md`、`docs/architecture/00-foundation/design-constitution.md` 和 `docs/architecture/06-governance/change-contract.md`。候选结果：独立 candidate_assessment 返回 `baseline_current`，结论是 `no_architecture_impact`。候选在两个隔离项目使用已发布版本的原生入口和正式结果。实验记录及复核报告供本 Issue 的观察与归因使用。候选沿用现有 workflow、运行状态和 owner 边界，不改变项目 Architecture authority。

## 2. 当前系统、边界与目标差额

两版真实 workflow 均在 Delivery Review 前要求发布架构资格。两版规划、执行和提交的具体阶段入口由各自安装决定。旧版的 early Draft 属于可选路径，本场景选择两版都支持的常规路径。若运行中的原 owner 判定有必要，保留其实际理由和停点。#793、#792、#794 已进入 .9。两发布版之间还存在其他 Guru 与 Fork 差异。本批首次针对一个标准 Delivery 测量并解释这些观察。

## 3. 来源设计处置

| 来源 | 承诺 | 处置及落点 |
| --- | --- | --- |
| #826 R3、AC3 | 冻结同一任务和评价规则，隔离执行材料，先匿名评价 | retain。第4、6节。这样两边互不消费对方产物，评价先于揭示映射。 |
| #826 R4 | 复用原生入口，保留足够复核的材料、实际运行、差异与失败 | retain。第5、7、8节。采集现有原生事件，保留原失败和环境边界。 |

## 4. 模块、职责与设计取舍

复用 #826 去敏 Python 笔记 CLI 的思路。固定三个已知顺序的样本和既有 `show` 行为。用相同自然请求让两边为 `show` 增加可选 `--limit N`。省略参数时保留完整有序输出。0 返回空数组，正整数返回至多 N 条，结果不写回存储。该小场景可以通过真实 CLI 测试，并走正式 Delivery 的读取、资格、工程验证和审查交接。资格触发的具体观察点是 Author 的 `author_candidate_set`。v0.7.0-guru.8 安装的 `.trellis/guru-team/skills/packages/guru-author-task-plan/references/authoring.md` 要求在这一候选入口调用正常场景与方案机制资格 owner。v0.7.0-guru.9 的同一合同要求分别判断适用条件，只提交真实适用的非空候选集合。这个只读 CLI 查询改动提供普通候选。依据两版合同，预期可观察到旧版调用和新版按条件省略。运行材料不透露这个预期。评价者按轨迹核对实际触发、合法不调用和未到达该入口的情况。

负责人持有任务材料、版本映射、评价标准及执行授权边界。每侧 Agent 在独立副本执行正式流程。评价者只读取去敏的中性记录和产物。原审核 owner 解明映射并判断差额。现有 Codex CLI 承接原生运行。采集仅整理事实，采用现有 JSON 事件及必要的原生子审查记录。

## 5. 接口与数据

输入为共同业务树、样本、同一自然请求、每版实际匹配安装。评价规则和计数边界单独冻结。输出为 `validation.md`（结论、阶段和指标）以及 `validation-observations.md`（可复算的去敏观察与定位）。保留最少的事件顺序、选段、有效字节、调用、退出、结果和否决原因。遵守凭据与授权信息保留边界。授权答复原文及身份不进入交付文件。

| 指标 | 冻结后的计数单位 |
| --- | --- |
| 必读流程字节 | 实际送达 Agent 的必读 workflow、Skill、合同正文 UTF-8 字节。按本阶段真实读取切段，截断只记送达部分，重读重复计入总量并单列。初始注入仅在实际可量化时计入同口径，两侧不可量化的注入标缺。 |
| runtime 调用 | 一次观察到的公开 wrapper 或 Trellis runtime 命令执行。批量工具内能辨别的各次执行分计。子调用只在两侧都有同层证据时纳入同口径。 |
| 输入装配失败 | 因缺字段、错误形状或合法身份输入不匹配而拒绝的一次调用。区分工具故障、语义未通过和未触达。 |
| 语义审查 | 一次实际执行的 stage owner 语义决定。保留其角色、范围和结果。多职责合并在同一轮时记一次，并核对职责覆盖。 |
| 测试重跑 | 同侧首次执行后，再执行同一入口、用例集合和目的的测试。记录候选是否变化。新覆盖首次执行单列。 |
| 用户确认 | 同侧实际发出并由人作答的一道具体选择或副作用确认。另记未答停点，区分平台提示和语义门禁。 |

## 6. 状态、顺序与停止边界

两边真实完成前置装配后，从选中首个 Delivery、开始初始 Planning 前的等价业务状态起计。前置安装、bootstrap 和 Task 创建另报。固定过程分段为 Planning、实施与工程结果、本地提交及 Check/独立 Review、发布资格与 Delivery Review。按双方的实际因果顺序记录交接，避免只凭阶段名字划段。

共同目标为两侧原 Delivery Review 的正式 `ready`，绑定各自经审核的候选，并完成实际适用的发布阶段 Architecture 判断。在准备进入任何未批准写入时停下。若版本真实路径需要更早的确认，报告精确操作并暂停该侧。若许可或环境只支撑较早路径，以双方已达到的最后一个等价观察点结束比较，保留未达到的目标。无批准的合并执行，归档列为未到达。

## 7. 恢复、兼容与集成

安装失败保留所选版本、命令、退出和原诊断。在同一版本修复普通环境问题后，可以另起有标识的尝试。保留原失败。若需替代版本，先说明障碍、替代来源和对可比性的影响。发生流程装配失败时，按该发布版原 owner 和公开恢复入口接续。两个实验副本与本 Task 的正式 Git/PR 状态分别保留。

## 8. 验证设计

- **V1 安装与共同起点（AC1）** 核对两个发布对象、两份 Fork lock、实际 CLI/Core、workflow 与受管 preset。读取各自的公共 Delivery 状态，确认匹配的任务材料、业务树和已选 Planning 起点。
- **V2 原生运行与重算（AC2）** 通过实时 Codex 原生入口及 JSONL/公开结果，观察实际 CLI 测试和所有适用 workflow 门禁。按事件和输出片段重算六项。部分可观测指标按共同覆盖标记。对照相同样本的正常输出及副作用。
- **V3 匿名结论与归因（AC3）** 先保持中性标识评价再揭示映射。将实际差异回接 #793、#792、#794 的源改动、具体调用和交接。遇到 Wording、Fork lock 或其他变化的影响时保留为额外因素。记录发布架构的实际开销、归档边界和是否需要独立架构工作。

## 9. Canonical 引用、差额与未决事项

适用仓库单元为 `docs/requirements/current/behavior-validation-method.md` R826-01/02、`docs/design/current/behavior-validation-method.md` D826-01、`docs/test/current/behavior-validation-method.md` T826-03。实验发布匹配安装、真实远端读取依赖和原生子审查记录可见性须在 V1 验证。若需要新建远端夹具或写入其 ref，先单独展示准备后的精确资源、命令与副作用。必要证据缺失时按其影响标出未验证区间。
