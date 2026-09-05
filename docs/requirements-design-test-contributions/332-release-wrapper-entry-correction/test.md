# #332 Original-entry correction Test contribution

- `T332-ENTRY-01`（R332-ENTRY-01/04）：静态与 package contract tests 证明四个原 wrapper/command 为唯一
  public invocation，四个 PR #341 facade command/wrapper 在 canonical、installed、manifest 和所有平台
  projection 中均为零。
- `T332-ENTRY-02`（R332-ENTRY-02/03）：同一 fixture 分别运行 Happy 与旧参数形态，比较 typed exit、DTO、
  mutation、blocker、recovery 与 lifecycle；断言 Happy mode 未调用 compatibility primitive 或重复完整
  fact scan。
- `T332-ENTRY-03`（R332-ENTRY-09）：覆盖 Commit hooks/dirty/staged/stdout loss、Publication ready/metadata/
  content/external、Finalizer reprepare/adoption/stale/recovery、Merge watcher/head/base/policy/closure/output loss，
  确认语义和副作用边界未削弱。
- `T332-ENTRY-04`（R332-ENTRY-06/07）：以 `restore-archived-task.sh` 验证 source/installed validator、
  compatibility matrix、throwaway、runtime/eval 与 Shared/Codex/Claude/Cursor actual-load 均按 Interface
  选择 wrapper，并拒绝 private-script leak。
- `T332-ENTRY-05`（R332-ENTRY-08）：preset README、manifest、ownership inventory 与 installed disk
  inventory 一致；共享 scripts 下不存在 Skill-private facade，recursive `.new`/`.bak`/sidecar 为零。
- `T332-ENTRY-06`（R332-ENTRY-02/03）：operation-budget fixture 证明正常 command invocation 相对旧基线
  下降至少 50%，重复完整事实读取下降至少 70%，terminal typed exit 后当前 Skill operation 为 0。
- `T332-ENTRY-07`（R332-ENTRY-10）：从 live registry/interface 重新派生 23 Skills / 97 exits / 77 commands，
  `.44` 不变，task contribution 独立；serialized promotion 生成唯一 `.45` 后对新增 diff 重跑 Phase 2、
  commit 与完整 Branch Review。
- `T332-ENTRY-08`（R332-ENTRY-10）：preparation merge 后旧 candidate evidence 不被复用；新的 detached clean
  candidate 精确绑定 fresh `origin/main`，完整 #332 Release Gate 从零执行。

Planning 只审查范围、路径、owner、before/after 与可验证性，不把上述 implementation/release 结果标记为
已通过。
