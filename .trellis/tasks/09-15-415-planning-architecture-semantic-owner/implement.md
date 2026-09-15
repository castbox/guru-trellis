# #415 Implementation Plan

## 1. 准备与边界

- [ ] 读取 live Issue #415、三份 planning 文档、Architecture/RDT current authority、
      workflow/spec 与受影响 package code。
- [ ] 每次写入前运行 workspace boundary check；只修改本 task 批准范围。
- [ ] 保留所有无关 dirty/untracked 文件、worktree 和远端状态。

## 2. Contract 修复

- [ ] 更新 canonical `guru-maintain-architecture-baseline/SKILL.md` 与 contract，明确完整
      contract load、当前 AI owner authoring/invoke 序列和具体失败分类。
- [ ] 更新 canonical `guru-approve-task-plan` 的相邻 consumption 文案，避免再次寻找外部
      Architecture owner。
- [ ] 增加/调整 package contract tests，保持 2.0 public I/O、exits、consumers 和 freshness
      不变。

## 3. Native semantic authoring regression

- [ ] 为 eval manifest 增加显式 semantic-authoring case mode，缺省保持 post-owner 行为。
- [ ] 拆分 owner fixture staging：authoring case 只准备 public input/live authority/project check，
      不生成或绑定 owner result。
- [ ] 扩展 native adapter context、stdin public boundary 和 trace validator，使 Agent 可读取完整
      public contract/authority，自行 author envelope，并只调用一次正式 wrapper。
- [ ] 新增 runtime tests，覆盖 mode schema、无预填 result、禁止答案泄露、required reads、单次
      invocation 和 fail-closed 路径。
- [ ] 新增 Architecture Planning native regression，证明 Agent 返回 fresh `baseline_current`。
- [ ] 闭合 corpus schema：adapter/model 仅允许且必需于 `semantic_authoring`；缺省 mode 与
      `post_owner` 携带这些字段必须失败。
- [ ] 修复 full-run applicability：所有 `post_owner` case 对所有 adapter 适用，只有
      `semantic_authoring` 按声明 adapter 过滤；focused mismatch 保持 `unsupported`。
- [ ] 让 runner aggregate 与 compatibility matrix 独立验证 expected/actual case ids 完全一致，
      missing、duplicate、unknown、unexpected 均 fail closed。

## 4. Projection 与安装同步

- [ ] 从 canonical source 同步 `.trellis/guru-team/skills/packages/` dogfood installed copy。
- [ ] 同步 `.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/` 及其
      preset overlays；不得手工维护不同语义。
- [ ] reapply Guru Team preset，检查并处理 `.new`/`.bak`，验证 dogfood overlay drift 为零。

## 5. 验证

- [ ] 运行两个受影响 Skill 的 focused contract/runtime tests。
- [x] 运行 `guru-approve-task-plan` contract suite 并只记录 fresh 实际结果：`23/23`。
- [ ] 运行 eval adapter/eval runner focused tests 与 Architecture semantic-authoring native case。
- [ ] 运行 skill package schema/interface/eval validation 和 projection parity 检查。
- [ ] 运行 preset reapply、dogfood drift、声明平台 projection parity。
- [ ] 根据变更风险决定是否执行一个代表性 clean throwaway；不执行完整 release matrix。
- [ ] 运行 `git diff --check` 并确认无 scope 外改动。

## 6. Phase 2 与交付门禁

- [ ] 重新执行 RDT/Architecture `task_impact_sync(stage=phase2)`。
- [ ] 执行完整 `guru-check-task`，修复 task-scope findings 后重新检查。
- [ ] 展示精确 commit 范围并另行取得 commit 授权；push、PR、merge、cleanup 均独立确认。

## 7. Docs SSOT 执行

- `update`：Architecture package `SKILL.md` / `references/contract.md`。
- `conditional_update`：Planning approval package `SKILL.md` / contract，仅限相邻承接歧义。
- `update`：`.trellis/spec/workflow/skill-package-contract.md`、`data-contracts.md`、
  `companion-scripts.md` 与直接声明 Skill Eval 行为的 workflow/preset public README。
- `no_update`：`docs/requirements/**`、`docs/design/**`、`docs/test/**`、
  `docs/architecture/**` 及其余 `.trellis/spec/**`，因为本任务只同步已直接变化的 Skill Eval
  durable contract，不改变 shared product/Architecture authority。
- 实现若推翻任一 `no_update` 判断，停止并返回 Phase 1 重做 RDT 或 Architecture owner gate。
