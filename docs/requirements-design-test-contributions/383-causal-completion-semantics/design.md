# #383 设计责任增量

状态：reviewed_promoted；继承 immutable current-main-0.6.17-guru.79，current successor 与 Architecture 为 .80/active，晋升 preimage 为 .79。
[共同语义](../../../trellis/presets/guru-team/spec/workflow/causal-completion-semantics.md)拥有正文；
以下责任是 implementation locator 与 owner 的引用。

| Responsibility | 当前实现与直接 consumer |
| --- | --- |
| D383-01 | 新共同 spec + 既有 installer MANAGED_SPEC_PATHS 安装映射；installed spec 由七个现有 owner 读取。版本为 1，identity 是 locator/version/current bytes。 |
| D383-02 | qualifier、Planning、Check、Branch、Delivery、Completion、base reconciliation 的 SKILL/contract 显式加载 spec，各自独占本阶段判断。 |
| D383-03 | 原 public Interface/typed exit/consumer 不变；Check 原 invoke 对已选 reapprove_plan 投影 current_scope 与 scope_change_required proposal refs，保留修复目标的补充调查可由原 Planning consumer 承接；clarify_requirements 仍只投影 scope_change_required。Completion 的 Delivery/Reactivate evidence slot 集合及 anchor 不变；pending 无新证据时等待。 |
| D383-04 | tests/causal_cases.json 的 host 期待答案与 native facts 投影分离；run_native_causal_eval.py 将实际 AI 结果原样交给 installed record/check/invoke。运行结果只由唯一 Test 承接。 |

qualification 只负责准入；Check/Branch 审本阶段真实行为；Delivery Review 审 payload，Publish 执行；
Completion 审 whole-task scope，Closure 执行 source disposition。global workflow graph 不增加节点。
直接修改现有 owner；root 临时 missing-SSOT 文案退出，没有 stub/adapter/双读或第二 state machine。
Architecture contribution 保持 task-isolated；ADR 与 shared-current promotion 由原 owner 决定。
