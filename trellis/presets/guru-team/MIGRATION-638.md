# 稳定知识身份与最终整合晋升迁移

本合同迁移原 Architecture/RDT/Check 及其受控消费者。旧完整安装可以固定原版本继续；采用新行为时必须通过原安装或 tools owner 切换完整匹配 source，不局部复制 runtime，也不从旧 pass 补字段生成新结果。

## 当前合同与退出边界

| 对象 | 当前入口 | 旧运行入口的处置 |
| --- | --- | --- |
| Architecture 非 Planning impact/promotion | repository5.0 / Delivery3.0；promotion stage=final_integration | 4.0 / Delivery2.0 不再由当前 selector 接受；旧 schema 保持原义供固定历史验证 |
| Architecture Planning | Planning3.0 / Delivery1.0，candidate_assessment 与 final_plan | 两个目的及唯一相邻 consumer 不变；bootstrap/repair 保持原合同 |
| RDT impact/promotion | 2.0；phase2 impact 可返回 candidate_ready，final_integration promotion 才返回实际 ssot_current | 命中的1.0运行分支退出；bootstrap/repair不改义 |
| Check | private6.0；新增独立 delivery_candidate_check / candidate_checked | 旧5.0不能转成新通过；原最终 profiles/passed 保留最终 public Check 语义 |
| 下游 | TaskCommit、Branch Review、Delivery Review、Publish/Ready、Completion/Finish | 只接受实际最终候选及必要 no_change/reviewed_promoted；候选输出不形成最终 gate |

新出口各有独立最小 DTO。RDT candidate_ready 交既有 current router，定位贡献及适用 authority；Check candidate_checked 只交 guru-knowledge-final-integration-router，含 TaskRef/DeliveryKey 和原 candidate head/content_identity。它们不携带私有审计、恢复 intent 或授权。

## 正常顺序与合法公共转换

1. 原 implementation 在 implementing 以固定 B、实际 HEAD 和全部已提交/dirty paths 调用 candidate/begin_check，进入 checking。
2. 原独立 Architecture phase2 和原 Check delivery_candidate_check 审完整实现、隔离贡献、完整拟写正文及受影响未改 consumers。候选通过时，Check 使用原 rework(target_role=implementation, affected_results=[readiness]) 返回 implementing，再发 candidate_checked。它不调用最终 record_gate，保留 Planning 和真实旧结果历史；历史不获得当前适用性。
3. 唯一 router 调原 Architecture/RDT final_integration promotion。原 owners 一次固定真实目标 branch/commit，读命中单元，保留双方仍有效条件，必要时沿唯一 Candidate Applicability And Coverage 合同补审全部差额和 consumers，随后写入并读回。无知识变化不创建贡献、ADR、空文件或空提交。
4. 原 implementation 以同 B、实际 HEAD 和全部晋升/关系/导航 paths 重建 candidate/begin_check。最终 Architecture/Check 检查新 content_ref；只有最终 Check record_gate 进入 reviewing，再由 TaskCommit 和独立完整 committed Review 到 readiness/Ready。

不增加 Task phase、公共 API operation、Skill 或新调度器。不要求为了知识晋升 merge/rebase；behind、无关 CURRENT 或 remote ref 前进不是同步理由。实际冲突、依赖或 required-check 集成阻塞仍回原 owner。根入口只在定位、身份或状态变化时修改，普通晋升可沿用稳定 authority identity；精确内容由完整 Git revision/locator 绑定。真实 API/schema 版本独立维护。

## 三类在途恢复

| 实际状态 | 原 owner 的恢复行为 |
| --- | --- |
| 尚未晋升 | 重读原适用 authority、完整候选和拟写正文，重新取得新候选判断，再进入最终整合；不转换旧通过 |
| 已晋升，最终 Review 尚未完成 | 保留真实写入，由原 promotion owner 读回同一 intent，仅补明确 pending；implementation 绑定实际 after candidate，补当前最终 Check/Review缺口，不重复晋升 |
| 已有最终 Review | 原 owners 核当前适用性；没有实质变化接续 readiness，真实变化回最早受影响 owner；不因新版本号重做同质审核 |

candidate_checked 输出丢失时先读公共 phase 与候选。仍 checking 时由原 Check 重读、实际判断并合法 rework；已 implementing 且尚未写入时由 implementation 重新 begin_check，再原 Check 实际重判；已有写入时由原维护 owner 恢复同 intent，再 implementation 绑定 after candidate 到最终 Check。不得从 phase 推导候选 pass或直接改公共文件。全部恢复保留同 DeliveryKey、Planning 和固定 B。

partial/output-loss 只恢复同一可唯一辨识 intent。completed 读回、pending 补写；conflict 或 intent 不明确时停原 owner。旧 schema、ADR、版本页、贡献和 Git 引用保持原历史含义，不回填。旧普通读 consumer 在 Task 完成、合法 Reactivate 改选或实际依赖变化后退出；历史永久可读。没有第二 current 或长期双 parser。

final_integration promotion 返回 bootstrap/repair 时，原 router 仅在当前调用保留原 promotion profile、Task/Delivery key、planning_root 和 stage；向原 maintenance 输入薄投影为其既有 stage=phase2。maintenance 完成后只回同一 final_integration promotion 重读真实 authority 并重绑实际 candidate，不把 maintenance current 当作 reviewed_promoted。bootstrap/repair 的旧 schema 和行为不扩张，也不新增持久恢复状态。

## 安装、代表迁移与证据

完整匹配 marketplace workflow、preset、三个原 packages、直接 consumers、schema/selector 与声明平台投影一同切换。workflow 按官方同 provider preview/create-new、审实际差额后 force 应用；preset 沿原 apply/reapply 与 managed hashes/sidecar/mode 路径保留用户内容。源码编辑不热迁移开发 Task。普通 apply 若因原 legacy archive 校验写前阻塞，保留诊断和归档；tools-only 成功不等于全仓 reapply 通过。

本批代表迁移知识维护 R/D/T、命中的 Task/Delivery 生命周期及 Architecture CURRENT/DOMAIN/INTEGRATION/GOV/change-contract、根导航和语义 ADR。其余能力与历史归档不批量改写。未晋升时完整拟写内容仅在 Task contribution 的 proposed/，真实 current 保持原状。最终同一业务 PR 交付实际正文；贡献存在不证明晋升或完成。

验证分开记录 production wrappers、公共 phase/content_ref、完整拟写与真实合成、source/dogfood/installed、一个代表 clean matching 安装/reapply及真实 native Agents。#636 Draft 与 #637 后继差额机制在原 owners 内组合验证。fixture/静态分发不证明真实 Agent 或远端成功；本合同不承担完整多平台 Release 矩阵、Backend采用或生产部署。

当前production-current-v5及current alias仅增加选定Check候选profile/exit/eval绑定，manifest结构/字段语义保持；旧v4/v3/v2历史manifest不改。extension descriptor的input/output/private库存按实际40个selected Interfaces投影，包括既有Draft与原维护/终态schema的库存差额校正，删除失去当前consumer的旧ID；不扩旧runtime或宣称旧功能重新验证通过。
