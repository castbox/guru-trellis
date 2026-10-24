# 修复流程合同承接断裂：整体需求

## 1. 来源与术语

Direct Source 为 [castbox/guru-trellis#663](https://github.com/castbox/guru-trellis/issues/663)。完整正文的“问题与目标”“F1–F4”“修复范围与约束”“V1–V8”是本 Task 的要求；历轮扫描属于历史证据，不是已完成验收。当前公共 package、registry 与 workflow 定义入口、出口和 owner。`docs/architecture/README.md`、`00-foundation/design-constitution.md`、`03-domains/ownership.md` 和 `06-governance/change-contract.md` 是架构约束。

Producer 是出口生成者，consumer 是该出口的唯一后继。B 是固定 Delivery 内容基点，H 是当前已提交候选；before authority 必须描述 B 的真实状态。

## 2. 背景与问题

当前合法路径有四个断点。F1：Bootstrap repair_required 声明投影携带 exit_id/profile，repair 输入却需要 source_exit/mode/continuation_id。F2：归档审核正式 example 带有当前只读输入不接受的 check_result_id。F3：本 Delivery 首次建立 authority 后，committed Architecture 要求在 B 读取尚不存在的三个文件。F4：final integration 的 Bootstrap 回程投影 stage=phase2，Bootstrap schema 只接受 planning。原失败及对照详见 Direct Source，不能用重试、改 B 或跳过校验解决。

## 3. 目标与非目标

修复四项原始失配，使正常入口、声明投影、正式 consumer 和后继 owner 可连续执行，并扫描当前全流程合同组合。整体责任包含回归、真实 owner 的代表性安装行为、完整分发同步和独立审核。

不承担已在 main 修复的 Finish/Reactivate 问题、业务仓旧安装升级、#802 现场恢复、#649 状态治理、#656 Release 或完整多平台矩阵。不新增通用恢复框架、审批链、持久交接记录、锁、攻击模型或故意伪造测试。

## 4. 真实调用方、场景与流程

| 场景 | 前置与触发 | 行为及可观察结果 |
| --- | --- | --- |
| F1 | 原 Bootstrap owner 判定修复必要并返回 repair_required | 原 caller 薄投影保留 mode、continuation 和必要基线上下文，同 owner repair 能消费并继续基线维护 |
| F2 | caller 依 Interface 正式 example 填入合法 schema2 archive 身份 | recorder/checker/invoke 完成只读审核，合法结果仍进入原 disposition stop |
| F3 | B 无 authority，Planning/Bootstrap 在该 Delivery 建立文件并提交 H | 明确真实 before absence，Phase 2、TaskCommit、committed Architecture 与完整 B..H Review 能承接并实际审核新增文件 |
| F4 | final_integration promotion 返回 baseline_incomplete/bootstrap_foundation | 保留原 Task/DeliveryKey/root 和调用期 continuation，Bootstrap 后回同一次 promotion；维护不授予 promotion 或最终 Check pass |

## 5. 行为要求

R1：修复 F1 的出口、Interface 投影、consumer 输入及 workflow/Skill/reference，明确 producer 字段与 caller 当前上下文的来源。Consumer 不读取 producer 私有结果，不猜造身份，不要求用户拼接未声明字段。

R2：修复 F2 正式输入 example，保持 archive、Completion/Closure、planning、range、PR snapshot 与只读约束；不引入当前 Check、active gate、重开 Task 或业务阶段推进。

R3：Architecture 原 owner 区分 B 已有和本范围首次创建的 authority。缺失事实有明确合同，完整固定范围和当前候选保持；不得用 H 冒充 before、移动 B、跳过原审核或引入通用 freshness 豁免。

R4：闭合 F4 whole-task 与 Delivery 两种 Bootstrap 回程；原 promotion profile/stage/context 保留，stage 必须被正式 maintenance schema 接受，再 fresh 回原 promotion。保持已合法 repair 分支。

R5：扫描实施时 registry/workflow/Interface 的正常前进、返工、恢复、stop 与唯一 consumer，检查公开 profile examples 与独立/aggregate schemas，新增断点仅在正常支持路径证实后纳入原 owner。

R6：canonical 修复通过既有 apply/reapply 同步完整安装包、dogfood 和声明平台。公共 I/O 调整写明兼容或迁移，不能静默改变既有语义。

## 6. 约束与依赖

AI 拥有 scope、充分性、修复判断及 pass/route；脚本只执行确定性投影、校验和记录。保留必填、身份、freshness、普通 missing/profile/continuation mismatch 检查，不无条件放宽 schema 或接受任意额外字段。

使用仓库固定 Fork/受管 Python 与官方 marketplace/preset 机制；不修改上游、全局 npm 或 node_modules。最多一个代表性 clean throwaway。真实 owner 与受控 wrapper 证据分别报告；安装验证不等于完整 Release、业务采用或生产证明。本任务没有业务持久化数据迁移；公共合同兼容由对应 package 负责。

## 7. 可观察验收与验证方式

| AC | 对应要求 | 输入、入口和预期 |
| --- | --- | --- |
| V1 | R1 | 正式 Bootstrap repair_required → 声明薄投影 → same-owner repair，保持原 mode/continuation/context，无字段失配 |
| V2 | R1 | 一个隔离代表性安装由真实 AI owner 消费回程并实际继续基线修复，返回与事实相符的原合法出口；与受控测试分开 |
| V3 | R1–R4 | new/existing/standalone repair 及其它出口继续可用；普通缺失和 mismatch 仍在错误操作前阻塞 |
| V4 | R5 | 当前全图输出投影、profile examples、aggregate schemas 与 stage/before absence 组合检查；列出确认断点及动态分支边界 |
| V5 | R6 | canonical/installed/platform 同步，必要 clean install、reapply/drift、可执行权限及 sidecars 定向检查 |
| V6 | R2 | 从 Interface example 填真实 archive 身份，原 recorder/checker/invoke 返回合法只读结果；原 archive 和 stop 保持 |
| V7 | R3 | B 无 authority 的隔离样本经真实 Planning/Bootstrap、Phase 2、TaskCommit、committed Architecture、完整 Review；另做 B 已有文件对照，保留 B..H |
| V8 | R4 | 正式 final promotion → Bootstrap → 同原 promotion；whole-task/Delivery 及已有 repair 对照，维护不冒充 promoted/最终 Check |

## 8. 实际未决项

没有尚需用户决定的范围问题。具体合同表示、投影与兼容方案由本 Delivery 的 Author 和独立 Architecture owner 完成。原生 owner、完整 Review 与安装验证尚待执行，不能由此前扫描通过替代。
