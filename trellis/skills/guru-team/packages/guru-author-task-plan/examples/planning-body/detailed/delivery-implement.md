# 全量 D1 清单校验实施与验证（教学正文）

## 1. 输入与引用

先实际读 [Task PRD](task-prd.md)、[本批 PRD](delivery-prd.md)、[design 第3–8节](delivery-design.md#3-来源设计处置唯一)、[source 全文](source.md)。design 第3节是唯一来源设计处置，本文件不复制。教学起点只有 version，无前序交付。真实实现还须读取当前 repo 规格、原 Architecture 结论及原身份范围，不能运行示例 B 代替真实 projection。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 依赖 | 文件/责任 | 行为与完成观察 |
| --- | --- | --- | --- |
| I1 | 输入和候选评估可用 | checker.py；原 Author/实施 | 写完整格式阶段、ManifestError、CheckResult、disabled 分支和有序检查；返回值及零访问边界可审。 |
| I2 | I1 | tests/test_checker.py；实施 | 验证合法/空/相对路径、disabled、缺失继续、后续坏字段/重复 id，覆盖 V1/V2/V4。 |
| I3 | I1/I2 | cli.py、tests/test_cli.py；实施 | 增 check adapter，读 JSON、标准流/exit 映射；真实子进程覆盖 V3/V4/V5，version 保持。 |
| I4 | I2/I3 的实际结果 | 原 RDT/Architecture owners | 形成真实文档差额并按原合同审查/晋升，再由原 Check 审完整候选。 |

不改 __main__.py 的入口职责，不把技术细化丢给产品用户。没有另分配的后续切片。

## 3. 验证入口、输入与预期观察

在示例仓库中计划运行 `python -m unittest discover -s tests`。实际路径和命令必须先由当前 repo 核对；本目录没有这些生产文件，也没有执行该命令。

- V1：test_checker 调引擎，使用临时目录中的文件和空 entries；观察 base_dir、结果顺序与 ok=true。
- V2：记录 is_file 调用，enabled true/false/true 混合；观察中项无调用，三项结果有序。
- V3：test_cli 以临时清单调用真实 `python -m report check <manifest>`，含缺失、目录和后续普通文件；观察完整 JSON、ok=false、exit 1。
- V4：引擎收到先合法项后坏字段/重复 id，观察零 is_file；真实 CLI 收到不可读、坏 JSON/字段，观察 stdout 空、stderr 原因、exit 2。合法 JSON 另核对只有 R3 字段及 0/1 映射。
- V5：比较 CLI 前后输入字节和目录条目；无新增/修改。运行原 version 用例，观察原 stdout/exit。

V1–V5 对应 design 第8节和 AC1–AC5。模块结果不能代替 CLI 集成；没有远程服务或完整 Release 矩阵责任。当前均未运行。

## 4. 停止条件与适用回退点

完整来源/候选依据不可读时停对应步骤，由原 owner 恢复。格式/顺序/disabled 任一验证失败，先修复当前机制并重跑相关验证；发现需求变化回 Clarify，机制变化回原候选评估。只修改本批文件中的错误，保留并行改动。没有持久化写入或服务部署，无 DB/发布回滚协议。Git/GitHub 操作仍需各自原边界，示例没有授权任何副作用。

## 5. Delivery Policy（唯一）

选择 full。本批覆盖 R1–R4、AC1–AC5 的引擎与 CLI，没有计划延期的剩余切片。完成需实现、适用实际验证和原审核；未执行验收仍是缺口。Delivery 合并不建立 Task Completion，由原 Completion 核对整体责任。

## 6. Docs SSOT Plan（唯一）

选择 delta_first。原 RDT writer 基于 [source §3](source.md#3-示例内-canonical-authority-摘录) 的 requirement/design/test 形成 check 行为、引擎分层和唯一测试差额，直接 consumer 为原 reconciliation/promotion 与 Check/Review。原 Author 写真实 Architecture contribution，原 Architecture owner 审查晋升。真实差额在最终 Phase 2 前完成 reconciliation/promotion。模板填充不创建空贡献或改共享导航；教学文件不代表这些动作已发生。
