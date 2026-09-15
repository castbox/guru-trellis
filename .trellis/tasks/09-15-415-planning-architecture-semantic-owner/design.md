# #415 Technical Design

## 1. 当前结构与根因

`guru-maintain-architecture-baseline` 的 runtime 已正确要求一个 AI-authored 2.0
`owner_result`，并只负责 schema、identity、freshness、project-check binding、consumer 和 typed
route 校验。缺陷不在 Architecture 2.0 runtime contract，而在两个执行可见层：

- `SKILL.md` 没有明确要求先完整读取 `references/contract.md`，也没有给出“当前 AI 判断 ->
  author owner result -> invoke wrapper”的直接步骤；
- 通用 native eval adapter 对 Architecture case 调用 `owner_recipe()` 后由 host 生成并写入
  `.trellis/.runtime/guru-team/evals/owner-result.json`，随后要求 Agent 不得改写它。

因此现有 eval 不能发现“Agent 把自己误判为缺失外部 owner”的回归。

## 2. 设计原则

- 保持 semantic owner 为 AI，host/runtime 只准备事实和验证结果。
- 保持一个正式 Architecture public wrapper 和现有 2.0 schemas/exits/consumers。
- 新增能力应是现有 native eval 的显式 case mode，不是生产 wrapper 或兼容路径。
- Agent 只能从 public Skill package、staged case facts 和 installed repository authority 作出判断。
- expected exit、owner recipe、预生成 semantic result 继续留在 eval control side，不进入模型
  evidence projection。

## 3. Skill 合同修订

### 3.1 Architecture owner

在 canonical `SKILL.md` 入口增加完整 contract 加载要求，并明确顺序：

1. 校验 profile/caller 并读取 public input；
2. 读取 contract、live authority、task/planning 与 project-check descriptor；
3. 执行必要 project check 并由 AI 解释其适用性、blocking 和 before/after 含义；
4. AI 完成 impact、change path、contribution/ADR、finding 和 route 判断；
5. AI 按 `semantic-result.schema.json` author 结果；
6. 使用正式 `scripts/invoke.sh` 提交 public input 与 owner result；
7. 只消费一个 declared exit。

合同增加故障分类：

- `owner_not_yet_executed` 是当前 owner 要继续完成的内部状态，不是 typed stop；
- authority/check 缺失映射现有 incomplete/blocked exits；
- wrapper 校验错误要求当前 owner 修正或 fresh reread；
- 只有平台确实不能执行合同要求的 AI owner/read/invoke 能力时才报告执行能力缺失。

### 3.2 Planning approval

相邻 Skill 只补强 consumption 表述：fresh `baseline_current` 已证明上游 Architecture owner
完成；Planning owner reread live authority 并做自己的八维判断，不重建或外包 Architecture
owner result。public DTO、private checkpoint 和 activation pause 均不变化。

## 4. Native Eval Authoring Mode

### 4.1 Case 声明

扩展 `skill-evals.schema.json`，为 case 增加一个闭合枚举字段（暂名
`native_execution_mode`）：

- 未声明该字段和显式 `post_owner`：保持当前预生成 owner result 行为；
- `semantic_authoring`：host 只 stage public input、task、planning、Architecture authority、
  project-check descriptor/command/evidence，不创建 owner result。

仅首个 Architecture Planning happy-path regression 使用 `semantic_authoring`。所有未声明该
字段的现有 case 均按 `post_owner` 处理；不得通过 skill-id 或 case-id 隐式特判执行模式。

### 4.2 Fixture staging

在 `owner_staging.py`/`fixture_io.py` 中拆开“事实 staging”和“owner result staging”：

- 两种模式都安装真实 canonical package，建立 planning task 与 authority 文件，绑定 current
  Git/content identities；
- `semantic_authoring` 不调用生成 Architecture owner object 的 recipe 分支，不写
  `OWNER_RESULT`，也不执行 `bind_owner_result_argument()`；
- facts 仅描述可观察场景和 public invocation 形式，不携带 expected decision；
- project check 可由 fixture 提供确定性 command/result contract，但 blocking/semantic conclusion
  仍由 Agent author。

