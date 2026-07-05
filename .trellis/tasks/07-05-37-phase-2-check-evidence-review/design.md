# #37 详细设计

## 设计目标

把 Phase 2 check evidence 的提交后校验从“只允许 metadata-only tail”改成“允许已被提交前 `dirty_paths` 覆盖的 task work commit”，同时保持 Review Gate 对未检查变更和工作区 dirty state 的 fail-closed 行为。

## 修改边界

- Canonical helper：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Canonical tests：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
- Canonical workflow/docs：`trellis/workflows/guru-team/workflow.md`、`trellis/workflows/guru-team/README.md`、`docs/requirements/requirement-main.md`。
- Preset overlay / platform entry：`trellis/presets/guru-team/overlays/` 下的 `trellis-continue` 文案，以及 dogfood installed copies。
- Dogfood runtime copies：`.trellis/guru-team/scripts/python/guru_team_trellis.py`、`.trellis/workflow.md`、`.agents/skills/trellis-continue/SKILL.md`、`.codex/prompts/trellis-continue.md`、`.codex/skills/trellis-continue/SKILL.md`。

## 核心算法

新增或改造一个可测试 helper，例如 `committed_paths_match_phase2_dirty_paths(root, recorded_head, recorded_dirty_paths)`：

1. 用 `git diff --name-only <recorded_head>..HEAD` 取得 Phase 2 check 记录后进入当前 `HEAD` 的提交路径。
2. 将路径分成 Trellis metadata 与 non-metadata：
   - metadata 继续使用现有 `METADATA_ONLY_PREFIXES` / `METADATA_ONLY_FILES`。
   - non-metadata 是代码、workflow、docs、tests、config、script、schema 等 task work。
3. 校验每个 non-metadata committed path 都存在于 `phase2-check.json.dirty_paths`。
4. 校验当前 working tree 不存在 non-metadata dirty paths；若存在则阻断。
5. 若提交范围中有未覆盖的 non-metadata paths，返回阻断错误，并输出未覆盖路径。

## `validate_phase2_check` 语义

- `recorded_head == current HEAD`：保持现有 dirty paths 与当前 working tree 一致性校验。
- `recorded_head != current HEAD` 且 `allow_committed_head=True` 且 recorded head 是当前 `HEAD` 祖先：
  - 不再要求提交 tail 只能是 metadata。
  - 允许 non-metadata committed paths，只要它们全部来自记录时的 `dirty_paths`。
  - 仍然要求当前 working tree 无 non-metadata dirty paths。
  - 仍然执行 digest、coverage、validation、findings 校验。
- 其他 HEAD 不一致情况：继续阻断。

## 文案同步

Workflow / entrypoint 文案需要表达给 AI 的判断规则：

- Phase 2 check 在 commit 前完成并记录当时 dirty paths。
- Phase 3.5 的 post-commit audit 会证明提交没有超出这些 dirty paths。
- commit 后不要为了让 `phase2-check.json.head` 匹配而重录 Phase 2 evidence；只有提交后新增未检查的非 metadata 变更或 artifact digest 失效时才回到 Phase 2。

## Durable Docs

更新 `docs/requirements/requirement-main.md` 第 3 章中的 Phase 2 check gate / metadata tail 描述，记录新的 post-commit audit 语义。

## 兼容性与风险

- 兼容旧 artifact：旧 `phase2-check.json` 已包含 `dirty_paths`，缺失时现有校验已经阻断。
- 风险点：路径匹配必须用仓库相对路径，不能因为 `...` merge-base diff 或 `..` direct range 误把 base 变化纳入检查。此处使用 issue 指定的 `<recorded_head>..HEAD` 更贴近“Phase 2 记录后新增提交”的语义。
- 安全风险：不涉及 secrets、环境变量、凭据或外部数据。
- 部署影响：不涉及服务、容器、K8s、DB migration 或 Makefile 运行入口；属于 workflow helper 与文档变更。

## 回滚策略

若验证发现新 helper 误放行未检查变更，回滚 Python helper 和对应测试/文案到 metadata-only tail 逻辑；但发布前必须重新评估 issue #37 是否仍阻塞正常流程。
