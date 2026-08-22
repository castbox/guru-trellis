# #299 技术设计：throwaway verifier fixture 与失败清理修复

## 1. Design Boundary

本 task 保持 Architecture Baseline Skill、compatibility validator 与 throwaway verifier 的现有合同。
修复 owner 是 canonical eval corpus 和 verifier cleanup；除非定位到实际 validator correctness bug，
不修改 profile 声明或集合完全一致门禁。

## 2. Architecture Eval Coverage Flow

```text
canonical architecture-baseline package
  -> package.yaml declared profiles
  -> evals/evals.json cases + input fixtures
  -> preset installer stages package into throwaway repository
  -> verify_trellis_compatibility_matrix.py collects input_profile_id
  -> covered_profiles == declared_profiles
```

- 分别为 `bootstrap_foundation` 与 `repair` 建立最小、真实、可独立审查的 input fixture 和 eval case。
- 每个 case 的输入、期望 exit 和语义描述必须符合该 profile 的 current contract；不复用其它 profile 的
  payload 只为满足集合检查。
- 保留 `promotion`、`task_impact_sync` 的既有 corpus 与严格集合比较。

## 3. Cleanup Flow

```text
verifier primary operation
  -> optional temp path creation and tracked append
  -> success or primary failure
  -> EXIT trap cleanup
       -> zero entries: no array element expansion
       -> entries exist: validate exact allowed path, remove it
  -> preserve primary exit status
```

- 在迭代前显式判断数组元素数量或使用经 macOS Bash 3.2 nounset 验证的兼容结构，确保零元素分支
  不展开未绑定元素列表。
- 不取消 `set -u`，不使用全局错误抑制，也不扩大 cleanup 既有 allowlist 路径范围。
- cleanup 如需保存退出码，应在 trap 入口捕获，并在完成后返回该码，避免二次动作改写首个失败。

## 4. Regression Strategy

- Profile coverage：从 canonical package metadata 与 eval corpus 读取真实 profile，断言集合精确一致，
  并让现有 compatibility route继续执行。
- Empty cleanup：以隔离 shell fixture触发 verifier 的早期、可控失败，使临时文件列表保持为空；断言
  原始非零状态/诊断存在且无 unbound-variable 二次错误。
- Non-empty cleanup：创建符合现有命名和目录约束的临时文件，触发退出并断言精确文件被移除。
- 代表性 clean throwaway：使用仓库 canonical installer/verifier 路由，而不是 direct import 或复制逻辑。

## 5. Distribution And Upgrade Safety

Canonical owner 位于 `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/**` 与
`trellis/presets/guru-team/scripts/**`。根据实际 changed paths 运行 preset reapply，同步 dogfood
`.trellis/guru-team/**` 及受管理平台投影；随后检查 overlay drift、文件 mode、sidecar 与
`.new/.bak`。不得只修安装副本。

## 6. Architecture And Docs

本修复补齐现有 eval coverage 并修正 deterministic cleanup correctness，不改变组件 owner、public
DTO、typed exit 或依赖方向。Planning path 为 `no_architecture_impact`，durable docs strategy 为
`task_local_only`。

## 7. Risks

| Risk | Control |
| --- | --- |
| 用标签凑齐 profile 覆盖 | fixture 必须通过对应 profile current contract 的语义审查 |
| cleanup 修复吞掉首个错误 | 回归同时断言原始 exit 与诊断 |
| 只测空数组导致非空清理退化 | 增加受约束临时文件的配对测试 |
| 只修改 dogfood 副本 | canonical-first，reapply 后检查 drift |
| 普通 task 吸收 Release matrix | 只跑一个代表性 throwaway，完整矩阵保留给 #267 |
