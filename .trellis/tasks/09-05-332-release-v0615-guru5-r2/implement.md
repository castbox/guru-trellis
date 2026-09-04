# #332 v0.6.15-guru.5 稳定实施计划

## Phase 1：规划与激活

以 fresh `origin/main`、live Issue #332、active knowledge baseline 和 task-local
Requirements/Design/Test/Architecture contract 完成 standard intake、规划审查、
Architecture/RDT impact 判断，并按官方 Trellis 入口激活 task。

## Phase 2：Preparation

1. 在已确认的 task worktree 内重读 relevant workflow、preset、spec 与当前 authority，
   保持 workspace boundary 和既有用户改动不变。
2. 按 #332 accepted scope 更新 canonical release identity、manifest、README、workflow/preset
   文档、fixture、verifier 与 canonical/dogfood/installed projection，使 `.5/.40/CLI 0.6.15`
   一致；保留历史 facts。
3. 运行与本 task 相关的 preset apply/reapply、package/runtime/integration/eval、安装投影、
   upgrade/update/reapply、平台 projection、Issue recovery、Publication/Finalizer 与 release
   identity 定向验证；不把 focused tests 当作完整 Release Gate。
4. 维护 task-isolated RDT 与 Architecture contribution；shared current 只通过 serialized
   promotion owner 更新，promotion-created diff 重新进入 Phase 2、task commit 与 Branch Review。
5. 完成 `guru-check-task` 的完整 semantic check，按实际 finding 重新进入相应 owner。

## Phase 3：提交、审查与合并

完成独立 task commit 前，对精确 staged paths、commit message 和预期结果进行当前对话确认；
提交后对完整 `origin/main...HEAD` 执行 fresh Branch Review，并依次经过 Publication、Finalizer、
PR merge 与 fresh main convergence。任一 scope、authority、content 或 base identity 变化都使
受影响 gate 重新入场。

## Post-merge Release Gate

合并后从 fresh exact candidate 执行 #332 要求的完整 pre-tag Release Gate，覆盖已合入
#311/#333/#339/#358/#361 的承接、clean throwaway、existing install/update/reapply、声明平台
入口、installed business-repository Publication/Finalizer 代表性链、secret scan、zero-residue
与 tag-pinned smoke。所有 mutation 分别经过其 owner 的 fresh gate 和独立当前对话确认，最终再
按顺序处理 annotated tag、GitHub Release 与 Issue #332 closeout。

## 停止条件

required gate 的 FAIL、SKIP、stale、cross-SHA、unknown 或 unmapped exit，以及历史 authority
被改写、shared-current writer 不唯一、scope 超出 #332 或 projection 无法从 canonical source
重建时，停止在对应 owner，不以动态 task metadata 或旧 evidence 代替 fresh judgment。
