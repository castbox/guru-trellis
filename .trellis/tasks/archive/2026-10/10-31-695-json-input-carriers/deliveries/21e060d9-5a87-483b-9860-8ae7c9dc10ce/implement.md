# D1：JSON 载体读取与 Bind 双输入实施计划

## 1. 输入与引用

先读整体 Task PRD、本批 PRD、design 第3节唯一来源设计处置和第4–8节。Direct Source 为 live #695；当前公开 Delivery key 和 planning_root 由原 API 定位，不按目录猜选。当前无前序交付，B/H0 为 `8d746ce561c464ca28af4dc91adf085132e4098c`，目标 main。

必要工程合同：`.trellis/spec/workflow/companion-scripts.md` Error Handling、`skill-package-contract.md` Public Skill I/O And Private State、`quality-guidelines.md` Test And Validation Value/Validation Scope Ownership/Python Syntax Check、`subtraction-first-compatibility.md`；分发读 `.trellis/spec/preset/installer.md`、`upstream-ownership.md` 和 `overlay-guidelines.md`。三份规划及所需源条款在实施前完整读取。

Architecture 使用当前独立 candidate_assessment 的原输出，最终仍需 Wording-current final_plan；当前 no-impact 不生成空 Architecture 贡献。RDT 原维护方及其 current-knowledge 合同负责必要知识贡献与最终整合，不能由普通实现直接晋升共享 current。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与 owner | 实际文件、行为及完成观察 |
| --- | --- | --- |
| I1 收敛读取 | 当前方案已接受；shared runtime owner | 修改 trellis/skills/guru-team/runtime/io.py，保留原支持并按 design 第5–6节分类；去掉吞异常后把未读路径当内容的旧分支，已读内容走同一 decoder |
| I2 适配 consumer | I1；各原 package owner | Bind runtime/invoke.py 增加读取前双 - 检查；Publish/Merge/Finish runtime/invoke.py 的已读 stdin profile 预读改走 decoder；其他 shared 调用方继承诊断，不改变其准入或语义 gate |
| I3 错误与调用说明 | I1/I2；原 package/docs owner | 更新实际受影响 commands 参数/help、error catalog 与公开错误 schema 描述；Bind SKILL 和 references 增加完整正常调用、错误表与恢复。canonical companion-scripts、必要 preset/workflow README 和 MIGRATION-695.md 同步；不新增全局CLI协议 |
| I4 行为验证 | I1–I3；原测试责任 | 新增 shared io 有行为价值的单元测试，扩充 Bind 原 runtime/contract 测试；执行原 wrapper 的完整正常输入、双 - 与 zsh 拒绝，命中三个已读consumer及既有入口准入回归。实际结果由原 Check 审查 |
| I5 RDT 隔离候选 | I3/I4；guru-maintain-requirements-design-test-ssot | 完成本节第6节的真实隔离 proposed 定义与追踪；记录已执行层次和未验证边界，不预填通过；共享 current 暂不写 |
| I6 分发与维护 | canonical 已收敛；原 guru-upgrade-tools/preset owner | 展示本 checkout 精确 tools-only 写集后使用原维护入口，同步 runtime/package/spec/声明投影并保留 Task/session；实际调用 apply、drift、source/installed 和 sidecar 检查，失败沿原 owner 恢复 |
| I7 原质量链 | 完整候选；原 Architecture/Check/RDT owners | 独立 Architecture phase2、完整 candidate Check；原 RDT final_integration 写回已审 current；重绑实际 after candidate 并执行 final Architecture/Check、TaskCommit、完整独立 Branch Review、readiness，再走原 Delivery/Completion/Closure/Finish/资源流程 |

无新增临时限制或后继切片。必要原文件若超过3000行，按既有规范审查机械拆分；不借此重构无关模块。所有产品写入只在本 Task checkout，保留并行内容。

## 3. 验证入口、输入与预期观察

