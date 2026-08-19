# #266 设计：当前双 SSOT 与 Architecture Baseline Bootstrap

## 1. 执行 profile 与 owner

本 task 使用 `guru-bootstrap-repository-ssot:existing_repository`。其编排顺序固定为：

1. fresh preflight 与 repository analysis；
2. upstream `trellis-spec-bootstrap` 刷新项目工程规范事实；
3. `guru-maintain-requirements-design-test-ssot:bootstrap_foundation` 建立三层 SSOT；
4. `guru-maintain-architecture-baseline:bootstrap_foundation` 建立架构基线；
5. Bootstrap owner 做 cross-SSOT consistency review；
6. 投影最小 `.trellis/spec` locator/index/usage contract；
7. 运行结构、链接、projection 与 current-context validator；
8. 仅在 semantic review 无 blocking finding 时激活 current version。

三个 child owner 独占各自 semantic judgment；Bootstrap 只消费最小 locator/version/status/
scope/freshness，不复制其私有扫描或 review artifact。

## 2. Canonical 文档布局

```text
docs/
  requirements/
    README.md
    versions/<current-version>/
      requirement-main.md
      requirement-non-functional.md
      traceability.md
      decisions.md
  design/
    README.md
    versions/<current-version>/
      design-main.md
      traceability.md
      decisions.md
      manifest.yaml
  test/
    README.md
    versions/<current-version>/
      test-strategy.md
      test-plan.md
      traceability.md
  architecture/
    README.md
    00-foundation/
    01-current/
    02-target/
    03-domains/
    04-integrations/
    05-gaps/
    06-governance/
    07-plans/
    adr/
    evidence/
```

current version 的最终目录名由 live manifest/release/current source 语义审查决定。不得仅因
extension revision 为 `0.6.5-guru.35` 就把尚未发布的 current main 写成 released version。
README 的版本矩阵同时表达 released baseline、active current-as-built 和 future target。

## 3. Authority 与迁移

- 现有 `docs/requirements/requirement-main.md` 与 `guru-team-trellis-flow.md` 作为恢复输入；
  其 current 定义被移动/吸收到 versioned authority 后，旧路径仅保留清晰导航或历史边界。
- Issue/PR/task/finish-summary 只作为 provenance/evidence locator，不成为 current authority。
- current code 可支持 `code_recovered` design/capability fact，但不能直接证明产品 intent。
- architecture EVIDENCE 指向代码/测试/release/installation evidence；不复制大段日志。

## 4. Current capability inventory

inventory 从 current live registry、每个 `interface.json`、extension manifest、workflow markers、
commands、managed paths 与平台 projection 派生，至少映射：

- Intake/base/context/clarification/wording/readiness/workspace；
- Planning/normal-scenario qualification；
- implementation/Phase 2/semantic commit/Branch Review；
- publication/finalization/merge/provider recovery/base reconciliation；
- task index/history、finish-summary/archive、semantic naming、Docs SSOT；
- Requirements/Design/Test、Architecture Baseline、repository Bootstrap；
- marketplace/preset/overlay/installer/managed runtime/platform entries。

inventory 使用 stable IDs 与 locator，不复制 interface/schema 正文。

## 5. Architecture 状态模型

- FOUNDATION：官方 Trellis 优先、Markdown/process 与 deterministic script 分层、AI-first、
  public API/compatibility 和 honest normal-path 边界。
- CURRENT：只放 `3c0d4a2f…` source/config/tests 与 `v0.6.5-guru.9` release facts可证明内容。
- TARGET：Trellis v0.6.15、双 SSOT 持续维护与后续 Phase owner 解耦目标。
- GAP：CURRENT 到 TARGET 的差距，绑定唯一 owner；不自动进入本 task。
- PLAN：#275/#260/#267 与后续 refactor 的顺序/依赖；不表示已授权或已完成。
- ADR：历史决策与 active projection 的关系；draft 不约束 current task。
- EVIDENCE：exact commit/tag/PR/task/test locator 与 evidence class。

## 6. Traceability

使用稳定引用链：

```text
REQ-* / BEH-* -> DES-* / CON-* -> TST-* / SCN-* / CASE-* -> ARCH-* / EVD-*
```

Requirements 定义 why/what；Design 定义 how/ownership/contract；Test 定义证明方式；
Architecture 定义跨域约束、CURRENT/TARGET 与决策。traceability 文件只记录 identity、locator、
version/status 和关系，不复制正文。

## 7. `.trellis/spec` projection

projection 包含：canonical locators、active version/status、适用 scope、推荐读取顺序、
traceability entry、task-impact/promotion route、freshness 规则。现有 workflow package contract
仍保留为可复用工程规范；新增 docs/architecture index 不与其重复。

## 8. 验证设计

- static：JSON/YAML/Markdown structure、placeholder、重复 heading、链接与路径存在性。
- context：`get_context.py --mode packages/phase` 可加载新增 index，且无第三 authority。
- inventory：live registry/interface/workflow/manifest/command/platform projection 的闭包检查。
- evidence：fresh 回读 #263/#264/#265 merged PR、archive task/finish-summary 与 focused command results。
- scope：`git diff --name-status origin/main...HEAD` 只含 task/docs/spec 允许路径。
- independent review：独立 reviewer 检查完整 committed docs/spec diff、事实 provenance、
  cross-SSOT consistency 和所有 unverified boundary。

不运行完整多平台 Throwaway、upgrade/update 或 release-candidate matrix。

## 9. 兼容与回滚

本 task 不改公共 runtime/API；回滚仅需还原新增/迁移 docs/spec projection。任何发现要求改变
Skill/schema/exit/runtime 的问题都返回对应 owner 或记录 GAP，不在 #266 内修复。
