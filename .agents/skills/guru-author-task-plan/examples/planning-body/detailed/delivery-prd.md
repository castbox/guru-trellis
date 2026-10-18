# 全量 D1 清单校验需求（教学正文）

## 1. 整体来源与术语

整体要求见 [Task PRD 第1–8节](task-prd.md)，完整输入和角色见 [source 第1–4节](source.md)。本示例 full D1 覆盖整体 R1–R4/AC1–AC5，不构造真实 accepted_scope 或 DeliveryKey。术语沿 Task 第1节，实施/审核实际加载完整相关条件。

## 2. 整体与本批目标、非目标

整体解决 CI 无法区分坏清单和缺文件的问题。本批一次交付纯引擎和 CLI adapter 的独立可用命令。排除缓存、网络、修复、内容校验、写报告及文本模式；没有另留后续功能。

## 3. 本批起点、前序结果、依赖与剩余责任

首次交付，尚无前序。起点是 source 第2节只有 version 的教学快照。本批依赖现有 Python CLI 和 unittest。所有行为与适用验证都由 D1 承担；未分配后续切片不表示验收已完成。输出的命令和证据支持整体 Completion，原 Check/Review/Completion 尚需分别判断。

## 4. 本批调用方、场景与流程

| 场景 | 调用方/前置 | 触发 | 行为 | 可观察结果 |
| --- | --- | --- | --- | --- |
| S1 | CI，合法或空清单 | report check | 读取、完整校验、按序检查 | JSON 顺序稳定；无缺失 exit 0。 |
| S2 | 操作员，合法清单含 disabled/缺失/目录 | report check | disabled 不访问；其余逐项检查，缺失后继续 | skipped/missing_file，ok=false/exit 1。 |
| S3 | CI，不可读/格式错误 | report check | 只报告输入原因，不检查文件 | stdout 空、stderr 原因、exit 2。 |

先完成整个文档的字段与重复 id 校验，再进入 S1/S2 文件判断。

## 5. 完整行为、条件与约束

R1：输入为 UTF-8 JSON，version=1，entries 数组；每项非空 id/path 和布尔 enabled，全局 id 唯一。相对 path 以清单目录解析；错误时零文件检查。

R2：按输入顺序处理合法 entries。启用项存在普通文件则 ok；不存在或为目录则 missing_file，并继续后项。禁用项返回 skipped，不访问 path；仍须满足 R1 字段。空数组合法。

R3：正常 stdout 输出一个 JSON 对象，version=1、results 数组每项只有 id/status、ok 布尔；status 取 ok/missing_file/skipped。无 missing_file（含空数组、全 skipped）则 ok=true/exit 0；否则 ok=false/exit 1。输入不可读、JSON 或字段错误时 stdout 空、stderr 具体原因/exit 2。

R4：不写盘、不修改输入，保留 version。D-A/D-B 的纯引擎、注入检查函数、adapter 分流和标准库要求落在 [design 第3节](delivery-design.md#3-来源设计处置唯一)，本节不另建矩阵。

## 6. 本批验收、验证方式与未决项

| AC | 对应场景/要求 | 本批入口与输入 | 预期观察 |
| --- | --- | --- | --- |
| AC1 | S1/R1/R2 | 引擎和真实 CLI；合法/空、相对路径 | 结果完整、顺序正确、exit 0。 |
| AC2 | S2/R2 | is_file 调用记录；混合 disabled/启用 | 禁用不访问而占据原结果位置。 |
| AC3 | S2/R2/R3 | 缺失、目录、后续文件 | 两个 missing_file 后仍产出后项，exit 1。 |
| AC4 | S3/R1/R3 | 坏 JSON/字段/重复 id/不可读；正常输出 | 输入错误不检查文件且 stdout 空/exit 2；正常 JSON 字段、ok 与退出码匹配。 |
| AC5 | S1–S3/R4 | CLI 运行前后目录/字节比较和 version | 无写入，version 不回归。 |

没有必要未决产品问题；技术细化交 Author/Architecture。未执行的验证不填通过。没有后续批次替本批承担缺口。

## 7. Canonical 引用与本轮差额

实际加载 [source 第3节](source.md#3-示例内-canonical-authority-摘录)：requirement 增加只读 check；design 在既有 adapter 下新增纯引擎；test 增加引擎和真实 CLI 验证；Architecture 保留分层且增加当前模块职责。这里是教学引用，真实 repo 按原 RDT/Architecture contribution/promotion 处理，不由模板写共享导航。
