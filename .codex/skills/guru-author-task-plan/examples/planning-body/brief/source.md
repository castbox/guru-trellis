# 简略工程来源与调查材料（教学输入）

本目录是去敏、合成教学材料；不是实际仓库、用户答复或测试证据。

## 1. 简略请求

“让 `pack --help` 显示已有 `--output` 选项的用途和默认目录。现有执行行为保持。”这个请求也可来自无 Issue 对话；没有 Issue 不改变调查和正文义务。未提供实现方案。

## 2. 可查证的示例事实

这些是教学提供的文件摘录，实际 Discovery 须查真实文件，不得只套用本例。

- `src/pack/cli.py:build_parser`：argparse 注册 `--output`，`default='dist'`、`metavar='DIR'`，当前 `help=argparse.SUPPRESS`。main 先 parse_args；`--help` 由 argparse 输出后退出，不调用执行函数。
- `src/pack/build.py:build`：输出到给定目录；目录已存在时返回错误，不覆盖。该行为及默认 dist 已由现有测试覆盖。
- `tests/test_cli.py`：有显式/默认 output 参数及目录已存在不覆盖测试；使用 unittest。尚无 help 包含 output 的断言。
- `docs/usage.md`：当前说明默认 dist、目标存在则失败；尚未描述 --output 选项。没有和代码冲突的产品口径。
- `docs/requirements/cli.md` §输出：本地命令指定输出目录，缺省dist，目标存在则失败。
- `docs/design/cli.md` §parser：argparse 负责help和参数，build模块负责写入；`docs/test/cli.md` §输出行为：原显式/默认/存在目标回归。
- `docs/architecture/cli.md` §边界：单进程CLI，parser和build分工，不新增服务或持久化状态。

这些路径属于教学仓库。下列正文通过本节定位完整摘录，不声称这些文件存在于 Guru 扩展源仓库。

## 3. 来源角色和实际信息边界

第1节是当前要求，第2节是可调查事实和既有canonical约束。请求没有指定实现机制；现有parser分工是repo约束，不是来源已选定的新方案。不存在规范性来源设计，不生成空来源设计处置矩阵。

若真实仓库无法查到默认目录，或文档与代码的输出行为相冲突，Clarify须保留“默认/覆盖口径未确定”的具体gap。涉及产品选择时问实际用户；未回答前不能宣称requirements_ready。这个分支没有用户回答，本目录也不默认选择一方。下面完整正文仅基于第2节所给事实一致的教学输入。
