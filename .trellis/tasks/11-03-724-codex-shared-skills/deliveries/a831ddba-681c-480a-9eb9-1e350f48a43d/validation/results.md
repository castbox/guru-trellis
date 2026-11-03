# D1 验证结果

本记录供当前 Check、完整 Review 和整体 Completion 消费。对象为 main 基线 42ffd32d70be3859a4493e084464738473c45dd6 上的本 D1 完整候选。源码、实际安装、native 调用与正式发布分别判断。

## 定向实现与恢复

实现 Agent 执行当前 projection/inventory/selection、installer、upgrade-tools 和 upgrade-installation 定向测试。最终 8 项迁移测试全部通过，覆盖旧 writer 正常产生 provenance、目标完整后退出、两端修改/未知内容保留、目标冲突及正常重试、Codex 选择增减、staged activation、已缺失文件派生空目录与未知空目录诊断。16 项完整事务测试通过；11 项平台 inventory、4 项 dogfood、4 项专属包测试通过。

维护包 16 项测试中 11 项通过、5 项因 opt-in 实际环境 fixture 未提供而 skip；完整升级包 78 项中 57 项通过、21 项环境依赖 skip。新增同操作 recovery 定向测试通过。skip 不记为执行通过，本批另有下述真实原维护入口验证。

首次最终 staging 复验曾有 2 项失败：旧文件已删除且 validator 通过，但父目录提前退出后残留空祖先。修复为沿具体 receipt 路径继续清理已消失父目录的祖先；未知目录不递归删除。5 项目录回归及最终 8 项迁移均通过。首次失败记录保留，不能用最后成功掩盖其原因。

主 installer 机械抽取 public-file 投影职责，三个提取函数 AST 与原实现相同。最终主文件 2916 行，所有 touched 非生成代码不超过 3000 行。独立质量 Agent 检查 426 个 Guru Python 文件的内存语法、跨层 owner/消费者及 diff hygiene；同步后 bytecode hygiene 4/4 通过。

## 实际安装与工具维护

使用 source lock 对应 Fork 17015f987166f4106034f115d23212446f16d536 的真实 CLI/Core 0.7.0-castbox.6 初始化两个隔离样本，workflow provider 固定 main 基线。唯一当前候选 clean 样本经完整 preset 的 codex 选择安装成功；同一样本用最终源码 reapply，installed/activation validator 均 passed，无 .new/.bak、旧 Guru 发现副本或 private tests。

另一个样本先由基线的真实旧 preset 安装，形成原 manifest 和旧副本，再由当前 source-owned guru-upgrade-tools 的 preview → prepare → invoke 正式升级。实际返回 tools_upgraded，目标 exact selection 保持 codex；旧 Guru 目录为零，专属 metadata 到共享根，installed validator passed、128 commands、0 conflict/sidecar/private tests。未手造前驱 manifest/hash。

当前 Task checkout 同样沿原工具 owner 更新，实际返回 tools_upgraded。目标选择保持 claude/codex/cursor；1928 项旧投影文件退出，共享专属 metadata 完整，Claude/Cursor 根保持。目标自身 resolver 可运行；get_context continuation 和当前 Delivery 查询可读，Task、Planning、session 和其它 checkout 不在工具写集。原 owner 的 peer-pointer 校验通过。.codex 的 config、agents、hooks 和 prompts 保留。

工作区 installed validator passed，128 commands、0 conflict/sidecar/private tests；check-dogfood-overlay-drift.sh 通过，workflow、selected platform 与 managed spec 均与 canonical 一致。Task Delivery validate 通过。

## 真实 Codex native 调用

宿主 codex-cli 0.162.1，使用官方 repo Skill scanner 的同机制代表组 G1。在上述 clean 样本中，两个被测 Skill 均无 .codex/skills 旧副本。CLI 收到的 prompt 只有 Skill 名和实际只读/dry-run任务，没有预装 Skill 正文或期望出口。原生 JSONL trace 记录模型主动打开以下共享包，并执行原公开入口。

- 公共包：.agents/skills/guru-sync-base/SKILL.md → .agents/skills/guru-sync-base/scripts/invoke.sh --invocation -。实际 public input 为 standalone / repo_change / operation=read / base_ref=refs/heads/main，返回 baseline_ready、进程 exit 0；只解析本地样本 main，未调用下游。
- 专属包：.agents/skills/guru-orchestrate-issue-sequence/SKILL.md，原显式 dry-run/preflight，返回 dry_run_blocked。实际缺 native saved-project/chat/message/wait_threads/heartbeat 工具，且样本未提交安装文件、无 main tracking；这些是本次真实前置诊断。没有启动 child、heartbeat、后台任务或 GitHub 写入。此结果证明发现并到达原门禁，不证明业务编排成功。

公共包最初在 CLI read-only filesystem sandbox 下遇 runtime_dependency_missing，未产生 typed exit。随后以同一只读 prompt 开放本机 runtime 文件访问，真实原公开调用才返回 baseline_ready。两次原始 trace 均保留；不能把第一次记为通过。

官方当前 Skills 文档声明桌面/CLI/IDE 的 repo .agents/skills 发现合同，作为分组依据。此次仅实际执行 CLI0.162.1，不声称桌面 UI、其它客户端独立执行或所有历史/未来版本通过。

## 证据边界

上述原始命令日志和 native trace 为本次本机验证输入；本记录保留后续 consumer 所需结论及真实失败归因，不复制完整审查过程或原生对话。Task/Git 与正式公共 Check/Review/Delivery 结果仍由各原 owner 提供，本文不预填其通过。

两次工具维护均为 local_candidate，返回 formal_fork_source_lock 未验证。未执行完整多平台 Throwaway/Release Gate、正式版本发布、其它客户端 UI、业务采用或生产效果验证；这些不属于 #724 的本批验收。本记录形成于候选 Check 前；知识晋升结果由后续原 final_integration 公共输出和实际current文件提供。native-observations.json保留本次真实trace的有界命令/出口摘录；完整原始记录不被改写。
