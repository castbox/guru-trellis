# 技术设计

## 设计结论

采用单一 source authority、多个受控文档投影的直接修复：canonical `trellis/presets/guru-team/source/trellis-source.json` 继续拥有 Fork repository、commit、parents、tree、CI、CLI 与 package-manager 身份；三个 README 只同步 current commit/CI 文案，不新增中间 manifest、生成器或兼容层。

## 修改边界

### 文档投影

- `README.md`
  - 将正文中的 current source candidate 更新为 `43fffc...`。
  - 将发布身份表中的 current Fork commit 与 Nightly CI 更新为 canonical 值。
- `trellis/workflows/guru-team/README.md`
  - 更新安装来源和版本边界段落中的 current commit/CI。
- `trellis/presets/guru-team/README.md`
  - 更新 source record、版本边界和验证说明中的 current commit/CI。

仅替换当前身份声明。`db4ca1df...` 仍是 canonical ordered parent，不建立“旧 commit 必须全局消失”的错误约束。

### 定向测试

在 `test_fork_preparation.py` 增加一个测试，从 canonical source lock 读取 `commit` 与 `ci_run_id`，逐一读取三个 README，并验证：

1. current canonical commit 出现在每份文档；
2. current CI 出现在每份文档；
3. stale CI `34838784963` 不出现在任何一份文档。

测试不复制新 commit/CI 常量，因此 source lock 仍是唯一机器可读 authority。旧 CI 不再具有任何 current 或 parent 语义，作为明确的退出断言。

现有 stale-build fixture 在临时 Fork 产生新 commit 后，从该 commit 重新读取完整 SHA、ordered parents 与 tree，并写入 fixture-local lock。该修正只保持 fixture 的内部 Git identity 自洽，使 production validator 继续执行到原有 build-origin 校验；不修改或放宽 validator，也不改变 repository canonical source lock。

## 数据流与所有权

```text
canonical trellis-source.json
  -> README current source claims
  -> workflow README current source claims
  -> preset README current source claims
  -> focused test reads canonical values and verifies all projections
```

- source identity owner：canonical `trellis-source.json`。
- installed projection owner：preset installer 与 `.trellis/guru-team/trellis-source.json`。
- human-facing current claim owner：上述三个 README。
- release orchestration owner：Issue #410；本任务不接管。

## 兼容性与迁移

- 无公共 Skill/API/schema/config 变化。
- 无 installed managed asset 内容变化，因为 canonical source lock 不变。
- 无业务数据或运行时迁移。
- README 的当前身份纠正不会改变支持的 predecessor、平台或安装命令。

## Docs SSOT Plan

- `.trellis/spec/docs/public-docs.md` 已正确要求从 canonical source lock 读取身份并区分版本轴，本任务不修改。
- Architecture、Requirements、Design、Test current authority 已正确描述 #410 与 source-lock 边界，本任务不晋升新 authority。
- 任务完成后只有三个 release-facing README 与一项定向回归测试发生变化。

## 验证设计

- 文档映射：新增定向测试。
- stale build：修正 fixture-local commit/parents/tree identity 后保留原有拒绝断言。
- source projection：现有 preset source-lock test。
- root preparation：现有 fork preparation tests。
- 安装投影与 reapply：现有 preset apply 与 dogfood drift 命令。
- 交付完整性：`git diff --check`、residue scan、完整 committed diff Branch Review。

## 架构影响预判

候选不改变组件职责、公共接口、数据流、owner、runtime 或 extension mechanism；预期 Architecture Planning 结果为 `no_architecture_impact`。该预判不替代正式 Architecture owner 判断。
