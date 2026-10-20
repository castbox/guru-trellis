# 跨环境生命周期验证

状态：`promoted`。完整 current 策略与正常预期位于 [生命周期](../../test/current/task-delivery-lifecycle.md) 和 [Completion/Closure](../../test/current/completion-closure.md)。本文件是本贡献实际结果的唯一记录；通过结果限定在下列对象和层次。

## 当前实际结果

精确 provider `e9fb95fd2eb0fb8441153e77384a9dfd3ea3358f` 的 matching Core→CLI 正常构建通过。canonical source 校验核对精确 merge、parents/tree、main CI `39475768514`、同版本包和 212 个模板，通过；4 项 source 准备测试通过。source 采用没有更新 Guru 目标安装。

上游 PR #56 的独立检查、65 项定向测试和提交钩子完整测试通过：Core 493 项通过、1 项条件跳过；CLI 2402 项通过。两个实际 SDK/Guru `local_candidate` 补验分别覆盖共享 main 快照及旧 root 只留 archive：删除两类私有 receipt 后，只 inspect 一次、零 prepare/acquisition，保持 g1 与原 Task/binding/ledger/两处 `.trellis` 内容模式。这些是 provider 和适配集成证据，不是实际 Guru session/Bind 或 V1–V8 通过。

当前独立工程运行共 245 项通过、0 SKIP：Reactivate 19、Bind 15、Publish 40、Closure 32、Finish 64、Cleanup 41，以及 identity/source_results/maintenance_foundation 34。Reactivate/Bind 使用 unittest；pytest-only packages 使用 pytest --import-mode=importlib，并提供 matching common/SDK 依赖。首次错误收集方式造成的未执行/跳过不算通过；上述数字仅计正确入口的有效运行。此前 archive-resume identity 4 项仍保留原候选与层次，没有重标为本轮执行。该工程结果不是正式 Architecture 或 Task Check。

I03 的真实 clone 与公共 producer 覆盖 carrier、private 丢失、动作集合、projection-loss 和零重复 close；provider 仍是受控 fixture。当前完整 Closure/Finish 结果见上述 32/64 项；此前 shared reader 8 项及 33 个 subtests 的原结果也适用。

首次真实 consumer 失败显示 Finish 原始目录移动没有建立 carrier 的 artifact_origin。修正使用原官方 relocation helper 并保留返回 record；归档后原 Finish 重入及相应 installed consumer 通过。旧安装 fixture 版本改为其实际 matching SDK 版本，没有放宽产品前置。Interface/registry 和新独立 schema 的引用已对齐；旧正常输入语义保持。共享恢复新入口的 source 漂移尚无独立样本，原 source mismatch/Finish drift 回归通过；最终 Check 仍须判断完整覆盖。

I05/I06 责任仅补测试，没有因此重写 Identity/Establish/Ensure/Bind/ledger/Cleanup 原实现。Bind 包含 2 项真实非 main ref→独立 common-dir→原环境 owners→原 Delivery 选择。真实 bare remote 正常前进后，旧 Cleanup 返回 remote_head_changed，保留新提交、新代 binding/ledger 与原分支。Reactivate 的 8 项 contract 包含在上述 19 项中，覆盖旧代不同资源 cleanup_pending 不阻止新代接续，并保留同资源冲突。它们仍是公共 owner/真实 Git/受控语义输入的集成证据，不是实际 Agent 全链验收。

I04 当前完整 Publish 40 项包含 9 个 remote 恢复场景。实际公共 Planning/Check/Review/readiness producer、独立 Git clone 与未入 main 的 source 参与验证；B 本地 branch 与原 PR ref 分开，GitHub/push 端口受控。已完成 Draft、metadata、Ready 和公共 Publication 恢复均检查零重复动作；Ready 缺当前适用性回原 Review。此前 355 个 Guru Python 文件内存语法检查及包 diff 检查结果仍适用。

独立源码检查已覆盖 I01/I02、I03、I04 最终差额、I05/I06、适用未改消费者和完整迁移说明，无未决问题；受 I03 影响的两套 Reactivate 组合回归共 11 项通过、0 SKIP。Finish 两处终态与本机资源责任条款也完成独立复核。原生 T08 已完成，结果见下；该工程检查不代替后续源码正式 Task Check。

