# #495 版本系列升级 Architecture 候选

状态：reviewed_promoted（升级与同源远端验收候选）；expected current `.74/active`，successor `.75/active`，晋升diff仍需fresh gates。继承 `guru-trellis-design-constitution-v1`、`guru-trellis-architecture-change-contract-v1` 和 ADR-017。change path：legacy_boundary_convergence。

Before：`.73` 拥有固定 `.41` 代表样本的验收，不能据此拒绝其它正常系列来源。After candidate：同一一次性升级边界覆盖两个系列，按 manifest/ownership/task/control 实际差异分组；普通运行 current-only，不增加 writer、状态机或双读层。正式 Fork `.3` 来源锁/CI 已通过，Guru exact-source successor 远端验收已由精确ecd完成。

| concern | 当前设计判断 |
| --- | --- |
| authority-binding | #495 范围修正及 generation 1 planning；RDT contribution 独立于共享 current。 |
| constitution-binding | 复用官方 marketplace/preset 和既有 migrate；版本、安装、task 三轴完整且隔离；最少路径分组，旧 parser 单向退出。 |
| boundary-and-decision | Fork 拥有 core/task 确定性迁移；Guru 拥有来源/资产与 AI 处置；current lifecycle 仍是控制面唯一 owner。 |
| owner-and-single-writer | current bytes 保留，known legacy 在一次性边界转换；不造当前 gate 或另一 binding writer。 |
| compatibility-and-exit | family selector 明确迁移；unknown/custom/inflight 显式 preserve/deferred；source-specific rollback。 |
| gap-and-deviation | 旧固定来源验收不覆盖本轮新增路径；正式 `.3` lock 和分组实际预演已通过，EVD-051精确远端同源验收已补齐，GAP012 closed。 |
| parallel-scope | 仅任务贡献/ canonical / dogfood，真实业务只读；shared current 经 expected-current `.74→.75` 串行晋升；真实业务未写入。 |
| evidence-and-freshness | 正式 Fork lock/CI 与本地分组实际验收通过；完整结果由 RDT test 维护，local历史不冒充source_locked；EVD-051只绑定exactecd。 |
| review-and-promotion | `11ef591c...ecd152ad` 完整独立复审与正式 Branch Review passed；晋升 diff重新 Phase2/commit/完整复审。 |

Project check `guru-trellis-architecture-convergence:repository:1` applicable/blocking，审查单 writer/current-only、来源覆盖、真实 before 回退和证据边界。当前文档不是 Phase2 pass。决策补充见 [ADR candidate](./495-upgrade-version-families-adr.md)。
