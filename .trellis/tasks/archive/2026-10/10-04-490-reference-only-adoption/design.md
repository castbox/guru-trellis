# #490 设计

## 最小演进

现有 task-lifecycle-dtos 已有 reference_only，现有上游 creator 已支持两种 Issue disposition；直接把 task-creation-input.schema.json 的 exact_source const 扩为 exact_source/reference_only enum，并检查现有 invocation、executor、recovery、source reader 使用原值。保留现有唯一 writer，不引入适配器、第二创建路径、迁移脚本或额外持久状态。没有需要删除的旧能力；本变更为 additive，原调用不变。

## 官方来源与投影

source lock 从 64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac 前进至 9c36002a324c16a09a85b6aa5a380b74aabf801f，tree 1eb0dc446bb8b8f122db771e00a7004b48eaf4d8，parents 为 64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac 与 505d853cbc90db050f135cf0cc8f81f36e434e18，CI 37179218822。使用已构建的真实 Fork CLI 正常生成官方模板；经官方 update/init 和 canonical preset apply 同步，不手工伪造 .template-hashes、版本来源 marker 或生成文件。CLI/core 与 extension 的版本轴保持 0.7.0-castbox.1 / 0.7.0-guru.1，repository 发布轴由 #489 决定。

## Owner 与兼容边界

guru-create-task 仍拥有正式创建与恢复；上游 task.py 仍写 task.json；Guru lifecycle reader 仍检查 current schema；现有 source disposition consumer 仍决定 closure。reference_only 只表示来源引用，不能用于 exact_source 关闭。正常旧归档保持只读诊断，旧 0.6.17 原地 update 仍拒绝，拒绝证明不在本任务扩成完整发布矩阵。

## Architecture 与 Docs SSOT

Architecture 选择 target_native：能力进入已有 C6 source 合同，source adoption 更新当前受测边界；无新 owner、GAP、ADR 或兼容双读。先写 docs/architecture/contributions/490-reference-only-adoption.md，涵盖九项 required concerns、before/after、唯一 writer、验证与 promotion。独立完整 committed diff Review 后由 Architecture owner 推广 current .70 至 .71，并对 promotion diff 重新 check/review。

RDT 先写 docs/requirements-design-test-contributions/490-reference-only-adoption/ 的 manifest、requirements、design、test、traceability；审查后由 RDT owner 串行创建 .71 successor。历史 .70 版本不可修改。README、source lock、current spec、canonical Skill 合同随实现同步；#489 release 目标与 predecessor 拒绝合同由该任务持有。

## 验证与风险

正式创建 fixture 覆盖 wrapper→schema→upstream writer→recovery，避免只有 enum 字符串断言。安装验证用一个代表性 clean repo 和同一新版本 update/reapply，逐一检查 .new/.bak 与 drift。平台 validator 证明可加载及投影一致，不能冒充所有平台 native-host 运行。上游 #25 的已完成测试是来源证据，Guru 投影与安装必须在本候选重新验证。
