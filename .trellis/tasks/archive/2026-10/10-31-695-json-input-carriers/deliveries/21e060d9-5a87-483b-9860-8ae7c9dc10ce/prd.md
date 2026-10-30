# D1：JSON 载体读取与 Bind 双输入需求

## 1. 整体来源与术语

整体 authority 为 `.trellis/tasks/10-31-695-json-input-carriers/prd.md`，本批 scope_ref 选择 R1–R6、AC1–AC4。其 accepted_scope 精确 revision 由当前 task.json 保存；本批 planning_root 为 `deliveries/21e060d9-5a87-483b-9860-8ae7c9dc10ce`。Direct Source 为 https://github.com/castbox/guru-trellis/issues/695 的六项行为与非目标，当前无评论。

来源角色：Issue 与整体 PRD 是要求；`docs/requirements/current/native-compatibility.md` R630-02 是原输入兼容约束；`docs/design/current/native-compatibility.md` D630-02 是既有职责约束；当前源码只证明行为。载体与 JSON 正文、语法失败与顶层类型不符保持整体 PRD 的区别。

## 2. 整体与本批目标、非目标

本批完整交付 #695：明确实际受影响命令的载体准入，修复读取诊断，提供 Bind 双输入完整调用并在读取前拒绝双 stdin，同步必要错误/help 与分发。

保持原 Task/Delivery、session、语义 gates 和原子能力。不实施 #694/#693/#692 或业务 #961，不统一全部 CLI，不支持任意设备/流，不改上游/全局包，不新增并发、锁、TOCTOU 或额外验收。没有业务 API、数据库或持久化身份变化。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首个 Delivery，尚无前序交付。起点为 main `8d746ce561c464ca28af4dc91adf085132e4098c`。#697/#698 已合并，原机制审核能力已存在。公共 current 为本 key 的 planning，尚无 Planning/Check/Review pass。

原读取器仅以 is_file 决定是否读路径并吞 OSError；原 Bind 顺序读两个参数。原 wrapper 已重现进程替换 `invalid_json/input` 与双 - 的 `invalid_json/owner_result`。这些结果不证明业务或完整合法 Bind 成功。

本批负责六项行为及兼容/分发；整体 Completion 仍须检查全部 accepted scope、实际验证与未分配工作。Delivery 合并不自动关闭 Issue 或归档 Task。

## 4. 本批调用方、场景与流程

| 场景 | 前提与触发 | 要求结果 |
| --- | --- | --- |
| D1-S1 原合法输入 | 原公共调用方使用其命令支持的 stdin/inline/file/envelope | 保留 object 与字段验证、原准入和下游结果 |
| D1-S2 读取/载体错误 | 输入可可靠识别为不存在路径、读取失败、空内容或不支持载体 | 指出真实类别、参数与恢复；不回显敏感原文或路径 |
| D1-S3 JSON 内容不符 | 已读正文有语法错误，或可解析但顶层不是 object | 前者说明语法，后者说明顶层类型；不能放宽类型或把类型叫语法错误 |
| D1-S4 Bind 双输入 | 原 wrapper 同时接受 --input/--owner-result | 完整正常调用可执行；两个 - 在读取前报冲突并给替代 |
| D1-S5 维护分发 | 原 canonical/preset/声明平台机制应用变更 | 实现与 commands/catalog/schema/help、dogfood/installed projections 一致；原升级/sidecar 规则保持 |

## 5. 完整行为、条件与约束

- D1-R1 → R1：按 shared reader 真实调用关系记录命令与参数。共享修复不向 package-local envelope-only loader 增加 inline，不统一不同入口。
- D1-R2 → R2：方案明确支持本次正常 zsh 进程替换或明确拒绝，并给准确诊断与可执行替代。不保留未读路径自动当语法失败的 fallback，不扩张任意设备/流。
- D1-R3 → R3：区分能可靠判断的不存在、读取失败、不支持载体、空输入、语法和 object 类型。混合字符串歧义不靠含斜杠猜测；保留合法 inline 并说明明确路径写法及歧义边界。仅正文已读且确有语法错误时描述语法失败。
- D1-R4 → R4：完整调用使用原公开合同的两份输入；读取前拒绝两个 -。不新增 FD 协议、总 envelope 或通用流层。
- D1-R5 → R5：保留既有合法输入与字段验证。错误 code/field_path/status/remediation 与受影响命令、catalog、公开 schema、help 一致。invalid_json 既有含义包含非 object，不能全局改成仅语法；能复用原 code 时不增加 code，不兼容变动须明确迁移。
- D1-R6 → R6：确定性 runtime 负责读取/分类/schema；原 Skill 持有语义判断、typed exit 与恢复。按原机制同步 canonical/dogfood/实际声明平台。

来源没有约定新的具体载体实现；本批方案及来源设计处置由后续 design 第3节唯一维护。R630/D630 原公开 inline/stdin 兼容和 runtime 分工仍须保留。

## 6. 本批验收、验证方式与未决项

| AC | 对应行为 | 原流程内验证入口与预期 |
| --- | --- | --- |
| D1-AC1 → AC1 | D1-R1/R5 | shared/kernel 与实际消费者合法调用保持准入/object/字段验证；清单可从 imports/调用核对 |
| D1-AC2 → AC2 | D1-R2/R3 | 原 wrapper/读取入口的 zsh 载体处置符合选定方案；能识别的载体/读取、正文语法及顶层类型错误说明准确、无敏感回显 |
| D1-AC3 → AC3 | D1-R4 | 文档给出的完整 Bind 调用沿原 wrapper 执行；双 - 返回读取前冲突与替代方法 |
| D1-AC4 → AC4 | D1-R5/R6 | 错误和 help 合同与实现、canonical/installed/dogfood/声明投影一致；沿原升级、reapply、drift/sidecar 门禁核对 |

没有未决产品问题。技术方案须经 Author candidate、独立 Architecture、Wording 与 Approval；尚未完成，不在此预填通过。验证只沿当前开发/Check/Review/升级流程，不增加专项回放、A/B、native eval、固定数量、耗时或额外安装/多平台矩阵。实际 SKIP 保持真实边界，不推定业务现场或 Release 成功。

## 7. Canonical 引用与本轮差额

R/D/T：`docs/requirements/current/native-compatibility.md` R630-02、`docs/design/current/native-compatibility.md` D630-02、`docs/test/current/native-compatibility.md` T630-02/07 保留原公开输入与分发边界；本批补充具体读取/载体诊断及 Bind 入口。具体新行为的 durable 文档与测试追踪由方案中的唯一 Docs SSOT Plan 决定，不接管 #630 历史矩阵。

Architecture：`docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` 与 `04-integrations/distribution.md`（均相对 docs/architecture）拥有 current authority、机制审核和原分发职责。是否产生 Architecture 影响由独立 reviewer 判断，不能用本 PRD 预选结论。现有 shared kernel 与 package-local ownership 保留，候选不得产生第二身份、状态或语义 authority。
