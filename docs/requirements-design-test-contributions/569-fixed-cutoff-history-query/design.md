# #569 设计增量

需求身份见requirements.md；实际结果唯一见test.md。延续Architecture .92、ADR-026/028，原Merge/history owner拥有事实和准备，原Completion/独立/恢复caller拥有适用性与路由。无新owner、Skill、状态库、ledger或ADR。

## D569-01 固定历史与隔离准备

落点：`trellis/skills/guru-team/packages/guru-merge-task-delivery/runtime/history.py` 的 `discover`、`HistoryContext`、`first_parent_history`。

原repo-bound gh读取remote base commit一次。first-parent必须完整到真实root；可达shallow边界即使rev-list成功也不构成完整。优先复用caller完整对象，缺少历史/必要候选对象时，在调用内temporary bare Git context获取固定cutoff和有限必要immutable目标，每目标最多一次。无destination ref、FETCH_HEAD、tags/submodule或maintenance；不写caller共同Git数据。上下文切换把已需要目标一并准备，后续读同一实际context。

临时初始化metadata/config/objects/pack及候选快照是真实写入，成功/失败退出清理。网络、认证、权限、目标不可得分别保留具体原因；必要历史不完整具体失败，不伪装空结果或要求人工fetch。Git transport只提供事实，不判断是否Task完成。

## D569-02 两类输入与截点后public fact

query1仍只识别合法schema1/2 trailers；query2经原public parser读已记录事实。保留真实repo/base/PR/merge/两父/parent2/head、候选bytes/modes及唯一identity核验。`manual_recovery.commit_candidate` 增加内部可选git_root参数，原manual调用默认自身root；history显式传入所选context，无第二候选hash实现。

固定cutoff扫描按原顺序融合和去重。扫描外public事实先验证真实身份、父提交和candidate；只有其完整first-parent链确实包含B1且其自身不等于B1才作为后继排除。其它关系或无法核验具体失败。该核验不把后继作为新cutoff或收集其它交付。

## CON569-01 public result与迁移

原输入query1/2不变，当前输出统一`delivery-history-result-3.0`：schema_version、status、task_identity、repo_ref、base_ref、cutoff_commit、deliveries。cutoff为完整B1 commit。完整扫描后无匹配交付才返回合法空数组。旧result1/2仅历史schema/example，不再是当前输出选择或fallback。

受控Merge、schema/interface/commands、Completion与平台投影按MIGRATION-569完整切换；commands准确为git_write（仅临时数据）。没有双读adapter。旧开发carrier不通过源码变更半升级，采用由原安装owner负责。

## CON569-02 原consumer与验证分层

consumer用公开repo/base/task/cutoff及原query上下文，不读producer私有状态。仅无关B2前进直接消费；明确同Task新Delivery/所需证据变化才向原owner有界补缺少事实并重判受影响结论。输出丢失重新查询得到新操作自己的明确cutoff，不推导未观察旧B1。不增加每次Completion的history强制前置，不重跑旧业务gate。

真实Git组件、matching installed wrappers、实际AI consumer、外部live与Release证据分层。原RDT单写本目录；本贡献在首次独立完整committed Review后由原owner调和晋升，新差额重新Check/commit/独立完整Review。source changes不迁移当前Task，不改upstream或共享内核。
