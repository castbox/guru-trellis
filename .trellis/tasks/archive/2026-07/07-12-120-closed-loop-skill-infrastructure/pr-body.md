## 变更摘要

- 建立 `trellis/skills/guru-team/` 唯一 canonical workflow skill root，并新增 reserved/active registry lifecycle、interface/schema 和 stable public API 合同。
- 扩展 Guru Team preset，以 exact previous managed hash 将 active package 分发到 installed runtime、shared skill root 和已选择的平台 skill roots。
- 新增 `check-skill-packages --mode source|installed`，对 package discovery、frontmatter identity、真实 tests evidence、workflow markers、typed exits、installed inventory、hash、mode、drift 和 sidecar 执行确定性 fail-closed 校验。
- Production registry 仅预留 `guru-create-work-commit`，本 PR 不实现任何具体 active workflow skill。

## 影响范围

- Canonical skill contract：`trellis/skills/guru-team/` 的 registry、两份 schema、fixture package 与回归测试。
- Companion runtime：canonical 与 dogfood `guru_team_trellis.py`、installed registry/schema 和 extension manifest。
- Preset 与平台分发：selected Claude/Codex/Cursor/shared skill copies、managed hash、platform shrink、`.new/.bak` 与 provenance 行为。
- Durable docs：requirements、workflow/preset/docs specs、根 README、workflow README 和 preset README。
- 不新增 API、CLI 业务入口、后台任务、运行时配置、数据库行为或部署单元；不需要修改 CI/CD、容器、Kubernetes/Kustomize、migration 或 Makefile。

## 验证结果

- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：`420/420`，exit 0。
- `python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py`：`54/54`，exit 0。
- Source/installed `check-skill-packages`、dogfood overlay drift、canonical/dogfood byte equality、JSON/Bash/Python、task 与 commit validators、`git diff --check` 全部通过。
- Local throwaway 已覆盖 workflow init、preview/switch、preset apply、`trellis update --force`、workflow/preset reapply、installed validation、closeout harness 与最终零 sidecar。
- Reviewed content push 后仍必须执行远端 exact feature-ref marketplace verification；本地 public `main` 抽样不替代该门禁。

## Review Gate

- Branch Review Gate 绑定 `5a1fb0412b68ef75fe05816c0eb29e1b1d417945`，覆盖 `origin/main...HEAD` 的 55 个文件与两条 work commit。
- Round 1 的 P1/P2 已由 Round 2 closure；Round 3 的测试命令 evidence P2 已由 Round 4 closure。
- Round 5 使用从未参与前序 review 的 fresh final reviewer，P0/P1/P2/P3 均为 0；五份 raw report digest 已由 assignment 与 gate 绑定。

## Issue 关闭范围

Closes #120

本 PR 不实现或关闭任何具体 workflow skill；raw review report 在 digest 绑定前的通用路径门禁维持为独立后续候选。

## Docs SSOT

- 策略：`partial_docs / ssot_first`。
- Durable primary inputs 包括 `docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/**` 与三个公共 README。
- Canonical layout、registry lifecycle、frontmatter/tests evidence、typed exits、managed hash、platform distribution、validator 和 update/reapply 合同已合并到 durable docs/spec。
- `task_history`：Task planning、approval、liveness、五轮 raw review 与执行时间仅作为任务历史证据，不形成第二套公共合同。
- 当前 PR 的唯一发布限制是 push 后 exact feature-ref marketplace verification；该证据由 finish-work transaction 生成并绑定。

## 安全说明

- 未发现 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或 workspace journal。
- 公共 package、fixture、manifest、example 与公开文档不包含真实本机绝对路径；task-local raw report 中的 worktree path 仅作为经确认的 workspace-boundary evidence 保留。
- Unknown local skill edit 与 invalid provenance 不会被静默覆盖；installer 保留原文件并生成 `.new` 或 fail closed。
- 无部署步骤、运行时配置迁移、数据库 migration 或回滚操作。
