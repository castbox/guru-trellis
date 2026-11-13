# ADR-EXPLICIT-TASK-QUALIFICATION：显式资格对象承接

状态：integrated_pending_review。来源：[Issue #812](https://github.com/castbox/guru-trellis/issues/812)。
固定 before 为 f16bb562e4ea844939786cebd5c6c20e686914b2。原 Architecture owner 在批准
Planning、完整实施和工程结果后，于 final_integration 写入并读回本决定。
独立 committed Review 尚待执行；本状态不表示质量通过、发布或 Task 完成。

## 问题与约束

固定 before 中，合法 explicit-task 已经由原 Identity/Ensure/Bind 确认 Task 与唯一
checkout，但资格共享 Planning 路径只收到 task_ref，以无 key current() 查询 session，
丢失 caller 已有的显式对象。不能借其他会话 key、从 inventory 选对象，或关闭
Planning/候选一致性检查。三个原资格 owner、条件加载、非通过出口与原 caller 必须保持。

## 决定与直接 consumer

七类 Task/Delivery 输入采用必填完整上游 delivery_key 的 input 2.0 与 aggregate3.0。
原 caller 从实际原身份/选择事实取得 key，共享 qualification_facts 是直接确定性 consumer。
事实解析复用既有公共 model、C4/C5、registered checkout 和 DeliveryProjection.current(key)。
有 context 时比较官方当前选择；只有确实无 context 时才校验显式对象，不写 session。

Planning 从该 key 的实际 planning_root 读取；supplied planning_paths 必须对应该目录
三份规划文件，原 raw-byte file-set 校验保持。author_candidate_set 只要求当前实际
来源/候选文件，不要求未来 design/implement。原 HEAD、路径和 candidate 检查继续成立。

typed output 不新增 key 或记录。同一 caller 保有自己的调用对象，原 router 按 profile
返回原 owner。没有新增 session/selection writer、资格 ledger、缓存或跨 owner checkpoint。
三 qualifier 的语义算法、短条件与原出口不改变。phase2_candidate_set 仍受原
pinned-old/recovery 限制，不创建新 Check 路线。

## 替代方案与成本

拒绝让 current() 从 Task inventory 推断唯一 Delivery：这引入隐式选择，并在有 context
缺失或冲突时掩盖真实错误。拒绝新增绑定写入或借会话 key：这改变原 session authority，
也会迫使合法无 context 调用创建会话。拒绝跳过 Planning：这会取消必要 stale/mismatch
校验而未完成对象传输。拒绝把 resolver 复制到三包：共同事实职责会分叉。

选择完整参数和原 model 校验，增加必要输入与事实读取，保留直接责任边界。
三个 package 的输入版本与真实 caller 必须同步维护；没有未来扩展容器、锁或恢复协议。

## 兼容、采用与退出

旧 profile/aggregate schema 与公开输入示例的 path/id/bytes 保留作历史验证资产。
current Interface、runtime selectors、caller、新版示例和受控 eval/test 同批迁移。
四类非 Delivery 输入及全部原 output/consumer 保持。current 不双读旧输入，也不从
ambient state 推断缺失 key。

旧待调用输入由原 caller 从真实对象重新装配；缺失身份回原 owner。已完成结论仅按原
applicability 采用，历史不改写。旧完整操作在实际固定旧 provider 恢复，不重复副作用。
[MIGRATION-812](../../../trellis/presets/guru-team/MIGRATION-812.md)拥有精确版本、恢复、
原 tools owner 的受管采用与回退边界；保 Task/session/peer，不迁移 Task 数据格式。

本决定窄替代 #793 当时输入保持的范围；不恢复固定三项调用。
ADR-CONDITIONAL-QUALIFICATION、ADR-008/020 的其余职责保持。完整 current 职责位于
[ARCH-DOM-QUALIFIER-APPLICABILITY](../03-domains/qualifier-applicability.md)。

## 验证、整合与重审

本轮确定性公开入口、真实无 context 和官方 context、原 caller 非通过接续及安装观察
由[配对 Test](../../requirements-design-test-contributions/812-explicit-task-qualification/test.md)
单写。root 的机制准入不证明整个修复完成。当前实际整合/readback 进入本地 TaskCommit；
随后同次独立 committed Architecture/Check/full_review 判断真实 before/after。

formal_fork_source_lock、完整多平台安装/升级/Release 矩阵与生产效果未验证。
本决定不承担外部交付终态。key authority、supported caller/恢复边界或 context 规则
实质改变时，由原 owner 重审；无跨仓修改或新增完整发布矩阵要求。
