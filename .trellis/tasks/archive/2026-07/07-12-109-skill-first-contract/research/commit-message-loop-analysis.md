# Bug Analysis: Commit subject/body 在提交后才被发现不合规

## 1. Root Cause Category

- **Category**: B - Cross-Layer Contract
- **Specific Cause**: #92 已定义完整中文 Conventional Commits 合同，`check-commit-messages` 也能校验已经存在于 Git history 的 commit，但提交前的 exact staging set、subject 和 body 没有一个 closed-loop owner。Workflow 要求 Phase 2 检查 planned message，实际 planning artifact 不绑定 exact payload；主会话在 Phase 2 后临时生成 commit plan；deterministic validator 只能在 commit 创建后读取 `origin/main..HEAD`。因此错误输入在副作用前没有进入同一个 AI review + human confirmation + validator 合同。

## 2. Why Fixes Failed

1. **#92 文档与 postcondition validator**: 能说明规则并阻止不合规历史继续发布，但不能校验尚不存在的 commit payload，属于不完整的 precondition enforcement。
2. **Phase 2 文案检查**: 规定检查 planned subject/body，却没有 current exact payload、digest 或 schema 作为输入，AI check 无法绑定后来由主会话临时生成的文本。
3. **用户确认 commit plan**: 确认发生在 deterministic validation 之前；human confirmation 证明用户同意 payload，不证明 payload 符合机器合同。
4. **本次提交**: 主会话沿用通用英文 Conventional Commit 习惯，没有在提交前重新读取仓库特有的中文 issue-bearing body 合同；错误直到 post-commit `check-commit-messages` 才暴露。

## 3. Prevention Mechanisms

| Priority | Mechanism | Specific Action | Status |
| --- | --- | --- | --- |
| P0 | Architecture | 建立 `guru-create-work-commit` closed-loop skill，成为工作提交的行为 SSOT。 | Proposed |
| P0 | Deterministic precondition | 扩展 validator，使其能在 commit 前校验 exact subject/body payload，而不只读取 Git history。 | Proposed |
| P0 | Human confirmation binding | 用户确认必须绑定 staging paths、subject、body digest 和验证摘要；payload 变化必须重新确认。 | Proposed |
| P1 | Postcondition | Commit 创建后继续运行现有 `check-commit-messages`，验证实际 commit bytes 与已确认 payload 一致。 | Existing |
| P1 | Test coverage | 覆盖 invalid plan -> revision -> confirm -> validate -> commit -> postcheck，以及 payload drift/re-entry。 | Proposed |

## 4. Proposed Closed-Loop Skill

推荐 stable id：

```text
guru-create-work-commit
```

该名称表达最终用户结果，不使用含义模糊的 `gate`、`helper` 或 `utils`。完整闭环：

1. 验证 task、workspace、Phase 2、issue ledger、Docs SSOT 和 dirty paths。
2. AI 生成 exact staging set、中文 subject/body 和 boundary/validation 论证。
3. AI Review Gate 检查真实性、scope、`Refs`/`Closes` 分工和无关文件排除。
4. 展示 exact payload/digest并取得 human confirmation。
5. Deterministic validator 在副作用前校验 subject/body schema、section order、issue id、footer 和 staged paths。
6. Executor 只 stage confirmed paths并创建 commit。
7. Postcondition validator 校验 actual commit hash、tree、subject/body 与 confirmed payload。
8. 返回一个 stable typed exit。

建议 external exits：

- `committed`：actual commit 与 confirmed payload/current task 完整绑定；consumer 是 Branch Review Gate。
- `revision_required`：AI 或 validator 发现 subject/body/staging 问题；consumer 是本 skill 的 revision loop。
- `blocked`：workspace、Phase 2、scope、Git 或用户确认无法满足；consumer 是 stop 或明确 prerequisite owner。

Workflow mode 与 standalone mode 必须使用相同 AI Gate、human confirmation、validator 和 executor boundary。

## 5. Script Boundary

Script 可以：

- 校验 subject/body 固定格式、section order、issue id 和 footer；
- 计算 payload digest；
- 校验 staged path set、HEAD 和 task binding；
- 按已确认输入执行 `git add` / `git commit`；
- 校验 actual commit bytes/tree/message。

Script 不得：

- 决定提交范围或排除哪些用户改动；
- 编写或判断背景、变更、边界、验证论证是否真实充分；
- 决定 issue close/ref/followup；
- 用模板默认值冒充 AI review 或 human confirmation。

## 6. Systematic Expansion

- **Similar Issues**: PR body、merge payload、closeout plan 均存在“AI 内容判断 + exact payload + human confirmation + deterministic executor”边界，必须检查是否同样只有 postcondition validator。
- **Design Improvement**: 所有有副作用的 AI-authored payload 都应先形成 immutable/digest-bound preview，再确认、校验、执行、复验。
- **Process Improvement**: Workflow 不得只写“AI 检查 planned payload”；必须存在可定位的 current payload owner 和 freshness binding。

## 7. Knowledge Capture Decision

- 当前 #109 的用户确认业务范围只有根 `AGENTS.md`，不得借 break-loop 扩改 `.trellis/spec/`、workflow、script 或 tests。
- #120 将先建立通用 closed-loop skill 合同与 Canonical 分发基础设施。
- `guru-create-work-commit` 必须作为 #120 之后的独立具体 skill issue 实施，不塞入 #120 的通用基础设施范围，也不回退重开 #92。
- 本文件只作为 #109 task history evidence；创建新 GitHub issue 仍需用户确认 exact title/body。

