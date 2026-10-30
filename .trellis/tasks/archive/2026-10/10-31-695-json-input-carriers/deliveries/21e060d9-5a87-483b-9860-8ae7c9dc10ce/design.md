# D1：JSON 载体读取与 Bind 双输入设计

## 1. 设计目标、需求承接与内容基线

本方案承接本批 PRD D1-R1–R6、D1-AC1–AC4，完整交付整体 #695，不建立后项。development baseline B 为 `8d746ce561c464ca28af4dc91adf085132e4098c`；原 `DeliveryProjection.content_base` 在无前序交付时按明确 development_base 返回同一 B。Planning H0 也是该 commit；实际实现 H 在 Check/Review 时读取，不能用 H0 代替。PR 目标为 castbox/guru-trellis 的 main，内容范围为固定 B 到实际 H。

阶段适用 authority 为 `docs/architecture/README.md` / `guru-trellis-architecture`、`00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1`、`06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`。以上后两路径相对 docs/architecture。独立 candidate_assessment 实际返回 `baseline_current / no_architecture_impact`：读取分类与 consumer 适配保持既有确定性职责和分发，不需要 Architecture contribution/ADR。该结果不代表 final_plan 或实现已通过。

## 2. 当前系统、边界与目标差额

shared `trellis/skills/guru-team/runtime/io.py::read_json` 目前以普通文件优先，否则尝试 inline JSON；`-` 读取 stdin；返回 object，非 object 也用 invalid_json。路径探测/读取 OSError 被吞，导致未读载体被描述为 JSON 无效。Bind execute 在 schema/身份操作前依次读 input 和 owner_result。

首批没有前序实现。本轮保留 mixed reader 的合法能力，改进失败分类，明确不支持非普通文件载体，并在 Bind 的任一读取之前拒绝双 -。已读正文不再重新探测路径。各 package 的后续 loader、字段验证、语义 owner、typed exits、Task/Delivery 和 session 状态协议保持原职责。

## 3. 来源设计处置（唯一）

Issue 没有指定新读取实现，而是要求 Planning 在支持进程替换与明确拒绝之间选定方案。以下是仍有效的既有规范性设计承诺；本节是唯一处置矩阵。

| 来源与承诺 | 处置 | 具体落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- |
| docs/design/current/native-compatibility.md D630-02：保留公开 inline/stdin，内部 fixture 的 stdin 不取消公开 inline | retain | 第4–6节保留每个入口原准入，非文件分支仍接受合法 inline；无新统一输入层 | 无来源修订 |
| companion-scripts.md Error Handling：package 声明 deterministic error，单一对象输出，不公开 traceback/secret | retain | 第5节沿原 code/field/status；错误说明不拼接异常、原文或路径 | 同步原 package catalog/schema/help 说明 |
| distribution.md ARCH-INT-001/006：canonical/preset/installed/声明平台投影一致，平台不带私有实现 | retain | 第7节沿原 installer、tools-only 维护、source/installed/drift 校验；无新 launcher | 无 Architecture authority 修改 |

## 4. 模块、职责与设计取舍

### 4.1 载体方案

选择**明确拒绝本次 zsh 进程替换**。shared reader 只承担原 stdin、inline 与普通 UTF-8 JSON 文件；合法 inline 仍优先于非文件的错误报告。非普通文件不打开读取，避免引入流生命周期和 descriptor 约定。替代方法是用一个 - 接收 JSON，另一参数使用 inline 或普通文件，或两份普通文件。

支持进程替换需要定义超出普通文件的载体读取与相关边界。本项正文允许准确拒绝，且完整双输入不需要该能力，因此本次不采用。拒绝只说明传输不受支持，不声称 JSON 内容错误、身份不符或业务处理成功。

### 4.2 真实消费者与修改责任

下表由当前 `from runtime.io import read_json`（含 alias）与调用点核对；修改针对这些实际读取关系，不把整个 CLI inventory 变成统一输入协议。后续 schema/owner 约束仍有效。

| 消费者 | shared reader 的参数或职责 | 本轮适配 |
| --- | --- | --- |
| guru-bind-task-session | --input、--owner-result | 共享分类及读取前双 - 检查；完整调用文档、commands/catalog/schema/help |
| guru-activate-delivery、guru-author-task-plan、guru-create-delivery | --input、--owner-result；Author 还读已定位 task.json | 继承共享诊断；不将 Bind 冲突规则推广到其他入口 |
| guru-create-task、guru-create-issue、guru-establish-task-identity、guru-establish-task-branch-binding、guru-ensure-task-checkout、guru-rebind-task-branch | 各自 --input | 继承共享诊断；保留原 profile/后续校验 |
| guru-clarify-requirements | record/check 的 --input、invoke 的 --invocation | 只继承原 shared reader 的分类，不改上下文或 envelope shape |
| guru-approve-task-plan、guru-review-contract-wording | --delivery-key | 仅此 JSON 参数继承共享读取；它们的 owner/source loader 保持原合同 |
| guru-sync-base | --invocation、check 的 --result-json | 保留原确定性 Sync 流程和输入形状，继承读取分类 |
| guru-reactivate-task | 当前 --input、适用 --semantic-result | 保留各 profile 的真实要求，继承共享分类 |
| guru-upgrade-installation、guru-upgrade-tools | 原 input/plan；tools 的 upstream-source | 继承读取分类，不改维护协议、来源或权限 |
| guru-qualify-normal-scenario、guru-qualify-solution-mechanism、guru-qualify-root-cause | 只把 - 交给 shared reader | 保留 stdin-only 准入，只有正文错误说明更准确 |
| guru-publish-task-delivery、guru-merge-task-delivery、guru-finish-task | invoke 的 profile 预读；适用 legacy owner 的 --input | 已读取的 stdin 正文直接 decode；后续原 loader 与 legacy profile 不改变 |
| shared read_json_file | 已定位内部 JSON contract 文件 | 已读正文直接 decode；保留它原有 regular/non-symlink contract 检查 |

