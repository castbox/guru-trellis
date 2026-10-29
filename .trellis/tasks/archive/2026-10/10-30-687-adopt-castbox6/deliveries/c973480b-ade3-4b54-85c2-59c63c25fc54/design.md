# D1 固定来源采用设计

## 1. 设计目标、需求承接与内容基线

本方案承接 D1 PRD 的 DR1–DR5、DS1–DS4、DAC1–DAC5，覆盖整体 AC1–AC5。development baseline B 为 `7718d129bcb2055d77c7f43d0e4edca9aee313ea`；原 DeliveryProjection.content_base 以明确 development_base/observed_target 返回该 OID，D1无前序交付。Planning H0 同为该 OID；PR目标是 `main`，不是随远端推进重新选取的内容基线。

适用 Architecture 为 `guru-trellis-architecture`、constitution `guru-trellis-design-constitution-v1`、change-contract `guru-trellis-architecture-change-contract-v1`。独立原owner的修订后实际 candidate_assessment 返回 architecture_impact / target_native：本轮除来源采用外，需同步 ARCH-CUR-074、ARCH-DOM-057、ARCH-INT-060 中仍将 .5 写成当前来源的完整定义。原source lock与owner边界保持，没有新架构决策、兼容层或公共抽象；无需新ADR。final_plan审查实际隔离贡献及完整proposed单元。

## 2. 当前系统、边界与目标差额

当前 canonical lock 固定79a97ed6/.5；extension target/requires/tested 和三处原upgrade runtime精确版本检查仍为.5。本批将它们一起切换至已发布17015f987166f4106034f115d23212446f16d536/.6，保留Core/CLI精确配对。README当前来源段落与受管投影同步；已发布Guru .6的历史Fork .5配对保留历史身份。

没有前序Delivery。本批不修改上游stop源码、Guru PR-only workflow、公共API、Task/Delivery schema或安装所有权。上游Core与匹配Python是修复的实现owner；Guru通过原公开维护机制采用。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置与落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| #687：唯一来源锁和preset投影 | retain：第4节source lock与installer | 保留唯一来源authority，无新协议。 |
| #687：Core/CLI精确配对与严格source_locked | retain：第4/6节版本pin、干净Git source/build与原validator | 同步.6精确值；不放宽源码、API、字节/mode校验。 |
| #687：官方资产所有权 | retain：第4/7节公开tools-only与原preset | 官方文件只由Trellis公开维护入口更新。 |
| #687：旧profile合法停止、peer/history/selection/重试与Completion/Closure边界 | retain：第5/8节实际installed Core/Python回归 | 不增加新profile或成功/完成语义。 |
| #687：代表性隔离采用及分层验证 | retain：第6/8节真实tools-only维护与定向检查 | 不扩大累计矩阵与业务安装；没有change/reject承诺，无上游变更请求。 |

## 4. 模块、职责与设计取舍

- Source owner：更新 `trellis/presets/guru-team/source/trellis-source.json` 的commit、ordered parents、tree、CI与cli_version。真实parents为f83c646a8498b6aac8e4973de4d4d66a5e786bd3和07f31d83543581647ef7852d177c3dd16587049a；tree为08f5fc32d766ab2ccf04226846449b87ef95c5fb，mainCI40882919377。repository和pnpm@10.32.1保持。
- Manifest/maintenance原owner：extension target/requires/tested同步.6；`guru-upgrade-installation/runtime/{owner,delivery_upgrade,delivery_upstream}.py` 同步精确目标pin与原测试预期。直接修改原检查，不加版本fallback。
- Installer原owner：生成 `.trellis/guru-team/trellis-source.json`、extension和原package/selected平台投影；按原managed hash处理sidecar。dogfood若因历史Task迁移门禁阻塞，沿原tools-only维护或原安装owner的合法投影入口恢复，不批量改写历史Task，也不手写官方资产。
- Docs原RDT owner：维护687贡献与三个native-compatibility完整proposed单元，明确.6当前采用关系和历史.5观察；Architecture差额由本Author写入 `docs/architecture/contributions/687-adopt-castbox6.md`，配套目录的manifest和完整proposed三单元保留原定义条件；原Architecture owner在candidate Check后final_integration晋升。无需新ADR。

