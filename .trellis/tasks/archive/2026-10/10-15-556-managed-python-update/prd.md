# #556 默认 python3 与受管 Python 环境更新

## 需求 authority 与问题

唯一 Direct Source：[castbox/guru-trellis#556](https://github.com/castbox/guru-trellis/issues/556)，当前正文的“目标与范围”“验收”“边界与相关 Issue”。该 Issue 无评论；本轮 source_selection 为空。Issue 中历史机器版本仅用于解释失败，不作为当前环境证明。

现有 bootstrap 在依赖安装前用 Python minor 白名单拒绝未枚举的 CPython3。初始化和显式 apply/reapply 的选取行为、实际失败原因及检查后激活合同须完整承接。

## Accepted scope

- R556-01：初始化和显式 apply/reapply 无显式解释器输入时，以执行当时 PATH 的 python3 计算 runtime identity；保留 bootstrap 的 --python 并为 apply 入口提供明确、可执行的解释器选择。显式选择优先于 PATH，失效时报告错误，不回退另一个解释器。
- R556-02：取消 CPython3 minor allowlist；未被枚举的 Python3 minor 不在依赖安装前被版本白名单拒绝。保留 Python3 和既有 implementation 约束；依赖及运行能力由真实安装和检查判定。
- R556-03：复用既有用户级 identity cache、apply/reapply、bootstrap 与 resolver。identity 包含既有 lock/API/layout、implementation/major/minor、OS/architecture/ABI/platform；patch 和解释器路径不进入 identity。相同有效 identity 复用；minor 变化选取或创建对应 identity。
- R556-04：锁定依赖安装、能力 probe 和真实公开 wrapper 的 Draft 2020-12 schema 运行检查成功后才能切换 active。安装/检查失败保持此前 active pointer 和此前环境，不删除或覆盖它们；只处理本次拥有的失败 candidate。
- R556-05：解释器不存在/不可执行、非 Python3、依赖安装失败和 managed runtime check 失败返回可识别原因及可执行修复方法；不以 minor 未枚举作为拒绝原因。错误不得泄露 secret。
- R556-06：同步 canonical、现有 installer 管理的 runtime 投影、相关使用和排障文档；日常 Skill 继续使用受管 venv 与锁定依赖，不回退全局 site-packages，不因 Homebrew 更新自动重建。
- R556-07：验证结果分清真实检查、fixture-only 与 skipped。执行 accepted installer/runtime 所需的聚焦验证及一个代表性 clean/reapply，不引入 Python-minor 或完整多平台/Release 矩阵。

## 验收场景

| 场景 | 可观察结果 |
| --- | --- |
| PATH python3 与 installer 当前 sys.executable 不同 | 默认 identity 来自 PATH 当前 python3；显式解释器覆盖默认 |
| 未枚举的 CPython3 minor | identity 计算不因 allowlist 失败；依赖安装按实际返回判定 |
| 相同有效 identity 重复更新 | action 为 reused，环境不重建；patch/path 单独变化不强制重建 |
| minor 变化 | 选择不同 identity 环境，检查成功后 active 才变化 |
| 解释器缺失、不可执行或非 Python3 | 稳定失败原因与修复命令，无 traceback、无 active 切换 |
| 依赖或真实公开 wrapper schema 检查失败 | 原 pointer bytes 和原环境保留；不以 probe/fixture green 冒充公开运行检查 |
| representative clean + 显式 reapply | PATH Python 无 jsonschema 仍通过受管依赖与公开 wrapper；canonical/installed equality、drift、sidecar 和 mode 检查结果真实记录 |

## 非目标与保护边界

不修改系统 Python/Homebrew；不自动清理旧环境；不改日常 Skill 业务语义；不升级业务仓；不发布软件 Release；不开始 #557；不触及 backend #148、#149/PR #526 或其资源。完整多平台/Release 与 Python-minor 兼容矩阵不属于本任务。

## 设计承接

来源设计承诺的唯一 retain/change/reject 矩阵由 design.md 持有。这里定义整体需求，不代替 Architecture 判断、Planning Approval 或 Activation。
