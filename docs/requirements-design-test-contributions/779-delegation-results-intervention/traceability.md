# #779 双向追踪与增加边界

适用 Git `221f74caef372414a1c7d700575742eb1e075af4`，authority `guru-trellis-rdt`；Architecture `docs/architecture/README.md / guru-trellis-architecture / active`。本贡献 proposed 镜像最终路径，内部相对链接按目标路径解释。完整前驱为该 Git 下三个 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 单元；保留全部旧身份和有效条件。

| Task accepted scope | requirement / behavior | design / contract | test |
| --- | --- | --- | --- |
| R779-01..06；SC779-01..04；AC779-01 | R779-01 / BEH779-DELEGATION | D779-01 / CON779-DELEGATION | T779-01 |
| AC779-02；实际投影采用 | R779-01 / BEH779-DELEGATION | D779-01 / CON779-DELEGATION | T779-02 |

只增加委托后的协作行为、原职责关系和最小验证层次，不替代原 source/scope、discovery、Check/Review、公共模型和知识晋升合同。canonical 方法单写；不改 root/current 导航或无关全局版本。候选 Architecture/Check 读完整 proposed；原 RDT final_integration 才写 shared current/readback，实施重绑实际 after 后最终质量链覆盖真实内容。以上保留候选 Check 前的拟写观察；实际晋升由原 RDT 结果承接。
