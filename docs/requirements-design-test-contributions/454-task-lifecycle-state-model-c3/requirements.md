# #454 C3 Checkout Substrate Requirements Contribution

状态：`contribution_candidate`。本 contribution 继承 active
`current-main-0.6.17-guru.59` Requirements、Design、Test 与 Architecture authority，
只承接 #454 C3 checkout acquisition/live resolution candidate。已提升的 C2+D0 contribution
保持 immutable；本目录不修改 shared current，也不授权 activation、promotion 或发布。

- `R454-C3-01`：C3 必须新增四个 named checkout DTO，分别承接 acquisition plan、candidate、
  resolution 与 selection。Machine path 只允许存在于 call-local DTO/transaction，不得进入 durable task、
  session、branch association、resource ledger 或跨 Skill public handoff。
- `R454-C3-02`：pre-task checkout acquisition 必须拒绝 invocation checkout 中已经存在当前 task artifact，
  或存在另一个 active task authority 的状态；不得覆盖、复用或静默切换该 authority。
- `R454-C3-03`：candidate 与 resolution 使用封闭状态集合，并拒绝状态、candidate 集合、selection、
  authority conflict 或 remediation 彼此矛盾的 payload。`valid` candidate 必须同时具有 live HEAD、branch ref、
  `primary | linked` topology 与空 dirty set；resolved shape 只携带 `selected_candidate_id`，selection-required/conflict
  shape 只携带 `candidate_ids`，其中 zero-candidate selection-required 保持合法。
- `R454-C3-04`：`adopt_invocation_checkout` 与 `provision_linked_worktree` 必须复用同一 live repository、
  checkout、branch、HEAD、dirty 与 task-artifact validator。Primary checkout 只能被 adopt，不得作为 provision
  target；需要 primary checkout 时必须返回 adoption route。
- `R454-C3-05`：checkout transaction/result 等 runtime identifier 必须使用共享语法
  `^[A-Za-z0-9][A-Za-z0-9._:-]*$`；schema 与 runtime 必须拒绝空值、leading separator、空白、slash
  及其它越界字符。
- `R454-C3-06`：shared checkout runtime error 只使用 dispatcher 共享字段 `code`、`field_path` 与
  `remediation`，三者语义必须精确；不得新增 message/details 别名或 package-private error shape。E434 后续
  public package 必须直接承接该 vocabulary。
- `R454-C3-07`：`guru-ensure-task-checkout` 在 C3 只预留 `state=planned` stable ID，canonical extension manifest
  只加入 `planned_skill_ids`。Planned row 不得携带 package/interface/I/O 字段，不得对应 canonical package
  directory，也不得被 source installer 或 active selector 选中；完整 package 由 E434 原子激活时交付。
- `R454-C3-08`：C3 不得修改 active registry selector、`active_skill_ids`、active graph manifest、
  production workflow、installed Guru copy或 Codex/Claude/Cursor/OpenCode projection。E434 独占后续 activation
  与 predecessor retirement。
- `R454-C3-09`：C3 acceptance 只绑定 shared schema、lifecycle runtime、active canonical package inventory、planned ownership、
  source validation、静态 legacy/path-authority 搜索与通用结构检查。完整 Release matrix 保持 unverified；raw
  preset apply 若因 canonical C3 bytes 与故意未同步的 installed bytes 产生 conflict，必须如实报告为未通过，
  不得通过同步 installed/platform projection 使该测试变绿。

C4-C7、D443、D436 与 E434 保持独立后续范围。本 contribution 不授权 commit、push、PR、merge、
shared-current promotion、Issue closure 或 cleanup。
