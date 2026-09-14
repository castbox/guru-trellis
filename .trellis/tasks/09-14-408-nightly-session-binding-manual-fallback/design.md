# #408 设计

## 设计依据与选择

需求增量见同目录 `prd.md` 的 `R408-01..08`。项目架构 authority 为 `docs/architecture/README.md` 的 `current-main-0.6.5-guru.50`，设计宪法为 `docs/architecture/00-foundation/design-constitution.md` 的 `guru-trellis-design-constitution-v1`，变更合同为 `docs/architecture/06-governance/change-contract.md` 的 `guru-trellis-architecture-change-contract-v1`。

本任务直接演进固定 source lock 和现有 Markdown 合同，不创建第二执行路径。保留旧生命周期是 #408 的显式兼容目标，不引入额外 legacy adapter。手动操作由当前会话 AI 执行独立 Git/GitHub 请求，不取得 Guru gate、Finalizer 或 archive 的 authority。

| 设计 | 需求 | 实现 owner 与取舍 |
| --- | --- | --- |
| D408-01 固定来源 | R408-01 | 更新现有 `trellis-source.json` 的 commit，增加非空正整数 `ci_run_id`；现有 source validator 负责验证和投影。保持 `repository`、`cli_version`、`package_manager` 与 schema 1.0 的现有含义；同步受控消费者和 fixture，不增加双读缺省分支 |
| D408-02 正式模板采纳 | R408-02..03 | 使用固定 Fork 自身 `pnpm install --frozen-lockfile` 与正常 build；build 成功后写既有 `.guru-source-commit` marker。运行官方 update/init，再应用 Guru workflow/preset，不手改 upstream-owned Python/hook |
| D408-03 自动与手动边界 | R408-04..07 | canonical workflow 拥有全局停止/独立操作边界；现有 Guru Skill 在自己的错误出口处引用该边界，入口只加载/路由，不复制步骤，不新增 Skill/exit/executor |
| D408-04 同源分发与验证 | R408-02..04,08 | preset 复制完整 source record；source validator 输出 commit/CI/实际 CLI 路径，focused installed fixture 验证实际生成的 runtime/hook；现有 package 与 finish-family 证明旧链未回退 |
| D408-05 正常创建链调用闭合 | R408-03..04 | 修正 Agent-visible 脚本/示例路径，落实 Clarification/Readiness 原有 recorder 派生职责，使用当前正常 authoring 串联创建、双端 mapping、boundary 与受控激活；不改映射写入算法 |

## D408-05 实现细化

本节补齐原正常链的覆盖遗漏。现有六步重放通过，说明没有证据支持重写 workspace writer；新修改集中于调用前的合同/确定性处理和验证入口。

1. Agent discovery 投影不拥有全部包脚本或示例。Discovery、Wording、Clarification、Readiness、Workspace 的本地合同给出仓库根 cwd 与 `.trellis/guru-team/skills/packages/<skill>/` 下的实际脚本/示例位置；明确各自现有 record/check/invoke 参数，不假定参数统一。复用已有 launcher，不增加 wrapper，不让正常调用导入 eval/private runtime。
2. Clarification recorder 接受完整的 AI 语义输入，确定性产生现有 `content_identity` 与合同声明的 proposal/action/target 派生绑定；checker 和 invoke 对同一规则核验。正常 authoring 省略派生值，仍必须显式包含 AI gate、最终 decisions、source actions 和 typed exit。来自上游的 opaque duplicate snapshot token保持原值，不由此 owner 重造。
3. Readiness recorder 从当前 source/transition 和已完成语义结果绑定 `reviewed_linkage_sha256`、`scope_conclusion_sha256` 及客观 findings count。没有 AI judgement 不产生 pass；提供完整当前派生值的输入继续接受一致性校验。现有 public input/profile/exit、owner-result 输出 schema 与 consumer 保持不变，不加第二版本 reader 或兼容状态机。
4. `verify_installed_phase0_transcript.py` 改用 Workspace 已有 `transition + authoring` 正常 record 路径，移除该链对手工 private plan/digest 的依赖；扩展对 primary/worktree 两份映射、boundary、当前 session 和 `start-task.sh` 的校验。测试的预置语义输入与真实 Agent 读取合同执行的证据分开报告，不把脚本预置 pass 当 AI 审查。
5. 已有 workspace 验证 fixture 若仍发送退役 `scope`，改为消费当前正常创建链，不恢复字段或手工补 mapping。无新生产入口、无新恢复 artifact。受控激活前满足原 Planning/JSONL 条件；缺失条件必须在原 gate 停止，而不是裸 `task.py start` 代替。

