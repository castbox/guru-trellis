# Design: Finalizer 最小 Provenance Tail

## 1. 现状与问题边界

当前 `guru-finalize-task/runtime/owner.py` 的 provenance tail preparation
从独立 source checkout 获取 preset apply entry，再以 target checkout 为
`--repo` 执行完整 installer。installer 重新构造整个
`.trellis/guru-team/extension.json`，其中 `installed_at` 使用当前时间生成。
Finalizer 只需要把当前 reviewed source identity 投影进 tail，不需要重新执行
安装清单计算，因此发生了职责混淆。

## 2. 方案

在 Finalizer package 的 provenance preparation 中拆出一个确定性的最小
metadata-tail producer：

1. 仍按现有 self-hosted/installed 规则解析独立 source checkout 和 target
   reviewed checkout。
2. 读取 target manifest preimage，保留顶层 schema、`installed_at`、`install`、
   `skill_packages`、`overlays`、`notes` 等既有内容。
3. 只构造并写入 allowlist 中的 `source` provenance 字段，source/ref/commit
   仍绑定现有 reviewed content head 或 immutable installed identity。
4. 对 postimage 执行现有 manifest field diff 和文件 action transition 校验；
   除允许的 source 字段及既有 `installed -> unchanged` action transition 外，
   任何变化均 fail closed。
5. 只允许 target reviewed checkout 产生 manifest tail；source checkout 保持
   clean 且 identity 不变。metadata tail 仍以一个 parent 等于 reviewed head
   的 commit 进入后续 publication lineage。

独立 producer 可以是 Finalizer runtime 内的 package-local helper，也可以是
canonical preset 中供 Finalizer 调用的专用 deterministic script；选择以当前
代码复用和安装投影边界为准，但不得重新调用完整 preset apply。

## 3. 责任分层

| 能力 | 所有者 | 允许的变化 |
| --- | --- | --- |
| 初次安装、完整 reapply、Trellis update 后 reapply | preset installer | 重建安装 inventory，按安装语义决定 `installed_at` |
| Finalizer provenance reprepare | Finalizer metadata-tail producer | 仅 source provenance tail |
| AI scope/finding/route 判断 | Finalizer semantic owner | 不由脚本替代 |
| manifest/postimage/diff 校验 | deterministic validator | 只校验客观条件并 fail closed |

## 4. 兼容性与失败行为

- 保留现有 `self_hosted` 与 `installed` 两种 source binding。
- 保留 canonical repo、exact OID、detached、clean、mutable-ref 和 reviewed
  HEAD 校验。
- source checkout 缺失、fetch/HEAD/identity/clean 校验失败时，在 push、PR、
  archive、Ready 和 Issue mutation 前停止。
- target manifest 存在额外字段变化、managed byte drift、sidecar 或未允许的
  action/list/order 变化时停止。
- 不对旧业务仓库做自动一次性迁移；Finalizer 应从当前 manifest preimage
  生成最小 tail。

## 5. 投影与同步

canonical 修改位于 `trellis/skills/guru-team/packages/` 或其明确的
`trellis/presets/guru-team/` companion source。完成 canonical 修改后：

- 同步 `.trellis/guru-team/` dogfood 安装副本；
- 同步声明支持的平台 package projection；
- 更新需要随 package 安装的测试、schema、examples、README/spec 合同；
- 运行 preset apply 后的 dogfood drift 检查，确认安装副本未漂移。

## 6. 设计决策

不通过让 Finalizer 调用 installer 后再恢复旧 `installed_at`，因为这仍然会
重建完整 inventory、扩大副作用并掩盖职责混淆。最小 producer 直接表达
Finalizer 的真实需求，能够将 `installed_at` 的稳定性变成可测试合同。
