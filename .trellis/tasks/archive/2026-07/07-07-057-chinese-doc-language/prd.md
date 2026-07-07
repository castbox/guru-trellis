# #57 统一业务项目 Trellis 文档语言为中文

## 目标

统一 Guru Team Trellis 扩展在业务项目中的人类可读文档语言规则：除命令、路径、代码符号、GitHub keyword、配置键等 literal token 必须保留英文外，业务项目内由 Trellis / Guru Team 生成、维护或要求 AI 更新的文档默认使用中文。

## 需求来源

- GitHub Issue: https://github.com/castbox/guru-trellis/issues/57
- Issue body 明确指出业务项目 `.trellis/spec/**`、`.trellis/tasks/**`、`docs/**` durable docs、Guru Team workflow human-readable artifact 字段都应使用中文。
- Issue comment 补充：`00-bootstrap-guidelines` 在发现项目没有 docs SSOT 时生成的 SSOT 主文档也应是中文。
- 官方 Trellis 文档依据已记录在 `research/official-trellis-docs.md`。

## 范围

### 必须覆盖

- 新安装或更新 Guru Team preset 后，业务项目 `.trellis/spec/**` 不再保留“所有文档必须英文”这类模板要求。
- Guru Team workflow / skill / overlay / generated artifact 规则明确业务项目人类可读文档默认中文，覆盖：
  - `.trellis/spec/**` 项目级规范；
  - `.trellis/tasks/**` 中的 `prd.md`、`design.md`、`implement.md`、`review.md` 等任务工件；
  - 业务项目 `docs/**` durable docs；
  - workflow 写入 artifact 的 human-readable 字段；
  - `00-bootstrap-guidelines` 触发创建或补齐 docs SSOT 时的主文档。
- 如存在中英文冲突，业务项目侧以中文规则为准。
- 保留例外边界：`guru-trellis` 仓库自身公共 README、源码注释、脚本帮助、marketplace 元数据和必须英文的 literal token 可继续按维护需要使用英文或双语。

### 不做范围

- 不修改官方 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不把某个业务仓库的私有产品规则写入公共 workflow / preset / spec template。
- 不静默完成 `00-bootstrap-guidelines` spec bootstrap；本任务只修正其语言规则和安装/更新后的模板冲突。
- 不新增新的 workflow/template id；`guru-team` 公共 API 保持稳定。

## 验收标准

- [ ] `rg` 检查确认安装到业务项目或指导业务项目的 `.trellis/spec/**` / workspace / bootstrap 相关模板中不再出现要求文档必须英文的句子。
- [ ] preset installer 对已存在的 Trellis 生成英文语言规则执行确定性替换，并有单元测试覆盖。
- [ ] throwaway install 验证包含 `.trellis/spec/**` 和 `00-bootstrap-guidelines` / workspace 语言规则检查。
- [ ] canonical workflow、dogfood `.trellis/workflow.md`、preset overlay、README / workflow README / preset README、`.trellis/spec/**` 和 `docs/requirements/**` 同步记录业务项目中文规则与 `guru-trellis` 自身例外边界。
- [ ] 修改 overlay 后运行 `apply.sh --repo . --all-platforms` 和 `check-dogfood-overlay-drift.sh`，处理所有 `.new` / `.bak`。
- [ ] 完成脚本语法、Python 编译、相关单测、task validate、`git diff --check`。
- [ ] 如无法完成 tag-pinned throwaway install 或 upgrade/update 全量验证，最终报告必须列出未覆盖项和风险。

## Docs SSOT

本仓库存在 durable docs SSOT：

- `docs/requirements/requirement-main.md`
- `docs/requirements/README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/docs/public-docs.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `.trellis/spec/workflow/workflow-contract.md`

本任务会把长期规则回写到这些 durable docs / specs；task artifact 只保留本次执行证据。

## Middle-platform Knowledge Gate

本任务修改 Trellis workflow/preset/installer 和文档语言规则，不涉及 Guru Team middle-platform SDK / framework，因此中台知识检索不适用。
