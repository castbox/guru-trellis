# #575 S3 来源校验修复设计

## D1. 身份、内容范围与Architecture

当前PRD定义独立来源修复要求，整体根PRD及accepted scope不变。Task/generation/S3 UUID保持，固定B=`d3bfeae0d8dc9f350317e5919fbd7751c394834c`继续作为内容范围；现有`a417a46726d95d071835f38c2b972bf6d594d797`整合包含#578/#579及其终态归档，是已完成来源事实，不重新Reconcile或追赶main。未来实际H和PR目标仍分别审查，不能用整合事实代替本切片Check。

fresh独立candidate Architecture依据baseline `current-main-0.6.17-guru.94`、constitution `guru-trellis-design-constitution-v1`判断 `no_architecture_impact`：恢复既有validator的source-only读取边界，True仍验证installed；不改变tools/preset/manifest writer、source_locked、恢复、归档guard或公共合同。此处不建立ADR或shared Architecture变更，final_plan及后续stage仍由独立owner判断。

## D2. 唯一source-design disposition matrix

| 来源与原承诺 | 处置 | 落点 | 理由、影响与上游处理 |
| --- | --- | --- | --- |
| 整体R575-03/04、S3 PRD R575-S3-01：正常source==target工具路径可完成，installed校验不得削弱 | retain | D3；P4 V1/V2 | 修原validator条件读取而非改tools顺序、制造manifest或跳过验证。 |
| 原tools合同：source_locked只消费真实已提交clean canonical source，resume保持原source/operation/preimages | retain | D4；P1/P3 | 来源修复先独立交付，后续新operation消费；不换source恢复旧operation。 |
| #575 Stage1、整体R575-05/06：完整准备责任、独立切片可审查、Refs-only | retain | P1/P2及PRD第3节 | S3只完成来源修复及当前delta；所有正式投影、样本及最终Docs留同Task后续Delivery，不宣称完成。 |
| 旧S3 design D3/P1：本切片先全安装、再最终Check/commit | change | D4/P3顺序 | 新发现修复必须先形成committed source，原顺序循环；同Task独立来源修复→实际交付→Completion/Creation→完整安装，整体约束不降低。 |
| #575及原S3：四平台parity、三平台reapply、真实stable3维护/native/恢复/兼容回退与保留责任 | retain | PRD第3节；P1后续责任 | 不把当前module回归替代正式安装，不迁移无关archives；A目标tools-only、B无旧归档样本普通reapply仍保留。 |
| #578/#579来源采用及ADR-029工程事实合同 | retain | D1/P4 | 两项来源保留；当前owner独立判断原执行事实真实依赖适用性，不读别的owner private证据或继承pass/token。 |
| 私有release Stage1：必要promotion前后完整committedReview；Stage2最终main冻结、remoteprovider/tag证明 | retain | D5/P2/P5 | 当前贡献draft；后续完整证据后晋升及fresh gates，最终发布重跑，当前修复不能代替。 |

本矩阵独占规范处置；PRD与implement不复制第二矩阵。整体requirement与外部来源未降级，无新增跨仓产品任务。

## D3. 原失败链与最小修复

正常tools-only操作在原owner退休old managed assets及installed manifest后进入preset。preset的`run_upstream_ownership_validator(validate_installed=False)`只应校验canonical来源，但`validate_upstream_ownership.py::_validate_repository`无条件`read_json(INSTALLED_EXTENSION_RELATIVE)`，把合法暂缺target manifest当作source错误。这是第一失败点；重复原source resume无法改变该条件。

修复限于同函数：只有`validate_installed=True`时读取installed manifest；False不触发该读取及其错误收集。原source schema/inventory/extension/registry与其校验保持，True仍走原installed读取和全部验证。无需新增状态、manifest writer、参数、fallback、恢复机制或异常吞掉分支。

因果验证使用正常source-only调用且installed manifest暂缺的同输入或等价sample；补default/True缺失或无效installed证据仍报错的对照。去掉修复时应重现原installed-manifest错误，采用修复后source-only继续；不能只看总pass数量，也不能把不同阶段的新错误说成安装成功。外部临时候选模块回归只是代码因果证据，正式source_locked安装仍待实际提交。

## D4. 来源修复与新安装操作分离

原tools rollback已经由原owner恢复旧`.3`安装及目标native/current，当前切片不再改旧恢复对象。新canonical修复会改变source token，因此禁止从修复source resume旧operation或重写其冻结输入。当前只在正常开发阶段改canonical代码与必要回归，原受管安装及Task/history/config/peer状态保持。

当前code/test/draft RDT经完整Check、TaskCommit、独立committed全范围Review与Refs-only实际交付形成修复source。后续由原WholeCompletion判断剩余责任，经原Creation建立下一Delivery；原tools owner使用实际clean committed修复source执行新的prepare/invoke。它是新操作，旧recovery不授权、不承载新source。当前不预写后续UUID/规划或创建资源。

## D5. Docs与整体收尾

原RDT owner只收敛既有贡献根的当前source修复delta及Test/trace，shared current不动。正式安装、四平台和隔离维护证据补齐后，最终contribution与shared promotion归后续完整安装切片；其首次完整committedReview后才必要晋升，晋升差额fresh Check/TaskCommit/完整独立Review。当前Review不能替代后续安装或promotion差额。

整体Completion继续检查PRD第3节全部责任；reference-onlyClosure保持#575OPEN，Finish与bookkeeping保留原owner。Stage2对最终main exact candidate重新执行远端provider、最终predecessor/tag/smoke/Release，来源修复交付不是软件发布。
