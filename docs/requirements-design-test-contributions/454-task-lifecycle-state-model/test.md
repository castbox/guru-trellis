# #454 Task Lifecycle State Model Test Contribution

状态：`candidate_pending_review`。以下是 C2 focused acceptance；它不等同于 C3-C6、production activation 或完整
Release matrix。

- `T454-01`：catalog 必须通过 Draft 2020-12 schema check，且 35 个 named DTO 各有一个 positive payload。
- `T454-02`：每个 DTO 拒绝 additional `authorization`；TaskArtifact additionally rejects machine path、session、
  generic evidence 与 undeclared Git fields。
- `T454-03`：TaskId/TaskRef rename 与 archive fixture 保持同一 TaskId/generation；control-ref-invalid TaskId、
  exact/case-fold collision、expected-id mismatch、symlink-backed store 与 invalid locator fail closed。
- `T454-04`：legacy missing generation 读取为 0；boolean、负数、浮点、字符串与 null generation fail closed。
- `T454-05`：仅 `IssueSource | NoIssueSource` 合法；repository schema/runtime 都拒绝 invalid component 与 `.git`
  suffix，branch schema/runtime 对齐 `git check-ref-format --branch` 并额外拒绝 remote-tracking namespace；Delivery
  target 拒绝 URL/local path、traversal 与附加 head 字段。Handoff receipt 必须位于 TaskId-stable control namespace，
  cleanup/remaining-work 字段拒绝未声明状态。
- `T454-06`：schema loader 拒绝 remote ref、parent ref、nested `$id` 与 contract-root escape；source/copy catalog
  identity 相同。
- `T454-07`：Fork preparation test 从 canonical source lock读取 commit/CI，并约束三份 README；task validation、
  JSON parse、Python compile、canonical/preset SSOT equality 与 `git diff --check` 必须通过。
- `T454-08`：静态边界证明 `.trellis/scripts/**` diff 为零，新 runtime 无 workspace mapping、second session store、
  durable identity index、compatibility alias、dual-read/dual-write；每个 touched non-generated runtime 文件低于
  3000 行。

不运行或宣称完整多平台 installer、upgrade、workflow-switch、marketplace、release-candidate、registry closure、
active graph、installed/platform projection 或真实 business mutation evidence。
