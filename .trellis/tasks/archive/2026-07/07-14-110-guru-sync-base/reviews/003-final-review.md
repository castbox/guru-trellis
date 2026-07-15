# 第 3 轮最终放行审查

## 审查身份与范围

- 角色：`最终放行审查代理`
- 技术代理：`/root/branch_review_110_release`
- 审查 HEAD：`420602b34759b7299861a7ab5b1a3a9876873419`
- 基线：`origin/main`（`f9f094f0a995e230226c8a94ff34944ba9d87b53`）
- 完整差异：`origin/main...420602b34759b7299861a7ab5b1a3a9876873419`
- 差异规模：104 个文件、13418 行新增、589 行删除、2 个工作提交
- 审查方式：从未参与 earlier review round 的全新技术代理独立全量审查。

## Findings

- `findings_count=1`
- P0：0
- P1：1
- P2：0
- P3：0

### F-006 [P1] `synced` 前清理 resolution evidence，使唯一 consumer 无法执行 `prepare-task`

证据：

1. Canonical Skill 在 `trellis/skills/guru-team/packages/guru-sync-base/references/contract.md` 中规定 `objective result validation -> evidence cleanup -> typed exit`。
2. 同一合同又要求每次后续 `prepare-task` 必须接收同一个 external resolution file 及 digest。
3. Task `design.md` 同样规定 Skill 删除临时 evidence 后才返回 typed exit。
4. Workflow 只有收到 `synced` 后才进入 context discovery、`check-env` 与 `prepare-task`，随后命令强制传入该 resolution file。
5. Runtime `read_base_sync_evidence()` 与 `cmd_prepare()` 必须读取现存 canonical file；文件不存在时 fail closed，没有替代输入。
6. Throwaway verifier 只覆盖 standalone `resolve -> execute -> validate -> rm`，没有调用 `prepare-task.sh`，因此未覆盖真实 `synced -> prepare-task` 链路。

影响：

- 严格执行 Skill cleanup 后，正常 issue-backed workflow 的第一个 `prepare-task` 必然因 resolution file 已删除而阻塞。
- 保留文件让流程继续，又违反 step-local Skill 的 evidence lifecycle 与 typed-exit 合同。
- Planner、create-issue、worktree、task mutation 的多次 freshness rerun 都依赖该文件。
- 当前 fresh-install/update evidence 不能证明 Phase 0 链路开箱即用。

修复要求：

- 统一 resolution evidence 的唯一生命周期与清理所有权，不能只删除单处文案。
- 定义跨 Phase 0 consumer 的受控 lease，并在最后一次 `prepare-task` consumer 后确定性清理；或定义 typed exit 携带可安全重新物化的 canonical bytes/digest 并让 prepare 使用明确接口。
- 同步 planning、canonical Skill/interface、workflow、durable requirements/spec、README 与全部受管副本。
- Throwaway 必须真实覆盖 fresh install 后的 `resolve -> pre-execution review/confirmation -> execute -> post-execution AI Gate -> validator -> synced -> prepare planner/mutation guard -> cleanup`，并断言零残留 evidence/sidecar。
- 修复后重新执行完整 Phase 2、创建 finding-fix commit，再完成问题闭环与全新的最终放行审查。

## 其余审查证据

- Live issue 状态：`#110`、`#98`、`#111` 均为 OPEN；scope 为关闭 `#110`、关联 `#98`、后续 `#111`。
- 三份 planning 文档 digest 与 schema 1.2 approval 一致；confirmation-before-executor 与 post-execution AI Gate-before-validator 已正确修订。
- Round 1 的 F-001 至 F-003 及后续 F-004、F-005 在当前 HEAD 均已闭环；F-006 来自本轮独立全量审查。
- Runtime resolver、canonical raw bytes、digest/source identity 重算、显式 refspec fetch、selected-checkout `ff-only`、三方 HEAD equality、live validator 与 `prepare-task` mutation 前 rerun 未发现其它缺陷。
- 独立复验通过：BaseSync runtime 12 项、package contract 5 项、source/distribution 35 项，共 52 项；Phase 2 记录全套 396 项通过。
- Canonical/installed runtime、canonical/dogfood workflow byte-identical；六份 package 的 8 个文件与 mode 一致。
- Commit `420602b` 的 parent、28 个 exact paths 与 tree `c5f43865818aecde1a068b5d4bab7c9449aafbe9` 一致，`hook_mutation=false`。
- 当前未提交内容仅为 task-local Branch Review/commit metadata；`git diff --check` 与 JSON/Bash 静态检查通过，无 `.new`、`.bak` 或 non-metadata drift。

## Docs SSOT

F-001 至 F-005 的 durable contract 已同步，但 F-006 证明 canonical Skill、task design、workflow consumer 与 throwaway acceptance path 对 resolution evidence 生命周期存在 current-scope 冲突。Docs SSOT 本轮不通过，必须在修复中统一长期合同并同步受管副本。

## 开箱即用与 Upgrade/Update

- Local fresh install、workflow preview/switch、preset apply、`trellis update`、reapply、managed inventory 与 zero-sidecar evidence 已存在。
- 因 F-006 未覆盖且真实链路当前不可同时满足合同，不能声明 Phase 0 workflow 开箱即用。
- 真实远端 branch-pinned marketplace verification 尚未执行，仍为 push 后 publish gate pending。

## 部署与安全

- 未修改 CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 migration/schema 或 Makefile。
- 未发现 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或真实本机绝对路径泄漏。

## 观察项

1. 真实远端 marketplace verification 必须在最终 reviewed HEAD push 后执行。
2. `issue-scope-ledger.json.acceptance_evidence` 必须在 publish 前补齐。

## 后续候选

1. `#111` 保持独立 follow-up，不承担 F-006。

## 结论

本轮 `findings_count=1`（P1=1）。F-006 属于 `#110` 当前闭环与开箱即用合同，阻塞 Branch Review Gate；不得进入 `trellis-finish-work`、push、PR 或 issue close。必须返回实现阶段修复，重新执行完整 Phase 2、创建 finding-fix commit，再完成 closure review 和全新最终放行审查。
