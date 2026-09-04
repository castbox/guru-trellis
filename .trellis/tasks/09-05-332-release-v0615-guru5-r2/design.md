# #332 v0.6.15-guru.5 发布设计

## 设计边界

本任务是 release-owned preparation 与正式发布编排，不重新实现 #311、#333、#339、
#358、#361 的已合入 payload。源代码、测试和文档修改必须遵循当前 `.43` authority，
并由 canonical `trellis/` 源生成 dogfood 与平台 projection。

## Source of Truth 与 projection

- extension version 的 canonical owner 是 `trellis/guru-team-extension.json`；根目录
  README、workflow/preset README、fixture 与 verifier 只作为 release-facing projection
  或直接验证面。
- workflow、preset、overlay、registry、ownership 和 installed files 通过官方支持的
  marketplace/preset/apply 路径维护；不对 Trellis 上游源码或生成副本做一次性 patch。
- `.trellis/`、`.agents/`、`.codex/`、`.claude/`、`.cursor/` 等 dogfood/runtime
  projection 必须从 canonical source 重新生成并检查 byte/mode/parity 与 drift。

## Candidate 与身份绑定

preparation branch 不是最终 candidate。PR merge 后重新 fetch `origin/main`，冻结
clean candidate commit/tree，并绑定：

`v0.6.15-guru.4..candidate` -> `v0.6.15-guru.5` -> `0.6.15-guru.40` -> Trellis CLI `0.6.15`。

任意 release-facing 内容、版本、目标 branch、工作区或 required evidence 变化都会使
旧 candidate/review 失效，必须重新从当前 authority 开始。

## Release Gate 分层

1. preparation branch：只证明实现、定向测试和 projection 结果。
2. merged main：重新冻结 exact candidate，执行完整 Release Gate 与 independent
   Branch Review/Publication/Finalizer 链。
3. immutable tag：live 回读 tag object、peeled commit/tree 后执行 tag-pinned
   install/update/reapply/smoke；失败时不移动、删除或重建 tag。
4. GitHub Release：仅在 tag 与 smoke 通过后创建非 draft、非 prerelease Release，并
   回读 target、tag、peeled candidate、latest stable 与 assets。
5. closeout：仅在 Release live facts 一致后关闭 #332。

## 已合入变更的承接

- #311：验证 source/target checkout identity、installed Finalizer provenance 与业务仓
  release-scoped replay。
- #333：验证 Issue 创建部分成功后的 exact recovery、唯一匹配和无重复创建。
- #339：验证仓库私有两阶段 release orchestration，不替代 semantic gate 或独立副作用确认。
- #358：验证 fresh reviewed task evolution 下 Finalizer transaction rebind。
- #361：验证 Publication Review owner 错误分类、content preflight 与精确 re-entry。

## Docs SSOT Plan

策略：`ssot_first`。

- 版本、tag、extension revision 与 CLI 映射的 durable owner：extension manifest 与
  canonical public README；workflow/preset README 承接安装、preview/switch、update
  和 reapply 合同。
- Requirements、Design、Test、Architecture 共享 authority 保持
  `current-main-0.6.5-guru.43`；本 task 不直接改写共享 current authority，除非
  `task_impact_sync` 判定存在被批准的 contribution。
- Release notes、candidate freeze、验证摘要和 PR body 属于本 task 的历史记录；不把
  动态 gate 状态写回 current RDT/Architecture 正文。
- verifier、ownership、drift 和安装结果只保留直接 consumer 所需的 candidate identity
  与结论，不保存授权过程、secret、完整临时日志或机器绝对路径。

## 兼容性与回滚

保持三个独立版本轴，不把 knowledge baseline 当作发布版本。保持历史 tag/Release
immutable；tag 创建后的验证失败只允许停止并记录，不允许移动或删除 tag。preparation
阶段的文件修改可在未提交前由任务分支回退，不能影响主工作区、旧分支或其他 worktree。
