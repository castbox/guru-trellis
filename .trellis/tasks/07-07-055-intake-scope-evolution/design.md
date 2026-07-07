# #55 设计：Issue Intake Scope Evolution

## 设计目标

把 issue intake “与时俱进”的要求放回 Guru Team Markdown workflow 和平台 overlay 中，让 AI 在运行时执行判断；companion script 继续只提供事实读取、执行、校验和记录能力。

## 影响面

### Canonical workflow

- 修改 `trellis/workflows/guru-team/workflow.md`：
  - Phase 0 intake 增加 “需求清晰度 / brainstorming 判定”。
  - Phase 1 planning 增加 “澄清结果同步到 GitHub issue comment/body 或新 issue body”。
  - Phase 1/2 增加 “Scope Change Gate”：新增需求或引用其他 issue 时，必须询问用户纳入当前 task 还是新开 issue，并同步 `issue-scope-ledger.json`。

### Preset overlay

- 修改 `trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md` 及平台对应 start 入口，让新会话 fallback 明确：
  - read issue body/comments 后判断是否需要 brainstorming；
  - 不足以 planning 时先澄清；
  - 澄清结论需要回写 issue comment/body 或 proposed issue body。
- 修改 `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md` 及平台对应 continue 入口，让 ongoing task 明确 scope-change gate。

### Dogfood installed copies

- 改 canonical overlay 后运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步：
  - `.agents/skills/trellis-start/SKILL.md`
  - `.agents/skills/trellis-continue/SKILL.md`
  - `.codex/prompts/trellis-start.md`
  - `.codex/prompts/trellis-continue.md`
  - `.codex/skills/trellis-start/SKILL.md`
  - `.codex/skills/trellis-continue/SKILL.md`
  - 以及 Cursor/Claude overlay 安装副本（如果当前 dogfood repo 安装了）。

### Durable docs

- 更新 `docs/requirements/guru-team-trellis-flow.md` 中 Phase 0/Phase 1 能力说明，补充 issue 清晰度、brainstorming、scope 增补留痕。
- 如 `docs/requirements/requirement-main.md` 的能力总览需要新能力条目，也一并更新。

## 行为合同

### Intake Clarity Gate

AI 在 handoff review 前必须区分三种情况：

| 情况 | 行为 |
| --- | --- |
| 明确 issue 且范围/验收足够 | 进入 handoff review 与 task 创建。 |
| 明确 issue 但范围/验收不足 | 先进行 `trellis-brainstorm` 式澄清；必要时把结论追加 comment 或建议更新 body。 |
| 无 issue 的自然语言请求 | 先 duplicate search 和 proposed issue；若请求模糊，先澄清，再生成 reviewed issue body。 |

### Issue Evidence Update Rule

- comment 优先用于追加澄清、scope 变更、用户确认、最终 closeout 口径。
- body 更新适合修正明显过期或会误导后续 intake 的原始需求，但必须由 AI/human 判断并说明原因。
- 新 issue body 适合新的交付单元、扩大边界、后续工作或当前 task 不能完整闭环的范围。

### Scope Change Gate

任务中出现新需求或关联 issue 后，AI 必须：

1. 停止把新范围直接塞进实现。
2. 给出推荐分类：当前 `close_issues`、`related_issues`、`followup_issues` / 新 issue。
3. 向用户确认分类。
4. 将结论写入 GitHub issue/comment 与 task artifact。

## 兼容性

- 不改变 `prepare-task` JSON schema 的强制字段。
- 不改变现有脚本的副作用 flags。
- 不新增 GitHub 写操作的自动判定；如果后续需要确定性 helper，可作为 executor 输入已审查 body/comment 文本后再执行。

## 风险与取舍

- 风险：只改 workflow 可能缺少机器强制力。取舍：issue 55 的核心是 AI 判断流程，按仓库 AGENTS.md 和 companion script 边界，不应把智能判断写进脚本。
- 风险：overlay 入口太简略会让新会话漏读规则。缓解：start/continue overlay 加短提示，并保留 “Full contract lives in `.trellis/workflow.md`”。
- 风险：dogfood installed copies 漂移。缓解：运行 preset apply 和 drift check。

## 验证设计

- 文本检查：
  - `rg "Intake Clarity|Scope Change|brainstorm|issue comment|issue-scope" ...`
  - `git diff --check`
- 脚本/测试：
  - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
  - `python3 -m py_compile ...`
  - `python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis` 的可运行等价命令（按文件路径执行）。
- Overlay/安装：
  - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
  - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- 开箱即用：
  - 如本轮时间允许，运行 `verify-throwaway-install.sh`；若未跑完整 throwaway install，最终报告必须列出未覆盖项。
