# Phase 2 recorder 输入职责迁移

本迁移直接演进原 `guru-check-task`。新匹配安装的
`record-phase2-check --input` 只接受现有封闭的 11 字段语义 authoring。
完整 6.0 对象是 recorder 输出，以及 checker、invocation 和原恢复入口的输入。
它不再是 recorder 输入。原命令 id、argv、结果 schema 6.0、public profiles
和 typed exits 均保留。本迁移不新增输入版本、兼容 flag 或第二 reader。

## 当前调用者与处置

盘点以 #710 的固定开发基线 `2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30`
为 before，同时检查实际 record 调用、输入模板、注册转发和结果消费者。
历史 README、迁移说明与已归档证据不构成当前 recorder consumer。

| 当前调用族与定位 | 实际入口、输入与迁移 |
| --- | --- |
| `guru-check-task/tests/test_candidate_check.py` 的 `recorded_owner` | before 从完整示例手填 Task/HEAD/私有摘要后传给 record；改从 `examples/phase2-authoring.json` 填语义，record/check 后将同一结果文件交 invoke。专门的完整输入案例只验证其明确退出。 |
| `guru-check-task/tests/test_runtime.py` | record 调用原已投影语义字段；正常输入改用正式语义示例。完整 schema/checker/project 测试继续构造其真实完整输入，不能作为 authoring/native 证据。 |
| `guru-check-task/tests/test_delivery_flow.py` 的 `check` | before 直接构造完整 invoke 输入，并非 record 生产 consumer；正常测试改经语义 record/check，再将原 artifact_path 交 invoke。 |
| `guru-check-task/tests/test_execution_consumption.py` | 原入口是完整结果的 invoke 消费；保留字段、成功/finding/planning/blocked、freshness 与恢复测试。它不要求保留 record 的完整输入分支。 |
| `adapters/eval/production_fixtures.py:production_phase2_input/production_record_phase2` 与 `delivery_production.py` | producer 已产语义输入；沿原 record/check/invoke。fixture 判断只证明命令运输，不能供应本轮 mandatory native 语义前置。 |
| `adapters/eval/phase2_authoring.py:execute` | 将 Agent 当轮语义对象原字节交 record，校验回执后以 `result.artifact_path` 交 invoke；不增补私有身份。候选/最终运输沿同一原 owner。 |
| `adapters/eval/owner_runtime.py`、`implementation_authoring.py`、`stage_result_authoring.py` | 原组件/命令 relay 透明转发 `--input`，本身不构造完整 Phase 2 authoring；其受影响测试使用语义输入。`test_phase2_authoring.py`、`test_implementation_authoring.py` 中原已排除五个结果字段的输入可直接采用新语义示例。 |
| `presets/guru-team/scripts/python/verify_installed_closeout.py`、preset 命令注册、workflow `scripts/bash/record-phase2-check.sh` | 透明 `--input` 转发或原命令定位；没有必须保留的完整输入生成者。命令、安装、可执行模式和回执职责保持。 |
| `guru-review-task-completion/tests/run_native_causal_eval.py` | 原模型 authoring 已明确只写 11 字段，wrapper 将其 semantic 文件交 record，并将原回执 artifact_path 交 invoke；不需完整输入兼容。此核对不代表重新执行其 native 矩阵。 |
| `guru-check-task/runtime/check.py`、`delivery.py`、`project.py`、`legacy_maintenance.py` / `recover.py` 及已录 checkpoint | 原 checker/invoke/投影继续消费完整 6.0 结果；legacy maintenance 只保留其原 schema 5.0 检查与退役/恢复边界，不是完整 6.0 record 输入 consumer。恢复不经 record 重新包装，不更改历史 schema 或 Task。 |

在上述正常调用和模板中，没有必须长期保留 record 完整 6.0 输入的生产
consumer。受控调用直接迁移到语义输入；新 recorder 对完整对象返回原
`schema_mismatch`，`field_path=input`，提示当前 authoring 和本迁移。
正常说明不再要求调用者在两种 authoring 之间选择。

## 安装切换与恢复

固定旧完整安装可继续使用其原合同。采用本行为时，通过原安装或
`guru-upgrade-tools` owner 切换完整匹配 source：package、示例、命令 metadata、
共享 runtime/schema、受影响 caller 和声明平台投影必须匹配。不要只复制
record.py，也不要手工覆盖受管 dogfood。按原 owner 处理用户修改、sidecar、
mode 和 Task/session 保留。本迁移没有业务数据或历史 Task 转换。

已录完整 6.0 结果继续由原 checker 和 invocation 恢复消费。
legacy maintenance 保持其原 schema 诊断与历史控制恢复合同。
需要原 public input 的消费仍须持有同一 Task/Delivery/Planning 和当前候选。
丢失输出只恢复该原结果。缺失、过期或不匹配时，由原 Check owner 重读当前
事实，完成新的完整语义轮次，再 author 和 record；不能重算旧结果的 HEAD
或摘要来延长旧结论。

`guru-reviewed-content-1.0` 候选 token 与
`guru-phase2-worktree-content-2.0` 私有 Phase 2 token 保持原算法和直接 consumer。
合法公共 producer token 原样承接；不能把它填入 Phase 2 私有字段。
checker 的 Task、内容摘要和路径覆盖诊断分别定位原字段，仍返回
`stale_identity`。摘要不同只证明绑定不符，不能据此断言算法、内容或编码根因。

## 验证与退出条件

定向命令测试从正式语义输入执行 record/check/invoke，覆盖五个适用 profiles
及其原成功、finding、planning、blocked 和 resolved 行为。完整结果消费者测试
保留合法恢复、真实业务变化拒绝及 metadata 连续性。说明/引用检查、命令测试、
真实 native 首次候选和最终阶段、matching 安装与 reapply/drift/sidecar/mode
证据分别报告。新合同不存在长期双输入退出期；本迁移随匹配安装直接切换。

本说明不是验证结果。#710 的实际验证位置提供固定候选提交、匹配安装来源、
profiles、命令及首次 native 定位供 #713 采用；#713 仍亲自执行其完整链当前
Check。本项不证明业务 #994 采用、完整多平台 Release 矩阵或生产部署。
