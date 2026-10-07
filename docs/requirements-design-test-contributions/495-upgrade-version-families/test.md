# T495 版本系列升级增量验收

状态：reviewed_promoted（已审查升级与同源远端验收，successor authority `.75`）；accepted migration 验收已齐备；任务仍需晋升后门禁与正式merge/Completion/Closure/Finish。分组与最小矩阵见 generation 1 [implement](../../../.trellis/tasks/10-06-495-legacy-installation-upgrade/implement.md)。所有正式 tag 有来源/资产投影归属，每种实际迁移路径选代表；任务格式和状态独立横向覆盖，不以旧 generation 0 pass 覆盖本轮 runtime。

## 当前结果

| 场景 / gate | 实际结果 |
| --- | --- |
| FAMILY | 19 正式 tag 来源/hash 投影核验；G1..G8 真实旧 installer before → public零写入preview → actual `.3` upgrade → actual source-specific rollback → old get_context smoke 通过。 |
| 差异补测 | 真旧 G1 SSH origin receipt实际upgrade/来源rollback通过；G6 `.41/core.6.17`、G7 `.1` 配置、G8 `.2` current task 各 actual upgrade/rollback/smoke 通过。 |
| TASK / PLAN / DEV / MIXED | G6 真 before 的七项 lifecycle 场景全部通过（203秒）；planning/dev正式owner接续、current creator、非UUID/full/minimal、mixed inventory与dirty/untracked保留。 |
| PARTIAL / NEW-WORK | lifecycle 七项覆盖部分恢复、新任务/notes写入后阻止覆盖回退。24 package tests通过；public 暂停→新增companion编辑→解决Skill.new→resume成功→rollback返回business_work_since_migration，新bytes保留；独立committed review发现的core/workflow显式preserve路径已修复：两条actualpublic partial pause→新规则→再次resume_required→rollback blocked/newbytes retained通过。 |
| PRESERVE | G1 config.yml bytes/modes、业务dirty/untracked保留；custom companion 0640、unknown目录和私有config setting在upgrade/reapply/rollback保持。ordinaryreapply保留custom并报告canonical.new。custom Bash同样保留0640权限；原恢复点resume成功后actual rollback通过。 |
| LINKED / current control/session | 真实 `.2` C4→C3→Bind 正式 writer 生成 branch/resource/session；linked upgrade `.3`、current session_resumed、rollback `.2`、old session_resumed 通过，task/control bytes/modes、primary 与 common pointer 保持。 |
| DELIVERY | 原 `.73` PR195/merged诊断与固定a32旧正式writer构造作为历史来源证据继承：本轮不改旧writer、deferred处置或远端副作用；current task anchor和family选择不使其变为current gate。同一新Guru远端源ecd的deferred public/provider复验已完成，见下方REMOTE；不声称新payload/原始业务在途已验证。 |
| Fork | 本地469 CLI + 5 core tests、lint/typecheck/build/version/diff通过；独立全9文件review无P0..P3，45项独立定向验证通过。 |
| Formal dependency | [PR28](https://github.com/castbox/Trellis/pull/28)已合并为 `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c`，main CI `37647767799` success，OID/tree/parent/版本/精确本地build/live CI 来源核验通过。 |
| dogfood / projection | 最新canonical正式apply→逐个核验并消费6个本次generated backup→reapply/installed/drift通过；183官方files投影、9官方行为与9ownership tests通过。 |
| 回归 | 20 package、73 upgrade contract、11 platform inventory、2 companion helper tests通过。preset完整101项重跑100通过/1失败：fixture复制尚未同步dogfood产生backup；最终同步后该clean-fixture项单独重跑通过，未将失败的full run改称全套pass。 |
| REMOTE | 精确远端 Guru `ecd152add05dbeb6df1873f0917ca3a62914ca7a` clean source/bootstrap，正式Fork `.3` bin；public/source_locked/provider create-new→canonical精确bytes校验→同provider force、installed/reapply、真实来源回退与native deferred通过。详见下方精确来源结果。 |

## 来源结果归属

| 组 | actual extension / core / manifest | task路径 |
| --- | --- | --- |
| G1 | `.6.5-guru.1` / `.6.5` / schema1 | legacy转换 |
| G2 | `.6.5-guru.25` / `.6.5` / schema1 | legacy转换 |
| G3 | `.6.5-guru.25` / `.6.5` / schema2 | legacy转换 |
| G4 | `.6.5-guru.31` / `.6.5` / schema2 | legacy转换 |
| G5 | `.6.5-guru.37` / `.6.15` / schema2 | legacy转换；tag不等于extension |
| G6 | `.6.16-guru.41` / `.6.16` / schema2 | legacy转换；core.17另补 |
| G7 | `.6.17-guru.43` / `.6.17` / schema2 | legacy转换；.1配置另补 |
| G8 | `.7.0-guru.1` / `.7.0-castbox.1` / schema2 | current原bytes/modes保留；.2另补 |

各组receipt由对应旧installer生成，均实际写入升级与回退，最后旧runtime smoke通过。组明细与19tag归属由PRD拥有，本表只记录实际代表结果。

## 首次失败和恢复边界

- 独立 committed `11ef591c...168c80ef` review：core `AGENTS.md` / workflow preserve 的新增规则在未解决Skill冲突时再次resume后被rollback恢复前像覆盖；真实public样本复现，BR-495-PRESERVED-CORE-WORK在 `5d4282ff` 修复，finding owner closure及不同reviewer复审确认新字节保护成立。不变更此前G1..G8通过事实，不将该review称passed。
- 独立 committed `11ef591c...5d4282ff` 复审实际复现 BR-495-RECONCILIATION-ROLLBACK：仅消费必须的canonical Skill `.new`、无新业务工作，成功resume后仍误阻止rollback。当前候选将必需package/overlay协调保留为managed，复用原business-before锚点；25 package回归（Skill/overlay子场景）及actual public暂停→仅canonical协调→upgraded `.3`→rolled_back `.2`通过，恢复旧定制bytes/modes。core/workflow实际暂停新工作保护再次通过；修复提交 `02da7d99`；closure于 `6cd766dd` 完成，最终完整复审通过；远端同源验收未完成。
- `02da7d99` 的 closure 和完整复审实际发现 BR-495-UNRESOLVED-SKILL-WORK：未消费canonical `.new`，暂停中新加Skill偏好，再次resume仍失败后rollback丢失新增字节；不将该提交称review通过。当前修复复用既有preimages及同一required projection，在restore前仅允许旧bytes/mode或canonical迁移bytes与旧/installer source mode，其它新增内容阻止回退，无新锚点。26 package及2helper通过；Skill/overlay各canonical-only和new-work四格actual public验收通过，另有companion新工作与canonical Skill协调组合仍blocked并保留新bytes。修复提交 `6cd766dd`；finding closure与不同reviewer完整复审已通过，正式 public Branch Review passed；该 pass 不覆盖知识晋升 diff。

- Fork完整CLI首次1884通过/1 ENOENT：工作树未初始化marketplace子模块；未声称全套通过。
- Preset首轮101项/2失败：版本期待仍为`.2`（修正`.3`后单项通过）；missinghash reapply的package conflict在独立重跑未复现。首次单项从scripts cwd运行temporary lifecycle不可用，改repo root后通过。
- dogfood首次apply生成46个已核验HEAD前像`.bak`，逐个消费后reapply与零sidecar通过；后续candidate configownership fix的一个backup按精确两行diff消费。
- 最新preset完整101项/1失败因dogfood未同步；最终apply的6个backup已核验为本轮旧生成副本并消费，reapply零sidecar，clean-fixture重跑通过。
- 正式lock切换首次101项/1 failure/38 errors：inventory到`.3`但schema/validator仍为`.2`，在preset写前阻塞；补齐常量后ownership检查通过，原custom Bash样本从same recovery恢复，不复制首轮pass。

没有真实业务安装、正式Guru tag/Release或完整累计多平台Release矩阵的通过声明。本地贡献已由 `11ef591c...6cd766dd` 完整独立复审及正式 Branch Review 接受并晋升 `.74`；晋升 diff 必须 fresh Phase2/commit/完整复审，测试不替代 gates。

## 精确远端来源与修复后验收（EVD-051）

来源为 [PR498](https://github.com/castbox/guru-trellis/pull/498) 的远端 Guru `ecd152add05dbeb6df1873f0917ca3a62914ca7a`，fresh fetch clean checkout/正式bootstrap；正式 Fork `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c`、main CI `37647767799`、CLI/core `0.7.0-castbox.3`，运行正式 `packages/cli/bin/trellis.js`。目标 extension `.7.0-guru.3`，升级均 `unverified=[]`。后继文档 HEAD 不继承“已重跑”声明。

| 场景 | 修复后实际结果 |
| --- | --- |
| G1 / PRESERVE / REAPPLY / ROLLBACK | 真旧 `.6.5-guru.1/core.6.5` before，public preview零写入；source_locked升级/同源provider应用、installed/reapply零sidecar；业务/config/dirty/untracked/HEAD保留；实际旧版本回退与旧get_context smoke通过。 |
| native G8 / current TASK | 真旧CLI init/旧preset/task writer before，`.7.0-guru.1/core.7.0-castbox.1`、AGENTS无file decision；实际升级/installed/旧版本回退/旧smoke通过，current tasks bytes/modes保留。 |
| native G8 / PAUSE / NEW-WORK | 实际Skill定制preserve正常产出canonical `.new`，消费同源canonical bytes后新增AGENTS inside/outside/mode三格：inside/mode resume_required，outside upgraded；三者rollback均business_work_since_migration，新增bytes/mode与task保持。outside再current preset reapply/installed，零sidecar。 |
| native oldwriter / DELIVERY / DEFERRED | 新隔离root复用真实旧native writer nonterminal before；source_locked升级/installed通过；push_content及task/gate/session/plans/history bytes/modes、HEAD/refs保持；两旧Task正式public identity均unsupported_legacy_task，无新远端payload或伪造gate。 |
| 修复回归与门禁 | 31 migration package、2 helper与source/installed/drift通过；bdf4eb82、ecd152ad两修复closure，`11ef591c...ecd152ad`完整123路径不同reviewer独立复审及正式Branch Review passed，Publication Architecture current、Delivery ready；这些不覆盖本次晋升diff。 |

REMOTE初次e6ba7dcc：G1无新工作实际rollback误阻止business_work_since_migration，原因是preset合法追加AI-first原则块；G8和native deferred当轮通过。bdf4eb82修复原则块projection，但独立完整复审正常native G8默认AGENTS暂停新增偏好被覆盖（BR-495-AGENTS-MANAGED-PAUSE），该轮不是review pass。ecd152ad补齐所有AGENTS preimage守卫/精确core projection与全文回退资格；finding closure及不同reviewer完整复审通过，本节精确远端再次证明两问题关闭。原e6失败及本地早期失败保留，不改称网络或全套通过。

19 tag/G1..G8来源归属、lifecycle七场景与current linked等不变有效证据复用；上述精确ecd最小同源验收补齐MIG-495-01..12 accepted证据，不逐版本重复。ARCH-GAP-012可按本轮证据闭合；Issue仍OPEN，merge、Completion、Closure、Finish各自正式owner/gate另行执行。晋升diff须fresh Phase2/commit/独立完整review；软件Release、真实业务安装、业务原始在途及完整累计矩阵未执行。此前full-suite失败与单项恢复边界继续有效。
