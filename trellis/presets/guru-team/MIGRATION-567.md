# #567：固定开发基线与正常在途接续

本迁移直接演进完整 canonical graph。开发中的旧 Task 仍由完整旧安装拥有；
升级工具或旧数据转换使用 #566 的独立入口。本合同不要求先 Reconcile，
不把当前 source Skill/DTO 单独复制到旧安装，也不触碰来源业务仓与会话资源。

## 切换与退役

- 原 `guard-task-base-pair` 命令、wrapper、validator 与两份结果 schema 删除。
  所有默认 guard→Reconcile 边同时退出。旧 caller 必须重新加载完整新 workflow，
  不把旧 `new_pair`/`current_pair` receipt 作为新阶段输入。
- Planning/implementation 选择固定内容 B，当前实际 HEAD 为 H；已有 Delivery
  candidate 优先用于恢复，D2 从真实前序 delivery_result 计算，不重取最新 target。
  正常新结果的 base_ref/head_ref 为完整 commit OID。旧 symbolic candidate 未具备
  可恢复的固定事实时，回原范围/实施 owner 读取既有 Check/Review/commit 事实；
  不能把后来 origin/base 的值冒充旧锚，也不为补锚强制同步。
- Reconcile 的 selected_base_ref 现在明确是一次操作的 target OID。旧请求有
  new_base_head 时，由原 owner核对其真实操作、候选、parents/tree/message 后，
  将同一个 target OID 投影到该字段。缺少事实时重新准备同一原子操作，不猜测 ref。
  保留 ordinary、实施前 resolved baseline、实施后 resolved candidate、精确提交
  与结果丢失恢复；整合目标不能替换 Delivery 内容 B。
- 原 `phase2` resume discriminator 保留接口，但其 consumer 执行实际差额与受影响
  依赖的有界复核。旧 Check/full_review 作为历史保留；新 candidate 后不 applicable。
  原实施 owner begin_check、Check 实际判断并记录、Review 实际判断既有完整审查
  加解决差额是否覆盖 B..Hi 后记录本人新 full_review。没有既有完整 Review 时仍
  执行首次完整 Review。continuity DTO 不能改标签成为 full_review。
- clean committed reentry 使用当前 Check 的固定完整范围，保留现有 commit、
  hooks、精确 staging、scope/plan、Task/Delivery/generation 及资源归属检查。
  不造空提交或同内容提交，不以 target ancestry 取得资格。

## Merge 与 Finish 私有恢复

Merge 私有 gate 2.0 删除无当前 consumer 的 pre_merge_base_head，action 绑定目标
branch 名、expected task HEAD、method/message。旧 1.0 先按原字段与原 action
digest 校验，再由同 owner 在内存薄投影为 2.0；其旧事实仍可读，不重做业务 gate。
已合并结果读取真实 parents/message/merge ID 和当前 target 可达性。#566 的旧
schema1 历史归属仍消费原 gate，不允许据此发起新 merge。没有服务器更新要求的
behind 不是 blocker；实际 conflict/check/server blocking 仍由原 Merge 判定。

Finish 当前 semantic-result 2.0 与 private transaction 3.0 删除 expected_base_head。
旧 semantic authoring 由原 AI owner 移除该无消费者字段后按当前合同复核；不把
schema1当自动公开兼容入口。已存在 private transaction 2.0 经其原 schema 校验，
只删除该字段并投影版本为3.0，保留 operation、commit、PR、payload 和 stage，
下一次正常写入持久化新格式。已成功 target 后续前进按原结果可达性恢复，
不要求目标停在旧 SHA；真实 archive/summary/active-path 终态仍必须存在。

## Authority 与历史 consumer

阶段保留明确适用 authority；普通 CURRENT、工具安装或无关提交不自动使其过期。
真实 scope/方案/依赖或明确立即适用的新规则归原 owner；shared-current promotion
仍有当次 expected-current 写前一致性。Completion 对当前全部 scope 和真实
Deliveries 作判断；历史截点只证明其范围，补缺失事实和受影响结论即可。
#569 独占查询准备，本迁移不实现查询、不将其设为交付前置。

完整 preset apply/reapply 和 declared platform投影在匹配 source＋installed
受控 checkout验证；旧开发 checkout 不被隐式迁移。实际验证与未覆盖项由
[本次 Test](../../../docs/requirements-design-test-contributions/567-fixed-development-baseline/test.md)记录。
