# #304 修正 capability preservation 判定

## Goal

修正兼容性矩阵的 capability preservation 判定，使其只把可观察的
Skill/workflow 能力标记丢失视为 capability loss，避免把内部 API/schema
投影变化或安装文件清单变化误报为能力丢失。

## Background

- Issue #304 的 2026-08-24 authority amendment 明确：capability preservation
  以 Skill/workflow external exit、consumer、re-entry 与 stop markers 为准。
- `compare_capabilities()` 当前同时比较 `distribution`、`skill_api`、
  `workflow`、`task_data` 和 `docs_authority`，导致合法的安装资产或内部接口投影
  变化进入 `blocking_differences`。
- `distribution` 与 `skill_api` 仍由安装、package、projection 和 consistency
  validators 独立验证；本需求不削弱这些验证。

## Requirements

1. `compare_capabilities()` 不得因 `distribution` 差异判定 capability loss。
2. `compare_capabilities()` 不得因 `skill_api` 差异判定 capability loss。
3. `workflow` marker 差异仍必须进入 `blocking_differences`。
4. `extension_identity`、`task_data` 和 `docs_authority` 的现有比较语义保持不变。
5. 测试必须分别覆盖安装文件清单变化、Skill API/schema 投影变化和 workflow
   marker 丢失，防止边界再次混淆。

## Acceptance Criteria

- AC-1：删除 `distribution.skill_package_files_and_modes` 中一个条目后，结果为
  `capabilities_preserved=true` 且 `blocking_differences=[]`。
- AC-2：清空 `skill_api.typed_output_schema_ids` 后，结果为
  `capabilities_preserved=true` 且 `blocking_differences=[]`。
- AC-3：删除一个 workflow capability marker 后，结果为
  `capabilities_preserved=false`，并报告 `group=workflow`。
- AC-4：升级合同测试、Python 编译检查和 `git diff --check` 全部通过。
- AC-5：dogfood overlay drift 与 upstream ownership 定向验证继续通过。
- AC-6：代表性本地兼容性矩阵通过；未发布分支的结果必须保留
  `unpublished_candidate_boundary=true`，不得冒充 tag-pinned Release proof。

## Out Of Scope

- 不改变 capability projection 的采集结构或输出 schema。
- 不删除 distribution、Skill API/schema、installed inventory 的独立验证。
- 不修改 workflow exit、consumer、re-entry 或 stop marker。
- 不执行 commit、push、PR、merge、tag、GitHub Release 或 Issue 关闭。
- 不重新冻结 #304 的 exact Release candidate；该动作必须在修正合并后 fresh 执行。

