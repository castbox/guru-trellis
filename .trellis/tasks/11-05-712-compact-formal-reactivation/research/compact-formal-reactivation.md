# Research: 精简 legacy 正式归档的 Guru 接线

- Query: #712 的最小直接影响面、固定公共候选消费方式及 native 联合验证入口
- Scope: mixed
- Date: 2026-11-05

## Findings

### 两仓责任与固定候选

Trellis #64 已由 PR #65 合入，merge 为 `ca0e8b931d19ccb87802d6866abd2113a6f707c0`。固定候选源码为 `619133c62d1487c5fbecbf9e00cea9e3f5ea52a6`，release 为 `issue-64-candidate-619133c62d14`。两包版本均为 `0.7.0-castbox.6`，maintenance API 为 `1.0`；必须按 source/build/package 指纹选择该候选，不能单凭版本号识别。

候选公开 `formal_archive_reactivation.task_families=[schema1,known_legacy]`。`inspectTaskTarget({root,task_ref,original_task_ref?})` 的 key 已可省略，返回 `key` 和 `classification`；原样 compact 输入可取得 legacy 家族和公共解释的 generation 0。Core 同时公开 `classifyFormalArchivePredecessor` 与 `validateFormalArchiveSuccessorSource`。调用方仍编写 source 投影并判断旧 Finish/业务范围资格；公共 owner 校验格式及 source 关系，执行增代与恢复。

### 直接代码影响面

| 文件 | 具体位置与含义 |
| --- | --- |
| `trellis/skills/guru-team/packages/guru-reactivate-task/runtime/shared_finish.py` | `read_shared_archive` 第75行先要求 raw generation，90–91行又排除 creator/assignee；两处都会拒绝原样十字段历史样本。应从精确 archive locator 消费公共分类/key，再独立保留 summary、Git/PR 与历史资格验证。不能在 Guru 给任意缺字段记录补0。 |
| 同上 | `_successor_at_checkout` 第132行只给 schema1 走公共 inspect；`find_successor` 第195行的 legacy exception 也只认 schema1。新增受支持正式家族应复用同一公共后继检查。 |
| `trellis/skills/guru-team/packages/guru-reactivate-task/runtime/invoke.py` | `acquire_incarnation.after_acquisition` 第197行只给 schema1 调用 `prepareFormalArchiveReactivation`，其他分支把归档移动后执行 schema2 reopen；compact 必须进入原公共正式转换分支。`execute` 的 shared archive reread 及 same-operation recovery 必须保持同一 source/key 解释。 |
| `trellis/skills/guru-team/runtime/task_lifecycle/identity.py` | `_archived_lifecycle_candidates` 第310–327行用 `lifecycle_generation(source)` 和 raw `source.source==successor.source` 校验保留前驱；compact 缺这两个结构化字段，后继再次归档时不能消歧。应消费目标安装的公共前驱关系读取，避免再实现一套 legacy generation/scope 算法。 |
| `trellis/skills/guru-team/runtime/maintenance_transport.py` | 已支持 `inspectTaskTarget`、`inspectFormalArchiveReactivation`、`prepareFormalArchiveReactivation`，现有 bridge 可直接消费新增 input 形状。`call` 的 formal capability gate 第147行仍至少要求 schema1，但并未给 compact 单独核对 known_legacy；应由选择该家族的原 owner 在公共调用前核验 capability。 |
| `trellis/skills/guru-team/runtime/delivery_projection/adapter.py` | `_installed_modules` 只加载目标 `.trellis/scripts/common`；`official_session_port` 与 `CurrentCheckoutPort` 提供目标原生身份/session 接口。这是接入目标原生消费者的现有边界。 |
| `trellis/skills/guru-team/runtime/task_lifecycle/source.py` | `task_source` 第63行起已解释规范旧 `GitHub issue: ...` scope。无需新增旧 source parser；该解释仍不能自动判断完整业务范围或扩大关闭权限。 |

目标候选 Python 的 `common/task_utils.py:197` 有非下划线的 `task_id_collisions(requested,tasks_dir,repo_root,exclude=selected)` 与 `require_unique_task_id`。它们内部已使用上游前驱解释，支持原样 compact 前驱。可以评估在 Guru 归档消歧边界加载这类目标公共入口；不要直接调用其下划线私有 helper，也不要把其内部补0/source正则复制进 Guru。具体最小 adapter 由实现 owner 确定。

### 需要同步的合同

`trellis/skills/guru-team/packages/guru-reactivate-task/SKILL.md` 第42–46行仍把人员时代归档统一交给维护 owner，且第98–105行只描述 formal schema1。应区分公共显式支持且经 AI 历史审核的 compact 正式家族与人工历史/未完成 closeout。

