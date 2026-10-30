# #694：独立 final_plan 的显式评审对象

本次直接演进原 Architecture `delivery_task_impact_sync / planning / final_plan` 接入。完整显式对象可在接收者无 Task 绑定或同 Task/generation 无 Delivery 选择时只读校验；对象不写为执行选择。现有合法匹配选择与确认无 context 的入口保留。其他选择、terminal、错误及完整对象失配保原 owner。原 Skill [合同](../../skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md) 拥有完整前置和读序。

没有新增 Skill、profile、typed exit、公共字段、配置或持久格式。共享 `DeliveryProjection.current(key)`、其他 Planning consumers 和 Architecture stages 不变。相邻 Approval 仍按自身合法选择承接实际 final_plan stdout；其他出口保原 consumer。普通执行缺绑定/选择仍由原 Identity/Ensure/Bind/Selection 恢复，其必要 session runtime 写入不属于一次性只读评审前置。

## 成套采用

从同一完整来源更新 marketplace workflow、Architecture package/runtime/contract 与匹配 preset、Shared 和全部选定平台投影。既有安装先通过官方 `trellis workflow --marketplace <同源marketplace> --template guru-team --create-new` 预览，检查 workflow bytes、live identity、用户修改和 sidecar 后，使用同一 provider 显式 `--force` 应用。稳定版本的 workflow 与 preset 使用同一不可变 release tag；本次源码候选不作为已发布 tag。

随后以该完整来源执行 preset apply/reapply，处理真实 `.new`/`.bak`，验证 source/installed packages、ownership、选定平台、dogfood drift、mode 与递归 sidecar。保留用户内容、Task/Delivery/session 和历史。普通 apply 若被历史数据 preflight 阻止，沿原 tools-only/upgrade owner 完成其精确受审写集；不手改 guard、manifest/hash 或无关 archive。

在途仍用同 TaskId/generation/DeliveryKey/planning_root 和实际未完义务。旧完整安装成套采用前保原合同；不把源码变更当作热迁移，不增双reader，不要求重开已有规划。只有实际 planning 对象满足当前入口才评审，不能用本迁移绕过 phase/scope/freshness。

## 验证边界

按原开发、Check、独立 Review 和升级 owner 执行本项命中的定向验证。不新增专项回放、A/B/native eval、固定案例数、耗时指标、额外 clean installation 或完整平台矩阵。fixture、正式语义结果、installed 行为与现有业务采用分别报告；实际观察由 [#694 Test](../../../docs/requirements-design-test-contributions/694-final-plan-object/test.md) 拥有。
