# 稳定知识身份与最终整合晋升需求贡献

状态：proposed；本文件记录#638批准delta，完整拟写正文在[proposed/docs](proposed/docs/)。未由原RDT owner实际晋升，不声明shared current已更新。

R638-01/05：完整知识单元和必要关系保持稳定ID，Architecture/RDT使用稳定authority identity，完整Git revision与locator绑定精确内容。普通Task不强制全局递增、总入口必写或逐Issue摘要；根导航只在定位/身份/状态真实变化时更新。真实public API版本、bootstrap distinct successor、旧引用及历史原义保留。

R638-02/03：Task在隔离贡献准备完整拟晋升正文，首次完整独立Architecture及原Check在写前审全候选。原implementation先candidate/begin_check进入checking；候选Check通过后合法rework回implementing，再candidate_checked进入唯一最终整合consumer，不写最终public Check。

R638-04：原Architecture/RDT在同Delivery最终整合固定真实目标，读取命中完整单元，保留双方有效条件，补审实际差额、组合语义和受影响未改consumers，实际写入读回。implementation以同B和实际HEAD重新candidate/begin_check，最终Check/commit/独立完整Review覆盖实际after。no-change无空贡献/ADR/文件/commit。无实际Git阻塞不要求merge/rebase或追赶。

R638-06/07：原owners/public模型保持。Arch非Planning5.0/Delivery3.0、RDTimpact/promotion2.0、Checkprivate6.0及直接consumers成套matching切换；Planning/bootstrap/repair不改义。旧runtime退出，不转换旧pass，不长期双parser或第二current。未晋升、已晋升未Review、已有Review三类由原owner按实际状态恢复，同key/B保留。源码、wrapper、安装、实际Agent/GitHub和完整Release证据分层，不以规划或fixture预填通过。

完整来源及替代位置由[traceability](traceability.md)拥有。完整目标需求为[knowledge](proposed/docs/requirements/current/knowledge-maintenance.md)和[lifecycle](proposed/docs/requirements/current/task-delivery-lifecycle.md)，保留未改能力及全部原有效条件；不修改Backend现场、#635、队列/锁、攻击/TOCTOU/压力/crash或完整Release矩阵。
