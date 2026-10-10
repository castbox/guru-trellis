# #383 因果完成语义 Architecture contribution

Identity：`383-causal-completion-semantics:phase2-final-v2`；状态：`reviewed_promoted`；Task locator：`.trellis/tasks/10-10-383-causal-completion-semantics`。当前状态为文末 committed review 与 expected-current promotion；promoted identity 为 `current-main-0.6.17-guru.80`，preimage 为 `.79`。下列 Planning/Phase2 段保留当时事实，不替代晋升后 fresh gates。

## Authority 与候选绑定

Guru contract：`guru-maintain-architecture-baseline:2.0`；baseline：`docs/architecture/README.md` / `current-main-0.6.17-guru.79` / active；expected current 同为 `.79`。Constitution：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / current。Change contract：`docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`；concern set：`guru-trellis-architecture-change-concerns-v1`。

长期 requirement/design 导航为 `docs/requirements/README.md`、`docs/design/README.md`。必要增量约束来源为 live Issue #383 `2026-10-10-r9` §5/§7：canonical 共同语义文件唯一拥有共用维度与 disposition 适用语义，各既有 owner 分别引用并判断，不重建 Delivery/Completion 图。设计对象为 task `design.md`，精确 SHA-256：`2f4d830f49ee65fb4f8f96b4ae110d39f30b036d3301b3b40ecef4b217e05a7a`；它不是 compliance authority。

## 独立判断与职责因果

Impact 为 `architecture_impact`，唯一 path 为 `target_native`。当前 root owner 合同只说明 #383 未来共同语义边界，完成维度尚无可复用共同正文；设计新增一个真实供 qualification、Planning、Check、Branch Review、Delivery Review、Completion 与 Reconcile 使用的 authority。若删除该正文及共用职责，各 owner 只能再次独立定义相同 disposition，不能满足唯一语义来源合同。这个共享 Markdown 边界有当前消费者，直接支持职责隔离与可维护性，符合 `minimum-necessary-complexity`、`cohesion-change-isolation` 与 `concept-semantic-completeness`，无需引擎、wrapper 或跨阶段 DTO。

共同 spec 单独拥有维度/disposition 的适用语义；root owner 继续拥有候选准入；各 stage owner 继续拥有本阶段 evidence sufficiency 与 route；Completion 保持 whole-task 唯一完成判断，Closure 保持实际 source Issue action-set ownership。Delivery 的一次 merge 仍不推出 Completion；未知 production effect 可以在独立 slice 交付后由原 Completion evidence_pending/refresh 承接。保持三项 Delivery evidence slots 和两项 Reactivate slots，避免新增 global causal store。Installer 只新增受管 source/target 映射，既有 hash/sidecar 执行不取得语义判断权限。

需要的 caller 适配是读取共同 locator 并替换 root 合同临时 missing-SSOT 说明；全局 workflow 只引用原 invocation/transition/consumer。旧说明在共同文件与 installed 投影可用后退出，不保留 stub、fallback、双读或第二共同正文。更直接替代方案就是当前设计采用的原 owner 引用单一正文；复制进各包或新增规则引擎都会增加无必要职责。

## 九项 concern

| Concern | 适用性与 Planning 结果 |
| --- | --- |
| authority-binding | applicable：绑定 current `.79`、Guru 2.0 与 current change contract；候选不改 shared current。 |
| constitution-binding | applicable：真实共用职责有现有消费者与 §5/§7 依据；没有 future DTO、缓存或扩展接口。 |
| boundary-and-decision | applicable：ARCH-DOM-035 / ARCH-INT-038 / ADR-020 与 ADR-016 的准入/阶段/交付/完成分工保持，唯一 target_native。 |
| owner-and-single-writer | applicable：canonical spec writer 拥有共同正文；原资格、阶段、Completion、Closure owners 各自单写判断；Architecture/RDT 原 owner 串行晋升。 |
| compatibility-and-exit | not_applicable：公开 I/O、exit、schema 与证据槽保持；没有新 legacy adapter、dual-read 或 migration。临时缺文件说明由正式引用替换。 |
| gap-and-deviation | applicable：ARCH-GAP-006/008 的闭合保持，不重建 gate aggregate 或跨 owner authority；不关闭 Release/业务验证缺口。 |
| parallel-scope | applicable：只允许 task-owned candidate/contributions 和受影响 canonical owners 的隔离修改；禁止并行改 shared current、其它 task 或 GAP lifecycle。 |
| evidence-and-freshness | applicable：Planning 绑定上述 exact design bytes 与现有 consumer/runtime 事实；实现行为、安装与 native eval 还未证明。 |
| review-and-promotion | applicable：本次仅 reviewed_candidate；后续 fresh Phase2、TaskCommit、独立 committed full-diff review，expected-current promotion 后再重新 gates。 |

## Project check 与后继 consumer

