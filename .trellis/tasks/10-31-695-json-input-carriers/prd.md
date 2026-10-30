# #695 公共 JSON 输入载体整体需求

## 1. 来源与术语

| 来源 | Locator 与条款 | 角色与用途 |
| --- | --- | --- |
| Direct Source | https://github.com/castbox/guru-trellis/issues/695 ，完整正文六项行为及非目标；当前无评论 | 整体要求与完成边界 |
| 当前请求 | 当前会话的 #695 串行委托 | 仅处理本项；保持现行开发、Check、独立 Review、升级及收尾流程，不恢复已删除的专项验收 |
| 兼容性要求 | docs/requirements/current/native-compatibility.md R630-02；docs/design/current/native-compatibility.md D630-02 | 保留既有公开 inline/stdin 形式；不推定所有命令具有相同准入 |
| 错误与分发约定 | .trellis/spec/workflow/companion-scripts.md Error Handling；docs/architecture/04-integrations/distribution.md ARCH-INT-001/006 | package 声明错误；canonical、installed、声明平台按原机制保持一致 |
| 当前实现证据 | trellis/skills/guru-team/runtime/io.py；packages/guru-bind-task-session/runtime/invoke.py（相对同一 skills/guru-team 根） | 定位首次读取偏离，不作为目标行为权威 |

载体是传给参数的 stdin 标记、inline JSON、文件或原 package envelope。正文是读取载体后得到的 JSON 文本。顶层类型不符合 object 合同与 JSON 语法错误是不同事实。

## 2. 背景与问题

当前 shared `read_json` 只读取 `Path.is_file()` 成立的路径，其他字符串进入 `json.loads`，并吞掉路径操作的 OSError。zsh 进程替换提供合法 `{}` 时，原 Bind wrapper 返回 `invalid_json/input`。两个参数都为 `-` 且 stdin 为 `{}` 时，第一个读取耗尽 stdin，第二个返回 `invalid_json/owner_result`。这两项已在启动基线的原 wrapper 复现，未证明字段、身份或业务处理成功。

当前合法数组和标量也会返回 `invalid_json`。本项不能把该 code 全局重定义为仅语法失败，或通过放宽 object 要求制造成功。

## 3. 目标与非目标

目标是让真实受影响调用方理解支持的载体，获得准确且不泄露敏感内容的读取诊断，并能正常完成 Bind 双输入调用。整体完成包括必要消费者适配、错误/help 文档与原分发闭环。

不处理 #694/#693/#692、业务 #961、在途会话或模型配置、所有 CLI 统一、任意设备/流支持、身份或语义 gate 重构。不得修改上游或全局包，不引入锁、并发压力、TOCTOU、fault injection 或跨 OS 原子性。没有业务数据库或持久化身份模型变更。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前提与触发 | 要求行为与可观察结果 |
| --- | --- | --- |
| S1 合法 JSON | 原 public wrapper 调用方使用该命令原已支持的 stdin、inline、普通文件或单 envelope | 保留原字段验证、顶层类型和后续流程；不得因共享修复扩大准入 |
| S2 载体与读取失败 | 调用方传入可可靠识别的不存在路径、读取失败、空输入或不支持载体 | 返回真实类别、实际参数和可用恢复方式；不得把未读正文描述为正文语法失败 |
| S3 内容不符合合同 | 已读正文语法错误，或可解析但顶层不是 object | 区分语法与类型，保留或明确迁移既有处理；不回显原文、凭证或敏感路径 |
| S4 Bind 双输入 | 调用方同时提供 --input 与 --owner-result | 给出完整正常调用；两个参数都为 - 时在读取前返回参数冲突与替代方法 |
| S5 分发与恢复 | 维护者通过原 canonical/preset/dogfood/platform 机制更新工具 | 实现、错误声明、help 和调用说明一致；保持原 reapply、drift、sidecar 与升级边界 |

## 5. 行为要求

- R1（S1/S5，正文行为1）：根据共享读取器真实 imports 和调用链列出受影响命令，以 Bind 为直接入口。保留各消费者 stdin/inline/file/envelope 的准入差异；envelope-only 入口不增加 inline。
- R2（S2，行为2）：Delivery Planning 明确选择支持本次正常 zsh 进程替换，或明确拒绝并给准确诊断与可执行替代。实现、help 和文档一致，不留模糊 fallback；不扩至任意设备/流。
- R3（S2/S3，行为3）：对能可靠识别的不存在、读取失败、不支持载体、空输入和真正语法错误给出真实类别、对应参数和恢复方式。混合输入确有歧义时保留合法 inline JSON，说明边界；不得凭含斜杠猜测所有路径。正文已经读取且语法确有错误时才能描述为语法失败。顶层类型不符单独说明，保持 object 要求和敏感信息保护。
- R4（S4，行为4）：提供一条完整、实际可执行且符合原公开合同的 Bind 双输入调用。读取前拒绝 --input - 与 --owner-result - 的组合。无新流协议、FD 约定或总 envelope。
- R5（S1/S3/S5，行为5）：保留合法输入和原字段校验。错误变动列明 code、field_path、exit status、remediation 和现有消费者关系，同步实际受影响 commands、catalog、公开错误 schema、help/调用文档。优先复用足以表达事实的既有 code；破坏性变化提供明确迁移。
- R6（S5，行为6）：确定性 runtime 拥有读取、错误分类和 schema 检查；原 Skill 保留语义 gate、typed exits 和恢复判断。同步 canonical、dogfood 与实际受影响声明平台，保持 Task/Delivery 身份与 session 隔离策略。

## 6. 约束与依赖

启动基线为 main `8d746ce561c464ca28af4dc91adf085132e4098c`，#697 与 #698 已合入。其机制审核和归档能力是现有能力，不成为本项新的重构目标。

实际载体策略、消费者清单和最小错误映射由当前 Author/Architecture 依真实合同确定。用户无需补做技术设计。原 Task scope、Delivery、Planning、Check、Review、Publication、Completion 与 Closure 的 owner 和权限边界保持。没有新增业务 API、数据库或数据迁移；错误公共合同若发生不兼容变化仍须明确迁移。

## 7. 可观察验收与验证方式

| AC | 覆盖 | 原流程内的入口与预期结果 |
| --- | --- | --- |
| AC1 | R1/R5 | 核对真实读取消费者及既有合法输入，原 wrapper 保持准入、object 与字段验证；受影响清单可追溯到调用关系 |
| AC2 | R2/R3 | 原读取/Bind 入口接收本次 zsh 载体，结果符合 Planning 选定的支持或拒绝合同；可识别读取失败与真正语法/类型结果准确且不泄露敏感内容 |
| AC3 | R4 | 文档的完整 Bind 调用沿原公开 wrapper 可执行；双 - 在读取前返回明确参数冲突和替代方法 |
| AC4 | R5/R6 | 实际受影响错误 code/field/status/remediation、commands/catalog/schema/help 与实现一致；canonical/installed/dogfood/声明投影和原升级/reapply/drift/sidecar 检查匹配 |

验证沿现行开发、Check、独立 Branch Review、PR readiness 与升级流程。上表定义正文交付行为，不新增专项回放、A/B、native eval、固定案例数量、耗时统计、额外安装或多平台矩阵。实际执行结果按原 owner 记录，SKIP/环境阻塞不得写成通过。业务现场效果、全平台兼容与 Release 结果不能由本项局部验证推定。

## 8. 实际未决项

没有阻塞整体需求接受的产品或范围问题。载体策略和错误最小映射属于下一步技术规划；整体 scope 接受不代表 Delivery 方案已批准或可开始实现。
