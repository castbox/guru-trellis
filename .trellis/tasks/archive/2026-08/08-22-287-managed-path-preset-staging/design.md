# #287 技术设计

## 现状与边界

`install_assets()` 当前在 `temporary_directory("preset_staging")` 下调用 `copy_repo_to_staging()`，随后让 `_install_assets_in_place()` 在 staging repo 中执行完整安装，再以 `activate_staged_repository()` 激活。#286 已定义临时对象的 root/prefix/登记、stale 回收、信号清理和诊断保留边界；本 Issue 只替换 transaction 的 materialization 面，不重做生命周期所有权。

## 方案

1. 建立 versioned managed inventory projection。Inventory 由 canonical preset manifest、`MANAGED_ASSET_PATHS`、`MANAGED_SPEC_PATHS`、runtime kernel、选定 platform package/overlay inventory 以及当前 installed manifest 的 managed records 组成。每项包含 source、target、stable asset id、kind/mode、merge/conflict、sidecar、validation 和 activation/rollback metadata。
2. 在同一 controlled temporary root 创建 `repo` staging 目录，但只 materialize inventory 需要的目标 preimage、canonical source candidates、目标父目录和 transaction metadata。以 lexical relative path 校验防止越界；不 walk/copy unmanaged repository content，`.git`、依赖、build output、nested repo、untracked files 默认不进入 staging。
3. 在 materialization 前计算 managed file count、logical bytes、预计 staged/backup/sidecar peak、safety margin 和 available space。将 strategy、root、inventory digest 和计数写入本次结果/诊断；空间不足在写入前返回稳定失败。
4. `_install_assets_in_place()` 继续作为目标-owned merge/action-plan 生成器，但所有 source/target 读取绑定到 managed inventory。`activate_staged_repository()` 改为按 action plan 的 writes/removals 执行，并保留每目标安全 replace、preimage 校验、backup/sidecar recovery 与 installed validation；不再以 staging tree 与 repository 的全量集合差异推导删除。
5. 当 activation validation 失败时，只 materialize manifest 中声明的 `.new`/`.bak` sidecars；recoverable managed backup validation 仍使用 #286 temporary lifecycle，并只恢复 action plan 剩余步骤。preimage 变化触发 fresh reprepare，不复用 stale plan。
6. 扩展 result/installed manifest 的最小 observable fields，保持现有 schema/version compatibility；需要 breaking contract 时新增 version 并提供迁移。通过 installer 重新投影 canonical/dogfood/installed 与平台 copies，运行 drift/update/reapply checks。

## 失败与兼容性

- unknown/modified managed target 继续 fail closed 或产生声明的 sidecar，不覆盖用户修改。
- legacy whole-repo staging state 只作为诊断/recovery 输入，不成为 current authority。
- non-APFS 使用 canonical managed-path transaction；APFS 如存在只可作为 managed candidates 的显式优化，不能成为 correctness fallback。
- 多文件 activation 的真实语义按可恢复 transaction 描述，不声称单一 filesystem atomic commit。

## 验证策略

目标覆盖 `test_apply_guru_team_trellis_preset.py` 的交易/冲突/恢复测试，新增 large-unmanaged fixture 统计 traversal/materialization 与 space-preflight 测试；另运行 preset apply、dogfood drift、installed validation 和一个 clean isolated throwaway。完整跨平台 exact-candidate matrix 延后给 #267。
