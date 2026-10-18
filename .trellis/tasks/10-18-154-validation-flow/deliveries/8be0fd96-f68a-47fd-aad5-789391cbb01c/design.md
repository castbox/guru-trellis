# D1：pack 输出目录帮助设计

## 1. 设计目标、需求承接与内容基线

本批承接 prd.md 的 D1-R1–R4、D1-S1–S3 与 D1-AC1–AC4。整个 Task 的 R2 dry-run 与 AC2/3 留给 D2，D1 不是整个 Task Completion。

原 public DeliveryProjection.content_base 已返回 B=`b1b096df218c25442ebdeebed72e9025c4c847e4`，来源为本次显式 development baseline；首次 Delivery 没有历史候选或 prior delivered head。Planning H0 同为该 OID，仅为规划观察。未来内容范围为固定 B..实际实现 HEAD 加本批 dirty increment；PR target 为 castbox/guru-trellis 的 codex/154-validation-base，与 B 和最终实现 HEAD 分别管理。

原独立 Architecture candidate_assessment 已实际返回 baseline_current、no_architecture_impact：baseline `current-main-0.6.17-guru.98`，constitution `guru-trellis-design-constitution-v1/current`。适用 authority 为 docs/architecture/README.md、00-foundation/design-constitution.md 与 06-governance/change-contract.md。候选未改变架构边界，无需 contribution/ADR。最终设计仍须 Wording-current 的原 final_plan，不把候选结论当最终批准。

## 2. 当前系统、边界与目标差额

当前 validation-fixture/sandbox/pack.py 中 build_parser 已声明 --output、metavar DIR、default dist，help 是 argparse.SUPPRESS。main 解析后调用 build；build 检查目标存在、创建目录、写 package.txt。

没有前序 Delivery。D1 只把该 action 的帮助元数据从隐藏改为可见，并增加对真实 CLI 帮助的测试及更新 fixture usage。目标为帮助可发现，参数输入和普通构建数据流不变。不新增 dry-run 分支；不重构 main/build；不引入额外默认值常量、wrapper 或 formatter。

## 3. 来源设计处置（唯一）

已完整读取 source-a.md、source-b.md 和根 PRD。A/B 是产品要求，没有指定规范性技术设计，故不建立空设计处置矩阵。

当前行为取舍是保留 dist 与普通构建，A 的改 build 要求不采用。A/B 的帮助、dry-run 和不覆盖要求保持：帮助落实于本设计 §4–8，dry-run 仍由根 PRD 与后续 D2 承担，未被本批删除。该产品边界不由技术设计重新解释。

## 4. 模块、职责与设计取舍

| 模块/文件 | 输入、职责、输出 | 本批差额 |
| --- | --- | --- |
| pack.py build_parser | 声明 argparse action，供 main 和 --help 消费 | 将 help 改为“输出目录（默认：%(default)s）”；保留 metavar/default |
| argparse | 解析已有 --output，按 action 的真实 default 插值帮助 | 复用已有内置能力，不新增 formatter |
| pack.py main/build | 解析后的 output、普通构建与 FileExistsError 处理 | 不改；回归验证 |
| tests/test_pack.py | subprocess 调用真实 CLI，观察返回值、stdout/stderr 与文件系统 | 新增一个帮助行为用例；保留已有三例 |
| docs/usage.md | fixture 实际使用说明 | 更新 output 帮助可见事实；dry-run 尚未实现的说明保留 |

选择 argparse 的 %(default)s，避免把 dist 再写成一份独立帮助默认值。仅硬编码帮助里的 dist 会产生双处维护；新增全局 formatter 会影响其他 action，当前没有必要。直接修改已有 action，无并行实现路径或兼容层。

## 5. 接口与数据

CLI 仍为 `python3 validation-fixture/sandbox/pack.py [--output DIR]`。--output 的生产者是本地调用者，argparse 解析后仍输出 args.output 给 main/build。未指定为字符串 dist，显式输入 DIR 原样按现有 Path 语义使用。

