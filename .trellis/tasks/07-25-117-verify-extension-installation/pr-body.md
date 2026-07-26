## 变更摘要

- 新增可独立调用的 `guru-verify-extension-installation` semantic Skill，分别支持
  workflow 与 standalone 输入，并为 `verified`、`not_required`、
  `return_to_task_work`、`blocked` 提供最小 `exit_id` typed DTO。
- 将 applicability、verification profile 与 adequacy judgment 保留给 AI，
  deterministic runtime 只负责 remote/ref/HEAD 校验、clean throwaway 执行、
  machine facts 记录和 artifact freshness 检查。
- 补齐 workflow marketplace、preset initial apply/reapply、`trellis update`、
  platform package、ownership、`.new/.bak`、managed assets 与 README 用户命令的
  安装验证矩阵。
- 为成功路径增加 231 项 retained installed asset inventory，按
  workflow/preset/schema/skill/platform 保存 digest、relation、category 与逐
  capability evidence，并对 missing、duplicate、unexpected、mismatch 与 relation
  error fail closed。
- 同步 canonical、dogfood installed、Shared、Codex、Claude、Cursor package，
  以及 preset installer、extension manifest、public docs、schemas、examples 与
  production eval corpus。

## 影响范围

本变更影响 Guru Team extension verification 的公共 Skill package、workflow
runtime、recorder/checker/wrapper、consumer schemas、extension registry、preset
installer 与四个平台分发副本。它新增任务内 private verification checkpoint，但
跨 Skill 只传递 consumer 直接需要的最小 DTO，不暴露 verification profile、
command/log/digest inventory 或 temporary repository state。

用户可在 task workflow 外针对指定 remote ref 调用 standalone profile；workflow
profile 仍由后续 finalization owner 提供 plan-bound reviewed HEAD。现有 upstream
Trellis Skill/Agent/Command/Prompt/Hook 不被覆盖，preset reapply 只恢复 Guru assets。

## 验证结果

- Runtime：600 passed，13 skipped。
- Skill integration：175 passed。
- Preset 与 ownership：54 passed。
- 12 个 package contracts：114 passed。
- Canonical/installed verifier contracts：各 9 passed。
- Source Skill validator：12 Skills、46 exits、27 targets、0 legacy。
- Installed validator：2,322 managed files，0 sidecar、0 removal、0 conflict。
- Shared、Codex、clean-env Claude source/installed：各 7/7 passed。
- Cursor source/installed：各 7/7 expected unsupported，未冒充交互 pass。
- Full local-source throwaway：exit 0，覆盖 initial install、preview/switch、
  preset reapply、update 与 post-update validation。
- Retained inventory：expected/observed/matched=`231/231/231`，
  `complete=true`；missing、duplicate、unexpected、mismatched 与 relation errors
  全空。
- Canonical/installed/platform distribution、runtime 与 native adapter equality、
  dogfood overlay drift、JSON/Bash/Python syntax 和 `git diff --check` 均通过。

Exact pushed feature-ref clean installation 尚未执行。当前通过的是本地 unpublished
source throwaway；后续 finalization 必须先 push reviewed content HEAD，再以真实
remote ref/HEAD 运行 mandatory extension verification。该 gate 通过前不得创建
最终 PR 或归档任务。

## Review Gate

Branch Review 覆盖完整 `origin/main...a28b38e5` committed range。六个
current-scope findings `BR-117-F1`、`BR-117-F2`、`BR-117-F7`、
`BR-117-F8`、`BR-117-F9`、`BR-117-F10` 均有独立 closure evidence。

Round 11 使用未参与 earlier finding 或 closure 的 fresh reviewer，结论为
0 qualified finding、0 scope proposal、0 blocker。Retained collector 单层
arbitrary-extra 候选被完整 installed package/manifest/platform/managed/sidecar
validator 证据反证并保留为 `rejected_candidate`；报告没有把 collector 夸称为任意
目录扫描器。Branch Review typed exit 为 `passed`。

## Issue 关闭范围

Closes #117

Related #115, #109, #116, #144, #146

Refs #81, #118, #119, #132

#117 的 Skill、runtime、schemas、distribution、tests 与文档合同已由当前完整 diff、
Phase 2 和 Branch Review 覆盖。#115 是上游 umbrella；#109/#116/#144/#146 是已完成
前置或相关合同；#81/#118/#119/#132 保持独立 follow-up，不由本 PR 关闭。

## 安全说明

Artifact 只保存去敏 repository identity、path、SHA-256、category、relation、
exit code 与 stdout/stderr digest/size，不保存 token、credential URL、原始 provider
响应、native transcript body、temporary repo 绝对路径或客户数据。Credential URL
会在写 artifact 前 fail closed；公开错误不会反射敏感输入。

Claude production eval 由 outer runner 清除 `ANTHROPIC_AUTH_TOKEN` 与
`ANTHROPIC_BASE_URL` 后执行。当前变更不新增 hostile-input、恶意篡改、并发竞态、
TOCTOU、锁、fault injection 或跨 OS atomicity 范围。

本 diff 不修改 CI/CD、容器、Compose、K8s/Kustomize、数据库 migration、
Makefile、dependency manifest 或生产数据面；不需要 deploy、service restart 或
data migration。发布阶段仅需要按 finalization workflow 完成 reviewed branch push、
remote extension verification 与 PR/archive transaction。

## Docs SSOT

- Strategy：`ssot_first`。
- Durable docs：公共 Interface/contract、private schemas/examples、runtime、
  tests、extension manifest、preset/ownership specs、requirements 与 README 已同步；
  F10 仅收敛 package-private installed evidence，没有改变 stable Skill id、public
  DTO、typed exit、consumer route 或用户安装命令。
- Task delta：workflow/standalone profiles、四 exits、consumer bootstrap、
  clean install/update/reapply、ownership 与 231 项 inventory 合同已经回写到对应
  durable owners 和六处分发副本。
- Task history：finding provenance、旧 command-only evidence 复现、Claude inherited
  provider environment 诊断、agent liveness、raw command capture 与 review lineage
  仅保留在任务历史中。
- Follow-up / limitation：exact pushed feature-ref 验证由后续 finalization gate
  执行；#118/#119 继续拥有 finalizer 与 Finish family integration，本 PR 不激活或
  替代这些后续能力。
