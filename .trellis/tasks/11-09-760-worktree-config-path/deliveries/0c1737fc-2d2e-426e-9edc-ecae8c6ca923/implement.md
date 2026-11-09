# #760 D1 实施与验证计划

## 1. 输入与引用

读取整体 Task prd.md、同目录 PRD、design 第3节唯一来源处置及第4—8节接口/流程/验证。固定 B 为 8c158381b5bdb61fd961cbb89e23c2d1f659c9aa。适用 Architecture 与 RDT 定位见 design 第1、9节。实施前读取 package/layer specs、clear-technical-writing、companion-scripts、skill-package-contract、subtraction-first-compatibility 与 Test And Validation Value。

## 2. 有依赖顺序的步骤与文件责任

- I1：实现共享位置事实模块及必要 inventory，接入 environment 和正式 configured 新建前核对；同步 schema/commands/errors。只改 canonical。
- I2：修订 create-task、task-free 原 Skills 及配置说明、README/MIGRATION-760。明确配置生成与真实显式位置，task-free 保持普通 Git。与 I1 接口一致。
- I3：补 V1—V3 的真实 Git 回归，复用原采用/恢复证据；运行命中 package/runtime 检查。
- I4：原 RDT/Architecture owners 准备隔离完整 proposed，独立 phase2 和 candidate Check 审完整实现及拟写。
- I5：原 owners final_integration 晋升并读回；原 tools-only owner 同步本 checkout 受管投影并检查 drift/sidecar。重新构造实际 candidate，执行最终 Architecture/Check、TaskCommit、完整 committed Review、Delivery Review/发布/合并。
- I6：原 Completion 按整体范围审核，Closure 处理 #760，Finish 归档 bookkeeping 并验证，Cleanup 只处理本任务资源。

## 3. 验证入口、输入与预期观察

V1—V3 的行为层和独立断言由 design 第8节定义。命中测试位于 create-task/tests、select-workflow-mode/tests、runtime/task_lifecycle/tests 或位置事实模块的原测试目录；通过受管 Python 与明确固定 upstream scripts 运行。外部 GitHub facts 在 fixture 边界隔离，Git 创建真实执行。

V4 使用 source/installed package validators、check-dogfood-overlay-drift.sh、受影响 Python 内存compile、JSON/Bash语法与 git diff --check。投影通过完整 matching source 的 guru-upgrade-tools，而非手抄受管文件。未知 sidecar 沿原 owner 处理。

Test 正文记录实际命令、结果和边界，不以测试数量替代行为证明。不运行完整多平台 Throwaway 或 Release 矩阵，不调用业务 #1232 或 Codex 自动清理。

## 4. 停止条件与适用回退点

身份或真实来源冲突回原 owner；新需求回 Clarify；机制变化回 Author/Architecture。验证失败先判归因并修实际差额，不能放宽断言。设施反复失败时改用足够的最小观察并保留未证明项。未解决验收缺口不得 pass。

受管同步使用原 frozen plan/recovery，保留 Task/session、用户配置和 peer；不以 reset/revert 覆盖并行内容。无数据格式迁移或生产部署，不建立新的回滚协议。证据足够后停止重复验证，继续交付。

## 5. Delivery Policy（唯一）

full：D1 覆盖 #760 全部行为及 AC1—AC4，没有延期实现责任。完成条件为两个入口实际消费配置、合法位置兼容、定向行为验证和分发一致性成立，随后通过正式完整质量链并合并 main。Delivery 合并不代替 Task Completion；原 Completion/Closure/Finish 保留整体闭环责任。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原 RDT owner 在本任务隔离贡献中修改完整 runtime-location R/D/T 单元；原 Architecture owner 在隔离贡献中展开 ARCH-RUNTIME-LOCATION 的新建路径事实与原执行边界。直接 consumer 是本批实现、Check、Review 和后续读审。配置、Skills、MIGRATION、README 是相同交付的可执行使用说明。

candidate Check 之后、最终 Phase2 之前由原 maintenance owners reconciliation/final_integration 晋升。只改真实受影响完整单元，保留原稳定 identity，不向共享根或索引登记。历史 #212/#718、ADR 原始观察保持；新的 Test 事实限定本候选和本地验证层。完整安装/升级/Release矩阵、业务采用和Codex清理行为未覆盖。
