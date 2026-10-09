# #464 实施计划

## 入口
任务保持 Phase 1；执行实现前消费 current Planning approved DTO 与 workflow 的计划展示边界，再由 guru-activate-task 状态转换。
每次 source/test/task artifact 写入前调用 check-task-checkout-boundary。实现仅按本计划写集；不从本次规划创建确认推导 commit、push、PR、merge 或 cleanup。

## 1. 固定当前 scope 与 baseline replay
刷新 live #464、当前计划、Architecture/RDT、package contracts、interface/commands、完整 diff；核对官方 Trellis 扩展文档。先复用已通过的局部能力。
对本任务用到的 Delivery/Reconcile 临时 fixture 补齐 current TaskLifecycleDTO/task schema 与既有 branch binding，实际调用原模块/wrapper。只修复这些 fixture 的前提，不因旧 header ERROR 增加产品需求。
在 current AI owner replay 中记录调用前后 observable：当前 candidate、执行的 check、检查次数、current结果引用、typed route、mock mutation 次数；记录留在当前运行，最终简洁结果进入 RDT Test consumer，不保留原始 transcript。
先复现同 HEAD recovery 仍强制 new BranchReview 的合同路径；对 Check 的必要细化用 A/B 两个真实独立依赖 check、正常修订 A、正常环境改变、新增 C 展示当前义务与执行事实。未复现的 runtime 猜测不实现。

## 2. 原 owner 合同直接演进
按 design 写集细化 Check；完整 current semantic round、检查集重新确定、check/version/依赖/toolchain/environment 适用性复核、当前候选绑定、不可用局部重跑。
细化 DeliveryReview 的同 HEAD/current checked anchor 条件；fresh DeliveryReview 输出丢失只重做该 owner，BranchReview output 真丢失只重做 BranchReview；内容变化完整 review。
workflow 只补路由衔接；原 public input、exit/consumer、schema、checkpoint/receipt 生命周期保持原合同。没有新增 runtime cache、scope classifier 或 script semantic review。
验证结果/外部证据补齐、metadata/projection/promotion/finding-fix、authority delta、后续 Delivery 与 session 恢复都沿原 owner 判影响。发现超出规划机制/架构边界就停止该候选编辑，执行现有 qualification/re-entry。

## 3. Docs 与分发
创建 isolated RDT 三层贡献，按 `AC01–13 -> owner responsibility -> replay case` 建 traceability；durable paths 见 design 的 Docs SSOT Plan。
同步 canonical workflow/Skill/spec 和两处 README；不直接竞争 shared RDT/Architecture current。
运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`，逐个检查 .new/.bak 与 managed hash；没有用户改动的副本按 canonical 安装，用户改动走既有冲突处理。运行 `check-dogfood-overlay-drift.sh`，结果必须无漂移。
检查官方 update 的托管语义，确认 canonical marketplace/preset/overlay 可重新应用；不对已安装文件做一次性 patch。

## 4. 最小行为验证集
| Replay group | 当前入口及观测 | 覆盖 |
| --- | --- | --- |
| validation delta | current AI Check owner + 原 recorder/check/invoke；两个实际独立模块检查 A/B、新增 C；观察执行次数和当前 checkpoint summary/content identity | AC03/04/06/12 |
| authority / metadata | 原 Planning/Architecture/Check owner；equivalent 与实质变化分别调用；metadata 修订仍由当前内容 recorder 绑定 | AC01/05/06 |
| committed revision | 原 Check/TaskCommit wrapper、独立 BranchReview owner；正常文档/projection/promotion/finding-fix 后观察当前 exact range | AC07/11 |
| recovery | Delivery ready 正常退休、丢 stdout、原 checked anchor 仍在与丢失两个分支；Publish/Commit 原 transaction 模块 mock 外部依赖 | AC08/10/11 |
| base / continuation | 原 guard/Reconcile wrapper，unchanged 零 mutation、evolved bounded route、后续 Delivery/validation-only continuation | AC02/09/10 |
| distribution | changed package/runtime/schema checker、声明平台 projection、installed、apply/reapply/drift、sidecar/mode | AC13 |

改变依赖、check/version、toolchain/environment 分别具备独立缺陷检出价值；只改变合法值不设置旧值白名单。native semantic evidence 和 post-owner deterministic evidence 明确区分；没有运行 native/外部实效就标 unverified，不能声称全部 AC passed。
用现有 managed Python 启动测试，不安装全局依赖。已有通过的能力仅在候选/依赖改变或新失败时重跑，不把几条命令绿替代完整 task scope check。
普通 issue 不执行全多平台 Throwaway matrix。当前不改 installer 行为、不以干净安装为 acceptance，因此无需为本 scope 新建 clean throwaway；累计 Upgrade/Release 验证 deferred 给专门 owner。
受影响非生成代码超过 3000 行时，先做机械拆分/小解耦审查；不扩成历史全仓重构。

## 5. 完整门禁与 Delivery
完成 Docs reconciliation 后调用 fresh Architecture Phase2 + guru-check-task（完整 scope），没有 open finding/blocking unverified 才进入 TaskCommit。独立 reviewer 读取完整 origin/main...HEAD，不能读 Phase2 private checkpoint 作证明。
每个 commit/push/PR/merge 的具体 plan 单独展示并遵守当前授权边界。Delivery Review 使用中文具体 title/body、Refs-only、实际验证、remaining/unverified、安全/部署影响；Publish 与 Merge 原事务处理，不闭 Issue 或归档。
RDT/Architecture promotion 如产生 diff，沿原 Phase2/commit/full review 接续；验证外部效果不足时不能声称 Release/部署或完整链路成功。
Completion/Closure/Finish 继续原 owner，cleanup 独立。当前 planning 交付只写 task 规划，不 stage/commit/push、不修改远端 Issue。
