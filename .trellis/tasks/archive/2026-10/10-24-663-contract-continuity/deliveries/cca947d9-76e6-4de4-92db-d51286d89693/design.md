# 当前流程合同连续性：D1 设计

## 1. 设计目标、需求承接与内容基线

本设计承接 D1 PRD 的 R1–R6、F1–F4 和 V1–V8，覆盖整体 Task 的同名 anchors。公共 DeliveryProjection.content_base 使用 development_base=main、真实 observed_target 后返回固定 B=`e9583202b67750d7b3ec2b7eab4b037c0c52a226`；Planning H0 与 B 相同。内容基线不随 remote main 推进而移动，PR 目标为 main，最终 H 在提交时重新观察。

适用 Architecture authority 为该 B 上 `docs/architecture/README.md` 的 guru-trellis-architecture、constitution-v1 和 change-contract-v1。原独立 Architecture candidate_assessment 已正式返回 architecture_impact/target_native，要求 ADR-CONTRACT-CONTINUITY；这不是 final_plan 或实现通过。

## 2. 当前系统、边界与目标差额

现有 Bootstrap、Archive Review 和 Architecture 各自拥有完整 semantic owner 与 deterministic wrapper。全局 workflow 只编排。当前四项失配分别在 Bootstrap Interface、Review example、Architecture before-authority 校验和 Bootstrap stage schema。本批直接修原声明和执行层；没有前序 Delivery，没有新总控、状态机或 persistent handoff。

## 3. 来源设计处置（唯一）

| 来源与承诺 | 处置及落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| #663 修复范围1–2：原 owner、caller 薄投影、mode/continuation/context 保持 | retain，第4–6节 F1 | 不扩输出；由原 caller 提供其已拥有的当前输入 |
| #663 F2/V6：archive 只读、无当前 Check、原 stop | retain，第4/5/8节 F2 | 只删除无效 example 字段，不改变当前 input schema 或阶段 |
| #663 范围3：严格 schema、身份与 freshness | retain，第5–7节 | 缺失状态必须逐项核真，不作 blanket waiver |
| #663 F3/V7：真实 before、固定 B、完整 H/diff | retain，第5节 absent_locators | 在现有 before_authority 增加最小明确事实；原独立 Architecture 接受此候选，无 scope 改写 |
| #663 F4/V8：原 promotion→Bootstrap→同 promotion | retain，第5/6节 | 只允许现有 phase2 投影，maintenance 不授予 promoted/final Check |
| #663 范围4–5/V4–V5：成套分发、兼容说明与真实组合 | retain，第7–8节 | 原 installer/reapply，最多一个 clean 样本，Release 矩阵排除 |
| AGENTS.md §§2/3/9：AI 语义、脚本事实、最小 public I/O | retain，第4–7节 | 不新增持久交接或授权字段；Git/GitHub 动作留原 owner |

## 4. 模块、职责与设计取舍

F1 由 `guru-bootstrap-repository-ssot/interface.json` 和 contract 明确 `exit_id→source_exit` 的 rename，seed_fields 只含 source_exit；authoring_fields 明确 profile、mode、continuation_id，必要的 repo_locator/baseline/scope/contribution 从原调用上下文保留。原 output 仍只有 repair_required；同一 caller 已持有原上下文，因此不扩大 DTO。正式 wrapper 继续核 profile/continuation。

F2 由 `guru-review-branch/examples/public-delivery-archived-review-input-1.0.json` 删除 check_result_id。原 schema、recorder、archive snapshot 和 stop 保持。回归必须从 Interface 指定 example 出发，不另造替代输入。

F3 由 Architecture active schemas、`runtime/promotion.py:check_before_authority` 和原 public consumers 对齐逐路径事实。直接修改当前合同，不新增 reader/adapter。F4 在原 Bootstrap whole-task/Delivery schema 和相关 contract/runtime 中补现有 phase2，保留 planning。全图回归放 canonical tests，复用既有 projection/schema validator。

## 5. 接口与数据

`before_authority` 新增可选 `absent_locators`：unique string array，仅允许 baseline_locator、constitution_locator、change_contract_locator 的值。省略或空集保持原有“三文件在 B 存在”的语义。列出的路径必须在 `git_revision` 的 tree 中确实不存在；未列路径仍须是可读的原 authority 文件。普通误列、漏列、错误 revision、范围或候选不一致继续 stale_identity。此集合只服务原 Architecture validator 和其声明的直接 consumer，不是恢复状态或授权。

committed_range 仍要求 before_authority.git_revision=B 且 current HEAD=review_head。当前 candidate 的 authority 文件、完整 H 内容及全部 B..H 差额必须由原 owner 实际审核。缺失集合不能替代当前文档、constitution 或语义 gate。

