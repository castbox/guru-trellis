# 最终放行审查

## 审查身份

- 逻辑角色：最终放行审查代理（本轮发现问题后成为 finding owner）
- Technical agent id：`issue114-final-review-r1`
- Primary issue：`#114`
- Reviewed HEAD：`dfde7dd37dc74848805c88f97e423e01a9e26f33`
- Diff range：`origin/main...HEAD`
- Findings count：`1`
- 审查方式：独立语义审查；未修改文件，未提交，未 push，未运行 Guru Team recorder/validator。

## 审查范围

- 完整审查 `origin/main...HEAD` 的 88 个 committed paths。
- 读取 `prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、`phase2-check.json`、`contract-wording-review.json`、`planning-approval.json`、`issue-scope-ledger.json`、`agent-assignment.json` 与 `task-commit-plans/001.json`。
- 审查 canonical Skill、shared runtime、workflow、schema、registry、extension manifest、preset installer、throwaway verifier 及 Agents/Codex/Cursor/Claude 分发副本。
- 复核 durable requirements、workflow/preset README 和 `.trellis/spec/` 六份相关规范。
- 检查 legacy owner 删除、archived task 边界、排除 issue 范围、部署资产与安全边界。
- 当前工作区仅保留既有提交后 metadata tail：`agent-assignment.json` 与 `task-commit-plans/001.json`；未覆盖或回退。

## Findings

### P2：Extension public API 未登记新的 task-local evidence artifact

- `trellis/guru-team-extension.json:39` 的 `public_api.artifact_contracts` 未包含 `contract-wording-review.json`。
- 新 workflow 已把该文件定义为正式 planning artifact：`trellis/workflows/guru-team/workflow.md:443`。
- Durable requirements 同样把它定义为 `guru-review-contract-wording` 的持久化 evidence：`docs/requirements/requirement-main.md:183`。
- 实际 runtime 会为 `planning_artifacts` 写入该 task-local tracked artifact，planning approval 也依赖其 public schema、facts/scope/scan identity；因此 extension manifest 的 artifact inventory 与 workflow、runtime、Docs SSOT 不一致。
- 现有 installer manifest 测试只断言旧 artifact：`trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py:1165`，没有覆盖新 artifact，导致该遗漏未被 39 个 preset tests 捕获。
- 这是正常安装路径即可观察的 public contract 缺口，不依赖伪造、篡改或非常规并发。
- Required fix：在 canonical extension manifest 的 `public_api.artifact_contracts` 中加入 `contract-wording-review.json`，同步 installed manifest，并增加 installer/public API 回归断言。
- 该修复属于非 metadata source 变更，必须返回 implementation、完整 Phase 2 check 和新的 committed HEAD，再重新进行 Branch Review。

## Docs SSOT 判断

- Docs SSOT strategy 为 `ssot_first`，canonical package contract、workflow、dogfood workflow、durable requirements、README 和相关 specs 已完成大范围同步。
- Vocabulary、classification 和 semantic loop 的完整定义仅存在于 canonical package/runtime 及其生成副本；active workflow/docs 未形成第二 semantic owner。
- Extension public API artifact inventory 未承接 durable docs 已声明的 `contract-wording-review.json`，因此当前 Docs SSOT 与公开 manifest 尚未完全收敛。
- 结论：Docs SSOT 存在 blocking inconsistency，不能通过最终放行。

## 部署与安全判断

- 完整 diff 未修改 `.github/workflows/`、Dockerfile、Docker Compose、容器启动脚本、Kubernetes/Kustomize/Helm、数据库 migration/seed 或 Makefile。
- 变更属于 workflow marketplace、Skill runtime、schema、preset installer、public manifest、文档和生成分发副本，不涉及服务部署或数据库迁移。
- 未发现 token、secret、`.env`、签名 URL、客户数据或敏感原始记录进入新增 package、example、task evidence 或文档。
- 未把 `#101`、`#112`、`#129`、`#132` 的后续职责纳入实现；恶意篡改、对抗输入和非常规并发加固也未被重新引入。
- 安全与部署范围本身无额外 finding。

## 证据

- 工作区边界：expected workspace 与 actual repo root 均为当前 task worktree；source checkout 干净，无 suspicious source artifacts。
- HEAD 在审查开始和结束时均为 `dfde7dd37dc74848805c88f97e423e01a9e26f33`。
- `origin/main...HEAD` 仅有一个 task work commit，commit subject/body 满足中文 Conventional Commits 与 `Refs #114` 边界。
- 独立复跑：package tests `14/14 passed`、runtime tests `500/500 passed`、preset tests `39/39 passed`、Python compile 通过、Bash syntax 通过、`git diff --check origin/main...HEAD` 通过。
- 六份 package 树共 8 个文件在 canonical、installed、Agents、Codex、Cursor、Claude 之间逐文件 SHA-256 一致。
- Canonical 与 dogfood workflow 字节一致；canonical 与 installed registry 字节一致。
- Legacy 搜索仅命中 `--normative-hit` 的负向测试断言；未发现 active `PLANNING_AMBIGUITY_*`、planning 专用 scanner/parser/helper 或旧 CLI usage。
- `origin/main...HEAD` 未修改 `.trellis/tasks/archive/**`。
- Planning evidence 中三份文档的 hash/size 与当前文件一致；wording facts、scope、scan digests 均可重新计算匹配，planning approval binding 一致。
- `task-commit-plans/001.json` 的 committed paths 与完整 branch diff 均为 88 项，无遗漏或额外 committed path。
- Phase 2 的 local unpublished workflow throwaway、三 profile、planning compatibility、closeout、`trellis update --force`、preset reapply 和全平台安装证据有实现脚本与 agent liveness/completion 记录支撑。
- Remote public marketplace 因网络不可达仍是 publish 前 gate limitation，未被误写为已验证。

## 观察项

- Remote public marketplace 的真实 branch/tag 安装仍须在 branch push 后由 publish gate 验证；当前仅有本地 unpublished workflow 与独立全平台 throwaway/update-reapply 证据。
- `issue-scope-ledger.json` 中 `#114` 的 `acceptance_evidence` 当前为空，并已明确标记 publish 前补齐；该状态不替代本轮 finding，也不能在 publish 时被跳过。

## 后续候选

无。当前问题属于 Issue #114 范围内必须修复的 public API 一致性缺陷，不应转为 follow-up。

## 结论

- 最终结论：不通过
- Reviewed HEAD：`dfde7dd37dc74848805c88f97e423e01a9e26f33`
- Diff range：`origin/main...HEAD`
- Findings count：`1`
- 阻塞 finding：`1 x P2`
- 必须修复 extension `artifact_contracts` 与对应 installer 测试后，重新执行 implementation、完整 Phase 2 check、task commit 和 fresh Branch Review。
