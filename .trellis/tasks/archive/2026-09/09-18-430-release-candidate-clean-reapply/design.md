# #430 设计：clean candidate 的幂等 reapply

## 1. 根因

`build_installed_extension_manifest()` 每次 apply 都生成新 `installed_at` 并读取当前 Git
`HEAD` 作为 `source`。因此 post-merge candidate 即使所有 managed bytes 与已提交安装结果
相同，也会仅因执行位置变化重写 manifest。与此同时，`apply.sh` 直接启动 Python，导入和
子 validator 会在 source/target checkout 写入 bytecode cache。

## 2. Manifest 等价判定

installer 仍先按当前结果构造完整 candidate manifest。若存在 previous manifest，则仅为
等价比较忽略 candidate/previous 的 `installed_at`、`source`，并忽略
`skill_packages.files` / `overlays.files` 中仅描述本次执行的 `installed` / `unchanged`
action 标签：

```text
candidate manifest
  -> stable installed state without timestamp/source/transient file actions
  -> equals previous manifest: write previous manifest unchanged
  -> differs: write candidate manifest with current timestamp/source
```

进入比较前，本次执行必须没有 managed install、restore、update、removal、sidecar、配置或
guidance mutation。比较覆盖其余稳定 manifest 状态。因此缺失 managed file 被恢复、extension
version、managed hash、platform selection、package inventory、overlay/removal/conflict/sidecar
等任何实际变化仍会刷新 provenance。旧 manifest 缺失、结构无效或字段不完整继续由现有
validator 阻断。

## 3. Bytecode 边界

canonical `apply.sh` 和共享 `trellis/skills/guru-team/runtime/resolve-python.sh` 在启动 Python
前导出 `PYTHONDONTWRITEBYTECODE=1`。前者覆盖 preset 本身及其子 validator；后者覆盖 Stage 2
独立调用的 source/installed validators 与其它 managed-runtime wrappers。环境变量自动传给
子进程，不依赖 release caller 额外设置。Python bytecode 继续不属于 managed/public asset；
本次不增加清理逻辑，避免用执行后删除掩盖入口副作用。

## 4. 分发与文档

- 更新 `.trellis/spec/preset/installer.md` 定义 no-op manifest retention 与入口禁写 bytecode。
- 更新 canonical 和 dogfood `data-contracts.md` 解释 installed provenance 的 apply 语义。
- 更新 preset README 的可观察行为。
- 运行 preset apply 同步 installed/dogfood copies；所有生成变化必须属于本修复的预期范围。

## 5. 测试策略

1. Unit：previous source 与当前 source 不同但完整 managed result 等价，manifest bytes 保持。
2. Unit：改变 canonical managed byte 后 reapply 写入新 source/timestamp。
3. Entry integration：复制当前 repository 到临时 Git fixture，提交后直接运行 raw `apply.sh`，
   断言 tracked/untracked status、diff check、bytecode 和 sidecar residue 全为空。
4. Repository gates：preset tests、source/installed validators、四平台 parity、ownership、apply、
   dogfood drift、recursive residue 和 Git hygiene。

## 6. 兼容性与风险

- 不改变 manifest schema 或 key set。
- fresh install 仍写当前 provenance；真实内容变化仍刷新 provenance。
- no-op 保留的是产生当前 installed bytes 的原 provenance，避免把验证 candidate 错记为安装源。
- installer Python 文件超过 3000 行；本次只增加单一等价 helper，避免无关大规模拆分。若实现
  需要扩大状态或修改 transaction architecture，立即停止并重新规划。

## 7. Architecture / Docs SSOT

这是 preset provenance 与执行副作用的局部修正，不改变系统 owner、public API、schema、Skill
route 或跨模块架构；Architecture impact 为 `no_architecture_impact`。Docs 使用 `ssot_first`：
先更新 installer/data-contracts authority，再修改代码与测试，最后通过 preset apply 同步副本。