实现写集限于上述现有 Skill 的本地合同/示例、Clarification/Readiness recorder/checker、对应测试、两个既有 installed transcript/workspace fixture及其必要 caller inventory投影。其余五阶段 transition、workspace executor、mapping storage、上游源码和 #398/#407 不改。

回归包含：不预填私有 digest 的有效语义输入经 managed recorder 成功；缺失语义判断仍被拒绝；正常记录后的内容变更导致旧派生绑定失配被 checker拒绝；真实 six-step stdout 连续承接到双端 mapping/boundary/受控激活；native Agent只按安装后的实际合同完成该路径。不能靠导入 eval helper、先写完整旧plan或人为补mapping使测试通过。

## Source 与运行链

```text
canonical trellis-source.json
  -> 指定 Fork checkout HEAD / package version / build marker / template bytes 校验
  -> 官方 CLI update 或 init
  -> Guru workflow 应用 + preset apply
  -> .trellis/guru-team/trellis-source.json + 实际 CLI/runtime/hook
  -> primary -> linked task -> primary 同 session 回归
```

`ci_run_id` 的直接消费者为构建/安装 provenance 输出和发布说明。对 `castbox/Trellis` 的 run metadata 读取必须证明 run id、head SHA、success 一致。CI 证明指定来源的上游构建结果；本地 build marker 只在本地正常 build 成功后产生，不能把上游 CI 成功当成本地 build 成功。

`verify_trellis_compatibility_matrix.py` 复用现有 `_validate_source_build`、`validate_fork_source` 与 `run_focused` 路径。predecessor 的历史 source 验证不要求其不存在的 CI 字段；current source lock 和 current 输出必须携带 CI identity。运行命令仍使用验证后的显式 Fork 路径，不使用全局 CLI、可变 main 或 npm fallback。

升级顺序为 official dry-run、preserve-mode update、workflow preview/显式应用、preset reapply、sidecar 逐项判定、drift/ownership。未知本地编辑不覆盖。生成文件差异单独标记，不将 upstream-owned 文件纳入 Guru ownership inventory。

## 自动失败与手动操作

自动调用失败时，AI 先停止该自动调用链，直接读取仍可获得的事实并报告错误。错误 hook 或缺失 checkpoint 不作为“没有 task”的证据。事实读取失败标为 unknown，不通过猜测、伪造 task 或补造 checkpoint 修复身份。

独立手动请求始终按下表执行；确认仅存在于当前对话，不写入任何文件、schema、DTO、checkpoint 或日志。

| 操作 | 必须重新读取与展示 | 操作后验证 |
| --- | --- | --- |
| commit | repo/worktree/branch/HEAD、完整变更和精确 stage 集、Git transaction、message、hook 影响 | 新 commit 的 parents/tree/message 与预期一致；未包含无关文件 |
| push | remote、refspec、当前本地/远端 HEAD | 指定远端分支 HEAD；不顺带创建 PR |
| PR 创建/更新 | repo/PR/base/head/head SHA、精确中文 title/body、关闭效果 | PR identity、Draft/Ready 与 metadata；不顺带 merge |
| merge | PR、当前 head、base、checks、merge 方法与精确 payload | 实际 merge commit 和 PR 状态；说明已展示的自动关闭效果 |
| Issue closure | 精确 Issue、当前状态和交付依据 | Issue 的真实 closed/open 状态；不由 task residue 推断 |
| tag/Release | Guru candidate、既有 release contract、tag target、notes、当前远端事实 | tag/Release 指向及实际发布结果；绝不发布上游 |
| cleanup | 精确资源、未提交内容/引用/使用状态、删除影响 | 只处理清单资源；不扩大删除范围 |

执行结果与 workflow residue 分栏报告。手动操作不写 Phase 2、Branch Review、Publication、Finalizer、Merge、archive 的完成标记。操作自身失败时只报告该操作失败，不伪装成自动 Guru 重入。

## 变更文件与减法边界

- 固定来源：`trellis/presets/guru-team/source/trellis-source.json`、source preparation/validator 的实际消费者、对应 fixture。
- 全局合同：`trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md`。
- 步骤局部：`trellis/skills/guru-team/packages/` 中实际声明自动失败阻断的现有 owner 文档；修改前逐个证明直接消费者，不批量重写所有 Skill。
- 入口：`trellis/presets/guru-team/overlays/` 现有三份 `guru-finish-work`，仅增加指向全局边界的路由说明。
- 验证：Fork preparation/session isolation、upgrade contract、受影响 package、finish-family 与 focused installed fixture。
- README：根 README、workflow README、preset README 更新当前来源及使用边界，历史版本记录不改写。
- 没有需要新增的 runtime recovery asset。旧 source pin 从 current source record 退出；历史 docs/ADR/归档与 predecessor fixture 保留历史用途。保留相同 source schema 的增量字段不构成新的长期兼容路径。
- 非生成代码文件修改后不超过 3000 行。当前 matrix 为 2717 行，installer 为 2777 行；达到阈值时只拆分本次触及职责，不能借机重构无关模块。

