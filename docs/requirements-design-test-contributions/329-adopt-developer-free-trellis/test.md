# #329 Developer-free Trellis adoption Test contribution

状态：`reviewed_promoted`；current successor：`current-main-0.6.5-guru.49`。下列条目定义稳定验证合同，
不记录尚未执行的 PASS，也不把 focused fixture 结果表述为完整 adoption、release 或 business smoke 证明。

- `T329-01`：验证 source lock、CLI `0.6.17`、`pnpm@10.32.1`、Fork HEAD、source marker、Guru
  manifest、installed source record、README 与 RDT/Architecture candidate 的 exact identity 一致。
- `T329-02`：验证 Trellis-owned dogfood/installed files 来自 fixed `0.6.17` official generation/update，
  Guru-owned files 来自 canonical preset；ownership、template hash、byte/mode parity、drift 与 sidecar gate 通过。
- `T329-03`：验证 active Guru caller/consumer graph 不调用 developer identity、workspace journal/index、
  session recording 或 `--mine`；保留引用必须分类为 upstream retired stub、negative/preservation test、
  current migration docs 或 immutable history。
- `T329-04`：验证 current-task resolution 在 valid linked worktree 中只消费 task/Git/runtime mapping facts；
  mapping missing、duplicate 或 mismatch 返回 `invalid_task_state`，不回退 legacy identity。
- `T329-05`：验证 task create 显式 creator/assignee、GitHub caller preflight 和 unresolved-owner write-before-fail；
  已有 task read/resume 不要求重复 person identity。
- `T329-06`：对 legacy absent、present-A、present-B 比较 lifecycle outcome；present fixture 的 path set、
  symlink identity、mode 与 bytes 在 update/reapply 前后完全一致。
- `T329-07`：Codex、Claude、Cursor 分别执行 clean install、existing update、reapply、linked worktree、
  new session、resume、task create、planning、implementation/check、commit/review/publication/finalization/archive
  代表入口，全部使用 target managed runtime；未发布 local workflow sample 明确报告本地 candidate boundary，
  不作为 exact remote marketplace proof。
- `T329-08`：验证 RDT/Architecture contribution、direct-evolution subtraction、3000-line touched-source review、
  task validation、schema/JSON/Python/Bash checks、`git diff --check` 与 independent full-diff Branch Review；
  installed closeout 只接受 clean committed candidate source provenance，capability comparison 对删除/缺失阻塞并
  单独接受 additive-only evolution。

## Fixed scenarios

| Scenario | Expected result |
| --- | --- |
| `SCN-079 clean developer-free install` | fixed Fork init 与 Guru preset apply 后不创建 identity/workspace/journal；session bootstrap 与 task resolution 使用明确 task/Git facts。 |
| `SCN-080 existing update and reapply` | dry-run 选择 retirement migration 后，以已审查 managed replacement、显式 assignee 和 `--force --migrate --skip-all` 完成 official update；同 provider workflow apply 后无 unresolved sidecar，非 managed 用户数据按官方冲突语义保留，第二次执行结果稳定。 |
| `SCN-081 explicit task owner` | creator/assignee 来自显式 metadata 或通过 preflight 的 authenticated GitHub caller；无 authority 时任何 write 前停止。 |
| `SCN-082 linked-worktree lifecycle` | 三平台 task lifecycle 在 linked worktree 中绑定同一 task/worktree mappings，不读取 developer identity 或 journal。 |
| `SCN-083 legacy preservation` | absent 保持 absent；present-A 与 present-B 的 path、mode、bytes 不变，三种 fixture 在相同 task/Git/caller authority 下结果一致。 |
| `SCN-084 unpublished sample and clean provenance` | local workflow sample 从 bundled `native` 初始化后安装本地 candidate 并报告 unpublished boundary；installed closeout 从 clean committed candidate source reapply，纯新增 capability 不构成 regression。 |
