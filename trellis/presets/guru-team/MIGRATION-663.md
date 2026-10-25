# 当前流程合同连续性迁移

本次直接演进 Bootstrap、Branch Review 和 Architecture 三个原 owner 的当前合同。
公共 skill、exit、阶段和业务状态不新增。三个 Bootstrap 当前 profile 保留原 runtime 对
source_exit、continuation_id 和可选 repo_locator 的非空检查，字段必填/可选关系保持。
现有合法输入的含义保持；原判断仍由 AI
完成，脚本只校验结构、Git tree、身份和当前内容。此合同承接 #638 的原维护回程，
补齐该路径所需的 Bootstrap phase2 输入。

## 当前差额与调用方

| 边界 | 当前合同 | 原 caller 的接续 |
| --- | --- | --- |
| Bootstrap repair_required | wire output 保持；Interface rename exit_id→source_exit，seed 只有 source_exit | 原 caller 提供 profile=repair、原 mode/continuation_id，保留原调用适用的 repo_locator/baseline/scope/contribution；同 owner 实际修复 |
| Bootstrap runtime input | runtime 使用 Interface 选择的 closed aggregate/profile；旧 authority/projection schema 退出当前 inventory | 旧 held authority/projection 输入由原 owner 按当前 profile 从 live authority 重构，不作 dual read |
| schema2 archived Review | 正式 example 删除原 schema 不接受的 check_result_id | 从当前 Interface example 填真实 archive/DeliveryKey/HEAD/PR snapshot，按原 recorder/checker/invoke 进入原 disposition stop |
| Architecture before_authority | 当前非 Planning input/output、owner/contribution 和 current consumer 接受可选 absent_locators | 仅声明 baseline_locator、constitution_locator、change_contract_locator 中在固定 git_revision 真正缺失的路径；省略或空集仍表示三文件存在 |
| Architecture Bootstrap 回程 | whole-task bootstrap_foundation 与 delivery_bootstrap_foundation 接受 planning 或 phase2 | final promotion caller 仅在调用期保留原 profile/stage/Task/DeliveryKey/root/continuation；phase2 maintenance 后 fresh 返回同一次 promotion |

before absence 必须逐路径对照固定 B 的 Git tree。未列路径仍须是可读 authority 文件，
误列、漏列或错误 revision 继续阻塞。首次建立后，原 owner 仍审完整当前 authority、
实际 candidate 和全部 B..H；不得移动 B、用 H 替换 before 或豁免原语义门禁。
Maintenance current 不等于 promoted，不等于最终 Check 或业务阶段完成。

## 安装与在途输入

采用本次合同前，沿原 installer/tools owner 安装完整匹配的 canonical workflow、
preset、三包及直接 consumers。不要只复制 schema 或 runtime。平台投影、installed
完整包和 dogfood 从 canonical apply 同步；源码修改不证明已有安装采用。

当前旧 held 失配输入回原 owner，从当前 Interface 和 live authority fresh 构造。
保留原 Task/Delivery 身份、固定 B、真实阶段和实际副作用；不得补造 pass 或把旧成功
结果改成新通过。旧固定发行继续使用其原完整安装与原合同，不新增长期 adapter、
dual reader 或版本猜测。历史 schema、归档和旧版本迁移文档不追溯改写。

workflow 更新仍使用同 provider preview/create-new，审核实际差额后 force 应用。
preset reapply 使用 managed hashes 与原冲突路径；逐项核对 .new/.bak，保留用户内容。
本次产品改动由 canonical package 及 managed spec 分发，禁止只 patch 安装副本。
没有业务数据迁移，也不增加持久 handoff、授权字段或恢复状态。

## 验证边界

当前 registry 的正式 profile examples 同时校验独立与 aggregate schema。每个公开出口
及当前 schema 接受的 published example 变体，经声明 projection 和 caller authoring
组合至正式 consumer；这些结果证明已覆盖输入的结构组合。

实际 wrappers 分别验证 repair、archive 只读链、固定 before absence 与 final promotion
回程。受控 owner fixtures 不等于真实 AI 判断。一个代表性 clean matching 安装及其
原生 owner 验证单独执行；同一安装承担 reapply、平台、mode、权限和 sidecar 检查。
本次不承担完整多平台 Release 矩阵、旧业务安装采用或生产验证。
