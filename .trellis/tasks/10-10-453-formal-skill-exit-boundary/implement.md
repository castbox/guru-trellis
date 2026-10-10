# #453 实施与验证计划

## Entry
本 task 当前处于 planning。只有当前 Wording pass、独立 Architecture baseline_current、正式 Plan Approval approved 且方案展示后的明确接受，才通过 guru-activate-task 进入实现。
本文件不代表实现、测试或阶段已通过；用户授权只存在于当前对话。

## 工作顺序
1. 从当前 registry/interface 重新清点所有 command。读取对应 wrapper、runtime output、schema 与现有 caller，明确 formal invocation 和 intermediate 类别；不生成长期扫描 ledger。
2. 新 commands 1.1 schema 显式描述两个 stdout 合同，迁移所有当前 canonical metadata/fixture。添加一个共享闭合 intermediate receipt schema；dispatcher 依据当前声明包装 stdout。public invoke DTO、helper 内部返回、checkpoint bytes 与现有参数不变。
3. 同步当前 CLI、eval/native authoring、integration test 的 result projection，保留真实 trace。更新 package contract、companion spec、受影响 Skill 和安装 migration 文档；退役旧当前 stdout 读取方式，不保留 fallback。
4. 补客观定向测试：真实 wrapper 的 recorder/checker/atomic executor/recovery output、同 owner result 投影、closed schema、正式/非通过 exit、unique consumer 与 normal stale/re-entry。内部旧能力不丢失；deterministic profile 不增加 review gate。
5. 执行两个真实 native Agent 行为 run：checker-only；record+check 尚未 invoke。每个 run 使用正常完整 review 生成的输出；Agent 在实际声明后自动补合法链。两个 run 的最终出口覆盖正向与 blocked/revision，并由 AI 审查 transcript 与动作。
6. 通过 RDT owner 维护 task-isolated contribution 与 trace；维护 architecture-contribution.md 的 transport before/after、九项 concern 与证据边界，由当前独立 owner 决定 stage 出口及 ADR 必要性。不得擅自写 shared current。
7. 执行 canonical/dogfood 同步、apply/reapply、drift、声明平台 projection、managed hash/mode 与 sidecar 检查。一个代表性 clean install 和一个旧完整安装 migration 使用固定当前 candidate；不跑完整多平台 Release matrix。
8. 全 scope Phase2 真实语义 review、Task Commit、独立完整 origin/main...HEAD Branch Review；如 contribution 晋升引入 diff，重跑受影响 Phase2/commit/Branch Review。
9. current Delivery Review 与 Publication readiness 后单独展示 commit/push/PR 目标边界；Merge、Completion、Closure、Finish、资源处置各遵循对应 owner 与已取得的当前对话授权。caller-owned app worktree 保留，Cleanup 不推断删除授权。

## 验证映射
| Requirement | Design responsibility | Evidence |
| --- | --- | --- |
| R453-01/02 | D453-01 command 分类与 stdout receipt | T453-01 live registry、actual dispatcher、schema 与 owner projection |
| R453-03/04 | D453-02 原 public exit/atomic/type | T453-02 package regressions、formal positive/non-pass consumer、deterministic profile |
| R453-05 | D453-03 direct consumer 与完整安装迁移 | T453-03 CLI/eval caller 集成、旧安装 reapply/update、mixed install 原门禁 |
| R453-06 | D453-04 canonical 与声明平台 | T453-04 package/runtime、apply/reapply、drift、hash/mode、sidecar、representative install |
| R453-07/08 | D453-05 真实声明与接续行为 | T453-05 两个 native transcript 与真实 receipts；AI 语义 grading 独立于 Python |

## 测试价值与最小范围
测试必须触发受支持的实际 entry，观察原缺口与改变后的消费者行为，且能检出错误实现。marker 字符串、fixture pass 或 command exit code 不能证明 Agent 正确报告阶段状态。
按 accepted scope 运行受到输出迁移影响的 package/runtime/consumer 测试，失败先区分当前实现、环境缺失和历史无关项；证据不足保持 unverified。
不扩张为 hostile forgery、并发压力、TOCTOU、fault injection 或完整 Release Gate；native 缺失不得算 pass。
每个被修改的非生成源码文件不超过 3000 行；若触发阈值，先由 AI 审查机械拆分/小解耦，并保持当前职责。

## Docs SSOT 与旧路径退出
PRD 的 Docs SSOT Plan 是本 task 文档策略入口。公共 receipt 规则只有 canonical contract 一个定义源；平台入口仅加载/路由。
受控 callers 在同一交付中删除旧直接读 stdout 字段的当前路径。历史 schema/版本、archive 与 ADR 不作为 legacy runtime consumer，也不回写。
task-isolated RDT contribution 通过 trace 串接 R453/D453/T453；shared authority 晋升由原 owner 单写。
不新增授权文件、reviewer ledger、跨阶段 digest chain、永久 runtime receipt 或完成声明模板。

## 风险与未验证边界
尚未执行实现、客观测试、native 行为回归、安装迁移、Phase2/Branch Review、Publication/Merge/Closure。
receipt envelope 是显式中间 CLI 格式迁移；未同步 caller 将报错，因此完整 unit 的 reapply、实际 consumer 与旧安装验证为必需。
本 task 不声称所有业务仓、native host 或全部平台 Release matrix 通过；旧安装的未覆盖版本、update 路径与平台在最终结果逐项列出。
本 task 仅交付 #453；序列后续 #396/#250/#292 由协调 chat 单独启动。
