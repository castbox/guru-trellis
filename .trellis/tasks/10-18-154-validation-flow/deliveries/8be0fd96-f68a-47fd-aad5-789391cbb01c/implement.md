# D1：pack 输出目录帮助实施与验证计划

## 1. 输入与引用

必须读取根 prd.md §1–8、本批 prd.md §1–7、本批 design.md §1–9（唯一来源设计处置在 §3）。读取 source-a.md/source-b.md 全文并保留改 build 不采用、其余承诺完整的边界。读取现有 pack.py、test_pack.py 与 usage.md。

本批从 H0/B=`b1b096df218c25442ebdeebed72e9025c4c847e4` 开始，没有 prior delivered 结果。实际原 Architecture candidate_assessment 已完成；当前 Wording、final_plan 与 Approval 仍走原 owners。实施只能在原 Activation 完成后开始，本文不构成实施或通过事实。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner 与文件 | 行为与可审核产物 |
| --- | --- | --- |
| I1 | 原 Activation 接受后，Author/实施 owner；pack.py | 在 build_parser 原 action 直接替换 SUPPRESS help 为输出目录说明与 %(default)s；保留 default dist、metavar DIR、main/build |
| I2 | I1 后，同一实施 owner；tests/test_pack.py | 加一个通过 invoke 调用 --help 的测试，观察 CLI 内容、返回值、stderr 与空目录前后集合；保留现有三例 |
| I3 | I1/I2 后，原 Author 承接 RDT 范围；docs/usage.md | 更新“当前帮助未展示 output”这一事实，加入帮助入口；保留普通构建说明和“当前无 dry-run”状态 |
| I4 | I1–I3 完成，原 Check | 执行 §3 验证、核对 docs/code/tests、整个 D1 内容与剩余责任；最终 Check 前完成 docs reconciliation |

每次 source/test/task 写入前使用原 check-task-checkout-boundary，TaskId/generation、branch、注册 worktree、当前 selection 必须匹配。不得修改 workflow、runtime、schema 或其他 worktree。D2 只保留需求，不在本批写参数、代码、测试或空实现。

## 3. 验证入口、输入与预期观察

- V1（design §8；D1-AC1/2）：新增帮助测试通过 subprocess 调用实际 CLI --help。受控空目录中记录运行前后目录树；预期无新增文件目录，returncode 0、stderr 空，stdout 含 --output、DIR、目录用途、dist。
- V2/V3（D1-AC3/4）：`python3 -m unittest discover -s validation-fixture/tests -p 'test_pack.py'`。执行新增帮助测试及现有 default/explicit/existing-target 三例；预期分别观察 design §8 中定义的真实输出与不覆盖结果。
- V4：`python3 validation-fixture/sandbox/pack.py --help` 读取实际帮助，再对照 usage.md 与参数 default。代码差额应只改变帮助元数据；人工核对普通构建无新分支、dry-run 仍未实现。
- 最终原 Check 必须针对固定 B..实际 HEAD 与本批 dirty increment，覆盖真实完整 D1 内容。测试通过不是完整语义 Check。

测试临时工作目录用于已有测试隔离；在本隔离 repo 范围内组织执行并保留其他并行内容。没有新增联网、安装、多平台、upgrade/update 或生产验证。上面是后续命令与预期，不是已执行通过声明。D2 的 dry-run 默认/显式/零写入验证不在本批提前执行。

## 4. 停止条件与适用回退点

- Task/session/Delivery/checkout 不匹配：停写，回原 Identity/Bind/Checkout 或 Selection owner，不伪造 context key。
- 需求或来源发生实际变化：停当前实现，回原 Clarify；候选机制改变回原 Author 与 Architecture。
- V1–V3 失败：保留首次实际失败，实施 owner 修复本批；涉及规划差额则回原 Author，不放宽既定验收。
- usage 与代码不一致：I3 必须修复后才进入最终 Check；原 RDT owner 处理共享 authority 的真实影响，不由实施者静默扩张。
- 普通构建行为被改动或出现 dry-run 提前实现：停本批，恢复其既定责任边界，不重建 Delivery 或改写根 scope 掩盖差额。

本批无发布、数据迁移或线上副作用，不新增回滚协议。局部改动回退只针对本批选定文件，保留其他用户工作。commit/push/PR/merge 不由本计划自动授权。

## 5. Delivery Policy（唯一）

policy=partial。整个 Task scope 是根 PRD R1–R4；当前切片是 R1 帮助及 R3 普通构建兼容回归，同时遵守 R4 的独立切片与整体责任。独立交付条件：CLI 帮助可直接使用、D1-AC1–AC4 有真实证据，且不依赖 dry-run。

剩余责任为 R2、整体 AC2/3/3E 的 dry-run 默认及显式目标零写入，包括目标已存在时仍成功预演，以及后续对 R1/R3 的集成回归；由同一 active Task 的原 Author、后续 D2 和原 Completion 保留。D2 尚未创建/规划/实现/交付，不能预填其结果。D1 的帮助机制和兼容验收不因此改变。

D1 验证边界是帮助与现有普通构建。D1 合并后原 Completion 审查整个 accepted scope；R2 未满足时必须保持 Task active，并沿 additional_delivery_required 交原 Creation 创建 D2。只有完整 R1–R3 及所有整体验收证据满足，才由原 Completion 判断完成，随后原 Closure 对 no_issue 返回无外部关闭效果。D1 交付不是 Task Completion。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。实际 durable delta 只有 validation-fixture/docs/usage.md 的 output 帮助可见性和 --help 使用入口。原 Author 为本批文档写作 owner，实施 owner 执行 I3；原 RDT owner 已对共享 Guru .107 authority 返回 ssot_current，不创建空共享 contribution、版本或导航更新。

requirement/behavior 引用根 PRD §5/7、fixture source-a/b 与 usage；design 引用本批 design §2–8 和 pack.py；test 引用 test_pack.py 及本计划 §3；Architecture 引用 docs/architecture/README.md 的 .98、constitution 与 change-contract。fixture 差额不改变共享 Guru requirement/design/test authority。若实际实施扩大为共享合同变化，回原 RDT/Architecture，不自行宣称 no-op。

I3 文档 delta 必须在最终 Phase2 Check 前 reconciliation；直接 consumer 为原 Check、完整 Branch Review 和 Delivery Review，依实际代码、文档与测试结果核对。后续 D2 再更新 dry-run 已实现的用法事实，不能在 D1 预写成功。当前规划只写本批 planning_root，不写共享 README/index/manifest/spec 或架构基线。
