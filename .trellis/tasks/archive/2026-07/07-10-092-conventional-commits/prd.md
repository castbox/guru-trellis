# #92 中文 Conventional Commits 规范

## 目标

把 issue #92 的提交规范固化为 `guru-team` workflow 的长期合同。进入 PR 分支和 `main` 的工作提交、Trellis metadata 提交、merge commit subject/body 必须使用 Conventional Commits 前缀、主 issue 位置、中文描述和 `Refs` / `Closes` 分工。

## 证据

- GitHub issue：`https://github.com/castbox/guru-trellis/issues/92`
- 官方 Trellis 文档核对：`https://docs.trytrellis.app/index.md`
- 官方 workflow 扩展面核对：`https://docs.trytrellis.app/advanced/custom-workflow.md`
- 官方 spec template marketplace 边界核对：`https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`
- 仓库规范：`.trellis/spec/workflow/index.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/workflow/quality-guidelines.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/docs/public-docs.md`

## 已确认事实

- canonical workflow 位于 `trellis/workflows/guru-team/workflow.md`。
- dogfood active workflow 位于 `.trellis/workflow.md`。
- canonical companion script 位于 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`，dogfood copy 位于 `.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- preset installer 从 `trellis/workflows/guru-team/` 复制 managed companion assets，再应用 `trellis/presets/guru-team/overlays/`。
- 当前 publish helper 只创建 PR，不执行 merge；因此本任务必须生成合规 merge commit subject/body 和明确 merge 命令输入，不能依赖 GitHub 自动 subject。
- 当前 finish/publish metadata commit subject 为 `chore(trellis): finalize task metadata`，不含 issue id 和中文描述。
- PR body 的 issue 关闭语义继续由 `Closes #92` 承担；commit message 必须只用 `Refs #92`。

## 需求

### R1 Workflow 合同

`trellis/workflows/guru-team/workflow.md` 和 `.trellis/workflow.md` 必须新增提交规范合同，覆盖工作提交、Trellis metadata 提交、merge commit、commit body、Phase 2 check、Branch Review Gate、finish-work、PR readiness 和 publish 后 merge 指令。

### R2 确定性校验器

`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 必须提供机器可判定的提交规范校验能力，阻塞下列不合规 subject：

- `Merge pull request #91 from ...`
- `完成：#73 ... (#91)`
- `#73 docs(agents): ...`
- `docs(#73): ...`
- `docs(agents): 合并 Trellis 官方文档链接 Markdown 化`
- `Update Guru Team extension public API metadata`

校验器必须接受下列合规 subject：

- `docs(agents): #73 将 Trellis 官方文档链接改为 Markdown 端点`
- `chore(trellis): #73 归档任务元数据`
- `chore(merge): #91 合并 #73 Trellis 官方文档链接 Markdown 化`

### R3 commit body 合同

工作提交 body 必须含 `背景：`、`变更：`、`边界：`、`验证：`，顺序固定，footer 使用 `Refs #<primary_issue>`。commit body 不得含 `Closes #<issue>`。

Trellis metadata 提交必须不写 body，subject 必须表达 metadata 动作。

merge commit body 必须含 `合并：`、`范围：`、`审计：`，并含 `PR: #<pull_request>` 与 `Refs #<primary_issue>`。

### R4 生成入口

finish-work metadata commit 必须生成合规 subject。publish dry-run 与正式 publish payload 必须输出合规 merge commit subject/body 和显式 merge 命令参数，供维护者执行 merge 时使用。脚本不得自动判断 PR 是否能 merge；PR readiness 仍归 AI review gate。

### R5 Canonical 与 dogfood 同步

必须先修改 canonical source，再运行 preset apply 同步 dogfood installed copy。若产生 `.new` 或 `.bak`，必须逐项处理并记录结果。

### R6 验证

必须补单测覆盖 issue #92 的正反例、work commit body、metadata commit body、merge commit body、finish/publish payload。必须执行语法检查、单测、dogfood drift 检查、workflow context 读取、throwaway 安装验证。

## 验收标准

- [ ] `guru-team` workflow 文档含提交 subject、body、issue id 位置、merge commit 合同。
- [ ] finish-work metadata commit 不再生成 `chore(trellis): finalize task metadata`。
- [ ] publish 输出合规 merge commit subject/body 和显式 merge 命令参数。
- [ ] 新增提交校验器对 issue #92 正反例给出确定性结果。
- [ ] Phase 2 check、Branch Review Gate、PR readiness 文案要求检查 commit message 合同。
- [ ] canonical source 与 dogfood installed copy 无漂移。
- [ ] PR body 继续使用 `Closes #92`，commit message 只使用 `Refs #92`。
- [ ] 最终报告列出开箱即用验证与 upgrade/update 验证覆盖项和未覆盖项。

## 不纳入范围

- 不修改 Trellis 上游 npm 包、`node_modules` 或全局安装目录。
- 不把需要 AI 判断的 review 充分性下沉到 Python 或 shell。
- 不自动执行 GitHub PR merge。
- 不改写历史已合入 commit。

## 开放问题

无阻塞开放问题。当前 issue 已给出完整提交规范、入口覆盖面和验收标准。