- V1（design V1、AC1/2）：通过已有 managed Python 运行 `PYTHONPATH=trellis/skills/guru-team .trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/runtime/tests -p test_io.py`。该新增测试只验证真实读取/解码行为、错误字段/status与不泄露原文；合法长 inline、文件名优先级、原 symlink 支持不能退化。正常读取失败用可控的单元依赖模拟，不扩张 fault matrix。
- V2（design V2、AC2/3）：通过相同 managed Python 与 PYTHONPATH，运行 `-m unittest discover -s trellis/skills/guru-team/packages/guru-bind-task-session/tests`，并用本 checkout 安装后的原 `scripts/invoke.sh` 执行文档完整双输入、双 - 与 zsh `<(...)`。前者保留真实 Task/Delivery，后两者必须在 schema/identity 写入前给预期分类；不要把 `{}` 的 schema failure 当完整合法调用成功。
- V3（design V3、AC1/4）：对 Publish/Merge/Finish 已读正文预读和 qualifiers/envelope-only 的受影响原测试运行定向入口。实施时按实际 test selector 选择能观察准入/语法/type而不触发 GitHub 写入的用例；没有新 public I/O、不改变其业务，则不重跑其完整远端生命周期。通过原包结构校验验证 commands/error/schema 声明，不按相似字符串改所有 CLI。
- V4（design V4、AC4）：原 `check-skill-packages.sh` source/installed 模式、原 wrapper `--help` 与错误 schema 校验；原维护后执行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`、`check-dogfood-overlay-drift.sh` 和递归 `.new/.bak` 检查。按真实输出区分 plain apply 被旧数据 preflight 阻塞与 tools-only 成功；不手改 manifest/hash 或清理无关 sidecar。
- V5（design V5、全部AC）：执行 quality-guidelines 的 in-memory Guru Python syntax、`python3 -m json.tool trellis/index.json`、声明 Bash syntax、官方 `task.py validate`、`git diff --check`；进入原完整 Check 与独立 Review。测试使用真实可用依赖；缺失为 SKIP/阻塞，不安装替代私有 runtime 绕过门禁。

本次不新增专项回放、A/B、native eval、固定案例数量、耗时统计、额外安装或多平台矩阵，不发布 tag/Release。源码、单元、安装投影、实际 wrapper 与业务现场结论分开报告；本 Task 不承担业务 #961 的现场修复验证。

## 4. 停止条件与适用回退点

来源/范围变化回原 Clarify；机制或消费者边界扩大回原 Author/Architecture 与 qualification。普通实现缺陷在原实现/Check 修复。无效/stale Task、Delivery 或 session 沿原 Identity/Ensure/Bind/Selection，不创建替代对象。工具维护失败只使用同一原 operation 的恢复；未知 sidecar/用户修改停止对应写入。

本批没有 DB/身份数据迁移、生产写入或新持久化，所以没有新的数据回滚协议。实现回退按实际 diff 限于本次文件；不得 reset/revert 无关改动。commit、push/PR、merge、Issue closure、Finish 和 Cleanup 仍各自展示精确目标并遵循当前边界；本计划接受不授权这些独立动作。

## 5. Delivery Policy（唯一）

选择 `full`。本批 scope 为整体 R1–R6/AC1–AC4，交付 shared 读取与真实 consumer 适配、Bind、错误/help/正常调用、必要分发与 RDT 当前定义。没有推迟到 D2 的本项实现，也不启动后项。

独立可交付条件：全部本项行为在原入口满足，合法输入与原 gate不退化，错误与分发一致，原质量链完成。剩余责任为尚未执行的实现/验证以及原 Whole-Task Completion/Closure/Finish，仍归本 Task 的相应 owner；“无后续切片”不代表已完成。Delivery 合并只建立该切片事实，整体 Completion 仍核对所有 accepted scope 与实际未验证项。

## 6. Docs SSOT Plan（唯一）

选择 `delta_first`。原 writer 为 `guru-maintain-requirements-design-test-ssot`；完整隔离贡献根为 `docs/requirements-design-test-contributions/695-json-input-carriers/`。本轮新增独立的 JSON 输入载体完整能力单元：R/D/T proposed targets 分别对应 `docs/requirements/current/json-input-carriers.md`、`docs/design/current/json-input-carriers.md`、`docs/test/current/json-input-carriers.md`；必要三层 current/README.md 导航仅增加 locator/关系。保留原 `guru-trellis-rdt` identity，不递增全局版本，不修改无关历史。

贡献包含原规范要求的 manifest、requirements/design/test/traceability 与真实 proposed target 内容，按当前 authority 和原 R630/D630/T630 的仍有效输入兼容关系承接。R695/BEH695 对应读取、载体、Bind与错误；D695/CON695 对应 shared decoder、原 parameter owner 与分发；T695 对应 design 第8节的可观察行为。公共 reusable 输入合同本体由 canonical companion-scripts 与 Bind package 的具体调用文档拥有，RDT 当前单元说明能力与关系，不复制整份公共 schema。

直接 consumer：当前实现和 Check 读取完整隔离定义；原 candidate Check 完成后，唯一 RDT final_integration owner 比较真实 target，写入并读回完整 current 定义及必要导航。随后 implementation 重绑实际 after candidate，最终 Architecture/Check、commit 和完整独立 Review 覆盖所有写入。未晋升 proposal 不声称 current。

Architecture 独立判定无影响，不创建空 contribution、ADR 或改共享 Architecture 导航。若真实实现改变了该判断，回原 owner刷新而不是沿用旧结论。当前定义只记录实际观察截止及未验证边界，不追写自身最终HEAD或归档结果；后续正式结果由原 Delivery/Completion/Closure/Finish 提供。
