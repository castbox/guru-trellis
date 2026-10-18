# #239 D1 实施与验证计划

## 1. 输入与引用

读取整体 PRD 第5–7节、本批 PRD 第4–7节、design 第3节唯一来源设计处置与第4–8节方案。完整读取 Issue #239、.trellis/spec/workflow/clear-technical-writing.md、preset/installer.md、preset/upstream-ownership.md、workflow/quality-guidelines.md 的 Test And Validation Value/Validation Scope Ownership、companion-scripts.md 的 Validation、subtraction-first-compatibility.md。Architecture 与 RDT authority 见 design 第1、9节。无前序 Delivery，起点 main@`ed59e851b6c1257bac6316a9571274427e383c93`。

## 2. 有依赖顺序的步骤与文件责任

1. I1，实施 owner 先读当前文件，更新 canonical quality/companion 及 project-local index/installer 的常规语法检查合同，保留原范围和隔离专项例外。
2. I2，实施 owner 修改原 dogfood _tree_files 后缀条件。对 bootstrap_check 产品复制先正常复现，再在原 ignore 补 .pyo；已有正确 selector/collect/digest 保持。不要动上游脚本复制或业务路径。
3. I3，实施 owner 在现有测试目录增加定向行为测试：完整真实安装 verify、过滤工具回归、产品副本、实际文档内存命令。测试执行时禁写普通导入缓存，仅专项临时目录生成字节码。不得改历史归档或为了报告增加 tracked 证明文件。
4. I4，实施 owner 运行 canonical apply 同步安装副本，逐个审查本轮 sidecar，再重复 apply；记录实际文件变化和验证输出给主会话。
5. I5，主会话完成 Docs reconciliation、独立 Phase2 Architecture、formal Check、Task Commit、独立完整 Branch Review、Delivery Review、Publish/Merge、Completion/Closure/Finish/Cleanup。实现 owner 不提交或发布。

## 3. 验证入口、输入与预期观察

V1–V6 的输入、层次、预期和边界由 design 第8节拥有。执行入口：
- 新增定向 unittest 文件，必须调用完整 verify 与原过滤/复制函数；三类字节码来自隔离临时编译；覆盖真实文件删除和变化。
- 实际运行最终文档的内存语法片段；用隔离合法源码、语法错误和顶层副作用样本验证不执行、非零、文件/原因与无写入。
- `test_preset_transaction_installer.py`；现有 ExtensionManifestInstallerTest 的 equivalent_reapply、changed_canonical、raw_apply、python_entrypoints 四个 #430 定向回归；触及 runtime 时运行直接相关模块/包测试。
- 原 source/installed `check-skill-packages.sh`、`check-upstream-ownership.sh --repo . --json`、`check-dogfood-overlay-drift.sh`、`git diff --check`，以及 Bash 语法检查。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`，审查首次同步结果后重复执行。比较实际受管产品变化，检查没有新增 sidecar 或非预期 tracked 变化；不清理既有源码缓存。
验证失败、环境阻塞或跳过如实上报；通过几条命令不能替代完整 Check。没有新增布局，不跑形式 clean 安装；完整多平台、历史版本升级与发布候选矩阵未执行。

## 4. 停止条件与适用回退点

新范围、API/owner/身份算法变化回 Author/Architecture；真实来源冲突回 Clarify。普通测试失败在原职责修复并重跑定向验证。环境缺失只阻塞依赖项，不能记 pass。未知 sidecar 或用户文件冲突保留，交原同步 owner。无数据/部署变更；本地回退仅撤销本任务选定代码，不覆盖并行改动。

## 5. Delivery Policy（唯一）

full。D1 覆盖 R1–R3、AC1–AC5，remaining_work 为空。独立交付条件是完整 verify 对缓存稳定且真实漂移仍失败，实际内存语法命令不落盘且错误可见，受管副本一致与重复 apply 通过。validation boundary 为 V1–V6 定向层，未运行完整历史/发布矩阵。整体 Task 的 Completion owner 仍须核对全部 scope、实际证据和外部边界；PR 合并不自动完成 Task。

## 6. Docs SSOT Plan（唯一）

strategy=no_docs_update_needed，指 RDT 知识版本无需新增。原 RDT owner 已读取本轮差额并正式返回 current .108；该修复不引入领域能力、公开契约或新长期责任。工程规范本身仍在 I1 更新：canonical quality-guidelines/companion-scripts 是常规检查正文，project-local index/installer 只指向它；安装副本由原 preset 机制同步。直接 consumer 为实施者、Check 与 Branch Review。最终 Phase2 前原 RDT owner fresh reconciliation；Architecture .99 无影响由独立 owner 确认，不制造 contribution/ADR/证明报告。保留不可变历史文档。
