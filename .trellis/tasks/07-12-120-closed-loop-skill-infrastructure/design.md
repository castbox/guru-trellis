# #120 技术设计

## 1. 设计目标

本设计新增公共 skill 基础设施，不交付任何 active production skill。系统必须先固定 package contract、registry lifecycle、workflow marker、managed hash 与平台分发语义，后续 issue 方可激活具体 skill。

## 2. SSOT 与责任边界

| 层 | SSOT | 责任 | 禁止事项 |
| --- | --- | --- | --- |
| Global workflow | `trellis/workflows/guru-team/workflow.md` | phase 顺序、mandatory skill invocation、跨 skill transition、typed exit consumer/stop | 复制 step-local skill 正文 |
| Dogfood workflow | `.trellis/workflow.md` | 当前仓库运行副本 | 成为唯一源头 |
| Canonical skills | `trellis/skills/guru-team/` | registry、schema、package、interface、fixture contract | 携带 active task 或平台 prompt |
| Installed runtime | `.trellis/guru-team/skills/` | 可审计 installed registry/package 副本和 provenance | 反向成为 canonical source |
| Platform roots | `.agents/skills/`、`.codex/skills/`、`.cursor/skills/`、`.claude/skills/` | runtime discovery copy 或格式 adapter | 拥有独立语义合同 |
| Preset installer | `trellis/presets/guru-team/` | 选择平台、复制 bytes、记录 hash、处理冲突 | 判断 skill 语义是否充分 |
| Validator | `check-skill-packages` | 校验 registry/schema/path/hash/marker/exit mapping | 执行 AI review 或决定 route 是否符合流程意图 |
| Durable docs/spec | `docs/requirements/**`、`.trellis/spec/**`、README | 公共合同、人类作者指南、升级规则 | 存储 task-local 决策日志 |

## 3. Canonical 目录

```text
trellis/skills/guru-team/
├── registry.json
├── schemas/
│   ├── skill-registry.schema.json
│   └── skill-interface.schema.json
├── packages/
│   └── <active-skill-id>/
│       ├── SKILL.md
│       ├── interface.json
│       ├── references/
│       ├── scripts/
│       └── examples/
└── tests/fixtures/
    ├── representative-active/
    └── invalid-*/
```

Production `registry.json` 初始只包含：

```json
{
  "schema_version": "1.0",
  "skills": [
    {
      "id": "guru-create-work-commit",
      "state": "reserved",
      "reason": "由后续独立 issue 实现"
    }
  ]
}
```

`reserved` entry 不声明 package path、workflow route 或 platform destinations。`active` entry 必须声明 package/interface 路径、supported platforms、validator command 和 workflow route identity。

## 4. Interface 合同

每个 active package 的 `interface.json` 必须由 `skill-interface.schema.json` 校验，并承载以下结构化字段：

- `schema_version`、`id`、`name`、`description`、`state`；
- `modes.workflow` 与 `modes.standalone`；
- `entry_preconditions[]`：id、evidence、binding、freshness；
- `ordered_stages[]`：forward behavior、AI Review Gate、conditional human confirmation、recorder/validator；
- `artifacts[]` 与 `schemas[]`；
- `validators[]`：stable command 与 objective scope；
- `external_exits[]`：stable exit id、evidence、consumer kind/id；
- `reentry` 与 stale behavior；
- `tests` 与 declared platform destinations。

Schema 只能证明字段、枚举、唯一性和引用形状。AI 必须审查 scope、内容充分性、finding、revision action 和 route 是否符合已审阅的流程意图。

## 5. Workflow marker 合同

机器 marker 使用 HTML comment 包裹单行 JSON，避免自然语言匹配：

```markdown
<!-- guru-skill-invoke: {"skill":"guru-example-action","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-example-action","exit":"completed","consumer":{"kind":"workflow","id":"phase-3"}} -->
```

Source validator 必须校验：

1. production workflow marker 引用的 skill 均为 active；
2. 每个 mandatory active skill 只有一个 invoke identity；
3. 每个 declared external exit 只有一个 consumer 或一个 explicit stop；
4. unknown、duplicate、multiple、unmapped marker 失败；
5. reserved id 出现在 marker 中失败。

Production registry 尚无 active skill，因此本任务不向 production workflow 添加虚假 marker。Fixture workflow 覆盖正常和失败矩阵。

## 6. 分发与 provenance

Preset apply 顺序：

1. schema 校验 canonical registry；
2. source mode 结构检查；
3. 安装 `.trellis/guru-team/skills/` registry/schema/active packages；
4. 按 selected platforms 生成 shared 与平台 runtime copies；
5. 对每个目标执行 managed hash 状态机；
6. 写入 `.trellis/guru-team/extension.json` 的 skill package provenance；
7. 运行 installed mode 结构检查；
8. 冲突、invalid provenance 或 drift 返回非零。

Installed manifest 的 skill package 区块必须记录：

- canonical registry digest 和 schema version；
- reserved ids 与 active ids；
- selected platforms；
- 每个 active package 的 interface digest、tree digest；
- 每个 installed destination 的 repo-relative path、file digest 和 executable bit；
- `.new` / `.bak` 结果。

Manifest 不记录本机绝对路径。Source commit/ref 继续由现有 extension provenance 记录。