唯一代表安装使用精确 e9 provider 的实际 Core/CLI packed 包及当前完整 Guru preset，平台为 Codex。临时 CLI 包仅将 Core 依赖指向同次实际 Core 包，解决未发布包无法从镜像取得的问题；没有修改源码或全局 npm。实际 CLI init、公共 tools plan/apply、完整 preset apply 和 reapply 成功，原 bootstrap Task 内容保持。安装校验通过：40 个 packages、124 个 commands、6358 个 managed files，无 conflict、sidecar、removal 或 private test files。原 get_context continuation 读取到 Guru 入口。这些结果证明该代表目标的安装与投影，不证明两条原生再次 Finish。

dogfood 经原 guru-upgrade-tools 的 local_candidate 路线更新，返回 tools_upgraded。Task、workspace、session、branch binding 和 resource ledger 的更新前后内容一致。三平台 Claude/Codex/Cursor 的 overlay/spec/workflow drift 检查通过；上游投影核对精确 e9 和 201 个文件，通过。该调用仍明确返回 unverified=[formal_fork_source_lock]：当前 Guru canonical 尚未提交，不能称为 formal_guru_source 安装。普通 full apply 也实际调用，但被 upstream_delivery_migration_required 阻止且没有写入；未为通过安装而迁移无关旧归档。代表目标的完整 apply/reapply 与 dogfood tools-only 结果分别成立。

上游投影配套 test_verify_dogfood_upstream_projection.py 经 managed Python 执行，9 项通过。完整 package source checker 也通过：40 个 active packages、124 个 commands；136 是声明的测试文件数，不是已执行用例数。这些客观检查不替代正式 Check 的语义结论。

旧归档原生样本的 SDK 预检另有模式边界：原始 pnpm CLI 包及临时 paired 包内的 task.py、common/cli_adapter.py 模板均为 0644，精确构建目录为 0755；dist 的 741 个文件内容相同，Core 的 276 个文件也相同。packed-root 的 source_locked 比较因此返回 candidate_mismatch，未修改包或源锁。实际安装目标的两份 native 脚本均为 0755，原 task.py 经 managed Python 调用正常。样本改用同一精确 e9 构建目录的 SDK，source_locked 校验通过且 unverified=[]；目标继续使用自身已安装 native common，不使用外部 common override。该结果不重标 packed-root 预检为通过，也不影响上述实际安装与投影观察。

V7 从同一代表安装的 tracked 工具基线派生独立 clone，保留 `.3@7d20a930`、原归档 `b61304bd` 与原 bookkeeping merge `b0289465` 的真实 Git 对象。实际 AI 读取原 #503 scope、历史和已安装 Skills 后，原 Reactivate 返回 session_binding_recovery_required/g1；Establish、Ensure、Bind 分别返回 binding_established、checkout_resolved、reactivate_rebound。原 Completion 实际消费新 key 与 archive anchor，返回 blocked/current_architecture_authority_unavailable：当前 clone 缺现行 Architecture authority 和 g1 acceptance_finish 结果，未宣称 #503 再次完成。原 Reactivate 随后恢复为 reactivated_to_planning/g1/session_bound，未再增代；原 native task.py current 读取正确 active ref。9 个原归档文件 bytes/modes 不变，无私有控制状态复制，Delivery/Completion/Closure 均为 0，provider close/create/merge 均为 0。该样本证明固定旧格式经原生环境恢复后可交下一实际 owner；它不承担原 #503 全部业务再次验收。

MERGED 恢复采用仍适用的原证据：[第 557 项实际结果](../557-manual-merged-delivery-recovery/test.md)记录真实 PR563 双亲合并、原 Merge delivered、同输入恢复及实际 Completion；[第 569 项实际结果](../569-fixed-cutoff-history-query/test.md)记录 matching installed 的 Merge/query2 与实际 consumer。原 39 项、58 项完整 suite 属于各自原候选，并非本轮重跑。独立 reviewer 核对当前 Merge package、delivery projection 及原公共 API 没有相关差额；新 Closure/Reactivate 不进入该恢复链，因此可采用该范围内工程/原生事实，不继承其语义 pass。

T08 在同一代表安装 profile 中，由实际 AI owners 完成两条原生再次 Finish。A 的 g0 经 Completion/Closure/Finish 归档并合入目标，Cleanup 未执行。独立 `git clone --no-local` 的 B 没有 A 的 runtime、session 或资源账本；原 Reactivate/Establish/Ensure/Bind 继续同一 `native-normalize` Task 到 g1，原 Reactivate 重入仍为 g1。目标随后正常增加独立文档，未要求业务分支追赶。

