# #195 迁移全部 Guru Team Skills 到 package-local runtime

## 目标与用户价值

在一次完整 Trellis 生命周期、一个 task/worktree/branch 和一个最终 PR 中，把 live registry 的 15 个 active Guru Team Skills 从共享 Python 单体迁移到各自 package 拥有的确定性 runtime，并删除共享单体、聚合测试、installed copies 和兼容路由。

迁移完成后，业务仓库中的 Agent 只读取 Skill 公共资产、command discovery 和精确 CLI help，即可生成语义输入、调用真实 wrapper 并验证 typed output；Agent 无需读取或理解 package private Python 实现。

## 当前证据与权威

- Live issue 权威为 `castbox/guru-trellis#195`，状态为 OPEN，2026-08-12 规划时重新读取。
- 当前 base 为 `main@7e0eb940051941b273ba10e5120a175482ada9f2`。
- `trellis/skills/guru-team/registry.json` 当前列出 15 个 active Skills：`guru-approve-task-plan`、`guru-check-task`、`guru-clarify-requirements`、`guru-create-task-commit`、`guru-create-task-workspace`、`guru-discover-change-context`、`guru-finalize-task`、`guru-merge-task-pr`、`guru-review-branch`、`guru-review-change-request`、`guru-review-contract-wording`、`guru-review-task-publication`、`guru-select-workflow-mode`、`guru-sync-base`、`guru-verify-extension-installation`。
- `guru-sync-base` 为 deterministic Skill；其余 14 个为 semantic Skill。`guru-verify-extension-installation` 为 `standalone_only`，业务仓库 workflow 不得路由到它。
- 共享实现 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 当前 38,333 行；聚合测试 `test_guru_team_trellis.py` 当前 24,023 行；合计 62,356 行。
- 15 个 package 当前各有一个 `tests/test_contract.py`；package eval tree 当前有 146 个文件。现有测试规模不证明 package-local runtime ownership 或 public-only execution。
- #81 的 `v0.6.5-guru.5` 是行为兼容、upgrade 对比和回滚基线。#205 已合并后的 verifier ownership、routing、public contract 和 installed behavior 是当前迁移基线。
- #156 独立拥有 Phase 0 producer-output 到 consumer-input 与 source-preserving freshness correctness。本 task 不修改、关闭或吸收 #156。

## Requirements

### R1 单一交付边界

- A-F 仅是同一 task 的内部 checkpoint，不创建额外 Issue、task、worktree、branch、PR、Publication 或 Finalizer。
- 最终 PR 只关闭 #195；#156、#205 保持 related，#196-#200 不进入 close scope。
- 任一保留共享单体的中间状态仅是未完成 checkpoint，不构成可发布交付。

### R2 唯一命令所有权

- 从 fresh registry 与全部 `interface.json.validators` 生成完整 Skill/command/runtime/test/install inventory。
- 每条 active command 必须映射到唯一 package owner，或映射到满足 R5 admission rule 的 shared primitive。
- inventory 必须覆盖 wrapper、entrypoint、参数、stdin/stdout、error code、side-effect 分类、tests 和 installed projection。

### R3 Package-local runtime

- Canonical package 位于 `trellis/skills/guru-team/packages/<skill-id>/`。
- 每个 package 仅创建其职责真实需要的 `runtime/record.py`、`runtime/check.py`、`runtime/execute.py`；没有该职责时不得创建占位模块。
- `scripts/` 只保留薄启动器：解析 package root、启动声明 entrypoint、传递 argv/stdin/stdout/stderr/exit status，不包含 Skill-specific 业务规则。
- semantic scope、finding、充分性、确认、revision action 和 route 判断继续由对应 Markdown Skill 的 AI owner 执行；runtime 只能执行 executor、validator、recorder 职责。

### R4 Command 与 error 合同

- 每个 package 新增机器可读 `commands.json`，声明稳定 command id、唯一 owner、entrypoint、参数、stdin、stdout、错误、side-effect 类型和 schema binding。
- 每个 package 新增 `errors/catalog.json`，声明该 package 的稳定 error code、精确触发条件、exit status、字段或路径定位规则和 remediation。
- `commands.json`、error catalog、wrapper、runtime parser、public invocation error schema、help 和 tests 必须逐项一致。
- 未知 command、未知 error、重复 owner、缺失 entrypoint 或跨 package 私有调用必须 fail closed。

### R5 最小 shared kernel

- Shared kernel 的唯一 canonical root 为 `trellis/skills/guru-team/runtime/`，installed root 为 `.trellis/guru-team/runtime/`。
- shared primitive 只承载 JSON、schema、path、command dispatch 或 Git primitive，并且必须存在两个或更多采用完全相同语义的真实 package consumers。
- 每个 shared primitive 必须在 inventory 中列出全部 consumers，并由 kernel test 与各 consumer contract test证明相同语义。
- Kernel 不得按 Skill id、profile、typed exit 或 workflow route 分支，不得包含 Skill-specific record/check/execute 业务逻辑，不得拥有 semantic judgment，也不得承载 Finalizer、Publication、Verification 或 PR merge 状态机。

