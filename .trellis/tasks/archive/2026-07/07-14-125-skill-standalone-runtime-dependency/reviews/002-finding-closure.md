# Issue #125 Round 002 F-001 问题闭环审查原始报告

## 一、身份与审查边界

- 逻辑角色：`问题闭环审查代理`
- 技术身份：`/root/trellis_final_review_125`
- 复用决策：`reuse-for-closure`
- 闭环来源：Round 001 / P2 / F-001
- reviewed HEAD：`93d9a416bd6b34a87844dde5d4d9da363af729c2`
- finding 原始 HEAD：`e4937dfe19c9e3d889144ca5ef9d7afd42a429b5`
- intake base：`origin/feat/122-guru-create-task-commit@49bf572e6a89bff9c63416bea64254cda0c20bf0`
- revision diff：`e4937dfe19c9e3d889144ca5ef9d7afd42a429b5..93d9a416bd6b34a87844dde5d4d9da363af729c2`
- 审查范围：只判断 F-001 root cause 是否关闭，并检查修复是否引入新 P0/P1/P2/P3 finding
- 禁止动作遵守：未修改 code、spec、planning、`review.md`、`review-gate.json`、ledger、assignment 或 commit plan；未运行 `review-branch.sh`、`check-review-gate.sh` 或任何 `record-*`

本代理已在 Round 001 成为 finding owner。本轮只能承担问题闭环，不能再次承担最终放行；即使本报告通过，仍必须由从未参与前序 review round 的全新 `最终放行审查代理` 审查完整 stacked-base diff。

## 二、读取与核对证据

已读取并交叉核对：

- `.agents/skills/trellis-check/SKILL.md`
- Round 001 `reviews/001-final-review.md`
- `review.md` 与 failed `review-gate.json`
- `finding-fix-handoff-001.md`
- fresh `phase2-check-report-f001.md` 与 `phase2-check.json`
- `task-commit-plans/002.json` 的 snapshot、classification、exact stage、AI review、message、freshness 与 committed result/tree evidence
- revision commit `93d9a416...` 的完整 message、path set 与 diff
- canonical/dogfood `guru_team_trellis.py`
- `trellis/skills/guru-team/tests/test_skill_packages.py`
- production interface、interface schema 1.1、fixture extension、canonical/installed extension inventory
- 与 F-001 边界相关的 installer、docs、spec、安全和部署资产变化事实

Revision commit 只包含四个路径：canonical runtime、dogfood runtime、source regression test 与 candidate 002。Commit parent 精确等于 Round 001 HEAD；4 个 revision diff path 与 4 个 `exact_stage_paths` 完全相等，tree evidence 匹配，`unrelated_preserved=true`，`hook_mutation=false`。

## 三、F-001 根因闭环判断

### 3.1 原问题

Round 001 证明 `runtime_command=run-skill-command` 同时满足 interface schema pattern 且属于 extension published `companion_scripts`，原 source validator 因此返回 passed；runtime resolver 却明确拒绝 dispatcher self-mapping，导致确定不可调用的 package 可以通过 source/installed validation 和分发。

### 3.2 修复实现

- 新增单一机械判定 `skill_runtime_command_maps_to_dispatcher(runtime_command, dependency)`。
- `validate_skill_interface()` 使用该 helper，在 source validation 阶段拒绝 validator target 等于当前 interface `runtime_dependency.dispatcher`。
- `resolve_skill_runtime_command()` 复用同一 helper，替代原先独立的常量比较。
- Helper 只比较已解析 string 与 dependency dict 中的 dispatcher id，不引入路径、fallback、I/O 或副作用。
- Canonical 与 dogfood runtime bytes 完全一致，Git mode 均为 `100755`。

结论：source 与 runtime 不再各自维护不同的 self-mapping 判断，F-001 的语义漂移根因已关闭。

### 3.3 精确负例证据

独立临时 fixture probe：

- self-mapping 值：`run-skill-command`
- interface JSON Schema errors：`[]`
- dispatcher published membership：`true`
- source validation status：`failed`
- 完整 errors 数组仅包含：
  `interface for guru-example-action validator result_validator runtime_command must not equal runtime_dependency.dispatcher`

永久 regression `test_validator_runtime_command_cannot_self_map_to_dispatcher` 精确断言同一个单元素 errors 数组，不是泛化的“有任意错误即通过”。

