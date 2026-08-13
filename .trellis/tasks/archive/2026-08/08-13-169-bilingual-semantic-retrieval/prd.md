# #169 中英文概念族语义检索合同

## 目标

为 Guru Team 建立唯一、版本化、可分发的 semantic retrieval SSOT。实际拥有语义检索职责的 Skills 与 agents 必须按当前请求和 live authority 构造最小充分的中英文概念族，避免因单一语言零命中错误断言实现、测试、历史决定、duplicate、consumer 或 Docs authority 不存在。

## 权威与现状

- Live authority：<https://github.com/castbox/guru-trellis/issues/169>，2026-08-12 修订要求从 fresh `main` 独立实施。
- Base：`main@3323d630d05f2d873ed931c7cdfa468eaa037fda`。
- #132、#161、#156 是已完成历史基线；#108、#164 是独立关联范围。
- 当前仓库只有零散的文档语言说明，没有版本化 semantic retrieval SSOT，也没有所有实际 retrieval owner 对共享合同的显式引用。
- 当前生产扩展以 canonical preset/package/overlay 为长期源头，dogfood `.trellis/`、`.agents/`、`.codex/`、`.claude/` 和 `.cursor/` 为本任务要求覆盖的 installed projection；workflow 与平台入口不得复制 step-local 内部规则。

## 需求

### R1 唯一版本化 SSOT

新增一个 Guru Team 可分发、版本化的 semantic retrieval contract，统一定义：

1. 用户原始中文或英文表述；
2. 中文正式名、口语、缩写和历史旧称；
3. 英文术语、同义表达和历史命名；
4. 代码 symbol、配置 key、CLI、schema 字段、错误文本和路径 literal；
5. 当前仓库或历史证据中已出现的 legacy alias。

合同必须要求 AI 选择覆盖当前语义空间的最小查询集合，而不是机械地把每条命令执行两种语言版本。精确错误、symbol、CLI、key、字段和路径保留原文；只有确有另一语言召回价值时才扩展。

### R2 Owner 消费边界

以下实际 owner 必须显式引用共享合同并保持原有 semantic owner、typed exit 和 public I/O：

- `guru-discover-change-context`
- `guru-clarify-requirements`
- `trellis-research`
- `trellis-session-insight`
- `trellis-implement`
- `trellis-check`
- `guru-check-task`
- `guru-review-branch`

`guru-review-change-request`、`guru-review-contract-wording`、Task Commit、Publication、Finalizer 与 deterministic executors 不取得广泛 semantic retrieval ownership。

### R3 否定结论门槛

关于现有实现、入口、测试、fixture、外部验证、历史决定、旧合同、duplicate Issue/PR、字段/helper/schema/config consumer、重复 Docs authority 或既往问题的“不存在”结论，必须证明覆盖当前适用的中文概念、英文术语、literal identifier 与 legacy alias。单一语言零命中不得独立支撑结论。

### R4 AI 与脚本边界

- AI 构造概念族、选择查询、判断 evidence coverage 和结论充分性。
- Python/shell 只执行给定查询、读取事实和校验客观结构。
- 不新增同义词生成器、自动翻译器、命中次数 gate、query digest 或 semantic pass 脚本。

### R5 Evidence 与 artifact

- 不新增 tracked raw search report、逐条命中 transcript、长期关键词清单、query approval、授权字段或 reviewer 元数据。
- 不扩展 public DTO 来记录搜索过程。
- AI 在当前 gate 中说明概念范围、来源、关键证据和未覆盖边界。
- 只有形成长期 domain/workflow contract 的术语映射才进入 durable Docs SSOT。

### R6 分发与兼容

- canonical source、installed package、dogfood、Shared/Codex/Claude/Cursor contracts 与 eval 保持一致。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- preset apply/reapply、Trellis update/upgrade、`.new/.bak`、drift 和多平台 discovery 不得丢失或复制合同。

## 验收标准

- AC1：仓库中只有一个版本化 semantic retrieval SSOT；workflow 和平台 launcher 不复制其内部规则。
- AC2：R2 中每个实际 owner 显式引用 SSOT，非 owner 没有新增广泛检索职责。
- AC3：中文-only Docs 与英文代码 fixture 能恢复同一机制。
- AC4：英文 Issue/PR 与中文 Docs、commit 或历史会话 fixture 能恢复同一决定。
- AC5：current name、legacy alias、缩写和 literal symbol 混合 fixture 能发现复用、冲突或 consumer。
- AC6：仅执行单一语言搜索并给出错误否定结论的 semantic eval 不通过。
- AC7：精确错误文本与代码 symbol 不被机械翻译，保持 exact lookup 精度。
- AC8：eval 判断概念覆盖和结论充分性，不统计 `rg`、GitHub search 或 `trellis mem` 次数。
- AC9：不存在仅用于证明搜索过程的新 public DTO 字段、tracked report、query digest 或授权记录。
- AC10：source/installed/dogfood/Shared/Codex/Claude/Cursor 的合同和 eval 一致。
- AC11：clean marketplace init、preset apply/reapply、update/upgrade、`.new/.bak`、drift 与平台 discovery 验证通过。
- AC12：真实 semantic change、未知 dirty 内容、authority 变化和证据不足继续 fail closed。

## 非目标

- 通用搜索引擎、embedding、vector database、知识图谱或自动翻译服务。
- 每个查询机械执行中英文两个版本。
- deterministic script 中的同义词生成、充分性判断或 route 判断。
- 修改或重新审核 #132、#161、#108、#156、#164 或已完成的 #81。
- 恶意 actor、伪造、对抗输入、并发竞态、锁、TOCTOU、额外 fault injection 或跨 OS crash consistency。

## Docs SSOT Plan

- 新增唯一版本化 semantic retrieval contract 到 canonical Guru Team spec source，并同步 dogfood installed spec。
- 更新 workflow spec 索引，使 agents 能稳定发现该合同；不改 `.trellis/workflow.md` phase 或 typed-exit routing。
- 各 owner package/agent 只引用 SSOT 并描述自己在哪个语义 gate 使用它，不复制概念族清单。
- 当新增或改变安装路径、managed inventory 或用户安装命令时，更新 preset README/workflow README 的分发位置；否则不修改这两份 README。两者均不得复制合同正文。

## 开放问题

无。Issue authority、当前仓库 ownership 和官方 Trellis 扩展边界足以确定实现。
