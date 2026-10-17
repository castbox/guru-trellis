# D1 执行计划

方案与源承诺处置以同目录 design.md 的唯一矩阵为准。本文件只拥有稳定执行顺序、Delivery Policy 和 Docs SSOT Plan，不记录动态发布状态或执行结果。

## Delivery Policy

policy 为 `full`。Task整体范围与本Delivery切片均为 R1–R5 / AC1–AC6；本Task无后续业务切片、无隐藏remaining work。正式来源、Plan2正常workspace入口及前驱版本轴须共同验证，才独立构成可采用的发布准备交付。

本Delivery的可交付条件是三项原实现差额、共享AGENTS限定修复与相应定向验证、真实source_locked/Plan2代表样本采用和长期Docs收敛完整。TaskCompletion随后核验全部准备范围、Delivery与正常归档；#575 Stage2 owner继续负责最终main exact-candidate、tag、smoke、Release和Issue关闭。这些发布动作不属于本Task remaining work，也不构成准备交付的先决循环。

## Docs SSOT Plan

选择 `delta_first`。当前RDT为 `current-main-0.6.17-guru.106/active`；阶段适用Architecture `.98/active` 仅以public locator/version/status继承。

唯一原RDT writer为 `guru-maintain-requirements-design-test-ssot`。隔离增量目录为 `docs/requirements-design-test-contributions/575-release-source-adoption/`，拥有manifest、requirements、design、test和traceability；需求/设计/策略按R1–R5与AC1–AC6形成双向trace。该目录不同于旧575-source-adoption；旧结果不改。

`test.md`是本次实际命令、首次失败/修复、采用结果和未验证边界的唯一长期owner；Task规划不复制执行报告。Phase2原RDT owner完成task_impact_sync及所需promotion，实际晋升在最终Check前，保持expected-current与完整受审差额。独立Architecture owner目前noimpact，不制造贡献或ADR；若实现改变Architecture边界，回原owner审查后修订。Check、committed Branch Review、Completion/Finish是该RDT结果的直接consumer。

## 实施与验证顺序

1. 核验实际PR52 commit/tree/parents、成功CI、matching clean Fork build/API。更新唯一lock、三个README和public-docs直接映射；MIGRATION577只追加当前正式采用事实与仍未验证边界。
2. 原位修正Plan2 Core定位。新增实际Node workspace/pnpm与npm布局测试、缺Core与错版本测试；沿原MigrationError处理普通失败。保持source/manifest/API/bytes/modes检查，不新增fallback、开关或持久化。
3. 原tools prepare在首次public apply前复用canonical Guru block renderer合成公开AGENTS唯一target，原public writer执行。同步原tools Skill/contract、SDK消费说明和canonical/installed投影。保留全部source/operation/candidate/guard、原rollback兼容检查和顺序；不修改既有失败样本或checkpoint。以等价新predecessor样本与真实prepare/rollback行为完成定向修复验证。
4. 修订四份私有release合同的predecessor取值，验证真实predecessor lock/manifest与`--before-cli`绑定，确认六输入和原verifier保持。执行四份byte parity及相关源码/语法检查。
5. 在隔离throwaway Git source，以当前完整canonical候选树精确bytes/modes生成clean本地验证提交并保留来源parent；正式Task分支不提前提交。用该source沿原source_locked tools与Plan2全inventory history_only/reapply实际验证代表隔离target。对比原失败inventory、保留文件、目标native continuation与下一consumer。验证提交仅用于本地工程证明，不是Task提交或远端candidate；不得用dirty source、伪checkpoint或partial Check取代门禁。证据完整后执行完整Check/TaskCommit，证明交付canonical bytes/modes与验证source等价；Stage2仍重跑真正final main远端SHA provider。
6. 先在隔离增量上完成 pre-promotion scoped Check、TaskCommit 与独立 B..HEAD 完整 Branch Review。该完整审查通过后，原 RDT owner 执行 expected-current 绑定的 serialized promotion，再对实际晋升差额完成 fresh Check、TaskCommit 与独立完整 post-promotion Branch Review。原 Architecture 当前 noimpact 结论保持；发生适用架构变更时，独立评估和晋升沿其当前原合同处理。零未解决 P0–P3 才进入 Refs-only PR。
7. 原Publish/Merge与wholeTask Completion/Closure/Finish完成本准备Task。完成后Stage2从bookkeeping合入后的main另冻结candidate；本计划不创建发布说明handoff或动态发布checklist。

## 最小可靠验证集

- `packages()`的真实Node解析测试覆盖两种受支持布局与两类普通错误；现有原Plan2 integration针对实际配对CLI/Core与合法旧inventory执行。删除解析修复应重新触发workspace缺Core路径错误。
- 共享AGENTS测试执行实际prepare/renderer与公开plan消费；真实正常upgrade→native continuation/下一consumer→原rollback分别证明工具、数据和恢复，block外内容与Task/session保留。旧失败样本不改，不用preview成功冒充rollback成功。
- 正式source validator核验lock/CI/build，原source_locked tools与Plan2真实采用证明配置可用，不靠字符串相等测试。
- source/installed package校验、registry/consumer图、四平台投影、ownership、三平台reapply/dogfood drift、sidecar和可执行mode按变更范围检查；原工具owner处理实际旧inventory和受管receipt。
- 私有Skill四份byte parity、predecessor自身manifest/lock值及原升级cell行为；当前与predecessorCLI必须分别绑定自身source。
- 真实secret scanner扫描全部适用变更文件，diff --check、递归bytecode/.new/.bak与未声明residue检查。触及非生成代码不超过3000行；缺失环境、失败或SKIP保持真实，不写为通过。

不执行累计完整多平台/native-host矩阵，不修改真实业务或生产。远端immutable provider、最终predecessor升级与tag-pinned smoke保留Stage2独立证明责任，不把本地准备验证提升为正式发布通过。
