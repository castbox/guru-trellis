# D1 跨仓 DAG 实施与验证计划

## 1. 输入与引用

本批输入为本 Delivery PRD D1-R1..R5、整体 accepted_scope R1..R5/AC1..AC5、design 第3节唯一来源设计处置，以及独立 candidate_assessment 的 no-impact 结论。首次 D1 没有前序交付。实施前读取 design 第4–8节的机制、数据流、兼容、工具/信任边界和验证条件。

必要 canonical：`trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/` 原公开入口与本地合同；`trellis/presets/guru-team/spec/workflow/issue-orchestration.md` 完整共享方法；Sequence package 的消费条件；`docs/{requirements,design,test}/current/issue-orchestration.md` 完整当前单元；Architecture baseline/constitution/change-contract。按照 `.trellis/spec/workflow/clear-technical-writing.md`、`quality-guidelines.md#test-and-validation-value` 和 `skill-package-contract.md#public-skill-io-and-private-state` 执行，不复制其规则。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | Owner、前置、文件与动作 | 完成观察 |
| --- | --- | --- |
| I1 合同实现 | trellis-implement，规划已激活；修改 DAG SKILL/interface/local contract/examples/forward-cases、共享 issue-orchestration 方法及必要 sequence 说明 | 多仓 identity/project/base/initiative/environment 贯穿原输入、调度、heartbeat、child和核证，单仓简写进入同一路径 |
| I2 行为验证载体 | trellis-implement，在 I1 明确消费边界后扩展 DAG tests 的真实 coordinator/child进程载体 | 跨仓同号、依赖、成员与环境各分支有独立事实观察；复用现有进程/MCP支持，源私有、不按自然语言造下一路由 |
| I3 RDT候选与用户说明 | 原 RDT owner 基于实际实现写隔离完整 proposed R/D/T及traceability；实现 owner 更新相关 README与同一 migration说明 | 不直接写shared current，不新增根索引；来源/拟稿/验证边界可查 |
| I4 最小自检及早期反馈 | 实现 owner 自检、敏感内容检查；原 TaskCommit/Publication owners 按早期 Draft profiles提交/发布可审阅候选，按原 router 并行独立反馈及 HEAD验证 | 原事务可恢复，Draft不代替正式Check；反馈修复回同Delivery |
| I5 受管安装同步 | 主会话原 guru-upgrade-tools 从完整匹配候选 source加载，preview→prepare→invoke；同步本 Task worktree dogfood工具/spec/Skill投影，原 current-only apply 前置成立才用普通apply | 保留Task/session/并行内容、exact platforms、peer状态；实际 target-native checks/reapply/drift/mode/sidecar完成；不手工复制受管文件 |
| I6 候选质量与整合 | 独立 Architecture phase2、原 RDT task_impact_sync、原 Check delivery_candidate_check检查完整实现及隔离拟稿；candidate_checked后原 owners执行final_integration | RDT实际晋升并回读，Implementation构造包含所有变化的新 Candidate并begin_check，候选检查不冒充最终通过 |
| I7 最终交付闭环 | 原 Architecture/Check、TaskCommit、独立完整 Branch Review、Delivery Review/Publish/Merge、Completion/Closure/Finish/Cleanup | 对最终实际内容及main目标完成原门禁，Issue与Task分别关闭/归档，不以Delivery合并代替整体完成 |

仅实现源和私有tests由 implement worker写；主会话负责规划、RDT、受管同步、commit及生命周期编排。任何工作者保留其他人的改动，不写共享journal或其他Task。

## 3. 验证入口、输入与预期观察

