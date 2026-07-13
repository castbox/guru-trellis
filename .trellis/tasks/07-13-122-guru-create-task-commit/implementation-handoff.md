# #122 实现交接

## 结论

`guru-create-task-commit` 已按 `ssot_first` 策略完成 durable docs、canonical
package、runtime、workflow、preset、platform entry、dogfood copy 与测试实现。本交接只
记录实现代理事实，不能替代后续独立 `trellis-check`、`phase2-check.json` 或 Branch
Review Gate。

## R1-R10 承接

| 需求 | 实现结果 |
| --- | --- |
| R1 | production registry 保留 `guru-create-work-commit` reserved tombstone，并激活 `guru-create-task-commit`；extension `0.6.5-guru.5` 登记 skill、artifact schema 与 executor public API。 |
| R2 | canonical/dogfood workflow 只有 1 个 mandatory invoke marker 和 3 个唯一 typed-exit consumers；finding-fix 返回 Phase 2 后重新进入同一 skill。 |
| R3 | candidate validator 绑定 worktree/task/status、planning approval、Phase 2、ledger、base、HEAD 与 NUL-delimited 完整 dirty snapshot。 |
| R4 | package 提供 `task-commit-plans/<sequence>.json` schema/example；AI candidate 记录 exact paths/message/review/authorization/freshness/result，不记录文件正文或本机绝对路径。 |
| R5 | validator 强制四类 path 全覆盖；executor 使用 literal exact path stage，拒绝 artifact 外 staged path，并保留 unrelated 状态。 |
| R6 | Markdown contract 独占 AI Review Gate、conditional confirmation 与 route 判断；runtime 只验证已记录事实。 |
| R7 | `check-commit-messages --candidate-artifact` 复用唯一 `validate_commit_message()`；`create-task-commit` 使用 exact message file 与 `--cleanup=verbatim -F`。 |
| R8 | postcondition 验证 parent、raw message bytes、committed paths、shared parser、unrelated preservation、index/hook mutation，并原子回写唯一 exit；旧 sequence 在新提交后失效。 |
| R9 | step-local 正文只在 canonical package `references/contract.md`；workflow 与五个 continue entry 只保留 stable skill invoke/exit/re-entry。 |
| R10 | preset 向 installed canonical、shared、Codex、Cursor、Claude 分发 package；managed wrapper、manifest、README、dogfood copy、throwaway update/reapply 均已覆盖。 |

## Docs SSOT

- Strategy：`ssot_first`。
- Durable owners 已先于 runtime/schema/installer 实现更新：三份 requirements
  文档、七份 workflow/preset/docs spec、顶层 README、workflow README 与 preset
  README。
- Task delta 已合并：active/reserved id migration、artifact/executor、typed exits、
  re-entry、分发与 upgrade/reapply 合同均进入 durable owner。
- Throwaway 新发现的 Phase 2 self-artifact 递归 digest 缺口已合并到
  `.trellis/spec/workflow/data-contracts.md` 与 package contract：只有 candidate 中
  已绑定 fresh digest 的当前 `phase2-check.json` self path 获得窄 coverage 例外，
  不扩展到其它 task/source/docs/schema/preset/overlay 路径。
- 本任务 `design.md` 第 14 节列出的 durable evidence paths 均有语义变更，无
  no-change evidence path。
- Task-history-only：planning approval、单次命令输出、临时 throwaway repo、真实
  smoke commit SHA、sidecar 处理过程与本交接保留在 task evidence，不进入公共
  package。

## 分发与升级

- Canonical preset apply 最终幂等：`updated_managed=[]`、
  `managed_backups=[]`。
- 首次同步本轮 delta 生成 1 个 runtime 与 5 个 package contract 已知升级 `.bak`；
  已逐个确认只含旧 managed bytes，清理失败 provenance manifest 后由 installer
  重建。
