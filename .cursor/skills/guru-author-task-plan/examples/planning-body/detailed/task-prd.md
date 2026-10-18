# 数据清单校验整体需求（教学正文）

## 1. 来源与术语

本正文基于完整 [source 第1节](source.md#1-当前要求)。这是教学输入，不是实际 Task acceptance。

| 来源 | 角色与用途 |
| --- | --- |
| source 第1节 R1–R4、AC1–AC5 | 当前要求、约束及整体验收。 |
| source 第1节 D-A/D-B | 已约定设计，保留引擎/adapter 分工及完整校验先行。Delivery design 第3节唯一处置。 |
| source 第2节、第3节 | 示例仓库事实和 canonical requirement/design/test/Architecture，定位既有能力和边界。 |
| source 第4节 C1/H1/E1 | 分别为建议/历史/示例证据，不能变成当前要求。 |

清单是含 version/entries 的 JSON；启用项是 enabled=true 的条目。missing_file 是文件不存在或不是普通文件的业务结果，不能等同清单格式异常。

## 2. 背景与问题

CI 维护者现在逐个查文件，输出不能区分坏清单与缺文件。既有 cli.py 只有 version，没有 check。目标让 CI 与本地调用得到稳定的 JSON 和退出语义，同时保留只读边界。

## 3. 目标与非目标

整体交付清单校验引擎与 `report check <manifest>`。覆盖 R1–R4 和 AC1–AC5。排除内容校验、网络、缓存、修复、写报告及文本输出。整体 Completion 需要引擎、CLI 集成、全部适用验证和原审核，单批合并不够。

## 4. 真实调用方、场景与流程

| 场景 | 调用方 | 前置条件 | 触发 | 行为 | 可观察结果 |
| --- | --- | --- | --- | --- | --- |
| S1 | CI runner | 清单合法，含启用文件 | 运行 check | 先完整校验，再按序检查 | JSON 有序，全部存在则 exit 0。 |
| S2 | 本地操作员 | 清单合法，含 disabled 和缺失项 | 运行 check | 跳过 disabled，缺失后继续 | skipped/missing_file 按输入顺序，exit 1。 |
| S3 | CI runner | 输入不可读或清单格式/字段错误 | 运行 check | 停止文件检查并报告原因 | stdout 空，stderr 具体错误，exit 2。 |

执行顺序是读取→完整格式校验→逐项结果→输出。S2 的 skipped 是检查文件的例外，不是整体字段校验的例外。

## 5. 行为要求

R1：check 读取 UTF-8 JSON；version=1，entries 为数组。每项 id/path 是非空字符串、enabled 是布尔，id 全局唯一；path 相对清单所在目录。格式或字段错误时不检查任何文件。

R2：合法清单按输入顺序产生结果。enabled=true 时检查普通文件，缺失或目录记 missing_file 后继续。enabled=false 时返回 skipped 且不访问 path。空 entries 合法。

R3：正常 stdout 仅一个对象 `{version:1, results:[{id,status}], ok}`。status 仅 ok/missing_file/skipped；没有 missing_file 时 ok=true、exit 0，否则 ok=false、exit 1。只含 skipped 或空数组亦为成功。不可读、JSON 或字段错误时 stdout 空、stderr 具体原因、exit 2。

R4：只读清单及启用项；不创建文件、不修改输入；version 原行为不变。D-A/D-B 的纯引擎、adapter 分工、标准库依赖和完整校验先行是约定约束，设计落点由选定 Delivery design 第3节承接。

## 6. 约束与依赖

运行依赖为现有 Python 标准库，无 DB、网络或服务。入口复用现有 `python -m report`。Discovery 已给出教学事实快照；实际实现前必须读真实源码。R2 的 disabled 不访问要求与测试注入接口是当前职责，不能以“减少代码”去掉。

## 7. 可观察验收与验证方式

| AC | 要求/场景 | 入口与输入 | 预期观察 |
| --- | --- | --- | --- |
| AC1 | R1/R2，S1 | 引擎与 CLI；合法/空清单、相对路径文件 | 有序结果，base_dir 正确，空清单 exit 0。 |
| AC2 | R2，S2 | 记录 is_file 调用；disabled 在存在/缺失项之间 | disabled 不调用，结果仍保持完整顺序。 |
| AC3 | R2/R3，S2 | 缺失文件、目录及后续普通文件 | 前两项 missing_file，后项仍检查，CLI exit 1。 |
| AC4 | R1/R3，S3 | 不可读、坏 JSON、字段错误、重复 id；合法项在坏项前 | 错误先于任何文件检查；stdout 空、stderr 原因、exit 2。正常输出字段/ok/exit 符合 R3。 |
| AC5 | R4，S1–S3 | 真实 CLI，比较输入和目录；运行 version | 无写入，version 原输出/exit 不变。 |

以上为验收设计，未运行，不声明通过。

## 8. 实际未决项

教学输入已明确产品与范围，没有必要未决问题。实现的数据类型和异常消息由原 Author/Architecture 设计；这不构成待用户回答。实际仓库与快照不一致时，由原事实/阶段 owner 处理后再接受。
