# Check 规划回退交接与恢复：Architecture contribution

Identity：`ARCH-CHECK-PLANNING-RECOVERY`。Task：775-check-planning-recovery / generation 0；Delivery：b548fca9-727b-4934-82e7-55afb662c6d1。状态：final_integration共享目标已写入并读回；正式promotion结果由原公开输出承接。Owner：guru-maintain-architecture-baseline；规划期候选正文writer：原Author；隔离完整目标及共享写入writer：原Architecture owner。

## 适用来源、前后边界与决定

需求authority为Issue775及[整体PRD](../../prd.md) R1/R2，行为与方案由[本批PRD](prd.md)和[design](design.md)第4–7节展开。适用before为Git `313d80215f65777fc70893a90c6d8dce8005d6dd` 中的 `docs/architecture/README.md`、constitution及change-contract。baseline identity为guru-trellis-architecture，constitution为guru-trellis-design-constitution-v1，change-contract为guru-trellis-architecture-change-contract-v1，required concern set为guru-trellis-architecture-change-concerns-v1。唯一change_path为target_native；决定由[ADR-CHECK-PLANNING-RECOVERY](research/adr-check-planning-recovery.md)承接。

before：Check无差别把scope_decisions投影为proposal_refs，非空时省略Author动作；planning_stale清Planning后普通入口再次要求它。6.0内容身份排除Task目录，原scope/plan不能由当前planning/空slots重建。

after候选：原Check AI选择scope分类、动作和路线；确定性输出在执行回退前完成验证。范围内reapprove_plan带具体actions交原Author；真实scope变化交原Clarify。原6.0结果的planning_stale专用rollback_binding保存回退后不可重推的原scope/plan/候选及规划evidence；独立恢复profile只读核同对象与当前内容，不重复rework或制造pass。旧无binding现场只从仍持有的原公共事实转换，缺来源保留blocked及原owner处理路线。

## 采用机制、替代与运行代价

删除恢复能力无法满足R2；继续使用普通_binding仍会要求已清Planning。仅依据当前scope=当前accepted_scope会接受普通后续scope修订，不能识别原对象。补造旧pass、新Task或第二事务账本均改变职责或扩大状态。

采用现有Check结果中的最小局部binding，唯一直接consumer是同Check恢复profile。首次planning_stale增加一次既有public Planning事实读取与原结果写入中的局部字段；恢复读取原结果和当前公共对象、三份规划字节及当前候选。无跨Task串行、锁、服务、长轮询、第二checkpoint或额外远端请求。binding随原Check结果生命周期退休，后继Author只消费actions。

原producer与受控consumer直接同步演进；旧结果转换不新增历史parser或双写authority。旧现场读取的是实际已保留公共query／精确Git对象；仅有当前状态不足以补造原来源。该决定的重新评估条件是accepted scope改变、旧事实来源不可用、上游rework保留字段改变、或原Check结果生命周期改变。

design第7.1节明确修复前现场的provider/目标顺序：先保留目标checkout的原HEAD、candidate、规划、tracked工具和业务字节，从目标之外的完整matching Guru provider公开Check wrapper使用既有 `--root <目标checkout>` 恢复。provider提供workflow/router、package、consumer及managed runtime；目标的Task schema2 / Delivery API1.0、C4和真实选择仍是身份与状态authority。目标缺兼容API或原来源时保留原诊断停止，不加载provider私有Task实现fallback，不新增身份环境覆盖、恢复状态或账本。

原Author/Clarify consumer承接恢复输出并进入当前重规划，确定不再复用旧结果后，原tools owner才按另行审查的写集成套采用目标工具。恢复不更新目标。先改tracked工具属于真实内容与candidate变化，不能补旧token或豁免差额继续旧恢复。此安排复用既有root/公开API，仅增加provider与目标的明确选择、兼容前置及顺序核对；不引入备用runtime或远程执行服务。

## 九项required concerns

