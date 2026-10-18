# full D1 pack 帮助设计（教学正文）

## 1. 设计目标、需求承接与内容基线

承接 [D1 PRD](delivery-prd.md) R1–R3/AC1–AC3及 [Task PRD](task-prd.md)。完整来源见 [source](source.md)。B为source §2教学快照，无真实SHA；实际项目用原projection确定B及来源，另列H0和PR目标。阶段适用Architecture是source §2的parser/build边界；示例不提供实际候选结论。

## 2. 当前系统、边界与目标差额

首次无前序。build_parser已注册output但隐藏。只改cli.py的该选项help文案和usage.md说明，补help观察；不改build.py、default、metavar或执行路径。

## 3. 来源设计处置

已读source §1–3。请求只给目标和保持约束，没有规范性来源设计，因此不生成空矩阵。source §2是当前repo分工和事实，方案仍须遵守；本批具体落点如下。

## 4. 模块、职责与设计取舍

cli.build_parser把`help=argparse.SUPPRESS`换为“输出目录（默认：%(default)s）”。保留default='dist'和metavar='DIR'；用argparse现有插值显示真实默认，避免文案另藏默认值。usage增加--output DIR用途、默认dist和已有目录失败说明。build仍负责构建和不覆盖。直接使用现有parser，不加帮助生成器或并行模板。

## 5. 接口与数据

既有接口为argv `--help`→argparse→stdout/exit0；`--output DIR`→既有args.output→build。只使已注册选项可见并增加说明，参数和值不变。没有新API、公共DTO或持久化字段，不创建schema填空。

## 6. 状态、顺序、正常与失败流程

无持久状态。build_parser→parse_args：--help时展示后exit0；普通执行仍把output传build。已有目标的失败结果保持。帮助路径无构建调用，不新增恢复分支或状态机。

## 7. 恢复、兼容、迁移与集成

只改帮助及文档，无数据迁移。CLI已有参数/执行行为保留，无旧reader或adapter；不增长期兼容层。帮助输出只读，无执行进度或DB/服务回滚。没有前后批次接口；后续若要改默认/覆盖须经新要求，不能夹带。

## 8. 验证设计

V1：真实help子进程+临时目录，观察--output、用途、默认dist、exit0和无产物→AC1。V2：跑原默认/显式/已有目录不覆盖用例，核对R2→AC2。V3：原owner对照usage和真实help、审参数/执行diff→AC3。只增加对实际可见行为的观察，不锁定整段help的换行或排序。无安装/远程链路或实际Agent验证义务；均未执行。

## 9. Canonical 引用、本轮差额与实际未决项

读source §2四类authority摘录，差额是可见帮助及usage，parser/build边界不变。真实RDT owner维护该差额，Architecture owner按原合同判断影响，不因模板创建空贡献或改共享导航。没有必要未决项；真实事实不符时返回原owner。
