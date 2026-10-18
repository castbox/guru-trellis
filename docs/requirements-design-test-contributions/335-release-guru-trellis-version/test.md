# #335 Repository-private release orchestration Test contribution

- `T335-01`（R335-01）：校验 Shared/Codex/Claude/Cursor 四个 project-local Skill definition 的
  identity 与受管内容一致；扫描 public Skill package、marketplace、preset、overlay、registry、
  extension manifest 和 installed fixture，断言不存在 `release-guru-trellis-version`。
- `T335-02`（R335-02/04/09）：contract guard 校验六项最小输入、fresh authority reread、exact
  candidate freeze，以及 missing、multiple、live mismatch、cross-SHA、lineage gap、unknown/
  unmapped exit 的 fail-closed 文字合同；真实执行仍由被编排 owner 的现有 validator 负责。
- `T335-03`（R335-03）：静态 owner-composition 测试确认 preparation 显式引用 standard intake、Phase 2、
  Task Commit、Branch Review、Publication、Finalizer 与 Merge owners，且不复制其 internal procedure、
  public schema、typed exit 或 transaction implementation。
- `T335-04`（R335-03/06/07）：honest-path 临时 Git fixture 执行稳定 planning -> 最终交付内容 ->
  Task Commit -> 一次完整 Branch Review，并把 checker-passed 结果依次交给 Publication 与 Finalizer
  production wrappers；断言没有 task-local release notes/status/body、release-status metadata commit
  或第二次完整 Branch Review。Finalizer package 另以普通 base 前进 fixture 执行 preview -> recorder ->
  checker -> public wrapper，断言 exact `base_reconciliation_required` 输出可达且无 closeout mutation。
- `T335-05`（R335-07/08）：在同一 reviewed delivery identity 上创建、替换和退休 owner-private
  lifecycle metadata，identity 保持不变；分别改变 Skill、durable docs、配置、schema、script 和 test
  bytes，identity 必须变化且相关 gate 返回 stale/re-review route。
- `T335-06`（R335-05/06）：静态检查 PR/Release payload 的 live-authoring owner 合同；task tree 不存在
  `release-notes*.md`、body handoff、release-status、review-status 或 candidate-status 文件，
  `implement.md` 不含 Markdown checkbox 或执行状态字段。
- `T335-07`（R335-09）：contract guard 覆盖 FAIL、SKIP、stale、candidate/preparation cross-SHA 与
  unsupported exit 的 stop-before-mutation 规则，并禁止用 tracked metadata 建立恢复点。
- `T335-08`（R335-10）：表驱动静态校验 merge、annotated tag、tag-pinned smoke、GitHub Release、
  Issue closure 和 cleanup 的独立 confirmation rows，以及一次确认不可复用、不可持久化的合同。
- `T335-09`（R335-11）：contract guard 校验 post-merge minimum gate 明确保留 predecessor full diff、
  版本映射、source/installed validators、四平台 parity、install/update/reapply、secret scan、
  residue check 与 tag-pinned smoke；exact candidate 绑定和缺失/SKIP stop 由执行时 owner fresh 验证。
- `T335-10`（R335-01/11/12）：current-checkout 检查覆盖 project-local projection drift、recursive
  sidecar、public inventory isolation 和 forbidden release artifact；测试不读取 #332 工作资源，不创建
  真实 PR、tag、GitHub Release，也不执行完整累计多平台矩阵。

以上均为 #335 的定向 contract 与 honest-path 回归设计；实际 Gate 结果、candidate SHA、tag/smoke/
Release 状态和时间不写入本 durable contribution。
