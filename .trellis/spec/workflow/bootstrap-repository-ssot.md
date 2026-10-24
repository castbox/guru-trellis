# Bootstrap Repository SSOT

`guru-bootstrap-repository-ssot` 是仓库级一次性基线编排 Skill。它支持
`new_repository`、`existing_repository`、`repair` 三个入口，先调用官方
`trellis-spec-bootstrap`，再调用 #263 Requirements/Design/Test SSOT 与 #264
Architecture Baseline。两个子 Skill 的内部正文和私有 checkpoint 不跨边界传递。

Bootstrap 自己只负责跨 SSOT 版本、适用范围、行为、设计、测试与架构约束对齐，
并把 canonical locator、version/status、traceability、读取/更新规则和 freshness
投影到 `.trellis/spec/`。该目录是 AI 使用投影，不是第三套业务正文 authority。

只有 `completed` 才能进入正常 task rollout 并 finish/archive exact bootstrap task；
`baseline_incomplete`、`repair_required` 和 `blocked` 保留诚实状态并 fail closed。Preset
安装、upgrade、update、workflow switch 和 reapply 只报告状态，不自动运行 Bootstrap。

后续 task 通过 #263/#264 的 task-impact/promotion contracts 更新 canonical authority；
普通并行 task 不直接修改 shared spec index。完整多平台安装矩阵和 upgrade/release
证据分别由 #260/#267 负责。

`repair_required` 的同 owner re-entry 由原 package 的 Interface 和 contract 定义。
Caller 使用其声明 rename/authoring，保留原调用上下文后执行实际 repair；不得读取
producer 私有结果。当前分发及旧输入重入边界见 preset `MIGRATION-663.md`。
