# #711 来源、目标与稳定引用核对

本次源 Git：`f75f0f5dd078a0c2c4c9a54ac861383774162806`，同 tree 读取 `docs/{requirements,design,test}/README.md`、`current/README.md` 及完整正文。原 current entry 的晋升状态及原单元来源保持；候选存在不代表新切换完成。原 `.109` 未迁移 inventory 与所有 predecessor Git 引用保持原义。

| Requirement / behavior | Design responsibility / contract | Test strategy / scenario | 完整正文 |
| --- | --- | --- | --- |
| R711-01/02 | D711-01/02 | T711-01/02 | 三层 current/knowledge-maintenance.md；根/current发现入口 |
| R711-03 | D711-01/02/04 | T711-02/04 | 同能力正文、必要 aliases、docs usage projection |
| R711-04/05 | D711-03 | T711-01/03/06 | 同能力原晋升/整合合同 |
| R711-06 | D711-01/05 | T711-02/05 | canonical共同方法；原Architecture contribution |
| R711-07 | D711-04 | T711-04 | MIGRATION-711；根历史/未迁移区 |
| R711-08 | D711-05 | T711-05/06 | canonical/spec/README引用；原 tools owner 安装结果 |

## 旧导航逐项 aliases

每行对应原 current/README 的一个条目。缺失 alias 只加入原所属完整单元，未缺失者保原字节；所有行为正文继续保留。表内是本次迁移核对，不建立共享逐项登记。

