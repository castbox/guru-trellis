# #717 Architecture 隔离贡献

TaskId：`717-review-sufficiency`；generation：0；Delivery：`a55b1bd3-718a-42aa-a77a-dc9387abc2b9`。状态：`proposed`，Planning 尚未晋升。

## Authority 与实际差额

适用 source 为 `404c841e9ca917b4680831aa0becd2e26d72fa0c`，baseline 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`，change-contract 为 `guru-trellis-architecture-change-contract-v1`。独立 candidate_assessment 选择 `architecture_impact / target_native`，decision refs：ARCH-FND-002、ARCH-GOV-012、ADR-034。

改变共同规则唯一 owner 和读取方向；不改公共 API、状态、writer 或阶段出口。现有 shared review-method→Check/Branch→review-method 互读，目标为原 reviewer→共同 managed spec，工程组合不再读阶段私有方法。保留专题 owner 及原阶段完整条件。

## 完整拟写 targets

在相邻 `717-review-sufficiency/proposed/` 下保留以下完整结果，直接由原 Architecture owner 在 candidate Check 后 final_integration 消费：

- `docs/architecture/03-domains/review-sufficiency.md`：新的完整 owner/依赖单元，正文引用唯一规则源。
- `docs/architecture/adr/review-sufficiency.md`：必要 ADR，明确替代范围、代价、旧路径退出和重审触发。
- `docs/architecture/README.md`：仅增加新单元的必要导航，不改 baseline identity。
- `docs/architecture/adr/README.md`：仅增加必要 ADR 导航。

## 九项 concerns

| Concern | 适用性与承接 |
| --- | --- |
| authority-binding | applicable；使用当前 Planning 3.0、后继 nonplanning 5.0/Delivery3.0 与固定 before authority，不用 proposed 自证 |
| constitution-binding | applicable；实际权衡唯一规则、职责隔离与最小状态，不复制原则或评分 |
| boundary-and-decision | applicable；共同规则 owner/依赖变化，target_native；ADR-REVIEW-SUFFICIENCY 记录取舍 |
| owner-and-single-writer | applicable；共同 spec 由唯一源维护，原审核 owner 判断；shared current 仍由原 Architecture owner 晋升 |
| compatibility-and-exit | applicable；旧共同正文在同批删除改引用，原 API/出口和历史适用版本保持，无新增双读 |
| gap-and-deviation | applicable；关闭本项方法互读与并行定义差额，不宣称其它历史 GAP 已关闭或所有审核缺陷已修复 |
| parallel-scope | applicable；仅本 Task 隔离 contribution/proposed 与 canonical 实现；其它 Task/共享 current 写入保留原 owner |
| evidence-and-freshness | applicable；当前 design、实际候选、old/new native 观察与安装分开；真实结果仍待执行 |
| review-and-promotion | applicable；独立 phase2 与 candidate Check 先审完整拟写，原 owner final_integration 读前像、写入/读回，随后实际 candidate 重绑并 final Check/完整 committed Review |

## 验证、晋升与限制

真实 Agent、机械检查、安装和 Release 边界按本批 design 第8节。此贡献不是通过声明或验证结果。晋升前所有 current targets 保持原样；原 owner 固定真实 target 并比较 expected-current，保留其它已生效变化。无新增锁、调度器、状态机或授权记录。具体迁移表留本批设计/验证位置，不把消费者列表写成长期 authority。
