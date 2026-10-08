# 发布准备实施计划

1. 复核 #500、current main、predecessor、manifest/source lock 与四个公开文档。读取 Architecture/RDT .76 authority，记录本次稳定范围，不复制历史验收为新证据。
2. 校准 public-docs、architecture usage、RDT usage 与 MIGRATION-495 四处当前投影为 .76 / 5c760463 / CI 37735554354；三份 README 已一致，仅复核。固定 extension/source lock；cc5f9a、ecd152、EVD-051 保留历史验收归属，EVD-052 不冒充最终 Release gate。
3. 调用 Architecture/RDT task_impact_sync 判断实际 delta；有真实增量才写隔离贡献。复用既有 migration entry，不实现新 runtime/API/兼容机制。
4. 运行 source/installed package validator、Shared/Codex/Claude/Cursor source parity、私有 release Skill parity、upstream ownership、preset reapply、dogfood drift 与 git diff --check。检查 reapply 变更和 .new/.bak，逐个处理本 task 引入的冲突。
5. scoped Phase 2 后由 guru-create-task-commit 创建精确提交；guru-review-branch 独立审核完整 origin/main...HEAD。零开放 P0-P3 后，Architecture/RDT owner 串行处理真实贡献 promotion。
6. promotion 产生 delivery diff 时重新 Phase 2、task commit 和完整独立 Branch Review。完成 current Architecture publication check 与 Delivery Review，现场生成中文 Refs #500 PR。
7. 经 Publish、Merge、Completion、reference-only Closure/no_mutation、acceptance_finish、Finish 与 Cleanup owners 完成准备范围。每项 Git/GitHub 副作用按 owner 独立展示并确认。
8. 准备和终态归档合并后，把后续工作交回 #500 Release owner：fresh origin/main exact-candidate 门禁、.1 与一个旧 0.6 来源迁移/rollback、tag、tag-pinned smoke、Release 和 Issue closure。步骤 8 不是本 task 的实施或 Completion 范围。

验证命令与结论服务当前准备 diff。最终远端 exact-candidate 的 install/update/reapply、来源迁移、secret scan 和发布证据由 Stage 2 重新执行；不扩张累计矩阵，不制造 tracked 进度或授权文件。
