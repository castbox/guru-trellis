# ADR-020：独立目标感知根因候选资格

- 状态：`accepted`；来源：#382 已独立审查的 `phase2-v1` contribution 与 ADR candidate。
- predecessor：ADR-008 的 normal/solution 分工、ADR-019 的独立新评估和 ADR-005 的 promotion 生命周期继续有效。

## Decision

新增 `guru-qualify-root-cause` semantic owner，独占新提出或实质变化真实故障机制的因果候选准入、稳定适用性与回程。按诊断、缓解、修复、保护和普通 feature 实际目标判断；不把未知根因一律阻断，不把症状抑制包装为修复。normal-scenario 继续拥有场景，solution-mechanism 继续拥有 authority placement；root 不循环调用或复制其正文。

四 typed exits 返回现有十 profile owners：classified 继续，mechanism revision 移除/替换，diagnosis required 暂停未经证明的修复并继续必要取证，blocked 保留真实阻塞。后续阶段消费仍适用结论并独立审其当前工作；实质变化回 root，caller/stage 变化本身不重审。阶段完成与 #383 的共同因果完成语义不由 root 承接。

## Alternatives and consequences

扩张既有两包会混合场景/authority/因果职责，复制到 callers 会形成重复认知；独立包复用现有 call-local dispatcher 与窄 facts extraction，保持原公开 API、无 durable qualification state 或新审批链。公开输出仅携带直接 consumer 所需结论。新包的 contract 独占资格正文，本 ADR 不重定义规则。

实际结果由[唯一 Test](../../requirements-design-test-contributions/382-root-cause-qualification/test.md)拥有。expected `.78→.79` knowledge promotion 后仍须 fresh Phase2/TaskCommit/独立完整 Branch Review；不证明任务完成、业务生产修复、候选远端安装或完整 Release gate。
