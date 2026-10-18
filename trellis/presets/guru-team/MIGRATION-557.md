# MIGRATION-557：手动 MERGED 的公共结果承接

本增量沿原 Merge owner 增加 `delivery_merged_recovery`，采用
`guru-merge-task-delivery-input-delivery-aggregate-2.0`、独立 input/review1.0、
history query2.0 与既有 delivered/TaskKey/Completion consumer。
公共 Task2/Delivery API1、DeliveryFact 和输出合同不变；没有第二模型或 ledger。

最低采用组合是包含本增量的完整 Guru preset：Merge package 的
SKILL/contract/interface/runtime/schema/commands/examples、Completion 的实际候选
审查合同、canonical workflow/spec 与声明平台投影必须成套应用。受控上游候选
继续由 [Task/Delivery migration](spec/workflow/task-delivery-migration.md)
绑定产品 SHA 与 CLI/Core tar，不以版本字符串替代内容身份。

现有 expected-head/Guru executor、合法 schema1/2 trailer history 和原输出恢复
保持原职责。query1.0 仍只读消息历史；具名消费者是 Merge 的旧私有历史迁移
及原 standalone trailer discovery 调用者。它不变成任意 public importer。
需要读取无 trailers 已记录事实的当前消费者显式选择 query2.0，并提供 exact
TaskRef；Completion 本身直接读取 aggregate，不依赖消息扫描。
旧查询最后一个真实具名消费者退出后，原 Merge owner 在其消费者迁移范围
中删除旧入口/解析/schema/example/tests；本 Issue 不扩张其支持期或增加 fallback。

直接把 query1 改为读 Task2 会改变既有三字段输入职责并要求不存在的 TaskRef，
因此本增量明确新 query2。新增 profile 交给旧 package 会被拒绝；中断调用应由
完整匹配安装的原 owner fresh re-entry，不桥接旧 checkpoint 或重建授权。
仍未完成公共与 Guru 私有成套迁移的旧安装固定原完整版本；不单拷 writer、
不提前切换 source dogfood。旧安装实际采用归原 Upgrade owner。

验证分别证明 source/runtime、新 matching installed 公开调用、真实 GitHub 手动
合并、reapply/drift、旧 source carrier 的实际拒绝/残留。source 通过不证明旧安装
已采用；代表性样本不证明原 backend #149/PR #526 恢复、业务验收或 Release矩阵。
源码同步受迁移前置拒绝时报告原错误，不手改投影掩盖失败。
