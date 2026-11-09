# #760 D1 worktree 配置路径设计

## 1. 设计目标、需求承接与内容基线

本批承接同目录 PRD 的 S1—S4、AC1—AC4，整体要求由 Task 根 prd.md 拥有。开发基线 B 与 Planning H0 均为 `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`，来源为本次显式 main 基线；PR 目标为 main。最终 H 由实际实现和提交决定。

阶段适用 authority：`docs/architecture/README.md` / guru-trellis-architecture，`docs/architecture/00-foundation/design-constitution.md` / guru-trellis-design-constitution-v1，`docs/architecture/06-governance/change-contract.md` / guru-trellis-architecture-change-contract-v1。实际独立 candidate_assessment 返回 architecture_impact / target_native；decision refs 为 ARCH-FND-002、ARCH-FND-004、ARCH-DOM-022、ADR-RUNTIME-LOCATION。该结果只准入方案写作，不代表 final_plan 或实现通过。

## 2. 当前系统、边界与目标差额

没有前序 Delivery。`guru-create-task/runtime/invoke.py::_plan` 直接接受 checkout_root；`guru-select-workflow-mode/runtime/environment.py` 对空 root 使用调用 root.parent；task-free 合同只说明普通 Git 新建。现有 acquisition、Task 身份、绑定、资源归属和恢复继续由原 owners 承接。

差额是共享确定性位置事实及其三个 consumer：环境查询、正式 Task 配置生成创建、task-free 普通 Git 创建。路径事实不成为 Task 身份，不保存映射，不选择业务策略。

## 3. 来源设计处置（唯一）

| 来源与条款 | 原承诺 | 处置与落点 | 理由及影响 |
| --- | --- | --- | --- |
| Issue #760 行为1 | live topology 确认 primary，配置相对 primary | retain，第4、6节 | 修复首次路径偏差；不猜 common-dir 父目录 |
| Issue #760 行为2—3 | AI 选择，脚本解析核对；两个原入口 | retain，第4—6节 | 复用事实职责，保持执行 owner |
| Issue #760 行为4—5 | 配置生成、显式、已有/恢复分流 | retain，第5、7节 | 不把生成 root 变成 allowlist |
| Issue #760 行为6 | 不重定位原 Task 或改变身份归属 | retain，第6—7节 | 恢复先分流，不重算新建目标 |
| Issue #760 行为7；配置模板 | 复用 owners，明确公开迁移，无额外台账 | retain，第5、7节 | 加性输入迁移；退出错误生成路径语义 |

## 4. 模块、职责与设计取舍

在现有 shared runtime 内提供 worktree 路径事实能力。优先复用现有 Git/config 基础；若独立 `runtime/worktree_paths.py` 更内聚，同步闭合 runtime inventory。它只读取 topology、worktree_root 和路径，不调用 Task validator 或创建资源。三个当前 consumer 足以支持共享，避免各自复制解析规则。

primary 候选来自 live Git worktree topology、可用 core.worktree，或实际调用位置的 gitdir==common-dir 事实。逐候选核对实际 toplevel、gitdir/common identity，排除 linked 位置冒充 primary。不能盲信 porcelain 首行：separate-git-dir 可将 metadata 目录列为首行。无法唯一确证时返回 primary_anchor_unavailable，不能推测相邻目录或新增映射。

配置源为确证 primary 的 `.trellis/guru-team/config.yml`。空值解析到 primary.parent / (primary.name + '-worktrees')；相对值对 primary 解析；绝对值直接解析。linked 空模板没有独立选址意图；调用位置存在非空 root 且解析后与 primary 项目 root 不同时，准确报告配置冲突，不覆盖配置。路径中的正常空格和引号由既定配置标量语义处理，不扩大为完整 YAML 框架。

AI 在原 Skill 中先读事实，再选择新建/采用、命名和真实显式位置。正式 Task 使用原 acquisition；task-free 仍执行普通 Git。无需新 Skill、锁、缓存、路径账本或清理机制。

## 5. 接口与数据

正式 create-task 的 acquisition 加性提供 `path_source=configured|explicit` 与 `worktree_name`。configured 仅用于 provision_linked_worktree 的新目录（new_branch 或 existing_branch），需要单个目录名及绝对 checkout_root。创建前计算 root/name，并与计划 checkout_root 比较；不一致返回稳定诊断，不能静默改路径。explicit 保留原绝对位置合同。adopt、existing_checkout、recover_created_task_result 不受生成位置约束。

