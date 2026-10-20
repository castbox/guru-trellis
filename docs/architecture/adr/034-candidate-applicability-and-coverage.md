# ADR-034：按真实候选差额接续独立审核

状态：accepted。来源 Issue #637；predecessor Architecture `.104`、ADR-019/028/029/030/033。仅在独立 Phase2 审完整候选及拟写内容、原 owner expected-current 晋升后生效。原完整 authority 保留在 immutable Git `39169628f5f79cb48673eae96a36670e73f4dbbb:docs/architecture/`；后继为 `.105`。

## 问题与决定

既有固定候选/整合差额及工程事实采用规则，与finding修正后必须distinct fresh reviewer完整重审、后继阶段无新事实仍重建独立架构判断的条款冲突。首次完整独立审核继续；后继由实际未参与当前实现的合规owner审原覆盖、真实全部差额及受影响依赖，形成精确当前完整结论。原reviewer可以继续，替代者先核可获得证据，缺哪段补哪段，影响无法界定完整审。

原finding owner核修正闭合后，可以由同合规独立reviewer完成最终覆盖判断；这两个判断都必须实际完成。保留fresh_final_review wire值，显式限定为当前最终结论，而非强制更换身份和重复全部相同工作。首次implementation_required不等于passed覆盖，不能从refs、理解或phase制造pass。

工程事实、当前语义判断与Git/PR事实分开。采用原命令需核定义/版本、输入/依赖、环境、工具链、参数与期望；缺失/变化/未知补命中检查。同树只刷新内容绑定，无关target不触发整合。Publication/Merge消费适用内容审核，真实审自身payload、Issue、候选和live资格。

## 精确替代与保留

只替代现行Branch Review finding lifecycle/promotion alignment中的“distinct fresh reviewer、closure reviewer不能做最终审核、必须重新完整相同审查”片段，以及Architecture独立入口中把后继身份/阶段本身当作重建原因的片段。保留首次完整独立、每阶段当前真实判断、当前candidate/predecessor、finding连续性、合法来源、原qualification与正式入口。ADR-028固定内容/真实Reconcile触发、ADR-030先晋升再最终Check/committed Review、ADR-033早期反馈非正式pass不变。

## 取舍、迁移与验证边界

直接修改现有Markdown、受控consumers和完整matching安装，不加public覆盖字段、账本、缓存、第二reader/phase/store或智能脚本。原公开结果、Git、当前正文和可核验原始命令不足时补真实审核/检查；便利不能替代证据。

MIGRATION-637明确旧完整安装固定/成套切换及原owner同Delivery恢复；不自动解释旧checkpoint、不制造空提交或授权状态。实际安装、Agent检错/差额、同构分阶段耗时、#636已交付组合和#638未来未验证边界由唯一Test记录。此决策接受不等于实现验证、Task Completion或软件Release。
