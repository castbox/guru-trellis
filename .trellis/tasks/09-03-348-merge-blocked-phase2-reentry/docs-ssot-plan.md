# Docs SSOT Plan

## 结论

本任务的持久产品/流程规范仍以 `castbox/guru-trellis#348` 和 canonical `trellis/` 源文件为权威。task-local `prd.md`、`design.md`、`implement.md` 只承接本次规划，不提升为 repository product SSOT。

## 计划

- Requirements/Design/Test 影响：通过 task-local 规划和测试/eval 变更承接；若 Architecture planning gate 要求 shared SSOT 更新，使用现有 contributions/promotion 路径，不直接覆盖 shared current。
- Workflow contract：更新 canonical workflow/package/spec 后，通过 preset apply 同步 dogfood 和平台投影。
- README/spec：补充 re-entry route、外部 blocker 边界、下游重跑和验证限制；不记录本机路径、授权或历史 checkpoint。
- 完成收敛：实现后以 canonical source、installed projection、workflow registry、schemas、examples/evals 和 drift checker 共同验证，避免单独修改安装副本。

## 不做

不新增独立业务文档体系，不把 task archive、runtime mapping、PR payload 或 gate history写入公共文档，不吸收 #248/#261 的整体目标态设计。
