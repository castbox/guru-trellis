# #694 实际观察与验证边界

观察截止：完整实施候选及同 checkout tools-only 安装。候选 Check 和 shared-current final_integration 尚未执行。完整策略见 [T694](proposed/docs/test/current/task-delivery-lifecycle.md#t694显式评审对象与执行选择)。

## 源码与正常调用

- Architecture 原套件 52 项通过。后续新增边界定向运行中，其他 Task 无 Delivery 选择的冲突、正常 scope/root/phase 失配、当前 aggregate/分支/current consumer/相邻 Approval schema、两 mode 下无绑定/Task-only/匹配选择，以及真正无 context 的原入口均通过。Task/session/规划/baseline/资源控制目录的字节快照保持。测试语义 fixture 不代替 AI 评估。
- 一条新 C4 断言最初误以为会到后层 worktree field；实际原 public identity resolver 更早以 task_id 拒绝普通 checkout 分支变化。保留生产首失败，修正期望后该测试通过。没有放宽 guard。
- 原 Author 全套 22、shared DeliveryProjection 16、Approval 31、Activation 6、Wording 32 项通过。Author 中新增组合测试实际从未绑定 reviewer 调用正式 final_plan 成功，再调用原 Approval recorder被原选择 guard拒绝，确认显式对象不授予相邻执行资格。原 candidate_assessment 仍拒无绑定。
- Source package validator passed。363 个 Guru Python 文件内存 syntax、git diff --check 通过。测试使用实际 .6 installed upstream public modules，经当前 managed resolver运行。首次误指旧 .5 fixture 的调用已停止，不作为当前通过证据。
- 无写快照首轮包含整个 .git，遇后台 Git object 移动而失败；改为需求中的 Task/session/规划/baseline/资源控制目录后通过。该修订只界定验证对象，不更改产品行为。

## 本 checkout 安装与采用

- 普通 apply实际返回 upstream_delivery_migration_required，被历史归档数据 preflight阻止；未迁移或修改无关archive。
- 原 guru-upgrade-tools 从本批完整 dirty source及核对过实际字节的 .6 CLI/Core local_candidate 执行冻结工具操作，返回 tools_upgraded / 0.7.0-guru.7；formal_fork_source_lock明确未验证。公共实际字节/mode变化只有 .trellis/workflow.md，preset同步Architecture受管投影和安装provenance。Task/Delivery/session/archive、AGENTS与用户config字节保持，原writer检查peer/common pointers保持。
- 同一次操作的原 installer与public maintenance proof完成真实reapply，skill_packages/overlays=ok、installed validation=0；保留快照保持。无手patch guard、manifest/hash。
- Source/installed packages、ownership、Shared/Claude/Codex/Cursor投影、dogfood drift、mode和递归零.new/.bak通过。workflow及installed Architecture runtime与canonical字节一致。目标原生get_context --json exit 0，原Task/Delivery仍为implementing，Planning accepted result保持。

## 尚未验证

原独立 candidate Architecture、candidate/final Check、final_integration/readback、实际candidate重绑、commit与独立committed Review仍待原owner执行。完整新入口的语义判断不从fixture或分发自动推定。

业务#961现场、后续串行Issues、所有平台实际Agent、额外clean installation、完整多平台升级/Release矩阵及性能收益未验证；不属于本项新增要求。静态、集成、installed、原正式语义门禁与GitHub交付分别表达。
