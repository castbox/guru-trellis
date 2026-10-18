# full D1 pack 帮助需求（教学正文）

## 1. 整体来源与术语

读 [Task PRD](task-prd.md) 和 [source §1–3](source.md)。本批覆盖整体R1–R3/AC1–AC3；不是实际DeliveryKey或范围接受结果。output仍是已有目录参数。

## 2. 整体与本批目标、非目标

整体消除help隐藏output造成的发现障碍。本批一次交付help显示、usage同步和行为保持验证。排除改默认dist、覆盖语义、参数集合、build实现或发布；没有另留功能。

## 3. 本批起点、前序结果、依赖与剩余责任

首次Delivery，无前序。source §2起点为SUPPRESS隐藏的既有output选项。依赖当前parser和unittest，无外部服务。D1承担全部适用验收；没有计划剩余切片不代表已经完成。真实结果交原Completion判断整体责任。

## 4. 本批调用方、场景与流程

S1：本地操作员在可启动环境调用pack --help，argparse显示output用途/默认dist后exit0，不执行build。S2：现有调用方按原默认/显式路径执行，已有目录仍失败且不覆盖。流程仍是parser解析→help早退或既有build，不加新状态。

## 5. 完整行为、条件与约束

R1：帮助可见--output，说明其用途为输出目录及默认dist；exit0，help不调build。R2：保持原default/metavar/解析和执行路径，缺省dist、显式目录及已存在失败不覆盖都不变。R3：usage和帮助同义，不引入新参数、模式或覆盖能力。无规范性来源设计，依据见design第3节，不建空矩阵。

## 6. 本批验收、验证方式与未决项

AC1/R1/S1：真实help入口和临时目录，观察选项/用途/默认值、exit0、无构建产物。AC2/R2/S2：原默认/显式/已有目录回归，观察执行含义保持。AC3/R3：原owner比较usage和实际help，并核对参数/行为diff。未执行，无通过声明。当前无必要未决产品选择；实际事实冲突回Clarify。

## 7. Canonical 引用与本轮差额

实际读source §2的requirement输出、design parser、test输出行为及Architecture边界摘录。本轮差额为帮助可发现性和usage，默认/构建分层不变；真实repo由原RDT/Architecture owner按实际影响处理，不造空contribution。
