# #350 Requirements Contribution

在合法 base evolution 加单一 provenance metadata tail 的 Finalizer recovery 中，fresh Publication Review 会正常更新 PR body。旧 rebind predicate 不应把该 payload mismatch 当成身份漂移。

- task、repository、base/head branch、close-Issue scope、PR/remote HEAD 与 Git topology 仍须精确成立。
- title/body mismatch 仅在 exact base evolution 加单一合法 provenance tail 的组合拓扑中作为 existing-PR metadata convergence 输入；pure base evolution 与 direct tail 继续要求 predecessor payload 精确一致。
- 不新增 public I/O、typed exit、transaction stage/schema，不修改 PR #337 或 #333 transaction。
