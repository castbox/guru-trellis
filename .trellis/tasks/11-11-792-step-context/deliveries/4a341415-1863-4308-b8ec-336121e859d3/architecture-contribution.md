# #792 按步骤加载与出口查询：Architecture 隔离贡献

状态：planning candidate，尚未晋升。Task为792-step-context/generation 0，D1为4a341415-1863-4308-b8ec-336121e859d3。直接来源为[Issue #792](https://github.com/castbox/guru-trellis/issues/792)。本文件与[design](design.md)构成真实方案候选，不证明实现或安装通过。

## Authority与问题

当前baseline为guru-trellis-architecture，constitution为guru-trellis-design-constitution-v1，采用当前change-contract；ADR-035保留唯一continuation、实际公共current及原producer恢复。现有全量graph、conditional router和历史正文集中在正常必读范围，而discovery只按Skill查询合同。直接影响ARCH-FND-001/002、ARCH-DOM-016/038、ARCH-GOV-012。

## 采用决定及边界

采用target_native：一个workflow-owned Markdown reference拥有完整graph和router/stop正文；原Interface拥有各Skill出口/consumer及public contracts，现有校验继续确保两者一致。原discovery以Skill+exit显式查询，确定性返回唯一consumer、其直接输入/投影及入口前置。条件理解、route intent和充分性仍归原AI owner。

现有native phase/step和唯一continuation通过正文组织按当前步骤定位；不改upstream extractor/hook，不新增状态、缓存、ledger、wrapper或授权记录。legacy详情由原维护owner实际入口加载，原支持/准确来源和历史字节保持。preset/tools owner分发matching引用和runtime，直接compatibility reader及preview显式读取matching assets。正常新runtime和查询直接采用reference-only。仅verifier自身保留原before-snapshot的inline只读观察输入；新candidate preview用显式matching reference。该分支不产生当前runtime资格，verifier owner在受支持before样本退出inline后删除它及用例。

必要新ADR候选为[adr-step-context.md](adr-step-context.md)。它补充ADR-035的加载与分发决定，不改变其身份、阶段、原producer和scope两次承接。公共Skill/exit/schema/consumer保持；新增CLI选项保留无出口查询。MIGRATION-792明确完整matching采用，混装停止由原tools owner恢复，无Task状态迁移。

## 适用原则与原九concern承接

实际命中的constitution refs为 `mature-practice-applicability`（复用官方Markdown/preset/native扩展面）、`concept-semantic-completeness`（唯一consumer与完整条件可取得）、`cohesion-change-isolation`（原AI/runtime/安装/晋升owner保持）、`minimum-necessary-complexity`（只增当前查询所需投影，正常runtime无旧格式双读）、`debt-one-way-convergence`（原全表只有一份，旧历史观察不恢复当前authority）。这些是当前变化的具体承接，不重新定义五原则或评分。

| 原concern | 适用性与理由及实际落点 |
| --- | --- |
| authority-binding | applicable；planning purpose 3.0、实际D1、baseline/change-contract和单一候选由design §1绑定，原owner正式输出决定可否接续。 |
| constitution-binding | applicable；current constitution身份见design §1，命中refs及具体作用见本节，不用另一组原则替换。 |
| boundary-and-decision | applicable；#792、ADR-035、ARCH-FND-001/002、ARCH-DOM-016/038、ARCH-GOV-012对应design §3/4，唯一target_native，不改变原AI owner。 |
| owner-and-single-writer | applicable；workflow写全局图、Interface写Skill合同、runtime提取、tools安装；Author只写当前规划，原Architecture/RDT在final_integration分别晋升。 |
| compatibility-and-exit | applicable；CLI无exit原功能保持，新runtime直接reference-only，无新legacy层；verifier原before观察限定只读输入及明确owner/删除条件；MIGRATION-792整体更新且无Task迁移。 |
| gap-and-deviation | applicable；当前全量必读和出口查询缺口由I1/I2消除，未建立新GAP或豁免其他已知边界；V1–V6未执行，不声称关闭或生产效果。 |
| parallel-scope | applicable；只写本D1隔离规划/贡献和本Task产品候选，不写其他Task、共享journal或争抢共享authority；晋升前由原owner核live目标。 |
| evidence-and-freshness | applicable；固定B/H0见design §1，实际design由本次原invoke绑定；V1–V6分别声明source/installed/Agent边界，当前仅方案，实施后绑定实际完整candidate。 |
| review-and-promotion | applicable；真实本贡献及ADR候选进入final_plan；完整实现与全部拟写在candidate Check后才由原owner final_integration晋升，实际after再进入最终Check/committed Review。 |

本次project-check消费上述真实单图、原owner、直接演进与最小状态判断；没有服务/DB或业务安全边界扩张。平台影响是受管定位/分发，source parity不能证明实际Agent行为。

## 拟晋升与验证限制

拟晋升至docs/architecture/contributions/792-step-context.md及docs/architecture/adr/step-context-loading.md；baseline必要投影由原owner核live完整单元后确定。原RDT owner维护独立requirement/design/test完整贡献。实现及隔离完整知识候选通过独立Architecture和candidate Check后，原owner在final_integration晋升，再将实际写入纳入rebound最终Check/完整Branch Review。规划不写共享导航。

计划V1–V6覆盖公开查询、普通错误/演进、native提取、legacy可达、reader/分发及实际AI消费；当前均尚未执行。本候选不声称安装、生产、成本改善、全平台兼容或Release矩阵通过。最终证据补齐和实际共享目标写前复核仍为原owner责任。
