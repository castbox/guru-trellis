# 全量 D1 清单校验设计（教学正文）

## 1. 设计目标、需求承接与内容基线

承接 [本批 PRD](delivery-prd.md) S1–S3/R1–R4/AC1–AC5。完整输入实际读取 [source 第1–4节](source.md)，整体责任见 [Task PRD](task-prd.md)。教学 B 是 source 第2节快照，无真实 Git SHA 或 PR 目标；实际 Author 必须经原 content_base projection 分别确定 B/来源、Planning H0 和目标分支。Architecture 为 source 第3.4节 adapter→纯计算边界；示例不伪造候选评估或 final_plan。

## 2. 当前系统、边界与目标差额

首次交付，无前序。cli.py 目前只分发 version。新增 checker.py 和 cli.check 分支；__main__.py 继续只调 main。目标是调用方获得有序 JSON/退出码，原 version 不变。不增加服务、存储、缓存或第三方依赖。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置 | 具体落点 | 理由 | 影响 | 上游处置 |
| --- | --- | --- | --- | --- | --- |
| source §1 D-A：validate_manifest(document, base_dir, is_file) 纯引擎返回 CheckResult/格式异常 | retain | §4 checker 职责、§5 函数及异常接口 | 计算可复用，CLI 负责副作用。 | 新增模块，不改 version。 | 无偏离。 |
| source §1 D-A：adapter 负责 JSON、标准流、exit | retain | §4 cli.py、§6 第1/4步 | 对外协议归入口。 | 新增 check 分支。 | 无偏离。 |
| source §1 D-B：先完整校验、后文件检查；disabled 先分支 | retain | §5 字段验证、§6 第2/3步 | 格式异常不得访问任何文件。 | 验证阶段分离。 | 无偏离。 |
| source §1 D-B：缺失是普通结果、标准库实现 | retain | §5 CheckResult、§6 正常缺失流程、§7 | 保持继续检查和依赖边界。 | 不引第三方异常框架。 | 无偏离。 |

C1 缓存建议和 H1 旧脚本历史不进入本矩阵，它们没有规范性设计角色。

## 4. 模块、职责与设计取舍

checker.py 拥有文档校验、相对路径解析和结果构建；不读取 argv、不输出、不退出、不写文件。cli.py 的 check adapter 读取清单、把 `Path.is_file` 作为 is_file 传入，序列化结果和决定 exit。__main__.py 只调 main，tests 分层观察引擎和真实入口。

选两阶段校验，避免边读边检查让后续格式错误前已经访问文件。选择简单有序列表而非并行队列，直接保留 R2 顺序。注入 is_file 有当前“不访问”验收 consumer，不扩成 provider registry。缓存无当前必要性，不采用。

## 5. 接口与数据

`validate_manifest(document, base_dir, is_file) -> CheckResult`：document 是 JSON 解析后的值；base_dir 是清单父目录；is_file 接收解析后的 Path 返回布尔。该函数先检查 document 为对象、version 的值及类型、entries 为数组，再检查所有 id/path 非空字符串、enabled 为布尔、id 唯一。校验数字版本时不把布尔当整数。字段类型错误抛 ManifestError，包含可读字段/条目原因；此前 is_file 调用数为零。

CheckResult 包含 version=1、results 有序列表、ok；每项含 id 和 status。enabled=false 直接 skipped；enabled=true 用 base_dir/path 调 is_file；true→ok，false→missing_file。ok 是没有 missing_file。空列表返回 ok=true。

CLI `report check <manifest>` → 读取 UTF-8/JSON → 引擎 → stdout JSON。不可读/JSON/ManifestError 映射 stderr 原因、stdout 空、exit 2；正常 CheckResult 的 ok=true→0，false→1。JSON 字段不增加内部路径或异常对象。没有输入写回或报告文件接口。

## 6. 状态、顺序、正常与失败流程

没有持久化状态。单次执行的顺序如下：

1. adapter 读清单并解析 JSON；读取/解析失败直接 stderr+exit 2，不调用引擎。
2. 引擎校验完整结构、每项字段及重复 id；失败抛 ManifestError，零文件访问。disabled 项也参加字段校验。
3. 仅在第2步成功后按序处理条目。先判断 enabled=false 并追加 skipped；否则调用 is_file，追加 ok 或 missing_file。missing_file 不终止循环。
4. 引擎返回结果，adapter 只输出一个 JSON 对象并按 ok 返回 0/1。

这保留 S3 对任何文件检查的阻断，以及 S2 对 disabled 的例外。目录按 is_file=false 得到 missing_file。空清单从第2步直接得到空结果、ok=true。

## 7. 恢复、兼容、迁移与集成

输入错误由调用方修正清单后重新执行，不保存检查进度或自动重试。命令只读，失败没有需要恢复的写入。现有 version 分支原地保留并回归；没有旧 check consumer，无需兼容 reader。没有持久化/接口迁移，没有 DB 或远程发布回滚。全量 D1 同时集成引擎与 CLI，不依赖后续批次；部分替代方案见 slices，不能混入本批历史。

## 8. 验证设计

| V | 要求/AC | 层与入口/输入 | 预期观察与限制 |
| --- | --- | --- | --- |
| V1 | R1/R2/AC1 | 引擎 unittest；base_dir 下普通文件、空 entries | 顺序、相对路径和空结果正确；只证明模块。 |
| V2 | R2/AC2 | 引擎；记录 is_file，禁用项夹在两启用项之间 | 调用列表无 disabled path，输出含 skipped 原位置。 |
| V3 | R2/R3/AC3 | 真实 CLI；缺失/目录/存在项 | 后项仍产出，JSON ok=false、exit 1。 |
| V4 | R1/R3/AC4 | 引擎先合法项后坏项/重复 id；CLI 坏 JSON/不可读及合法结果 | 格式失败零 is_file；stdout 空/具体 stderr/exit 2；正常 JSON 字段与exit一致。 |
| V5 | R4/AC5 | 真实 CLI 前后输入/目录比较，version 回归 | 无写盘，version 原行为保持。 |

入口与数据安排由 implement 第3节承接，尚未执行。没有安装、远程成功或实际 Agent 行为结论。

## 9. Canonical 引用、本轮差额与实际未决项

[source §3.1–3.4](source.md#3-示例内-canonical-authority-摘录) 是示例内 requirement/design/test/Architecture。差额是 check 行为、纯引擎与测试，分层不变。真实项目按原 owners 形成任务独占 RDT/Architecture 差额，最终 Phase 2 前沿原路径审查/晋升；本文不创建共享 authority。没有必要未决项。真实代码与教学快照不一致时返回原事实/阶段 owner，不假定一致。
