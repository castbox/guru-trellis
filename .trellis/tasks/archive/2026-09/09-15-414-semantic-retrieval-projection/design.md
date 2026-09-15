# #414 技术设计：semantic retrieval ownership 收敛

## 1. 设计原则

1. 以 current ownership authority 替代 Issue 正文中的旧 13-path 修复机制。
2. 保持一个 canonical semantic retrieval SSOT 和一个由 preset 管理的 dogfood
   projection，不建立第二份规则或 adapter。
3. Guru semantic Gate 由四个 Guru owners 承担；upstream workers/providers 只
   提供 evidence，Guru caller 对消费后的语义结论负责。
4. 测试验证 current contract，不通过 patch upstream-owned 文件来迎合旧断言。
5. `guru-reconcile-task-base` 保持 bounded pair reconciliation owner，但不成为
   broad semantic retrieval owner。
6. 修改只覆盖 owner wording、reconcile package guidance、shared package-contract
   中同一 direct-consumer 声明、对应 focused test 和必要 installed projection。

## 2. 所有权模型

| 角色 | 拥有 | 不拥有 |
| --- | --- | --- |
| Canonical semantic retrieval spec | concept family、coverage、negative conclusion、AI/script 与 artifact 边界、Guru owner 列表 | upstream agent 内容或平台生成文件 |
| 四个 Guru owners | 直接检索时的语义扩展与充分性；消费 worker/provider evidence 后的最终语义判断 | upstream worker 实现 |
| `guru-reconcile-task-base` | exact caller input、old/new base pair、live authority/planning locators、candidate delta 与 qualified base impact 的 bounded reconciliation judgment | broad semantic retrieval SSOT ownership、concept-family search contract、第五 owner 身份 |
| 官方 `trellis-*` skills/agents/workers | Trellis 官方定义的 research/implement/check/session behavior 与 evidence production | Guru SSOT ownership、Guru semantic Gate |
| Preset installer | canonical spec 到 dogfood/installed path 的确定性投影 | 修改 upstream-owned files |
| Focused test | current owner 引用/eval/fixture、non-owner 不扩权、canonical/installed identity、upstream exclusion | 规定新的 workflow 行为 |

## 3. Contract 修改

在 canonical `semantic-retrieval.md` 的 Ownership Boundary 中：

- 将 owner 列表收敛为四个 Guru Skill ids；
- 说明直接调用 upstream worker/provider 不转移 semantic ownership；
- 说明 Guru caller 在采用这些 evidence 形成 current/negative conclusion 前，
  必须完成适用 concept family、coverage 与 sufficiency 判断；
- 保持 Python/shell 仅执行 caller-supplied query 与客观 validation 的既有边界。

不改动 concept taxonomy、artifact policy、public DTO 或任何 Skill interface。

`guru-reconcile-task-base` 的 canonical `SKILL.md` 与 `references/contract.md` 同步
移除直接读取 semantic retrieval SSOT 及 concept-family/evidence-coverage owner
声明，改为明确消费现有 closed inputs 与 candidate evidence。其六个 input
profiles、typed exits、workflow routes、normal-scenario qualification、candidate
executor、persistent reconciliation executor、schema 与 runtime 全部保持不变。

Canonical `skill-package-contract.md` 的 `Task Base Reconciliation Owner` 段落同步
删除“读取 broad semantic-retrieval SSOT”的要求，改为只描述 exact caller-supplied
task/base pair、closed candidate facts 与 qualified base-impact candidate 的 bounded
judgment。该共享合同不复制 concept family，也不成为第五 owner。

## 4. Test 修改

`test_semantic_retrieval_contract.py` 保持四项 focused coverage：

1. 唯一 spec 与 canonical/dogfood byte identity；
2. 四个 Guru owners 的 SKILL/contract references、semantic eval assertions 和
   fixture adequacy，以及包含 `guru-reconcile-task-base` 与 shared package-contract
   wording 的 Guru non-owner 不扩权；
