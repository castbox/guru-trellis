# ADR-850-DEFAULT-WORDING-RETIREMENT

状态：`integrated_pending_review`。来源为 Task `850-retire-default-wording-gate` / generation 0 的 D1 `eb5ddae6-a516-41a4-9058-fb5d5d59c20b`。原 Architecture owner 已在 final_integration 写入并读回本决定；尚待 TaskCommit 与独立 committed Review。本状态不表示完整验收、交付或 Release 通过。

## 来源、背景与边界

来源为[#850](https://github.com/castbox/guru-trellis/issues/850)的职责承接、完整迁移及在途续接条款。固定before为a72981db56d2070d8140b468cab3a97ae82effd3。既有Clarify、Author、Readiness、Architecture、Approval和清晰写作规范承担实际内容判断，独立Wording仍带来扫描分类/回执/绑定和return依赖。

本决定窄替代旧独立Wording mandatory、专属scanner和receipt机制，以及ADR-ISSUE-REVIEW-INTAKE中Wording局部补审和全链承接片段。旧决定的真实来源、历史结果、先行Readiness、评论、source与Task创建责任保持。ADR-022/024/035及EXPLICIT-REVIEW-OBJECT的唯一writer、双Architecture目的、scope/continuation、只读对象与Activation职责保持，仅退出其中独立Wording前置与回程。

## 决定与责任

采用target_native，同批直接迁移实际consumer。完整Intake成为Discovery→Clarify→Readiness；Planning成为Author requirements→candidate Architecture→Author方案→final Architecture→Approval→展示接受→Activation。原七项语义职责由原内容与审核owner实际执行，不搬七字段或另一套逐词证明链。

Clarify独占Issue内容、来源/范围和有界Issue/draft措辞审核；Author独占Task/Delivery规划及原content revision。Readiness独立复核当前覆盖和十维，局部事实回Discovery，内容/措辞缺口回Clarify并回同次Readiness。final Architecture保持独立实际方案评估，Approval保八维，script只校客观事实。

源title/body身份与Clarify语义identity分开，单一source token从真实快照派生，只供Readiness检查当前对象；它不是semantic pass或授权。显式只读路径无需Task/Delivery绑定，不写对象，不自动进入完整Intake或开工审核。选定Markdown全文由现有review-change新增explicit_files/wording_only承接，包括未变更文件；working_tree的Git差额不能替代全文。新profile只承担本次表述与保义审核，不继承range的实现完整度、测试及三视角前置；原range方法与wire保持，public aggregate2.0同批加入1.0分支。

删除同名Wording包、注册、scanner/词表/分类/receipt、专属schema/配置和无人消费wrapper/tests；不保optional scanner、新Skill、长期转发wrapper、双reader或coverage ledger。shared通用元schema和历史资产按实际consumer/固定历史身份保留，不以词面命中扩大删除。

## 兼容、在途与退出

current-only successor的接口、schema、graph、当前文档和controlled consumers同批切换；具体版本由D1 design第5节及实施发布的MIGRATION-850拥有。当前对象等待Wording或原content_changed时，原caller将真实对象/refs/适用内容覆盖交回原owner，不制造旧Wordingpass或新阶段通过。必要新source identity由原Clarify补齐；同Delivery范围、合法选择和已完成有效结果保留，普通等义变更不重跑全链。

已经开始的fixed-old-provider副作用在该完整固定provider恢复同一对象后再匹配更新；不混用envelope、不重复远端动作。旧版本只服务该原操作或历史读取，操作完成及匹配切换是退出条件，不为新调用开放旧链。

原tools/installer以完整matching source更新inventory，复用managed stale删除和用户内容sidecar，保Task/session。源码变化不等于已有安装采用，受管文件不手抄。原RDT与Architecture owners分别准备完整隔离定义；实施与工程事实充分后final_integration写入/readback，TaskCommit及独立committed Review核actualbefore/after后才产生reviewed_promoted。

## 替代方案、成本与复审条件

保留optional scanner、仅改提示或仅删mandatory标签都会保留原专属证明consumer。把扫描/分类整体搬入Clarify/Author会复制机制而非保留必要职责。新增通用迁移层会扩大维护和状态成本；现有live对象、原producer恢复与matching安装已提供直接边界，因此不采用。

本方案成本是一次真实public contract/consumer迁移、源内容identity衔接、原有界审核profile及受管退役验证。源token有明确Readinessconsumer；有界profile服务无法要求Task绑定的既有显式请求；两者不承担新审批职责。

若实际来源、消费者、语义owner、外部support或迁移约束变化，回原Architecture/Author判断实际差额；真实scope选择回Clarify。无关HEAD/时间/Agent变化不自动废除有效覆盖。实际Agent、生产wrapper、受管安装、独立Review与wholeTask完成分别由原owner证明，本ADR不预填结果。

## 本次整合的证据边界

本决定与实际公共合同、原 owner 和受管采用同批整合。可读原文证明本轮 `local_candidate` 工具更新、受管字节/权限、installed 校验及 drift；`formal_fork_source_lock` 仍为 `unverified`。源工程汇总、真实有界审核、live Readiness 和隔离 Planning 的观察分别保留其边界。#819 `wording_only` 的受控本地三来源 fixture 已实际完成同次补审、单次 PATCH/GET、supplemented 和 Readiness ready；首错保留，不能称首次正确，也不证明 live GitHub 写入、完整链或全部正常分支。不据此声明全 I07、完整 AC、独立 committed Review 或远端交付通过。实际结果由 [#850 Test](../../requirements-design-test-contributions/850-wording-retirement/test.md) 单写，历史结果不重标。
