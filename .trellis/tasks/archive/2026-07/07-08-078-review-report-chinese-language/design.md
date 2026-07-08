# #78 详细设计：Branch Review report 中文规则防复发

## 设计目标

在不改变 Branch Review raw report retention 数据模型的前提下，把 #57 中文 artifact
规则扩展到 #70 新增的 `reviews/*.md` raw reports 和 `review.md` rollup。

设计分三层：

- Markdown 合同：workflow、spec、durable docs 明确规则和 literal token 例外。
- 生成入口：continue / check-agent / platform overlay 明确 raw report 与 rollup 的中文结构。
- 客观校验：companion Python 在 record/validate gate 时扫描明显英文模板标题，测试覆盖防复发。

## 官方 Trellis 依据

- `https://docs.trytrellis.app/advanced/custom-workflow.md`：`/.trellis/workflow.md`
  定义 Trellis 开发流程，phase、skill routing、workflow-state 和 task command
  catalog 都在 Markdown 中；运行时读取，不需要改 Python/hook 或重新发布 Trellis。
- `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`：
  spec template marketplace 用于可复用工程约定、测试规则、release rules 和 review
  checklist；不得作为 remote task store，也不得放 `.trellis/tasks/`、workspace
  或平台 prompt 文件。

因此本任务不修改 Trellis upstream/npm 包，不把 AI 语义判断写进脚本；脚本只做
机器可判定的模板痕迹检查。

## 目标文件与职责

### Canonical workflow 和 dogfood workflow

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`

改动点：

- Artifact Language 小节加入 `reviews/*.md`；
- Branch Review Gate 小节明确 raw report 和 rollup 的中文标题、字段名和叙述规则；
- 给出推荐中文 rollup 小节名：`审查轮次`、`问题生命周期`、`最终审查`、`证据`、
  `观察项`、`后续候选`、`结论`；
- 明确 literal token 例外。

### Platform / overlay entrypoints

Canonical overlay 源头：

- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md`
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
- `trellis/presets/guru-team/overlays/.codex/agents/trellis-check.toml`
- `trellis/presets/guru-team/overlays/.claude/agents/trellis-check.md`
- `trellis/presets/guru-team/overlays/.cursor/agents/trellis-check.md`

Dogfood 安装副本由 `apply.sh --repo .` 同步。

改动点：

- continue 入口的 “after commit” 路径补充：raw report 与 rollup human-readable 内容中文为主；
- check agent 的 Branch Review 输出格式改为中文标题和字段名；
- Codex check agent 保持 `nickname_candidates` ASCII，只改 `developer_instructions` 的输出结构；
- Claude / Cursor / channel runtime check agent 保持技术 id 不变，只改报告模板。

Finish-work 入口通常只消费 gate，不生成 review report；如果文案提到 review evidence，
同步强调已存在的 `review.md` / `reviews/*.md` 应为中文 human-readable artifact。

### Durable docs 与 spec

- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- 必要时同步 `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`

改动点：

- durable docs 记录 `reviews/*.md` 与 `review.md` 的中文规则；
- overlay guidelines 把中文 raw/rollup report 纳入必备内容；
- quality guidelines 增加本任务相关 grep/test/check 关注点。

### Companion Python validator / tests

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`

设计：

1. 增加常量 `FORBIDDEN_REVIEW_REPORT_ENGLISH_TEMPLATE_HEADINGS`，至少包含 issue 指定的
   五个字符串。
2. 增加纯函数，例如 `review_report_language_template_errors(root, task_dir, review_report, review_reports)`：
   - 读取 final `review.md`；
   - 读取 `review_reports[]` 中每个 `reviews/*.md` raw report；
   - 只扫描明显英文模板标题 / 小节行；
   - 返回中文错误，指出 path 和命中的 forbidden heading。
3. 在 `cmd_review_branch` 中，`review_report`、`review_reports` 和
   `agent_assignment` 校验完成后调用该函数。pass 与 findings artifact 都应阻塞，
   因为 failed gate artifact 也会持有 prior independent review evidence。
4. 在 `validate_review_gate` 路径中也复用校验，避免旧 artifact 或后续文件被改回英文模板。
5. 单测覆盖：
   - final `review.md` 含 `Review Rounds` 时 `review-branch --pass` 失败；
   - raw `reviews/*.md` 含 `Evidence Handoff` 时 `review-branch --pass` 失败；
   - 中文 rollup + raw report 通过现有 digest/link 校验；
   - `Deployment / safety impact` / `Follow-up Candidates` 等 issue 指定字符串至少在测试中覆盖。

该校验不判断“中文比例”或审查语义充分性，只阻止已知英文模板痕迹。

## 同步与安装副本策略

1. 先改 canonical：`trellis/workflows/guru-team/**` 和
   `trellis/presets/guru-team/overlays/**`。
2. 运行：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

3. 如出现 `.new` / `.bak`，逐一检查处理，不能带着未决冲突进入 commit。
4. 再检查 dogfood 安装副本是否与 overlay 同步。

## 验证设计

最小验证命令：

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-078-review-report-chinese-language
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

实际 unittest import path 可能因目录含 `-` 不能直接用 module path；实现阶段以仓库现有测试命令为准。

开箱即用门禁若时间允许，运行 throwaway install：

```bash
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

若完整 throwaway 安装无法跑完，最终报告必须明确未覆盖项。

## 风险与回滚

- 风险：校验过严误伤普通英文 literal token。缓解：只拦截固定英文模板标题，
  不做泛化语言比例判断。
- 风险：只改 dogfood 副本导致 update 后丢失。缓解：先改 canonical overlay，
  再 apply + drift check。
- 风险：平台 prompt 不一致。缓解：按 overlay 源头同步 Codex / Claude / Cursor /
  channel runtime check agent。
- 回滚：本任务变更集中在 Markdown/overlay/Python validator/test；如发现误伤，可回滚
  forbidden heading 列表或调用点，不影响 #70 digest 数据模型。
