# Issue #100 实施计划

## 1. 前置门禁

- [ ] 主会话完成 `prd.md`、`design.md`、`implement.md` 歧义审核并展示链接。
- [ ] 用户给出独立 post-planning approval；随后记录并校验 schema 1.2 `planning-approval.json`。
- [ ] `implement.jsonl` 与 `check.jsonl` 均包含真实 spec 条目。
- [ ] `task.py start` 后再进入 Phase 2。

## 2. Docs SSOT 先行

- [ ] 在 `.trellis/spec/workflow/companion-scripts.md` 固化 CLI、退出码、错误隔离和一次性迁移边界。
- [ ] 在 `.trellis/spec/workflow/data-contracts.md` 固化 backfill 来源、confidence、按 kind 聚合和 #97 schema 关系。
- [ ] 在 `.trellis/spec/preset/installer.md` 固化新 managed executable asset。
- [ ] 更新 canonical workflow、workflow README 和 preset README；不复制 active task 内容。

## 3. Canonical 实现

- [ ] 在 `guru_team_trellis.py` 增加 archive task 路径校验与 deterministic discovery。
- [ ] 增加白名单 artifact loader、JSON/Markdown 固定抽取 helpers 和 per-task error collector。
- [ ] 增加 task/git/github/artifacts/index/backfill payload builder，复用 #97 validator/retrieval helper。
- [ ] 实现按 kind 聚合 surface、100-path 分批和 20-surface fail-closed。
- [ ] 实现 dry-run/write/force/task 模式、atomic write、JSON/表格 renderer 和 0/1/2 退出码。
- [ ] 在 parser/main 注册 `backfill-finish-summary`，不改变其它 command 输出。
- [ ] 新增 canonical bash wrapper并设置 executable bit。

## 4. Preset 与 public API

- [ ] installer `MANAGED_ASSET_PATHS` 加入 wrapper，preset tests 覆盖复制和 executable。
- [ ] extension manifest `public_api.companion_scripts` 加入命令；保持尚未发布的 `0.6.5-guru.3`，不创建 tag。
- [ ] 运行 `apply.sh --repo . --all-platforms` 同步 `.trellis/guru-team/**`。
- [ ] 处理所有 `.new` / `.bak`，运行 overlay drift 检查。

## 5. 测试实现

- [ ] 参数：互斥缺失/冲突、force 无 write、非法 task 路径、active/repo 外/symlink escape。
- [ ] 扫描：空 archive、未提供 `--task` 的多 task、指定 task、已有 summary skip、force 覆盖。
- [ ] 数据：complete、缺 PR/issue partial、basename minimal、损坏 JSON 后批次继续。
- [ ] index：problem/outcome/behavior、kind 聚合、100-path 分批、20-surface fail-closed、contract table、search terms、retrieval text。
- [ ] 安全：绝对/parent/workspace/runtime path、禁止旧式顶层 `summary`/`keywords`、禁止内容。
- [ ] CLI：JSON 与表格输出一致，per-task errors 退出 1，参数错误退出 2。

## 6. Dogfood 一次性迁移

- [ ] 先运行 `backfill-finish-summary.sh --json --dry-run`，保存候选/skip/error 数量。
- [ ] 确认所有候选可生成 schema-valid payload 后运行 `--json --write`。
- [ ] 对全部新增 `finish-summary.json` 逐个执行 Python validator。
- [ ] 再次 dry-run，确认 45 个 archived task 均为已有文件 skip，且 `errors=[]`。

## 7. 验证命令

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-11-100-backfill-finish-summary
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

- [ ] 使用 throwaway repo 运行 preset apply，并执行 installed wrapper dry-run。
- [ ] 执行 workflow preview/switch、update 兼容性验证、preset reapply 与 `.new/.bak` 空扫描。
- [ ] 记录所有命令、退出码和未验证风险。

## 8. Phase 2 Check 与提交

- [ ] 委派独立 `trellis-check` 子代理覆盖需求、设计、代码、测试、spec、Docs SSOT、安装升级和安全。
- [ ] 主会话修复所有 P0/P1/P2/P3 finding；每轮修复后由同一 checker 复核闭环。
- [ ] 记录并校验 `phase2-check.json`，更新 issue acceptance evidence。
- [ ] 只 stage #100 范围文件，提交信息符合 Conventional Commits 与 issue 关联规则。

## 9. Branch Review Finding 闭环

- [ ] F-001：让 explicit resolver 与 discovery 共用 task-root marker/ancestor 判定；补 task root、task 子目录、archive 分组目录、symlink escape、write/force 回归。
- [ ] F-002：恢复 issue 固定 problem/outcome fallback；phrases 先执行 issue 固定顺序和少于 3 条补足，仅在无 #97 completion marker 时追加 `历史归档 task 已完成`。
- [ ] F-002：在 final validator 增加严格 backfill-only、精确 problem fallback 的 task title / problem 边界重复例外；不得修改通用 helper、schema 或 normal finish-work 行为。
- [ ] 删除 durable spec 中未获批准的 phrase 规则，写入 GitHub comment `4941670415` 确认的唯一 completion fallback。
- [ ] 将 GitHub comment `4941812435` 的 retrieval 冲突口径同步到 durable data contract；补 4 个真实冲突 fixture、normal finish-work、非精确 fallback 和其它重复继续失败的回归。
- [ ] Phase 2 P2：按 GitHub comment `4942002004` 支持 pr-body-only 第一列表项 outcome，并增加严格 backfill-only outcome / behavior 单一边界例外；保留完整 `changed_behavior`。
- [ ] 补 paragraph 与更高来源优先、来源标记、首项匹配、deterministic derivation、派生篡改、其它重复和 normal finish-work 的正负回归。
- [ ] F-003：人类 preview 为每个 `to_write` 项显示 `source_artifacts`、`missing_fields`、`confidence`，并补 JSON/table parity 回归。
- [ ] 用最终 builder 重建 44 个 backfill summary，验证 #97 正常 summary 未变、45/45 schema、44/44 deterministic rebuild 与写后 45 skip/0 error。
- [ ] 重新派发 Phase 2 check、记录新的 `phase2-check.json`、提交修复；同一 finding owner 以 `问题闭环审查代理` 复核 3 个 finding 后，再派发 fresh `最终放行审查代理`。

## 10. Branch Review Gate 与发布

- [ ] 独立 reviewer 覆盖 `origin/main...HEAD` 完整 diff；记录 raw reports、agent ledger、review rollup 和 gate。
- [ ] public extension 改动触发 remote marketplace verification；ledger 中 pending 证据必须被真实 passed artifact 替换。
- [ ] 完成 PR readiness，标题/正文使用中文，`Closes #100`，其它 issue 只用 Refs/Follow-up。
- [ ] 执行 finish-work dry-run、正式 archive/publish 和 PR URL summary tail。

## 11. 回滚点

- 代码/安装回滚点：删除新 parser、wrapper、managed asset 和对应 docs/tests。
- 数据回滚点：历史 summary 独立集中在 `.trellis/tasks/archive/**/finish-summary.json`，通过专门 revert commit 删除；不得运行脚本批量删除未知现有 summary。