3. semantic eval runner 必须依赖完整 external grading；
4. ownership projection：13 个官方 Trellis 文件不要求 Guru spec reference，且
   不进入 Guru managed owner inventory。

第四项直接替换陈旧 positive assertion，不删除失败来弱化行为门禁。断言只
检查 current ownership 可客观验证的边界，不解析或复制 upstream 文件内容。

## 5. Projection 与数据流

```text
canonical semantic-retrieval.md
              |
              | preset apply
              v
dogfood .trellis/spec/workflow/semantic-retrieval.md
              |
              +--> source/installed identity validation

upstream worker/provider evidence
              |
              v
four Guru semantic callers -> concept family / coverage / sufficiency -> conclusion

exact base pair + live locators + candidate evidence
              |
              v
guru-reconcile-task-base -> bounded reconciliation judgment
```

Dogfood 文件只通过
`trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 产生。若 apply 生成
`.new`/`.bak` 或其它冲突结果，停止并按 installer contract 处理，不手工覆盖。

## 6. Compatibility 与迁移

- 这是对既有 owner 声明和 consumer test 的同步收敛，不变更 public API/schema、
  typed exit、Skill package identity、workflow graph 或 platform interface。
- 被移除的是不再受 authority 支持的 owner claim 和测试要求；不存在需要保留
  的 deprecated Guru adapter 或 dual path。
- Reconcile 只减少越界的 broad retrieval dependency；既有 input/output、route、
  candidate construction、validation、commit continuity 与 recovery 语义不变。
- 官方文件继续由 Trellis 0.6.17 generation/update 管理，本任务不写这些文件。
- 旧 candidate 仅作为 defect provenance，不作为合并后 release evidence。

## 7. 风险与控制

| 风险 | 控制 |
| --- | --- |
| 误删四个真实 Guru owner 的语义门禁 | 保留 owner references、eval assertions 和 fixtures 的正向测试 |
| 将 non-owner 扩成第二 semantic owner | non-owner negative assertions 与完整 diff review |
| 收敛 reconcile wording 时误改 base evolution 行为 | 限定两份 canonical guidance，验证 interface/runtime bytes 不变并运行 package tests |
| 手工修改 dogfood 导致 canonical 漂移 | canonical-first 修改，preset apply 后 byte identity 与 drift check |
| upstream 文件被意外 patch | 精确 path diff、ownership test 和 Branch Review 检查 |
| focused test 通过但 installed/update 回归 | source/installed validators 与 clean throwaway update/reapply |
| 混入 release 副作用 | Publication 仅 Refs #410；不 tag、不 Release、不关闭 #410 |

## 8. Rollback

- 在 commit 前可恢复本任务五个 canonical 实现/测试文件到 branch base，并重新运行
  focused 与 reconcile package tests；不触碰 upstream-owned 文件。
- preset apply 出现 sidecar 或 unexpected paths 时停止，不提交尚未完成同步的
  projection。
- 若实现中发现必须新增 owner/API/schema 或改变 #408 行为，视为 scope change，
  返回 requirements clarification 与 fresh planning，不在 Phase 2 临时加补丁。

## 9. Docs SSOT Plan

- Docs state：`complete_docs`；strategy：`task_delta_only`。
- Durable authority path：
  `trellis/presets/guru-team/spec/workflow/semantic-retrieval.md` 与
  `trellis/presets/guru-team/spec/workflow/skill-package-contract.md` 的现有 owner
  boundary 段落。
- Installed/dogfood projection：
  `.trellis/spec/workflow/semantic-retrieval.md` 与
  `.trellis/spec/workflow/skill-package-contract.md`，仅由 preset apply 同步。
- Task files记录 Issue #414 的 authority replacement、取舍和验证计划，不成为
  parallel durable contract。
- 预期无需修改 requirements/design/test contribution 或 Architecture Baseline；
  Phase 1 Architecture task-impact owner 必须 fresh 确认该结论后才能 approve。
