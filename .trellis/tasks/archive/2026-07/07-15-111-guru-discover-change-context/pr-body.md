## 变更摘要

- 新增公共 `guru-discover-change-context` semantic 闭环 Skill，在 updated base 上先调查当前 Docs SSOT、代码/API/config/schema 与测试，再搜索 archived task 的 `finish-summary.json:index.*` 历史候选。
- 固定 workflow 与 standalone 的 fresh-base precondition、current-state-before-history 顺序、duplicate candidate 投影、history query/scoring/digest、invalid isolation、zero-candidate、AI candidate selection 与 task-local same-snapshot persistence 合同。
- 提供 `context_ready -> guru-clarify-requirements`、`refresh_base -> guru-sync-base`、`blocked -> change-context-blocked` 三个稳定出口及唯一 consumer。
- 新增 `preview-change-context-history`、`record-context-discovery`、`check-context-discovery` companion commands，并同步 canonical package、schema、runtime、workflow、preset、dogfood 与 Agents/Codex/Cursor/Claude 分发副本。

## 影响范围

- Phase 0：repo-changing intake 在 `guru-sync-base:synced` 后 mandatory invoke `guru-discover-change-context`，再进入需求澄清与 workspace 创建流程。
- Skill 与 artifact：新增 interface `1.2`、`guru-context-discovery-1.0` schema、contract、example、thin wrappers、package tests，以及 task-local `context-discovery.json` 合同。
- History discovery：只扫描 `.trellis/tasks/archive/**/finish-summary.json:index.*`，不创建全局 index/cache，也不读取或写入 `.trellis/workspace/**`。
- 分发与升级：extension version 更新为 `0.6.5-guru.11`，preset managed inventory、public README、durable specs、throwaway install、`trellis update` 和 preset reapply 合同同步。
- 本 PR 不实现下游 `guru-clarify-requirements`、`guru-review-change-request` 或 workspace creation Skill。

## 验证结果

- Fresh targeted change-context suite：29 项通过。
- Fresh full related suite：589 项通过。
- Source Skill validator：3 个 active skills、3 个 invoke markers、9 个 exits、6 个 targets，全部通过。
- Installed Skill validator：128 个 managed files，`sidecar/removal/conflict=0`；canonical、installed、Agents、Codex、Cursor、Claude package 与 runtime 字节一致。
- Upstream ownership：43 个 active frozen paths、13 个 managed claims；dogfood overlay drift、`python3 -m py_compile`、`bash -n`、`git diff --check` 均通过。
- Clean throwaway 覆盖 workflow marketplace init/preview/switch、preset apply、direct discovery、candidate/zero-candidate、task-local record/check、`trellis update --force`、reapply 与 zero sidecar，结果通过。
- Reviewed branch push 后，`trellis-finish-work` 必须在创建 draft PR 前完成 exact feature-ref remote marketplace verification；失败会阻塞发布。

## Review Gate

- Branch Review Gate 绑定 HEAD `dc3e2e9a32b7b8db1dc7e5645f8599ddfa2700b7`，覆盖 `origin/main...HEAD` 的 114 文件完整 diff及两个 task commits。
- Round 001 的 BR-001/BR-002 已由同一 finding owner 在 Round 002 对新 HEAD 完成闭环；Round 003 使用未参与 earlier rounds 的 fresh technical reviewer 完成最终放行。
- 最终 findings 为 `P0=0, P1=0, P2=0, P3=0`。审查覆盖 live #111 最新 scope、approved planning、Docs SSOT、实现、测试、Phase 2、精确 task commit、开箱即用、upgrade/update、部署影响和 issue scope。

## Issue 关闭范围

Closes #111

### 仅引用

- Refs #98：父 umbrella，保留跨 Skill 编排上下文，本 PR 不关闭。
- Refs #53、#96、#97、#100、#105：消费 task-local/no-shared-write、archived finish-summary 与 PR refs 既有合同。
- Refs #109、#110：消费 Skill-first semantic profile 与 fresh base 上游合同。
- Refs #101、#112、#113：下游 review/workspace/clarification Skills，本 PR 只提供 context discovery 上游合同。

## Docs SSOT

- `docs_state`：`partial_docs`；`strategy`：`ssot_first`。
- `durable docs`：已更新 `docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/public-docs.md`、仓库 README、workflow README 与 preset README。
- `merged delta`：已回写 fixed order、workflow/standalone parity、freshness、duplicate projection、history query/scoring/digest、invalid isolation、deep-read/mem gate、same-snapshot persistence、typed exits 与 task-local/no-shared-write 边界。
- `task history`：scope correction、候选选择理由、sub-agent liveness、Phase 2 与三轮 Branch Review 过程仅保留为任务历史证据。
- `limitation`：exact feature-ref remote marketplace verification 由本次 finish-work 发布事务完成；下游 Skills 仍由对应 related issues 独立交付。

## 安全说明

- Artifact 持久化仅发生在 direct active task 目录；pre-task preview 保持 stdout-only，不写 workspace、runtime、repo-level index/cache 或共享状态。
- 不包含 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或持久化本机绝对路径；实现范围保持在 live #111 明确的正常调查与 correctness/reproducibility 合同内。
- 未修改 `.github/workflows`、Docker、Compose、Kubernetes/Kustomize/Helm、数据库 schema/migration、Makefile 或业务配置，无业务部署拓扑、运行时配置或数据库迁移要求。
- 回滚使用 Git revert，并从上一 extension ref 重新应用 workflow/preset；本 PR 不创建 release tag。
