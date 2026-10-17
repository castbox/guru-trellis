# #577 Design 增量

状态：active，随 RDT `.106` 晋升；继承 ADR-024/027 的公共模型、独立维护和原owner边界。要求由 [requirements](./requirements.md) 单写，实际结果由 [Test](./test.md) 单写。

| Responsibility / Contract | 原位承接 |
| --- | --- |
| D577-01 / CON577-01：独立语义入口 | 原 source-loaded `guru-maintain-legacy-task` 新增闭合 `archive_resume` profile，明确 archive task_ref、original_task_ref、active_ref、TaskKey与source。AI判断恢复意图、历史事实、未完成义务、精确处置及下一owner。convert/history_closeout/resume/rollback不改义。 |
| D577-02 / CON577-02：公共数据恢复 | 原transport转发 `inspectTaskTarget`/`prepareArchivedTaskResume` 与公共apply/resume/rollback。AI提供resume_intent和完整projection/artifact/session/binding计划，公共Trellis唯一写入模型并返回resumed_task。Guru不推导generation或复制转换/updater。actual pair digest和source_locked build/mode校验保持。 |
| D577-03 / CON577-03：原私有owners | 原Publish/Merge核验历史；原Publish/Merge/Finish及明确选定gate owners分别检查、冻结、退役和恢复自己的controls。original_task_ref用于控制归属，archive物理source用于原始bytes。未完成Closure/Finish/Finalizer回原事务，terminal与seal保留；coordinator不代删私有目录。 |
| D577-04 / CON577-04：唯一当前身份与业务续接 | 原current Identity/Bind复用目标安装官方active TaskId resolver与bound checkout。首次C4前只用目标公共schema parser核验active artifact及占用；C4建立归属后，bound执行回官方active resolver，不形成首次绑定循环。创建/历史reservation保留；原archive不成为第二current。目标installed Identity、C3 checkout、C4 branch binding、Bind和native continuation后，执行真实所需Clarify/Completion或真实新Delivery的Creation/Author。恢复不制造当前pass或业务完成。 |
| D577-05 / CON577-05：同操作恢复与保护后续工作 | 原维护checkpoint仅保存公共operation/recovery、原私有preimages/refs及返回identity。丢输出和普通写集前缀恢复不reprepare。回退先检查private postimage，再由公共owner核对data兼容/后续工作，最后恢复原controls；不扩大tool backup。 |
| D577-06 / CON577-06：完整分发与依赖边界 | canonical Skill/workflow/preset为源；原apply/reapply同步dogfood及声明平台，检查installed inventory、drift、sidecar和upstream-owned文件不改。原tools owner对明确记录dirty的provenance commit按原路径核验历史bytes，不把其整体metadata或HEAD当安装身份；未知preimage仍显式处置。新pair仅local_candidate隔离证明，正式pin维持原值，缺能力写前阻塞；无正式采用/真实业务/Release结论。 |

兼容为原maintenance边界的有界旧数据支持。普通lifecycle保持current-only；旧profiles/Plan2有真实consumer，consumer退出后由明确migration删除。没有新增Skill owner、第二状态机、授权持久化或OS原语业务authority。Architecture contribution位于 [专属贡献](../../architecture/contributions/577-manual-archive-resume.md)，晋升由原owner串行执行。