### R6 Public projection 与 installed ownership

- Package runtime、internal tests 和 error implementation 只安装到 `.trellis/guru-team/skills/packages/<skill-id>/`；shared kernel 只安装到 `.trellis/guru-team/runtime/`。
- `.agents/`、`.codex/`、`.claude/`、`.cursor/` 只接收 Agent 所需 public projection，不复制 private runtime、internal tests 或 error implementation。
- Installer manifest、source validator、installed validator、upstream ownership 与 selected-platform inventory 必须精确反映该边界、文件 hash 和 executable mode。
- Canonical source、dogfood installed copy、preset overlay 和文档必须同步；official Trellis update 后 reapply 必须恢复相同投影且不静默覆盖用户修改。

### R7 精确 CLI 合同

- 每个公开 command 的 `--help` 必须 exit 0、无 repo/Git/GitHub 副作用，并完整列出 usage、required/optional arguments、stdin、stdout、errors 和 JSON mode。
- 每个公开 command 的 `--json` stdout 必须恰好包含一个符合声明 schema 的 JSON 对象；diagnostics 只写 stderr。
- 失败必须返回声明的非零 exit status 和闭合错误对象，包含稳定 `code`、适用的 `field` 或 `path`、以及 `remediation`，且不得输出 traceback。
- missing、unknown、repeated、conflicting arguments，错误 mode/profile，schema mismatch，stale identity 与 unsafe path 均必须 fail closed。

### R8 合同冻结与依赖边界

- 兼容基线由 `v0.6.5-guru.5`、#205 合并结果和实现开始时的 fresh registry/interfaces 共同组成。
- 除 #205 已批准的迁移外，不改变 stable Skill id、judgment mode、public input/output schema id、typed exit、consumer projection、workflow marker、workflow/standalone precondition 或 confirmation lifecycle。
- #205 已退休的 target-business-repo verifier profiles、DTO、exits、consumer projections、artifacts 和 recovery paths 不属于冻结兼容面；不得恢复它们。
- 若迁移必须引入 #205 之外的不兼容 public API 变化，该不兼容变更以 `blocked` 停止并提出独立 migration proposal。

### R9 Test 与 eval ownership

- 每个 Skill 的 CLI、errors、record/check/execute、profiles/exits/re-entry 测试归 package-local `tests/`。
- 跨 Skill graph、installer、workflow、upgrade 和 end-to-end 测试归明确 integration owner，只消费 public commands/DTO，不 import package private runtime。
- public-only eval 必须从 package-external public projection 启动，正向生成 semantic authoring/input，调用真实 wrapper，并验证真实 typed output。
- Eval 输入不得包含 expected exit、checker-passed owner result 或 private runtime 路径；trace 必须证明 public-only 闭环没有读取 private Python implementation。
- Extension Verification public-only eval 仅由 extension source repository 使用 clean throwaway target 执行。代表性业务仓库 smoke 必须证明 task/Publication/Finalizer/finish-work 不调用 verifier、不执行 verifier `not_required` round、不写 marketplace verification artifact。

### R10 删除与迁移收敛

- 只有 15 个 Skills 的 source/installed invocation trace 和静态引用全部归零，且全部 command 有 owner 时，才能删除两个共享 Python 文件。
- 删除范围包含 canonical monolith、aggregated test、installed copies、compatibility import/fallback、dead dispatcher、manifest、README、eval 和 test references。
- 从 `.5` existing repo upgrade 必须按 managed provenance 删除旧单体；未知用户修改必须通过 `.new`/`.bak` 冲突路径 fail closed。
- 不建立长期双 runtime feature flag；`.5` tag 保留为外部回滚和行为对照。

## 内部实施 Checkpoints

| Checkpoint | 范围 | 进入下一阶段的条件 |
| --- | --- | --- |
| A | inventory、schema、kernel、installer 基座；迁移 `guru-sync-base` 与 `guru-clarify-requirements` | 两个 judgment profile 的真实 public invocation、package tests、source/installed validation 全部通过，且两者不 import/read/call 单体 |
| B | 迁移 `guru-select-workflow-mode`、`guru-discover-change-context`、`guru-review-contract-wording`、`guru-review-change-request`、`guru-create-task-workspace` | 五个 package 的 command ownership、contract tests、eval 与受影响 Phase 0 integration 全部通过 |
| C | 迁移 `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit`、`guru-review-branch` | planning freshness、Phase 2 adequacy、exact staging/commit、完整 diff 与 fresh-final review 路径全部通过 |
| D | 迁移 `guru-review-task-publication`、`guru-verify-extension-installation` | Publication contract 与 source-repository-only verifier 合同通过；业务仓库 verifier 路径保持不可达 |
| E | 迁移 `guru-finalize-task`、`guru-merge-task-pr` | confirmation budget、immutable push、archive recovery、expected-head merge 与 closure mismatch 路径全部通过 |
| F | 零引用核验、删除单体、全量 install/upgrade/update/platform/business smoke、文档收敛 | 本 PR 的全部验收项通过；遗漏 owner 必须返回其所属 checkpoint 修复，不得在 F 引入新 runtime 架构 |

