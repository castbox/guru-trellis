# D2 实施与验证计划

## 1. 输入与引用

读取整体 [PRD](../../prd.md)、本批 [PRD](prd.md)、[design](design.md) 及其第3节唯一来源设计处置。B/H0 为 D1 已交付 head aaf7f939；原 D1 planning、Check/Review、PR776/三平台 CI 是实际前序事实，不代替本批门禁。

候选 Architecture 为 `architecture_impact / target_native`，要求完整 runtime-location 贡献及窄后继 ADR。实施前实际读 tools package 当前 Skill/contract/Interface/schema/runtime/tests、skill-package-contract Public Skill I/O And Private State、companion-scripts、quality-guidelines 的 Test And Validation Value/Validation Scope Ownership、subtraction-first-compatibility 和 clear-technical-writing。官方 workflow/spec marketplace 扩展文档已核：AI 判断保留 Markdown，脚本只执行事实，不改上游、全局包或 hook。

## 2. 有依赖顺序的步骤与文件责任

1. P2-1，Author/原知识 writers：完成当前三正文、真实隔离 Architecture/RDT 完整 proposals、必要 ADR 和官方 implement/check JSONL。经 Wording、同一独立 Architecture final_plan、Approval、Activation 后实现。
2. P2-2，实施 owner：只改 canonical `guru-upgrade-tools/` 及 MIGRATION-769。加性输入/输出/Interface/consumer/examples；有限 roots 事实校验及原 engine 前后透传；保留省略/[]、同源 profile、common/gitdir/存续变化及 #759 原边界。无新 cp、源替换或第二状态机。
3. P2-3，同实施 owner：补 V2-1/2/3 的真实 Git/原入口回归和有/无字段 consumer 分支，运行受影响完整 package。若发现新机制或实际缺陷，先回原 qualification/Author/Architecture。
4. P2-4，原 tools owner：从完整修复 source 更新当前 checkout，保 Task/session/config/AGENTS，实际目标 own installed/native 和 drift 取证；未知编辑、sidecar、unfinished transaction 回原 owner，不手抄 manifest/hash。
5. P2-5，原 Architecture/RDT/Check：评估完整实现和 proposals，candidate Check 后原 final_integration/readback；重绑所有真实写入，最终 Architecture/Check、精确 commit、原独立完整 B..H Review、Delivery Review、Publication/Merge。
6. P2-6，原 tools owner：从交付后的完整修复源执行 V2-5。保留 #766 原 ref/source/public operation/plan/preimages/snapshot；输入仅加本轮已核正常退出的准确 roots。成功后才交 #769 whole-Task Completion，#766 回自己的原任务继续。

主协调者拥有规划、知识贡献与正式交付；实施 owner 不写 shared current，不覆盖其它人的修改。每次写入前执行 `check-task-checkout-boundary.sh --json --task .trellis/tasks/11-09-769-tools-peer-growth-recovery`。

## 3. 验证入口、输入与预期观察

- V2-1/2/3：原受管 Python 执行 `guru-upgrade-tools/tests` 全包及命中恢复/contract 回归。真实 Git 加 peer、原观测/begin、正常移除后公开 frozen 入口携 roots；独立核原固定 bundle 未变、后续原阶段及 consumer 结果。旧省略、[]和存续变化/普通选错分别观察，不增恶意或压力排列。
- V2-4：用 matching managed resolver 执行 source validator；原 tools 同步后执行目标自身 installed validator、get_context/native/current、drift、Task context validate、必要内存 Python compile/Bash/JSON/diff 检查。区分本轮执行与采用不受影响事实；核无 conflicts/sidecars、Task/config/AGENTS 内容与模式保持。
- V2-5：交付后对实际 #766，`recover_frozen_source / action=resume / recovery_ref=05d804ba-1a5d-4975-93bd-9909ff00e719`，准确 retired root 为原 #759 checkout。依据原 Cleanup 已恢复的同一 `cleaned` 与当前目录/注册事实，由 AI 先判适用，再执行。核原 public operation=8838ed00-b7c3-4ab3-97cd-0fd392e0740b 及原 source/plan/preimages/peer snapshot 保持，并读目标自身 resolver/installed/native。

组件测试中的 SDK/preset/native 隔离只证明其层次。完整多平台安装/升级/Release 不在本批；local_candidate 的 formal_fork_source_lock 未验证项仍保留。D1 三平台 CI 的成功不提前成为 D2 或现场成功。

## 4. 停止条件与适用回退点

根对象不关联原观测、仍注册/存在、原 source/owned/common/存续 peer 真实不匹配时，原工具 owner 具体阻塞；不得改快照、重 prepare、复活759或追加未核 roots。正常退出依据缺失时先由 AI 补原 owner 事实，不能用 OS 结果替代。

范围变化回 Clarify，机制/复用前提变化回 Author/qualification/Architecture，普通实现缺陷由原实施/Check修复。原事务可恢复失败只消费同 profile/action/ref及必要roots；rollback仍先public兼容后原恢复。没有业务数据迁移或生产服务发布，不造新rollback协议。必要验证和实际现场充分后停止可选实验；失败不得重写成通过。

## 5. Delivery Policy（唯一）

full：本批完成当前剩余 R2–R6/AC2–4，D1 的 R1 和已交付事实保持。D2 先独立交付接口、实现、回归、知识及实际当前目标分发；合并后从已交付修复 source 继续原 #766 操作，这是整体 Completion 的必要验收，不是另一个功能切片。实际恢复未成功时，#769 不完成/关闭/归档。#766 后续业务质量与交付由其原 Task 承担。

兼容只覆盖原 schema1.0 操作及其原保留期限。新能力的 caller 采用完整 matching package；旧输入/旧 retry保持，无强制新字段。原操作终态且原恢复责任结束后，由明确迁移处理退出，不建周期台账或监控。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原 RDT writer 在 `docs/requirements-design-test-contributions/769-tools-peer-growth-recovery/d2-retired-peer-observations/` 维护 runtime-location requirements/design/test 的完整 proposed 单元，写明 AI 原退出依据、有限 roots 输入、仍存续保护和分层证据。原 Architecture writer 在对应 Architecture Task-owned 子目录维护完整 runtime-location proposal 及 ADR-TOOLS-RETIRED-PEER-OBSERVATIONS；D1 contribution/ADR及旧观察保留。

独立 Phase2 和 candidate Check 前不改 shared current。原 owners 在 final_integration 固定真实目标、整合/readback 后，重建候选并覆盖全部写入的最终质量门禁。实际原操作结果由后续 Completion 消费，不追写正文自己的最终 pass/HEAD，不新增根索引或结果 ledger。