`trellis/presets/guru-team/README.md:235` 仍描述原 schema1 上游能力，应补入固定候选及 family 消费边界。修改公共 Skill 后，canonical、managed package 和声明平台投影须经原安装 owner 同步，不能只改 dogfood 副本。

相关规范：`.trellis/spec/workflow/index.md`、`companion-scripts.md` 的 Script Boundaries、`data-contracts.md` 的当前 Task/历史边界、`quality-guidelines.md` 的 Validation Scope Ownership，以及 `.trellis/spec/guides/cross-layer-thinking-guide.md` 的真实 producer→consumer 续接规则。全局 workflow 顺序无需因本项新增 family 改写。

### 现有测试与最小增量

- `guru-reactivate-task/tests/test_formal_archive_reactivate.py:20` 的 `prepare_formal` 目前只复制 #503 canonical schema1，并直接读 raw generation。它依赖真实 matching SDK，但 PR provider 为受控 mock；可作为定向确定性测试，不能声称实际 native AI 联合验收。
- 同文件已覆盖原档字节不变、pending 同 plan 恢复、public applied 后 local control 失败、后继再次归档及原入口检查。新增 compact 参数/fixture 后可复用这些机制，避免另建平行 recovery 实现。
- `test_delivery_reactivate.py:155–192` 已覆盖私有 receipt 丢失及 retained root 发现 linked successor；compact 正式路径还需对等证明实际公共后继检查被调用且不另 prepare。
- `test_delivery_reactivate.py:221–251` 的 independent clone 测试按原 Establish→Ensure→Bind 消费后继，是 native 接线参考，但仍是单元级受控语义结果。
- `runtime/task_lifecycle/tests/test_archive_resume_identity.py` 与 `test_identity.py` 是归档前驱消歧回归位置。新增 compact 后继再次归档用例时，保留 current Task reader 严格性，不扩大所有 legacy reader。

### 实际 native 联合验证建议

1. 使用一个隔离安装目标，同时安装固定 CLI/Core 两包及当前 Guru 完整 preset。工具更新由 `guru-upgrade-tools` 原 owner 执行；检查目标自身 native 与所选指纹一致。
2. 保留原样十字段旧档，或同样关键条件的去敏样本：缺 generation/source/schema_version，保留 creator/assignee 与规范旧 scope。用隔离 Git 历史保留交付和归档在同一 PR 的合法关系，不强行拆成两个 PR。
3. 实际 Agent 阅读旧安装/Finish合同、PRD、summary、原档及受控只读 PR facts，判断正式资格和 source 投影。再由已安装 Reactivate wrapper 执行公共分类、准入、转换、绑定及同操作续接。语义结果必须由实际 Agent 编写，fixture helper 不能制造 pass。
4. 从真实 stdout 投影 TaskId/generation/task_ref 到原 Identity、Establish/Ensure、Bind 入口；在同一安装目标运行 `get_context.py`、`get_context.py --mode continuation` 和下一 scope owner。无 Delivery 时不要为验收创建空 Delivery。
5. 对后继再次归档补充目标原生 TS/Python identity 和原 Reactivate 入口读取，证明保留 compact 前驱不会造成重复身份。不要求第二次实际增代或重复完整生命周期。
6. 分别报告公共 applied、本地 controls/session/continuation、下一 scope owner 消费。上游自带 `candidate-smoke.mjs` 的40次公共子进程证明仅覆盖 Trellis；不能作为 Guru 联合验收的替代。

现有 `tests/setup_native_fixture.py` 可在 `--repository` 指定的完整已安装空目标中保留安装，仅构造 Git/受控 gh facts 与 objective seeds；其 docstring 明确不生成语义结果。当前 helper 使用 existing implementation fixture，需要实现 owner 决定最小复用方式以引入 compact formal 样本，不能静默把 host-prepared JSON 当 native AI pass。

## External references

- https://github.com/castbox/guru-trellis/issues/712
- https://github.com/castbox/Trellis/issues/64
- https://github.com/castbox/Trellis/pull/65
- https://github.com/castbox/Trellis/releases/tag/issue-64-candidate-619133c62d14

## Caveats / Not Found

本研究只读代码、公开交付事实和候选合同，未运行安装、转换、业务恢复或 native 联合验收。历史原安装合同/正式完成资格仍须由实际恢复 owner 重核。`local_candidate` 只适用于隔离开发证据；生产 `source_locked` 的原固定源码门禁仍适用。完整多平台安装/升级/发布矩阵不属于本普通 Issue 验证范围。
