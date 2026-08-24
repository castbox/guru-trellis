# #304 Release readiness blockers 修复设计

## Approach

本 task 是一次 current authority repair，不改变 executable contract。修改分为两个互相约束的文档面：release-facing installation identity 与 capability/consistency 分类。

## Release Identity Rules

当前发布入口采用：

| Identity | Value |
| --- | --- |
| Repo tag | `v0.6.15-guru.1` |
| Extension revision | `0.6.5-guru.37` |
| Official Trellis CLI | `0.6.15` |

README 可以说明这是本次发布使用的 immutable source，但在 tag/Release 创建前不得声明 tag object、peeled commit、GitHub Release 或 tag-pinned smoke 已验证。旧 `v0.6.5-guru.10` 只保留为 historical/existing migration before-state。

## Verification Responsibility Model

```text
before/after projection
  capability-loss gate
    workflow
    task_data
    docs_authority

  consistency/installation gates
    skill_api and interface/schema/command projection
    distribution and managed/installed file inventory
    executable mode, template hash, sidecar and platform parity
    extension identity and version binding
```

前一组回答“用户可观察 workflow capability 是否丢失”；后一组回答“package/install projection 是否一致并可安装”。后一组任一 blocker 仍可阻断 release，但不应被命名为 capability loss。

## RDT Repair

- Requirements：拆开 `REQ-013` 的安装完整性职责与 `REQ-018` 的 capability preservation 职责。
- Design：让 `DES-010` 保留 compatibility/migration 公共合同；重写 `DES-016` 为与 verifier 一致的两层比较模型。
- Test：重写 `TST-015` 与 `SCN-013`，在 test plan 中把 capability 与 installed projection 拆成可独立判定的结果；traceability 保持现有 ID 链并澄清 evidence 含义。
- `capability-inventory.md` 如存在同类混合陈述则同步，不改变 inventory 数量或历史 evidence。

采用 `guru-maintain-requirements-design-test-ssot:repair`，因为 #304 Release gate 直接消费 shared current `.40`，本次是对已确认 stale authority 的原位修复，不是并行产品需求 contribution。

## Architecture Repair

在 `docs/architecture/04-integrations/distribution.md` 建立 capability 与 installation consistency 的明确集成边界，并同步 `01-current/system.md` 与 `evidence/current-evidence.md` 中混合描述。若 traceability/support locator 无需改变则不制造额外文件。

该变化不改变 architecture boundary、owner、decision、GAP、single-writer 或 compatibility exit。Architecture lifecycle 使用 `repair` 收敛 stale current wording，随后 fresh `task_impact_sync(stage=planning)` 的结论为 `no_architecture_impact`；不创建 contribution 或 ADR。

## Spec Projection Decision

`.trellis/spec/workflow/quality-guidelines.md` 当前定义 validation ownership 与 distribution checks，但没有把 API/schema 或 installed-file inventory 定义为 capability loss。保持 no-op，避免把 repository authority 正文复制成第三份定义。实现后再次检索；只有发现明确相反语义时才做最小 projection 修正。

## Risks And Controls

- 误把 historical before-state 替换为新 tag：按上下文逐处审查，不做全仓机械替换。
- 在 tag 创建前虚构已发布状态：只描述 target/current release source，不写未知 tag object 或 post-publish evidence。
- 弱化安装门禁：每处修订都明确 API/schema/distribution inventory 仍可独立阻断 consistency/installation。
- authority ID 断链：保留现有 REQ/DES/TST/SCN/ARCH IDs，只修正文案与映射解释。
- scope 扩张到代码：用 `git diff --name-only` 和禁止路径检查阻断。

## Rollback

本 task 仅修改 Markdown 与 task planning。若语义 review 发现职责混淆，回到 task planning/authority repair，不修改 verifier 来迎合文档。
