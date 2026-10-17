# #589 不可变内容读取责任增量

本增量保留DES-557-01/02/03、D569-01/02与CON569-01/02的业务authority，只收敛实现与资源生命周期；旧贡献仍是其发布时的历史证据。

## D589-01 公开Git摘要owner

manual_recovery.commit_candidate与history query2直接使用固定Fork公开GitCandidateContent(actual_root).content_ref(exact_commit, paths)，算法和序列化仍归上游delivery_store。替代DES-557-02临时文件物化落点，不改变完整差额、expected摘要、事实归属或Completion判断；可变filesystem API不变。Guru不导入private observation、不复制hash、不新增缓存或公共DTO。

一次手动恢复拥有并关闭context；一次历史discover在当前实际root共享context。摘要操作置于原HistoryContext.prepare/retry内；换至临时bare前关闭旧context，重建后处理同完整不可变目标，退出释放。D569-01的隔离metadata/config/objects/pack与原失败原因保持，候选内容不再由Guru逐路径物化文件；公开上游内部临时批量传输由其生命周期管理。CandidateObjects及其唯一caller退出，其他consumer的shared reader保留。

## D589-02 复用与独立检查

以实际repo、完整commit/blob与相同计算规则在一次调用内复用内容和摘要；各路径mode/删除/编码/排序贡献保持。各份Task/Delivery/PR/merge/ancestor/cutoff/expected独立检查不复用阶段结论。相邻操作刷新移动ref/index/worktree。D1–D6的其他已优化原owner仍拥有其算法与语义，不改#588范围。

## D589-03 来源与证据

current source lock、extension manifest、ownership和原安装/升级目标断言成套一致，公开能力由实际模块检测；原source_locked tools owner消费clean committed source生成完整投影及receipt。历史已发布来源、Task/session/peer和原迁移算法保留，不手改上游安装或历史Task。current来源数值只在原source lock拥有，不在此复制。

按Issue当前§6固定可比较方法：请求volume、独立hash/profile、plain wrapper timing和RSS有明确测量边界；以冗余读取/计算消除、独立校验及有界资源验收，不设耗时改善百分比硬门槛。旧数值门槛与全部失败cohort保留为历史观测，不改称通过。实际结果由本目录test.md链接原Delivery唯一工程结果，避免复制样本。RDT由原owner按expected`.103`晋升`.104`；Architecture贡献仍由其原owner在独立committed Review后晋升。新增diff重新质量门禁。
