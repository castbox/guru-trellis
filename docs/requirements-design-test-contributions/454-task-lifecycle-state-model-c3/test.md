# #454 C3 Checkout Substrate Test Contribution

状态：`reviewed_promoted`。以下测试是 `.60` C3 current acceptance authority；提升前 focused evidence 已通过，
但不证明 promotion-created diff、production activation、完整 installer/upgrade/workflow-switch/release-candidate
matrix 或 E434 retirement。

- `T454-C3-01`（R454-C3-01/03）：Draft 2020-12 校验 39 个 named DTO；四个 checkout DTO 各有正例，
  并拒绝 additional fields、valid candidate 的 null HEAD/branch、registered topology、dirty paths，以及
  resolved/selection-required shapes 之间的重复或缺失 identity；zero-candidate selection-required 保持正例，
  durable authority 字段继续被拒绝。
- `T454-C3-02`（R454-C3-02）：pre-task fixture 覆盖 clean invocation checkout、existing current-task artifact、
  another active task authority 以及 ambiguous authority；后三者必须在 mutation 前 fail closed。
- `T454-C3-03`（R454-C3-03/04）：resolution fixture 覆盖 zero/one/multiple candidate、wrong repository、
  detached、base branch、dirty、HEAD drift、explicit selection fresh revalidation 与 authority conflict non-downgrade。
- `T454-C3-04`（R454-C3-04）：adopt 覆盖 primary/linked checkout；provision 覆盖 new/reuse linked worktree，
  并断言 primary checkout target 返回 adoption route且不调用 worktree mutation。
- `T454-C3-05`（R454-C3-04/05）：transaction fixture 覆盖 create、post-create revalidation、bounded rollback、
  identity mismatch preservation、caller-owned preservation 与 output-loss read-only recovery。
- `T454-C3-06`（R454-C3-05）：schema/runtime 表驱动测试接受 letter/digit 起始及 `._:-` 后续字符，拒绝
  empty、leading separator、whitespace、slash 和其它 grammar 外 identifier。
- `T454-C3-07`（R454-C3-06）：shared runtime/contract tests 精确断言 error 的 `code`、`field_path`、
  `remediation`，并拒绝 message/details alias 与 unknown fields。
- `T454-C3-08`（R454-C3-07/08）：registry/schema 与 upstream ownership validator 断言 32 active package
  directories + 1 planned ID；`guru-ensure-task-checkout` 不得存在 canonical package directory，active selectors、
  active graph、workflow、installed/platform projection 中不得出现 C3 activation。
- `T454-C3-09`（R454-C3-01..08）：完整 lifecycle runtime 与 focused checkout suites、JSON parse、Python compile、
  task validation、workspace boundary、`git diff --check`、touched file line limit 和 zero legacy/path-authority
  static search 构成 C3 Phase 2 的 required deterministic evidence。
- `T454-C3-10`（R454-C3-08/09）：运行 preset suite 时，若 raw apply 因 forbidden-to-sync installed copies
  产生 `.bak` conflict，记录该 case 与 suite 为未通过；不得改 installed/platform bytes、不得把其改写成 C3 pass，
  完整 Release matrix 继续由专门 owner 验证。

以上测试不得创建真实 PR、merge、Issue closure、production activation 或 cleanup 副作用。

提升前 lifecycle runtime 为 `51/51`。Global package suite 保持 `19/20`，preset suite 保持 `85/86`；
两项 suite 都不声明为通过。Promotion-created diff 仍须 fresh Phase 2、Task Commit 与完整 Branch Review。
