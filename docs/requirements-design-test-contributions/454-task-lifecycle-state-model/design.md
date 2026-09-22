# #454 Task Lifecycle State Model Design Contribution

状态：`reviewed_promoted`。采用 `target_native`，关联
`architecture-contribution-454-task-lifecycle-state-model-v1`，expected current 为
`current-main-0.6.17-guru.58`，promoted successor 为 `current-main-0.6.17-guru.59`。

- `D454-01`：`task-lifecycle-dtos.schema.json` 是单一 Draft 2020-12 catalog，声明 35 个 named DTO。
  Top-level union 只用于 catalog 完整性，不作为 package public output；consumer 选择 exact `$defs/*DTO`。
  Handoff receipt 使用专用 control-ref primitive，terminal cleanup 与 Delivery remaining-work 字段保持封闭。
- `D454-02`：`identity.py` 分离 TaskId、TaskRef 与 generation，扫描 active/archive canonical artifacts，拒绝
  symlink/non-canonical locator、control-ref-invalid TaskId、exact/case-fold collision 与 invalid generation，并返回
  immutable `TaskArtifactIdentity`。
- `D454-03`：`source.py` 只规范化 closed source union、portable `owner/repository` ref、Git-valid branch ref 与
  Delivery target；schema 与 runtime 使用相同值域。它不拥有 Closure disposition、branch association、checkout
  acquisition 或 Git mutation。
- `D454-04`：`schema.py` 从固定 sibling contract root 加载 regular schema，验证 Draft 2020-12，拒绝 remote/parent
  `$ref`、nested `$id`、symlink escape 与 unknown DTO；`results.py` 只构造 minimal named DTO。
- `D454-05`：`LifecycleContractError` 提供稳定 code/field/remediation/details。Runtime 不写 task/session/mapping，
  不导入 Fork private code，不修复 metadata，不选择 semantic route，也不持久化 validation result。
- `D454-06`：Fork source lock 固定到 reviewed commit `eb370008c7689d4e272ae626bd002190ecbb3296`、tree
  `bd1f133cc55d0562ad9ec5f426bca70d1584194b` 与 CI `35621578090`。四份 workflow SSOT 在 canonical/preset
  保持字节一致；task-owned contribution 保持 pending，C3-C6 与 #434 activation 不提前投影。
- `D454-07`：D0由`guru-reconcile-task-base`拥有pre/post-review integration，`guru-create-task-commit`只输出exact
  committed candidate，`guru-review-branch`分别拥有full与continuity profile。Pre-review pair由fresh selected base与
  唯一merge-base派生，compatible route创建parents为`[prior_task_head, new_base_head]`的本地merge commit；
  `post_check/post_commit`回fresh Phase 2。Continuity只允许post-Branch-Review/Publication/Finalizer，且验证prior
  full-review commit、new base ancestry与candidate tree identity。