可观察接口变化仅为 --help：stdout 展示 --output DIR、目录用途和实际 dist，成功退出 0；stderr 为空。没有新增 API、配置字段、持久化模型或 schema。package.txt 内容与构建 stdout/stderr 的普通路径保持。

## 6. 状态、顺序、正常与失败流程

1. main 调用 build_parser。
2. 传入 --help 时，argparse 格式化现有 action 的说明，以其 default 插值；输出并退出 0，不返回到 build。
3. 普通无参或 --output DIR 时，解析仍进入 build。
4. 目标不存在时，build 按现有顺序创建目录和 package.txt，main 打印已构建并返回 0。
5. 目标已存在时，build 抛 FileExistsError，main 向 stderr 写现有原因并返回 2，不覆盖任何已有内容。

本批无持久化状态转换或新增恢复协议。未知参数和 argparse 的已有退出语义不改；不为该元数据变更增加异常包装或 fallback。

## 7. 恢复、兼容、迁移与集成

现有 --output 调用者不需迁移；默认目录、显式相对/绝对目录与普通构建行为保持。没有数据库、配置或数据迁移。帮助变化没有写入副作用，无需业务回滚协议；后续实现若失败，原 Author/Check 修复本批差额并保留其他并行改动。

D2 从本批的同一 --output action 消费目录选择语义；其 --dry-run 不得另建默认权威。D1 不预埋 D2 参数或执行分支。D1 的使用与验证均不依赖 D2 完成。整个 Task 后续由 Completion 识别剩余 R2，走后续独立 Delivery，不能因帮助交付而关闭整体责任。

## 8. 验证设计

| V | 对应要求/验收 | 测试层、入口与输入 | 预期观察与检测价值 |
| --- | --- | --- | --- |
| V1 | D1-R1/R4，AC1/2 | subprocess 真实 CLI --help，在受控空目录 | returncode=0、stderr 空；stdout 含 --output、DIR、输出目录说明、dist；目录树前后相同。若仍隐藏帮助或错误地触发构建会失败 |
| V2 | D1-R2，AC3 | 现有 test_default_output/test_explicit_output | dist 或 artifacts 下 package.txt 正确，returncode=0；检测帮助编辑误改 default/参数解析 |
| V3 | D1-R2，AC4 | 现有 test_existing_target_is_not_overwritten | returncode=2、stderr 原因、原内容和文件集合保持；检测普通构建拒绝路径回归 |
| V4 | 文档一致性 | 阅读 usage 与真实 CLI 输出、代码及 V1–V3 结果 | 帮助可见与实际一致，dry-run 仍标未实现，不预填结果 |

新帮助用例直接运行实际 CLI，不通过源码字符串自比或复制 parser 模拟。无需为每个帮助词再加重复用例。计划命令见 implement §3。当前只有规划，V1–V4 的目标结果尚未执行。无需安装/upgrade、多平台矩阵、网络或生产链路证明。

## 9. Canonical 引用、本轮差额与实际未决项

需求/行为 authority：根 prd.md §5/7、来源 A/B；实际调用说明为 fixture docs/usage.md。
设计与测试依据：现有 pack.py 的 build_parser/main/build 和 test_pack.py；本批差额见 §2/4/8。
共享 RDT current .107（docs/requirements、docs/design、docs/test 的版本入口）管理 Guru 扩展，不因隔离 fixture 帮助变化扩出共享业务合同。原 RDT owner 已返回 ssot_current；fixture usage 仍须在 Phase2 以 delta_first 同步，见 implement §6。
Architecture authority 同 §1，原 owner 负责最终评估；本批不直接写共享 baseline、constitution、index 或 spec，不创建空 contribution/ADR。
无必要技术未决问题；若后续候选变化，回原 Author/Architecture 刷新依赖，不能借本设计放大范围。
