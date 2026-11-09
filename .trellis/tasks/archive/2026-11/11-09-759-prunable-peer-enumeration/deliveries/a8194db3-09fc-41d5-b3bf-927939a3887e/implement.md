# tools-only 失效 prunable peer 实施计划

## 1. 输入与引用

- 整体范围：Task 根 `prd.md` REQ-01 至 REQ-04、AC-01 至 AC-05。
- 当前切片：本 Delivery `prd.md` REQ-01 至 REQ-05、AC-01 至 AC-05；唯一技术方案见本 Delivery `design.md` 第 3 节。本设计已审内容属于现有 Author Planning，不是 Architecture accepted authority。
- 输入代码：`tools_owner.py` 中 `peers()`、`isolated_layout()`、`peer_pointers()`；现有 package tests 用于保持契约覆盖。
- Architecture：调用本 Delivery 已返回的 `baseline_current/no_architecture_impact`，其结论只适用于当前 pre-write 机制候选；没有共享 Architecture write 或 ADR。
- 代码基线 B：`main@8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`；目标分支 `main`。尚无前序 Delivery。

## 2. 有依赖顺序的步骤与文件责任

1. **S1 建立回归夹具**：在 `test_contract.py` 增加 porcelain worktree 记录与临时 peer 目录 helper；只在系统临时目录创建 fixture。为 stale prunable `.git` 缺失、normal peer、prunable `.git` 存在和 non-prunable `.git` 缺失提供相互独立的输入。观察不执行 prune、marker 与目录保留。
2. **S2 扩展 peer 枚举**：修改 `tools_owner.py::peers()` 按 worktree 记录保留 `prunable`；只过滤 `prunable` 且 `os.path.lexists(path / '.git')` 为 false 的注册。其它注册继续返回原 path 类型并进入当前 consumers。
3. **S3 验证 peer consumer**：用 `peer_pointers()` 驱动真实 helper，断言 stale peer 未调用 `rev-parse`，其它 peers 仍调用，non-prunable 损坏 peer 仍报错。若测试结果暴露解析误差，修复 S2 并重新执行受影响验证。
4. **S4 完成 package 验证**：先运行 `test_contract.py` 的定向单元，再运行 `guru-upgrade-tools/tests` 全部可执行 package tests。保留原有 skip/环境限制并单独报告，不把 skip 计为通过。
5. **S5 自检变更边界**：审查代码与完整 diff，确认只改 tools owner 与测试/Task Delivery planning；确认没有 prune 命令、旧 checkpoint、残留业务路径、Task/session schema、binding 或共享 Architecture 文档改动。

## 3. 验证入口、输入与预期观察

- V-01 / AC-01：定向运行新增 stale prunable case；使用 Git porcelain 的 `prunable` 记录和没有 `.git` 路径项的独立 checkout 目录。预期 `peer_pointers()` 不对该路径执行 `rev-parse`，其 residual marker bytes 和目录仍存在。
- V-02 / AC-02、AC-04：定向运行正常 peer 与有 `.git` 的 prunable peer case。预期两者都执行原 `rev-parse` 和适用 runtime selection 检查。
- V-03 / AC-03：定向运行 `.git` 缺失但未标 `prunable` 的 case。预期仍执行 `rev-parse` 并传播原失败。
- V-04 / AC-05：运行新增测试的 fixture 断言并确认没有 prune 调用、没有残留目录写入；通过 `git diff --` 检查源码改动不涉及旧 checkpoint。
- V-05 / AC-01 至 AC-05：从仓库根运行 `python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-upgrade-tools/tests`。预期所有适用 package tests 通过；`test_native_install.py` 中的 opt-in tests 若缺少原生 fixture/候选，则按测试定义记录为 skip，不当作通过。

验证只证明此 Guru source package 的代码路径与回归用例。没有目标业务安装、source_locked preview/prepare/invoke 或真实环境 peer 的执行计划；完成源码修复后，原升级 owner 会以匹配的完整来源重新 prepare 并验证安装。运行命令时若依赖不可用，报告具体环境缺口并保留可执行的定向结果。

## 4. 停止条件与适用回退点

- porcelain 记录解析、`.git` 路径判断或某个 peer 状态与 Issue 条件不一致时，停在 Author/Clarify 的原责任，不扩大可忽略注册集合。
- 新增回归若不能到达被测 `peers()`/`peer_pointers()`，先修正测试入口；不得以单纯检查 fixture 字段宣称函数覆盖。
- 定向测试或 package test 失败时，定位真实失败并保持未通过；不清理 peer 注册或目录来让测试成功。
- 本改动不迁移数据、不写旧 checkpoint、不执行远端操作，故无数据回滚步骤。若误写了测试临时目录，在测试退出时由临时目录生命周期处理；业务/Task 路径不纳入清理。
- 验证充分后停止重复执行相同输入。若当前源码或输入身份改变，重新读取对应来源并重跑受影响的原验证。

## 5. Delivery Policy（唯一）

本 Delivery 为 `full`：它覆盖唯一 accepted Task scope 的全部 REQ 与 AC。其最终完成条件是 narrow peer filter 与四类对照回归符合 Task PRD，且 `guru-upgrade-tools` package tests 的实际结果均如实记录。源码测试通过只支持源码行为；它并不意味着目标安装已采用，也不单独完成 Task Completion 或 Issue closure。

## 6. Docs SSOT Plan（唯一）

策略为 `no_docs_update_needed`。本修复不改变受支持 peer lifecycle、tools-only 公共接口或既有架构责任；R687-02、R718-06 与 D687-02 已覆盖保留合法 peers、Task/session 和原 tools-only owner。AC-01 的窄失效注册条件属于本 Task 的实现修复，不需新建共享 Requirements/Design/Test 单元、Architecture contribution、ADR 或导航条目。若实施中发现共享 authority 需要更改，回原 RDT/Architecture owners 评估，不在此实施计划内直接改共享文档。
