# 技术设计

## 设计原则

路径解析属于 `guru-create-task-workspace` owner 的确定性 runtime 事实，不属于
AI 命名或 scope 判断。实现保持 package-local，不引入 shared monolith、兼容
fallback 或 public I/O 迁移。

## 单一解析入口

在 canonical package 的 `runtime/common.py` 提供一个共享 resolver：

1. 从 repository root 读取 `.trellis/guru-team/config.yml`。
2. 要求 `workspace_mode` 为 `worktree` 或 `current`；缺失或其他值 fail
   closed。
3. `current` 返回规范化 repository root，并拒绝会暗示另一个 workspace 的
   不一致输入。
4. `worktree` 对空 root 使用 `repo.parent / f"{repo.name}-worktrees"`；绝对
   root 直接规范化；相对 root 以 repo 为基准规范化。
5. resolver 返回 mode、workspace root 与具体 workspace path，供 executor、
   checker、reuse/recovery 共同消费。

配置读取使用仓库现有 YAML/结构化解析能力；若现有 runtime 没有可复用 helper，
仅实现该 package 所需的最小标量解析，并通过错误合同拒绝歧义或非法结构。

## 执行与检查

- `worktree`：executor 在业务写入前解析并检查目标，随后创建或 exact reuse；
  checker 使用同一 resolver 重算期望路径并核对 live Git facts 与 mapping。
- `current`：executor 不调用 `git worktree add`，在当前 checkout 内执行 task
  artifact/mapping 写入；branch/base/task boundary 仍按现有合同校验。
- 任一冲突、stale/mismatch 或不可接受路径在 branch/worktree/task/mapping 写入
  前返回现有稳定错误类别。
- public result 不新增绝对路径字段，绝对路径只存在 ignored mapping 与 live
  checker 内存。

## 分发与文档

canonical package 是实现 SSOT。使用 preset installer/apply 流程同步 dogfood
installed package 与平台 projections，并更新 manifest/hash。现有 contract、
workflow README、preset README 只补足共享 resolver 与两种 mode 的准确行为，
不复制实现细节。

## 测试设计

使用临时真实 Git repository 加载明确 config，覆盖：默认空 root、绝对 root、
相对 root、current、exact reuse、目标冲突、invalid/missing mode、stale/mismatch。
每个失败用例同时断言没有部分 branch/worktree/task/mapping。分发层验证 clean
initial install、existing reapply、official update、platform parity 与 sidecar
hygiene。

## Docs SSOT Plan

- 需求与验收：本 task `prd.md`，完成后归档。
- Skill 行为合同：canonical package `references/contract.md`。
- 用户安装/配置说明：`trellis/workflows/guru-team/README.md` 与
  `trellis/presets/guru-team/README.md`。
- 配置字段 SSOT：现有 `trellis/workflows/guru-team/config-template.yml`；若文案
  已准确则不制造无意义改动。