| 原完整正文 target | 旧 identity/alias | 本次补齐 |
| --- | --- | --- |
| `docs/requirements/current/codex-skill-distribution.md` | RDT-REQ-CODEX-DISCOVERY; R724/D724/T724; Codex Skill共享目录 | R724/D724/T724；Codex Skill共享目录 |
| `docs/requirements/current/review-sufficiency.md` | RDT-REQ-REVIEW-SUFFICIENCY; R717/D717/T717; 审核充分性 | R717/D717/T717 |
| `docs/requirements/current/requirement-decisions.md` | RDT-REQ-DECISIONS; R-DEC/BEH-DEC; 需求歧义探索与分级确认 | R-DEC/BEH-DEC |
| `docs/requirements/current/local-fix-intake.md` | RDT-REQ-LOCAL-FIX-INTAKE; R692/BEH692; 局部修复 Intake 与诊断 | R692/BEH692；局部修复 Intake 与诊断 |
| `docs/requirements/current/json-input-carriers.md` | RDT-REQ-JSON-INPUT; R695/BEH695; JSON 输入载体 | R695/BEH695 |
| `docs/requirements/current/task-delivery-lifecycle.md` | RDT-REQ-LIFECYCLE; Task/Delivery; BEH-001..006; R531-01..05/08; R636/BEH636; R637/BEH637 | R531-01..05/08；R636/BEH636；R637/BEH637 |
| `docs/requirements/current/completion-closure.md` | RDT-REQ-COMPLETION; Completion/Closure/Finish; R531-06; R547 | 已在原正文，未为alias复制 |
| `docs/requirements/current/knowledge-maintenance.md` | RDT-REQ-KNOWLEDGE; RDT/Architecture; REQ-007/BEH-007; R331 | REQ-007/BEH-007 |
| `docs/requirements/current/native-compatibility.md` | RDT-REQ-NATIVE; R630/BEH630; 三系统兼容 | RDT-REQ-NATIVE；R630/BEH630；三系统兼容 |
| `docs/requirements/current/runtime-location.md` | RDT-REQ-RUNTIME-LOCATION; R718/D718/T718; runtime与Git来源 | R718/D718/T718；runtime与Git来源 |
| `docs/design/current/codex-skill-distribution.md` | RDT-DES-CODEX-DISCOVERY; R724/D724/T724; Codex Skill共享目录 | R724/D724/T724；Codex Skill共享目录 |
| `docs/design/current/review-sufficiency.md` | RDT-DES-REVIEW-SUFFICIENCY; R717/D717/T717; 审核充分性 | R717/D717/T717 |
| `docs/design/current/requirement-decisions.md` | RDT-DES-DECISIONS; D-DEC/CON-DEC; 需求歧义探索与分级确认 | D-DEC/CON-DEC；需求歧义探索与分级确认 |
| `docs/design/current/local-fix-intake.md` | RDT-DES-LOCAL-FIX-INTAKE; D692/CON692; 局部修复 Intake 与诊断 | 局部修复 Intake 与诊断 |
| `docs/design/current/json-input-carriers.md` | RDT-DES-JSON-INPUT; R695/BEH695; JSON 输入载体 | R695/BEH695 |
| `docs/design/current/task-delivery-lifecycle.md` | RDT-DES-LIFECYCLE; Task/Delivery; BEH-001..006; R531-01..05/08; R636/BEH636; R637/BEH637 | BEH-001..006；R531-01..05/08；R636/BEH636；R637/BEH637 |
| `docs/design/current/completion-closure.md` | RDT-DES-COMPLETION; Completion/Closure/Finish; R531-06; R547 | R531-06；R547 |
| `docs/design/current/knowledge-maintenance.md` | RDT-DES-KNOWLEDGE; RDT/Architecture; REQ-007/BEH-007; R331 | REQ-007/BEH-007；R331 |
| `docs/design/current/native-compatibility.md` | RDT-DES-NATIVE; R630/BEH630; 三系统兼容 | RDT-DES-NATIVE；R630/BEH630 |
| `docs/design/current/runtime-location.md` | RDT-DES-RUNTIME-LOCATION; R718/D718/T718; runtime与Git来源 | R718/D718/T718；runtime与Git来源 |
| `docs/test/current/codex-skill-distribution.md` | RDT-TST-CODEX-DISCOVERY; R724/D724/T724; Codex Skill共享目录 | R724/D724/T724；Codex Skill共享目录 |
| `docs/test/current/review-sufficiency.md` | RDT-TST-REVIEW-SUFFICIENCY; R717/D717/T717; 审核充分性 | R717/D717/T717 |
| `docs/test/current/requirement-decisions.md` | RDT-TST-DECISIONS; T-DEC/SC-DEC; 需求歧义探索与分级确认 | T-DEC/SC-DEC；需求歧义探索与分级确认 |
| `docs/test/current/local-fix-intake.md` | RDT-TST-LOCAL-FIX-INTAKE; T692/SC692; 局部修复 Intake 与诊断 | 局部修复 Intake 与诊断 |
| `docs/test/current/json-input-carriers.md` | RDT-TST-JSON-INPUT; R695/BEH695; JSON 输入载体 | R695/BEH695 |
| `docs/test/current/task-delivery-lifecycle.md` | RDT-TST-LIFECYCLE; Task/Delivery; BEH-001..006; R531-01..05/08; R636/BEH636; R637/BEH637 | BEH-001..006；R531-01..05/08；R636/BEH636；R637/BEH637 |
| `docs/test/current/completion-closure.md` | RDT-TST-COMPLETION; Completion/Closure/Finish; R531-06; R547 | 已在原正文，未为alias复制 |
| `docs/test/current/knowledge-maintenance.md` | RDT-TST-KNOWLEDGE; RDT/Architecture; REQ-007/BEH-007; R331 | RDT/Architecture；REQ-007/BEH-007 |
| `docs/test/current/native-compatibility.md` | RDT-TST-NATIVE; R630/BEH630; 三系统兼容 | RDT-TST-NATIVE；R630/BEH630；三系统兼容 |
| `docs/test/current/runtime-location.md` | RDT-TST-RUNTIME-LOCATION; R718/D718/T718; runtime与Git来源 | R718/D718/T718；runtime与Git来源 |

## 状态与关系边界

原维护 owner 为 guru-maintain-requirements-design-test-ssot；Architecture 原 owner 保独立 authority 与最终写入。RDT 三层根的 guru-trellis-rdt/active、各层 current identity 与全部历史/legacy rows 保留。结构变化只补缺失定位元信息，不将 target/inferred/unpromoted 改为已实现。任何最终集成的真实 target 差额仍由原 owner 重读并整合，不能从本表推导语义 pass。

候选 Check 前只写隔离 proposed。manifest 的 project projection 仅指 docs usage；Architecture baseline-usage 及根/治理的完整拟写由对应 Architecture owner 提供并纳入整体 candidate。缺失实际 Agent/安装结果仍待原测试 owners，不以本表或链接存在代替验证。
