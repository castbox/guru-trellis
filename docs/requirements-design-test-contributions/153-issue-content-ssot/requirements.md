# #153 Issue 内容需求增量

provenance=`source_confirmed`。来源为 [Issue #153](https://github.com/castbox/guru-trellis/issues/153) R1–R4、V1–V7、AC1–AC10。继承 RDT108、Architecture99 与 #154 来源保留边界；本贡献只定位责任，内容规范由原 Clarify package 单写。

| Requirement / Behavior | 来源 | 本轮责任 | Design | Test |
| --- | --- | --- | --- | --- |
| R153-01 / BEH153-01 | R1、AC1 | 实际入口调查差额，复用正常工作的原能力 | D153-01 / CON153-01 | T153-01 |
| R153-02 / BEH153-02 | R2、AC2/4/10 | Clarify 保留仍有效承诺，整合当前明确变化及必要评论，完整表达适用行为 | D153-01/02 / CON153-01/02 | T153-02/03 |
| R153-03 / BEH153-03 | R3、AC2/3/4/9 | 创建与修订共用单一内容规范，支持适用深度与裁剪，复用语言及来源规则 | D153-01 / CON153-01 | T153-02/03/04 |
| R153-04 / BEH153-04 | R4、AC5/7/10 | 四原 owners 实际同源读取；完整性审核覆盖完整 postimage，语言修改保持本轮范围，遗漏回原 owner | D153-02 / CON153-02 | T153-02/03 |
| R153-05 / BEH153-05 | §4、AC6/8 | 三类需求的 V1–V7 实际行为、创建与修订真实写入回读、受管分发和定向安装分别验证 | D153-02/03 / CON153-02/03 | T153-02/03/04/05 |

不新增 Skill、阶段、公共 I/O、语言权威或通用 gate。完整多平台升级/Release、其他平台实际 Agent 行为与业务仓采用保留为验证边界；历史 Issue 不追溯改写。
