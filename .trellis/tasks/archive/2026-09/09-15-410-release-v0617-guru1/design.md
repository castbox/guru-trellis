# #410 技术设计

## 设计依据与边界

本设计承接 Issue #410、`.agents/skills/release-guru-trellis-version/references/contract.md`、`.trellis/spec/docs/public-docs.md`、`.trellis/spec/docs/requirements-design-test-ssot.md` 和 `.trellis/spec/workflow/quality-guidelines.md`。发布编排只消费现有 owner 的结果，不复制或削弱 `guru-check-task`、`guru-create-task-commit`、`guru-review-branch`、Architecture/RDT promotion、Publication、Finalizer 和 Merge 的内部合同。

本任务的唯一长期交付是候选 source/document/package 变更及正式 tag/Release；生命周期状态、授权、完整 gate 历史、候选 digest 和发布进度不写入 tracked artifact。

## 版本轴与候选身份

| 轴 | 前序 | 目标 | 权威位置/验证 |
| --- | --- | --- | --- |
| repository tag/Release | `v0.6.16-guru.1` | `v0.6.17-guru.1` | live Git tag 与 GitHub Release |
| Guru Team extension | `0.6.16-guru.41` | `0.6.17-guru.42` | `trellis/guru-team-extension.json` 与 public README |
| Trellis CLI/core | `0.6.17` | `0.6.17` | candidate source/build 与 README |
| framework source lock | 当前 main lock | 按当前 accepted change 保持明确 | `trellis/presets/guru-team/source/trellis-source.json` 及验证输出 |

Stage 2 冻结的 candidate 是 fresh `origin/main` 的完整 commit SHA 和 tree identity。前序 tag 到 candidate 必须通过祖先关系和完整 diff 验证。所有命令输出、gate 结论、tag 和 Release body 都以这个 candidate 为唯一身份，不能使用短 SHA 或 Stage 1 reviewed HEAD 替代。

## 两阶段数据流

```text
stable planning -> pre-promotion delivery -> fresh Phase 2/check
  -> guru-create-task-commit -> full Branch Review
  -> serialized Architecture + RDT promotion -> fresh Phase 2/check
  -> guru-create-task-commit -> full post-promotion Branch Review
  -> Publication (Refs #410) -> Finalizer -> preparation PR -> Merge
  -> fresh origin/main exact candidate -> targeted release gate
  -> annotated tag + smoke + GitHub Release -> independent Issue closure
```

任何 promotion-created delivery bytes 都使先前 Phase 2、commit、Branch Review 和 Publication 失效；任何 candidate drift、远端变化、版本映射不一致、验证 skip/fail 或 Release 文案语义不足都停止在当前 owner。

## Docs SSOT Plan

实施阶段先运行 Architecture `task_impact_sync(stage=planning)` 和 RDT `task_impact_sync`。本任务只在 task-local contribution 中记录可追溯增量，推荐路径为：

- `docs/architecture/contributions/410-release-v0617-guru1.md`：说明发布版本轴、candidate authority、release boundary 和不新增架构 owner 的结论。
- `docs/requirements-design-test-contributions/410-release-v0617-guru1/`：按 `R410 -> D410 -> T410` 记录需求、设计、验证和 traceability，不复制 current authority 全文。
- canonical public surfaces：`README.md`、`trellis/guru-team-extension.json`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`，以及必要的 workflow/preset/source lock/validator 文件。
- generated/dogfood/installed projections：按受影响 canonical source 同步 `.trellis/workflow.md`、`.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/` 和 preset 安装副本；不得把 projection 当作唯一源头。

Docs 只写稳定合同、版本关系、安装/升级方式、验证入口和未验证边界。命令输出、授权、reviewer 元数据、候选生命周期和临时路径保留在当前会话或 owner-private runtime。

## 兼容性与回滚

保持已有 Skill ids、exit ids、schema ids、script commands、template ids 和 workflow/preset ownership。若必须新增公共 API，另建迁移合同；不得静默重命名或改变既有语义。官方 Trellis-owned 文件按 `.new/.bak` 语义处理，未知用户修改不得覆盖。

回滚只允许针对本任务已识别的 candidate/发布动作，并重新读取 live refs 后执行对应独立操作；不使用 `git reset --hard`、历史重写、强推或无确认 cleanup。tag/Release 创建后，回滚优先通过明确的 release/tag 处置流程报告，不伪造为未发布状态。

## 架构判断

当前影响为 `architecture_impact`：发布合同明确绑定 source identity、四轴版本映射、candidate authority、Docs SSOT promotion 和独立副作用边界。方案复用现有 single-writer、AI-first、official ownership 和 fresh evidence 原则，不新增 lifecycle owner、公共 Skill、恢复层或业务仓库职责。若实施发现需要改变现有 owner、exit、GAP 或架构基线，停止并重新进入 Architecture review。
