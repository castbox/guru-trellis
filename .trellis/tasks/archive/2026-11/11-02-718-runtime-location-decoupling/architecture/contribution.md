# #718 Architecture contribution

状态：历史候选快照（Planning与晋升前候选阶段）；identity=`architecture-contribution-718-runtime-location-v1`；TaskId=`718-runtime-location-decoupling`，generation=0，Delivery=`a12847c3-5f1e-4e72-9300-fca42bcf9e43`。适用before为main `610a810d45bb30173906d55c77709389adf1cf31`。当前baseline identity=`guru-trellis-architecture`，constitution=`guru-trellis-design-constitution-v1`，change contract=`guru-trellis-architecture-change-contract-v1`。change_path=`legacy_boundary_convergence`。

本页固定记录规划与晋升前候选；下文的candidate、未晋升和当前描述均属于该阶段，不报告后续晋升或交付状态。当前生效定义见 `docs/architecture/01-current/runtime-location.md` 及其必要关系。

本贡献承接原D1设计，不构成第二需求或完成台账。改变两个现有职责组合：环境自动指针从唯一启动前置收敛为可替代解析hint；明确Git对象只读来源与有副作用Sync分开。保留共享identity、真实显式类别、锁定依赖/真实wrapper验证、source-loaded单目标维护、公共Task模型与正式阶段资格。

| Concern | 当前候选中的适用判断 |
| --- | --- |
| authority-binding | Direct Source为Issue #718；原baseline/constitution/change contract与固定B绑定；本贡献未晋升 |
| constitution-binding | 内聚分离环境/位置/Task/branch，复用原owners；以直接consumer证明hint/来源DTO必要，不新增全局偏好或Task authority |
| boundary-and-decision | 新ADR `runtime-location-decoupling.md`窄替代ADR-027 pointer必要性及ADR-006对只读来源的误用；实际Sync原约束保持 |
| owner-and-single-writer | bootstrap单写环境选择，Git owner单写明确对象事实，Discovery单写证据判断；官方Task/session原writer不变 |
| compatibility-and-exit | selection-v3.json单写，旧active.json原文保留且仅在新载体不存在时一次迁移；旧完整安装及工具rollback由原owner支持；新只读来源不冒充旧synced输出 |
| gap-and-deviation | 解决本次正常worktree/草案复现；不关闭无证据GAP，不新增pool/GC/telemetry或上游生命周期实现 |
| parallel-scope | 实现仅本718checkout canonical和Task-owned proposed；维护只写明确目标；peer工具/状态/实际选择保持 |
| evidence-and-freshness | 各阶段核自己的完整候选；before/after真实wrapper、Git链、维护/rollback与分发分别观察；当前没有实现或Release通过声明 |
| review-and-promotion | final_plan评实际方案/contribution；Phase2独立Architecture及candidate Check先审完整proposed，原final_integration再晋升；最终候选重新Check/Review |

完整当前定义与必要导航由原Architecture owner在final_integration合并到实际命中单元；不要求全局版本递增。ADR-027其余维护与数据兼容条件保留。RDT当前行为/设计/验证由原RDT owner完整单元承接，历史贡献保留来源而不成为当前执行拼图。

## 完整拟写与最终整合

本Task隔离 `architecture/proposed/` 下的完整目标为：

- `docs/architecture/01-current/runtime-location.md`：完整职责/机制/旧consumer与退出、代价和再评估条件。
- `docs/architecture/01-current/system.md`：保留完整原文，只明确ARCH-CUR-013归实际Sync及新只读单元关系。
- `docs/architecture/README.md`：新增上述identity的必要导航。
- `docs/architecture/adr/README.md` 与 `docs/architecture/adr/runtime-location-decoupling.md`：新决定和前驱窄替代关系。

上述相对链接按最终target解析；隔离正文current/accepted不是提前晋升。candidate阶段共享目标原文不变。独立Architecture与完整candidate Check通过后，原Architecture owner固定实际target、核before/proposed/live差额，才final_integration写入并逐个readback。原RDT的六个目标由其原owner另行晋升。实际after全部重绑再最终质量链。
