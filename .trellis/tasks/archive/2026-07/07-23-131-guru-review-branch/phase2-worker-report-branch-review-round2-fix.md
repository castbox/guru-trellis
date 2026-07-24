## 检查完成

### 审查基线与候选范围

- Active task：`.trellis/tasks/07-23-131-guru-review-branch`
- 审查 HEAD：`0fdbb708f91296847b5812c3c1b9dd80b6e488a2`
- Merge base：`ea132e350c4b6861fc955f17e590651a46e890ab`
- 完整候选：`origin/main` 至当前工作树，共 312 个 tracked diff path；当前 9 个 tracked dirty path 均已包含在这 312 个 path 中，另有 1 个 untracked Branch Review 报告，因此候选共 313 个唯一 path。
- Workspace boundary：通过；expected workspace 与 actual repo root 均为当前 issue worktree，source checkout 干净，suspicious source artifact 为 0。
- Planning approval：通过；`typed_exit=approved`，`ambiguity_review`、fixed-scope scanner、normative-hit review、来源与 planning document digest 均由 validator 确认为新鲜有效。
- 本轮只写本报告，未修改实现、现有 review/gate/assignment、task commit、`phase2-check.json`，未执行 commit、push 或 PR 操作。

### 已检查文件

- 需求与计划：`prd.md`、`design.md`、`implement.md`、`check.jsonl`、`implement.jsonl`、`planning-approval.json`
- 实现交接与审查证据：`implementation-handoff.md`、`review.md`、`review-gate.json`、`reviews/02-finding-closure.md`、`agent-assignment.json`、`task-commit-plans/002.json`
- F-131-BR2-01 实现：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - `.trellis/guru-team/extension.json`
- Docs SSOT 与合同：`.trellis/spec/workflow/skill-package-contract.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/workflow/companion-scripts.md`，以及 `implement.jsonl` 中其余 curated specs
- Canonical / installed / preset / platform package：`trellis/workflows/guru-team/`、`.trellis/guru-team/`、`trellis/presets/guru-team/`、`.agents/`、`.codex/`、`.claude/`、`.cursor/`
- 全分支范围：`origin/main...HEAD` 的 312 个 committed changed path，以及当前所有 dirty path

### F-131-BR2-01 关闭结论

- 根因成立：旧 helper 只要发现任意轮次的 replacement closure 就返回成功，导致 finding 的 round 2 lifecycle 可能被不相连的 round 3 closure 错误支撑。
- 修复正确：`finding_round_has_replacement_closure(...)` 新增可选 `expected_closure_round`；per-finding lifecycle 传入当前 `closure_number`，因此只接受该 finding 当前轮次的 replacement closure。
- 错轮次已被拒绝：新增回归测试证明，合法 round 2 replacement 存在时，不相连的 round 3 closure 不会再支撑 round 2 closure evidence。
- 兼容语义保持：
  - 合法 round 2 replacement lifecycle 仍通过；
  - explicit new-agent 与 chained new-agent lifecycle 仍通过；
  - same-agent prior-head closure 仍通过；
  - branch-wide/global final validation 仍不传 `expected_closure_round`，继续接受任意有效 replacement recovery chain。
- 未引入第二套 lifecycle helper，也未改变公共 Skill I/O、typed exit、schema 或现有 durable contract。
- 结论：`F-131-BR2-01` 已在当前候选实现中关闭；未发现新的 P0/P1/P2/P3 current-scope finding。

### 十维语义复核

- 范围与需求：实现仅修复 accepted current finding，未扩张到恶意篡改、对抗输入、TOCTOU、锁、原子性或并发加固。
- 运行时行为：per-finding exact-round 与 global final any-valid-closure 两层语义分离正确。
- 合同与 API：public Skill I/O、exit、schema、consumer projection 未改变；既有 same-agent/new-agent/replacement 语义保持。
- Docs SSOT：策略为 `ssot_first`。当前 durable docs 已定义完整 recovery chain；本轮 runtime 是追平现有合同，不需要新的 durable docs delta。
- Canonical / installed：runtime byte parity 通过；workflow、package、adapter、平台 wrapper parity 均通过。
- Preset / overlay / upgrade：source/installed package validator、ownership validator、dogfood overlay drift 与 throwaway install/update/reapply 均通过。
- 测试：focused regression、runtime full、Skill package、preset installer、ownership、contract 与 shared eval 全部终态通过。
- 安全与仓库卫生：credential、绝对本机路径、task/workspace 路径、敏感文件名扫描通过；无残留 `__pycache__` / `*.pyc` sidecar。
- 发布与部署：未修改 CI/CD、container、K8s、DB migration、Makefile 或生产配置；无部署迁移要求。
- 审查证据：现有 `review-gate.json` 仍诚实记录上一轮 `implementation_required`，本轮 reviewer 未篡改；主会话需要基于本报告记录新的 Phase 2 gate，并在提交后重新执行独立 Branch Review closure round。

