# Design Constitution

Authority identity：`guru-trellis-design-constitution-v1`；状态：`current`；适用范围：Guru Team Trellis extension repository。本文是五项设计原则正文与解释的唯一项目 authority；公共 Skill、schema、fixture、task artifact 与 `.trellis/spec` 只可引用 identity/short name，不得复制本文或把它转成机械评分表。

| Identity | Short name | Current principle |
| --- | --- | --- |
| `mature-practice-applicability` | 成熟实践与适用性 | 优先采用官方、成熟、可维护的扩展面与工程实践，但每次必须结合当前 task 的真实边界、风险和证据判断适用性；不因惯例本身制造无 consumer 的机制。 |
| `concept-semantic-completeness` | 概念与语义完整性 | 每个进入公共合同的概念必须有唯一 identity、owner、状态、边界、关系与生命周期；缺失适用语义时 fail closed，不以 optional 空字段或脚本默认值冒充判断。 |
| `cohesion-change-isolation` | 职责内聚与变化隔离 | 语义判断、确定性执行、项目 authority 与 task-local contribution 各归唯一 owner；跨边界只交换最小 typed projection，并行 task 不直接竞争 shared current。 |
| `minimum-necessary-complexity` | 最小必要复杂度 | 只实现 accepted happy path 和正文明确要求的 correctness/compatibility 边界；不增加无直接 consumer 的状态、wrapper、双读、锁、对抗模型或推测性抽象。 |
| `debt-one-way-convergence` | 技术债务单向收敛 | 新能力优先 `target_native`；保留 legacy 时必须选择可审查的局部收敛路径、明确 owner/GAP/退出与删除条件，禁止新增第二 authority、扩大无退出双写或让旧路径重新成为默认。 |

使用这些原则时，Architecture semantic owner 只记录与当前 task 真实冲突、权衡、例外或不足相关的 identity 和 evidence。未命中的原则不创建空白 verdict；no-impact/current-conforming task 不创建 contribution 或 ADR。