## Acceptance Criteria

- [ ] AC1：fresh registry 的 15 个 active Skills 及全部 validator/public invocation commands 都出现在唯一 ownership inventory 中；重复、遗漏与未知 owner 的 validator 测试均 fail closed。（R2）
- [ ] AC2：每个 package 有准确 `commands.json`、`errors/catalog.json`、薄 wrapper 和职责所需 runtime modules；不存在占位 runtime 或 Skill-specific shared-kernel 分支。（R3-R5）
- [ ] AC3：所有公开 command 的 `--help`、`--json`、参数冲突、schema mismatch、stale identity、unsafe path 与稳定 error object 测试通过。（R4、R7）
- [ ] AC4：14 个 semantic Skills 的 AI ownership 和 `guru-sync-base` 的 deterministic profile 未反转；runtime tests 无法用 exit code、空 findings 或 fixture 合成 semantic pass。（R3、R8）
- [ ] AC5：每个 package-local test 可独立运行；integration tests 只消费 public contracts；public-only eval trace 不读取 private runtime。（R9）
- [ ] AC6：canonical、installed、shared runtime 和四个平台 public projection 文件集合、字节内容与 executable mode 满足 manifest 和 validator 合同；平台 roots 中 private runtime/internal tests/error implementation 数量为 0。（R6）
- [ ] AC7：`guru_team_trellis.py`、`test_guru_team_trellis.py`、installed copies、compatibility routes 和 dead references 数量为 0；全仓 active reference scan 为 0。（R10）
- [ ] AC8：clean repo initial install、exact remote candidate install、从 `v0.6.5-guru.5` existing repo upgrade、official Trellis update 后 workflow/preset reapply 均通过，且 `.new`/`.bak` 无未处理文件。（R6、R10）
- [ ] AC9：Codex、Cursor、Claude 和 shared projection 的 discovery、真实 wrapper invocation、typed output validation 与 private-path denial 测试全部通过。（R6、R9）
- [ ] AC10：一个代表性业务仓库安装方式的 smoke 证明支持的 closeout 不读取共享单体，不调用 `guru-verify-extension-installation`，不执行 verifier `not_required` round，不写 marketplace verification artifact；报告明确标注非生产证明和未覆盖边界。（R8、R9）
- [ ] AC11：完整 `guru-check-task` 与 independent Branch Review 覆盖 `origin/main...HEAD` 全 diff，findings 为 0，并确认无遗漏 owner、第二个共享单体、public API drift 或 ownership 反转。（R1-R10）
- [ ] AC12：最终 PR title/body 为中文且具体，验证证据与实际命令一致，`Closes #195` 是唯一关闭语义，不发布 release tag，不升级未授权业务仓库。（R1、R8）

## Docs SSOT Plan

- `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md` 继续只拥有全局 phase、mandatory Skill invocation、typed-exit consumer 和 fail-closed routing。
- 各 package 的 `SKILL.md`、`references/contract.md`、`interface.json`、`commands.json` 与 public schemas/examples 是 step-local behavior 和 public I/O 的 SSOT。
- `.trellis/spec/workflow/skill-package-contract.md` 定义 package/public-private/runtime ownership 通用规则；`.trellis/spec/workflow/companion-scripts.md` 定义 executor/validator/recorder 边界。
- `trellis/presets/guru-team/README.md` 记录 installer、installed tree、platform projection、upgrade/update 和验证命令；`trellis/workflows/guru-team/README.md` 记录 marketplace workflow 使用方式。
- 根 `README.md` 仅保留面向使用者的安装、升级与验证入口，不复制 package 内部 command/error 清单。
- 实现完成时同步 canonical 与 dogfood 文档，并用 link/reference scan 阻止过期单体路径。

## 非目标

- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不在平台 projection 中复制 private runtime 来声称 package 自包含。
- 不修复或关闭 #156，不恢复 #205 已移除的业务仓库 verifier route。
- 不发布迁移后的新 release tag；release 使用合并后的独立 gate。
- 不自动升级未明确授权的业务仓库。
- 不为恶意篡改、伪造 artifact、对抗性输入、并发压力、锁、TOCTOU 或 crash consistency 增加机制；正常 stale/mismatch、错误 payload 和常见兼容边界仍在范围内。

## Open Questions

无阻塞问题。Issue 已明确单 task、package-local ownership、kernel admission、平台投影、`.5` 基线、#205 不可达合同、A-F 顺序和最终验收边界。
