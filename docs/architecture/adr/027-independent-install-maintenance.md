# ADR-027：独立维护入口与原 owner 承接

状态：accepted；补充 ADR-017/018，保留 ADR-024 公共模型 authority。首次独立完整 committed Review 范围 `3e8b281c93894cd3df4e704901bda63ca2885f23...95bcf24334f9a4d25df3f9175af9d00b58d86915`；由原 Architecture owner 随 `.91` 晋升，新增文档差额仍须 fresh gates。

旧格式原只在 source-loaded 完整 Plan2 升级边界解释。正常场景中安装工具不应强制转换全部任务，旧任务也可能无法使用目标 Identity/Continuation/Reconcile 取得迁移能力。

决定：保留完整 Plan2，另提供 source-loaded 单 checkout tools 与 selected legacy Task 两个独立 semantic 闭环。公共模板、Task/Delivery/session 模型、转换与恢复归 Trellis；Guru 只判断维护意图、编排自身资产，并由原 owners 核实历史事实/退役私有控制。普通 installed lifecycle 继续 current-only。所选任务自身 native continuation 和下一真实 owner 是恢复条件；历史已交付而待验收保持 evidence_pending，不从旧 gate 或已合并 PR 推导业务完成。

单目标 tools 使用原 managed Python owner 的 checkout-local override，primary/linked 同样隔离；普通 activation 更新现有 effective scope，完整升级恢复覆盖该路径。公共数据兼容性在任何单侧工具回退前核对；不兼容写前阻塞，不扩大工具备份。

不采用：绕过旧预检、伪写版本/declaration、复制公共 converter、外部代执行冒充目标恢复、第二生命周期、普通旧格式 dual-read，或为历史保留制造 Completion/Closure/Finish。raw archive/note 可读后才由原 owners 精确退役所选 carriers，保留外部义务及其它任务。

兼容退出：旧完整 Plan2 仍有现存 consumer，原 API 不改义；legacy-only profiles 在真实 consumer 退出后由明确 migration 删除。source_locked 正式缺口与本地 matching candidate 分别报告。具体责任、实际证据及未验证边界由[已晋升贡献](../contributions/566-single-checkout-upgrade.md)与其唯一 RDT Design/Test 承接。知识晋升不表示正式依赖采用、业务完成或软件发布。
