# T495 版本系列升级增量验收

状态：draft_candidate；本轮完整 task 验收未完成。分组与最小矩阵见 generation 1 [implement](../../../.trellis/tasks/10-06-495-legacy-installation-upgrade/implement.md)。所有正式 tag 有来源/资产投影归属，每种实际迁移路径选代表；任务格式和状态独立横向覆盖，不以旧 generation 0 pass 覆盖本轮 runtime。

## 当前结果

| 场景 / gate | 实际结果 |
| --- | --- |
| FAMILY | 19 正式 tag 来源/hash 投影核验；G1..G8 真实旧 installer before → public零写入preview → actual `.3` upgrade → actual source-specific rollback → old get_context smoke 通过。 |
| 差异补测 | 真旧 G1 SSH origin receipt实际upgrade/来源rollback通过；G6 `.41/core.6.17`、G7 `.1` 配置、G8 `.2` current task 各 actual upgrade/rollback/smoke 通过。 |
| TASK / PLAN / DEV / MIXED | G6 真 before 的七项 lifecycle 场景全部通过（203秒）；planning/dev正式owner接续、current creator、非UUID/full/minimal、mixed inventory与dirty/untracked保留。 |
| PARTIAL / NEW-WORK | lifecycle 七项覆盖部分恢复、新任务/notes写入后阻止覆盖回退。23 package tests通过；public 暂停→新增companion编辑→解决Skill.new→resume成功→rollback返回business_work_since_migration，新bytes保留。 |
| PRESERVE | G1 config.yml bytes/modes、业务dirty/untracked保留；custom companion 0640、unknown目录和私有config setting在upgrade/reapply/rollback保持。ordinaryreapply保留custom并报告canonical.new。custom Bash同样保留0640权限；原恢复点resume成功后actual rollback通过。 |
| LINKED / current control/session | 真实 `.2` C4→C3→Bind 正式 writer 生成 branch/resource/session；linked upgrade `.3`、current session_resumed、rollback `.2`、old session_resumed 通过，task/control bytes/modes、primary 与 common pointer 保持。 |
| DELIVERY | 原 `.73` PR195/merged诊断与固定a32旧正式writer构造作为历史来源证据继承：本轮不改旧writer、deferred处置或远端副作用；current task anchor和family选择不使其变为current gate。同一新Guru远端源的deferred public/provider复验归REMOTE剩余工作；不声称新payload/原始业务在途已验证。 |
| Fork | 本地469 CLI + 5 core tests、lint/typecheck/build/version/diff通过；独立全9文件review无P0..P3，45项独立定向验证通过。 |
| Formal dependency | [PR28](https://github.com/castbox/Trellis/pull/28)已合并为 `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c`，main CI `37647767799` success，OID/tree/parent/版本/精确本地build/live CI 来源核验通过。 |
| dogfood / projection | 最新canonical正式apply→逐个核验并消费6个本次generated backup→reapply/installed/drift通过；183官方files投影、9官方行为与9ownership tests通过。 |
| 回归 | 20 package、73 upgrade contract、11 platform inventory、2 companion helper tests通过。preset完整101项重跑100通过/1失败：fixture复制尚未同步dogfood产生backup；最终同步后该clean-fixture项单独重跑通过，未将失败的full run改称全套pass。 |
| REMOTE | 固定远端Guru exactsource的public/source_locked/provider actual执行尚待Guru候选发布；Fork成功不替代。 |

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

- Fork完整CLI首次1884通过/1 ENOENT：工作树未初始化marketplace子模块；未声称全套通过。
- Preset首轮101项/2失败：版本期待仍为`.2`（修正`.3`后单项通过）；missinghash reapply的package conflict在独立重跑未复现。首次单项从scripts cwd运行temporary lifecycle不可用，改repo root后通过。
- dogfood首次apply生成46个已核验HEAD前像`.bak`，逐个消费后reapply与零sidecar通过；后续candidate configownership fix的一个backup按精确两行diff消费。
- 最新preset完整101项/1失败因dogfood未同步；最终apply的6个backup已核验为本轮旧生成副本并消费，reapply零sidecar，clean-fixture重跑通过。
- 正式lock切换首次101项/1 failure/38 errors：inventory到`.3`但schema/validator仍为`.2`，在preset写前阻塞；补齐常量后ownership检查通过，原custom Bash样本从same recovery恢复，不复制首轮pass。

没有真实业务安装、正式Guru tag/Release或完整累计多平台Release矩阵的通过声明。知识贡献仍待完整独立committed review与受控promotion，测试通过不替代这些gate。
