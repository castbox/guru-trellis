# #117 BR-117-F9 Implementation Complete

## Files Modified

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - 新增 requested ref direct/peeled 解析；
  - executor 冻结 resolved commit，checkout 后验证
    `git rev-parse --verify HEAD^{commit}`；
  - checker 使用相同解析规则复核 remote freshness。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - 新增 branch、lightweight tag、annotated tag、checkout mismatch、
    workflow reviewed commit binding、checker/public projection 测试；
  - 更新 marketplace compatibility fixture 以承接 checkout commit evidence。
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/interface.json`
  - 明确 remote identity 与 executor 绑定 resolved checkout commit。
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/references/contract.md`
  - 明确 annotated tag peel、checkout commit 验证、fail-closed mismatch 及
    `remote_head`/`resolved_head` 字段语义。
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - 由 canonical workflow runtime 同步的 dogfood 运行副本。
- `.trellis/guru-team/skills/packages/guru-verify-extension-installation/`
  - 同步 canonical package 的 `interface.json` 与 `references/contract.md`。
- `.agents/skills/`、`.codex/skills/`、`.claude/skills/`、
  `.cursor/skills/` 下的 `guru-verify-extension-installation`
  - 同步相同的 package contract。
- `.trellis/guru-team/extension.json`
  - 更新 package/provenance digest，并稳定为全平台 `status=ok`。
- `.trellis/tasks/07-25-117-verify-extension-installation/implementation-handoff.md`
  - 本轮 F9 实现、Docs SSOT、验证与 check 交接。

未修改既有 `agent-assignment.json`、`review-gate.json`、`review.md`、
`task-commit-plans/004.json` 或 `reviews/005-f8-closure.md` /
`reviews/006-final.md`；这些并行生命周期产物保持原样。

## Implementation Summary

1. `git ls-remote` 现在一次请求 exact `<ref>` 与 `<ref>^{}`。共享 parser
   只接受无重复、合法 lowercase 40-hex 的 exact rows：
   - branch：direct commit；
   - lightweight tag：direct commit；
   - annotated tag：peeled commit，direct tag-object 不作为 resolved HEAD。
2. Executor 在 clone 前冻结 resolved commit，并用它执行
   `git checkout --detach <resolved-commit>`。
3. Checkout 成功后必须运行并记录 sanitized
   `git rev-parse --verify HEAD^{commit}` evidence。只有实际 checkout commit
   与冻结 resolved commit 完全一致，才允许运行 throwaway installer；不一致时
   `status=failed` 并 fail closed。
4. Workflow 的 `reviewed_head` 与 compatibility API 的 `expected_head` 都和
   resolved commit 比较，不再和 annotated tag direct object 比较。
5. Checker freshness 复用相同 direct/peeled parser；private `remote_head`
   与 standalone public `resolved_head` 均继续使用既有字段，但统一表示
   verified checkout commit。没有向 public DTO 增加 tag-object identity。
6. Branch、lightweight tag 和既有 marketplace source/ref 行为保持兼容；
   schema version、public output shape、typed exits、consumer mapping均未改变。

## Requirement And Design Carryover

- 完成 `BR-117-F9`：区分 requested ref direct object 与 resolved checkout
  commit，冻结后验证实际 checkout，并在 mismatch 时阻止 throwaway/success。
- 保留已审核的 public/private 边界：tag-object identity 不进入 public DTO；
  `remote_head`/`resolved_head` 是 resolved commit。
- 保留 workflow reviewed-commit binding、standalone session-only、blocked
  unresolved ref、semantic Gate 与 recorder/validator 分层。
- 未扩展恶意篡改、并发竞态、TOCTOU、锁、原子写入或其它已排除非功能场景。
- 未修改 workflow route、schema、preset installer 行为、overlay surface、
  ownership inventory、README command 或 release/deployment contract。

## Docs SSOT Handoff

- Strategy: `ssot_first`
- Durable docs updated or checked:
  - 已更新 canonical Skill `interface.json` 与 `references/contract.md`，使
    ref peel、checkout verification 和字段语义成为 package durable contract；
  - 实现前已核对 `.trellis/spec/workflow/workflow-contract.md`、
    `companion-scripts.md`、`skill-package-contract.md`、
    `quality-guidelines.md`、`.trellis/spec/preset/installer.md`、
    `upstream-ownership.md`、`overlay-guidelines.md` 与
    `.trellis/spec/docs/public-docs.md`；
  - 上述 spec 已要求 cloned checkout commit verification、canonical-first
    distribution、known-managed backup recovery 和 zero-sidecar 终态，因此没有
    为 F9 重复新增更高层规则。