### 已修复问题

- 无。本轮是 Phase 2 reviewer；实现修复已由 implementation worker 提供，reviewer 仅验证并写本报告。

### 未修复问题

- 无 current-scope 实现问题。
- 非阻塞限制：
  - 远端尚无当前 feature ref；默认 throwaway 因禁止把 public `main` 当作 feature ref 而按预期返回 exit 2，使用显式 `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 后完整 throwaway 终态 exit 0。
  - 本仓库未声明独立 `ruff`、`mypy`、`pyright` 或 `shellcheck` 工具；已用 JSON parse、`bash -n`、Python compile、`git diff --check` 与仓库 validator 覆盖静态检查。
  - 本轮没有验证未来 Trellis CLI 版本或真实发布后的远端 feature ref；当前验证覆盖仓库锁定/可用 CLI、public marketplace discovery 与本地未发布 canonical sample。

### 验证结果

- Focused F-131-BR2-01 regression：通过，6/6。
- Runtime full suite：通过，566 passed / 13 skipped，exit 0。
- `guru-review-branch` contract suite：通过，8/8，exit 0。
- Skill package suite：通过，167/167，exit 0。
- Preset installer suite：通过，45/45，exit 0。
- Upstream ownership tests：通过，6/6，exit 0。
- Source package validator：通过，10 active skills / 39 exits / 23 targets。
- Installed package validator：通过，10 active skills / 39 exits / 23 targets；1903 managed files，0 sidecar / removal / conflict。
- Direct ownership validator：通过，43 frozen/active paths、37 generated、6 legacy-not-generated、43 overlay paths、13 claims、48 assets。
- Shared eval：source 7/7、installed 7/7，全部通过；覆盖 `workflow-passed`、`standalone-passed`、`implementation-required`、`scope-confirmation-required`、`blocked-stale`、`finding-fix-passed`、`fresh-final-passed`。
- Full throwaway：默认安全拒绝 exit 2 符合预期；显式允许 public marketplace sample 后 exit 0。覆盖 fresh init、existing preview/switch、平台入口、package smoke、wrapper/eval、closeout/task workspace、`trellis update --force`、workflow/preset reapply、normal/no-developer fixture、ownership/dogfood/post-reapply。
- Lint：通过。2633 个 JSON 文件解析、295 个 shell 文件 `bash -n`、`git diff --check origin/main`、`git diff --check origin/main...HEAD`、dogfood overlay drift 均通过。
- TypeCheck：不适用（仓库未声明独立 type checker）；116 个 Python 文件 compile 通过。
- Tests：通过。
- Task validation：通过，implement context 11、check context 0。
- Repository hygiene：index 为空，source checkout 干净，当前 worktree 无测试生成 sidecar。

### 证据交接

- 阶段二：已覆盖完整候选、F-131-BR2-01 代码路径、正常 replacement/same-agent/new-agent/global-final 语义、全套测试、安装/升级、所有支持平台入口、ownership、eval、静态与安全检查。本报告可支撑主会话生成新的 `phase2-check.json`，但 semantic gate 仍必须由主会话按 Skill 合同记录。
- Docs SSOT：`ssot_first`；durable docs、task artifacts、runtime、package、tests 当前一致。本轮是 runtime 对既有 exact-round closure 合同的实现补齐，不需要 task delta merge 或 follow-up docs issue。
- Branch Review：本轮不是 post-commit Branch Review，不替代下一轮 Branch Review Gate。完整审查 HEAD 为 `0fdbb708f91296847b5812c3c1b9dd80b6e488a2`；提交当前 Phase 2 修复和证据后，应以新 HEAD 对 `origin/main...HEAD` 再做独立 finding-closure review。
- 部署/安全影响：无 CI/CD、容器、K8s、数据库迁移、Makefile 或生产配置变化；公开包 credential/路径/敏感文件扫描通过。
- 现有 `review.md` / `review-gate.json`：仍属于上一轮 `implementation_required` 证据，不能直接用作 Branch Review Gate pass；本报告只支撑新的 Phase 2 gate。

### 结论

`F-131-BR2-01` 已关闭，完整候选与 Docs SSOT 一致，所有必需验证终态通过，未发现新的 current-scope finding。

Typed exit：`guru-check-task:passed`