| ID | 执行入口 | 输入/预期与采用边界 |
| --- | --- | --- |
| V1/V2/V3 | DAG `tests/` 的真实 Codex隔离 runner正常公开Skill入口；具体命令由I2新增scene/help公开后记录 | 多仓同号/跨仓边/各仓base、动议总控与工程、环境可建/不可建/信任/恢复；人工独立读取真实动作和结果，不用fixture自证 |
| V4 | `python3 trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/tests/run_native_orchestration.py --root . --scene dag --output <新外部目录>`，及 `--scene sequence` | 原单仓DAG/Sequence受影响回归；保留首失败/未知发送恢复；按真实trace判行为，外部目录不提交。若新载体已完整覆盖同一路径，采用可验证等价事实并说明，不重复无价值场景 |
| V5a | `python3 -B -m unittest discover -s trellis/skills/guru-team/tests -p test_instruction_only_packages.py`（使用项目managed Python缺依赖时沿原resolver） | 原interface/discovery、源私有tests排除、Codex-only安装、reapply及冲突逻辑；不证明AI调度 |
| V5b | `bash .trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`，同步后 `--mode installed` | canonical/interface与实际投影一致，未改公开exit/schema |
| V5c | `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`，原tools同候选reapply与target-native入口回读 | 无drift/未处置sidecar，mode正确，Task/session和peer不变；不是Release矩阵 |
| V6 | quality-guidelines的内存Python语法检查、`git diff --check`、官方Task validate与当前Delivery query | 语法/文本/身份机器事实；正式语义门禁仍独立执行 |

验证先观察真实行为，再补相关机械分发证据。可采用原隔离进程/MCP与单仓覆盖，但跨仓和环境分支必须新增实测。测试运行失败先判断是否到达声明边界，保留设施失败，不把未触达路径当产品失败或通过。已有证据足够且无新增变化/风险时停止额外测试。

## 4. 停止条件与适用回退点

新增需求、来源冲突、机制/owner变化回原 Clarify/Author/Architecture。缺原生产者或真实工具能力且无支持路径时，只暂停其依赖工作并说明缺口；本项目交付不能用虚构工具能力补齐。测试未覆盖必要分支仍是验收缺口，不把静态parity当替代。

受管同步冲突沿原工具owner恢复同一操作，不重prepare或覆盖用户内容；未知Git/GitHub副作用先回读原事务，不重复操作。无业务数据迁移或生产部署。本地可逆修订使用普通文件编辑，只改本批范围，不reset/revert并行内容。source锁/平台矩阵边界如实报告，不修全局npm/node_modules。

## 5. Delivery Policy（唯一）

`full`。本批承担整体R1–R5及AC1–AC5；无延期功能和后继Delivery责任。独立交付条件是跨仓身份、各仓base/流程/核证、动议成员、环境建立/用户步骤/信任/恢复和旧单仓兼容均有适当层级证据，源码与受管投影一致，RDT已由原owner完成晋升，最终Check/full Review/readiness成立并实际合并main。

剩余整体验收及Issue关闭、Task归档仍由原Completion/Closure/Finish所有；Delivery合并不证明它们完成。真实App生产业务、Fizz动议和完整Release矩阵不在本批accepted scope，不将其记成已验证。

## 6. Docs SSOT Plan（唯一）

`strategy=delta_first`，原writer为 `guru-maintain-requirements-design-test-ssot`。以 `docs/{requirements,design,test}/current/issue-orchestration.md` 的R731/D731/T731为适用现有来源，新增R761/D761/T761的跨仓与环境定义及必要关系，在 `docs/requirements-design-test-contributions/761-cross-repo-issue-dag/` 给出完整proposed目标。保持原稳定能力identity、现有条件和source provenance，不复制未改authority，不写共享根/current索引。

原RDT owner在phase2 task_impact_sync检查完整拟稿与追踪，交原candidate Check；仅candidate_checked后在final_integration回读真实目标、整合实际重叠、晋升并回读。Implementation随后重绑全部正文/关系/说明变化进入最终Architecture/Check与完整committed Review。直接consumer为后续维护/查询和本Delivery最终质量链。

Architecture当前no-impact，未要求贡献或ADR；后续实际实现若改变该事实先回原owner。canonical Skill、共享spec、README/migration由原受管分发同步dogfood，不将源修改冒充已有安装采用。历史贡献保留原观察，新文案分别说明隔离Agent、安装、真实App及Release未验证边界。
