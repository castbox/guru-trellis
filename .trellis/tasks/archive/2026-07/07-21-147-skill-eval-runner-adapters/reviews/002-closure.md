# #147 Branch Review Round 2 问题闭环审查报告

## 审查身份与结论字段

- 审查角色：原 Round 1 finding owner `/root/issue147_branch_discovery`，本轮作为问题闭环审查代理复用
- reuse_decision：`reuse-for-closure`
- Base：`origin/main` / `ac14a0d605335e57c47c26c1f21e28c9ea41371c`
- 原 reviewed_head：`1cbf3dd85f8845441df2bb3172e82054568c30b5`
- 本轮 reviewed_head：`889387cdfcdf0b0ca8f3e32028c91d19548c3349`
- Finding-fix diff：`1cbf3dd85f8845441df2bb3172e82054568c30b5...889387cdfcdf0b0ca8f3e32028c91d19548c3349`
- findings_count：0

## 审查范围

本轮独立只读复核：

- Round 1 `001-discovery.md` 的 P1 finding、正常路径复现、影响和修复要求；
- finding-fix commit `889387c` 的完整 11-file diff；
- canonical/installed/fixture runtime 与 adapter mirrors；
- side-local Interface/public-contract/corpus/fixture validation、invocation DTO、per-exit output schema 与 adapter binding；
- 新增 different-wrapper 正例、missing outputs 与 missing fixture 负例及完整 EvalRunnerTests；
- fresh `phase2-check.json` 的 implementation handoff、semantic review、完整 rerun、Docs SSOT reconciliation 与唯一未验证项；
- `.trellis/spec/workflow/skill-package-contract.md`、`quality-guidelines.md` 的 durable contract 增量；
- `origin/main...HEAD` 完整 diff 的 whitespace、sidecar、部署与安全影响。

仍只评估 honest-but-fallible 正常执行、普通安装/打包 drift、平台兼容和行为回归。恶意篡改、对抗输入、非常规并发、TOCTOU、锁与 crash consistency 不进入本轮 finding。

## 原问题生命周期

### Round 1 finding

P1：comparison side 只校验 corpus hash 与 Interface id/version，却把 current package discovery 的 `public_invocation` 传给全部 side。合法的 exact comparison 版本若声明不同 wrapper path，会错误执行 current wrapper 或返回 `execution_error`；缺少 outputs/fixture 的普通 package drift 还可能直接抛出 `KeyError`/`OSError`，脱离 closed eval error/status。

### 修复承接

- `skill_eval_comparison_sides()` 只解析 caller-resolved absolute exact paths，不再把轻量 identity 检查冒充完整 side validation。
- `skill_eval_side_validation_context()` 从当前 source/installed extension context 读取 Interface 1.3 schema、published runtime commands 和 active registry references。
- `skill_eval_discover_side()` 在任何执行或 run-root write 前，逐 side 校验 closed Interface、完整 public contracts/assets、byte-identical corpus、fixtures、expected profiles/exits，并生成 side-local `public_invocation` 与 `output_schemas` DTO。
- Runner 在 adapter request 中使用 `side_interface`，不再复用 canonical discovery invocation。
- Adapter 从 exact package Interface 读取 local invocation，并要求 request DTO 与其完全相等，再执行该 side 自己声明的 wrapper。
- 普通 unreadable JSON/wrapper/fixture 进入稳定 error collection；缺失 outputs/fixture 在 run root 创建前返回 closed eval error，不再出现 traceback。

### 闭环判断

原 P1 已完整关闭。合法 current/comparison versions 可以声明不同 wrapper paths；每个 side 的 invocation 与 output contract 独立绑定。无效 side 在任何一侧执行前 fail closed，因此不存在半执行 comparison 或未结构化 `KeyError`/`OSError`。

## 验证证据