## 7. Managed hash 状态机

```text
missing
  -> install canonical -> managed(current_hash)

same as canonical
  -> unchanged -> managed(current_hash)

different + previous manifest hash matches target
  -> write target.bak -> install canonical -> managed(current_hash)

different + previous hash missing/invalid/mismatch
  -> preserve target -> write target.new -> conflict -> fail closed
```

公共 skill copy 使用 exact previous hash，不调用 overlay 内容启发式。`.bak` 只能由 known managed upgrade 产生；`.new` 表示 unresolved local ownership conflict。验证结束前必须处理全部 sidecar。

## 8. Validator 设计

Stable wrapper：

```bash
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json \
  --mode source|installed
```

Canonical implementation 归属 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 的 `check-skill-packages` subcommand；preset 将 wrapper、Python runtime、registry/schema 安装到目标仓库。

`source` mode 输入 canonical root、canonical workflow 和 registry。`installed` mode 输入 target repo、installed manifest、installed registry/package 和 selected platform roots。两种 mode 只输出结构化 facts、errors 和 status。

## 9. 测试设计

- Registry/interface schema unit tests：valid reserved、valid active、duplicate id、bad id、missing contract、unknown schema。
- Route unit tests：missing invoke、duplicate invoke、reserved invoke、unknown/multiple/unmapped exit、unique consumer、explicit stop。
- Installer unit tests：missing、unchanged、known upgrade + `.bak`、unknown edit + `.new`、invalid provenance、selected platform roots、executable bit。
- Representative fixture：test-only active package 在 temporary target 的 shared/Codex/Cursor/Claude roots 中可发现；production registry/install 断言不存在该 id。
- Throwaway integration：workflow init、preview、switch、preset apply、source/installed validation、`trellis update --force`、workflow reapply、preset reapply、drift 和零 sidecar。
- Dogfood：apply preset `--all-platforms`，核对 installed manifest，再运行 overlay drift checker。

## 10. Docs SSOT Plan

- `docs_state`：`partial_docs`。现有 durable docs 已覆盖 workflow、preset、installer、overlay 和 update/reapply，但没有公共 closed-loop skill package/registry/interface/typed exit 分发合同。
- `strategy`：`ssot_first`。实现代理必须先更新 durable requirements/spec，再实现 schema、validator、installer 和测试。
- 必须更新：`docs/requirements/README.md`、`docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`、`.trellis/spec/workflow/index.md`、`.trellis/spec/workflow/workflow-contract.md`、新增 `.trellis/spec/workflow/skill-package-contract.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/docs/public-docs.md`、`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- Task artifact delta：本文件中的 canonical layout、interface、marker、hash state machine、validator 和验证矩阵必须合并进入上述 durable docs/spec。
- Merge checkpoint：实现任何 schema/validator/installer 代码前完成 durable docs/spec 更新；Phase 2 check 必须复核 docs、code、schema、tests 和 installed behavior 一致。
- Task-history-only：历史检索过程、候选方案比较和当前任务执行证据保留在 task 目录，不进入公共 package。

## 11. 兼容性、升级与回滚

- 新 schema/id/command 从 `1.0` 起步；既有 workflow id、preset path 和 companion command 不改名。
- `trellis/guru-team-extension.json` 必须增加公共 managed paths/command/artifact 声明并递增 Guru extension patch version。
- `trellis update` 若恢复官方 platform 文件，后续 workflow reapply + preset reapply 必须恢复 Guru Team installed state。
- 升级遇到 unknown local skill edit 时 installer 保留原文件并写 `.new`，不继续声称 installed validation passed。
- 回滚使用 known upgrade 产生的 `.bak` 和 Git 历史；installer 不自动替用户选择回滚内容。

## 12. 安全边界

- Public registry、package、fixture、manifest 和文档不得包含 secret、客户数据、签名 URL、`.env`、workspace journal、active task state 或本机绝对路径。
- Platform destination 和 manifest locator 必须为 repo-relative path。
- Script 不得根据内容判断 AI Review 是否通过，不得决定 issue close/ref/followup。

## 13. 中台知识门禁

`not_applicable`。本任务修改 Guru Team Trellis extension 自身，不涉及 `go-guru`、`proto-guru`、Unity3D Guru SDK、Flutter Guru SDK 或其它中台 SDK/API 合同，因此不查询 `guru-knowledge-center`。

## 14. 需求追踪

| 需求 | 设计承接 | 实现计划承接 | 验收承接 |
| --- | --- | --- | --- |
| R1 | 第 2、4 节 | 第 2、3 节 | AC1、AC4 |
| R2 | 第 3、4 节 | 第 3 节 | AC2、AC3 |
| R3 | 第 2、6 节 | 第 5 节 | AC3、AC7、AC9 |
| R4 | 第 6、7 节 | 第 5、7 节 | AC6、AC7 |
| R5 | 第 8 节 | 第 4、7 节 | AC4、AC5、AC7 |
| R6 | 第 5 节 | 第 4、6 节 | AC4、AC5 |
| R7 | 第 2、10、11 节 | 第 2、3 节 | AC1、AC8、AC10 |
| R8 | 第 9、11 节 | 第 6、7、8 节 | AC3、AC6、AC8、AC9、AC11 |
