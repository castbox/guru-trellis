## 检查完成

### 审查基线与候选范围

- Active task：`.trellis/tasks/07-23-131-guru-review-branch`
- 分支：`codex/131-guru-review-branch`
- 审查 HEAD：`38a0e8dd2314b086378e0674f4bd377dc5e6f694`
- Base / merge base：`origin/main` / `ea132e350c4b6861fc955f17e590651a46e890ab`
- 完整候选：`origin/main` 到当前工作树共 315 个 tracked diff path；其中当前 9 个 tracked dirty path 已包含在这 315 个 path 中，另有 3 个本轮开始前已有的 untracked Branch Review 报告。本文档作为新的 Phase 2 原始报告，不计入上述实现候选统计。
- Workspace boundary：通过；expected workspace 与 actual repo root 均为当前 issue worktree，source checkout 干净，suspicious source artifact 为 0。
- Planning approval：通过；`typed_exit=approved`，当前 HEAD 为 `38a0e8dd2314b086378e0674f4bd377dc5e6f694`，approval HEAD 为 `ea132e350c4b6861fc955f17e590651a46e890ab`，facts SHA-256 为 `bdb2f2e720b2224eb65af1d0cb87dafde15b82753ef296f0291b7798a336257e`。
- 本轮按 fresh Phase 2 semantic review 覆盖完整 `origin/main...HEAD` 与 dirty tree，没有复用旧 pass 结论。
- 本轮没有修改 `review.md`、`review-gate.json`、`agent-assignment.json`、`phase2-check.json`、task commit 或现有 Branch Review 原始报告，也没有 commit、push 或创建 PR。

### 已检查文件

- 需求与计划：`prd.md`、`design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`、`planning-approval.json`
- 实现交接与当前审查状态：`implementation-handoff.md`、`review.md`、`review-gate.json`、`reviews/03-finding-closure.md`、`reviews/04-final-release.md`、`reviews/05-problem-discovery.md`、`agent-assignment.json`、`task-commit-plans/003.json`
- F-131-BR4-01 五个预期实现路径：
  - `.trellis/tasks/07-23-131-guru-review-branch/implementation-handoff.md`
  - `.trellis/workflow.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - `trellis/skills/guru-team/tests/test_skill_packages.py`
- Branch Review Skill SSOT：`trellis/skills/guru-team/packages/guru-review-branch/SKILL.md`、`interface.json`、`references/contract.md`、`tests/test_contract.py`
- Docs SSOT：`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/skill-package-contract.md`，以及 task planning 中列出的其余 curated specs
- Canonical / dogfood / preset / installed / platform surfaces：`trellis/workflows/guru-team/`、`.trellis/guru-team/`、`trellis/presets/guru-team/`、`trellis/skills/guru-team/`、`.agents/`、`.codex/`、`.claude/`、`.cursor/`
- 全分支范围：`origin/main...HEAD` 的 315 个 committed changed path、当前所有 dirty path，以及 3 个既有 untracked review report
- 官方 Trellis 文档：`https://docs.trytrellis.app/index.md`、`https://docs.trytrellis.app/advanced/custom-workflow.md`、`https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`

### F-131-BR4-01 关闭结论

- `#### 3.5 Branch Review Gate` 当前只保留一次 `guru-review-branch` mandatory invocation、四个 declared typed exit、两个 workflow route target 与一个 fail-closed stop target。
- 全局 workflow 已删除 `review-branch.sh`、`check-review-gate.sh`、reviewer 角色、raw report、finding closure、fresh final、recorder/checker、artifact body/digest 等 Branch Review step-local 细节。
- `guru-review-branch` package 仍独占 13 个 entry precondition、semantic review、qualification-before-severity、finding lifecycle、recovery、fresh final、recorder/validator 与四个 typed exit；没有把职责删除或迁移到脚本。
- `.trellis/workflow.md` 与 `trellis/workflows/guru-team/workflow.md` byte parity 通过；Phase 3.5 的 routing-only regression 对 canonical 与 dogfood 同时通过。
- `get_context.py --mode phase --step 3.5` 的 Phase 3.5 注入结果只呈现 invoke、typed exits、workflow targets 与全局路由说明，没有重新注入 Branch Review 内部闭环。
- 结论：`F-131-BR4-01` 已在当前候选中关闭。

