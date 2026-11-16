# D1 Discovery 关联检索与草稿绑定设计

## 1. 设计目标、需求承接与内容基线

全量承接本批 PRD R1—R4/S1—S3/AC872-01。development B=e33ecf82d47fba88c95d74f298d55d0616cbb1a4，来自本次实际 Sync main 固定对象；Planning H0 同 B；PR 目标 main 与内容基线独立。内容范围为完整 B..最终H及本批dirty内容，由原candidate constructor固定，不截取单文件缩小已提交范围。

独立 Architecture candidate_assessment 已正式返回 baseline_current/no_architecture_impact：baseline guru-trellis-architecture，constitution guru-trellis-design-constitution-v1/current。authority 为 docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md。只澄清现有指引，无新owner、DTO、状态或共享写入。

## 2. 当前系统、边界与目标差额

现有4.0 schema及支持的同步来源合同已约束draft+非空issue_refs必须真实绑定；空issue_refs要求null。canonical_query对terms与issue_refs分别处理，原计分不同。原contract的无绑定示例只有source fragment，缺少此条件及关联线索的就地说明。已有普通装配恢复与公开三阶段执行器可用。首次D1无前序；目标差额限于原指引和必要行为回归，不改运行时。

## 3. 来源设计处置（唯一）

| 来源/原承诺 | 处置及落点 | 理由与影响 |
| --- | --- | --- |
| #872：关联线索保留用途、未绑定草稿可正确调用 | retain；§4—6原contract给现有字段表达 | 不丢线索、不伪造绑定 |
| #872：真实绑定一致性、原AI Gate与公共链保持 | retain；§5/7保持schema/runtime/DTO | 无接口改义、无迁移 |
| #872：不将terms局部通过当完整等价 | retain；§4/8说明计分差异与真实Agent证据 | 不预定权重/排名，不夸大证明 |
| #872：canonical与受管投影同步 | retain；§7原tools owner执行 | 保留Task/session/peer和用户内容 |
| #872：Discovery外沿验收、不外推下游 | retain；§8公开context_ready为止 | 不要求业务创建、全矩阵 |

无额外已接受技术方案；上述为来源约束，原schema条件也是必须保留的现行兼容边界。

## 4. 模块、职责与设计取舍

- canonical Discovery SKILL.md：短导航指向原contract的关联引用与绑定条件，不复制完整规则。
- references/contract.md：在无绑定草稿捕获示例原位定义draft条件；关联背景编号和主题使用现有terms，issue_refs为空、binding=null。说明terms保留检索线索用途但不保证与issue_refs同分同序。当前恢复表定位这种普通输入错误，原owner纠正完整输入后重跑record/check/invoke。
- tests/test_runtime.py：复用真实临时安装的Git-object recovery fixture，增加有编号/主题的terms、误填issue_refs字段被拒与纠正后terms/null保留、check/invoke真实context_ready的断言。fixture只供确定性合同证明，不冒充实际Agent。

采用直接修改原责任正文，不加wrapper、schema字段、兼容reader或自动更正。放宽schema不能解决AI语义混用；删除线索违反需求；仅改报错名称把失败转移给调用方，均不采用。保留原算法与一致性检查的当前消费者是Discovery记录/校验及后续Clarify，删掉它会破坏既有来源合同。原规则本身未被判错，因此无旧路径退休或新兼容负担。

## 5. 接口与数据

原pre_task/context_request和owner-result来源版本保持。正常未绑定草稿：change_input.issue_refs=[]，相关编号及主题位于terms，live_change.kind=draft、issue_binding=null；其余必需字段仍由原owner真实读取后作者化。真实同内容绑定走原issue_binding对象/来源事实。不把关联关系转成绑定，不手填derived query/history/result identity。公共输出仍为原context_ready DTO及唯一consumer。

无新增API、schema、持久状态、依赖、配置或数据迁移。示例只提供源片段/选择规则，不能预填完整semantic pass或producer transition。

## 6. 状态、顺序、正常与失败流程

调用方读原指引→判断本对象为新草稿且只有关联背景→保留编号/主题线索并按现有字段表达→真实Sync→Discovery语义读取/Gate→record→check→invoke→context_ready。字段装配误填发生时保留原schema_mismatch，不把null局部定义当普遍允许；原owner重读同一源/上游与当前schema，纠正完整输入，重跑原链。真实stale/未知内部故障保持原owner/stop。不新增状态机或恢复存储。

## 7. 恢复、兼容、迁移与集成

原同范围装配恢复保持，没有新操作或重试协议。公共I/O/算法/绑定校验不变，无迁移说明需求。原guru-upgrade-tools从完整当前canonical source以隔离local_candidate同步本checkout，匹配锁定Fork，保留Task/公共session/peer、用户指令；处理真实managed差额与sidecar。声明Claude/Codex/Cursor投影及dogfood drift/mode由原installer验证。此采用只证明本checkout开发投影，formal_fork_source_lock、外部业务及完整多平台发布矩阵不宣称通过。

## 8. 验证设计

- V1/AC872-01：原fixture的公开record入口提交该场景普通误填issue_refs输入，观察schema_mismatch；修正完整输入后观察关联terms与null保留，check/invoke实际context_ready。已有source/observation诊断回归保持，不加字符串自证。
- V2/S3：复用test_contract.py中现有绑定组合及schema回归；不放宽门禁。仅补实际受影响断言，不增对抗负例。
- V3/AC872-01：独立实际native Agent读取改后installed指引，根据仅有关联背景的新草稿意图自行组装并完成公开Discovery到context_ready；保留可核验的线索用途与最终输出，不由主会话预写其semantic pass。与fixture证明分开。
- V4/R4：最小source/installed package、原tools实际采用、目标自身resolver/native entry、声明平台投影及drift/sidecar/mode；Python内存语法、Task validate、diff check。源码通过不等于安装或Agent行为。

现有可复用fixture与原绑定回归承担确定性证据，实际缺口是V3与当前分发。观察足够即停止，不要求惯例旧新回滚、多轮样本或额外矩阵。设施失败保留原事实，仅解决阻塞必要结论的具体缺口。

## 9. Canonical引用、本轮差额与未决项

命中step-local canonical contract及其Skill导航；RDT docs/{requirements,design,test}/current/local-fix-intake.md的现有owner/字段恢复/精确package定义关系保持。原RDT phase2亲自判断no-change或真实差额，不造空贡献。Architecture候选no-impact不要求ADR；最终完整plan仍交同独立owner做final_plan。无用户未决问题。真实实施、Agent及分发结果尚未建立。
