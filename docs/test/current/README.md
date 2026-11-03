# 当前知识发现入口

本层属于 `guru-trellis-rdt` / active；状态与历史边界从 [根入口](../README.md) 读取。采用 `knowledge-navigation-1`，能力完整正文位于本目录 `**/*.md`，多文件能力可有自身目录的局部 README。本页不维护逐单元清单。

1. 原 owner 先选择问题、Task、阶段与候选适用的版本。运行 `rg --files docs/test/current` 定位范围，再用 `rg -n '<稳定ID、别名或概念>' docs/test/current` 限定检索。
2. 实际读取命中完整单元，核稳定身份/aliases、状态、适用来源、原 owner 晋升依据和替代范围，再展开回答所需 R/D/T/Architecture 关系。目录、标题、搜索排名、日期或更大版本不产生 authority。
3. current、accepted target、未晋升 contribution/proposed、历史与 superseded 分开。贡献/历史只用于来源或未迁移边界，晋升后的普通查询不拼贡献链。断链、缺来源/晋升依据或重复 current 返回原 repair/澄清，保留最后可读 authority。

新增或修改独立主题只维护所属完整正文、局部导航与真实关系，不在本页追加条目。既有能力沿原正文整合，不创建每 Issue 第二 current。改名保稳定 ID；替换/删除保前驱/后继、仍有效引用及旧引用意义。真实关系重叠由原 owner 整合，不复制关系规避。

## 历史与未迁移范围

| Legacy scope identity | Status | Locator | Relations |
| --- | --- | --- | --- |
| RDT109-LEGACY; 未列入迁移关系的身份/范围 | legacy_unmigrated | [immutable .109](../versions/current-main-0.6.17-guru.109/test-strategy.md) | [migration inventory](../../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md) |
| RDT109-PINNED-TASK; 固定旧阶段适用来源 | historical_applicable | [immutable .109](../versions/current-main-0.6.17-guru.109/test-strategy.md) | Git bdb5185c673c91b2fb5cfc66ffbb33849904a69c |
