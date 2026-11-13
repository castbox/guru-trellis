# #815 D1：原 owner 内的 manifest 冲突恢复设计

## 1. 设计目标、需求承接与内容基线

本批承接 PRD DS815-01..04、DAC815-01..05，覆盖整体 R815-01..06。development baseline B=cb8b4ce349b54cd832ff5b8f72602c5a721ce875，来源为 Intake 选定固定 Git object；Planning H0 同 B，未来实际 H 由原 constructor 构造。PR target main 不代替 B。

原独立 Architecture candidate_assessment 正式返回 baseline_current/no_architecture_impact，baseline identity=guru-trellis-architecture，constitution identity=guru-trellis-design-constitution-v1。其 authority locators 为 docs/architecture/README.md、docs/architecture/00-foundation/design-constitution.md、docs/architecture/06-governance/change-contract.md。该结果允许现有职责内展开，不证明实施或安装通过；Wording后仍需原final_plan。

## 2. 当前系统、边界与目标差额

tools preview/prepare 的旧 inventory 通过 guru-upgrade-installation/runtime/owner.py 的 old_manifest 先 json.loads 现存 extension.json。正常 Git 冲突标记不能作为 JSON。原 tools 已有旧 provenance/hash、逐路径 preserve/replace、installer 和 frozen plan resume/rollback；原 Reconcile 已有 resolved tree/parent 和自然 dirty metadata 例外；原 Publication 已有 retire_completed。

差额是上述现有能力间缺少公开有界接续。选择直接增补原 Markdown 与定向组合验证，不改 parser、validator、schema、dispatcher 或 owner。不要求无关Task迁移；D1没有前序。

## 3. 来源设计处置（唯一）

| 来源承诺 | 处置与设计落点 | 理由与影响 |
| --- | --- | --- |
| Issue815要求1：固定已生成完整manifest blob | retain；§6.1 | 合法旧安装前像只为原inventory读取，不新增恢复owner |
| 要求2：原provenance/hash、逐路径判断、installer生成 | retain；§4、§6.2 | 不改hash、不拼接manifest；最终字节由组合canonical生成 |
| 要求3：同身份与自然dirty task.json | retain；§6.3 | 原resolved exception不扩大到其它metadata |
| 要求4：原retire_completed、unknown先恢复 | retain；§6.4、§7 | 不手删事务，不丢公共facts，不重放未知mutation |
| 验收：正常两分支到最终组合安装/验证/resolved | retain；§8 | 原writer产生真实输入和状态，fixture不修补待测输出 |
| 兼容边界：matching source、受管同步、原门禁 | retain；§5、§7 | 原I/O不变，无新状态、ledger或通用框架 |

全部是原承诺的具体落点，无change/reject，不需新上游需求处置。

## 4. 模块、职责与设计取舍

- Reconcile的SKILL.md/references/contract.md拥有真实Git冲突识别、固定H/blob的适用性和临时工作文件恢复。仅处理该managed manifest的正常冲突，其它冲突沿原owner。
- tools的SKILL.md/references/contract.md承接完整旧前像，基于真实组合canonical逐路径决定preserve/replace，核原pending后一次prepare并执行原invoke。旧hash缺失查原exact source，不用successor hash填旧事实。
- 原installer生成最终manifest和全部投影；不手写final manifest，不以target当前hash冒充previous-managed hash。
- Publication的references/contract.md明确同PR后继action中的完成事务退役及未完成原操作恢复，保持现有runtime行为。
- 新增source-private tests/managed_manifest_conflict_flow.py承载真实CLI/Core/installer、Git组合和原公开wrapper观察，不成为公共恢复脚本。现有三个package的test_contract.py只验证真实分发/入口关系，不能用正文自比较证明Agent行为。

取一侧为最终manifest会遗漏另一侧；手工合并hash使安装前像失真；直接apply不能代替tools语义判断且可能触发无关旧Task迁移。因此保留原owners并补其明确前置。无新兼容路径、wrapper、解析器或长期状态。

## 5. 接口与数据

无公共Skill id、profile、argv、exit、DTO、manifest或事务字段变化：
原Reconcile实际冲突处理→AI固定完整旧blob→原tools preview/prepare/invoke→原installer最终生成→原resolved executor→原implementation candidate/committed Review；tools结果只提供安装事实，不提供Check/full_review。
后继Publication action仍由原retire_completed校验并退役完成的旧私有事务，公共publication_result保持原含义。

H/blob/路径/工具计划是调用期事实，不新增tracked/ignored前像ledger、handoff字段或授权记录。source/target身份和原frozen recovery归属不变。

## 6. 状态、顺序、正常与失败流程

### 6.1 固定和临时前像