未提供新字段的已发布调用继续其原绝对 checkout_root 语义；当前 AI 自行生成新位置必须显式 configured，不能从其自行填入的绝对值推断用户选址。旧调用的实际消费者是已安装的 create-task 公开输入及其创建/恢复脚本。兼容 owner 为原 create-task；当调用方更新为新策略字段后，该调用的省略字段用法退出。兼容不增加另一 executor，原输入仍由同一公开 schema 和 runtime 消费。

环境 `check-env.sh` 保持原入口，worktree_root 改为按项目锚点解析的绝对 root；输出必要 primary/config 来源事实供 AI 核对。增加 `--worktree-name` 与 `--checkout-root` 供配置生成预检：前者生成目标，后者在提供时验证计划一致。命令 declarations、error catalog 和帮助同步。task-free 使用该预检的实际目标执行普通 `git worktree add`，创建后以 Git 注册与实际 root 读回；不调用 Task acquisition。

仅保留直接 consumer 必需的调用期字段。typed exits、Task/session/Delivery、C4/C5 与持久数据格式不变。

## 6. 状态、顺序、正常与失败流程

1. 原 owner 读取调用位置、topology、配置与当前身份。已有采用或恢复先沿原路径分流。
2. 配置生成策略解析 primary/root/name，展示并核对绝对计划。真实显式位置使用原合同。
3. 在任何 branch/worktree/Task 创建前核对 configured 目标；路径失配、配置冲突或锚点不可确证返回准确诊断，原 owner 修正后重入。
4. 正式 Task 继续原 acquisition/materialize/binding；task-free 执行普通 Git，再重新检查 linked/non-base 位置适用性。
5. 直接后继读取实际目录和 Git 注册。无新生命周期状态、授权记录或位置映射。

## 7. 恢复、兼容、迁移与集成

原 Task recovery 使用已验证绑定和原目标，配置变化不重定位它。existing_checkout 和 invocation adoption 保留原身份、干净/位置适用性要求。显式 root 外的新位置仍合法。

`MIGRATION-760.md` 说明新策略字段、旧绝对输入、省略字段的支持边界、环境 root 输出修正与受影响 callers；当前 canonical Skills 直接迁移到 configured 正向入口。旧已安装工具继续其匹配版本，采用新能力通过原 tools-only owner 同步完整工具投影，不迁移 Task 数据。不恢复 workspace_mode:current 写 primary。

共享 current 文档先准备完整隔离 proposed。独立 phase2 与 candidate Check 后，由原 RDT/Architecture owners final_integration 读真实目标、整合并写回；实现重新绑定 actual after，再最终 Check 和 committed Review。

## 8. 验证设计

| 验证 | 对应 | 入口、输入及独立观察 |
| --- | --- | --- |
| V1 | S1/AC1 | 真实 Git fixture 下解析空/相对/绝对 root；代表性 primary、linked、detached 调用得到同一 root；外置 gitdir 可确证与不可确证分别观察 |
| V2 | S2—3/AC2 | 正式 create-task 公开入口创建 configured 目标；检查实际目录、Git 注册、原后继绑定。正常错计划在首副作用前拒绝，纠正后成功 |
| V3 | S2、S4/AC2—3 | 环境公开预检→task-free 普通 Git 创建→后继位置读回；无 Task 身份。复用原显式新位置、采用与恢复回归，补配置变化不重定位的差额 |
| V4 | AC4 | 命中 package/runtime tests、source/installed validators、原 tools owner dogfood 同步、drift、sidecar、JSON/Bash/内存compile/diff 检查 |

已有 acquisition 测试证明其声明的显式创建/采用/恢复；不重复全生命周期矩阵。新测试必须触及实际配置 consumer，不能只比较常量或测试自己的 mock。脚本测试不声称完整 Agent 业务链或生产效果。证据足以回答要求后停止额外实验；完整多平台安装/升级/Release 不在本项验收。

## 9. Canonical 引用、本轮差额与实际未决项

RDT 现行 `docs/{requirements,design,test}/current/runtime-location.md` 保留原能力，补路径生成行为、接口迁移与验证。原 RDT owner 在 `docs/requirements-design-test-contributions/760-worktree-config-path/` 准备完整 proposed。Architecture 在 `docs/architecture/contributions/760-worktree-config-path.md` 及同名 proposed 目录准备 ARCH-RUNTIME-LOCATION 的完整差额；既有 ADR-RUNTIME-LOCATION 的独立身份与原 owner 决定适用，不新增平行 authority。原 promotion owners 拥有晋升。

没有需求或方案阻塞问题。锚点事实不足是明确运行诊断，不是猜测路径的许可。实际测试和分发结果尚待实施，不预填通过。
