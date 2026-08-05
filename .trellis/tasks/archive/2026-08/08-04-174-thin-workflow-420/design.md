# #174 设计：thin workflow 行预算压缩

## 1. 设计结论

本任务包含两个保持边界清晰的实现面：一是保持公共语义不变的 workflow 文本收敛，
二是为 #174 closeout 闭环修复一个已由 live Finalizer 路径定位的 pending-Ledger 重入
缺陷。canonical `trellis/workflows/guru-team/workflow.md` 仍是 workflow 唯一编辑源；
`.trellis/workflow.md` 是 dogfood 安装副本。runtime 修复只改变 Finalizer dirty-path
allowlist 的正常路径判定，不改变 Skill public graph 或 workflow marker。

## 2. 所有权与不变量

| 区域 | 本任务保留的 global owner | 本任务不改变 |
| --- | --- | --- |
| Public graph | 13 mandatory Skills、51 exits、28 targets | registry、package interface、projection、consumer 与 target kind |
| Phase routing | Phase 0/1/2/3 顺序、status breadcrumbs、入口标题 | `get_context.py` 所需 heading/tag 语法 |
| Boundary | workspace、Docs SSOT、Issue Scope Ledger、human artifacts、interaction、platform ownership | Skill 内部 semantic review、recorder/checker、private artifact、非 Finalizer runtime contract |
| Finalizer runtime | `prepare_closeout()`、计划拥有的 pending Ledger allowlist、verification re-entry | 不改变 publication semantic ledger、marketplace pending/passed contract 或 archive transaction |
| Distribution | canonical workflow/runtime → dogfood copies | preset installer、overlay inventory、平台 Skill 与 upstream ownership |

所有 `guru-skill-invoke`、`guru-skill-exit`、`guru-workflow-target` 和
`guru-stop-target` marker 必须原样保留；最终按 payload 集合和计数复核，而不是只看
Markdown diff。

## 3. 压缩策略

1. 记录 427 行 baseline、两个 line-budget assertion、marker payload 集合和 parser
   context 读取结果。
2. 在 canonical workflow 中识别重复的全局解释、重复的 route handoff 说明和不承载
   新语义的空白/换行；优先合并相邻句子或删除可由同一节直接表达的重复行。
3. 不删除 #161 stale handback 的 `reviewed_content_head` 语义、不删除任何 fail-closed
   规则、不把 package-owned evidence 或 route 判断写回 workflow。
4. 修改后按 canonical source → dogfood copy 同步，使用 `cmp` 检查字节一致；不从
   #132 worktree 的未提交压缩尝试复制内容。
5. 若语义 review 发现某一压缩改变了可观察边界，则恢复该语义并在其它重复说明中
   重新压缩；不得通过改测试阈值、删除断言或重写 graph 来满足行数。

## 4. Finalizer runtime 修复设计

1. 以 `verification_verified` 重入进入的既有 schema 1.2 closeout plan 为 authority，
   区分“closeout plan 声明拥有并纳入追加路径的 pending Ledger”与真正未授权 dirty path。
2. 保持 `closeout_ledger_matches_plan_semantics()`、pending marketplace evidence 以及
   Finalizer transaction 的现有绑定；修复只改变 dirty-path allowlist 在该正常重入组合
   下的投影，不放宽任意路径或跳过 plan/HEAD 校验。
3. 在 `test_finish_family_integration.py` 建立最小真实 fixture：
   `verification_verified`、schema 1.2、pending Ledger、现有 closeout plan 和重入
   `prepare_closeout()`，先证明旧路径误报，再证明修复后继续进入后续 gate。
4. 同步 `.trellis/guru-team/scripts/python/guru_team_trellis.py` 与
   `.trellis/guru-team/skills/tests/test_finish_family_integration.py`，使用现有 canonical
   source → installed/dogfood 机制，不手工 patch 安装副本。

## 5. Docs SSOT Plan

### 4.1 Strategy

`no_docs_update_needed`。本次补充的是既有 Finalizer companion runtime 的 correctness
修复和回归，不新增 Skill、schema、consumer、target、安装 API、README 命令或 durable
workflow/preset/spec 语义；规划文档本身记录新增验收边界。

### 4.2 Review and evidence

- 实现前已读取 workflow、preset、docs 与 shared guides；实现后复核
  `.trellis/spec/workflow/{index,workflow-contract,quality-guidelines,data-contracts,skill-package-contract}.md`、
  `.trellis/spec/preset/{index,installer,upstream-ownership}.md` 与
  `.trellis/spec/docs/public-docs.md` 的现有表述仍被当前 workflow 满足。
- `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、
  `README.md` 和 requirements/docs SSOT 不需要为纯行数收敛改写；若验证发现其中有
  427 行或已删除语义的事实性表述，停止实现并返回 planning 更新。
- task-local planning/check/review evidence 只记录本任务过程；不把 runtime digest、
  授权或完整验证历史写入 durable docs。

## 6. 兼容与风险

- Markdown 解析风险：保持 Phase/step heading depth、workflow-state 标签、裸 marker
  行和命令块结构；通过 context reads 与 runtime tests 验证。
- graph 漂移风险：使用 source/installed graph validators 和完整 marker 集合比较。
- dogfood 漂移风险：同步后执行 `cmp`、dogfood drift、managed installation 与
  update/reapply 检查。
- 历史误用风险：不读取或复制 #132 worktree 未提交的压缩候选；只以当前 worktree
  diff 和 current HEAD 验收。
- Closeout 风险：不得把 pending Ledger 的合法 metadata tail 处理扩大为任意 task-local
  dirty allowlist；必须用 plan semantics、reviewed HEAD 和现有 schema 1.2 contract 约束。
- 分发风险：canonical runtime/test 修改后必须同步 dogfood，并分别验证 source 与 installed
  bytes、权限、managed update/reapply 和 `.new`/`.bak` 状态。

## 7. 预期变更面

产品实现预期只包含：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/skills/guru-team/tests/test_finish_family_integration.py`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/skills/tests/test_finish_family_integration.py`

规划文档和 JSONL spec 清单属于 task-local artifact。runtime/test 变更必须严格限制为
上述 Finalizer pending-Ledger re-entry 回归；其它 runtime、Skill package、preset、
README 与 docs 不得借机修改。
