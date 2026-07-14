## 变更摘要

- 新增公共闭环 Skill `guru-create-task-commit`，统一承接初次 Task work commit、Phase 2 后提交、Branch Review finding 修复提交和后续 revision commit。
- 将完整 dirty snapshot、Phase 2 evidence、Issue Scope Ledger、exact stage paths、中文 Conventional Commit bytes、AI Review 与授权绑定到连续 task-local plan；candidate validator 与 executor 共用唯一 commit message parser。
- 将普通文件、symlink、delete、rename、copy、gitlink、hook、Git operation、ref、live index 和 candidate result 收敛为 artifact-authorized 事务；`index.lock` 作为全程 sentinel，最终 candidate identity read 作为成功线性化点。
- 显式分离 `renamed_from` 与 `copied_from`：只有 rename source 继承 deletion/exact-stage authority，copy source 必须独立分类和接受 Phase 2 覆盖。
- 同步 canonical workflow、dogfood runtime、公共 skill package、Claude/Codex/Cursor/shared 安装副本、preset installer、manifest、README、requirements 与 workflow specs。

## 影响范围

- Workflow 只保留 mandatory skill invocation、finding-fix re-entry、typed exits 和 fail-closed routing；candidate、AI Gate、确认策略、executor 与 postcondition 由 skill-local contract 独占。
- Companion runtime 只解析、记录、校验和执行 Git/schema/digest/object 等确定性事实；scope、path classification、message 充分性、finding 和 route 仍由 AI 判断。
- Public schema 保持 `guru-task-commit-plan-1.0` / `1.0`；`copied_from` 为 optional additive field，历史 ordinary plans 无需迁移。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`，不接管 metadata commit、merge commit 或其它 issue 的发布流程。
- 不涉及 GitHub Actions、Docker/Compose、Kubernetes/Kustomize、Helm、数据库 migration、Makefile、运行时服务或数据迁移。

## 验证结果

- Copy/rename targeted：`8/8`；两个非同义 mutation probes：`2/2 rejected`。
- Task commit transaction：`39/39`；assignment/liveness：`30/30`；六个 package roots：`24/24`。
- 完整 suite：canonical package `4/4`、skill infrastructure `58/58`、runtime discovery `427/427`、preset `36/36`，合计 `525/525`。
- Clean throwaway exit 0，覆盖 fresh init/preset、initial/finding-fix commit、旧 plan reject、`trellis update --force`、workflow preview/switch/reapply、preset reapply、archive/ready projection 与 recursive sidecar 检查。
- Source/installed validator、dogfood overlay drift、Python/Bash/JSON/static、安全、部署、历史提交和 tree/blob/mode 审计通过。
- 远端 exact feature-ref marketplace verifier 是 Ready PR 的强制前置门禁；未通过时 finish-work 会 fail closed，不会把 PR 标记为 Ready。

## Review Gate

- Branch Review Gate 绑定 HEAD `9135d6e3414597bd75a5b5a13b4656a0bd0bfd89`，覆盖完整 `origin/main...HEAD` 的 7 个 task work commits 和 109 个 changed files。
- Round 1-9 的所有 P0/P1/P2/P3 finding 均有显式 findings=0 closure；Round 10 使用此前未参与实现、Phase 2、finding、closure 或 review round 的 fresh reviewer `trellis_final_review_122_04`。
- 最终结论为 `final release pass`，findings_count=0，P0/P1/P2/P3 均为 0。

## Issue 关闭范围

Closes #122

### 关联范围

- Refs #92：复用中文 Conventional Commits 唯一 parser/validator，本 PR 不关闭该 issue。
- Refs #120：复用公共闭环 Skill package 与 distribution 基础设施，本 PR 不关闭该 issue。

## Docs SSOT / 文档同步

- 状态与策略：`partial_docs / ssot_first`。
- `durable_docs`（durable docs）：已同步 `README.md`、`docs/requirements/README.md`、`docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`、workflow README 以及五份 `.trellis/spec/workflow/**` durable contract；canonical package contract、interface、schema、example、tests 与 runtime 承接可编码合同。
- `task_history`：task planning、Phase 2、finding lifecycle、liveness、candidate result 和 raw reports 只保留为任务历史证据，不形成第二份长期 SSOT。
- `followup_or_limitation`：remote marketplace verification 将由 finish-work 对已 push 的 exact feature ref 生成，不以本地 throwaway 结果冒充远端证据；无其它 follow-up。

## 安全说明

- 不包含 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- Candidate artifact 只记录 repo-relative path、digest、mode、Git object identity 和审查结论，不记录文件正文或 credential。
- 无应用部署、容器发布、运行时配置迁移、数据库迁移或回滚步骤。
- Executor 不执行 push、amend、rebase、reset、stash、force 或已发布历史改写；发布副作用只由通过 immutable plan digest 握手的 `trellis-finish-work` 执行。
