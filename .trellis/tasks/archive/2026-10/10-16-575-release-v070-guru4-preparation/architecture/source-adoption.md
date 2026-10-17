# #575 首来源切片的 Architecture 贡献候选

Identity：`architecture-contribution-575-source-adoption-v1`；状态：`candidate`；继承 `current-main-0.6.17-guru.93/active`、constitution `guru-trellis-design-constitution-v1` 与 change-contract v1。

本候选采用独立 Planning 判断的 `legacy_boundary_convergence`，沿 ADR-024、ADR-027、ADR-028、ARCH-INT-014/015；不新增 ADR。它不是 shared-current 晋升或已交付声明。

## 当前差额与职责

Before：canonical 已有 Task/Delivery 和独立维护能力，但正式锁与真实旧 installed 图尚未构成一次可正常续接的正式采用。After 的首切片目标：固定包含上游 #40/#43 的匹配 Fork 来源，保留 manifest `.3` 以满足原 maintenance source consumer，使真实 source/doc 增量能经既有切片门禁独立交付。旧 installed 图保留到真实成套维护，不把它称为最终投影。

整体迁移方案由 task design D3..D6 拥有。公共 Task/Delivery/session/binding与恢复仍归 Trellis；Guru tools installer与各private owners分别处理自身资产；当前完整旧 workflow承接首切片，目标native与下一实际owner验证后才进入新Delivery规划。不会从旧pass、旧status或路径猜新身份。历史交付由原Publish/Merge核验；delivered/pending acceptance先进入真实Completion，不跳过其evidence_pending。

## 项目 concern 的适用约束

| Concern | 本切片约束 |
| --- | --- |
| authority-binding | 整体Stage1来源、四层live README、source锁与实际构建绑定；切片不是release authority |
| constitution-binding | 复用既有独立维护和staged能力，消除当前正常采用循环；不新增状态/adapter/无consumer的artifact |
| boundary-and-decision | ADR-024公共模型、ADR-027维护边界、ADR-028固定内容基线保持 |
| owner-and-single-writer | 原Author/Approval/Check/Commit/Review/Publish/Merge/Completion各守职责，公共与private转换分开 |
| compatibility-and-exit | 旧完整安装只在真实依赖仍在时保留；原maintenance成功与目标native续接为退出条件，无永久双读 |
| gap-and-deviation | 不重开GAP006/008，不把来源采用当业务采用、完整矩阵或最终发布证明 |
| parallel-scope | 只处理同Task checkout与隔离样本；peer/common pointer和业务仓库无新增写入 |
| evidence-and-freshness | S1唯一Test位于`docs/requirements-design-test-contributions/575-source-adoption/test.md`，在实现阶段形成；历史结果不改写 |
| review-and-promotion | 首次完整committed独立Review后才由原owner晋升；新差额fresh Phase2/commit/全量独立Review |

## 长期承接与剩余边界

本切片的 durable 候选定位为 `docs/architecture/contributions/575-source-adoption.md`，由原Architecture owner在受审查promotion中维护。后续`.4`、实际转换/native与最终投影使用独立`575-release-preparation`贡献，不改写已晋升S1结果。原RDT owner拥有各切片的requirements/design/test与双向trace。

本文件没有运行结果、用户授权、当前PR/HEAD或动态发布状态。正式tools安装、Task转换、native下一consumer、最终`.4`定向证明、共享晋升和软件发布均由其后续真实owner与唯一Test承接，不能从本候选推出通过。
