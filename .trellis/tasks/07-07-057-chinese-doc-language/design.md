# #57 设计：统一业务项目文档语言规则

## 设计目标

业务项目侧形成一个可安装、可更新、可验证的中文文档默认规则，且不破坏 `guru-trellis` 自身作为公共扩展仓库维护英文/双语说明的自由度。

## 技术方案

### 1. Workflow 规则扩展

在 canonical `trellis/workflows/guru-team/workflow.md` 中把当前“task planning artifacts 和 review fields 中文”扩展为“业务项目人类可读文档默认中文”。范围显式包含：

- `.trellis/spec/**`
- `.trellis/tasks/**`
- `docs/**` durable docs
- `00-bootstrap-guidelines` 产生或补齐 docs SSOT 的文档
- workflow / helper 写入 artifact 的 human-readable 字段

同步 dogfood `.trellis/workflow.md`，并同步 start/continue overlay 中与 planning / Docs SSOT / spec bootstrap 相关的短入口文案。

### 2. Preset installer 语言归一化

在 `apply_guru_team_trellis_preset.py` 中新增确定性 post-install 归一化函数，只处理 `ENGLISH_LANGUAGE_RULES` 中列出的已知 Trellis 生成英文语言规则句子。

目标文件范围限制在业务项目的 `.trellis/spec/**/*.md`、`.trellis/workspace/index.md` / `.trellis/workspace/*/index.md` 和 `.trellis/tasks/00-bootstrap-guidelines/**/*.md`。替换为中文规则句，不扫描或修改普通历史 task、未知 task 内容或业务 `docs/**` 内容，避免把 installer 变成 docs 重写器。`docs/**` 的中文要求由 workflow / bootstrap prompt / AI 执行规则承载。

该脚本行为是 Executor/Validator 允许的确定性动作：输入是固定路径和固定字符串，输出是固定替换结果；脚本不判断某个文档是否应该中文，也不重写未知内容。

### 3. Bootstrap / docs SSOT 文案

`00-bootstrap-guidelines` 不由 Guru Team preset 静默完成；但 workflow、README 和 spec bootstrap 相关文案必须告诉 AI：当用户确认执行 bootstrap 或需要创建 docs SSOT 时，生成的人类可读规范和 docs 主文档应使用中文。公共工具仓库例外边界仍保留。

### 4. Durable docs / spec 同步

更新本仓库长期说明：

- `docs/requirements/requirement-main.md` 和 `docs/requirements/README.md` 增加 issue #57 语言规则能力。
- `trellis/workflows/guru-team/README.md` 和 `trellis/presets/guru-team/README.md` 说明安装/更新后的中文归一化和例外边界。
- `.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/docs/public-docs.md` 记录可执行合同和验证要求。

## 数据与兼容性

- 不新增配置字段，避免已有 `.trellis/guru-team/config.yml` 迁移风险。
- installer payload 可新增 `language_guidance` 结果块，记录 `action`、`path` 和替换数量，作为确定性安装证据。旧调用方忽略未知字段即可。
- 只替换精确匹配的英文语言规则行；用户自定义文本不会被语义重写。
- 如果目标文件不存在，跳过并记录空结果。

## 测试策略

- installer 单测覆盖：
  - `.trellis/spec/backend/index.md` 中的英文规则被替换为中文；
  - `.trellis/workspace/index.md` 中的英文规则被替换为中文；
  - 不含目标句的文件保持不变；
  - install payload 暴露 language guidance 结果。
- throwaway install 验证新增 grep：
  - `.trellis/spec/**` 不包含 `All documentation ... English`；
  - `.trellis/workspace/index.md` 不包含英文强制语言规则；
  - 如生成 `00-bootstrap-guidelines`，其 `prd.md` / 相关提示不要求英文。
- 常规验证：脚本语法、Python 编译、相关单测、task validate、dogfood overlay drift、diff check。

## 风险与边界

- 如果官方 Trellis 后续更改模板句子，本次精确替换可能漏掉新措辞；验证脚本中的 grep 会暴露风险，后续可扩展已知短语表。
- 如果 tag-pinned marketplace 无法访问当前分支，throwaway install 只能验证 public release 或本地 installer，最终报告必须说明未覆盖当前分支 marketplace 安装。
- 业务项目 `docs/**` 已有英文内容不由 installer 重写；本任务只定义后续生成/维护规则，避免破坏用户文档。
