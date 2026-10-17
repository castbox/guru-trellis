# #575 S3 来源修复执行计划

当前PRD拥有要求，design D2是唯一规范处置矩阵；实际结果只写原RDT唯一Test。

## P1. 唯一Delivery Policy

策略为staged。已交付S1/S2和既有#578/#579整合保留历史事实；当前S3只独立交付source-only ownership读取修复、同失败点回归及isolated RDT delta。其出口可由实际下一tools操作直接消费，是完整准备任务中的独立来源修复，不等于整个准备完成。

当前入口为原tools合法rollback、原implementation owner合法rework到同key planning、Clarify no_change及Author requirements_revision→fresh candidateArchitecture→solution planning→Wording→finalArchitecture→Approval。展示当前三文档并接受后由原Activation记录Planning，再实施；旧Planning与旧工具结果均不成为新放行。

当前出口为R575-S3-01..04及A575-S3-01..03满足，经完整Check/TaskCommit/独立committed全范围Review后Refs-only交付。剩余工作由同Task原Completion/Creation建立下一Delivery：实际修复source的完整`.4`投影、四平台parity、A目标tools-only与B无旧归档样本三平台reapply、focused clean、真实stable3维护/targetnative/下一owner/同操作恢复/不兼容rollback、最终RDT及promotion前后fresh gates。整体Completion/Closure/Finish及软件Stage2边界不变，不提前创建新Delivery。

## P2. 唯一Docs SSOT Plan

策略delta_first，writer=`guru-maintain-requirements-design-test-ssot`。沿既有 `docs/requirements-design-test-contributions/575-release-preparation/` 五文件收敛当前修复的要求、机制、Test与双向trace，final Phase2前reconcile。Test区分原失败/真实rollback、临时候选module结果、正式当前source回归及尚未完成安装，不复制动态gate账本。

当前贡献保持draft，最终全量reconciliation/shared promotion留后续完整安装Delivery；首次完整committedReview后原owner按fresh expected-current晋升，晋升差额fresh Check/TaskCommit/完整独立Review。当前不promote，也不把本切片Review转给后续当pass。

## P3. 稳定执行顺序

1. 当前规划完整门禁及展示接受后原Activation；原根scope、S1/S2和B保持，不重做既有本地整合。实现worker按当前规划承担canonical validator和最小回归；main协调Docs与门禁，不覆盖并行工作。
2. 在原`_validate_repository`中按`validate_installed`条件读取installed manifest，不改变True/default验证、source校验或tools顺序。仅处理已资格根因，任何新owner/API/authority机制变化回原资格与规划。
3. 运行V1/V2，保留原失败同输入对照和default/True对照。临时候选结果可在真实依赖适用时采用并注明来源，但最终源码差额必须可核实；不为补正式安装在dirty source重试旧operation，不执行当前`.4`安装或data维护。
4. 原RDT owner完成当前delta，运行V3；fresh独立Architecture phase2和完整TrellisCheck后由guru-check-task判断当前source切片。正式安装缺口是当前policy明示的后续责任，不冒充已通过。
5. 原TaskCommit展示精确staging/subject/body并独立确认；独立完整BranchReview审查B→实际H及live origin/main...H，区分继承#578/#579和当前修复。当前无shared晋升；fresh publicationArchitecture/DeliveryReview审查独立source出口及完整剩余责任。
6. 原Publish与Merge分别展示精确远端对象/HEAD/中文Refs-only正文并确认。只有actual delivered进入WholeCompletion的剩余义务判断和原Creation；后续正式安装使用实际修复source的新operation，不能当作旧操作恢复。Finish、清理和软件发布仍由各原owner另行处理。

## P4. 最小可靠验证

| 编号 | 对象与入口 | 观察条件与边界 |
| --- | --- | --- |
| V1 | 原preset source-only ownership调用及定向回归；当前canonical validator | 正常source-only/installed manifest缺失样本不再产生installed-manifest读取错误；source schema/inventory/manifest/registry验证保留。原代码同失败点能复现，修复只消除该根因。 |
| V2 | 原ownership validator default/True路径及现有相关测试 | 缺失或无效installed证据仍有原错误；合法installed路径不退化。使用真实当前调用与最小正常fixtures，不造recovery/hash/state。候选module证据不等于正式安装，必须核验当前源码回归。 |
| V3 | 当前source/test/Docs/规划差额的语法、diff hygiene、真实secret scan；原RDT delta检查与适用source检查 | scanner覆盖实际适用变化bytes；无未审查告警/bytecode/sidecar。按#578先独立判断真实依赖/工具链/参数/期望与原始执行事实，受影响、未知、缺失、新义务才补跑；不读其他owner私有状态或复用旧pass/token。 |

原Fork lock和#578/#579完整来源继续保留，不机械重跑不受影响矩阵。当前测试失败先区分当前回归、不可分前置、环境与已证实无关历史，不放宽guard/timeout或换样本求绿。新修复source的正式tools安装、target自身native和下一actualowner、四平台/clean/predecessor/恢复证明由后续Delivery执行；缺失、FAIL或SKIP不算通过。

## P5. 保留与停止

旧operation及原恢复锚点保持原owner终态；当前不改其source/plan/preimages。Task2/session3、五规划历史、raw source、配置、peer/common pointer及未选归档保持原责任。新发现越出当前修复的机制先原资格，真实scope/authority变化回原Clarify；普通mapped re-entry不重复询问。

后续未完成责任全部留同Task，不新建产品workstream，不实现#577/#46、不改upstream/global/node_modules、不做业务/生产迁移或累计矩阵。本计划不记录授权、gate进度、发布清单或伪造正式安装成功。
