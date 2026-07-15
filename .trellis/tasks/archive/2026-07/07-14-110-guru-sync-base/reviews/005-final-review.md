# 第 5 轮最终放行审查

## 审查身份与范围

- 角色：`最终放行审查代理`
- 技术代理：`/root/branch_review_110_final_gate`
- 审查 HEAD：`2def8b748dae986e6f9e4d2912c2f8e6d617917a`
- 基线：`origin/main`（`f9f094f0a995e230226c8a94ff34944ba9d87b53`）
- 完整差异：`origin/main...2def8b748dae986e6f9e4d2912c2f8e6d617917a`
- Issue 范围：关闭 `#110`，关联 `#98`，后续 `#111`
- 审查方式：从未参与 Round 1-4 的全新技术代理独立全量审查。
- 副作用：本轮严格只读，未修改文件，未 commit、push 或创建 PR，未调用 Guru Team recorder/validator。

## Findings

- `findings_count=1`
- P0：0
- P1：0
- P2：1
- P3：0

### F-007 [P2] malformed/non-canonical result evidence 在校验失败后残留

证据：

1. `cmd_check_base_sync()` 在建立 cleanup `try/finally` 前调用 `read_base_sync_evidence(...)`。
2. result evidence 包含 invalid UTF-8、malformed JSON、non-object JSON 或 non-canonical JSON 时，读取或解析直接抛错，清理逻辑不会执行。
3. 独立隔离复现 malformed `{not-json`：`check-base-sync exit=2`，错误为 `Base sync result evidence file must contain valid UTF-8 JSON.`，随后 `residue=present`。
4. Non-canonical JSON 同样 `exit=2` 且 `residue=present`。
5. `design.md:112` 要求 result evidence 在 validator 所有 terminal path 删除，blocked 路径也必须清理已创建 evidence；workflow 同样声明每个 typed exit 前消费并删除 result evidence。
6. 现有测试覆盖 canonical JSON 内字段篡改、digest 与 live-state failure cleanup，但未覆盖 invalid UTF-8、malformed JSON、non-object JSON 或 non-canonical JSON cleanup。

影响：

- 校验器拒绝异常证据后留下本应一次性消费的运行时 artifact。
- Blocked terminal path 不满足 zero-residue 合同，后续重试与审计状态失去确定性。
- Docs SSOT 声明的 cleanup 行为与实际 malformed path 不一致，属于当前 `#110` 范围缺陷。

修复要求：

1. 分离安全路径/regular-file 检查、原始字节获取，以及 UTF-8/JSON/canonical/schema 解析。
2. 一旦安全确认 exact path 指向 repo-external regular non-symlink file 并取得原始字节，后续 UTF-8、JSON、canonical、schema、digest 或 live-fact 校验无论成功失败，都必须通过 `finally` 删除同一未变化文件并确认零残留。
3. Symlink、component 或 path-boundary 检查失败时不得删除不可信对象。
4. 增加 invalid UTF-8、malformed JSON、non-object JSON、non-canonical JSON cleanup regression tests，并在 throwaway 断言 terminal zero-residue。
5. 修复后重跑完整 Phase 2、创建 finding-fix commit，再由本 finding owner 做 closure review，并另派全新最终放行代理。

## 已通过验证

- Runtime tests：290 项。
- Skill package tests：66 项。
- `guru-sync-base` package tests：5 项。
- Preset tests：36 项。
- 合计：397 项。
- `git diff --check origin/main...HEAD` 通过。
- Trellis CLI `0.6.5` marketplace、`--create-new`、`--force` 命令面已核对。
- Extension `0.6.5-guru.7`、active skills 与 companion commands 已核对。
- Canonical、dogfood、installed workflow byte-identical；shared、Codex、Cursor、Claude 六份 package SHA 一致。
- 未发现 `.new`、`.bak` 或非 metadata dirty path。
- Planning approval 的三份规划文件 SHA、fresh Phase 2 check、task commit plan 003、commit parent/tree/exact paths 与 `hook_mutation=false` 一致。
- 三个 work commit 的中文 subject/body 与范围、验证结果一致。

## Docs SSOT

- Mandatory `guru-sync-base`、typed exits 的 consumer、resolution lease 到 `prepare-task` guards 的传递和 terminal release 规则已建立。
- F-001 至 F-006 的当前 lifecycle 已闭环。
- F-007 证明 malformed result evidence terminal path 尚未满足设计与 workflow 的 cleanup 合同。
- 结论：本轮 Docs SSOT compliance 不通过，必须随修复同步长期合同、实现与测试。

## 开箱即用与 Upgrade/Update

- Fresh install、dogfood overlay drift、installed package 一致性与多数 upgrade/update 抗漂移检查通过。
- Malformed terminal zero-residue 门禁未通过，因此不能声明完整 Phase 0 链路已最终放行。
- Remote branch-pinned marketplace verification 仍属于 push 后 publish gate，当前保持 pending，不能表述为已验证。

## Issue、部署与安全

- `issue-scope-ledger.json` 方向正确：只允许 `#110` 作为 close issue，`#98` 保持 related，`#111` 保持 follow-up。
- 未发现 secret、token、private key、数据库 URL、签名 URL或真实本机绝对路径泄漏。
- 无 CI/CD、Docker/Compose、Kubernetes/Helm、数据库 migration、Makefile 或部署入口变更。
- 当前工作区仅存在预期 task-local review/commit metadata，未发现非 metadata drift。

## 观察项

1. 真实远端 branch-pinned marketplace verification 必须在最终 reviewed HEAD push 后执行。
2. `issue-scope-ledger.json.acceptance_evidence` 必须在 publish 前补齐最终验收绑定。

## 后续候选

1. `#111` 保持独立 follow-up，不承担 F-007。

## 结论

本轮 `findings_count=1`（P2=1），结论为 `block`。不得写 passing gate 或进入 `trellis-finish-work`；必须返回 Phase 2 修复 F-007，形成新的 finding-fix commit，完成问题闭环与全新最终放行审查。
