# #490 实施计划

1. 在当前 task checkout 逐次执行 boundary check；读取 workflow/preset/docs/architecture specs、当前源与正式 creator 调用链。
2. additive 更新 canonical C6 source enum；同步合同、示例及定向创建/recovery/source identity 测试。运行原 no_issue/exact_source、session/branch/Closure 回归。任何新发现超出当前规划先返回 qualification owner。
3. 核实 upstream commit/tree/parents/main CI/build marker，更新 canonical source lock。用真实 Fork CLI 正常官方生成/update，再运行 canonical apply.sh --repo .；逐一处理 .new/.bak 后运行 check-dogfood-overlay-drift.sh。同步 installed runtime 与声明平台 projection。
4. 执行 Docs SSOT Plan：任务独立 RDT 五文件与 Architecture contribution，更新 current README/spec/来源合同；只在 RDT/Architecture owner 各自审查后推广 .71，不改历史 .70 或归档。
5. 运行定向 package/runtime、source validator、canonical/dogfood/installed/platform 检查，以及一个代表性 throwaway clean install/current update/reapply。每项保留命令、结果与范围；完整 #489 Release 矩阵保持未验证。
6. 独立 Phase 2 semantic check、准确文件 task commit、完整 origin/main...HEAD Branch Review；Architecture/RDT promotion 后重新 check/commit/full-diff review，再通过正式 Delivery publication/merge、Completion/Closure/Finish 闭环。

## Docs SSOT Plan

策略 ssot_first：先贡献后推广。durable paths：docs/requirements-design-test-contributions/490-reference-only-adoption/、docs/architecture/contributions/490-reference-only-adoption.md、docs/requirements/、docs/design/、docs/test/、docs/architecture/、.trellis/spec/preset/upstream-ownership.md、canonical create-task/source README 与根 README。版本 successor .71 只包含本次 accepted scope；正式 release 版本轴留给 #489。

## Delivery 与未验证边界

本次单一 Delivery 为全部 R1-R4；task 内无剩余工作。可独立使用 reference-only 正式创建并安装新源，不依赖 #489 已发布。完整多平台/native-host矩阵、predecessor 拒绝无写证明、fresh release candidate、tag smoke、Release 和 #489 closure 由 #489 owner 完成。
