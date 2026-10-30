# 机制审核追踪

固定前驱：Git `2f70796103406683a2f63adfb6b54d247a7433a5` 下六个 `docs/{requirements,design,test}/current/{knowledge-maintenance,completion-closure}.md` 完整正文。`proposed/` 保留前驱并追加本次定义，未删除或重编号既有身份。架构方法投影另由 `docs/architecture/contributions/architecture-mechanism-review.md` 承接，不复制为 RDT authority。

| 整体需求 | 新要求/行为 | 设计责任 | 测试 |
| --- | --- | --- | --- |
| R1/R3 | R-MECH-01 / BEH-MECH-ADOPTION | D-MECH-01 / CON-MECH-ADOPTION | T-MECH-01/02/03/05 |
| R2 | R-MECH-02 / BEH-MECH-PROTECTION | D-MECH-02 / CON-MECH-PROTECTION | T-MECH-01/02/05 |
| R4 | R-MECH-03 / BEH-MECH-EVIDENCE | D-MECH-01/03 | T-MECH-01/03/05 |
| R5 | R-MECH-04 / BEH-MECH-UNCERTAINTY | D-MECH-01/02/03 | T-MECH-03 |
| R6 | R-MECH-05 / BEH-MECH-LEGACY | D-MECH-03 | T-MECH-03/04 |
| R7 | R-MECH-06 / BEH-MECH-COMPLETION | D-MECH-04 / CON-MECH-COMPLETION | T-MECH-04 |
| R8 | 上述规则的验证与分发 | D-MECH-01..04，原分发机制 | T-MECH-01..05 |

本项实际结果唯一在 test.md。历史观察、旧来源和公共接口原义保持；无导航身份或关系变化，不改根 README、全局版本或历史结果。