亲自按 `guru-trellis-architecture-convergence@1` 执行 Planning 语义检查，descriptor 为 `guru-trellis-architecture-convergence:repository:1`，entrypoint 为 current change contract；rule refs `ARCH-GOV-006..009`，decision refs `ADR-005` / `ADR-009`，GAP refs `ARCH-GAP-006` / `ARCH-GAP-008`。Planning result 为 applicable/blocking/pass：计划保留唯一 authority、writer、path、路由与 promotion 边界，无发现的职责扩张、新偏移或 closed-GAP 重现。

ADR 不需要：本设计实现 current ARCH-DOM-035/ADR-020 已明确留给 #383 的共同语义责任，遵从 ADR-016 现有完成图，不改变 architecture decision、原则例外、GAP lifecycle、owner/single-writer 或 compatibility exit。实现中若出现这些实质变化须 fresh re-entry。

下一直接 consumer 是当前 Planning owner；此 contribution 的长期 consumer 是后续 Architecture committed review 与 expected-current promotion。Promotion 仍 required；committed review pending，未定义 promoted identity。唯一实际结果将由 RDT contribution 的 `test.md` 承接，不在本文复制 suite 历史。

未验证：共同 spec 实际正文、各 owner authoring/eval、源/installed/platform parity、installer apply/reapply/update/sidecar、新实现 wrapper 行为、生产或外部效果。Planning pass 不表示这些已完成；完整多平台 Release matrix 与业务生产安装仍由专门 owner 承担。没有产品修复、promotion、Git/GitHub mutation 或授权存储。

## Fresh independent Phase 2 assessment

本轮以仅含执行约束和 locator 的独立 prelude 进入，完整读取已安装 Architecture skill/contract，先读 constitution、current `.79` baseline/change contract、实际 canonical diff 与全部 changed/untracked 候选及 unchanged consumers，形成职责判断后再读 task 与上述 Planning contribution。最终稳定候选重新核对；精确 freshness 只保存在本轮 private invocation，不在本文写自引用 digest。必要需求 fresh 来自 live #383 `2026-10-10-r9` §5/§7。

Before：ADR-020/ARCH-DOM-035 已分离 root 候选准入和阶段完成，root contract 留待 #383 提供共同正文。After：一个 canonical causal spec 唯一拥有共用 evidence/disposition 语义；root、Planning、Check、Branch Review、Delivery Review、Completion、Reconcile 七个现有消费者读取 installed projection。共同职责有现行需求与直接消费者；删除它将迫使各 owner 重复定义 disposition。实际 impact 为 `architecture_impact`，唯一 path 为 `target_native`，状态为 `reviewed_candidate`。采用既有 owner 读取一个正文，未新增规则引擎、workflow owner、public schema/DTO/exit 或长期 causal store。

Root 保持候选准入；Check/Branch Review 判断当前阶段；Delivery Review 审 payload，Publish 执行；Completion 独占 whole-task 完成判断；Closure 拥有 source Issue action-set；Finish 承接 terminal bookkeeping。共同 spec 不取得 invocation、route、recorder 或完成决定。诊断/缓解可保留未知根因并按自身 accepted scope 判断；一次 merge 不产生整项任务完成权限。三项 Delivery 与两项 Reactivate evidence slots、merge_result/reactivation_anchor 保持。旧 missing-SSOT 说明由正式引用替换，无 stub、fallback 或双读。Installer 只新增现有 MANAGED_SPEC_PATHS 的 source/target 注册，继续使用受管 hash/sidecar 机制，不承担语义判断。

正常 C11 路径暴露原 Check projection 缺陷：AI 已选择 planning_stale/reapprove_plan，current_scope decision 保留原修复目标但要求补充 causal plan；原 projector 只保留 scope_change_required，导致 proposal_refs 为空并被既有 public schema 拒绝。本轮读取原实际 authoring/错误与 unchanged schema/consumer；最终修订仅在已选定的 reapprove_plan 中投影 current_scope 与 scope_change_required，clarify_requirements 仍只接受 scope_change_required。Python 不选择诊断或 route，不改变公开合同；必要修订在原 owner 的客观 projection 完成，旧筛选缺陷退出。

五项 constitution 在此发挥具体约束：官方 marketplace/preset/skill 扩展面承接成熟实践与适用性；单一共用正文和各阶段独占判断维持概念与语义完整性、职责内聚与变化隔离；复用原 owner/installer/evidence slots 满足最小必要复杂度；原临时说明和错误 projector 退出支持技术债务单向收敛，无无关历史债务扩张。

