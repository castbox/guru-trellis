# #83 设计：planning artifact ambiguity review gate

## 设计目标

把 ambiguity review 做成 Guru Team Phase 1 planning gate 的正式合同：AI 负责语义判断，companion script 只记录和校验结构化证据。实现必须保持官方 Trellis 扩展方式：Markdown workflow / skill / prompt / agent overlay 承载流程判断，Python / shell 只承担 recorder / validator 职责。

## 设计依据

- Trellis 官方 `custom-workflow.md`：workflow 行为由 `.trellis/workflow.md` Markdown 控制，phase、skill routing、workflow-state 均由 AI 运行时读取。
- Trellis 官方 `custom-spec-template-marketplace.md`：spec template marketplace 用于复用工程约定，不用于 active task state。
- 本仓库 `AGENTS.md`：Markdown 定义流程，脚本执行事实；语义判断不得放进 Python / shell。
- `.trellis/spec/workflow/*`：workflow 改动必须同步 canonical、dogfood、overlay、docs、tests。

## 边界

### Markdown / AI 判断层

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/**`
- dogfood `.agents/skills/**`、`.codex/prompts/**`、`.codex/skills/**`
- durable docs / specs

这些文件必须定义 ambiguity review 的判断口径、审查维度、受控词表、引用豁免、planning stop 条件、post-planning confirmation 条件。

### Recorder / Validator 层

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- thin bash wrappers
- unit tests

脚本必须只校验结构化字段存在、状态值、受控词表字段、digest freshness。脚本不得判断需求是否弱化、设计是否冲突、引用是否误导。

## `planning-approval.json` 数据合同

Schema version 升级为 `1.2`。新 artifact 必须包含：

```json
{
  "ambiguity_review": {
    "status": "passed",
    "reviewer": "codex-main-session",
    "summary": "中文 ambiguity review 结论",
    "normative_language": {
      "controlled_terms": ["可以", "允许", "建议", "尽量", "视情况", "类似", "相关", "等"],
      "unchecked_normative_hits": []
    },
    "checked_dimensions": {
      "no_requirement_weakening": true,
      "source_issue_semantics_preserved": true,
      "conditional_paths_have_conditions": true,
      "no_parallel_implementation_paths": true,
      "gates_have_machine_verifiable_conditions": true,
      "acceptance_criteria_are_deterministic": true,
      "external_quotes_are_labeled_non_contract": true
    }
  }
}
```

Validation rules:

- `status` 必须为 `passed`。
- `reviewer`、`summary` 必须非空。
- `controlled_terms` 必须包含完整受控弱约束词表。
- `unchecked_normative_hits` 必须是数组，且通过状态下必须为空。
- `checked_dimensions` 必须包含全部七个维度，且值必须为 `true`。
- 旧 `schema_version=1.1` artifact 必须 fail closed，触发重新展示三份 planning docs 并取得用户确认。

CLI interface:

```bash
.trellis/guru-team/scripts/bash/record-planning-approval.sh --json \
  --reviewer "codex-main-session" \
  --summary "中文规划审查结论" \
  --ambiguity-reviewer "codex-main-session" \
  --ambiguity-summary "中文 ambiguity review 结论" \
  --ambiguity-status passed \
  --user-confirmation "用户在看到 prd.md、design.md、implement.md 三个链接后确认进入实现" \
  --confirmation-source explicit-post-planning-review
```

`record-planning-approval` 默认使用完整受控词表和全部维度；调用方只提供 AI 审查身份与 summary。若未来加入词表扫描，扫描输出只能写入 `unchecked_normative_hits` 作为辅助事实，非空时必须阻塞。

## Workflow 改动

Phase 1.4 必须新增以下顺序：

1. 完成 `prd.md` / `design.md` / `implement.md` 与 Docs SSOT Plan。
2. 主会话执行 ambiguity review。
3. 审查通过后运行 human artifact resolver。
4. 展示三份 planning docs 链接。
5. 取得用户 explicit post-planning confirmation。
6. Phase 1.5 写入 `planning-approval.json`，其中包含 `ambiguity_review`。

Planning artifacts section 必须说明：

- 规范性条款不得无条件使用受控弱约束词表。
- 外部引用、历史记录、风险说明中的弱约束词必须标注来源，且不作为执行合同。
- 脚本扫描只能作为辅助 evidence。

## Overlay 同步设计

需要修改 canonical overlay 后同步 dogfood 副本：

- `trellis/presets/guru-team/overlays/.agents/skills/trellis-brainstorm/SKILL.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-before-dev/SKILL.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
- `.codex/prompts/trellis-continue.md`
- `.codex/skills/trellis-continue/SKILL.md`
- implementation / check agent overlays where they consume planning approval

Overlay 原则：只写短入口约束，并指回 `.trellis/workflow.md`；不得在每个平台复制完整审查说明。

## Docs SSOT Plan

- Docs state: `complete_docs`
- Strategy: `ssot_first`
- Reason: 本任务改变长期 workflow / gate / data contract，durable docs 和 specs 必须先更新，task artifact 只保留执行 delta 与证据。
- Affected durable docs:
  - `docs/requirements/guru-team-trellis-flow.md`
  - `docs/requirements/requirement-main.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
- Task artifact deltas to merge:
  - ambiguity review definition；
  -受控弱约束词表；
  - `planning-approval.json` 1.2 contract；
  - script boundary；
  - validation plan。
- Merge checkpoint: Phase 2 implementation 完成前，durable docs/specs 必须已更新并通过 Phase 2 check。

## 兼容性与迁移

- 旧 `planning-approval.json` 1.1 在新 workflow 下不得放行实现；用户需要重新 review 三份 planning docs。
- `record-planning-approval` CLI 增加新 flags，但旧调用缺少 ambiguity summary 时必须 fail closed。
- installed target repos 通过 preset installer 获取新 script 与 overlay；dogfood copy 通过 `apply.sh --repo .` 同步。

## 部署与安全影响

- 不涉及服务部署、容器、Kubernetes、数据库 migration、Makefile。
- 不读取或写入 secret、token、`.env`、签名 URL。
- GitHub 操作仍由现有 `gh` preflight 和 publish gate 控制。

## 回滚

- 回滚代码与 docs 即可恢复 1.1 planning approval 合同。
- 若 target repo 已生成 1.2 planning approval artifact，旧脚本把新增字段当作额外 JSON 字段处理；回滚后仍需按旧 workflow 重新确认 planning。