Discovery、Readiness、Wording 的 package-local envelope loader 不是 shared read_json 的可替换公共输入层。它们仍只接受其已声明 file/stdin/envelope，不新增 inline。其他 package 自有 JSON helper 不因同名而纳入改造。

共享 `io.py` 保留一个正文 object decoder，直接服务 reader、read_json_file 和上述三个已读 stdin consumer。它只做 JSON 正文/类型处理，不创建新公共命令、Skill、DTO、模式配置或持久化。package-local `execute` 与原命令元数据继续拥有参数冲突及其 help。

## 5. 接口与数据

### 5.1 错误合同

保留原三字段错误对象 `code / field_path / remediation` 和 exit status。`invalid_json` 不重新定义为仅语法失败；本次细分通过原 code、实际参数和准确 remediation 表达，不添加类别字段或新 error code。表中说明是语义要求，不要求所有 remediation 文本逐字相同。

| 情况 | code / status | field_path | 恢复说明 |
| --- | --- | --- | --- |
| 可识别的明确路径不存在 | invalid_json / 2 | 原读取参数 | JSON 文件不存在；给出存在的普通 UTF-8 文件或该入口原支持的其他形式，不回显路径 |
| 文件探测、读取或 UTF-8 解码失败；stdin 读取失败 | invalid_json / 2 | 原读取参数 | 明确说明读取/编码失败，修复可读 UTF-8 输入；不输出 OS exception |
| 非普通文件，包括本次进程替换 | invalid_json / 2 | 原读取参数 | 载体不支持；改用该入口已支持的 stdin/inline/普通文件 |
| 空或仅空白的正文 | invalid_json / 2 | 原读取参数 | 输入为空，需要一个 JSON object |
| 已读文件/stdin 正文有语法错误 | invalid_json / 2 | 原读取参数 | 正文 JSON 语法无效，修复 JSON |
| 可解析数组/标量/null | invalid_json / 2 | 原读取参数 | JSON 顶层必须为 object；不能称为语法错误 |
| 无法区分的 mixed 字符串既非可读文件也非合法 inline | invalid_json / 2 | 原读取参数 | 保留歧义；使用明确 ./、../ 或绝对文件路径，或合法 inline/该入口支持的 stdin |
| Bind 两个参数都是 - | conflicting_arguments / 2 | arguments.--owner-result | 同时点明 --input 与 --owner-result 不能共用 stdin；只保留一个 -，另一份改为 inline/普通文件 |
| 读取成功后的 schema、身份和语义结果 | 原合同 | 原合同 | 仍由原 owner 处理，不能改称读取失败 |

Bind commands 增加已有 `conflicting_arguments` 声明，catalog 同步；参数 description 说明支持形式和双 - 限制。不能把两个必填 flag 写入无条件 conflicts 列表，否则所有合法双输入都会被拒绝。公开 error schema 仍允许相同三字段与 string code；其 description 补足上述边界，不破坏原 schema id/形状。shared reader 的真实 owning catalogs、参数说明和公开错误 schema 中若存在比实际更窄的描述，同步该描述；不得改与本次读取无关的 error code 语义。

现有错误消费以原 code/field/status 承接；检查实际 caller 和测试对 invalid_json 的处理。Bind 非法双 - 从 invalid_json/owner_result 变为 conflicting_arguments/arguments.--owner-result；明确迁移说明指导按 exit2 和新分类处理该无效调用。没有新 public success output、Task 字段或数据迁移。

### 5.2 完整正常调用

package 文档提供两份普通文件的完整示例，以及一个 stdin 加另一份 inline 的完整示例。示例使用原五种 Bind profile 中适用的一个及真实 TaskId/generation；不使用 `<(...)`、FD 或新增总 envelope。可执行说明须包含前置：已通过原 Identity/Ensure、当前 session 确实适用该 profile，owner 已完成原语义 gate。参数载体示例不构造 gate pass或虚构任务。

本 Task 的正常验证可使用当前真实 TaskKey、已读 current session 和原 resume profile 构造对应 input/owner；只观察读取后原合法出口，保留同一 Task/Delivery selection。不执行业务 #961，也不声称示例替代任何身份或语义判断。