| Concern | Applicability与本批承接 |
| --- | --- |
| authority-binding | applicable：Planning两目的及后续非Planning沿原合同；本贡献绑定上述before与原Task/Delivery |
| constitution-binding | applicable：涉及concept-semantic-completeness、cohesion-change-isolation、minimum-necessary-complexity、debt-one-way-convergence；理由是原结果必要绑定、同owner恢复及旧路径直接退出 |
| boundary-and-decision | applicable：Check→Author/Clarify交接、恢复拒绝条件及旧结果转换由本决定和design第5–7节界定 |
| owner-and-single-writer | applicable：Check判断/结果、Author业务规划、Clarify需求范围及Architecture/RDT晋升保持各自唯一owner |
| compatibility-and-exit | applicable：matching成套采用；旧现场由目标外完整provider先恢复未变目标，目标公共API仍单写authority；原consumer承接且不再复用旧结果后采用工具。旧无binding结果在同profile使用现有因果事实转换，不保留旧非空refs→Author路径或私有API fallback。 |
| gap-and-deviation | applicable：拟关闭Issue775两处有证据缺口；未主张关闭其他GAP，无新增或恶化的authority偏移；缺真实来源的现场保持未恢复 |
| parallel-scope | applicable：本Task仅写自己的规划/贡献及后续所需canonical变更；禁止改别人的Task/contribution或提前竞争共享current |
| evidence-and-freshness | applicable：V1/V2观察原入口、真实consumer和已回退状态；旧现场命中外部provider/root、未变目标及tracked工具改变后的旧恢复拒绝。最终Check/Review绑定完整actual after，局部fixture不代表完整升级链，计划不是执行证据。 |
| review-and-promotion | applicable：原独立Phase2已返回reviewed_candidate，原Check已candidate_checked并合法回implementing。本方共享目标已由原owner整合/readback；正式promotion与actual-write applicability在双方知识写入完成后的整体after上执行，不把候选Check当最终Check。 |

## 拟维护目标与single writer

原Architecture owner仅在合法final_integration维护 `docs/architecture/04-integrations/distribution.md` 的“公开执行资料与原生产能力”完整单元，替换旧Check非空refs说明并整合本次恢复职责；新增必要ADR目标 `docs/architecture/adr/check-planning-recovery.md`，不改共享ADR index或baseline根导航。本Delivery的完整实现与隔离拟写已共同通过原独立Phase2及candidate Check；原owner已在该合法边界完成本方共享目标写入/readback，隔离拟写保留proposed来源。原RDT owner在其自身三层完整单元维护R713/D713/T713关系；本贡献不代写其authority。

| Shared target及精确范围 | 唯一隔离完整拟写 | 组合与晋升边界 |
| --- | --- | --- |
| `docs/architecture/04-integrations/distribution.md`，从唯一 `## 公开执行资料与原生产能力` 标题起至文件末尾 | [完整单元](proposed-architecture/distribution-public-execution.md) | 以本贡献固定before的该完整单元作比较；最终整合时读取live完整文件，保留标题前全部有效单元，并语义合成该单元的真实并行变化。只替换这一完整单元，不把前文历史观察复制到隔离delta。 |
| `docs/architecture/adr/check-planning-recovery.md`，新文件全部正文 | [完整ADR](proposed-architecture/check-planning-recovery.md) | before中不存在该路径；真实目标若已存在，原owner先核实际内容及归属，不覆盖。原Author的research ADR继续作为proposed来源，不作为第二current。 |

两份拟写中的相对链接均按shared target位置解释，供最终整合后的正文使用；不是从Task目录另建authority导航。新增ADR及MIGRATION-775关系已纳入原独立完整候选审核。共享distribution按已审完整单元整合，标题前全部字节保持；新共享ADR由原owner在final_integration接受，并把观察截止更新为已发生的独立Phase2与candidate Check。隔离proposals继续保留原proposed来源。原owner还须按双方知识写入后的actual after执行正式promotion及实际写入适用性判断，再交implementation重绑；未声明后续最终Check、committed Review或PR结果。

允许并行维护其他独立单元。触及同一实际目标时，原维护owner读取本Task before、完整proposal与live目标，保留双方有效条件；真实冲突返回原owner，不用Git自动合并证明语义一致。expected-current identity在实际晋升前按live完整目标绑定，不在规划预填通过。

## project-check与证据边界

项目descriptor为guru-trellis-architecture-convergence:repository:1，check id/version为guru-trellis-architecture-convergence / 1，result contract为guru-project-architecture-check-result-2.0。原独立Architecture owner按change-contract执行当前语义project check并在原调用结果记录，不由本文或脚本生成通过。

design第8节V1–V4及implement第3节保留规划时的验证合同，不因知识写入变成执行证据。截至本次final_integration，原独立Phase2与candidate Check已对同一完整候选给出实际公开结果，原Check已合法回implementing，本方共享目标已写入/readback。具体实现、installed及测试事实仍从原测试定义和实际结果读取，历史失败保持原观察。正式promotion、after重绑及最终Architecture/Check、TaskCommit和完整committed Review继续各由原owner完成。PR发布、merge、业务恢复、生产效果和Release仍是不同事实。