- 最终 source/installed validator：reserved 1、active 1、invoke 1、exit 3；
  dogfood selected platforms 为 Claude/Codex/Cursor，managed skill files 43，
  conflict/removal/sidecar 均为 0。
- Canonical workflow 与 `.trellis/workflow.md` 字节一致；canonical runtime 与
  dogfood runtime 字节一致；overlay drift 通过。

## 验证证据

- Targeted candidate/executor tests：7/7 通过，包含 dirty
  `phase2-check.json` self-evidence 回归。
- Package/preset/runtime full suite：484 tests，124.443s，`OK`。
- Clean throwaway：公开 marketplace discovery 后使用当前未发布 canonical workflow
  样本，preset install 与 source/installed discovery 通过。
- Throwaway initial commit：`e6ce08e097e00355305fd85b416f9f714abb5272`，
  parent `baa5c24c3197cc1e40f3d58b3cefb59edff8fa36`，sequence `001`，
  exact paths 包含 task evidence、fresh Phase 2、candidate 与 source fixture。
- Throwaway finding-fix commit：`217fb13577306d83be2ae2e52ba90b8de0ff2f49`，
  parent 为 initial commit，sequence `002`，包含 fresh Phase 2、sequence 001
  post-result、sequence 002 与 source fix；旧 plan candidate 返回非零。
- 两轮真实 executor 均返回 `status=committed` / `exit=committed`，unrelated file
  内容与 untracked 状态在两轮提交后保持不变。
- Throwaway 后续 `trellis update --force`、workflow preview/switch、workflow
  reapply、preset reapply、source/installed validation、dogfood drift、closeout smoke
  与最终 recursive sidecar scan 全部通过。
- Task validation、phase 2.2/3.4/3.5 context parsing、JSON parse、`py_compile`、
  全量 Bash syntax、`git diff --check`、公共 package/manifest/README 安全扫描通过。

## AC 状态

- AC1-AC11：本地实现与验证证据已覆盖，交由独立 checker 复核语义充分性。
- AC12：local throwaway 已通过；remote current feature-ref marketplace verifier
  仍按合同延后到 reviewed content push 后由 `trellis-finish-work` 生成，当前不能
  宣称 remote feature-ref 已验证。
- AC13：ledger 只把 #122 放入 `close_issues`；#92、#120 仅在
  `related_issues`，work message 只使用 `Refs #122`。
- AC14：公共 package/schema/example/manifest/README 未发现 secret、客户数据、
  `.env` 内容、签名 URL或本机绝对路径。

## 部署与安全影响

本任务只修改 Trellis workflow/preset/runtime/package/docs/test 资产，不增加应用
service、CLI runtime service、worker、queue、migration 或 runtime config。未修改
GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、数据库 migration 或
Makefile；无需部署资产同步。Executor 不打印 dirty file content，不 push、不改写历史，
temporary message file 使用 `0600` 并在 `finally` 删除。

## 后续门禁与剩余风险

1. 独立 `trellis-check` 仍需覆盖 R1-R10、AC1-AC14、完整 dirty diff、Docs SSOT、
   parser compatibility、installer/update/security/deployment，并记录
   `phase2-check.json`。
2. 通过 Phase 2 后才使用当前 skill 为本任务创建真实 task work commit；本交接阶段
   未 commit 当前分支。
3. Work commit 后仍需独立 Branch Review Gate；本交接阶段未运行 Branch Review。
4. 当前分支未 push，因此 local throwaway 的 marketplace discovery 来自公开
   `main`，随后明确覆盖当前 canonical workflow 样本完成本地验证。Remote exact
   feature-ref discovery 是唯一已知未覆盖的开箱即用证据，必须在 publish 前补齐。
5. Throwaway 观察到本机 npm 最新 Trellis 为 `0.6.6`，本扩展的已批准兼容目标仍是
   `0.6.5`；本任务不扩展 CLI baseline，后续升级需单独执行兼容性评估。
