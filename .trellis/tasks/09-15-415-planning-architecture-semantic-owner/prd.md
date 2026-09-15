# #415 修复 Planning Architecture semantic owner 自阻塞

## 1. 背景与问题

2026-09-15，`wesleywu/chengtuo-resume` 的 Issue #323 按标准 Guru Team
Planning 流程执行
`guru-maintain-architecture-baseline:task_impact_sync(stage=planning)` 时稳定停止。
执行 Agent 已读取 Architecture authority 并理解脚本不能代替语义判断，却把这一边界
误解为必须依赖一个外部 semantic owner，随后无法生成 `owner_result`、无法取得
`baseline_current`，也无法进入 `guru-approve-task-plan`。

live authority 为 `castbox/guru-trellis#415`。当前 canonical 与已安装 package 的
Architecture Skill 实质一致；仅升级 extension 不能证明问题已经修复。现有 native eval
由 host 预先构造并写入 owner result，只证明 post-owner deterministic route，未证明
真实 Agent 会承担 semantic owner 职责。

## 2. 目标

确保当前合同指定的 Architecture semantic owner 在 Planning 正常路径中完成以下闭环：

1. 加载完整 public Skill contract；
2. 读取 live task、planning、Architecture Baseline、Design Constitution、change contract
   与 applicable project check；
3. 由当前执行 AI 形成语义判断；
4. 由该 AI 编写完整 `owner_result`；
5. 调用正式 deterministic wrapper 校验 identity、freshness、schema、consumer 与 route；
6. 消费唯一 typed exit，并在 `baseline_current` 时继续 Planning approval。

## 3. 功能需求

### R1 Architecture Skill 执行合同

- canonical `guru-maintain-architecture-baseline` 必须直接要求完整读取
  `references/contract.md`。
- Skill 必须明确当前合同指定的执行 AI 就是 semantic owner；“runtime 不生成语义判断”
  不能被解释为“需要另一个外部 owner”。
- Skill 必须给出可执行的 authoring/invoke 顺序，并区分：owner 尚未执行、authority 或
  project check 真实缺失、deterministic validation 失败、平台确实缺少合同要求的执行能力。
- 重复用户确认不是生成语义判断的前置条件，也不得被记录为 owner result 或授权 artifact。

### R2 Planning approval 承接

- `guru-approve-task-plan` 必须明确 fresh
  `task_impact_sync(stage=planning):baseline_current` 是相邻上游结果。
- Architecture owner 已由当前合同指定并完成时，Planning approval 不得再次寻找外部 owner，
  也不得重复 Architecture 私有判断。
- 非 current typed exits 继续使用现有 fail-closed router；不得降低 Architecture 或 Planning
  approval 门禁。

### R3 Native Agent 行为回归

- 新增一个真实 native Agent eval，覆盖 task 为 `planning`、三份 planning 文档、
  Architecture authority 和 project check 均存在的正常路径。
- 该场景不得由 host 预填 pass、expected decision 或完整 owner result。
- Agent 必须读取真实 canonical/installed public package，亲自 author semantic result，调用
  正式 wrapper，并返回 `baseline_current`。
- trace 必须能够证明完整合同读取、必要 authority 读取、一次正式 public invocation，以及
  Agent 未读取 eval corpus/private runtime 来推导期望答案。
- 保留现有 post-owner eval；新增模式只用于需要证明 semantic authoring 行为的明确 case。

### R4 投影与安装一致性

- canonical package 是修改源头；同步 dogfood installed package、`.agents`、`.codex`、
  `.claude` 和 `.cursor` 五类声明投影。
- preset reapply 后不得产生未处理 `.new`/`.bak` 或 projection drift。

## 4. 验收标准

- [ ] 正常 Planning 场景中，Agent 不以“脚本不能生成 semantic owner result”为理由停止。
- [ ] Agent 先形成语义判断并 author 完整结果，再调用 deterministic runtime。
- [ ] authority 完整且判断通过时产生 fresh `baseline_current`，并可进入
      `guru-approve-task-plan`。
- [ ] authority、project check 或执行能力真实缺失时返回具体 declared exit/error，不泛化为
      “无法生成 owner result”。
- [ ] 重复用户确认不参与 owner authoring，也不被持久化。
- [ ] native regression 可复现旧缺口，并证明修复后同一正常路径不再自阻塞。
- [ ] regression 使用 canonical/installed package 与正式 wrapper，不通过 fake/pre-authored
      semantic decision 制造通过。
- [ ] source、dogfood、installed 和声明平台投影一致；preset reapply 与 drift 检查通过。
- [ ] Architecture 2.0 schemas、public exits、consumers、freshness 与 fail-closed 语义不变。

## 5. 非目标

- 不修改 `chengtuo-resume` 或继续其 Issue #323。
- 不实现 #404 的独立 reviewer 模型，不实现 #292 或 #398 的生命周期重构。
- 不让 Python/shell 生成、选择或改写 Architecture 语义判断。
- 不新增 wrapper、兼容读取、平行 Architecture authority、长期 handoff、授权 artifact、
  retry/lock/fallback 或新的 public Skill I/O。
- 不降低现有 Architecture、Planning approval、task activation 或 publication 门禁。
- 不执行专门 Release/Upgrade Issue 才拥有的完整多平台 throwaway 矩阵。

## 6. 约束与风险

- 必须遵守 AI semantic judgment 与 deterministic script 的现有职责边界。
- eval authoring 模式不得向 Agent 暴露 expected exit、owner recipe 或 corpus 答案。
- 新模式应复用现有 native trace、public projection 与 installed fixture，不形成第二套 eval
  runtime。
- 实现发现 schema/public I/O 或 Architecture authority 必须变化时，本计划失效并重新进入
  Planning Architecture gate。

## 7. Docs SSOT Plan

策略：`contract_local`。

- 更新 `guru-maintain-architecture-baseline` package 的 `SKILL.md` 与
  `references/contract.md`，它们是本缺陷执行语义的直接 durable owner。
- 仅在承接文字确有歧义时更新 `guru-approve-task-plan` 的 `SKILL.md` 与 contract。
- 不更新 repository Requirements/Design/Test shared authority：Issue #415 已完整定义行为需求，
  task planning 提供本次实现与验证设计，改动不引入产品能力、public I/O 或新架构决策。
- 不更新 Architecture shared authority 或 ADR：本任务纠正当前合同/测试对既有 AI owner 语义的
  表达与证明，预期结果为 `no_architecture_impact`。
- 若实现期发现上述判断不成立，停止写入并重新执行 RDT/Architecture impact sync。
