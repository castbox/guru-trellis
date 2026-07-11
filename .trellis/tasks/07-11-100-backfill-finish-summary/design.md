# Issue #100 技术设计

## 1. 设计原则

1. #97 schema/validator 继续作为唯一结构 SSOT；backfill 只负责确定性抽取和写入。
2. Bash 只做入口转发，Python 负责 scanner、validator、executor 和 recorder。
3. 单 task 失败不阻断批次，但命令必须以非零退出码暴露不完整批次。
4. 不读取 workspace/runtime，不访问 GitHub，不调用 `trellis mem`，不从自然语言编造事实。
5. 正常 finish-work 与 backfill 共用 validator，不共享自然语言生成路径。

## 2. 组件与变更边界

| 组件 | 变更 | 边界 |
| --- | --- | --- |
| `guru_team_trellis.py` | 增加 `backfill-finish-summary` parser、路径校验、扫描、抽取、构建、输出和退出码 | 不改变 `build_finish_summary()` 与 `cmd_finish_work()` 正常路径 |
| `backfill-finish-summary.sh` | 转发全部参数到 canonical Python subcommand | 不包含判断或抽取逻辑 |
| `test_guru_team_trellis.py` | 覆盖 CLI、抽取、错误隔离、schema 和安全边界 | fixture 不读取真实 workspace/GitHub |
| preset installer | 把新 wrapper 加入 `MANAGED_ASSET_PATHS` 和 executable 处理 | 不修改用户自有配置 |
| extension manifest | 把 `backfill-finish-summary` 加入 public companion list | 不创建 release tag，不改变 workflow/template id |
| durable docs | 描述一次性迁移命令、数据来源和 #98 依赖 | 不把 active task 状态写入 marketplace template |
| archived task | 生成缺失的 task-local `finish-summary.json` | 不生成全局 index，不改其它历史 artifact |

## 3. CLI 合同

Canonical parser 增加 `backfill-finish-summary`：

```text
--root <repo>
--json
--dry-run | --write
--force
--task <repo-relative archived task dir>
```

- 参数组合或 `--task` 路径非法时，在扫描前退出 2。
- dry-run 与 write 使用同一 discovery/build/validate pipeline；dry-run 省略最后的 atomic write。
- 批次完成且 `errors=[]` 时退出 0；存在任一 per-task error 时完成其它 task 后退出 1；JSON 与表格模式一致。
- JSON object 固定包含 `mode`、`archive_glob`、`scanned_tasks`、`to_write`、`skipped`、`errors`。
- 非 JSON 模式按上述字段渲染稳定表格和错误段，不改变 payload 决策。

## 4. 扫描与路径安全

### 4.1 无 `--task` 扫描

- root 必须是 Git repository 且包含 `.trellis/tasks/archive/`。
- 递归扫描 archive root 下包含白名单 artifact 或现有 `finish-summary.json` 的 task 目录，并在识别 task 根后排除其 `research/` 和 `reviews/` 子目录。
- 空 archive 返回 `scanned_tasks=0`。只有目录 basename 的 minimal fixture 通过显式 `--task` 处理，避免把 archive 分组目录误识别为 task。

### 4.2 指定 task

- 原始参数必须是相对路径且不含空、`.`、`..` segment 或反斜杠。
- resolve 后必须严格位于 archive root 下；archive root 本身和 active `.trellis/tasks/<task>` 均为无效目标。
- symlink escape、绝对路径、repo 外路径全部在读文件前退出 2。

## 5. Artifact 读取模型

白名单固定为 issue #100 的 10 个文件。读取结果分三类：

- `present_valid`：文件存在且 JSON 可解析或 Markdown 可读取，进入 `source_artifacts`。
- `missing`：文件不存在，不记 error；由字段生成规则决定是否进入 `missing_fields`。
- `invalid`：JSON 损坏或文本无法按 UTF-8 读取，记录 task/path/error，排除该 artifact，继续使用其它来源。

所有 JSON 字段先验证预期类型再读取。Markdown helper 只支持固定标题、第一段、列表、完成 checklist 和第一张表格，不做模型推断。

## 6. Payload 构建

### 6.1 Task、Git、GitHub 和 artifacts

