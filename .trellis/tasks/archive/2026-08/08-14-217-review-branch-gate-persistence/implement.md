# #217 实施计划

## 1. 固化当前缺陷与路径合同

- 在真实临时repo中用现有public wrapper复现 recorder不创建checkpoint，并保留为修复前证据。
- 对照 `guru-review-branch` Skill/interface/commands/runtime与其它owner-private checkpoint package，确定唯一task/owner path resolver及terminal/non-terminal生命周期。
- 不读取或复用旧快照作为实现authority；所有判断绑定当前task base与live Issue。

## 2. 实现 recorder/checker/invoke 生命周期

- 在canonical `guru-review-branch/runtime`实现安全checkpoint resolver、regular JSON写入/读取与retire helper。
- recorder在semantic gate和schema/objective validation通过后写精确checkpoint，只输出最小receipt。
- checker从精确checkpoint读取并验证task/base/head/review intent/typed exit/content freshness，不接受Agent手工复制stdout作为normal path。
- invoke内部重新check，投影现有唯一typed output，并按明确矩阵retire terminal或retain非终态checkpoint。
- 对duplicate、retired、stale、mismatch和unsafe/symlink路径返回稳定错误；不增加锁、TOCTOU或恶意actor机制。

## 3. 更新公共package合同

- 同步 `SKILL.md`、`references/contract.md`、`commands.json`、interface、必要schema/example和thin wrappers。
- 保持现行semantic ownership、gate schema 4.0、五个exits和consumer mapping不变。
- 若需要通用Docs SSOT说明，仅最小更新canonical `skill-package-contract.md`/`companion-scripts.md`/`quality-guidelines.md`，避免复制step-local细节。

## 4. 补齐真实wrapper测试

- 用shell wrappers完成`record -> check -> invoke -> retire/retain`，测试不得手工写recorder返回值或直接注入private owner result。
- 覆盖`passed`和至少`implementation_required`一个非终态route。
- 覆盖stale content、wrong task/base/head、unsafe/symlink path、duplicate record/invoke及retired checkpoint。
- 保留必要package纯函数测试，但将现有手工gate测试改为不冒充生命周期acceptance。

## 5. 同步canonical、installed与平台投影

- 更新canonical package后运行targeted preset apply `--all-platforms`，同步`.trellis/guru-team`与Shared/Codex/Claude/Cursor public projections。
- 更新managed inventory/manifest中受影响hash；处理当前task产生的known `.bak`，确保未知`.new/.bak`为零。
- 第二次reapply证明幂等；检查dogfood overlay drift与canonical/installed equality。

## 6. 验证命令

- `guru-review-branch` package contract/runtime tests及新增wrapper lifecycle fixture。
- 受影响shared runtime与package integration tests。
- source/installed package validator及canonical/installed equality。
- Shared/Codex/Claude/Cursor projection equality。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` targeted apply与reapply。
- managed inventory、`check-dogfood-overlay-drift.sh`与recursive未知sidecar scan。
- `guru-check-task`对当前task完整scope执行semantic check。

明确不运行：完整12-capability `guru-verify-extension-installation`、完整marketplace、official Trellis update、全平台throwaway、业务仓库upgrade smoke、tag或Release。

## 7. Phase 3 交付

- 只stage当前task规划、canonical/installed/package/docs/tests及受管投影文件；不提交无关worktree内容。
- 通过`guru-create-task-commit`创建reviewed commit后，独立Branch Review覆盖完整`origin/main...HEAD`。
- Publication readiness确认中文PR标题/正文、真实验证范围、`Closes #217`、#219 related与#218/#222 follow-up边界。
- push与PR各自作为Git/GitHub副作用边界单独展示并取得确认；不创建tag/Release，不声称main可发布。

## 高风险文件

- `trellis/skills/guru-team/packages/guru-review-branch/runtime/{common,record,check,invoke}.py`
- `trellis/skills/guru-team/packages/guru-review-branch/commands.json`及thin wrappers
- package wrapper lifecycle tests
- preset installed manifest与四平台public projections

## 实现前门禁

- live Issue、ledger与本规划一致，只关闭#217。
- `prd.md`、`design.md`、`implement.md`无开放问题并完成措辞审查。
- `guru-approve-task-plan`通过并自动激活task后才进入Phase 2。
- 实现与check按当前`codex.dispatch_mode: sub-agent`交给Trellis sub-agents；主会话负责spec、集成、commit与finish。