## 6. 状态、顺序、正常与失败流程

不新增状态。Bind 顺序为：解析 CLI → 检查双 - → 读取 input/owner_result → 原 schema 验证 → 原语义结果与 Task/session 一致性校验 → 原操作/typed exit。

shared reader 的读取顺序：

1. `-` 只读一次 stdin，读取失败返回读取错误；成功进入正文 decoder。
2. 对其他 mixed 字符串探测现有普通文件；普通文件保持原优先级，包括原已支持的 symlink 到普通文件。读取或 UTF-8 失败就报告真实读取错误，不把文件名当 inline。
3. 非普通文件或未定位文件时仍尝试合法 inline JSON。合法 inline 和原非 object 类型语义不因文件探测失败而改变；合法长 inline 不因文件名过长而失效。
4. inline 无法解析时，按已知载体事实返回第5节的准确说明。明确绝对或原生 ./、../ 是显式文件定位；单凭包含斜杠、文件后缀或猜测不是分类依据。裸相对名与非法 inline 的剩余歧义公开说明。
5. 已读正文不重新走路径探测。decoder 区分空正文、语法和非 object，不回显 JSON 或本机路径。

## 7. 恢复、兼容、迁移与集成

直接修改原实现与消费者，不保留旧读分支、兼容 adapter、第二 parser 或 fallback 开关。保留原合法载体和类型是本 Issue 明确要求，不是新增长期兼容层。失败发生在读取或参数层时，调用方修正载体/内容再调用原 wrapper；没有新恢复协议或 checkpoint。

`MIGRATION-695.md` 说明载体拒绝、shared/mixed 与 envelope-only 的不同准入、双 - 错误变化、普通文件/单 stdin 替代及 matching preset 采用。新错误说明不意味着所有 CLI 已支持同一输入形式。

canonical 修改经原 Guru tools-only 维护同步当前 Task checkout 的 installed runtime、共享/声明平台 projection 与 managed specs，保留全部 Task/session/private controls。按仓库要求运行原 `apply.sh --repo .` 并如实处理旧数据 preflight 拒绝；不得 bypass、手改 manifest/hash 或迁移无关 archive。再用原 `check-dogfood-overlay-drift.sh` 和 source/installed validator 核验实际 bytes/mode/sidecars。具体维护写集在执行前单独展示；当前规划不授权它。

本项不改 installer、workflow graph、上游 source lock、官方 hooks 或平台私有入口行为。官方 update 后恢复依赖原 marketplace/preset/overlay，不能靠对生成文件的一次性 patch。检查此分发责任不增加 clean throwaway、额外安装或多平台矩阵。

## 8. 验证设计

| 验证 | 对应需求/AC | 层与可观察结果 | 限制 |
| --- | --- | --- | --- |
| V1 | D1-R1/R3/R5；AC1/2 | shared io 单元检查合法 inline/stdin/普通文件、原非 object、已知读取/空/语法/歧义及敏感回显边界；每个用例验证不同真实缺陷 | 不推定业务或平台会话成功 |
| V2 | D1-R2/R4；AC2/3 | Bind 原 wrapper 检查明确 zsh 拒绝、双 - 读取前冲突，以及完整正常双输入；原 Bind runtime/contract/recovery 测试检查原 gate/selection 未变 | 不操作 #961，不增加 FD 协议或专项回放 |
| V3 | D1-R1/R6；AC1/4 | 三个 profile 预读 consumer 的已读正文直接解码；stdin-only qualifiers 和独立 envelope loader 保持准入，命中受影响既有测试 | 不做全部 CLI 重构或全 lifecycle 重跑 |
| V4 | D1-R5/R6；AC4 | source/installed package、help/error schema、canonical/dogfood/声明平台、mode、reapply/drift 和递归 sidecar 检查 | 不代表全 OS/平台实际 Agent 或 Release 矩阵 |
| V5 | 全部 | 原 candidate Check → RDT 最终整合 → 重绑 final candidate/Check → commit → 独立完整 Branch Review → readiness；语法/JSON/Bash/Task/diff 基础检查按既有要求执行 | 尚未执行，不预填 pass；SKIP/环境阻塞保留 |

## 9. Canonical 引用、本轮差额与实际未决项

R630-02/D630-02/T630-02、T630-07 的公开输入与分发职责保持。新增完整 JSON 载体能力单元由原 RDT owner 按 implement 第6节处理；不改变 #630 其他历史验证和矩阵责任。原 package SKILL/commands/errors/schema、canonical companion-scripts 及必要 README/migration 承载实际调用合同。

Architecture candidate 判定无影响，故不制造 contribution/ADR、GAP 或 shared baseline 写入；final_plan、Phase2 与 Branch Review 仍各自执行原 owner 判断。没有剩余产品选择。实现/安装/现场结果均未验证；共享 helper 的 decoder signature 与最小文件拆分属于本方案职责内实施细节，不新增公共协议。
