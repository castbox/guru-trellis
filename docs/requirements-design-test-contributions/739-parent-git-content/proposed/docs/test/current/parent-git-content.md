# 父仓 Git 内容测试策略

Identity：RDT-TEST-PARENT-GIT-CONTENT；aliases：gitlink regression、自然resolved metadata。Owner：RDT。Status：proposed。来源：R739-01..03及D739-01..03；原RDT owner经candidate Check后晋升/readback。本文定义必要观察，不预填测试通过。

T739-01（R739-02→D739-03）：一个真实Git resolved fixture保留公共begin_check自然task.json状态，经生产record/check/invoke/projection/Reconcile wrappers；独立核实际tree/parents/message和Taskbytes/index。fixture不得额外stage metadata修补被测producer输出，后继consumer只补命中回归。

T739-02（R739-01→D739-01/02）：代表性真实父index fixture证明child未初始化/dirty/不同HEAD或无对象不影响父身份；父新增/更新/删除/类型变化进入原子捕获与isolated index，删除保留child目录也成立，父index drift仍stale。普通文件和hook兼容复用现有回归；按逻辑分支选用例，不做child状态×Skill×平台矩阵。

T739-03（R739-03→D739-03）：直接受影响package/runtime与canonical/dogfood/声明平台投影一致性检查；只有安装行为实际改变时补必要定向安装。保留17015时上游regular-only阻断的历史观察；采用#62固定3c37后，原adapter回归须经真实provider核父路径进入candidate、verify接受及父tree OID，不再断言旧拒绝。工具采用与未验证业务现场分开报告，不mock为完整成功，不以业务复跑、Release矩阵或独立证明artifact增加本Issue门槛。

真实结果归原Check/Review及Git交付事实，本文不建立第二通过台账。关系：../../requirements/current/parent-git-content.md、../../design/current/parent-git-content.md；payload和算法由原canonical spec单写。
