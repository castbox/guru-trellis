# #147 Branch Review 问题发现报告

## 审查身份与 reviewed_head

- 审查角色：独立问题发现审查代理 `/root/issue147_branch_discovery`
- 审查方式：只读审查 `origin/main...HEAD` 完整提交差异；未参与实现、finding 修复、commit 或 gate recorder
- Base：`origin/main` / `ac14a0d605335e57c47c26c1f21e28c9ea41371c`
- reviewed_head：`1cbf3dd85f8845441df2bb3172e82054568c30b5`
- Diff：105 files changed，17366 insertions，52 deletions

## 审查范围

已独立核对：

- GitHub Issue #147 正文及其 #144 前置、#145/#146 后续边界；
- `prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、research evidence；
- `phase2-check.json` 的 implementation handoff、R1-R12、AC1-AC15、第五轮检查证据与唯一未验证项；
- canonical runner、四 adapter、closed schemas、representative semantic/deterministic fixtures 与测试；
- extension/preset/installed dogfood mirrors、installer、throwaway update/reapply 逻辑；
- durable requirements、workflow/preset/public docs SSOT；
- `origin/main...HEAD` 完整 diff、sidecar、部署与敏感信息影响。

审查只覆盖 honest-but-fallible 正常执行、普通错误、stale/mismatch、平台兼容和行为回归。恶意篡改、对抗输入、非常规并发、TOCTOU、锁和 crash consistency 均未作为 finding 来源。

## 需求、设计、实现、测试与 Docs SSOT 一致性

Corpus closed schema、actual typed exit、per-exit schema、deterministic/external-semantic/human 三边界、四状态聚合、四 adapter、public-only projection、trace receipt、repo 外 evidence、source/installed/preset/platform 分发和 normal invocation zero-impact 的主体实现，与 Issue、R1-R12、AC1-AC15 和 durable docs 基本一致。

当前测试充分覆盖同构 current/comparison package、四平台 fake native execution、receipt 缺失、unsupported、malformed output、semantic grading、run-root boundary 及 byte identity。但 comparison 测试仅复制当前 package，未覆盖两个 exact 版本拥有不同 Interface public invocation 的合法情形，也未覆盖 comparison package 的普通结构漂移。因此未发现下述 P1 回归。

## 问题

### P1：comparison side 复用当前包 invocation，无法比较合法的不同版本并可能脱离闭集状态

- Priority：P1
- 路径/行：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19221`、`:19292`、`:19307`；`trellis/skills/guru-team/adapters/eval/native_adapter.py:217`
- Current scope：R9/AC9 明确要求 current/comparison exact package pair；R5/R6 要求每侧实际执行其 Interface public invocation，并把普通执行失败收敛到 closed error/status。
- 正常路径复现：caller 解析两个相同 Skill id、Interface 1.3、byte-identical corpus 的 exact package 版本，其中 comparison 版本把公开 wrapper 从 `scripts/invoke.sh` 合法迁移到另一个 Interface 声明路径。`skill_eval_validate_comparison_pair()` 只校验 corpus hash、id 和 schema version，随后 adapter request 的 `interface` 仍写入当前 registry 的 `discovery`。`stage_public_projection()` 虽按 comparison package 自身 Interface 复制资产，却在第 217 行使用当前包 discovery 的 wrapper path，导致 comparison side 返回 `execution_error`，而不是执行该版本声明的 exact public invocation。若 comparison package 是普通安装/打包漂移（例如缺少 `public_contracts.outputs` 或 corpus 声明的 fixture），runner 还会在第 19294/19305 行直接 `KeyError`/`OSError`，不会生成 `execution_error` evidence。
- 影响：comparison 目前只对 public invocation 完全同构的 package copy 可用，不能可靠承担“既有 Skill current/comparison exact version”合同；同时普通 package drift 未稳定 fail closed 到结构化结果。
- 修复要求：在任何 side 执行前，针对该 exact package 独立验证完整 Interface/corpus/fixture/public assets，生成 side-local invocation/output-schema DTO，并将该 DTO传给 adapter；合法版本差异必须调用各自 Interface 声明的 wrapper，普通结构错误必须返回稳定错误或 `execution_error`。补充 wrapper path 不同的正例，以及缺少 outputs/fixture 的负例。

Findings 统计：P0=0，P1=1，P2=0，P3=0。

## 观察项

- `implement.md` 仍保持计划态未勾选清单，而 `phase2-check.json` 已记录全部完成。当前 completion evidence 的 SSOT 是 Phase 2 artifact，因此不单独列 finding，但最终人类可读文档容易产生状态误读。
- exact remote branch marketplace 尚未验证，原因是分支未 push；Phase 2 已明确标为非阻塞、由 publish gate 在 push 后验证，当前不作为 Branch Review finding。
- source checkout 未观察到写入；target worktree 除并行 gate metadata 外未发现额外实现漂移。

## 后续候选

- 无 out-of-scope 必需 follow-up。上述 comparison 缺口属于 #147 current scope，应在本分支修复并重新执行完整 Phase 2 与 Branch Review。
- #145/#146 继续保留 production Skill corpus migration 与 coverage closure，不应被本 finding 扩张进 #147。

## 部署与安全影响

- 变更影响 Guru Team extension、preset、Python/shell companion runtime、schemas、selected-platform package copies 与 docs；不涉及 CI/CD、container、K8s/Kustomize、数据库 migration、Makefile、生产配置或生产数据。
- 未发现 token、secret、private key、`.env`、signed URL、客户数据或敏感 provider 原始记录进入 diff。
- public-only projection、Unix socket broker 和 repo 外 evidence 保持预期边界；本 finding 是正常 comparison correctness，不涉及恶意 actor 或防篡改模型。

## 验证证据

- `git rev-parse HEAD`：`1cbf3dd85f8845441df2bb3172e82054568c30b5`
- `git diff --check origin/main...HEAD`：通过
- 递归 `.new` / `.bak` 扫描：0
- `python3 -m unittest trellis.skills.guru-team.tests.test_skill_packages.EvalRunnerTests`：9 passed
- `check-skill-packages.sh --json --mode source`：passed
- installed `check-skill-packages.sh --json --mode installed`：passed，400 managed files，0 sidecar/removal/conflict
- canonical 与 installed adapter/schema 逐文件 byte comparison：无 drift
- Phase 2 既有完整证据：workflow 548 passed/13 skipped、Skill packages 137 passed、preset 39 passed、ownership 6 passed、throwaway sample exit 0；本审查将其作为已有 gate evidence复核，不冒充本代理重跑。

## 结论

`origin/main...1cbf3dd85f8845441df2bb3172e82054568c30b5` 存在 1 个 current-scope P1 finding。Branch Review 不应通过；需先修复 comparison side-local Interface/public invocation 绑定与结构错误分类，重跑完整 Phase 2，再对新 HEAD 进行独立 Branch Review。
