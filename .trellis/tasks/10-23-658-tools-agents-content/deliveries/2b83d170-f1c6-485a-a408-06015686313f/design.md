# D1：AGENTS 最终内容维护设计

## 1. 设计目标、需求承接与内容基线

承接本批 DS1–DS5、DAC01–DAC05 和整体 R1–R8。development baseline B 为创建时已同步 main 的 319202beab79c7666ecdb855291bf117e43d407e；本批完整内容范围固定为 B 到最终交付候选。Planning H0 同为该创建起点；PR 目标为 main，后续远端推进不自动改变 B。

使用 guru-trellis-architecture、guru-trellis-design-constitution-v1 及 docs/architecture/06-governance/change-contract.md。独立候选评估判断 no_architecture_impact：原 Guru 内容编排、Trellis 公共写入/恢复与 Core receipt 职责不变，不新增贡献或 ADR。

## 2. 当前系统、边界与目标差额

现有 tools_owner.project_agents_target 在公共 prepare 后改 action.target，使公共候选校验拒绝。preset 后置写入也会使原公共 operation 与实际文件不一致。没有前序 Delivery。

目标为：调用方明确准备 AGENTS custom 内容；Guru 纯 renderer 在公共 prepare 前更新其中的 Guru 块；公共 prepare 原生冻结最终内容，返回后只读取和校验计划，不再改它。旧操作的恢复、Guru 资产编排、权限与 Task 隔离保持。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置 | 落点、理由与影响 |
| --- | --- | --- |
| #658 不预设新增 Fork 接口，先比较最小适配 | retain | 第4节：旧API缺少最终内容输入，后置写入破坏两层恢复；采用#57最薄新增处置，避免临时恢复/补偿桥 |
| #658 保留块外正文与 preserve/replace 语义 | retain | 第5节：明确custom选择，原旧action不被静默改写；renderer只改Guru块 |
| #658 原恢复绑定与旧操作合法处置 | retain | 第7节：原来源先回退旧失败操作，新来源重新准备，不迁移checkpoint |
| 原Skill prepare后修改target | change | 第4–6节：改为prepare前合成显式输入，保留公共返回计划原样；同步原合同和安装说明 |
| #566/ARCH-DOM-047 原公共writer与两层恢复 | retain | 公共最终内容/receipt仍由Fork维护，Guru不复制updater或公共rollback算法 |
| #656 固定原Fork来源 | change，条件依赖协调 | 在采用新来源前由原发布owner更新到#57交付的实际commit/CI，保留已发布前驱来源及版本轴 |

## 4. 模块、职责与设计取舍

- tools_owner.py：移除prepare后target投影；新增窄的纯输入合成，复制调用输入，要求唯一且明确的AGENTS custom处置。使用原installer renderer更新其content，不改变source snapshot和其它文件处置。读取公共能力声明并在prepare前核验。公共prepare返回后校验实际AGENTS target已包含正确块；skip等导致最终内容不正确时写前停止。
- 原preset renderer/installer：复用既有块更新与正文保留算法，不新建模板合并器。安装阶段对最终AGENTS幂等。
- Fork #57：仅增加AGENTS custom输入、必要guard内容和实际被Guru读取的能力声明；Core模板receipt仍表示Core候选。公共apply/resume/rollback保持原算法。
- canonical Skill、references及安装说明：说明显式custom输入、最终内容审核、原来源恢复及固定来源。通过原installer同步dogfood/平台投影。
- source lock：采用新Fork的实际commit/tree/parents与成功CI，不修改已发布tag/npm或伪造版本。

没有新增Guru公共profile、DTO、状态、持久化或补偿桥。旧公共API无法表达最终内容；绕开AGENTS校验或先改回文件再调用rollback都不采用。

## 5. 接口与数据

public tools_input.file_decisions 的新显式行由Fork拥有：path=AGENTS.md、source=实际原snapshot或null、action=custom、content=已审查的基底正文。Guru只在该输入content内渲染canonical Guru块，再调用公共prepare一次。需要更新上游模板正文时，调用方须明确提供已审查的最终基底；不把preserve/replace隐式转成custom，不复制上游模板渲染算法。

getMaintenanceContract.tools_custom_instruction={path:AGENTS.md,action:custom}由准备owner直接消费；缺能力在写前报告前置缺口。公共prepare冻结最终content/mode，其guard和receipt由公共owner维护。Guru只校验返回target的renderer幂等，不修改target、guard、hash或operation_id。

私有prepare仍使用原tools_input结构载体，公开install/resume/rollback I/O和typed exits不变。prepare结果进入原AI工具写集审核；输入计划不是用户授权或语义通过。

## 6. 状态、顺序、正常与失败流程

读取固定来源与目标 → 检查Fork能力 → 明确custom基底 → 纯renderer合成 → 公共prepare → 检查实际target幂等与公共preview → 原AI Gate → 原工具执行。

公共执行后进入原Guru资产/preset阶段，状态名称及原preimages不变。缺custom、重复AGENTS处置、无所需能力、skip导致旧块仍未更新或公共校验失败，均在目标写入前停止。后续编辑按原owned-path与公共later_work检查停止，不吸收为恢复基线。

## 7. 恢复、兼容、迁移与集成

同操作恢复只使用初次冻结plan和原来源，不重新合成输入。回滚先检查兼容性与后续工作，再执行原公共rollback及Guru资产恢复。普通重复安装是新操作；多个操作按实际覆盖关系回滚，不要求跨越后续工作回滚旧操作。

原业务失败操作先从未改变的原Guru/Fork来源回读检查，再按原rollback/退出合同处置；完成后使用固定修复来源重新准备。原数据/非目标指针保持。没有Task格式迁移，没有旧checkpoint转换，没有永久旧路径fallback。受支持旧公共action保持原义，新工具准备显式要求所需能力和custom输入；历史成功/失败证据保留来源身份。

## 8. 验证设计

- V1/DAC01：真实匹配CLI/Core测试，含旧块、块外正文、非默认mode；prepare无写入，计划/实际相同，preset renderer幂等，成功回滚原字节/mode。
- V2/DAC02：真实公共/preset组合正常恢复、重应用及回滚；追加真实项目编辑后恢复/回滚保护。旧双写诊断可保留原冲突预期。
- V3/DAC03：完整tools-only真实旧安装样本，比较业务数据/peer指针，目标自身installed/native运行。旧Task只返回受支持维护诊断，不迁移。
- V4/DAC04：原失败业务操作只读核验、合法处置、固定修复来源重装与目标验证；结果独立于V1–V3和发布证据。
- V5/DAC05：source/installed package validation、dogfood/平台投影、reapply/drift/sidecar、相关package测试及diff检查。不运行完整发布矩阵。

## 9. Canonical 引用、本轮差额与实际未决项

requirements/design/test沿#566既有正确行为与职责，执行说明由本次canonical Skill收敛；不改历史贡献中的既有验证结论。Architecture无决策变化，无新ADR或贡献。必要规范为本批PRD第7节列出的完整相关合同，实施前实际加载。

Fork远端交付与其main CI是固定来源采用前置；来源约束由#656原owner协调。业务原操作与安装是整体验收前必要事实。需求无未决选择；若实际机制/范围扩大，回原Author/Architecture，不直接增加新协议。