### 本轮新发现与自修复

- Finding：`F-131-P2-R5-01`
- Severity：P2
- Scope：normal required behavior / AC15 开箱即用与 upgrade-update 门禁
- 问题：`verify-throwaway-install.sh` 在 `trellis workflow --create-new` 后仍无条件断言 `.trellis/workflow.md.new` 包含旧的 `review-source independent-agent` 文案。显式 public `main` 采样会因远端尚未合入新 workflow 而偶然通过，但精确 feature ref 或合并后的 `main` 会因 routing-only workflow 正确删除该文案而失败。
- 修复：
  - public `main` 仅作为显式 opt-in discovery sample 时，只验证 `.new` 是有效 Guru Team workflow；
  - 精确当前/发布 ref 时，要求 `.new` 含 `guru-review-branch` mandatory invoke，并要求旧 `review-source independent-agent` 文案不存在；
  - 新增聚焦测试，只截取 `.new` preview check 段验证分支、当前 invoke 与旧文案负断言，避免被脚本其他相似字符串误通过。
- 修复后 focused regression、169 项 Skill package suite、45 项 preset suite、完整 throwaway 与所有静态检查均通过。
- 结论：`F-131-P2-R5-01` 已关闭。

### 十维语义复核

- 范围与需求：变更只关闭 accepted current finding 和本轮正常发布路径 finding；没有扩张到恶意篡改、对抗输入、TOCTOU、锁、原子性或并发加固。
- 运行时行为：全局 workflow 只编排 phase、mandatory invocation、typed exit consumer 与 fail-closed stop；Branch Review 内部闭环保留在 package。
- 合同与 API：Skill id、四个 exit id、schema、public input/output 与 consumer projection 未改变。
- Docs SSOT：策略为 `ssot_first`。现有 workflow/skill package contract 已定义 global-vs-step-local ownership；本轮脚本/test 自修复只是让开箱验证承接现有合同，不产生新的 durable contract delta。
- Canonical / dogfood：workflow byte parity 通过；package、adapter 与平台 wrapper parity 由完整 Skill / installed validation 覆盖。
- Preset / overlay / upgrade：dogfood drift、ownership、public marketplace preview/switch、`trellis update --force`、workflow/preset reapply、normal/no-developer fixture 与 sidecar 检查均通过。
- 测试：focused routing、runtime full、Skill package、preset installer、ownership、package contract、shared eval 与 throwaway 全部取得终态。
- 安全与仓库卫生：credential、绝对本机路径、敏感文件名、debug marker 扫描未发现新增问题；测试生成的 23 个 `*.pyc` 和 5 个 `__pycache__` 目录已删除，复扫为 0。
- 发布与部署：未修改 CI/CD、Docker/Compose、Kubernetes/Kustomize、DB migration、Makefile 或生产配置；无部署迁移要求。
- 审查证据：当前 `review-gate.json` 仍诚实记录上一轮 `F-131-BR4-01` 为 open / `implementation_required`。本轮没有篡改它；主会话需要先记录新的 Phase 2 gate、提交当前非 metadata 修复，再执行新的独立 Branch Review finding-closure / fresh-final round。

### 已修复问题

- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - 修复 `.new` preview 对旧 Branch Review step-local 文案的错误正向依赖；
  - 区分 public discovery sample 与精确当前/发布 ref 的语义断言。
- `trellis/skills/guru-team/tests/test_skill_packages.py`
  - 新增 `test_throwaway_preview_checks_current_branch_review_routing`，阻止旧正向断言回归。

### 未修复问题

