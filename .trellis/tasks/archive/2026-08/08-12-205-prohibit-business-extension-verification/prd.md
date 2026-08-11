# #205 禁止业务仓库触发扩展安装验证

## Goal

将 `guru-verify-extension-installation` 收敛为 Guru Team 扩展源仓库主动发起的独立安装验证能力，并从业务仓库的 task、Publication、Finalizer、finish-work、re-entry、recovery 与 task-bearing standalone 路径彻底移除 verifier 调用、路由和状态依赖。

## Background

- 当前 Finalizer 依据 changed path 将 `README.md`、`docs/requirements/**` 识别为 marketplace surface，业务需求文档因而触发 `verification_required -> guru-verify-extension-installation`。
- installed preset、`.trellis/guru-team/extension.json` 和 Skill package 只证明扩展已安装，不证明当前仓库拥有扩展源验证职责。
- Issue #184 与 #198 的 target-business-repository task-bearing 模型由 #205 取代；Issue #195 只迁移 #205 合并后的 source-owned 合同。

## Requirements

### R1 业务路径不可达

- 业务仓库 Finalizer 不输出 verifier consumer 的 `verification_required`。
- 业务仓库 reviewed content push 后直接进入 Draft PR、archive、Ready 或当前 Finalizer 定义的其它合法 transition。
- 业务 workflow 不调用 verifier 获取 `not_required`；不可达判断发生在调用前。
- Publication、Finalizer、finish-work、re-entry 和 recovery 不读取 verifier DTO、owner checkpoint、verification ref 或 `marketplace-verification.json`。
- 业务仓库修改代码、测试、配置、`README.md`、`docs/requirements/**`、`.trellis/**` 或平台安装副本时均不进入 verifier。

### R2 删除 changed-path applicability

- 删除 `marketplace_verification_required` 及仅由业务 diff path 推导 verifier applicability 的 surface/prefix 逻辑。
- 不以更窄前缀、配置开关、三态判断、installed manifest 存在性或 AI path conclusion 恢复业务 task 路由。
- 安装副本 provenance、drift、upgrade/update 和 sidecar 由各自 owner 处理，不转交 verifier。

### R3 source-owned standalone verifier

- verifier 只接受 Guru Team 扩展源仓库中的明确独立验证意图，不接受 task-bearing workflow 或 business-repository fallback。
- 入口在 clone、install、临时目录、artifact write 或 Git/GitHub mutation 前，核对当前 checkout 的 canonical source repository、origin、requested ref、resolved commit 与 HEAD。
- 非 `castbox/guru-trellis` source checkout、repo/ref/HEAD mismatch 和 task-bearing input 返回稳定调用错误。
- verifier 创建 clean throwaway target，验证 marketplace、preset、workflow、平台一致性、ownership、redaction 与 upgrade/update；target 不绑定真实业务 task、业务 branch、Finalizer plan 或 publication HEAD。
- verifier owner state 只位于 source-repository session 的 ignored runtime，完成后删除；不写入 `.trellis/tasks/**`。

### R4 公共合同迁移

- Finalizer current aggregate input、gate 与 transaction 使用新 schema 版本，删除 verifier re-entry profiles、`verification_required` exit、consumer projection 与 `verify` transition。
- verifier current public input 使用新 schema 版本，只保留 source-owned standalone profile；current outputs 不投影到 Finalizer。
- 旧 schema/example 保留为明确标注的 immutable legacy compatibility assets，current interface、runtime 和 workflow 不消费旧 bytes。
- 遇到旧 task-bearing verifier input、旧 Finalizer verification re-entry 或旧 owner state 时 fail closed，并给出返回当前 Publication/Finalizer reprepare 的稳定 remediation；不将旧 payload 自动投影成新输入。
- stable Skill id 与仍受支持的 script command 保持不变；无 consumer 的 exit、DTO、artifact 和 recovery route 从 current graph 删除。

### R5 canonical、安装副本与文档同步

- canonical workflow、Skill packages、runtime、registry/interface、schemas、examples、evals、tests、extension manifest、preset installer 与 README 同步修改。
- 通过 preset apply 生成 `.trellis/guru-team/`、`.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/`，禁止从 generated copy 反向定义合同。
- Codex、Claude、Cursor 的 finish 入口只路由 Publication、Finalizer 和 Merge，不声明业务 closeout verifier hop。

## Acceptance Criteria

- [ ] 业务仓库 task、Publication、Finalizer、finish-work、re-entry 与 recovery 的 current graph 不含 verifier consumer。
- [ ] 业务 Finalizer 不输出 `verification_required`，不通过 verifier `not_required` round 继续。
- [ ] 业务仓库任一 changed path 与 installed extension manifest 均不构成 verifier applicability。
- [ ] 业务 closeout 在 verifier 所需 network/API 不可用时不受 verifier 阻断。
- [ ] verifier 不 clone、checkout 或扫描真实业务 task ref，不在业务 task 中写 verification artifact。
- [ ] source checkout 的明确 standalone 调用使用 clean throwaway target 完成安装、更新、平台、ownership 与 redaction 验证。
- [ ] 非 source checkout 的直接调用在任何外部动作或 artifact write 前返回稳定错误。
- [ ] #184/#198 的 task-bearing DTO、profile、exit、checkpoint、artifact 与 recovery contract 已迁移或标注退休；#195 的 current baseline 与 #205 一致。
- [ ] current typed exit 均有唯一 consumer，unknown、multiple、orphan exit fail closed。
- [ ] canonical、dogfood、preset/overlay、schema、test、README 与 Codex/Claude/Cursor 入口同步。
- [ ] clean initial install、existing repo upgrade/update、official Trellis update/reapply 和 zero-sidecar 验证通过。
- [ ] 一个 clean representative business-repo fixture 的完整 closeout trace 不调用 verifier且不写 verifier artifact。
- [ ] 独立 current-HEAD semantic review 无未关闭 P0-P3 finding。

## Out Of Scope

- 修改业务仓库的业务代码、需求文档或运行数据。
- 使用真实业务仓库 task 作为安装验证 fixture。
- 取消扩展源仓库的安装、更新、平台一致性、ownership 或 redaction 验证。
- 将业务安装副本 drift 视为合法状态。
- 修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 增加恶意 actor、对抗输入、竞态、锁、TOCTOU 或 crash consistency 机制。

## Open Questions

无。Issue #205、#195 的 current wording 与 live code 已固定 ownership、routing、migration 和 acceptance。
