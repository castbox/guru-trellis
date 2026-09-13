# #247 Issue Scope Ledger retirement Design contribution

本 candidate 采用 `target_native`，保持 23 Skills / 97 exits / 78 commands 与四阶段 workflow
顺序，直接建立无 ledger aggregate 的 authority boundary，并同步迁移受控 consumer。

- `D247-01`：Workspace owner 删除 ledger authoring、writer、artifact declaration、checker reader、
  schema/example/eval/test；created output只保留 official task identity 和唯一 consumer 必需数据。
- `D247-02`：Clarification、Planning、qualification、Phase 2、Commit、Branch Review 各自 fresh
  读取 current requirement、planning、source、Git 与 diff，不传递 `scope_ledger_path`、
  `primary_issue` 或 Issue classification arrays。
- `D247-03`：Publication owner 从 current requirement、reviewed full diff、validation、target/default
  branch 与 live GitHub facts唯一形成 PR payload 和 closure decision；Issue-backed completed 默认关闭，
  remain-open 必须有明确 current-authority 原因，reference 与 closure intent 是不同语义。
- `D247-04`：默认分支 PR 由 Publication 在 body 编码 closing keyword；非默认分支 PR 只引用，后续
  目标默认分支 Publication fresh 判断。Finalizer 只绑定已 reviewed PR payload 和 exact
  task/base/head identity；正常、existing-PR 与 terminal recovery使用同一规则。
- `D247-05`：Merge 独立重读 live PR/GitHub facts并完成 readiness semantic review、confirmation、
  expected-head 与 closure verification，但不重判关闭决定、不调用 Issue close API；
  Finish/Restore/Cleanup不消费 Issue aggregate。
- `D247-06`：所有仅服务 ledger 的 package contract、runtime、script、schema、DTO、example、eval、
  fixture、test、manifest、registry、README/spec 内容直接删除；共享文件只移除 ledger-owned 分支。
- `D247-07`：canonical 是唯一编辑源，preset reapply同步 dogfood 与 Shared/Codex/Claude/Cursor；
  source/installed/ownership/drift/sidecar检查验证 current package unit一致。
- `D247-08`：legacy ledger path 不属于新 managed inventory；preset/update不主动触碰，current runtime
  不打开。旧 task不迁移、不转换、不建立兼容测试；历史 archive/ADR/superseded/released RDT保持不变。

Architecture inheritance 由
[`architecture-contribution-247-remove-issue-scope-ledger-v1`](../../architecture/contributions/247-remove-issue-scope-ledger.md)
和 [`ADR-009-CANDIDATE`](../../architecture/adr/009-issue-reference-closure-ownership.md) 拥有。
实现若要求新增 owner、public Skill、graph router、替代 aggregate、兼容层或 #305 target 重构，
本 Planning result 立即 stale 并返回对应 semantic owner。
