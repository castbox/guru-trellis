# 父仓 Git 内容要求

Identity：RDT-REQ-PARENT-GIT-CONTENT；aliases：gitlink、submodule、父仓原子内容。Owner：RDT。Status：proposed。来源：Issue739行为要求/最小验收（2026-11-05修订）；适用前驱Git b78edbbdc32e77392bc3775366473971050ccb4b。原RDT owner经完整candidate Check后晋升/readback才为current，不以文件存在声明实现。

R739-01：父仓流程以父index/tree path/mode/OID处理gitlink，不进入child或读取其HEAD/root/clean/初始化/文件/对象，不init/update/fetch。正常child状态不改变父身份或准入。父显式新增/更新/删除/类型变化保持可见，捕获后父条目改变继续stale；精确提交用被审父OID/absence，不重采childHEAD。

R739-02：自然resolved路径保留唯一MERGE_HEAD、stage0 tree及原Reconcile精确parents/message；公开校验的精确当前Task task.json自然metadata可保持unstaged，原bytes/index保留。其它Task/业务unstaged、unmerged及过期父内容仍拒绝，不额外stage metadata掩盖缺陷。

R739-03：真实同责任Check/Commit/Review/Reconcile/shared/verification snapshot与canonical/受管投影采用同语义。旧未执行private重新prepare，既成commit/receipt由原owner恢复。显式child root独立执行；破坏性清理边界保持。

本单元只定义Guru侧职责；上游API由castbox/Trellis owner承担。17015调查时存在regular-only缺口；#62已通过PR63合并为3c37c75897f530c3ae8c5c4d85f6c1f3455b2e5f，公开接口新增父gitlink原子语义，业务工具采用与现场效果仍独立判断。源码/投影和最小行为验收完成不声明业务恢复；不新增采用、复跑、全矩阵、独立验收artifact或审批义务。设计关系：D739-01..03（../../design/current/parent-git-content.md）；测试：T739-01..03（../../test/current/parent-git-content.md）。
