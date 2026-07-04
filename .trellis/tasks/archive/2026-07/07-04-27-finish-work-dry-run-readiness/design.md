# #27 详细设计

## 设计结论

在 `cmd_finish_work()` 中保留现有前置校验顺序：intent marker、repo/config/handoff/task、Branch Review Gate、non-metadata dirty path、PR body/readiness。完成这些只读校验和派生字段计算后，如果 `args.dry_run` 为真，立即返回一个 planned action payload，不进入 archive、journal、metadata commit 或 `cmd_publish_pr()`。

正式路径继续使用现有实现：archive task、add session journal、`commit_if_metadata_dirty()`、重写 archived task artifact path、内部调用 `cmd_publish_pr()`。

同时把 Guru Team Codex dispatch 默认模式改为 `sub-agent`：缺省配置与新安装项目走 `[workflow-state:in_progress]`，main session dispatch `trellis-implement` / `trellis-check`；显式 `codex.dispatch_mode: inline` 才走 `[workflow-state:in_progress-inline]`。这样 Branch Review Gate 的 independent review 要求在 Codex 默认路径下可达，不会因默认 inline 阻塞 `trellis-finish-work`。

## 行为边界

- dry-run 允许读取文件、读取 Git 状态、解析 task/handoff/gate/ledger、校验 PR body/readiness。
- dry-run 不允许调用：
  - `python3 ./.trellis/scripts/task.py archive ...`
  - `python3 ./.trellis/scripts/add_session.py ...`
  - `commit_if_metadata_dirty(...)`
  - `cmd_publish_pr(...)`
  - `git push`
  - `gh pr create`
- publish readiness 校验仍在 dry-run 下执行；non-draft 缺少 reviewed body source 时仍阻塞，因为这是 readiness preview 的核心价值。
- `publish-pr --dry-run` 自身保持内部 helper 语义不变；本任务只改变 `finish-work --dry-run` 不再通过 archive/journal 后转调 publish。
- Codex sub-agent 不继承 parent transcript 的风险通过 agent prelude 消解：dispatch prompt 首行必须包含 `Active task: <task path>`，agent 若未拿到该行则运行 `task.py current --source`，再读取 `check.jsonl` / `implement.jsonl` 与 task artifacts。
- `inline` 模式保留但必须显式配置，适用于暂时无法使用 Codex sub-agent 的项目或调试场景。

## Payload 设计

`finish-work --dry-run` 返回：

- `status: "dry-run"`
- `task_dir` / `task_name`
- `review_gate` / `reviewed_head`
- `checks`
  - `non_metadata_dirty_paths`
  - `pr_readiness.body_source`
  - `pr_readiness.reviewed_source_required`
  - `pr_readiness.reviewed_source_ok`
  - `pr_readiness.body_quality_ok`
- `plan`
  - `archive`: `would_run`、`task_name`、`skip`
  - `journal`: `would_run`、`title`、`summary`、`commits`、`skip`
  - `metadata_commit`: `would_run`
  - `publish`: `would_run`、`repo`、`base_branch`、`head_branch`、`remote`、`draft`、`title`、`body_source`
- `dry_run_side_effects: false`

该 payload 只描述计划，不承诺业务充分性；PR body 内容真实性仍由 AI readiness review 负责。

## 同步范围

- canonical source: `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- dogfood installed copy: `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- tests: `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- workflow/docs: `trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`README.md`
- Codex dispatch: `.codex/hooks/inject-workflow-state.py`、`.trellis/scripts/common/workflow_phase.py`、`.trellis/config.yaml`、`trellis/workflows/guru-team/config-template.yml`、`.codex/agents/trellis-check.toml`、`.codex/agents/trellis-implement.toml`

## 兼容性

- 非 dry-run 正式 finish-work 输出仍包含 `metadata_commit` 和 `publish`。
- dry-run 输出 shape 会新增 plan/checks 字段；这是 issue #27 的目标行为，不需要兼容旧的“archive/journal 后 dry-run publish”语义。
- parser help 改为明确无副作用，避免 throwaway install 或人工 recovery 误用。
- Codex 默认模式从 inline 改为 sub-agent 是行为变更；显式 `codex.dispatch_mode: inline` 继续兼容旧行为。

## 风险与缓解

- 风险：dry-run 不再调用 `cmd_publish_pr()`，可能漏掉 publish 内部某些客观校验。
  - 缓解：在 `cmd_finish_work()` dry-run 分支复用与 publish 相同的关键输入解析和 readiness 校验，包括 PR body quality、reviewed source、repo/base/head/draft/title/body source。
- 风险：canonical 与 dogfood copy 漂移。
  - 缓解：修改 canonical 后运行 preset apply 同步 dogfood，再运行 dogfood overlay drift check。
- 风险：文档仍暗示 dry-run 会 archive/journal。
  - 缓解：搜索并更新 `finish-work` / `dry-run` 相关文案。
- 风险：Codex sub-agent 在 `fork_turns="none"` 下拿不到上下文。
  - 缓解：保留并强化 agent prelude 的 `Active task:` / `task.py current --source` 加载路径；增加 hook/parser 测试覆盖缺省 sub-agent 与显式 inline。
- 风险：新安装项目缺少 `codex.dispatch_mode` 时行为变化。
  - 缓解：在 `config-template.yml`、README 和 workflow 中明确默认 sub-agent，inline 作为显式降级；preset apply 同步 dogfood 后运行 drift check。
