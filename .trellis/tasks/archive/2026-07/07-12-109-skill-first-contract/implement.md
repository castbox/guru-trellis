# #109 实现计划

## 1. 规划门禁

- [ ] 主会话完成三份 planning artifact 的 ambiguity review。
- [ ] 运行 fixed-scope controlled wording scanner并分类全部命中。
- [ ] 向用户展示更新后的 `prd.md`、`design.md`、`implement.md`，取得 `explicit-post-planning-review` 确认。
- [ ] 记录并验证 `planning-approval.json`，启动 task。
- [ ] 运行 `trellis-before-dev` 并确认适用 spec。

## 2. 单文件实现

- [ ] Trellis implement sub-agent 读取 planning artifact、根 `AGENTS.md` 和适用 workflow/docs spec。
- [ ] 仅在根 `AGENTS.md` 增加 Skill-first 闭环流程模块化章节。
- [ ] 保持现有章节职责，必要的章节编号机械顺延不得改写其它正文语义。
- [ ] 新章节覆盖 SSOT 分层、mandatory invocation、closed loop、workflow/standalone mode、typed exits、强制/禁止拆分、stable API 和 package state。
- [ ] 不修改 workflow、preset、overlay、skill、script、schema、README、requirements/spec 或 tests。

## 3. 检查与修复

- [ ] Trellis check sub-agent 审核新增规则是否完整、确定、无重复 SSOT、无 script 越界。
- [ ] 确认业务 diff 只有 `AGENTS.md`。
- [ ] 运行受控措辞扫描并处理未分类命中。
- [ ] 运行：

```bash
git diff --check
git diff -- AGENTS.md
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-12-109-skill-first-contract
```

- [ ] 记录并验证 `phase2-check.json`。

## 4. Review 与发布

- [ ] 主会话决定 `.trellis/spec/` 不需要更新，并记录具体理由。
- [ ] 只 stage `AGENTS.md` 与本 task 的必要 gate/archive artifacts，不包含无关文件。
- [ ] 使用 Conventional Commit 提交。
- [ ] 独立 reviewer 覆盖完整 `origin/main...HEAD` diff，处理所有阻塞 finding。
- [ ] PR readiness 前重读 #109 与 #120，确认当前 PR 只关闭 #109，#120 保持 open。
- [ ] PR title/body 使用中文，准确列出只修改 `AGENTS.md`、验证结果、安全说明和无 runtime/deploy 影响。

## 5. 回滚

回滚仅删除 `AGENTS.md` 新增章节并恢复章节编号。由于不修改 runtime、installer、schema 或生成副本，不存在数据迁移与安装回滚。