g1 真实实现 `normalize` 的首尾裁剪，并经原 Planning、独立 Architecture、候选 Check、实际知识晋升、最终 Check、TaskCommit、首次完整 Branch Review、Readiness 和 Publication/Merge。唯一业务提交为 `2c5840f6dee8f969e3fa2ee4131b1b4dfcb76ab2`；提交后刷新 Check，clean committed reentry 没有第二提交。实际四个 subtest 通过。D1 的双亲合并 `b0e8b57b27ab84711debc3ae5bf5d732e5d3d73f` 保留目标独立推进及新行为，五项 schema-2 trailers 正确。整体 Completion、Closure 与 Finish 随后真实完成；bookkeeping PR #3 已合入目标，Finish 为 `finish:v1:99c996902f3cb99a`。

g2 从 g1 终态目标另作独立 `--no-local` clone，未复制 A/B 私有状态。原 Reactivate 和环境 owners 接续同 Task 到 g2，公共状态为 `no_current_delivery`。原 Task-only Architecture 返回 `no_change`。原 `delivery_reactivation_validation` 对当前 clone 尚缺 AC1–AC4 实测返回 `evidence_pending`；实际 Python 3.12 运行现有一个测试方法的四个 subtest 后，原 `delivery_evidence_refresh` 返回 `completed`，再经 Closure/Finish 成功。bookkeeping PR #4 的合并为 `363a48fc49e7e4cf316543b730a9fa941eb47c43`，Finish 为 `finish:v1:d352943625ed1398`。原 shared archive reader 已核验最终 g2 归档；历史仍只有 g1 的一个 Delivery，业务、测试定义和共享 authority 未改。

T08 的首次环境失败保持其归属：受控 provider 缺少实际请求的字段、Ready 和 immutable Git commit 读取时，补齐准确端口后由原事务恢复同一 PR，未重复创建或合并；其 merge 使用真实 Git 三方组合。g2 默认解释器依赖安装失败，原 bootstrap 显式选择现有 Python 3.12 后成功。三代公共历史、bootstrap Task 和所有 checkout 保留，A/B 的 Cleanup 均未执行。本样本证明实际 Agent、已安装原入口与真实 Git 的受控本地集成，不证明真实 GitHub、业务生产或完整多平台安装矩阵，也不代替源码最终 Check。

## 验收状态

| 场景 | 当前边界 |
| --- | --- |
| T635-01 / V1 两条原生再次 Finish | 上述 T08 两条完整原生链均完成；同 Task 的 g1 新 Delivery 与 g2 evidence-refresh 分别再次 Finish，独立 common-dir、目标推进、旧 Cleanup pending 和无空 Delivery 已实际观察。 |
| T635-02 / V2 活动 ref 接续 | 已有独立 common-dir、非 main ref、同 Task/Delivery 的实际 public owner 集成通过；semantic 输入是 fixture，不标作实际 Agent 全链。 |
| T635-03 / V3 三类副作用恢复 | Closure、Open Draft/Ready 的当前定向恢复通过；MERGED 采用上述仍适用原事实。各原 owner 保留准确归属、当前资格与零重复副作用边界。 |
| T635-04 / V4、V6 资源和正常双 Task | 不同 common-dir/Task 的原 owner 真实 Git 集成覆盖同资源冲突、无关 pending、remote 推进与新代资源保留；T08 另实际完成旧 Cleanup pending 下的新环境再次 Finish，bootstrap Task 保留。 |
| T635-05 / V5 缺失和未完成 | 原 Reactivate/Publish/Closure 定向检查覆盖未入目标归档、身份/来源/资源冲突及不可用提交；V7 实际 owner 对缺现行 authority 给出具体 blocked 并保留 g1。未发布 dirty 不迁移，不能据此推导无损接续。 |
| T635-06 / V7 固定正式旧格式 | 上述实际 Reactivate→Establish→Ensure→Bind→Completion 消费及同操作恢复完成；没有将原业务 Completion blocked 写成完成。 |
| T635-07 / V8 分发 | source 采用、唯一 Codex 代表目标完整安装/reapply、安装校验及三平台 dogfood drift/上游投影通过；T08 原生全链已完成。formal_fork_source_lock 保留上述边界；源码最终 Check 由原 owner 单独执行。 |

没有运行完整多平台 Release 矩阵。实际业务现场没有修改；本轮不以 source、fixture、CI 或依赖合并证明整体完成。
