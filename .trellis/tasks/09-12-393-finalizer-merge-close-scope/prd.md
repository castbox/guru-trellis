# Issue #393: 修复 refs-only 关闭集合合同不一致

## Goal

修复 Guru Team active Publication -> Finalizer -> Merge 交付链，使“交付验收 Issue 集合”和“本次合并由 PR 关键词自动关闭的 Issue 集合”保持语义分离。对 refs-only PR，Finalizer 必须向 Merge 传递空的 `expected_close_issues`，同时保留 Issue 归属、验收和 follow-up 语义。

## Confirmed Facts

- Live Issue: `https://github.com/castbox/guru-trellis/issues/393`。
- 当前基线为 `main` / `fa23476316fdaa35ba9345f3a2a8d25e0f7e49af`。
- 复现中 ledger 的 `close_issues=[127,129,130]`，但 PR 正文只有 `Refs #127/#129/#130`；Publication 已允许该正文，Finalizer 却把 ledger 集合直接投影为 Merge 关闭集合。
- Merge 已支持 `expected_close_issues=[]`，并在空集合时不读取或修改 Issue；其精确集合校验必须保留。
- #293 是未来 staged owner 重构，不作为本任务实现路径；不修改业务仓库 #127/#52。

## Requirements

1. 在 Publication、Finalizer 和 Merge 的 active contract 中明确区分交付验收/关联范围与 merge auto-close 范围。
2. 根据当前 PR 正文和明确关闭意图计算 merge 关闭集合；refs-only 正文必须产生空集合，不得自动补入 `Closes`。
3. 修复 Finalizer 正常 `ready_for_merge` 投影、existing PR recovery、terminal recovery 以及相关 consumer/schema/eval/test 证据。
4. 保留 Merge 的 expected-head、base/head、policy、CI、review、mergeability、精确集合比较和 post-merge 校验。
5. 合法非空自动关闭集合继续精确承接；正文漂移、非法关键词和非默认分支 closure mismatch 继续 fail closed。
6. 成功恢复不得重复 push、创建 PR、merge、归档或 Issue 关闭副作用。

## Out Of Scope

- 不修改业务仓库、业务 Issue 或业务 PR。
- 不实现 #293 的 staged owner 重构，不增加 alias、ledger 绕行、宽松校验、第二执行路径或新授权持久化。
- 不执行完整多平台 throwaway/release 矩阵；该范围由专门兼容性/Release Issue 负责。
- 不修改 GitHub merge 权限、Issue closure policy 或上游 Trellis 源码。

## Acceptance Criteria

- [ ] 非空交付验收集合 + refs-only PR 可从 Publication 经 Finalizer 到 Merge，公开 `expected_close_issues=[]`，Merge 不执行 Issue closure 读写。
- [ ] 合法包含 `Closes #N` 的 PR 仍只传递正文解析出的精确集合，并通过现有 Merge exact-set 校验。
- [ ] existing PR recovery、terminal output recovery、正文关闭范围漂移和非法关闭关键词均有覆盖；恢复不重复不可逆副作用。
- [ ] Finalizer 的 ready 输出 schema/example、Publication/Finalizer/ Merge tests 与当前 installed/canonical 投影保持一致。
- [ ] 运行 targeted package tests、全量 Python compile、JSON/schema、dogfood overlay drift 和 `git diff --check`；未覆盖的完整发布矩阵明确标记为 deferred。

## Docs SSOT Plan

- Requirements: 本任务不修改 `docs/requirements/evolution/requirement-main.md` 的产品目标；仅在 task-local 规划中引用现有 closure authority。
- Design: 本任务 `design.md` 记录跨包 ownership、数据流和兼容边界。
- Test: 本任务 `implement.md` 记录测试矩阵与未覆盖边界；实现只同步 package-local contract/eval/test 文档，不复制 workflow 全局规则。