- 严格按 issue #100 列出的来源优先级取值；缺失值使用 schema 定义的空字符串或空数组。
- `task.artifact_dir` 只有 artifact 明确给出可验证 repo-relative 原路径时才填写，否则为空并记录 missing field。
- commits、changed paths、issue arrays 和 PR URL 必须通过类型、SHA/number/URL/path validator；非法候选按损坏来源处理，不透传。
- `artifacts` 只记录实际存在且成功读取的白名单文件，value 为 task-relative basename。

### 6.2 文本字段

- problem/outcome 只读取固定标题后的第一段或固定 fallback。
- changed behavior 只读取固定章节列表或完成 checklist，规范为 1 到 12 条。
- 文本统一 trim、折叠空白，并按 #97 各字段最大长度做确定性尾部截断；禁止文本命中时该 task 校验失败，不做替换掩盖。

### 6.3 affected surfaces

- 先对完整 `git.changed_paths` 去重排序，再按 issue 的 path-prefix 映射到 `kind`。
- 每个 kind 的 paths 保持完整排序；超过 schema 单 surface 100-path 上限时分成稳定的 100 条批次。
- name 使用 kind 与批次号，change 使用固定中文句式；若总 surface 超过 schema 的 20 条，不截断，记录 error 并跳过写入。
- changed paths 为空时生成 issue 指定的单个 `task-artifact` fallback surface。

### 6.4 contract changes 与 search terms

- contract changes 只读取 `design.md` 固定标题下第一张、列名完全匹配的 Markdown 表格；不满足时为 `[]`。
- issue/pr/branch/path search terms 只从结构化字段派生。
- commands/config/schema/symbol 使用固定 regex、固定输入集合、排序去重和 schema 上限；phrases 按 issue 顺序截取到 60 字、去重并限制 40 条，少于 3 条时使用固定 fallback 补足。
- retrieval text 只调用现有 `finish_summary_retrieval_text()`。

### 6.5 missing fields 与 confidence

- missing fields 使用 canonical dotted field name，排序去重。
- `complete`：结构化核心 artifact 齐备，changed paths、source issues、PR URL 和所有核心 index 字段非空。
- `partial`：核心 index 字段可生成，但 changed paths、source issues 或 PR URL 中任一字段缺失。
- `minimal`：只能依赖目录 basename、task title/name 或 Markdown 标题形成基础检索字段。

## 7. 写入与重复执行一致性

- payload 在写盘前通过 `finish_summary_errors(payload, task_dir=task_dir)`。
- write 使用同目录临时文件、flush 后 `os.replace()`，避免留下半写 JSON。
- 已存在目标在未提供 force 时进入 skipped；提供 force 时仍先完整重建和校验，再 atomic replace。
- write 后重新 read/validate；失败记录 error，临时文件必须清理。
- 首次 write 后再次 dry-run 应只返回 skipped，不生成第二份索引或变更已有文件。

## 8. Docs SSOT Plan

- docs state：`complete_docs`。
- evidence：canonical/dogfood workflow、两份 README、`companion-scripts.md`、`data-contracts.md`、`preset/installer.md`、#97 schema/tests。
- strategy：`ssot_first`，因为新增 user-facing public companion command 和一次性 migration 合同。
- durable docs：先更新 `.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md` 和 `.trellis/spec/preset/installer.md`，再更新 canonical workflow/README/preset README，最后 apply 同步 dogfood。
- task deltas：聚合规则、错误退出码、历史 write 结果和验证证据只在 task artifact 记录；可复用合同必须合并到上述 durable docs。
- merge checkpoint：代码完成前检查 durable docs 已包含最终 CLI 与聚合规则；Phase 2 check 前验证 canonical/dogfood 一致。

## 9. 安装、升级与回滚

- preset installer 显式复制并 chmod 新 wrapper；throwaway install 后执行 `--json --dry-run`。
- 执行 workflow preview/switch、`trellis update` 兼容性检查，再 reapply preset，确认 wrapper 和 parser 仍存在且可执行。
- apply 后运行 overlay drift，并递归检查 `.new` / `.bak`。
- 回滚代码时删除 wrapper/parser/installer list/docs；历史 `finish-summary.json` 是 schema-valid task-local 数据，可通过专门 revert commit 删除，不由脚本自动回滚。

## 10. 安全与兼容性

- 不输出 artifact 原文、secret、token、环境变量或 GitHub auth 信息。
- error 只包含 repo-relative task/artifact path 和解析原因，不包含文件内容。
- 不改变正常 finish/publish、#98 消费格式、官方 Trellis 或 workspace ignore 策略。
