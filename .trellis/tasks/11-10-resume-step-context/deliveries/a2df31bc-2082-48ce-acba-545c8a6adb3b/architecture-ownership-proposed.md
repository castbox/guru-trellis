# Ownership 完整拟写单元

状态：proposed。固定来源：`26630149070e2988ad08102679931468b3535ef8:docs/architecture/03-domains/ownership.md`。目标仍为同一路径。本文三个章节各自包含一个完整 resulting definition，仅替换目标中对应 identity 的原完整表格行或段落。章节标题和本说明是候选定位，不进入共享正文。其它原文及 #419、#443、ARCH-DOM-024/025/043/045/053/060 等关系不作替换。

## ARCH-DOM-016：替换原表格完整行

| Identity | Domain | Authority |
| --- | --- | --- |
| `ARCH-DOM-016` | active-task continuation | Guru workflow 独占 detailed continuation、mandatory 调用与唯一 typed-exit consumer；原 `guru-ensure-task-checkout` 的 current profile 只组合上游 public current 与既有 Guru checkout 校验，向原 current-checkout router 提供最小定位。caller 从实际出口取得原 owner 合同后，完整加载适用条件和必要依赖；定位或 phase 不产生语义通过。adjacent DTO 的 consumer、deterministic producer recovery、semantic owner fresh rerun 与 activation owner 各保持单写；upstream 独占 extractor 和 thin entries，原 start/default get_context 不由此查询修改。 |

## ARCH-DOM-019：替换原表格完整行

| Identity | Domain | Authority |
| --- | --- | --- |
| `ARCH-DOM-019` | task identity session binding | official Trellis task/session store 拥有稳定 task identity、底层 context resolver、public current 与 persistence；`guru-bind-task-session` 独占 lifecycle-aware resume/rebind/switch/reactivate/manual-recovery 判断与最小 runtime write。原 Ensure current profile 复用 public context/current 和 C4/C5/唯一 checkout 校验，只投影同 Task/generation 的必要事实；无 context key、真实 context 无绑定及读取或关系错误保持区分并交原 router/恢复 owner。查询不借另一会话、不从 inventory 或目录选对象、不写 Bind/Selection；Delivery 选择与 terminal 处理仍属原生命周期 owner。独立 final_plan 的一次性对象评审由原 Architecture 本地入口只读核验，不产生绑定或第二 writer，普通执行恢复仍保本 owner 必要 runtime 写入；#438 保留 creation attach，#436 保留 terminal lifecycle receipts，#434 独占 production route activation。 |

## ARCH-DOM-038：替换原完整段落

`ARCH-DOM-038`：原 Skill 单写 semantic 判断、内部 owner/checkpoint 与 public exit，共享 dispatcher 单写声明驱动的 CLI transport；具名 caller 校验后投影 result，workflow 只消费真实 public invoke DTO。原 `discover-skill-contract` 从 registry/Interface 定位公共合同；实际 exit 查询与 installed validation 共用原 workflow marker parser，校验唯一 consumer 及 Interface 一致性，只返回选定 output、consumer input/projection 和原入口或 workflow/stop target 定位。动态 `profile_selector` 保留原合同，由持有实际 payload 的 caller 按原条件消费；discovery 不猜 profile、不执行下一 owner，也不建立第二路由表或缓存。caller 在实际调用前完整读取适用合同及必要依赖，未知、多重、未映射或不一致声明沿原诊断停止。Architecture/RDT 原 promotion owners 继续各自串行更新共享 authority；原 #453 的 expected `.81→.82` 记录保留其历史含义，不成为普通查询或后续 Task 的全局版本写入要求。无新增授权状态、reviewer ledger 或业务 writer。
