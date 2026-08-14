# #222 受管 Python wrapper 修复执行计划

- [x] 审计所有直接调用 `python3 -m runtime.*` 的共享 wrapper 与安装投影。
- [x] 将需要第三方依赖的 wrapper 路由到 repo-local `resolve-python.sh`。
- [x] 补充 PATH Python 无 `jsonschema` 的 source/installed 回归。
- [x] 更新 verifier，使 fresh-install 阶段显式证明共享 wrapper 使用 managed runtime。
- [x] 运行 preset apply，同步 dogfood installed copies并刷新 manifest。
- [x] 将 extension revision 从 `.28` 更新为 `.29`，同步 README、fixtures 和 release notes。
- [x] 运行 targeted tests、managed runtime、preset tests、projection equality、ownership、
  drift、JSON/schema/compile/diff 与零 sidecar检查。
- [x] 修复 BR-222-001：四个平台 eval adapter 通过 checkout-local resolver 执行。
- [x] 修复 BR-222-002：fresh source 建立 commit identity且 source/installed eval实际通过。
- [x] 将 finding-fix candidate revision 前进到 `.30`并重跑 focused/projection/drift 门禁。
- [ ] 由独立 Trellis check agent 审查完整 task scope并调用 `guru-check-task`。
- [ ] commit/push/PR/merge 前分别展示精确副作用；merge 后重新冻结 exact candidate。
- [ ] 在新 candidate 上重新执行完整正式 verifier、剩余 pre-tag matrix与隔离业务仓 smoke。

不创建 `implementation-handoff.md`。
