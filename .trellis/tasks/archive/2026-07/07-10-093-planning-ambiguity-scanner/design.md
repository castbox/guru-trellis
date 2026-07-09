# #93 设计：planning ambiguity scanner 与分类 gate

## 设计目标

在不把语义 review 下沉到脚本的前提下，给 planning approval 增加可审计正文扫描链路。脚本只负责扫描固定词表、接收 AI 已分类命中、校验结构和一致性；AI 仍负责判断命中是否已经改写为确定性合同，或是否属于可允许分类。

## 架构边界

### Markdown / AI 判断层

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/**`
- dogfood `.agents/skills/**`、`.codex/prompts/**`、`.codex/skills/**`
- durable docs / specs

这些文件定义词表、分类集合、分类规则、AI ambiguity review 责任、planning stop 条件和 post-planning confirmation 条件。

### Recorder / Validator 层

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- thin bash wrappers
- unit tests

这些文件只能执行确定性动作：读取三份 planning artifacts、逐行匹配固定词表、接收 CLI 传入的分类、校验必填字段、校验 artifact 与重新扫描结果一致、在未分类或 violation 时阻塞。

## 数据合同

`planning-approval.json` 继续使用 `schema_version=1.2`，扩展 `ambiguity_review.normative_language`：

```json
{
  "controlled_terms": ["..."],
  "scan_scope": ["prd.md", "design.md", "implement.md"],
  "hits": [
    {
      "path": ".trellis/tasks/<task>/design.md",
      "line": 12,
      "term": "推荐",
      "text": "...",
      "classification": "contract_violation",
      "reason": "规范性设计合同使用受控词且缺少确定性触发条件"
    }
  ],
  "unchecked_normative_hits": []
}
```

合同规则：

- `controlled_terms` 等于 v2 词表。
- `scan_scope` 固定为 `["prd.md", "design.md", "implement.md"]`。
- `hits[]` 记录全部扫描命中。
- `unchecked_normative_hits[]` 只记录未分类命中和 `contract_violation` 命中。
- 允许分类命中必须包含非空 `reason`。
- `contract_violation` 出现在 `hits[]` 时，`unchecked_normative_hits[]` 必须非空，planning approval 必须失败。

## CLI 设计

新增或扩展 `record-planning-approval` 参数：

```bash
--normative-hit "path|line|term|classification|reason"
```

解析规则：

- `path` 必须指向当前 task 的 `prd.md`、`design.md`、`implement.md` 之一。
- `line` 必须是正整数，并且该行必须包含 `term`。
- `term` 必须属于 v2 词表。
- `classification` 为空时视为未分类命中。
- `classification` 非空时必须属于分类白名单。
- `reason` 对允许分类必须非空。

未通过 `--normative-hit` 分类的扫描命中由 recorder 自动写入 `hits[]`，并以空分类与空理由进入 `unchecked_normative_hits[]`。这样脚本能 fail closed，但不替 AI 选择分类。

`check-planning-approval` 不接收分类输入；它重新扫描三份文件，并验证 artifact 中保存的 `hits[]` 与当前扫描命中完全一致。若 planning artifact 正文变化、词表变化、分类字段被手工删改或当前文件新增未分类命中，validator 必须 fail closed。

## Scanner 设计

- 扫描单位：UTF-8 文本行。
- 命中策略：每个受控词在同一行出现一次以上时记录一条 `{path,line,term,text}` 命中；同一行多个不同词分别记录。
- 词表顺序：按 `PLANNING_AMBIGUITY_CONTROLLED_TERMS` 顺序输出，保证 artifact 稳定。
- 路径：写入 repo-relative task-local 路径。
- 行号：1-based。
- text：保留整行去除尾部换行，不截断；scanner 不读取 secret 文件，扫描范围固定为 task planning docs。

## Docs SSOT Plan

- Docs state: `complete_docs`
- Strategy: `ssot_first`
- Reason: 本任务改变长期 workflow gate、data contract、companion script 行为和 platform overlay 文案，durable docs / specs 必须作为长期 SSOT。
- Affected durable docs:
  - `docs/requirements/guru-team-trellis-flow.md`
  - `docs/requirements/requirement-main.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
- Task delta merge: v2 词表、分类集合、正文扫描合同、recorder/validator 边界、测试矩阵写回 durable docs / specs。
- Task history only: issue intake、调试输出、临时验证失败原因。
- Merge checkpoint: Phase 2 check 前完成 durable docs / specs 同步；Branch Review Gate 复核 docs sync 结果。

## Overlay 同步设计

Canonical overlay 更新后运行：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

覆盖范围：

- `.agents/skills/trellis-brainstorm`
- `.agents/skills/trellis-continue`
- `.agents/skills/trellis-before-dev`
- `.agents/skills/trellis-check`
- `.codex/prompts/trellis-continue`
- `.codex/skills/trellis-continue`
- `.codex/agents/trellis-implement`
- `.codex/agents/trellis-check`
- Claude / Cursor 对应 command、skill、agent overlay
- `.trellis/agents/implement.md`
- `.trellis/agents/check.md`

## 自举兼容性

本任务会修改 `check-planning-approval` 自身。当前 task 在进入实现前会先按现有脚本记录 planning approval。实现 scanner 后，若三份 planning artifacts 内容未变化，主会话必须使用已经展示并取得确认的同一规划内容重新记录新版 `planning-approval.json` evidence；若任一 planning artifact 内容变化，主会话必须重新展示三份链接并取得 fresh post-planning confirmation。

## 风险与缓解

- 风险：脚本变成语义 reviewer。缓解：脚本只接收分类并校验结构，不自动判断分类正确性。
- 风险：词表在 docs、workflow、scripts、overlay 间漂移。缓解：单测断言 canonical 和 dogfood 常量一致，并增加词表一致性测试。
- 风险：planning artifact 中词表定义自身触发 scanner。缓解：AI 必须给定义行传入 `term_definition` 分类和理由；scanner 只验证分类结构。
- 风险：overlay 更新遗漏。缓解：运行 preset apply 和 dogfood drift check。
- 风险：开箱即用验证耗时。缓解：优先运行本仓库 preset apply/drift、CLI help、targeted tests；无法完成 throwaway install 时在最终报告写明。

## 部署与安全影响

- 不涉及服务部署、容器、Kubernetes、数据库 migration、Makefile。
- 不读取 `.env`、token、private key、签名 URL 或客户数据。
- 扫描范围固定为当前 task 的三份 planning Markdown。

## 回滚

回滚 workflow、docs、overlay、script、test 改动即可恢复 #83 行为。已生成的新版 `planning-approval.json` 包含额外字段；旧脚本忽略额外字段，但重新进入实现仍需按当时 workflow gate 重新确认 planning。
