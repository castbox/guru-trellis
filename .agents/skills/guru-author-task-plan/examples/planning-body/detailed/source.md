# 详细技术来源：数据清单校验（教学输入）

本文及同目录正文是去敏、合成的教学材料。文件名、接口、快照和历史均用于演示写作方法，不属于真实业务仓库，不是实际用户答复、Git/Delivery 结果或运行证据。以下各节是示例内可读取的完整输入；实际项目必须读取真实来源和仓库文件。

## 1. 当前要求

背景：CI 维护者现在逐个打开清单中的文件查缺项，不能稳定区分“清单格式错误”和“文件缺失”。调用方是 CI runner 和本地操作员，没有面向最终消费者的界面。

- R1：新增 `report check <manifest>`。输入清单为 UTF-8 JSON，顶层 `version` 必须为 `1`，`entries` 为数组。每项必须具有非空字符串 `id`、非空字符串 `path` 和布尔 `enabled`。全部项的 id 不得重复。path 以清单所在目录为基准。格式或字段不合法时停止，不检查任何文件。
- R2：对于 enabled 为 true 的项，按清单顺序检查普通文件是否存在。缺失文件和目录都产生 `missing_file`，其余项继续检查。enabled 为 false 的项返回 `skipped`，不得访问其 path。空 entries 合法。
- R3：输出一个 JSON 对象到 stdout，包含 `version:1`、`results` 和 `ok`。results 按输入顺序，每项仅含 `id` 与 `status`；status 为 `ok|missing_file|skipped`。清单合法且没有 missing_file 时 ok 为 true，否则为 false。正常存在 missing_file 时 exit 1；全部通过或只含 skipped 或空 entries 时 exit 0。输入不可读、JSON 或字段错误时 stdout 为空，stderr 输出具体原因并 exit 2。
- R4：命令只读清单及启用项，不创建报告文件，不修改输入。现有 `report version` 行为不变。不增加网络请求、修复命令、文件内容校验或文本输出模式。

约定设计 D-A：纯校验引擎 `validate_manifest(document, base_dir, is_file)` 不打印、不退出、不写盘；返回有序 CheckResult 或格式异常。CLI adapter 负责读取 JSON、输出和 exit 映射。`is_file` 是当前测试与真实文件检查的注入边界，不是未来 provider 插件。

约定设计 D-B：先校验完整文档和重复 id，再检查 enabled 项；disabled 项在文件检查之前分支。缺失结果是普通业务结果，不是格式异常。保留 Python 现有标准库实现，不引入第三方依赖。

验收：AC1 覆盖合法、空清单和相对路径；AC2 覆盖 disabled 不访问与顺序；AC3 覆盖缺失/目录但继续处理；AC4 覆盖输入错误先失败、JSON/exit 契约；AC5 覆盖只读和原 version 命令。

## 2. 示例仓库事实快照

这是教学作者提供的快照，不声称执行过搜索或命令。

- `src/report/cli.py`：已有 `main(argv)` 和 `version` 分支；没有 check 命令。入口由 `python -m report` 调用。
- `src/report/__main__.py`：只调用 cli.main；不承载业务判断。
- `tests/test_cli.py`：已有 version 的 stdout/exit 测试。测试 runner 为 `python -m unittest discover -s tests`。
- `src/report/checker.py`、`tests/test_checker.py` 尚不存在。采用标准库 unittest，包无需数据库、后台任务或远程服务。
- 示例内容基线 B 为本节快照；示例不提供真实 Git SHA。实际 Author 必须用原 content_base projection 写真实 B/来源并另列 PR 目标，不能把这个标记用于运行。

## 3. 示例内 canonical authority 摘录

### 3.1 requirement/behavior

工具为本地只读 CLI。version 命令必须保留；当前没有清单校验能力。新增行为须给调用方明确 stdout、stderr 和 exit。

### 3.2 design

现有 CLI adapter 负责参数/标准流。可复用的计算不读取 argv，不直接输出。仓库以标准库为依赖边界。

### 3.3 test

生产接口由 unittest 调用；CLI 层另以临时目录和真实 `python -m report` 子进程验证标准流与退出码。文件系统效果以输入内容和目录内容前后比较观察。

### 3.4 Architecture

当前分层为 CLI adapter → 纯计算模块；不增后台进程或持久化 store。实质新增模块可形成真实 task-owned contribution，再由原 Architecture owner 审核和晋升；示例文件本身不执行晋升。

## 4. 其他来源角色

建议 C1：“以后可加缓存提高速度。”它没有当前 consumer 或验收，不是当前要求，不进入方案。

历史 H1：“旧脚本遇到第一个缺失文件就退出。”该事实解释问题，不覆盖当前 R2 的继续检查要求。

原始证据 E1：`[教学替代摘录] item=b status=missing`。这只是示例日志片段，不证明当前工具已实现或测试通过。
