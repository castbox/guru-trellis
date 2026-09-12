# Journal - wumengye (Part 1)

> AI development session journal
> Started: 2026-09-01

---



## Session 1: 修复 Finalizer provenance reprepare 并完成 #325

**Date**: 2026-09-01
**Task**: 修复 Finalizer provenance reprepare 并完成 #325
**Branch**: `main`

### Summary

修复 Finalizer provenance reprepare 调用完整 preset apply 重写 extension.json installed_at 的问题；改为最小 provenance tail，保留 manifest inventory；完成 69 项 Finalizer 测试、81 项 installer 回归测试、Branch Review、PR #326 合并与 Issue #325 关闭。

### Git Commits

| Hash | Message |
|------|---------|
| `45c89eb27c4d074f05097934eac0e0741d6f5188` | (see git log) |
| `a448d94ac85198c514e2e41ab3ab0f3401ca23a9` | (see git log) |

### Status

[OK] **Completed**


## Session 45: Issue #400 workspace identity 修复收尾
<!-- trellis-session: v=2 fp=62b5cf301070060d -->

**Date**: 2026-09-12
**Task**: Issue #400 workspace identity 修复收尾
**Branch**: `codex/400-create-task-workspace-identity`

### Summary

完成 Issue #400 workspace identity fail-closed 修复；补齐 canonical/dogfood/installed start-task wrapper、manifest provenance 回归测试与 clean source snapshot；Phase 2、ownership、dogfood drift、focused tests 和 fresh Branch Review 通过。完整 preset 测试仍有 2 个既有 canonical eval 文本断言失败，已明确记录为非本 Issue 阻塞边界。

### Git Commits

| Hash | Message |
|------|---------|
| `aa110594` | fix(trellis): #400 闭合启动前 workspace identity 校验 |
| `35bb6337` | fix(trellis): #400 补齐安装 workspace identity wrapper |
| `f6ae345d` | fix(trellis): #400 绑定 installed manifest 到当前提交 |
| `baf1e3cc` | chore(trellis): refresh installed manifest provenance |
| `9d3e8a27` | test(trellis): #400 pin install provenance semantics |
| `c32d7aea` | chore(trellis): refresh installed manifest after provenance test |
| `a6e87998` | chore(trellis): bind installed manifest to clean source snapshot |

### Status

[OK] **Completed**
