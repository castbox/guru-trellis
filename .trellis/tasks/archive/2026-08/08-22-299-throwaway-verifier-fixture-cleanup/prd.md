# #299 修复 throwaway verifier fixture coverage 与 failure cleanup

## 1. Goal

修复代表性 clean throwaway verifier 的两个独立 correctness 缺陷：Architecture Baseline eval
fixture 未覆盖全部声明 profile，以及失败退出时空临时文件数组在 macOS Bash 3.2 + `set -u`
下触发二次 `unbound variable`，掩盖原始失败。

Live authority：<https://github.com/castbox/guru-trellis/issues/299>。

## 2. Confirmed Facts

- task 基于 clean `main@1c2dbe908387576493afa5654a4d020bfa865f74`，隔离 branch 为
  `fix/299-throwaway-verifier-fixture-cleanup`。
- fresh `guru-sync-base` 已返回 `synced`，fresh Discovery public invocation 已返回
  `context_ready`；Issue #299 无重复 owner，也没有待用户决策的需求歧义。
- Architecture Baseline package 声明 `bootstrap_foundation`、`promotion`、`repair`、
  `task_impact_sync` 四个 profile；当前 eval corpus 仅覆盖 `promotion` 与
  `task_impact_sync`，而 compatibility validator 正确要求 declared 与 covered 集合完全一致。
- `verify-throwaway-install.sh` 使用 `set -euo pipefail`，退出 trap 的 cleanup 直接展开
  `"${GURU_TEMP_FILES[@]}"`；在目标 macOS Bash 3.2 中，空数组展开可触发
  `GURU_TEMP_FILES[@]: unbound variable`。
- #267 拥有完整多平台 Release matrix；#287 拥有 managed-path staging 工作，本 task 不接管
  二者。

## 3. Requirements

### R1. 补齐真实 Architecture Baseline eval profile coverage

- 为 `bootstrap_foundation` 与 `repair` 增加符合各自真实 entry contract 和 semantic intent 的
  最小 eval fixture，使 covered profile 集合与四个 declared profile 精确一致。
- 不删除声明 profile、不弱化 `covered_profiles != declared_profiles` validator，也不以虚假 profile
  标签包装其它 profile 的 fixture。
- 新 fixture 必须沿用 package 的 canonical eval schema、去敏示例与当前 Architecture authority。

### R2. 修复失败清理且保留原始错误

- cleanup 在临时文件数组为空时安全完成，不得因 nounset 产生二次失败。
- 数组非空时仍只清理由 verifier 创建且通过现有 allowlist/工作目录约束的精确临时路径。
- 另一个步骤先失败时，退出状态与可诊断输出必须保留原始失败，不得被 cleanup 覆盖或吞掉。

### R3. 回归测试

- 测试证明 Architecture Baseline eval corpus 精确覆盖四个声明 profile。
- 测试以目标 Bash 行为覆盖空数组 cleanup，证明失败退出不再出现
  `GURU_TEMP_FILES[@]: unbound variable`，且原始失败仍可见。
- 测试覆盖非空数组路径，证明既有精确清理仍有效。
- 回归测试应验证 canonical verifier/eval 入口，不以复制实现逻辑的测试替代产品证据。

### R4. 代表性 clean throwaway

- 按普通 Issue 的验证责任执行一个代表性 clean throwaway，证明当前版本可干净安装并运行
  Architecture Baseline compatibility verifier 路径。
- 若受到本 task 范围外的真实环境或上游失败阻塞，保留首个失败证据并明确标为 blocked/unverified，
  不将其声称为通过，也不扩张到 #267 的完整矩阵。

### R5. 分发与边界

- canonical source、preset 安装面、dogfood 安装副本及声明平台投影按实际受影响面保持一致。
- 处理 reapply 产生的 `.new` / `.bak` 并验证 upgrade/update 不会回退本修复。
- 不实现 #287，不自动关闭 #287，不执行 #267 完整 Release matrix。

## 4. Acceptance Criteria

- [ ] A1：Architecture Baseline eval 的 covered 与 declared profile 集合精确限定为
  `bootstrap_foundation,promotion,repair,task_impact_sync`。
- [ ] A2：空临时文件数组的 cleanup 在目标 Bash + nounset 下安全退出，不产生
  `GURU_TEMP_FILES[@]` 二次错误。
- [ ] A3：预先存在的 verifier 失败仍保留其原始退出状态和主要诊断。
- [ ] A4：非空数组 cleanup 仍删除通过既有 allowlist 检查的临时文件，且不放宽现有路径保护。
- [ ] A5：targeted tests、package/installed validation、dogfood drift、sidecar、
  `git diff --check` 与 recursive `.new/.bak` scan 通过。
- [ ] A6：一个代表性 clean throwaway 通过，或以首个 task 外阻塞事实诚实记录未验证边界。
- [ ] A7：fresh full-diff review 无 blocking finding；PR scope 只关闭 #299。

## 5. Docs SSOT And Architecture

- Docs strategy：`task_local_only`。本 task 修复既有 verifier/eval contract 的实现与 fixture，不改变
  对外使用方式；若实现发现 durable contract 必须变化，停止并重新评估文档 owner。
- Planning Architecture classification：`no_architecture_impact` / current-conforming correctness
  repair。不新增 owner、public Skill API、typed exit、状态或交互方向，不创建 Architecture
  contribution/ADR。

## 6. Out Of Scope

- #287 managed-path staging 的任何实现或关闭动作。
- #267 完整多平台 clean/existing/update/reapply/workflow-switch/release-candidate 矩阵。
- 新 workflow/Skill public API、Trellis 上游源码、全局 npm、`node_modules`。
- 攻击模型、恶意 artifact、锁、压力竞态、额外 crash-consistency 加固。
- commit、push、PR、merge、发布、Issue closure 与资源清理。

## 7. Open Questions

无。若新 fixture 无法在现有 profile contract 下表达，或 cleanup 修复要求改变公开合同，则停止实现并
重新澄清范围。