核同Task/Delivery/branch/worktree/PR、prior task H、MERGE_HEAD和冲突路径。用普通git show读取H:.trellis/guru-team/extension.json的完整blob及原mode，核其为H已生成且可解析的旧安装manifest。原冲突处理仅把原字节恢复到工作文件供inventory读取，不把这份临时旧状态作为最终stage-0候选。原source/provenance/hash保持。

H缺文件、前像不完整/不可用、来源含糊或有重叠未完成工具操作时回对应原owner；不构造假manifest。其它canonical冲突先按原职责解决，保留原merge/index身份。JSON暂可解析不表示整合完成。

### 6.2 逐路径tools与最终安装

从完整组合canonical调用原tools owner，选实际适用的source_locked或隔离local_candidate。trellis dirty不能声称source_locked；local_candidate保留formal_fork_source_lock未验证标记。对实际managed差异逐路径判断，expected_sha256绑定实际前像；不改旧manifest的hash。核原pending，审精确写集，一次prepare后以原frozen plan执行invoke。

本仓开发同步沿原local_candidate；形成真实canonical clean H后，正式采用经新的原source_locked操作。不能把开发结果改标正式或重写旧source/plan/ref。各写操作保留原独立副作用边界，未知动作先原恢复。

### 6.3 最终候选与resolved

原installer从组合canonical生成最终manifest和投影后，运行目标自身resolver、installed validator、native context、drift和sidecar/mode检查，核两侧canonical行为均存在。然后按原冲突处理将最终生成物加入resolved index，清零unmerged并构造stage0_tree/digest。核真实最终内容来源，不以installed_at单值判断临时前像已退出。

原resolved executor核H/new_base、正确父序和最终tree；仅保留原当前Task task.json自然dirty例外。其它无关内容按其原前置处理，不扩大allowlist。保持原B/key/PR，后续完整committed Review覆盖组合与受影响未改consumer。

### 6.4 Publication与失败

完成私有Publication事务由原新action的retire_completed校验并退役，保留公共发布事实；不手删transaction/gate。未知或未完成mutation先用原recovery核实际动作。tools失败/输出丢失复用原recovery_ref/frozen plan/preimages；不重新prepare或刷新rollback前像。

## 7. 恢复、兼容、迁移与集成

原public I/O、current-only校验和语义门禁不变。兼容说明直接增补原合同，无旧Task/schema转换、dual-reader或新recovery family。已有在途工作按原完整provider恢复；源码更新不表示已有安装已采用。

canonical变更经guru-upgrade-tools整体同步本Task checkout及实际所选Claude/Codex/Cursor投影，逐个处理真实sidecar/未知owned preimage，不手抄dogfood或改peer。README只定位原owner与采用入口，不复制内部步骤。

## 8. 验证设计

| ID | 场景/入口 | 独立观察和证据边界 |
| --- | --- | --- |
| V815-01 | R1/R2：真实Git两分支canonical、各自原installer输出 | merge实际产生manifest冲突，公开路径恢复固定完整blob；原字节/provenance/hash不改，不手工造hash/state |
| V815-02 | R2/R5：原tools公开preview/prepare/invoke及目标自身入口 | 原plan一次prepare，观察最终组合manifest及两侧安装内容；实际resolver/installed/native/drift/zero-sidecar通过，mock不能代替 |
| V815-03 | R3/R4：原resolved wrapper与Publication事务定向回归 | 核父序/tree/零unmerged、同key/PR事实、自然dirty metadata与无关Task/session/peer保持；provider fixture不证明live远端mutation |
| V815-04 | R1/R2：当前执行Agent实际加载修订后两owner正文并在fixture接续 | 观察Git前像→tools判断→最终候选的真实动作与缺口，正文扫描和driver成功不能证明AI已作判断 |
| V815-05 | R5：package/source/installed/声明平台/reapply/drift/mode | 原安装owner同步后验证实际target；字节一致只证明分发，其它native host/完整矩阵未验证 |

采用原tools recovery/native、Reconcile metadata和Publication transaction的适用覆盖，补managed manifest真实组合缺口。断言从需求和两侧canonical行为推导，不复制installer算法当expected。先定向回归与组合观察，再受管同步及实际目标验证；证据足够即停止。设施失败保留未证明项，不更改断言或加无关fault injection。

## 9. Canonical引用、本轮差额与实际未决项

精确原合同为Reconcile/tools/Publication packages。RDT单元增量由原RDT owner在实施后提交前整合/readback，目标见implement第6节；不写无关root/index。Architecture no-impact不生成空contribution/ADR。根因准入允许候选，不表示修复完成。

当前无需求/设计选择未决。实际matching Fork与CLI/Core pair是实施前置；发现真实公开入口缺口、owner/API变化或超出写集时回原Author/Architecture，不现场扩框架。以上验收尚未执行。
