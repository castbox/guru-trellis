# #813 Task Creation 固定审核来源迁移

## 当前合同与旧资产

本迁移只改变原 `guru-create-task` 的当前输入及直接消费者。正式 Task、Delivery、
C4/C5、session 和已有输出/typed exits 保持原职责。Markdown owner 选择来源、
范围与路由；脚本只校验 Git 对象和原身份关系。

| 角色 | 原发布资产（保留原路径、id、字节） | 当前选定资产 |
| --- | --- | --- |
| 共享 Creation | `contracts/task-lifecycle/task-creation-input.schema.json` / `guru-task-creation-input-2.0` | `task-creation-input-3.0.schema.json` / `guru-task-creation-input-3.0` |
| Delivery profile | `schemas/public-delivery-task-creation-input.schema.json` / `guru-create-task-input-delivery-task-creation-1.0` | `public-delivery-task-creation-input-2.0.schema.json` / `guru-create-task-input-delivery-task-creation-2.0` |
| Aggregate | `schemas/public-input.schema.json` / `guru-create-task-input-delivery-1.0` | `public-input-2.0.schema.json` / `guru-create-task-input-delivery-2.0` |

上述路径分别相对共享 Skill 根或原 Creation package。旧 schema 仅供固定历史输入验证，
不进入当前 executor。当前 Interface、commands、公开示例和 runtime 同时选择新版。
新旧闭合输入不能互换，不设置 current 旧 parser、kind 推断或 fallback。

## 原 owner 的薄投影

保留 TaskId、TaskRef、source_profile、reviewed_source、accepted_scope_identity、
delivery_target 和 selected_base_ref。当前输入删除 reviewed_base_head，新增必填
reviewed_base_source，其闭合字段为 kind、selected_ref、commit。

- 实际 `ready.transition.base.kind=git_object`：逐项复制 kind、selected_ref、commit。
  selected_ref 只定位所采用来源，不重新解析；精确 commit 必须在同仓可读且确为 commit，
  并等于 acquisition.decision_head。本地同名分支、primary clean 不决定该对象 freshness。
- 实际同步来源：kind 为 synced_branch；selected_ref 是原 selected_base 的标准化 branch，
  commit 复制实际 decision_head。新建前来源 branch 与 selected_base_ref 一致，本地 HEAD
  与 commit 相等；原 Sync 的同步事实不能由 read 结果或邻近字段补造。
- selected_base_ref 独立选择 Task 基线 branch，供官方 task.py --base-branch 及非基线/
  非交付分支资格。delivery_target 继续表示未来交付仓库/分支。read 不替 owner 选分支。

固定对象不存在或非 commit、source/acquisition 不符、错误 common-dir 或源 branch 装配
错误，沿原诊断指明 reviewed_base_source.commit、reviewed_base_source.selected_ref、
acquisition.decision_head 或 acquisition。缺真实上游来源回原 Sync/Intake；不靠改 hash
或省略检查恢复。同步新建真正 stale 仍经 refresh_review 回原 Sync。

## 受控消费者切换

原 Creation AI caller、共享 composition、record/create/check/recover 命令、公开示例、
Creation/C6 测试、Delivery 链与当前 eval/benchmark 调用方成套采用新版。
canonical data-contracts 的旧字段/本地分支断言同步替换。历史 legacy-profile fixture
保持其固定旧语义；其它 lifecycle owner 的同名 reviewed_base_head 不属于本迁移。

同一来源归一化用于新建和恢复。恢复不重跑 precreation uniqueness，不重复创建 Task、
branch、worktree 或 C4/C5。保留原 session owner：同 Task/generation/ref 保持，缺 record
重新 attach，不同或无效 session 阻塞，缺 context 继续 explicit-task。后来正常 ref 前进
不把已完成结果变成缺失。没有新持久化字段、授权存储、来源台账或第二恢复 writer。

## 在途调用、旧结果与退出

1. 已成功的旧创建或其丢失 stdout：固定原操作使用的完整旧 provider 和匹配 upstream，
   由其原 check/recover 读取同一身份。当前切换不将旧输入送入新版 runtime，也不重复创建。
   固定前驱源码为 `5c6a4591db7165ece045e6b0eb789c21d06d7d38`；更早操作使用其实际
   采用的完整版本。不能只复制一个旧脚本到新安装冒充 matching provider。
2. 尚未执行的旧输入：回原 Sync/Intake 取得真实来源，经当前 Creation owner 重审并装配
   新版输入；没有足够来源时停止。不得从旧 reviewed_base_head 或当前环境猜 kind。
3. 已消费 created 的活动 Task：按当前 Identity/Ensure、session、Delivery 和原阶段续接，
   不重建 Task、不增 generation、不将旧成功结果转换为新 gate。
4. 原 provider 的结果恢复消费完毕后，旧调用退出普通执行；历史 Git/schema 验证保留。
   当前包维护方不延长 runtime 兼容期，也不删除已完成历史或扫描清理其它 Task。

## 分发、回滚与验证边界

完整 canonical source 经原 `guru-upgrade-tools` preview/prepare/invoke 更新选定目标，
保留 Task/session、用户配置和 peer。当前 Task 存在时不得用普通 apply 或手抄受管副本
绕过维护边界。按原 managed hash/manifest 逐项处理冲突及 .new/.bak，再由目标自身
installed/native/公开 Creation 验证，核声明平台、mode、drift 和 reapply。

更新中断或冲突由原 tools 同操作 resume/rollback 处理；回滚先核其 tools/data 兼容，再
恢复原 preimage。没有 Task 数据格式迁移。原结果仍由实际 matching provider 恢复，
不能用回滚改变历史身份或重做已完成副作用。

定向验证覆盖完整 Sync read→Discovery→Clarify→Wording→Readiness→Creation、旧 main 与
primary staged/unstaged 保持、原结果恢复、真实 mismatch、同步新建/恢复、新旧 schema
替代拒绝及原 session 分流。至多一个代表性 clean 安装，复用同样本 reapply。
确定性 fixture、实际 Agent、source/installed 和正式 Release 证据分别报告；本合同不
声明任何执行通过，也不要求完整多平台 Release/upgrade 矩阵。