## Docs SSOT Plan

本轮只写 task planning 与上下文 JSONL，不修改 shared current。实施时先调用 RDT `task_impact_sync`，写 `docs/requirements-design-test-contributions/408-nightly-session-binding-manual-fallback/` 下的 requirements/design/test/traceability/manifest；映射 `R408 -> D408 -> T408`，不复制整个 `.50`。

Architecture 采用下节 task-local 设计作为 Planning-stage contribution；实施后由同一 owner 在 `docs/architecture/contributions/408-nightly-session-binding-manual-fallback.md` 收敛实际 before/after 与证据。shared current RDT/Architecture 仅经各自 owner 的独立 committed review 和串行 promotion 更新。promotion 后重跑 Phase 2、task commit 和完整 Branch Review；本次规划不激活 successor、不预分配 current version。

公开 README 与 `.trellis/spec/docs/`、`preset/`、`workflow/` 的受影响投影在 contribution 收敛后同步。用户授权、review 历史、原始命令输出和恢复状态不进入 tracked 文档。

## Architecture Planning Contribution

影响类型为 `architecture_impact`：外部框架 source identity 与自动流程/独立操作边界发生明确增量。唯一 change path 为 `target_native`，含义是直接使用现有 AI/tool authority，不代表实现 #398 target lifecycle。当前与目标 semantic owner 均为原 workflow/Skill AI；脚本只验证来源和执行明确命令。

| Required concern | 判定与任务合同 |
| --- | --- |
| authority-binding | applicable：绑定 public `guru-maintain-architecture-baseline:2.0`、`.50` 和项目 change-contract-v1 |
| constitution-binding | applicable：引用 current constitution-v1；本设计遵守既有 owner 与最小复杂度边界，不复制原则正文 |
| boundary-and-decision | applicable：#408 只直接演进 source 与停止后的独立操作；不建立新的 Guru lifecycle authority |
| owner-and-single-writer | applicable：任务 worktree 写 candidate；Architecture/RDT owner 分别串行提升 shared current |
| compatibility-and-exit | applicable：旧 lifecycle 为需求明确要求；无新增 adapter、fallback runtime 或双写，旧 source pin 从 current 配置退出 |
| gap-and-deviation | applicable：不关闭或重开 `ARCH-GAP-006/008`；保持现有 closure ownership，缺失实际安装证据不能描述为 GAP 已关闭 |
| parallel-scope | applicable：仅写 #408 task/contribution；禁止修改 #398/#407 工作区及 shared current 的并行版本 |
| evidence-and-freshness | applicable：当前 pin/旧回归为 before；目标 pin/CI/跨worktree/手动场景为计划 after，实际运行仍 UNVERIFIED |
| review-and-promotion | applicable：Planning 仅证明方案一致性；独立 committed review 和 expected-current promotion 后才能进入 Publication |

ADR 判定：当前方案遵循既有 AI-first、Git/GitHub authority、single-writer 与 official ownership；不改变这些架构决策，无新增 ADR。若实施发现必须新增 owner、兼容出口或改变 GAP，则停止该变更并重入 Architecture，不将它视为既有计划内容。

Evolution 对齐：`EVO-001/003/004/005/006/007` 仅由既有目标提供方向参考，分别涉及真实authority、局部增量、不中断目标、轻量上下文、完整交付和同源安装；`EVO-002` 只使用现有 Architecture gate。本任务不宣称实现任一完整 Evolution 目标。

## 重要替代与未验证边界

拒绝手工 patch 全局包或 generated hook：它无法证明正式 update 后仍生效。拒绝新增 recovery Skill/DTO：超出 #408 且形成第二流程。选择 Markdown 独立操作边界的代价是必须用真实 Agent 行为场景验证，字符串匹配不能单独证明执行正确。

本地 target Fork build、真实 installed update、同 session 正向场景、手动 Git/GitHub 行为验证及远端发布均未执行。真实远端手动验证使用独立测试资源并单独展示操作取得确认；fixture 证据与实际远端成功严格区分。