- Task artifact delta merged back to durable docs:
  - annotated tag direct object 与 peeled commit 的区分；
  - checkout 后 `HEAD^{commit}` exact comparison；
  - private `remote_head` / public `resolved_head` 均表示 resolved commit；
  - direct tag-object 不进入 public DTO。
- Task-history-only content:
  - F9 review finding provenance、复现用 direct/peeled OID、实现过程状态、
    初次 installer recovery 过程和本 handoff 的命令证据。
- No-update reason or follow-up / current PR limitation:
  - `.trellis/spec/`、workflow、schema、overlay、README 和
    `data-contracts.md` 无更新；现有 durable owners 已覆盖行为边界，F9
    未新增 API 字段、route、安装命令或平台能力；
  - exact pushed feature-ref clean install 仍受当前 PR 尚未 push 的限制。
- Implementation inputs from durable docs:
  - companion script executor/validator 边界；
  - Skill minimal public I/O/private state；
  - canonical/runtime/package/platform 镜像和 installer recovery 合同；
  - normal-path correctness scope 与 required validation。
- Implementation inputs from confirmed task delta:
  - `BR-117-F9` 对 annotated tag object/commit 分离、post-checkout evidence、
    mismatch fail-closed、branch/lightweight compatibility 与 workflow reviewed
    commit binding 的精确要求。

## Verification Results

- Focused runtime:
  - `ExtensionVerificationRuntimeTest`: 23 passed；
  - `MarketplaceVerificationContractTest`: 7 passed。
- Package contract:
  - `guru-verify-extension-installation/tests/test_contract.py`: 8 passed。
- Full runtime:
  - `test_guru_team_trellis.py`: Ran 596，OK，13 skipped。
- Real Git ref probe:
  - branch 与 lightweight tag 只返回 direct commit；
  - annotated tag 返回 direct tag-object 与 `<ref>^{}` peeled commit；
  - peeled OID 与实际 checkout commit一致。
- Preset distribution:
  - 初次默认 apply 按合同生成 9 个 known-managed `.bak` 并因平台选择缩小
    暂时移除 Claude；
  - 9 个 backup 均逐一验证为 HEAD 旧托管版本后删除；
  - `apply.sh --repo . --all-platforms` 重放并再次验证幂等；
  - 最终 shared/Codex/Claude/Cursor 全同步，2322 managed files 全
    `unchanged`，0 conflict、0 sidecar、0 removal。
- Static/install checks:
  - `check-dogfood-overlay-drift.sh`: passed；
  - `check-upstream-ownership.sh --json`: `status=ok`；
  - `check-skill-packages.sh --mode source`: passed；
  - `check-skill-packages.sh --mode installed`: passed；
  - canonical/installed runtime `cmp`: passed；
  - canonical/installed runtime `py_compile`: passed；
  - package wrapper `bash -n`: passed；
  - recursive `.new`/`.bak` scan: zero；
  - `.trellis/guru-team/extension.json`: package `status=ok`，全平台，
    zero conflict/sidecar；
  - `git diff --check`: passed。
- Lint: pass，`git diff --check`、Python compile 与 shell syntax均通过。
- TypeCheck: skipped；仓库对该单文件 runtime 没有独立静态 typecheck 命令，
  由 full unittest、schema/package validators 与 Python compile 承接。

## Handoff For Check

- Focus areas:
  - 用真实/fixture annotated tag 复核 direct object 与 peeled commit 不同，
    executor checkout 与 public projection只使用 peeled commit；
  - 确认 `HEAD^{commit}` command evidence 在 throwaway 之前，mismatch 时
    throwaway 未执行且结果 fail closed；
  - 复核 workflow `reviewed_head`、compatibility `expected_head`、
    private `remote_head`、public `resolved_head` 的 commit identity 一致；
  - 复核 branch/lightweight behavior、blocked unresolved ref、checker
    freshness 与 semantic route 无回归；
  - 检查 canonical/runtime/shared/Codex/Claude/Cursor bytes 和 extension
    manifest digest；
  - 执行完整 Docs SSOT reconciliation，确认无遗漏 schema/README/spec owner。
- Validation intentionally deferred to `trellis-check`:
  - Phase 2 semantic review 与 `phase2-check.json` recorder/validator；
  - full throwaway install/update/reapply matrix；
  - production native eval；
  - exact pushed feature-ref real remote clean installation；
  - Branch Review Gate、commit、push、PR readiness 与 issue closure。
- Remaining risks:
  - 当前验证使用 local working-tree candidate；尚未绑定新的 task work commit；
  - exact pushed ref 与真实外部网络/CLI 安装 surface 尚未验证；
  - 首次 default apply 的 recoverable backup/platform-shrink 路径已恢复并通过
    all-platform idempotence，但 check 应把最终 clean manifest 作为验收输入，
    不引用中间 conflict 状态。
