# Implementation: Finalizer 最小 Provenance Tail

## 1. 实施顺序

1. 在 canonical Finalizer runtime、preset companion 和现有测试中定位完整
   installer 调用、manifest postimage 校验和 source/target fixture 边界。
2. 实现 package-local 的最小 provenance-tail producer；保留现有 source
   binding、target-only mutation 和 fail-closed validator。
3. 增加或调整 Finalizer contract/runtime tests，证明：
   - reprepare 不调用完整 preset apply；
   - `installed_at` 与 install inventory 保持字节稳定；
   - 允许的 source tail 正常生成；
   - source/target identity、dirty/mutable、managed-byte、sidecar、extra
     field/action/list/order drift 仍然阻塞。
4. 增加并行 PR regression fixture，模拟两个业务 task 从同一安装 manifest
   生成 tail，确认不会因为时间戳制造 `extension.json` 冲突。
5. 调整 preset installer 回归测试，确认完整初装、reapply、update 后 reapply
   仍保留 installer 自己的 `installed_at` 语义，Finalizer 改动不改变该路径。
6. 将 canonical 变更投影到 dogfood/shared/platform installed assets，运行
   package inventory、manifest/schema、drift 和相关 installed validation。

## 2. 预计变更范围

- `trellis/skills/guru-team/packages/guru-finalize-task/`
- 必要时 `trellis/presets/guru-team/scripts/python/` 的独立 companion producer
  或其测试
- 相关 `interface.json`、references、examples、schemas 与 tests
- `.trellis/guru-team/` 及平台安装副本的生成同步
- Issue #325 task-local planning/validation artifacts

不修改业务 repo；不修改 Trellis upstream、global npm、node_modules 或隐藏
安装状态。

## 3. 定向验证

- Finalizer package contract/runtime tests。
- preset installer tests 与 manifest regression tests。
- canonical -> dogfood drift 检查。
- installed business fixture 的 Finalizer/reprepare regression。
- 必要的 `trellis-check`，覆盖完整 Issue #325 accepted scope。

## 4. 完成门禁

- 先完成 Phase 1 规划审查，再进入实现。
- 实现后执行 Phase 2 `guru-check-task`，不得用单个命令代替完整语义检查。
- 通过 Branch Review，审查范围为当前 base 到 HEAD 的完整 diff。
- PR readiness 只在实现、测试、projection、sidecar/drift 证据完整后判断。
- 当前文档不宣称完整多平台 Release/upgrade 矩阵已通过。