Bootstrap repair seed 为 source_exit，caller 补固定 profile=repair 与其原 mode/continuation/context。Bootstrap stage 只扩为 planning|phase2，phase2 用于原 final-integration maintenance。原 promotion 的 profile/stage/Task/DeliveryKey/root/continuation 留在调用期；consumer 不读私有 checkpoint。公共 error/exit id、owner 和业务状态不新增。

## 6. 状态、顺序、正常与失败流程

F1：原 owner 判断需修复→repair_required→声明 rename/authoring→同 owner repair 正向维护→实际原合法出口。不能由字段校验替代修复判断。

F2：填真实 archive example→recorder→checker→invoke→原 archived disposition stop；全过程无当前 Check 或 active gate 写入。

F3：B 无文件→Planning/Bootstrap 建立当前 authority→phase2→Check→TaskCommit H→committed Architecture(B+真实缺失集合,H)→完整 Branch Review。B 原有文件路径不变；漏报缺失或错误 current 状态均阻塞。

F4：final promotion baseline_incomplete/bootstrap_foundation→保留原调用 context→phase2 Bootstrap→维护实际结果→fresh 原 final promotion；repair 对照沿现有路径。缺原 continuation 回原 owner fresh entry，不猜造 promotion。

## 7. 恢复、兼容、迁移与集成

采用直接原位演进并成套更新受控 consumers。F1 wire output 不变，修正无法消费的声明；F2 删除的字段本来就不被当前 schema 接受。F3 是有直接当前 consumer 的 additive presence 表示，已有合法省略输入含义不变；只在 matching package/workflow/consumers 安装后使用 absent_locators。F4 additive 接受既有 router 所需 phase2，不改变 planning。旧 held 失配输入回原 owner 从当前 Interface fresh 构造，不能人工补 pass。

`MIGRATION-663.md` 明确 canonical/installed/平台成套 reapply、旧固定发行保持和 sidecar 处置；不引入长期 dual-read/adapter。实际副作用继续由原 owner 恢复。没有业务数据迁移或额外回滚协议；本地未提交修复按同 Task 继续，保留并行内容。

## 8. 验证设计

T1/V1/V3：正式 Bootstrap producer→按 Interface projection→正式 repair consumer，分别核 workflow/standalone、原 context 与普通 missing/profile/continuation mismatch。T2/V6：真实 schema2 archive 从正式 example 填身份，原 recorder/checker/invoke，前后 archive/snapshot/stop 不变。

T3/V7：隔离 B 无三 authority 的原公共 Task/Delivery 样本；真实 AI owner 执行 Planning/Bootstrap，再经 Phase2、TaskCommit、committed Architecture、完整 Review；另设 B 已有 authority 对照。受控 wrappers 使用同样输入验证确定性链，真实 owner 的判断与实际 stdout 单独报告。

T4/V8：正式 final producer 请求 Bootstrap，whole-task/Delivery 两类 caller 薄投影 phase2，consumer 后回同一 promotion；已有 repair 分支作对照。观察维护后的原 owner 实际结果，不能只看 schema 通过。

T5/V4：遍历当前 active registry 的所有 public profile examples，通过独立及 aggregate schema；遍历每个公开 output/合法示例变体，经声明 direct/select/rename/normalize 和 authoring seed 组合至目标 schema。验证 stop 的零载荷/最小 DTO；人工核动态 stage/first absence 和唯一 consumer。结果限于已覆盖输入，不能证明所有原生动态分支。

T6/V2/V5：一个代表性 clean 安装，使用当前源码完整 preset，真实 Bootstrap owner 接受 repair_required 并执行可观察基线修复；同一安装用于 reapply/平台/mode/sidecar 检查，不另跑完整矩阵。源码/installed/source checker、Python in-memory syntax、shell syntax、dogfood drift、diff hygiene 按命中范围执行。

## 9. Canonical 引用、本轮差额与实际未决项

公共细粒度接口由三个 canonical packages 和 workflow 单写；`skill-package-contract.md` 的 Public I/O、`quality-guidelines.md` 的 Validation Scope/Test Value、`subtraction-first-compatibility.md` 的直接演进约束保持。

Architecture task-owned 贡献为 `docs/architecture/contributions/663-contract-continuity.md`，ADR 候选隔离于同目录 `663-contract-continuity-adr.md`。拟晋升 change-contract 的真实 before 缺失条款与必要 ADR 导航，由原 Architecture owner 在 candidate Check 后 final_integration 写入完整单元；Planning 不改共享 current。原 RDT owner 在隔离贡献内形成 task-delivery-lifecycle 完整 R/D/T proposed definitions，最终整合并读回。没有未决范围选择；所有实现、原生验证与最终阶段结果待执行。