复用现有 `_prepare_clean_candidate_source` 和 `_upgrade_native_bootstrap_tools` 组织隔离验证。前者创建真实本地已提交干净Guru源码快照；逐项核对canonical字节和mode与本轮候选一致。记录实际local SHA，不宣称远端marketplace安装或新Guru发行。后者通过原source-owned preview→prepare→invoke执行真实source_locked维护，没有第二维护实现。

## 5. 接口与数据

唯一source-lock结构不变，仅更新固定事实。原 `guru-upgrade-tools(profile=install, dependency_mode=source_locked)` 接收明确source_ref/checkout和真实匹配Fork源码/build；原public maintenance API验证candidate后写工具资产，返回tools_upgraded且unverified为空。原精确来源失败保持失败。

stop仍通过已安装Core公共operation和Python `delivery.py apply/stop` 进入原阶段owner。输入是受支持历史路径保留的manual/local_commit key、合法role/owner和非空停止evidence；合法结果为stopped，匹配retry读回同一结果。没有新增API、字段或数据库迁移。

## 6. 状态、顺序、正常与失败流程

先核对Release/merge/CI→修改canonical lock/pins/docs→同步受管副本→运行定向静态与package检查→从精确Fork Git源码正常install/build，在成功后写原build marker→创建干净Guru本地snapshot→原validate-source→隔离已有目标原tools-only实际采用→installed stop/保留性与reapply检查→RDT/Architecture候选与Check→原知识owner final_integration晋升→重绑实际candidate和最终Check。

来源、版本、API或实际build不匹配时原validator阻止写入；安装冲突/sidecar沿原owner恢复并保留用户内容。stop的owner、phase、evidence错误仍由原public store拒绝；不将任何维护或停止结果写成Completion/Closure。

## 7. 恢复、兼容、迁移与集成

采用沿原tools-only recovery_ref和原投影机制；不扩张为全量Task转换。隔离目标维护前后比较Task/session/用户内容和peer工具指针的bytes/mode；保留原selection/history。真实目标不升级。历史已发布版本、证据及归档不回写。原source_locked clean-source前提保持；普通本地快照身份不等同远端发布身份。没有新兼容分支或长期双读。

## 8. 验证设计

| ID/验收 | 测试层、入口与输入 | 预期观察及限制 |
| --- | --- | --- |
| V1/DAC1 | Git/GitHub merge/tag/mainCI和Release四附件；实际Fork源码正常build | 精确17015f98/.6配对、parents/tree/CI一致；附件hash/CLI依赖一致。CI不替代安装。 |
| V2/DAC2 | source/installed package、ownership、canonical/dogfood lock和manifest | 所有当前映射.6、严格pin生效；历史Guru .6仍为.5。 |
| V3/DAC3 | 单个隔离目标，原tools-only source_locked preview/prepare/invoke | tools_upgraded、unverified=[]；实际installed API/bytes/mode匹配；Task/session/用户内容/peer保留。只证明本地匹配source采用。 |
| V4/DAC4 | 维护后的已安装Core/Python，对合法历史manual/local_commit样本公开stop | 两profile停止、peer/history保留、selection释放、匹配retry相同；空evidence仍拒绝，无Completion/Closure；不增加新profile。 |
| V5/DAC5 | 原maintenance测试、tools-only installer/source-contract回归、reapply/drift与sidecar | 原严格检查与投影恢复有效，sidecar逐项归属处理。非完整多平台矩阵、远端marketplace或业务验收。 |

## 9. Canonical 引用、本轮差额与实际未决项

适用完整body：`docs/requirements/current/native-compatibility.md` R630-03/05/06；`docs/design/current/native-compatibility.md` D630-03/05/06；`docs/test/current/native-compatibility.md` T630-03/06/07；`docs/architecture/04-integrations/distribution.md` ARCH-INT-014/060/063；原`guru-upgrade-tools/references/contract.md` strict source_locked；`.trellis/spec/preset/{installer,upstream-ownership}.md` 安装与所有权。当前差额是固定来源与原pin同步、具体采用/停止证据；实际Architecture贡献为 `docs/architecture/contributions/687-adopt-castbox6.md`，完整proposed目标为system/ownership/distribution中的命中单元；按原owner晋升，无新ADR。必要未决项无。实际实现若发现新边界或原计划不能承接，返回原qualification/Author/Architecture处理。
