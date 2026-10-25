# 流程合同连续性：验证责任与实际证据

完整策略在 `proposed/docs/test/current/task-delivery-lifecycle.md` 的T663-01..06；与D1设计第8节及V1–V8对应。public wrappers、schema/projection组合、真实AI owner、源码/installed/platform与GitHub事实分别报告。此前Issue扫描是原失败证据，不是当前修复通过。

本文件拥有本项必要长期验收结果。以下区分实际完成的验证与剩余门禁，不保存完整执行日志。

## 包与合同组合

实施 owner 使用匹配 Fork `79a97ed60fe19e8f287eaddfa74722b5250ced35`、CLI/Core `0.7.0-castbox.5` 和受管 Python，实际执行 canonical package 的 `unittest`：Bootstrap `tests/test_contract.py` 4项、Branch Review `tests/test_archived.py` 11项、Architecture `tests/test_promotion.py` 14项、TaskCommit `tests/test_committed_reentry.py` 9项，以及 `tests/test_delivery_contract_graph.py` 4项通过。后者读取当时 registry，检查40个 active packages、177个 structured profiles、212个出口投影及当前 schema 接受的 published example 变体；这些数量是该次快照，不是固定验收阈值。

F1 的原 wrapper 实际拒绝合法 baseline/contribution；runtime 对齐 current closed profiles 后，正常 producer→projection→repair 和原非空/缺失/identity 错误边界通过。F2 从 Interface 正式 example 出发，完成 recorder/checker/invoke 和只读 stop，归档与 PR snapshot 保持。F3/F4 通过实际 Git 与正式 wrappers 检查 before 缺失、当前候选、whole-task/Delivery Bootstrap 维护和原 repair 对照。语义 owner 结果在这些测试中受控，不能作为原生 AI 通过。

F3 存在性读取还实际暴露了中文路径转义和合法 `./` locator 的回归。生产 validator 改用 Git 原始路径并保留原相对路径含义后，当前 Check owner 亲自执行中文/`./` 用例与首次 authority 缺失用例，2项通过；source checker、修改文件语法和差额格式检查通过。此前14项中的其它执行事实只按实际未变依赖采用，不声称重复执行。

原完整 Architecture suite 的固定 eval 清单在 B 中已遗漏三个现存 native cases，本次未改该历史断言。另一次只读断言受隔离 Git 后台 maintenance 影响；仅该测试进程禁用自动 maintenance 后，原断言通过。完整 suite 不计为全绿。最初受管环境缺 pytest，实际改用同受管 Python 的 unittest，没有修改产品依赖。

## 分发与代表安装

普通 source-checkout `apply.sh --repo .` 因既有 legacy archive 前置在写前阻塞。原 `guru-upgrade-tools` 使用完整本地候选及匹配公共维护 API，同步 workflow、packages、managed specs 和平台副本；没有转换本仓历史 Task。最终 source/installed checker、dogfood drift、共享及 Claude/Codex/Cursor 投影、可执行权限和 sidecar 检查通过；installed snapshot 为10148个 managed files，conflict/sidecar/private-test均为0。原 tools 输出仍标记 `formal_fork_source_lock` 未验证，不作为正式发布证明。

唯一 Codex focused clean 样本的原 verifier 在 init 生成的旧格式 bootstrap Task 处返回 `upstream_delivery_migration_required`。保留同一样本后，原 legacy owner 经正式公共转换保留 raw source/PRD，将其转换为空 Task2；随后普通 preset 安装成功，原维护正式返回 `task_resumed`。原 Identity、branch binding、checkout、真实 session Bind 和 target-native current 均已执行。原始一键 verifier 不计为通过。后续仍使用同一样本，原 tools owner 从完整 matching source 执行实际更新，再执行 focused `update --skip-all`、preset reapply、installed checker 与实际 SessionStart/SubagentStart 装载，均成功。该次 installed snapshot 为6422个 managed files、124 commands，conflict/sidecar均为0；54份项目文件在工具采用前后保持字节与 mode。实际 mode、当前 Task/Delivery 和 context 装载已核对；自动 update 的101文件恢复备份完整保留在样本相邻验证目录。此项是受支持维护后安装/更新链通过，不改写原一键 verifier 的失败。

## 实际 Bootstrap 与原生质量链

真实 owner 已读取该安装的 Bootstrap、upstream spec-bootstrap、RDT/Architecture 合同与实际仓库，正式产生 `repair_required`，再按 Interface rename/authoring 进入同一 owner 的 repair。原 standalone mode、continuation、repo、baseline 和 scope 保持。它实际修复14份项目 spec并形成三份 Architecture 候选，如实返回 `baseline_incomplete`；原保留哨兵字节不变。这证明 V2 的实际维护继续。其后原基础维护 owner 实际补齐完整 Architecture/RDT 定义，激活 native-foundation-2、native-constitution-2、native-change-contract-2 与 native-rdt-1，并经原 Bootstrap 返回 completed；基础维护不替代独立质量门禁。

该样本的固定 B 为 `caeb16ab3d6fa3f43b7e62635ea399be4bb67b48`。选定 baseline 为 `docs/architecture/native-bootstrap.md`，另两条为 `docs/architecture/00-foundation/design-constitution.md` 和 `docs/architecture/06-governance/change-contract.md`；三者在 B 中均缺失。原 Task 已经实际 Clarify→Author→scope acceptance→CreateDelivery→Author requirements_ready，Delivery 为 `72de25d4-fdb6-4490-95ac-1babb86d29bb`。该样本随后实际完成独立 candidate assessment、三规划与 Wording、独立 final_plan、Approval/Activation、原 Architecture/RDT phase2、候选 Check 的合法回程、重新 candidate/begin_check 和最终 Check。原生 Check 曾发现样本规范的一条失效导航，返回 implementation_required；原 spec writer 修复后，原 owner 验证闭合并完成当前完整检查，没有将该写作错误纳入主仓产品修复。

原 TaskCommit 实际创建 H=`bba327eea41a233025b7031e4d563c9da17cbc7e`。提交后由当前 Reviewing owner 合法返工并重绑同 B/实际 H，原 Architecture/Check 刷新实际绑定，TaskCommit clean re-entry 返回同一提交，没有空提交。独立 committed Architecture 如实消费 B 的三条 absent_locators，完整 Branch Review 正式返回 passed，公共 full_review 已读回 applicable，predecessor 为该 H 的当前 Check。独立覆盖完整 B..H 的34个文件、三份新 authority、四份 RDT、14份项目 spec、规划/context、matching 工具差额及必要未改 consumers，八份 sentinel 与 raw 来源保持。V7 的原生 owner 链已完成；B 已有 authority 的路径由前述正式 wrapper/Git 对照分别证明，未创建第二个 clean 样本。

主 Task 的候选 Check、原两 owner final integration、最终 Check/TaskCommit/独立 Review、GitHub Delivery 与整体终态由其原公共 Task/Delivery 记录及正式输出拥有；本 Test 不重复保存这些逐阶段状态。完整多平台 Release 矩阵、业务旧安装采用和生产从始至终不由本项证明。
