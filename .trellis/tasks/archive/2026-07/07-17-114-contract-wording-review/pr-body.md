## 变更摘要

- 新增公共 `guru-review-contract-wording` semantic closed-loop Skill，统一承载 controlled terms v2、九类 classification、固定 profile scope、AI rewrite/review、deterministic scanner/validator 与 typed exits。
- 固定 `change_request`、`planning_artifacts`、`explicit_paths` 三个 profile；每个 profile 都绑定不可缩小的 scope、内容 hash 和唯一 consumer，content mutation 后必须重新扫描并绑定新 evidence。
- 保留 #93 的 planning approval blocking semantics 与七项 planning semantic dimensions；planning approval 只消费已验证 evidence，不再拥有词表、分类、scanner 或默认语义判断。
- 支持 current `content_changed` / `blocked` evidence 通过 digest-bound same-profile re-entry 收敛为 `pass`，同时拒绝 wrong profile、wrong digest、stale result、missing target 和 conflicting replacement。
- replacement-first 验证通过后，已删除旧 active planning ambiguity constants、scanner/parser/helpers、active flag usage 和完整规则副本；历史 archived #93 artifacts 未追溯修改。
- 同步 canonical workflow/package、shared runtime、schema、registry、preset、Agents/Codex/Cursor/Claude 副本、dogfood、requirements、README 与 durable spec。

## 影响范围

- Workflow：Phase 0 change request 与 planning approval 都显式调用同一 stable Skill id，workflow 只负责 mandatory invocation、profile route、typed-exit consumer 与 fail-closed stop。
- Skill/runtime：新增 scope builder、objective hit facts、AI-authored classification/reason、recorder/validator、re-entry supersession 与 planning evidence projection 合同。
- Standalone：允许用户对 issue/draft 或显式 repo-relative Markdown 路径执行完整审查，不要求进入 Guru Team Phase 0；`explicit_paths` 不可用于缩小前两个固定 profile。
- 分发与升级：5 个 active Skills、5 个 invokes、17 个 exits、11 个 targets 和 208 个 managed files 已同步；canonical、installed 与四平台 package 保持 byte/mode 一致。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`；不改写 archived task artifacts；不实现或关闭其它 issue。

## 验证结果

- Shared runtime：`507/507 passed`。
- Production Skill package：`71/71 passed`。
- Canonical wording package：`16/16 passed`。
- Preset installer + upstream ownership：`45/45 passed`。
- Planning / Phase 2 gate subset：`54/54 passed`。
- Source validation：5 active、5 invokes、17 exits、11 targets；installed validation：208 managed、0 sidecar、0 removal、0 conflict。
- Canonical、installed、Agents、Codex、Cursor、Claude 六树 package byte equality，canonical/installed workflow、runtime、registry byte equality，12/12 wrappers executable。
- Clean throwaway 已覆盖 fresh workflow/preset install、五平台安装、initial 与 after-update `content_changed -> pass` re-entry、`trellis update --force`、workflow/preset reapply 和最终零 `.new` / `.bak`。
- `git diff --check origin/main...HEAD`、JSON/JSONL parse、Python/Bash syntax、dogfood overlay drift、secret/deploy/sidecar audit 均通过。
- 远端 branch-pinned marketplace verification 由 `trellis-finish-work` 在 reviewed content HEAD push 后、PR 创建前执行；失败会阻塞发布。

## Review Gate

- Branch Review Gate 绑定 HEAD `32119d2ed400046a44148d7f6b580b59a95a0f94`，覆盖 `origin/main...HEAD` 的 5 个 commits、94 个 paths 和完整 task scope。
- 八轮审查中发现的 3 个 P1、2 个 P2 finding 均已由修订、closure review 与 fresh final review 闭环。
- Round 8 最终开放 findings 为 `P0=0, P1=0, P2=0, P3=0`，`findings_count=0`；审查覆盖 replacement-first 删除、planning compatibility、Docs SSOT、分发/update、部署与安全边界。

## Issue 关闭范围

Closes #114

- 仅关闭已由 Phase 2、Branch Review 和发布门禁完整覆盖的 Issue #114。
- 父级、依赖、被阻塞事项及其它 issue 均不在本 PR 的关闭范围。

## Docs SSOT / 文档同步

- Strategy：`ssot_first`。
- Canonical package contract 独占 controlled terms v2、classification、三个 profile、semantic loop、evidence、re-entry 与 typed exits；global workflow 只保留全局调用和路由合同。
- Durable docs 已更新 `docs/requirements/**`、canonical workflow/package README、preset README 与六份 `.trellis/spec/**`，并同步旧 owner 删除、planning evidence consumer、分发和 update/reapply 验收口径。
- Issue intake、finding lifecycle、Phase 2 和八轮 Branch Review 只保留为 task history；当前无待后续处理的 Docs SSOT 缺口。

## 安全说明

- 未发现 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录；public artifacts 不持久化本机 secret。
- 本次只处理正常运行、常见操作错误和明确 correctness/compatibility 边界，不引入 issue 已排除的恶意 actor、故意伪造、额外并发/锁、TOCTOU、fault injection 或跨 OS 原子性机制。
- 未修改 `.github/workflows`、服务/API、业务 CLI、worker、数据库 schema/migration、Dockerfile、Compose、Kubernetes/Kustomize/Helm 或 Makefile，无业务部署、生产配置或数据库迁移要求。
- 本 PR 不创建 release tag；回滚使用 Git revert，并从上一 extension ref 重新应用 workflow/preset。
