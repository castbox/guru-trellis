# #304 修正 Release owner 文案

## Goal

修正三处 stale Release owner 文案，使公开 README 与 #304 current contract 及
active `.40` Requirements authority 一致，不再把重构前稳定版发布归属到 #267。

## Background

- #304 是 `v0.6.15-guru.1` 重构前稳定版 Release 的 current semantic owner。
- `docs/requirements/README.md` 已声明该发布由独立的重构前稳定版 Release Issue
  晋升，#267 与下一阶段重构链不属于该发布的 owner 或前置。
- `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md` 仍保留 #267 负责或独占 `.37` tag、
  GitHub Release、tag-pinned install 与 release smoke 的旧文案。
- #304 authority amendment 将原 candidate `0169f8c5...` 标记为 stale，并把本任务
  固定为三处文案修正。

## Requirements

1. `README.md:34` 将发布 owner 改为独立的重构前稳定版 Release Issue（#304）。
2. `trellis/workflows/guru-team/README.md:53` 使用同一 owner 语义。
3. `trellis/presets/guru-team/README.md:160` 使用同一 owner 语义。
4. 保留 extension `0.6.5-guru.37`、Trellis `0.6.15`、candidate evidence、
   stable-source 状态和安装命令的既有内容。
5. 不修改 workflow 行为、Skill API/schema、安装文件清单、candidate 功能代码、
   active RDT/Architecture authority 或其它文档。

## Acceptance Criteria

- AC-1：三个固定位置均明确由独立的重构前稳定版 Release Issue（#304）拥有
  `.37` tag、GitHub Release、tag-pinned install 与 release smoke。
- AC-2：三个文件不再把上述发布职责归属到 #267。
- AC-3：`git diff --check` 通过，diff 仅包含三个目标句子和 task 规划文件。
- AC-4：定向文本检查通过；无需运行安装矩阵或功能测试，因为本任务不改变
  workflow、runtime、schema、installer 或 manifest。
- AC-5：合并前不声称 Release candidate 已重新冻结；重新冻结和完整 Release gates
  由 #304 在本修正合并后 fresh 执行。

## Out Of Scope

- 不修改、关闭或评论 #267。
- 不改动 `docs/requirements/**`、`docs/design/**`、`docs/test/**` 或
  `docs/architecture/**`。
- 不执行 commit、push、PR、merge、tag、GitHub Release、Issue 关闭或资源清理。

