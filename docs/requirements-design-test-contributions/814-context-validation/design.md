# #814 设计差额

适用 before 为 Git `ce4644392d1ed9815d59071388b9bff9978d1cee:docs/design/current/runtime-location.md`。原 RDT owner 将固定正文原样保留，并在末尾追加下方完整章节，形成唯一完整 after。未变正文不在贡献中复制。Architecture 继承该 Git 的 `docs/architecture/README.md` / `guru-trellis-architecture` / active 及 ARCH-RUNTIME-LOCATION；原独立 Planning assessment 为 no_architecture_impact。本次没有新 authority、持久格式或 ADR。

## 原生 context 来源采用与解析职责（#814）

本单元追加定义修订：`context-adoption-814`。来源为 [Issue #814](https://github.com/castbox/guru-trellis/issues/814)，适用 before 为 Git `ce4644392d1ed9815d59071388b9bff9978d1cee`。原 R718/D718、D760、D769 与 #813 条件保持；本节承接对应 Requirement 的 R814-01/02，实际观察由 T814 拥有。

### D814-01 / CON814-FACTS：原生解析内事实复用

原生 context/session 身份解析由固定 Fork 的 `session_storage.py` 拥有。一次同步 `RepositoryFacts` 解析内合并 toplevel/common-dir 查询，复用已经成功核验的工作区事实；既有分支拓扑缩小 Task 候选后，选中分支仍独立查询。全部 eligible peers、原 prunable 例外、唯一位置及必要拒绝继续执行。解析结束即结束该局部复用；Guru 不复制身份算法，不增加跨调用缓存、持久 store、锁或新 writer。

该选择减少正常多 worktree 下重复 Git 子进程，同时保留原身份条件。维护成本限于固定 Fork 来源、匹配构建、原工具投影与定向回归；正常规模计时由 Test 限定对象和环境。若 Task/C4/session 协议、拓扑条件、prunable 语义或原生入口变化，原实现与审核 owner 重新评估受影响路径。

### D814-02 / CON814-ADOPTION：原 owner 采用与接续

采用来源由 canonical `trellis/presets/guru-team/source/trellis-source.json` 拥有；CLI/Core 必须从该 lock 的同一精确 Fork commit 成对构建。版本字符串相同不证明源码相同。完整 Guru source 经原 `guru-upgrade-tools` 对显式单 checkout 做 preview、一次 prepare 和冻结 invoke，目标自身 resolver、installed/native 与受管投影分别验证；D718-03/06/07 与 D769 的 source/target、Task/session、peer/common 保持及 rollback 合同继续适用。

开发 `local_candidate` 保留 `formal_fork_source_lock` 未验证标记。实际包含新 lock 的 Guru commit H 形成后，从完整 H 及其自身 lock 重新 preview，再建立独立 `source_locked` 操作，workflow provider 固定 H；不能把开发结果改名为正式结果，或复用旧操作来替换其 candidate。若正式采用产生内容差额，原实施/TaskCommit owner 纳入真实候选并刷新受影响证据。

原 probes 仍真实执行且各为10000ms。外层等待结束不判定 executor 失败：先读原执行 handle 和原操作；仍运行则继续跟随，需要恢复则消费原 ref，保留原 operation/candidate/plan/preimages，不 reprepare 或放宽 candidate_mismatch。没有自然重现历史超时时，报告新样本和原 ref 接续事实，不把它们写成旧历史事务恢复。

该采用复用原安装/恢复 owner，无公共 API/schema/Task/session 迁移。只有来源配对、原公开 probes/恢复协议、实际写集或兼容义务变化时重评。必要 RDT 整合/readback 只建立 integrated_pending_review；TaskCommit 后的完整独立 Review 和后续交付仍各有原 owner。
