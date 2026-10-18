# pack 帮助展示与 dry-run 整体需求

## 1. 来源与术语

本 Task 的 source.kind=no_issue。TaskId 为 `154-validation-flow`。无 GitHub Issue 关闭关系。

| 来源 | locator / 条款 | 角色 | 用途 |
| --- | --- | --- | --- |
| A | `validation-fixture/source-a.md` 全文 | 原始要求 | 保留帮助展示、dry-run、不覆盖承诺；其中改为 build 不采用 |
| B | `validation-fixture/source-b.md` 全文 | 要求 | 保留默认 dist 与全部共同承诺 |
| C | `conversation:current/source-c`，本次原生会话新增输入 | 要求 | D2 在目标已存在时仍可预演；只报告目标且零写入 |
| C-JSON | `conversation:current/source-c-json`，同次输入的 JSON 建议 | 建议 | 以后可考虑，不进入本次范围或验收 |
| 当前范围 | 本文 §3–7 | 要求 | 固化已澄清的产品行为，不保存授权过程 |
| 当前用法 | `validation-fixture/docs/usage.md` 全文 | 当前行为证据 | 默认、自定义目录、返回值、不覆盖 |
| 代码与测试 | `validation-fixture/sandbox/pack.py`、`validation-fixture/tests/test_pack.py` | 当前行为证据 | 解析、构建、回归基线 |

帮助指 CLI 的 `--help` 输出。dry-run 指只报告目标目录的预演，不执行构建。Delivery 是整体 Task 的切片，其完成不代表整个 Task 完成。

## 2. 背景与问题

现有 `build_parser()` 已支持 `--output DIR`，默认值为 dist，但使用 argparse.SUPPRESS 隐藏帮助。现有 main 解析后直接调用 build，没有 dry-run。usage 与现有三个测试确认普通构建使用 dist 或指定目录、创建 package.txt，成功返回 0；已有目标返回 2，不覆盖。

本地 CLI 调用者无法从帮助发现 output，也无法在零写入条件下预览目标。

## 3. 目标与非目标

整体目标包含两个独立能力：R1 帮助可发现性和 R2 dry-run。R3 兼容性贯穿两项。
首次 D1 只交付帮助；后续 D2 负责 dry-run。整个 Task 持有全部要求与最终验收责任，D1 的 partial 交付不得关闭整个 Task。

不改变默认目录为 build，不改变普通构建语义，不新增打包格式、远程服务、并发控制、安装器或发布机制。本轮规划不实现产品代码。

## 4. 真实调用方、场景与流程

| 场景 | 调用方及前置条件 | 触发 | 行为与可观察结果 |
| --- | --- | --- | --- |
| S1 | 本地 CLI 使用者，Python 可运行 fixture | pack --help | 输出 output 的用途、DIR 参数及真实默认 dist，返回 0；不构建 |
| S2 | 本地 CLI 使用者，工作目录确定 | pack --dry-run 或追加 --output artifacts | 解析目标，只报告 dist 或 artifacts；不创建目录或文件 |
| S2E | 本地 CLI 使用者，默认或显式目标已存在，可含 package.txt | pack --dry-run 或追加 --output DIR | 仍报告目标并成功返回 0；不进入普通构建的已存在拒绝分支；已有内容和目录树不变 |
| S3 | 现有本地构建调用者，目标不存在 | 无参数或 --output DIR | 按现有路径构建 package.txt，成功返回 0 |
| S4 | 现有构建调用者，目标已存在 | 普通构建 | stderr 报目标已存在，返回 2；已有内容不变 |

顺序为参数解析、选择预演或普通构建行为、输出结果。S1 由 argparse 帮助路径处理，不进入 build。dry-run 不得以普通构建来模拟预演。

## 5. 行为要求

- R1（A/B、S1）：pack --help 必须展示 --output DIR 的用途及实际默认目录 dist。帮助值必须与实际默认值一致。
- R2（A/B/C、S2/S2E）：新增 --dry-run。按同一 output 解析语义确定将写入的目录，只报告该目录，不创建任何目录或文件，不写 package.txt。默认与显式 output 都须承接。目标已存在时也须成功预演并返回 0；不得复用普通构建的已存在拒绝分支。已有目录树和文件内容保持不变。
- R3（B 与共同兼容承诺、S3/S4）：无参数普通构建仍使用当前工作目录下 dist；显式 --output DIR 仍使用该目录；成功返回 0、创建 package.txt；已有目标返回 2、stderr 说明原因且内容完全不变。不改默认为 build。
- R4（切片责任）：D1 独立实现 R1 并回归 R3；D2 完成 R2 并回归 R1/R3。D1 不提前引入 dry-run 实现。整体完成须覆盖 R1–R3，保留尚未交付的 R2。

来源未指定规范性技术设计。实现细化由 Author 与原 Architecture owner 承担，不重新提出已解决的产品问题。

## 6. 约束与依赖

真实入口为 `python3 validation-fixture/sandbox/pack.py`，相对目标基于进程 cwd。只涉及本地 Python CLI，无网络依赖、数据库字段或数据迁移。普通构建已有 FileExistsError 路径与返回值是兼容约束。

D2 消费 D1 已公开的 output 帮助与参数语义，不能复制第二套默认值。D1 不依赖 D2 才具有独立价值。dry-run 的输出措辞、测试组织由该 Delivery 的 Author 细化，不能削弱零写入要求。

## 7. 可观察验收与验证方式

| AC | 要求/场景 | 入口及输入 | 预期观察 |
| --- | --- | --- | --- |
| AC1 | R1/S1 | CLI --help | 返回 0，stdout 包含 --output、DIR、目录用途与 dist；不写目录文件 |
| AC2 | R2/S2 | 在受控空目录执行 --dry-run | 报告 dist；工作目录目录树前后相同，不出现 package.txt |
| AC3 | R2/S2 | --dry-run --output artifacts | 报告 artifacts；目标与父目录不存在时也不创建目录文件 |
| AC3E | R2/S2E | 已有 dist 或显式目标，内含原 package.txt，执行 dry-run | 返回 0、报告同一目标；目标目录树及文件字节前后相同，无新增目录文件 |
| AC4 | R3/S3 | 既有默认、自定义构建测试 | 分别在 dist 与指定目录生成 package.txt，返回 0 |
| AC5 | R3/S4 | 已有目标及已有 package.txt 后普通构建 | 返回 2、stderr 报错，原内容与文件集合不变 |
| AC6 | R4 | 整个 Task Completion | 两项 Delivery 的实际证据覆盖 AC1–5 及 AC3E；R2 未完成时保持 Task active |

这些是待实施的验收要求，不是已执行通过结果。D1 只验证 AC1、AC4、AC5；AC2/3/3E 保留 D2，AC6 由原 Completion 审查。C 只补充 D2 的既有目标场景，不改变 D1 的帮助方案或 partial policy。

## 8. 实际未决项

需求层没有必要未决问题。默认 dist 已明确；A 改 build 保持为未采用的历史候选，不改写来源 A 的原始身份。C-JSON 只是后续建议，本次不实现 JSON 输出。当前停在规划流程，不宣称实现或验收完成。D2 的方案尚未规划，仍由整个 Task 承担，不能作为 D1 的已交付事实。