| Concern | 最终 Phase 2 判断 |
| --- | --- |
| authority-binding | applicable：Guru2.0、current `.79`、constitution/change contract 与最终候选绑定，shared current 未改。 |
| constitution-binding | applicable：共享正文有当前 requirement 和七个实际 consumers，无投机字段或未来接口。 |
| boundary-and-decision | applicable：ADR-020/ARCH-DOM-035 与 ADR-016 的准入、阶段、交付、完成分工保持，唯一 target_native。 |
| owner-and-single-writer | applicable：canonical 共同正文单源；各既有 owner 单写本阶段判断；Architecture/RDT 串行 promotion 保持。 |
| compatibility-and-exit | not_applicable：公开 I/O、schema、exit、consumer 未变，无新 adapter、dual-read 或 migration。 |
| gap-and-deviation | applicable：ARCH-GAP-006/008 保持闭合，无新增/恶化偏移或 closed-GAP recurrence，不关闭业务/Release 验证缺口。 |
| parallel-scope | applicable：候选仅含 task 隔离贡献、受影响 canonical owners 与生成投影，不竞争 shared current、其它 task 或 GAP owner。 |
| evidence-and-freshness | applicable：读取完整最终候选、原消费者及实际 native/distribution evidence，current invocation 绑定精确字节；生产与安装边界如实保留。 |
| review-and-promotion | applicable：当前 reviewed_candidate；committed review pending，expected `.79` promotion required，晋升 diff 后再次 fresh gates。 |

本轮亲自执行 `guru-trellis-architecture-convergence@1` 的九 concern 与 before/after 语义协议；descriptor/rule/decision/GAP refs 绑定上一节 current project authority。未发现新增或恶化职责缺陷；current-only、唯一 path 与单写保持。ADR 不需要：实现 current ARCH-DOM-035/ADR-020 已分配的共同语义职责，遵从 ADR-016 完成图，没有 architecture decision、原则例外、GAP lifecycle、owner/single-writer 或 compatibility exit 变化。

个人执行 Check runtime 与 Completion contract 定向套件合计 44 passed、17 subtests passed；source/installed package validator、dogfood drift 和 diff hygiene 通过。个人读取全部 32 个 latest native authoring/rationale 与原 wrapper 输出，核对 C11 reapprove_plan、C14 pending、C15 原 merge anchor、C16 generation1 refresh、C20 no_mutation 及 C21 实际 fixture 第一次/第二次 merge 后 whole-task 完成；结果文件保留 7 个历史失败，未以重试覆盖首次证据。个人读取 22 个声明平台 apply/reapply JSON，均 status ok、installed validation passed，errors/conflicts/sidecars 为空，并核对 changed installed/platform packages 与 canonical 字节一致。详细测试结果由 [唯一 Test](../../requirements-design-test-contributions/383-causal-completion-semantics/test.md)承接，本文不复制 suite 历史。

Eval host 只准备事实并持有期望结果，native owner 原样提交实际 authoring 到原 installed wrappers；最新 source/Git facts、非空 commit、实际两次 fixture merge、reactivation anchor 与实时 trace 均为 private test infrastructure，不扩大产品状态。上述证据支持本次语义与 transport 判断；fixture Git/生产观察不是远端 Delivery 或业务生产效果。

下一直接 consumer 是 Phase 2 Check；长期 consumer 为独立 committed Architecture review 与 expected-current promotion。尚未验证 committed review/promotion、真实下游 Delivery/Closure/Finish、官方 init/update 完整链、完整多平台 Release matrix、candidate 远端安装、业务生产安装或实际生产效果。机制或相关证据变化时须 fresh assessment，当前结果不跨候选字节复用。

## Independent committed review 与 serialized promotion

独立审查范围：`origin/main@ef83e6d61e3c35d966b1baf95ab4bcab8409e993...f7944544122309035bb30da4ab88b6fa442c986c`。先从 constitution/baseline/change contract、完整 95 paths 与 unchanged consumers 形成 Architecture 判断，再读 task narrative，亲自执行九 concern 协议与原 wrapper；实际结果为 architecture_impact/target_native/reviewed_candidate。随后 fresh normal/solution qualification 和完整 Branch Review 经原 recorder/checker/invoke 正式返回 passed，无 P0–P3 finding；不是 Phase2 结果复用。

原 Architecture owner 核对 current `.79` 与该 contribution identity 未变化，按 expected `.79` 串行晋升为 `.80/active`。新增 ARCH-CUR-053 / ARCH-DOM-036 / ARCH-INT-039 / EVD-056 只导航现有共同 spec、owner 分工、分发与唯一 Test，不复制认知正文。无新的 decision、原则例外、GAP/owner/compatibility exit，ADR 不需要；所有 `.79` snapshot、#382 contribution 和历史证据保持原对象。RDT 同步 successor `.80`，software axes、public API 和全局图不变。

本 owner 在 promotion 再次检查全部九 concern：authority/constitution 与 preimage 绑定；唯一 target_native；各原 semantic owner/单写与 parallel task isolation 保持；无 adapter/dual-read、GAP 关闭或恶化；current evidence 指向原执行对象；review/promotion 精确承接上述 committed range。Project-check 为 applicable/blocking/pass，无发现的架构 regression。本文状态只说明知识晋升；新产生的完整 diff 必须 fresh Phase2、TaskCommit、独立完整 Branch Review 后才进入 Delivery。正式 Delivery/Completion/Closure/Finish、软件发布、官方 init/update 完整链和业务生产效果仍待相应 owner 判断，不以本段冒充完成。
