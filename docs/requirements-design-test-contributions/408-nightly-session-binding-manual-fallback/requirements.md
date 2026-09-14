# #408 Requirements 增量

状态：`draft` task-isolated contribution。唯一新增产品 authority 为 [Issue #408](https://github.com/castbox/guru-trellis/issues/408)；当前 shared authority 保持 `.50`。本文件不代表实现、发布或 current promotion。

| Identity | 相对 current 的需求增量 | 继承 |
| --- | --- | --- |
| R408-01 | source 精确绑定 db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0 / CI34838784963 / CLI与core 0.6.17 | R329-01 的 current pin 被本候选替代；历史记录不改写 |
| R408-02 | 官方 build/update/init 与 Guru preset 同源投影 | R378-03、R329-02/09 |
| R408-03 | 同一明确 session 经正常 Guru authoring/创建器建立 linked task，双端mapping和boundary通过后受控激活，返回primary仍解析同一任务 | R378-02 的非所属 session 隔离继续有效；裸task-store probe不代替Guru创建链 |
| R408-04 | 正常Agent能按实际安装合同调用原owner；私有派生字段归recorder，不依赖eval runtime或手工补mapping；保持旧lifecycle与retired-zero | R247-01..10、R329-03..07；不新增节点/Skill/exit/recovery artifact |
| R408-05 | 自动异常停止时报告原错误、已知状态及未知事实，不视作新 no_task 或自修复 | 既有诚实报告与 fail-closed |
| R408-06 | 用户指定的每项手动 Git/GitHub 操作独立读取、展示、确认和执行 | 既有 Git/gh authority 与操作确认边界 |
| R408-07 | 手动操作结果与 task/runtime/Finalizer/archive residue 分离，不追认 lifecycle 完成 | 既有 Publication/Finalizer/Merge ownership |
| R408-08 | source、installed、Agent 行为和远端发布证据分别报告 | R378-04、R329-10 |

#398、#407、上游源码/版本/npm 发布均不属于本增量。授权不持久化；不引入恶意输入、锁、TOCTOU、进程/FD authority 或额外恢复协议。
