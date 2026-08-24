# Implementation Plan

## Steps

1. 在 `README.md` 替换 stale #267 Release owner 句子。
2. 在 `trellis/workflows/guru-team/README.md` 应用同一中文 owner 语义。
3. 在 `trellis/presets/guru-team/README.md` 应用等价英文 owner 语义。
4. 检查完整 diff，确认三个产品文件各只有一个句子变化。
5. 运行定向文本检查和 `git diff --check`。
6. 完成 Phase 2 后，单独展示 task commit 副作用计划；commit 完成后执行
   committed full-diff Branch Review，再单独展示 push 和 PR 副作用计划。

## Validation Commands

```bash
rg -n '独立的重构前稳定版 Release Issue（#304）' \
  README.md trellis/workflows/guru-team/README.md
rg -n 'independent pre-refactor stable Release Issue \(#304\)' \
  trellis/presets/guru-team/README.md
git diff --check
git diff -- README.md \
  trellis/workflows/guru-team/README.md \
  trellis/presets/guru-team/README.md
```

## Risk Controls

- 目标路径固定为三个 README，不运行 overlay reapply，避免产生无关 projection
  变更。
- 不修改 active Requirements 正文；实现只让公开 projection 承接既有 authority。
- 不把规划或静态文本检查表述为重新冻结、安装验证或 Release gate 通过。
- commit、push、PR、merge 与发布均保留独立确认边界。
