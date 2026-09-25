# #454 C5 Session And Resource Control Test Contribution

状态：`reviewed_promoted`，successor 为 `current-main-0.6.17-guru.63`。以下 focused acceptance 不构成 Phase 2、promotion-created diff Branch Review、
Publication、production activation 或 Release Gate 证明。

- `T454-C5-01`（R454-C5-01/02）：official fake/fixture 覆盖 exact schema-2 record、extra field rejection、context key
  present/absent、explicit-task mode、stale generation在write前拒绝，以及session write failure不触发lifecycle rollback。
- `T454-C5-02`（R454-C5-03）：覆盖多 session、同 session A-to-B-to-A、TaskRef move 后 fresh resolve 与 generation
  mismatch invalidation。
- `T454-C5-03`（R454-C5-04/06）：Draft 2020-12 与 runtime 同时验证 ledger closed shape、resource incarnation、
  ledger revision、epoch/revision/branch alignment，以及 C4 `OwnershipPort` current/snapshot/restore contract。
- `T454-C5-04`（R454-C5-05）：active ledger missing 以 pre-existing facts恢复 caller-owned；conflict 独立失败；
  exact successor output-loss retry只读rematerialize；terminal missing返回manual-selection且不创建ledger。
- `T454-C5-05`（R454-C5-07）：rebind 保留旧 incarnation，Guru-owned retired进入cleanup-pending，caller-owned retired
  保持 retained；未收敛同 ref阻止复用。
- `T454-C5-06`（R454-C5-08/09）：remote current-delivery role与current branch/ref alignment、exact current
  incarnation只读恢复、同仓库多个remote name的精确定位、无关合法ledger mutation后仍可rematerialize、Finish seal
  把 exact `finish_head` 写入最后一个 current Guru-owned incarnation 并返回完整inventory、ordinary cleanup仅返回
  带可验证 HEAD 的 Guru-owned cleanup-pending、caller/unknown与retained-control refs排除，并验证control ref
  runtime/schema同域。另以真实 Git ancestry 覆盖同一 remote H1→H2 的同 incarnation推进、相同 HEAD 无写重试、
  旧 HEAD 回退拒绝、首次 Guru-owned remote 无 HEAD 拒绝、rebind 封存最新 H2，以及 caller-owned conservative
  recovery 从无 HEAD 补入已验证 HEAD 且保持 origin；schema/runtime 同步约束 Guru-owned remote cleanup HEAD。
- `T454-C5-07`（R454-C5-10）：unique candidate自动选择；zero/multiple返回selection-required；discovered与explicit
  target使用同一 fresh validation，explicit target不能覆盖非法repository/task/generation/branch/resource事实。
- `T454-C5-08`（R454-C5-11）：canonical registry断言新增ID仅planned、无package/interface/command/active graph/
  installed/platform projection。
- `T454-C5-09`（R454-C5-01..11）：完整 task-lifecycle focused runtime、三个schema、Python compile、task validation、
  touched file line limit与`git diff --check`只形成当前candidate supporting evidence。

完整 installer/upgrade/workflow-switch/multi-platform Release matrix 保持 deferred；不得通过同步 installed/platform
bytes使 C5 看似 production-ready。
