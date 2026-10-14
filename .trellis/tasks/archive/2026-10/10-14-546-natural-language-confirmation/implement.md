# #546 实施计划

## 顺序与职责

1. Main按 design.md 的唯一来源处置矩阵维护公共 Interaction Budget 与必要spec/Docs；先由原RDT owner落实 `ssot_first` 的最小独立贡献。
2. Trellis implement子代理负责 canonical workflow、现有阶段Skill薄引用、平台overlay源和README加载入口，读取当前文件与project specs；不修改installed运行副本、runtime、脚本、schema、registry或public API。不得覆盖其他人的改动。
3. Main核对六项需求及无重复正文；Trellis check子代理提供完整scope语义检查和定向执行证据。原Phase2 Architecture/Check门禁仍按installed graph执行，子代理测试不冒充正式gate。
4. 存在真实finding时按原owner修订并刷新受影响门禁；提交、推送、PR、合并、收尾各保留原独立动作边界。

## 唯一 Delivery Policy

`full`：当前一个交付单元覆盖六项交互要求、公共正文、所有受影响的声明平台源引用、RDT trace和定向验证；当前accepted scope内无剩余切片。

完整交付条件：六组场景的合同语义闭合，canonical/source投影及必要格式校验通过，原Check与完整Branch Review无未决finding，结果明确区分source/static与真实客户端。旧dogfood同步由原安装/迁移owner在合格完整迁移后承担，已由来源评论排除当前阻塞；客户端行为验证和完整Release矩阵不借本任务宣称完成。

## Docs SSOT Plan

`ssot_first`，唯一reconciliation consumer是原Phase2 Check前的 `guru-maintain-requirements-design-test-ssot:task_impact_sync`；shared promotion仍归同一owner。贡献root与trace规则见 design.md#D546-05，不复制公共正文。实际结果只由贡献的test.md持有。任何RDT scope revision返回原Author，不能由implement子代理扩张范围。

## 验证计划

| 编号/场景 | 入口、观测与缺陷检测 | 证据边界 |
| --- | --- | --- |
| V1 / S546-01..05 | 语义读取完整Interaction Budget和原owner入口，逐项审查普通聊天、自然语言、已有授权、迟到/重复答案、选择/澄清、未回答、强制审批与mapped接续 | 发现遗漏、矛盾、额外确认或授权扩大；这是合同审查，非native客户端行为 |
| V2 / S546-06 | 现有source runtime validator：完整canonical包/Interface/workflow与平台源装配检查；通过source managed Python调用 `runtime.validate --root . --mode source --json` | 结构/装配证明；不改验证器，不声称安装或语义pass |
| V3 / S546-06 | 读取声明平台清单及所有改动overlay，执行现有 `test_guru_platform_inventory.py` 的相关投影检查，核对Markdown、JSON、TOML入口能够加载同一公共locator | 发现缺失或错误引用/格式；同源静态投影不等于真实平台执行 |
| V4 / 全范围 | `task.py validate`、官方context读取、`git diff --check`；审查完整tracked/untracked diff | 保证任务上下文与改动范围；不运行无关代码编译或全量矩阵 |
| V5 / 安装边界 | 记录基线旧dogfood与canonical的已知差异；若执行既有drift只作诊断，未运行installed/reapply/drift单列 | 不在旧target调用apply，不新造部分安装器，不将预期旧版本差异当本task缺陷 |
| V6 / 客户端 | Codex/Claude/Cursor真实交互若没有运行环境和完整兼容安装，逐个平台标为未验证 | 不用脚本、文本比较或fixture宣称已消除真实客户端对话框 |

不新增镜像实现的文本单测；只有现有验证确有行为覆盖缺口且范围要求时才补必要测试。不执行完整多平台throwaway/installer/upgrade/release矩阵，不新增授权证据或question状态。

## 实施与发布边界

本轮规划完成后，展示当前三份规划及启动动作，由原workflow取得当前方案接受并调用installed `guru-activate-task`。启动只将本Task从planning转为in_progress；不创建另一Task/Delivery、不迁移runtime。实施和后置检查自动接续；commit/push/PR/merge及旧dogfood迁移不由本规划自动授权。