- 无 P0/P1/P2/P3 current-scope 实现 finding。
- 非阻塞限制：
  - 远端尚无包含当前 dirty 修复的精确 feature ref；默认 throwaway 因禁止把 public `main` 当作当前分支而按预期 exit 2。显式 `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 后，public marketplace discovery 加本地未发布 canonical sample 的完整链路 exit 0。
  - 当前环境未安装或仓库未配置独立 `ruff`、`mypy`、`pyright`、`shellcheck`；以 JSON parse、`/bin/bash -n`、Python in-memory compile、`git diff --check`、仓库 validator 与完整测试覆盖。
  - 一次并行 adapter eval 的 Claude/Codex 直接终态输出未被调用层保留，因此不作为独立通过证据；169 项完整 Skill suite 和 source/installed shared eval 已覆盖对应 adapter/corpus 合同。
  - 未验证未来 Trellis CLI 版本；完整 throwaway 覆盖仓库当前锁定/声明的 Trellis CLI `0.6.5`。运行日志提示 npm 最新为 `0.6.8`，不能据此声称未来版本兼容。

### 验证结果

- Focused Branch Review routing-only regression：通过，1/1。
- Focused throwaway preview regression：通过，1/1。
- Runtime full suite：通过，566 passed / 13 skipped，exit 0。
- `guru-review-branch` contract suite：通过，8/8，exit 0。
- Skill package suite（自修复后最终复跑）：通过，169/169，exit 0。
- Preset installer suite：通过，45/45，exit 0。
- Upstream ownership tests：通过，6/6，exit 0。
- Source package validator：通过，10 active skills / 39 exits / 23 targets。
- Installed package validator：通过，10 active skills / 39 exits / 23 targets；1903 managed files，0 sidecar / removal / conflict。
- Direct ownership validator：通过，43 frozen/active paths、37 generated、6 legacy-not-generated、43 overlay paths、13 claims、48 assets。
- Shared eval：source 7/7、installed 7/7 通过；Cursor source adapter 对 7 个 case 返回声明的 `unsupported` typed result。
- Full throwaway：
  - 默认模式：按预期 exit 2，明确拒绝把 public `main` 冒充当前 dirty feature ref；
  - 显式 public-sample 模式：exit 0，覆盖 fresh init、existing preview/switch、三平台入口、package smoke、wrapper/eval、initial/after-update closeout、task workspace、`trellis update --force`、workflow/preset reapply、normal/no-developer fixture、三次 ownership checkpoint、dogfood 与最终无 sidecar。
- Lint / static：2634 个 JSON 文件解析通过，295 个 shell 文件 `/bin/bash -n` 通过，`git diff --check origin/main` 与 `git diff --check origin/main...HEAD` 通过，dogfood overlay drift 通过。
- TypeCheck：仓库无独立 type checker；116 个 Python 文件 in-memory compile 通过。
- Task validation：通过，`implement.jsonl` 11 entries、`check.jsonl` 0 entries。
- Workspace / planning：boundary 与 fresh planning approval validator 均通过；source checkout 干净。
- Repository hygiene：Git index 为空，canonical/dogfood workflow byte parity 通过，测试生成 sidecar 复扫为 0。

### 证据交接

- 阶段二：完整候选、F-131-BR4-01、F-131-P2-R5-01、五个预期实现路径、Branch Review package ownership、测试、安装/升级、三平台分发、ownership、静态与安全范围均已覆盖。本报告可供主会话记录新的 `phase2-check.json`，但 recorder/validator 不能替代主会话的 semantic gate。
- Docs SSOT：`ssot_first`；官方 Trellis workflow 扩展面、当前 local workflow contract、Skill package contract、canonical/dogfood workflow、preset 验证脚本与测试当前一致。`trellis-meta` 的 local architecture / customize-local 指南约束了本轮只在 canonical + dogfood Markdown workflow 和确定性验证脚本层处理相应职责。
- Branch Review：本轮是提交前 Phase 2，不替代 post-commit Branch Review。提交当前 Phase 2 修复与证据后，必须以新 HEAD 对完整 `origin/main...HEAD` 重新执行独立 finding-closure 与 fresh-final review。
- 现有 `review.md` / `review-gate.json`：仍是上一轮 `implementation_required` 证据，不能直接作为 pass gate 复用。
- 部署/安全：无部署资产或生产迁移变化；没有引入 secret、本机绝对路径或私有运行状态。

### 结论

`F-131-BR4-01` 与本轮发现的 `F-131-P2-R5-01` 均已关闭，完整候选与 Docs SSOT 一致，所需验证终态通过，未发现新的 open current-scope finding。

Typed exit：`guru-check-task:passed`