### 4.3 Agent-visible context

复用现有 qualification native sandbox 的成熟边界，并抽取为可被 Architecture authoring case
使用的通用 semantic authoring context：

- 公开投影包含 `SKILL.md`、`references/contract.md`、`interface.json`、所需 input/result schemas
  与 `scripts/invoke.sh`；不包含 `evals/` 和 runtime private control。
- repository evidence projection 包含 task/planning、Architecture authority、project check
  entrypoint 及当前 Git identity。
- prompt 要求 traced read 完整 Skill contract、public input/result schema、所有 staged case facts 与必要 live
  authority，然后构造一次 call-local invocation envelope。
- 不告诉 Agent expected exit，禁止搜索 eval corpus，禁止读取 `.trellis/.runtime`。

### 4.4 Invocation 与 trace validation

扩展 public runtime boundary，使 `semantic_authoring` 接收 Agent 通过 stdin 提交的完整
`public_input + owner_result` envelope，转交真实 installed `scripts/invoke.sh`。

trace validator 对该模式要求：

- Skill 与 `references/contract.md` 均已读取；
- interface、public input/result schemas、全部 case facts 和规定 authority 已读取；
- 恰好一次正式 public invocation；
- 无 eval corpus/private runtime 读取；
- wrapper stdout 是 schema-valid 的唯一 expected typed exit；
- repository fixture 中不存在 host 预写的 owner-result 文件。

host 仍可比较最终 exit 与 eval metadata，但不得据此为 Agent author semantic fields。

## 5. 测试设计

### T1 Contract tests

- Architecture Skill 强制 contract load、owner sequence 和故障分类文案存在。
- Planning approval 承接 current Architecture result，不要求第二 owner。
- eval schema 接受两种明确 mode，拒绝 unknown mode。

### T2 Adapter/runtime tests

- `post_owner` cases 保持原有 staging、binding 与 trace 行为。
- `semantic_authoring` fixture 不生成 owner result，Agent-visible request 不含 expected decision。
- traced contract/authority reads 与单次 stdin invocation 均为必需。
- 缺少 authority、遗漏 contract read、读取 private/evals、重复 invocation、wrapper validation
  failure 均 fail closed。

### T3 Native behavior regression

- 使用真实 Architecture package 和 installed preset fixture运行 Planning happy path。
- task、`prd.md`、`design.md`、`implement.md`、active baseline、current constitution、change
  contract 和 project check 均完整。
- Agent 自行判断 `no_architecture_impact`，author 2.0 result，得到
  `baseline_current(source_profile=task_impact_sync, stage=planning)`。
- regression 不依赖预填 owner result、关键词断言或 fake semantic pass。

### T4 Projection/install validation

- package unit/contract tests；native eval focused case；eval runtime tests。
- canonical/installed package parity 与 Agent/Codex/Claude/Cursor projection parity。
- `apply.sh --repo .` 后检查 `.new`/`.bak`，运行 dogfood overlay drift checker。
- 最多一个代表性 clean throwaway，仅当修改后的 eval/preset 安装路径需要证明 clean install；完整
  多平台矩阵 deferred 给专门 Release/Upgrade Issue。

## 6. 兼容性与迁移

- Architecture 2.0 public input/result/output schema、exit id、consumer id 和 wrapper argv 不变。
- 新 eval case 字段只扩展 repository-owned eval manifest；缺省保持现有 post-owner 行为。
- 不迁移或读取旧 owner result，不新增生产 runtime state。

## 7. Architecture Impact

规划判断：`no_architecture_impact`。

本任务修正既有 semantic governance owner 的执行说明和行为验证，不改变 shared authority、
Skill public I/O、owner boundary、single writer、持久化或 integration boundary。若实现需要新的
生产 owner/runtime、public contract 或共享 authority，则必须停止并重做 Architecture planning。

## 8. Docs SSOT Plan

以 `prd.md` 第 7 节为唯一 Docs SSOT Plan。durable change 限于两个 package-local
Skill/contract；repository RDT 与 Architecture shared SSOT 记录 `no_update`。
