# 技术设计

## 架构

```text
canonical semantic-retrieval spec (versioned SSOT)
  -> preset installer / managed inventory
  -> dogfood installed spec
  -> semantic owner package contracts and Trellis agents reference the SSOT
  -> owner-local semantic evals prove coverage and negative-conclusion behavior
```

共享 spec 拥有概念族构造、exact literal 保留、查询最小化、evidence coverage、否定结论门槛和 artifact 禁令。每个 owner 只拥有“何时在自己的 gate 中应用该合同”以及自身既有结果/exit；不会形成新的共享执行 Skill 或 deterministic runtime。

## Canonical 与 Installed 边界

1. 先定位 preset 中现有 spec canonical source 与 installer managed inventory，新增一个稳定、版本化的合同文件。
2. 通过 preset `apply.sh --repo .` 生成/同步 dogfood installed copy；不手工把 dogfood 当唯一源头。
3. Guru package canonical source 中修改 R2 所列 `guru-*` Skill contract；由 installer 同步 `.trellis/guru-team/skills/packages/**` 和 Shared/Codex/Claude/Cursor discovery copies。
4. Trellis bundled/project agent canonical source按现有 ownership 模型修改，确保 research/implement/check/session-insight 的已声明分发路径一致。
5. `.trellis/workflow.md` 保持 thin orchestration，不写概念族规则。

## Owner 集成

每个 owner 使用同一个短引用合同：

- 进入实际 Docs/code/tests/history/duplicate/consumer 搜索前读取 semantic retrieval SSOT；
- 形成本轮概念族与最小查询集合；
- 在自己的 AI Gate 评估 coverage；
- 若声称“不存在”，显式满足双语、literal 与 legacy alias 门槛；
- 不将查询过程加入 public DTO 或 tracked artifact。

`guru-discover-change-context` 和 `guru-clarify-requirements` 在 Phase 0 搜索与 duplicate/repository-answerable question 中应用；`guru-check-task` 和 `guru-review-branch` 在完整实现/影响面检查中应用；Trellis research/implement/check/session-insight 在自己的资料、复用、consumer、测试和历史搜索中应用。

## Eval 设计

新增或扩展 semantic eval cases，fixture 以 evidence 与结论为断言，不模拟命令次数：

1. 中文 Docs `发布门禁` 与英文 code `release_gate` 指向同一机制。
2. 英文 Issue `stale context` 与中文 commit/历史会话 `上下文过期` 指向同一决定。
3. current `workspace mapping`、legacy alias `handoff map`、缩写与 literal `workspace_ref` 找到同一 consumer。
4. 只有英文或只有中文搜索后断言“不存在”时，Gate 必须阻塞。
5. exact error `OBJECT_ACCESS_DENIED` 和 symbol `reviewed_content_sha256` 保持原文，不生成翻译查询。
6. evidence 缺失、authority 变化、未知 dirty 内容继续沿现有 blocked/re-entry 路由。

eval 使用静态语义场景和 AI-owned expected result；deterministic runner 只校验 declared case、schema 与实际 exit，不依据 query 数量判定通过。

## Public API 与 Artifact

- 不新增或修改 public input/output DTO 字段。
- 不新增 runtime command、schema id、query digest 或 search-report artifact。
- 新 SSOT 的稳定 path/version 是公共合同；后续破坏性语义调整需要新版本或迁移说明。
- owner 的 `judgment_mode`、typed exits、consumer 和 freshness 语义保持不变。

## 兼容与升级

- 使用 preset 官方 source/overlay/managed inventory 机制，不 patch Trellis upstream template。
- `apply.sh --repo .` 后处理所有 `.new/.bak`；dogfood drift 必须为零。
- clean throwaway 安装验证 marketplace workflow、preset、platform discovery 和 semantic eval。
- update/upgrade 后重新 apply preset，确认合同、owner references 与 executable modes 保留。

## 风险与回滚

- 风险：规则在多个 owner 中复制。控制：owner 只放 SSOT 链接与局部使用点，测试检查唯一正文。
- 风险：只改 installed copy。控制：先改 canonical，再 apply 并执行 drift checker。
- 风险：eval 退化为关键词/命令计数。控制：fixture 断言 evidence coverage、结论和 exact literal 行为。
- 风险：误给非 owner 增加检索职责。控制：按 Issue 明确 owner 清单和非 owner 负面检查。
- 回滚：所有变化为 Markdown/spec/eval/preset 投影，无数据迁移；可按当前 task diff 回退，不影响外部状态。
