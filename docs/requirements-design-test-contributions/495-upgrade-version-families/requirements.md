# R495 版本系列升级增量候选

状态：reviewed_promoted（本地可执行 slice，authority `.74`）；继承 immutable current `.73` 的 MIG-495-01..09。当前增量 authority 是 [范围修正评论](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6040798771)及 generation 1 [PRD](../../../.trellis/tasks/10-06-495-legacy-installation-upgrade/prd.md)。共享 current `.74` 承接本贡献；远端整体验收仍未完成。

MIG-495-10 拥有全部 `v0.6.x-guru.*` / `v0.7.0-guru.*` 正常安装的后继升级：19 个现存正式 tag 全部有来源投影归属，G1..G8 各实际迁移合同代表执行；未来同系列符合相同合同的来源进入同入口，不声称未存在版本已实测。release tag、extension revision、实际 core 与 exact source 分开核验。来源分组唯一明细见 PRD，公开操作投影见 MIGRATION-495。

MIG-495-11 拥有 current task/control/session 原字节和合法身份状态保留，以及正式 lifecycle owner 的实际接续；版本与 task 格式独立，仅 known legacy 转换。MIG-495-12 拥有真实来源的 backup/resume/rollback 与新业务工作保护，回退报告不再固定 `.41`。

MIG-495-02/03/07/08 的后继解释由上述增量扩展：定制、业务/spec/规划/history/journal 和无关 dirty/untracked 保留；缺旧 hash 从核验旧来源补齐，未知字节显式处置；正式 Fork lock 和同一远端 Guru source 的实际运行仍是完整验收条件。本地候选、旧 generation 0 pass、知识晋升均不代替这项证据。仍不自动完成任务、关闭 Issue、真实业务升级或发布版本。
