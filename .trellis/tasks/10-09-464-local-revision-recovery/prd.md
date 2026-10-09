# #464 正常修订与恢复的局部接续

## 当前需求 authority
唯一需求为 https://github.com/castbox/guru-trellis/issues/464 ，合同 `2026-10-09-r11`，accepted scope identity `issue-464:2026-10-09-r11`。规划基于 `main@648b68daeabc4228992149132c0d50b0da06c423`。Issue 正文优先；本文只定义本 task 的实现映射，不复制第二份完整需求。
当前 RDT/Architecture：`current-main-0.6.17-guru.77 / active`；设计宪法 `guru-trellis-design-constitution-v1`，项目 change contract `guru-trellis-architecture-change-contract-v1`。

## 目标与交付
正常修订只使真正受影响的既有 owner 和检查失效。原 owner 保留仍适用的判断与执行事实，为当前候选形成当前结果；新 committed content 必须完整 exact-range Branch Review。身份、一致性、semantic gate、真实副作用确认、Completion/Closure/Finish 规则保持各自职责。

本 task 当前 Delivery slice 覆盖下面 AC01–13 的完整局部接续合同、必要投影和定向行为验证。无计划内剩余工作；仍未验证的远端效果必须披露，不能包装为完成。若实际实现暴露超出该边界的需求，先返回既有资格/澄清 owner，不自动增加第二 task 或新的交付目标。

## 正常路径研究结论
现有 Check rematerialization、private runtime 排除、Task Commit 同次 mutation 恢复已通过前序定向测试。Publish 的 missing-transaction 回程与 metadata postimage 恢复模块测试已通过。Delivery Review 当前 schema fixture 修正后，真实模块调用证明 ready 后 checkpoint 正常退休及同 HEAD re-entry 均成立。fixture 修正只发生在临时测试仓库，未修改 canonical 测试或产品代码。

确认的合同缺口：Delivery Review Public Entry 对 Publish `review_stale` 一律要求“new complete Branch Review”的 anchor，未区分 HEAD/range/适用合同仍未变化且原 checked Branch Review DTO 仍在当前上下文的恢复。这会在正常恢复中要求不受影响 owner 重做完整审查。正确恢复仍需 fresh Delivery Review，不能恢复已退休语义 pass。
Check 已有 delta classification，详细的依赖/check-version/toolchain/environment 复核及当前候选结果重新绑定尚未被合同明确承接；这是 accepted 正常行为的合同落实工作，不能预设 runtime cache 缺陷。
未证明的猜测不进入 finding：metadata 更新必然导致候选重建、所有 base unchanged 都错误、现有 mutation 恢复重复发布。基于旧 task header 的 reconcile/Delivery fixture ERROR 不证明产品缺陷。

## 验收映射
编号按 live Issue 第 8 节的顺序对应。每项观察实际 owner 行为、调用次数、当前输出或拒绝结果；固定文本或自构 digest 比对不单独证明通过。

| ID | 正常动作 | 必须观察的结果 / owner |
| --- | --- | --- |
| AC01 | session/checkout 重绑定，任务业务内容不变；task metadata 正常变化 | #454 identity owner 重验；Phase 2 原 owner 重分类当前内容并记录当前结果，未变化业务判断不全重做；不删除 metadata 的 exact-candidate 校验职责 |
| AC02 | 对相同 base pair 调 guard；随后 base 正常前进 | unchanged 直接恢复原 consumer；new_pair 由 Reconcile bounded 判断，保持已有确认和 merge/continuity 路径 |
| AC03 | 改 A 而 B 依赖不变；分别改变 B dependency、check/version、toolchain/environment；增加 C check | B 执行次数在 A-only 后不增加；每种 B 依赖变化均执行 B；C 必须执行 |
| AC04 | 原 check owner 仍合法持有 B 的执行事实；随后事实不可用 | 复核后在当前候选结果中记录 B；旧候选记录保持原对象；不可用只重跑 B；不合成 semantic pass |
| AC05 | shared authority 前进但 task 适用合同不变；再改变适用合同 | 对应 authority owner fresh 判断；前者刷新局部适用性，后者返回最早受影响 owner |
| AC06 | 检查完成或外部证据补齐；证据另揭示真实行为缺口 | 结果更新不循环改变候选；真实缺口使受影响内容/义务失效 |
| AC07 | 待提交后改文档/生成/projection；promotion 写 diff；提交后 finding-fix | 自动回原 Check/实现 owner；Task Commit 校验当前 tree；新 committed HEAD 完整 exact-range Branch Review |
| AC08 | checked 输出丢失、checkpoint 正常退休、同次 commit/PR mutation 结果丢失 | 原 owner/transaction 恢复；同 HEAD 且原 Branch Review DTO 可用时不因局部恢复重跑 Branch Review；DTO 缺失重跑该 semantic owner，不重建历史链；不重复 mutation；真缺证据仍阻塞 |
| AC09 | 同 task 后续 Delivery / validation-only 补证 | 由唯一 continuation 恢复正确 consumer；Completion/Closure/Finish 意义不变 |
| AC10 | mapped re-entry、same-plan retry；再提出新 payload 或新副作用 | 前者自动承接；后者保留原对话边界；无授权状态持久化 |
| AC11 | 从当前 task/session/live authority 恢复上下文 | 使用原 continuation 与原 owner 合法状态；Phase2 → TaskCommit checkpoint consumer 保留；Branch Review 不读取它；不建立 capsule/ledger |
| AC12 | 合法 environment 配置调整 | 对应 check 重跑；不因旧值比对失败；适用集成运行证明可用性，不冻结端口/版本/开关 |
| AC13 | canonical 更新后 apply/reapply | dogfood、installed、声明平台投影一致；drift 为零；每个 .new/.bak 有处理结果；mode 未回退 |

## 非目标与验证边界
不新增 Generation、Freeze、ValidationReceipt/cache 协议、全局 registry/ledger、continuation capsule、cross-Skill private-state 依赖或确认链；不修改上游/node_modules；不重建 #454、#434/#435、#436，不实施 #404/#383，不批量治理历史测试。
范围只含诚实正常动作、常见 stale/mismatch、结果丢失和既有恢复。不用人为伪造 hash/artifact 构造缺陷，不扩展并发压力、TOCTOU、锁或 crash consistency。
远端 push/PR/merge/Issue mutation 实效当前未验证；定向模块测试 mock 外部依赖不能冒充远端完整链路。完整多平台 Upgrade/Release matrix 由专门 owner 负责。
