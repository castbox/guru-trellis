# #489 发布准备实施计划

1. 验证 TaskId/source/branch/checkout 的正式 owner边界，读取 live #489、current RDT/Architecture、官方 Trellis 文档及公开文档规范；完成 wording、Architecture与规划批准并激活。
2. 直接更新当前四个公开文档的 tag/predecessor/安装版本轴；读取 canonical manifest/source lock并核对其当前值。按既有owners完成Docs/RDT/Architecture影响判断。
3. 运行 source、installed、Shared/Codex/Claude/Cursor validators、ownership、dogfood drift、Markdown引用及git diff check。审查所有变化及真实未验证边界，正式 Phase 2与task commit。
4. 独立完整pre-promotion Branch Review；仅在owner要求shared-current promotion时串行更新，再完成fresh Phase2/commit及不同reviewer的完整post-promotion Branch Review。无promotion时消费正式current/no-change，不制造空提交。
5. fresh publication Architecture与Delivery Review，中文Refs-only PR经Publish、expected-head Merge；准备任务Completion、reference-only Closure、acceptance_finish Architecture及Finish archive/bookkeeping PR/merge闭环。

本计划固定，不记录执行进度、候选SHA、gate状态、tag/Release状态或授权。Stage 2由发布Skill在终态merge之后独立执行。
