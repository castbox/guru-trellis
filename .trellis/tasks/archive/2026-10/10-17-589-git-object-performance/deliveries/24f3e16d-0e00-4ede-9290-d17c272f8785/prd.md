# D4 Cleanup 同调用不可变对象读取

Direct Source为#589全步骤盘点与第5–8节；整体AC01–15不变。D1–D3已交付，本批解决原select_explicit_cleanup_targets对多个正常旧Task快照资源重复枚举同head树、读取同Task blob的热点。

同次原公开调用复用按实际仓库与不可变commit/path/blob绑定的元数据与唯一内容；各资源ledger/binding、当前ref/worktree、expected head、归属与删除前检查仍独立实时执行。保留typed exits、错误、首次/恢复及删除行为，不改normal/machine-handoff合同，不新增public API/schema/持久cache/审批。使用D3原TaskObjectReader有限OID spool，不建新通用框架。

实施前原公开wrapper测10/100正常同head快照分支，其他规模固定；先完成两轮before再固定热点、完整preview/实际删除及恢复耗时/RSS门槛；记录全部Git、show/cat-file/ls-tree、唯一OID和内容bytes。之后才改生产，原方式同步dogfood/代表性installed并同条件after。覆盖多head/多Task、正常缺失/类型/读取错误及相邻调用ref移动，原owner检查不减。

上游task_store逐路径创建与delivery_store重复hash仍未完成；不绕过、不缩scope、不关闭#589，不执行#575完整Release矩阵或业务仓升级。