- `git rev-parse HEAD`：`889387cdfcdf0b0ca8f3e32028c91d19548c3349`
- finding-fix commit：`fix(trellis): #147 修正 Skill 对比侧调用绑定`
- `python3 -m unittest trellis.skills.guru-team.tests.test_skill_packages.EvalRunnerTests`：本代理独立运行，10 passed
- 新增测试确认 current 使用 `invoke.sh`、comparison 使用 `invoke-v2.sh`，整体 status 为 `passed`
- 新增负例确认 missing outputs 返回 `eval_side_interface_invalid`、missing fixture 返回 `eval_fixture_invalid`，均无 traceback 且 run root 未创建
- `git diff --check origin/main...HEAD`：通过
- 递归 `.new` / `.bak` 扫描：0
- canonical runtime 与 installed runtime byte-identical；canonical adapter、installed adapter、representative fixture adapter byte-identical
- fresh Phase 2 evidence：workflow 548 passed/13 skipped、Skill packages 138 passed、preset 39 passed、ownership 6 passed、400 managed files、0 sidecar/removal/conflict、full throwaway init/update/reapply 通过
- fresh Phase 2 `typed_exit=passed`、semantic findings=0；其 pre-commit snapshot 绑定旧 HEAD `1cbf3dd` 与完整 finding-fix dirty paths，随后由 exact commit plan 002 形成 reviewed commit `889387c`

## Docs SSOT

`ssot_first` reconciliation 已同步：

- `.trellis/spec/workflow/skill-package-contract.md` 明确每个 comparison side 在执行前独立验证 closed Interface 1.3、byte-identical corpus、fixtures、public invocation/output assets，并生成 side-local DTO；合法版本允许不同 wrapper path。
- `.trellis/spec/workflow/quality-guidelines.md` 新增 different-wrapper 正例，以及 missing outputs/fixtures/Interface/public assets 的 pre-execution closed failure 门禁。
- Docs 内容与 runtime、adapter 和新增测试一致，没有把 finding 生命周期复制为新的 durable SSOT。

## 部署与安全判断

- 修复仅影响 Guru Team eval runner、adapter、dogfood mirrors、tests、extension provenance 与 durable specs。
- 不涉及 CI/CD、container、K8s/Kustomize、DB migration、Makefile、生产配置、生产数据或权限变更。
- 未发现 token、secret、private key、`.env`、signed URL、客户数据或敏感 provider 输出进入 finding-fix diff。
- public-only projection、runner-owned runtime boundary、repo/package-external evidence 与 private runtime locator 隔离均保持不变；本修复没有扩大 native execution 可见面。

## 问题

P0=0，P1=0，P2=0，P3=0。

未发现原 finding 残留，也未发现 finding-fix 引入的新 current-scope correctness、compatibility、distribution、Docs SSOT、部署或安全 finding。

## 观察项

- exact remote branch marketplace 仍因分支未 push 而未验证；fresh Phase 2 已明确列为 non-blocking，必须由 publish gate 在 push 后验证。
- 当前 worktree 中 `agent-assignment.json`、commit-plan metadata、review artifacts 与 review gate tail 由主会话并行维护；本代理未审查或修改这些未提交 tail 的 recorder 状态，只审查它们引用的 finding lifecycle 与已提交 fix。
- `phase2-check.json` 按 commit workflow 记录 pre-commit HEAD 与 finding-fix dirty snapshot，而不是伪装为 post-commit Branch Review；commit plan 002 和 commit diff提供了到 `889387c` 的确定性承接。

## 后续候选

- 无新增 current-scope 或 out-of-scope 必需 follow-up。
- #145/#146 继续拥有 production Skill corpus migration 与 coverage closure；本轮 closure 不改变其边界。

## 结论

Round 1 P1 已在 `889387cdfcdf0b0ca8f3e32028c91d19548c3349` 完整关闭，finding-fix diff 未引入新的 current-scope finding。`findings_count=0`，`reuse_decision=reuse-for-closure`，可由主会话继续汇总最终 Branch Review Gate；exact remote branch marketplace 仍保留到 publish gate。
