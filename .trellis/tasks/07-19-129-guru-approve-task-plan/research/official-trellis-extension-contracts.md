# 官方 Trellis 扩展合同核对

核对日期：2026-07-19

## 来源

- https://docs.trytrellis.app/advanced/custom-workflow.md
- https://docs.trytrellis.app/advanced/custom-skills.md
- https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md
- https://docs.trytrellis.app/advanced/architecture.md

## 本任务采用的结论

1. `.trellis/workflow.md` 是运行时读取的流程合同，负责 phase、skill routing、workflow-state 与 task lifecycle 路由；流程变更不通过修改 Trellis 上游源码、全局 npm 包、`node_modules` 或 hook fallback 落地。
2. Skill 是跨平台复用的流程模块。一个 Skill 使用独立目录和 `SKILL.md`，补充 references、schemas、examples、scripts 与 tests 后，仍由平台 discovery root 加载。
3. Codex 同时使用 `.codex/skills/<name>/` 与 `.agents/skills/<name>/` discovery surface；Guru preset 还声明 Claude 与 Cursor，因此 canonical package 必须分发到 shared、Codex、Claude、Cursor 四类目标。
4. `prd.md`、`design.md`、`implement.md`、research 与 JSONL manifest 属于 task knowledge；长期工程合同进入 `.trellis/spec/`、durable docs、canonical workflow 或 canonical Skill package。
5. Spec template marketplace 只承载复用工程规范，不承载 active task、项目私有运行状态或平台 prompt。本任务不会把 `guru-approve-task-plan` 的 active evidence 写入 spec template marketplace。
6. Trellis 生成文件保留本地修改和 template hash 语义；Guru package 必须通过 preset additive distribution、clean throwaway install、`trellis update` 后 reapply 与 sidecar 检查证明升级后可恢复。

## 边界

- 本文件只记录官方扩展面与本任务采用的架构依据，不替代 Issue #129、三份 planning artifact 或 canonical Skill contract。
- 本任务不修改 Trellis upstream Skill、Agent、Command、Prompt、Hook、runtime agent、全局安装目录或 `node_modules`。
