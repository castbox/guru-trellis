# 当前知识读写与晋升测试策略

知识单元：`RDT-TST-KNOWLEDGE`。状态：`current`。固定前驱 RDT `.109` / Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。需求：[RDT-REQ-KNOWLEDGE](../../requirements/current/knowledge-maintenance.md)；设计：[RDT-DES-KNOWLEDGE](../../design/current/knowledge-maintenance.md)。保留 `TST-006 / SCN-006` 三层SSOT、`TST-018/023/024` 的Architecture/并行/晋升关系；旧无条件stale与旧首次晋升顺序以ADR-028/030为后继。

## T331-01..06 与稳定关系

| Test / scenario | Requirement → design | 正常输入、观察与预期 |
| --- | --- | --- |
| T331-01 / V331-A / S331-01/02 | R331-01/04 → D331-01/04 | 从正常入口查询多轮Task/Delivery和后继Architecture规则；完整定义、条件/否定/顺序/替代范围正确可追溯。不能只答摘要或沿日期取最新。历史拼接查询的三次中位文档字节与历史拼接步骤须下降。 |
| T331-02 / V331-B / S331-03/04 | R331-02 → D331-02 | 为Completion插入独立知识条目、拆出Closure不等Finish；受影响R/D/T一致，原ID/前后继/无关ID不变，判断Architecture实际影响，不改API或旧snapshot。每次正确；中位历史拼接或无关维护减少。 |
| T331-03 / V331-C / S331-05/07/08 | R331-02/05 → D331-02/04/05 | 两Task隔离delta依次受控promotion，完整current保留两增量及原全部约束；旧Task仍读B适用authority，新查询按successor。每次正确，晋升后查询的历史拼接减少；兼容子项不强求节省。 |
| T331-04 / V331-D / S331-06/09 | R331-01/03/05 → D331-01/03/05 | 实际generic source/version与project差异；只改project，另给普通source缺失/断链/迁移未完。明确owner/影响/原repair，保留旧源，不将target/inferred当current。语义等价旧新fixture、每次正确，不强求兼容收益。 |
| T331-05 / V331-E | R331-02/04/05 → D331-02/04/05 | 逐条来源迁移inventory、稳定trace、否定/例外/顺序/被替代范围、legacy区；focused tests及package/source检查、Markdown引用、历史字节核对。AI判完整性，机械命令仅其实际证据。 |
| T331-06 / V331-F | R331-04/05 → D331-05 | canonical/dogfood/installed分发、完整apply/drift；一个clean代表安装和旧匹配update/reapply。实际references可读、平台投影/modes一致、用户内容保留、sidecars逐项处置。不等完整Release矩阵或业务采用。 |

R331-06 / D331-06 是上述真实对照方法与结果责任，横切 T331-01..06。完整样本/必答事实/条件/修订范围与次数在实施前的Delivery design第8节已冻结。old/new同语义、预期、模型配置、权限及正常起点；各组各3次独立native Codex，共24次。query read-only、revision workspace-write，双方一致。测试owner的期待表不注入受测Agent，另一侧答案/历史不共享。样本/环境改变则说明原因并双方同口径重跑。

## 成本、错误与证据层次

每次保留repo外临时raw JSON events、实际命令/路径/工具输出字节、最终答案、文件改动与usage。AI逐次判断正确完整，并按navigation、必要正文、重复和无关history分类。总input包含公共注入，cached_input单列，不扣除伪造节省；注入/读取指令也算成本。读取步数和维护paths实报，首次人工迁移/导航维护成本另报，无自动生成器也不能记为零维护。

完整查询正确性先于成本；错误、省略条件或失效引用不能以低token/字节补偿。保留首次失败、修复和未覆盖范围，不以最后retry掩盖失败。legacy范围不全迁移不是当前能力完整性通过依据；若所选能力缺约束，仍须修复。

工程检查按当前package及验证作用域选择。原 `T600` before/after/promotion、`T578` 工程事实适用性和 `TST-006` 三层关系继续，但历史绿色不自动成为本候选结果。真实Agent行为与deterministic/source/installed/live证据分开；去敏两层fixture不证明外部业务采用，完整多平台Release由专门scope拥有。

## 唯一实际结果与缺口

全部24次及迁移/安装实际结果、分类/中位成本、首次失败/修复和限制只由 [#331 test.md](../../requirements-design-test-contributions/331-current-effective-knowledge/test.md) 拥有；当前正文不复制summary为第二结果authority。尚未执行项保持未验证，缺source/安装依赖时沿原repair/blocked，不能用目录/schema/链接成功宣称行为通过。
