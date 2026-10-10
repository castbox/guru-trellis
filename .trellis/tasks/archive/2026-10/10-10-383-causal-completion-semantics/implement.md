# #383 实施与验证计划

## 执行顺序

1. fresh 读取 live #383 r9、current task/base、RDT/Architecture .79 与正式 Readiness；创建后保持 planning。规划措辞审查、normal/solution qualification、独立 Architecture 与 Planning approval 全部满足后呈现规划；经本轮方案接受才由 guru-activate-task 激活。
2. 激活后写 canonical causal-completion-semantics.md，再更新 design D383-02 中各 owner 的读取、本阶段判断和现有出口。删除 root owner 临时“共同文件尚不存在”段，保留资格 SSOT 与仍适用机制结论。
3. 在既有 installer 的 MANAGED_SPEC_PATHS 注册新 spec 的 canonical→installed 路径对，沿原 managed-hash/sidecar 安装机制；同步 canonical workflow/spec/package docs 和真实受影响平台入口；入口只路由，不复制共同正文。公共 I/O 保持原版；不新增 causality runtime classifier、persisted qualification、global DTO 或 wrapper。
4. 先补语义行为 eval 的事实集和 host-only 期待结果，再执行真实 native authoring 与 installed wrappers。复用当前 fixture；新增 harness 只准备隔离环境、执行 AI、运行 wrapper 和比较实际出口，不选择语义 route。将首次失败、修复与边界放唯一 Test，未完成不能填 pass。
5. 建立隔离 RDT contribution。Architecture impact/contribution/ADR 按独立 reviewer 实际结论执行；不提前改 shared current。
6. 从 canonical 运行 preset apply 同步 dogfood，然后 drift、parity、sidecar/mode 和受影响 package tests；普通任务只做定向验证。验证发现 accepted scope 内缺陷，回对应 owner。
7. fresh Phase2 Architecture/check；Task Commit 单独确认；完整 committed Branch Review 由符合独立方法的 reviewer 执行。受审贡献由原 owner expected-current promotion 后，promotion-created diff 重跑 fresh Phase2/commit/独立 Branch Review。
8. fresh Delivery Review/readiness 后单独确认 publish；PR 中文且 Refs #383。merge 单独确认。Completion 再判断 R383-01..09/C01..C21；通过 Closure、Finish、Cleanup 各自当前边界，才完成 #383；不启动 #468。

## 可修改路径

- trellis/presets/guru-team/spec/workflow/causal-completion-semantics.md：共同语义正文唯一 owner。
- trellis/skills/guru-team/packages/guru-{qualify-root-cause,approve-task-plan,check-task,review-branch,review-task-delivery,review-task-completion,reconcile-task-base}/：D383-02 的 stage-local Markdown 与真实行为 eval。
- trellis/workflows/guru-team/、trellis/presets/guru-team/spec/workflow/、README/overlays：实际消费变化的调用、导航与职责文案。
- trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py：新 spec 的 managed path registration；保持原 installer、hash 与 sidecar 行为。
- docs/requirements-design-test-contributions/383-causal-completion-semantics/；Architecture contribution/ADR 由独立判断决定。
- 安装投影 .trellis/workflow.md、.trellis/spec/workflow/、.trellis/guru-team/、.agents/skills/、.codex/skills/ 与其它 manifest-selected 平台：只从 canonical 生成。
- 本 task 三份规划及必要 context。每次 task/source/test 写入前执行 check-task-checkout-boundary.sh；只 stage 本次路径，不改并行 checkout。

若代码文件进入 3000 行边界，按 current spec 做必要小拆分；未触及历史大文件不扩大范围。脚本改动限定新 spec 的 managed-path 注册、行为 fixture 或当前正常路径证明的局部 objective bug；不借语义补丁治理其它 machinery。

## 最小可靠验证集

| Gate | 入口与观测 | 缺陷检测/验收 |
| --- | --- | --- |
| V1 当前接口 baseline | Completion 两个已选 test 节点，uv pytest/jsonschema 隔离环境 | 现有八项 transport 通过是 baseline，不是 causal pass。 |
| V2 因果行为 | native 读取实际 Skill/common spec 与 C01..C21 facts；host 独立比较 judgment 和 installed wrapper stdout | 区分抑制、修复、未知诊断/缓解、protection、等价证据与 pending；缺 native 证据保持未完成。 |
| V3 接续/唯一 consumer | 复用各 package fixture，经公开 wrappers 的 actual stdout 投影到 current consumer | 保留 Check/Branch/Delivery/Completion 路由；真实 stale reread；两种 current anchor；第二次 Delivery；completed 经 Closure。 |
| V4 安装与分发 | canonical apply、reapply、check-dogfood-overlay-drift.sh、声明平台投影、mode、zero unknown .new/.bak | 新共同 spec 被安装，Skills 实际读 installed locator；reapply 不丢语义且无漂移。 |
| V5 代表性 clean target | 仅当 V4 需要证明 clean installation，最多一个临时 repo 的 local workflow/preset install 与 affected wrapper smoke | installed 无 source-private 路径依赖；不声明完整 Release matrix 或业务生产效果。 |
| V6 语义闭环 | current Architecture、完整 Phase2、exact base/head committed Branch Review、truthful Delivery、whole-task Completion | 测试数量/字段齐全不能替代 AI adequacy；promotion 差异重新审查。 |

C01..C21 预期详见 prd.md；本计划不把 fixture production facts 当业务证据。V2 的 native 环境不可用时报告缺少的具体 owner/case，走当前未完成/blocked 路由，不以预写 assertion 代替。完整多平台 clean/existing/upgrade/workflow-switch/release-candidate matrix、远端业务部署与生产写入不属于 #383。

## 交付条件与风险

task_scope 与唯一 delivery_slice 均为 R383-01..09；remaining_work 为空的前提是实现及所有 accepted 定向验证实际完成。活动 task 自己拥有任何未完成范围；未验证事项不能挂 #468 来假称完成。

主要风险：将 root-fix 证明要求误套诊断/缓解；把普通 pending 改成 stop 或即时循环；跨阶段复制语义；失去 current merge/reactivation anchor；native eval 自证；source/parent 被错误关闭。分别由 C08..C11/C17..C18、C13..C16、V4、V3、V2 和 C20 捕获。Common version/content 变化只触发原 owner 判断后的最早依赖重审，不能制造全链 digest authority。