### 3.4 Production 正向路径

Production interface mappings 未变化：

- `candidate_validator -> check-commit-messages`
- `exact_executor -> create-task-commit`
- dispatcher：`run-skill-command`

Canonical source validation 与 installed validation 均 passed；installed facts 为 43 managed files、Claude/Codex/Cursor 三平台、0 sidecar、0 removal、0 conflict。`.agents/.../check-task-commit-plan.sh --help` 经 shared dispatcher 正常进入 companion command。

## 四、验证结果

| 验证 | 结果 |
| --- | --- |
| F-001 targeted regression | 1 passed |
| Canonical package contract | 5 passed |
| Skill package/source/distribution/runtime dispatcher | 65 passed |
| Preset installer | 36 passed |
| Shared runtime | 275 passed |
| 完整 suite 合计 | 381 passed |
| `check-skill-packages --mode source` | passed；1 active、1 reserved、1 invoke、3 exits |
| `check-skill-packages --mode installed` | passed；43 files、三平台、0 sidecar/removal/conflict |
| dogfood overlay drift | passed |
| canonical/dogfood runtime bytes 与 mode | 一致，`100755` |
| JSON parse、Python `py_compile`、`git diff --check` | passed |
| recursive `.new` / `.bak` scan | 0 |
| candidate 002 commit/tree/path audit | commit、parent、4 paths、tree、preservation 全部匹配 |

## 五、边界复核

### 5.1 Schema 与公共合同

Interface schema 1.1 未变化；`runtime_command=run-skill-command` 继续合法通过 schema，cross-field self-mapping 由 source semantic validator 负责，符合 JSON Schema 与 semantic validation 的分工。Extension manifest、runtime API、dispatcher id、production interface 与 typed exits 未变化。

### 5.2 Docs SSOT 与 upgrade/update

修复只承接既有“command mapping mismatch 在分发/调用前 fail closed”合同，没有改变 mode、runtime dependency、installer、remediation、upgrade 或 public wording，因此无需修改四份 spec、durable requirements 或三份 public README。Installer 与 throwaway verifier 相对 Round 001 HEAD 未变化；前序 clean throwaway/update-reapply evidence 仍适用，fresh installer/runtime/source tests、installed validation 与 dogfood drift 未发现回归。

Exact feature-ref remote marketplace verification 仍必须在 reviewed content push 后由 `trellis-finish-work` 完成；本轮未把 public canary 当成 exact remote pass。

### 5.3 安全与部署

修复没有接受任意 runtime path、没有改变 `os.execv` target 形成方式、没有新增 fallback；无 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或本机绝对路径进入修订 diff。服务、API、worker、schedule、queue、DB migration、CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm 与 Makefile 均未变化，部署形态不变。

## 六、问题清单

- P0：无
- P1：无
- P2：无
- P3：无

F-001 状态：`closed`。

本轮未发现新 finding，因此本代理不产生新的 finding owner 身份；既有身份仍严格限于 F-001 closure，不得转为最终放行。

## 七、观察项与后续门禁

1. Current worktree 仍保留 assignment、Phase 2、两份 commit plan result、Round 001 gate/report 与 fix/check handoff 等 task-local metadata tail；main session 应按 workflow 继续记录 closure 和 fresh final review，不得把它们误判为功能 drift。
2. #125 仍 stacked 于 PR #124；如 PR #124 合并并 retarget 到 `main`，必须按新 base 重跑 freshness-sensitive Phase 2、Branch Review 与 remote marketplace verification。
3. Issue #125 `acceptance_evidence[]` 必须在 publish 前依据真实验证补齐；#122 保持 related-only。
4. 本报告不是最终放行报告，不能单独使 Branch Review Gate passed。

## 八、结论

- `findings_count: 0`
- reviewed_head：`93d9a416bd6b34a87844dde5d4d9da363af729c2`
- F-001：`closed`
- 问题闭环结论：`passed`
- 最终放行结论：`not-applicable`
- 下一路由：main session 记录 Round 002 closure 后，派发一个从未参与 Round 001/002 的全新 `最终放行审查代理`，审查当前 HEAD 的完整 `origin/feat/122-guru-create-task-commit...HEAD` diff。
