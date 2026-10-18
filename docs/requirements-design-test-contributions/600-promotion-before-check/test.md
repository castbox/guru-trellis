# #600 验证结果与边界

本文件是本次验证结果唯一长期来源。本次包级实现和匹配安装已经完成下述目标验证。当前真实 Task 的最终 Check、committed Review 与交付结果由各原 owner 的公共结果和 PR 承接；本文不通过后续补最终 pass 或最终 SHA 制造文档提交循环。

| Test | 观察对象 | 当前证据 |
| --- | --- | --- |
| T600-01 | 稳定正常候选的独立评估、晋升、最终 Check/Commit/committed 完整 Review/consumer | Planning candidate_assessment 与 final_plan 已由独立 reviewer 实际正式调用。实现主链将由本 Task 的实际 Phase2、晋升、最终 Check、Commit 与 committed Review 执行，最终结果沿原 public consumer 承接；不以 fixture 代替。 |
| T600-02 | 原 authority 与候选的独立比较；新 CURRENT 不掩盖职责偏离；缺失/mismatch 不放行 | Architecture package 39/39（含7个新候选/晋升场景）通过；before_authority、tracked/untracked candidate 与拟写/实际差额通过真实 wrapper 校验。独立语义判断由当前真实 Architecture reviewer 执行。 |
| T600-03 | 受审写入一致、变化回程、expected-current mismatch、partial/output-loss recovery | 真实 wrapper 覆盖一致写入、candidate变化、expected-current mismatch、已完成/未完成/冲突读回及输出丢失恢复；7项新场景均通过。不扩展攻击、竞态或故障注入。 |
| T600-04 | no-change 与多 Delivery 独立路径 | no-change 的真实 wrapper 对完整candidate绑定、缺省无贡献/ADR及内容变化拒绝通过；既有Delivery fixture按独立key/planning root接续。 |
| T600-05 | finding 修复影响与完整 Review 后窄修订的正式最终结果 | Branch package 58/58通过；4项新增真实wrapper链验证原passed在checkpoint退休后恢复、合法rework清除旧slot、新Check、全部Git差额、正式新passed及Delivery Review ready接续；行为变化由fixture owner阻塞。该层不证明AI窄范围判断。 |
| T600-06 | 无 Review/SHA 循环补写，事实状态和来源准确 | 迁移及当前workflow/原owners明确取消例行post-Review晋升循环；实际本Task以最终完整Review后不补最终pass/SHA正文方式验证。完整diff语义审查仍由本轮原Check与独立Review负责。 |
| T600-07 | 三类在途状态、旧入口成套迁移与独立 reviewer/finding lifecycle | MIGRATION-600逐项承接未晋升、已晋升未完成最终Review、已完成最终Review三状态；当前旧输入拒绝，新current-only入口由真实wrapper验证。实际业务在途及其它旧安装均未宣称已切换。 |
| T600-08 | canonical/installed/平台、apply/reapply/drift/sidecar 与真实 AI 行为 | 完整 tools owner 已在本checkout返回 tools_upgraded；40 packages/124 commands安装验证通过，Shared及Claude/Codex/Cursor投影和canonical workflow/spec drift通过，conflict/sidecar均为0。22平台manifest/ownership投影检查通过；其余平台实际Agent行为未验证。完整reapply的installed/activation验证通过，conflict/sidecar均为0；四个生成的.bak已逐项核对为原受管字节并移至私有临时目录，当前文件等于canonical。受影响eval结果由其原输出承接。 |

## 已发生的正常失败与恢复

最初 Task 创建输入使用错误的 source 字段，创建器返回 `input_schema_mismatch`，没有以它宣称创建成功。改用官方 `kind=issue/disposition=exact_source` 后原创建器完成。创建调用输出丢失后，原 recovery 入口实际返回同一 TaskId/generation；没有重复创建。

独立 candidate_assessment 首次正式调用因 fresh 子会话未选择 Delivery 返回 `stale_identity`。原 bind/selection owners 恢复明确 Task/Delivery 后，reviewer 新轮次核对同候选并自行正式返回 baseline_current。此处只证明 Planning 路径的恢复和真实判断，不证明新晋升 runtime 已工作。

## 未验证边界

完整累计多平台 Upgrade/Release 矩阵、其它业务仓安装、业务采用、部署和生产效果不属于本任务，均不作通过主张。后续只补实际发生的目标验证，不用 schema、词匹配或预填绿色 DTO 替代 AI 行为。

## 已执行工程证据

Architecture package使用真实npm-installed CLI/Core `0.7.0-castbox.3` 的scripts运行39/39；Branch package58/58；Architecture authoring adapter9项通过。目标 source validator 与 installed validator 均通过。以上包级及wrapper事实不等于实际AI独立判断。

安装前普通apply被旧archive inventory缺本checkout原迁移receipt拦截，preset没有写入。原guru-upgrade-tools随后以明确local_candidate执行完整工具更新，保留Task/Workspace/AGENTS/config原字节及mode、peer/common runtime pointers；formal_fork_source_lock未验证。没有伪造迁移receipt或转换历史Task。

首次installer测试从脚本子目录运行缺少当前runtime查找上下文，后从repo root运行；19项中18通过，1项既有断言仍要求Merge aggregate1.0，而base/main和现有Interface均已是2.0。本Issue未改Merge aggregate，故此为已定位的历史测试偏差，不改生产API或无关断言追绿。

本轮受影响eval fixture首次缺Core版本元数据，原normal-scenario与solution-mechanism owners实际返回qualified_current后，仅补同来源版本文件。另一次facts置于被native transport排除的runtime路径而不可读，已改为既有排除内容hash、可传输的eval-only task evidence locator；没有投影private owner result。Architecture authoring adapter最终9项通过；Phase2 adapter结果由原定向运行输出承接。

## main 冲突整合的定向验证

PR 的实际 CONFLICTING 状态触发原 Reconcile，固定整合 main 的 #589 D7。11 个文档冲突逐项保留双方事实；Architecture 由原 owner 组合为 `.97`，RDT 保留 main `.104` 并以 `.105` 接续 #600，根需求与计划未改变。原公共结果保持历史事实，解决树和整合后的当前结果由原 Check/Reconcile/Review owners 继续承接。

整合引入 Fork `.4` 公开内容读取依赖。原 tools-only owner 使用实际配对 CLI/Core `0.7.0-castbox.4` 完成成套更新，保留 Task、配置与 peer/common 状态；第一次末端 peer-pointer 相等检查未满足而返回 resume_required，读回正常状态后沿同一 recovery ref 成功恢复，没有重建操作或改写 peer 指针。该操作仍为 local_candidate，formal_fork_source_lock 未验证。

在 `.4` 实际 scripts 上，Architecture package 39/39 通过。Branch 首轮因未设置公开 common 来源而跳过5项；补上同一 `.4` common 后完整58/58通过，无skip。新alignment真实wrapper和archived Task2场景因此在匹配依赖上实际执行。完整tools安装与drift通过；当前source/installed验证结果沿实际输出承接。不把这些工程结果等同于最终AI门禁或整个#589采用完成。
