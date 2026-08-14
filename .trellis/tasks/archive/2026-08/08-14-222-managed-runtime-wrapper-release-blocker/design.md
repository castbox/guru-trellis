# #222 受管 Python wrapper 修复设计

## 根因

公共 Skill package wrapper 已通过 `trellis/skills/guru-team/runtime/launch.sh` 进入
`resolve-python.sh`，但 `trellis/workflows/guru-team/scripts/bash/` 下的共享 validation、
discovery 和 compatibility wrapper 仍直接 `exec python3 -m runtime.*`。preset 将这些
wrapper 安装到目标仓后，source/installed 检查会继承调用者 PATH，绕过刚创建的 active
managed runtime。Branch Review 进一步发现 eval runner 进入 managed runtime 后，四个
platform adapter shell 又直接 `exec python3 native_adapter.py`，形成第二个 PATH fallback；
focused source fixture 也没有建立 commit identity，不能稳定代表正常 fresh source checkout。

## 设计

1. 为共享 wrapper 复用同一个 repo/runtime root 解析合同。
2. wrapper 在 canonical source layout 与 installed layout 中分别确定 `REPO_ROOT` 和
   `RUNTIME_ROOT`，然后调用 `RUNTIME_ROOT/runtime/resolve-python.sh`。
3. `resolve-python.sh` 继续独占 active pointer、interpreter path、runtime identity 和
   dependency probe 的确定性校验；wrapper 不复制 Python 依赖判断。
4. 补充无依赖 PATH Python fixture，证明 source validation、contract/eval discovery、
   eval execution 和 compat command 都不会落回 PATH Python。
5. 四个 eval adapter 从自身路径判定 canonical/installed layout并使用所属 checkout 的
   resolver；用 PATH 完全无 `python3` 的 source/installed 八路探针验证第二跳。
6. Fresh source fixture 在 apply 前创建本地 commit identity，完整 source/installed eval
   execution 必须实际通过，不接受降低 assertion 或 PATH fallback。
7. 运行 preset apply 同步 dogfood installed copies并刷新 manifest hashes。
8. 将 extension revision 更新为 `0.6.5-guru.30`，同步所有稳定映射与发布文档。

## Docs SSOT Plan

- strategy: `ssot_first`
- canonical runtime contract: `trellis/skills/guru-team/runtime/resolve-python.sh`
- canonical shared wrappers: `trellis/workflows/guru-team/scripts/bash/`
- installed projection: `.trellis/guru-team/scripts/bash/`
- public version mapping: repo/preset/workflow README 与 release notes

## 风险与恢复

- source wrapper 必须选择 source checkout 的 runtime，installed wrapper 必须选择目标仓
  runtime，不能跨 checkout 复用 active pointer。
- active runtime 缺失或损坏时必须输出结构化 `runtime_dependency_missing`，不得自动使用
  系统 Python。
- 修复会改变 extension bytes，因此必须废弃 `.28` candidate 身份并重新执行全部 pre-tag
  gate；不得复用此前失败轮次的 SHA、digest 或测试证据。
