# #174 设计：thin workflow 行预算压缩

## 1. 设计结论

本任务是一个保持公共语义不变的 workflow 文本收敛。canonical
`trellis/workflows/guru-team/workflow.md` 是唯一编辑源；`.trellis/workflow.md`
是 dogfood 安装副本。实现只减少 global workflow 中可重新推导的重复 Markdown
说明或排版行，不迁移任何 step-local Skill 合同到其它位置，也不改变机器可读 marker。

## 2. 所有权与不变量

| 区域 | 本任务保留的 global owner | 本任务不改变 |
| --- | --- | --- |
| Public graph | 13 mandatory Skills、51 exits、28 targets | registry、package interface、projection、consumer 与 target kind |
| Phase routing | Phase 0/1/2/3 顺序、status breadcrumbs、入口标题 | `get_context.py` 所需 heading/tag 语法 |
| Boundary | workspace、Docs SSOT、Issue Scope Ledger、human artifacts、interaction、platform ownership | Skill 内部 semantic review、recorder/checker、private artifact、runtime implementation |
| Distribution | canonical workflow → dogfood byte equality | preset installer、overlay inventory、平台 Skill 与 upstream ownership |

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

## 4. Docs SSOT Plan

### 4.1 Strategy

`no_docs_update_needed`。Issue 只要求把已有 workflow global contract 在 current
HEAD 恢复到固定行预算；不新增或改变 Skill、schema、consumer、target、安装 API、
README 命令或 durable workflow/preset/spec 语义。

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

## 5. 兼容与风险

- Markdown 解析风险：保持 Phase/step heading depth、workflow-state 标签、裸 marker
  行和命令块结构；通过 context reads 与 runtime tests 验证。
- graph 漂移风险：使用 source/installed graph validators 和完整 marker 集合比较。
- dogfood 漂移风险：同步后执行 `cmp`、dogfood drift、managed installation 与
  update/reapply 检查。
- 历史误用风险：不读取或复制 #132 worktree 未提交的压缩候选；只以当前 worktree
  diff 和 current HEAD 验收。

## 6. 预期变更面

产品实现预期只包含：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`

规划文档和 JSONL spec 清单属于 task-local artifact。现有 runtime、tests、preset、
README 与 docs 不预期修改；若实现中出现必要修改，必须证明它是本 Issue 的直接
current-HEAD 回归且不会扩张 #174 scope。
