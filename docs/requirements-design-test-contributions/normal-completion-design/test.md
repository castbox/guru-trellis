# 正常完成与协调成本：本地验证记录

状态：本地实现候选；正式候选 Check、final_integration、最终 Check 和 committed Review 尚未完成。本记录只写实际执行，不预填这些阶段结果。

## 范围与入口

Task `normal-completion-design` / generation 0，Delivery `850accc1-21f2-47ce-86c6-8212cec58bd7`。固定 B 为 `80fc24eed3d4deb2dd0fc63126c0affb9789d365`。当前源码只改三个 canonical 方法文件；RDT shared current 未写，三份完整 proposed 由原 owner 后继集成。

验证采用所选 Delivery V1—V4：实际方法及消费者的语义检查、三个原 package `test_contract.py`、命中引用存在性、diff 格式与完整 RDT 拟写核对。不新增锁定文案的测试，也不运行原历史八次 native、完整 CI、镜像或全平台安装矩阵。

## 实际观察

### 实现自检与真实消费者

逐段检查三个 canonical diff 以及 Approval、Check、Branch Review、独立 Review 的既有方法引用。默认不准入、作者与审核方主动尝试、跨对象成本及原方案已最小的边界在 Architecture 唯一正文；Root Cause 和 Author 只补各自消费。没有新增公共字段、状态、owner、资格层或入口清单。本地实现者的推理和引用检查不替代后续独立审核或实际 Agent 行为证据。

以本轮要求涉及的正常时序核对实际正文：

- 独立账号稳定配置读取却共同推进 revision：先从各账号可按原配置完成的直接路径出发，额外共享写不能凭保护标签或旧测试准入。
- 初始化锁包慢模型、持续入流却等待整批最慢任务：正文要求主动尝试缩小临界区及移除不必要串行阶段，且核到最终结果，不以较快 ACCEPTED 掩盖后续等待。
- 必要短事务或资源容量限制：依据真实资金/资源约束及简单替代可行性判断保留，不按名称禁用。原方案已最小时解释依据，无需虚构替代。
- 存量缺证与已证缺陷：前者有界调查、不擅删或批准扩用；后者由原 owner 承接有界纠正及必要消费者。原公共路由及无关工作的边界保持。

以上为实现自检，不是负载实验、原生 old/new 对照或正式 Check 通过。

### 定向命令

| 实际命令 | 实际结果与范围 |
| --- | --- |
| `python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-qualify-root-cause/tests -p test_contract.py` | 2 项通过；验证已有示例和 consumer schema 投影，不证明方法运行效果。 |
| `python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-author-task-plan/tests -p test_contract.py` | 2 项通过；验证原 profiles 和 consumer 投影保持。 |
| `python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/tests -p test_contract.py` | 首次 40 项均在 setUp 因未设置 `GURU_UPSTREAM_DELIVERY_SCRIPTS` 失败，未进入断言；未记为通过。 |
| 设置下述 matching provider 的 `GURU_UPSTREAM_DELIVERY_SCRIPTS` 后执行同一 Architecture 命令 | 实际执行 40 项，34 项通过、6 项失败，316.290 秒。失败均位于 fixture 只读前后文件快照相等断言，详见下文；没有跳过或记为通过。 |
| `git diff --check` | 通过，检查实际 tracked 修改的格式。 |
| 对本贡献 Markdown 执行本地路径存在性和尾空白检查；完整 proposed 按最终 target 解析相对路径 | 7 份 Markdown、45 个本地链接均存在，无尾空白；只是路径/格式证据。 |
| `git diff --exit-code -- docs/requirements/current/knowledge-maintenance.md docs/design/current/knowledge-maintenance.md docs/test/current/knowledge-maintenance.md` | 通过；shared current 三文件未改，仍待原 owner final_integration。 |

Architecture 测试所需 provider 已核对：`castbox/Trellis@b5067a62ed3631389346c891c20a8a70249f39f5` 的 `packages/cli/src/templates/trellis/scripts`，CLI 版本 `0.7.0-castbox.6`；该目录 36 份 Python 文件与本工作树已安装 scripts 字节一致。只读取并供临时测试 fixture 复制，没有修改上游源码、全局安装或本工作树安装。

### Architecture 六项失败与最小诊断

失败均在 `ArchitectureBaselineContractTest`，不是新增方法措辞断言：

| 测试方法 | 实际失败点 |
| --- | --- |
| `test_archived_readonly_sources_preserve_current_and_blocked_without_writes`，`review_refresh_required` 子项 | `test_contract.py:542`，`before == after` |
| `test_final_plan_does_not_hide_different_selection_or_object_mismatch` | `test_contract.py:1609`，`repository_bytes() == before` |
| `test_final_plan_reads_explicit_object_without_selecting_in_receiving_session`，`workflow/unbound` 子项 | `test_contract.py:1573`，同一文件快照断言 |
| `test_final_plan_rejects_other_task_even_without_delivery_selection` | `test_contract.py:1663`，同一文件快照断言 |
| `test_final_plan_reports_real_scope_and_checkout_changes` | `test_contract.py:1637`，同一文件快照断言 |
| `test_final_plan_retains_no_context_explicit_entry_without_writes` | `test_contract.py:1547`，同一文件快照断言 |

完整错误把大字典差异省略，不能据其显示位置推断 bytecode 或运行状态原因。为定位真实字节变化，仅对最后一项执行一次临时诊断：原 unittest loader、同 provider 与原测试方法保持，只将失败字典的报告改为新增/删除/修改路径，仍保留原相等判断和失败状态。3.499 秒后仍失败，唯一新增路径为 `.trellis/.runtime/guru-team/python/selection-v3.json`；没有删除或修改路径，也没有 bytecode 差异。本次诊断没有修改测试文件、断言预期或产品运行逻辑，不作为该测试通过。

为判断该单项是否本次引入，另用 `git archive 80fc24eed3d4deb2dd0fc63126c0affb9789d365` 导出 repo 外隔离副本，仅初始化测试所需 Git common-dir（无 commit、branch ref 或注册 worktree），沿同一已安装 Python 定位、matching provider、相同测试方法和路径差异报告运行。固定 B 仍在同一原断言失败，5.225 秒，唯一新增路径同样为 `.trellis/.runtime/guru-team/python/selection-v3.json`，没有修改或删除路径。该单项在 B 与当前候选均复现同一读入口副作用，因而不是本次三份 Markdown 修改引入；其余五项未做固定 B 对照，不据此宣称它们全部同因。

六项失败及具体影响交原质量 owner 判断。本批未改 session/selection 运行逻辑，不为纯方法范围修无关 runtime，不通过关闭字节检查消除失败，也不重跑已经通过的其它项目。当前验证到此停止，原独立审核和质量门禁仍须实际执行。

## 未验证边界

没有执行 native Agent old/new 行为对照、性能基准、dogfood/installed 更新、代表 clean 安装、业务安装采用或生产验证。源码改动和合同检查不能证明这些结果；本批 accepted scope 不因此新增整套矩阵或业务故障关闭条件。

完整目标位于 `proposed/docs/test/current/knowledge-maintenance.md`：新增 T-MECH-06/07，原 T-MECH 专项次数和历史事实保留。当前测试策略与结果分开，后续正式门禁从真实公共结果承接。
