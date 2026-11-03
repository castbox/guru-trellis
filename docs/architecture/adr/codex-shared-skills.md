# ADR-CODEX-SHARED-SKILLS：Codex 公共发现目录收敛

状态：accepted。来源：https://github.com/castbox/guru-trellis/issues/724。
适用基线：42ffd32d70be3859a4493e084464738473c45dd6；Architecture identity 保持 guru-trellis-architecture。

## 问题与采用决策

Codex 的共享公共包同时在 .agents/skills 与 .codex/skills 出现，专属编排包只在旧根。官方当前 repo-skill 合同使用 .agents/skills。采用一个 current Codex 根，复用原平台选择、public allowlist、installer/provenance 和维护恢复，不新增双投影或通用兼容层。

Codex selected root 与共享根相同，去重后只有一份受管公共投影。专属包仍只支持 codex，保留 agents/openai.yaml 的显式调用策略和原生能力前置。目标 exact platform selection 决定包集合，不以共享目录存在扩大平台支持。

## 迁移与旧决策替代范围

窄替代 ARCH-INT-006 中 Codex 同时要求 shared 与独立 selected root 的路径解释；ARCH-DOM-020 的各 owner 保持。旧 .codex/skills/guru-* 仅作为有界 predecessor retirement 识别，不进入 current descriptor、claims 或新 expected inventory。

原迁移 owner 确认目标公共文件集合内容/mode 完整且无冲突后，按 previous managed provenance 移除未修改旧文件及其派生空目录。两端用户修改、未知来源内容和未解决目标冲突保留；目标冲突解决前保留仍需迁移旧副本。重试沿原恢复路径，不用双根掩盖未完成。

保留其它 Codex 配置/Hook/agent/prompt、Claude/Cursor 根、公共 Skill API、用户级/第三方和上游资产。移除 codex 选择时按原受管规则退出专属共享投影，保留其它平台需要的公共包。

## 依据、成本与重审条件

现有 descriptor 和 selection 机制可以承载新根；单根减少重复发现、同步与校验。一次迁移需要来源核对、冲突处置及定向测试。保留原 staged activation、恢复和用户内容保护，避免新台账、锁或长期 fallback 的维护成本。

真实受支持宿主依赖旧根、官方 scanner 合同变化、公共集合或平台适用性变化时重新评估。native discovery、实际公开调用、确定性投影和完整发布矩阵分别报告。当前 ADR 不证明实现、迁移或宿主兼容已通过。

## 验证与生效

按本 Task D1 design 的 V1–V6。原独立 Architecture phase2 与 candidate Check 审完整 proposed targets；原 Architecture owner 在 final_integration 比较真实 before/target 后写入并读回。此时才切换当前定义；最终 Check 和完整 committed Review 覆盖实际候选。

