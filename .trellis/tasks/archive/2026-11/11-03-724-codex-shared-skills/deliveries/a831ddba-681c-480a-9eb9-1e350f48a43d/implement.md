# D1 Codex Guru Skill 迁移实施与验证计划

## 1. 输入与引用

整体范围 .trellis/tasks/11-03-724-codex-shared-skills/prd.md 的 AC1–AC5，本批 PRD、design 第3节唯一来源处置及第4–8节方案为执行输入。源为 main B=42ffd32d70be3859a4493e084464738473c45dd6，无前序 Delivery。

实际加载 .trellis/spec/preset/{installer,upstream-ownership,overlay-guidelines}.md、workflow/{companion-scripts,skill-package-contract,subtraction-first-compatibility,quality-guidelines}.md 的相关完整条件；维护和 native 调用分别加载原 package 合同。框架流程保持 Markdown 判断与确定性脚本执行边界。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与 owner | 文件及实际结果 |
| --- | --- | --- |
| I1 | 已激活本 D1；implement 子 Agent | 在 preset 原 owner 内机械抽取 public projection/removal 职责，原 tests 验证行为不变；所有 touched 非生成代码保持 <=3000 行 |
| I2 | I1；同 implement owner | 修改 guru_platform_inventory.py、platform_projection_contract.py、canonical manifest/ownership 及必要 validators；Codex 指向共享根且 exact selection 承接专属包 |
| I3 | I2；原 installer/maintenance owner | 实现有界旧根 provenance retirement、目标完整次序、冲突保留和恢复，调整 upgrade-tools/upgrade-installation 的受影响消费者 |
| I4 | I2/I3；implement 与 check | 更新旧路径测试并补 V1/V2 的独立行为；运行当前 package/runtime、ownership、installed/native 和 mode 定向验证 |
| I5 | I4；主会话与原 tools owner | 维护本工作区 dogfood，保护 Task/session/peer；一个代表 clean 样本及同样本 reapply，执行 V3 原生发现/调用 |
| I6 | 实现可审；原 RDT/Architecture owners | 形成完整隔离拟写 targets，独立 Architecture phase2 和 Check candidate_checked 后 final_integration；原 owner 读回真实共享写入，implementation 重绑候选并 begin_check |
| I7 | 实际最终候选 | 最终 Architecture/Check、TaskCommit、首次独立完整 B..H Branch Review、Delivery Review、Publish、Merge；随后整体 Completion、Closure、Finish 与 Cleanup |

实现子 Agent 负责 canonical 代码和定向测试，不写 shared current、归档或发布。主会话协调工具更新、文档原 owner 和正式交付。独立 Check 子 Agent 提供质量证据，formal Check 仍由 Guru owner 亲自审查。

## 3. 验证入口、输入与预期观察

- V1/V2：在 preset scripts/python 下运行受影响 inventory、installer、dogfood selection、upstream ownership 和 migration/upgrade 定向测试。正常合法前态由原安装/fixture 入口生成；观察选择增减、目标冲突保留旧文件、用户内容和 manifest，不能只断言常量相等。
- V3：真实 codex exec/原 interactive 能力，以 Skill 名称显式调用并保留真实 trace。公共包运行原 public wrapper，专属包运行显式 dry-run，观察原合法出口及能力诊断。绝不把 package 文本预载或本聊天 Skill 清单当作 native 证明；不启动真实业务编排。
- V4：原完整 preset 入口执行一个代表性 Codex clean 安装，继续同样本 reapply；运行 source/installed package validators、公开文件/权限、ownership 和递归 sidecar 检查。
- V5：按 guru-upgrade-tools 的 preview→prepare→invoke 原路径同步当前 checkout；实际 target resolver、get_context 和 installed validation 后执行 bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh。核目标 exact selection 与保留资产。
- V6：候选文档和代码一起完成原 RDT/Architecture→candidate Check→final_integration→实际候选重绑→最终 Check/committed Review。执行质量规范要求的 in-memory Python syntax、Bash syntax、JSON、Task validate 与 git diff --check。

最终报告分别说明确定性、安装、native 及 formal lifecycle 结果；未执行完整矩阵、其它客户端 UI 和正式 source-lock 不能表述为通过。planned 命令不预填成功。

## 4. 停止条件与适用回退点

目标冲突、unknown provenance 或未解决 sidecar 停在原安装/维护恢复；保留原文件及仍需迁移旧副本。源/整体范围或设计机制实质变化回原 Clarify/Author/Architecture；普通输入装配与同范围恢复直接承接。

本批实现不写生产。维护 rollback 只能用原 frozen plan/preimage 和 owner；不 reset Git、不删除新业务改动、不覆写其它工作树。native 环境缺口只暂停对应验收，继续独立工作，但整体完成仍要求必需证据。对已排除的攻击/压力场景不增加阻塞。

## 5. Delivery Policy（唯一）

policy=full。本 D1 覆盖整个 accepted scope 的 AC1–AC5，不把迁移或 native 证据拆成未分配后续工作。独立交付条件为实现、正常迁移/选择变化、真实 native 入口、代表安装及当前知识整合均达到本批验收。

没有计划延期责任，也不表示验证已完成。Delivery 合并后原 Completion 亲自核全部 accepted scope 与实际证据；缺口回原 owner，不用合并或关闭事实替代完成。不存在额外临时能力限制；native 工具前置与 local_candidate 证据边界由原合同保留。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原 RDT writer 为 guru-maintain-requirements-design-test-ssot，原 Architecture writer 为 guru-maintain-architecture-baseline。实际命中单元是 Skill 分发/平台选择及 ARCH-INT-006、ARCH-DOM-020。

Phase2 前由 RDT owner 在 docs/requirements-design-test-contributions/724-codex-shared-skills/ 形成完整 requirements/design/test/traceability 和 proposed current targets；Architecture 隔离 contribution/必要 ADR 由 Author 先按候选结论展开。两者在 candidate Check 后由原 owners 于 final_integration 集成真实 targets；保留其它 Task 已生效内容，更新必要关系/导航，不增加全局版本号，不重写不可变历史。

canonical installer spec、skill-package-contract、README、MIGRATION-724 和当前测试说明按原 owner 承接路径迁移。直接 consumer 是 installer/maintenance、Agent discovery、后续 Check/Review 和用户安装说明。dogfood 规范与公共 Skill 投影通过原完整 tools owner 同步，不手工覆盖受管副本。promotion 后实际内容重绑，最终质量链覆盖所有实现、文档与导航。

