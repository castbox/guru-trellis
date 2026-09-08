# 实施计划

## 1. 进入实现前

- [x] 运行 workspace boundary check，确认 branch/worktree/task identity。
- [x] 重新读取 Issue #377、当前 main、canonical package 和相关 workflow/spec。
- [x] 完成 direct-evolution 与 solution-mechanism qualification：真实支持入口
      是现有 `scripts/invoke.sh --invocation -`，消费者是现有 typed-exit
      projections；缺陷来自公开 schema 与 runtime 的正常路径不一致。直接让
      runtime 从 checked owner result 生成 DTO，不引入兼容 wrapper 或第二执行路径。

## 2. 合同与实现

- [x] 定义并落实唯一 public invocation envelope 语义。
- [x] 修改 canonical schema/runtime/Skill/interface/reference，使 runtime 与
      声明合同一致，并保留 freshness、duplicate、target、owner-result 和
      typed-exit 校验。
- [x] 更新 eval adapter，删除依赖未声明顶层字段的调用样例。
- [x] 补充真实 wrapper 回归：合法 envelope -> `clear`，并覆盖错误/过期输入。

## 3. 验证

- [x] package contract/runtime tests。
- [x] envelope Draft 2020-12 schema validation、声明外字段和错误出口测试。
- [x] stale target、duplicate snapshot、live target freshness 回归。
- [x] canonical/installed/platform equality、preset apply、dogfood drift、
      sidecar 检查。
- [x] 一个代表性 clean throwaway 安装并运行 Phase 0 public wrapper；不宣称
      完整多平台或 Release Gate 通过。
- [x] `git diff --check`、JSON/Python/Bash 静态校验和 task validate。

代表性 clean throwaway 使用 validation ref
`validation/377-clarify-requirements-invocation-contract` 完成；`claude-clean`
通过 provenance、preset、Phase 0 及 Clarify `clear/needs_context/refresh_context/
retarget_context/new_task/blocked` 路径。完整 `claude-existing` 累计兼容性矩阵
仍有既有 installed package inventory/provenance 边界，属于本 Issue 非目标，记录为
非阻塞 deferred/unverified，不作为 #377 的实现缺陷或完整 Release Gate 结论。

## 4. 后续门禁

- [x] 原始实现已完成 fresh Phase 2、commit、Branch Review、Publication 和
      Finalizer，并创建 PR #380。
- [x] PR review 发现 P2：`needs_context` 对不完整 `transition.base` 直接索引，
      可能输出 traceback。提交 `e292c3f6` 增加结构、字段、SHA 与 repo locator
      校验，malformed 输入统一返回 `stale_identity` JSON error。
- [x] finding-fix 定向验证：canonical 与 installed Clarify contract tests 各
      10/10，source skill-package validator 和 Python compileall 通过。
- [x] fresh-final review 继续发现同一 P2 的残余类型路径：`transition.base.source`
      为数组或对象时，集合成员判断会抛出 `TypeError`。当前实现先校验字符串
      类型，并在 canonical/installed 测试中覆盖数组和对象，统一返回
      `stale_identity` 且无 traceback。
- [ ] finding-fix 必须重新完成 Phase 2、Task Commit、fresh Branch Review、
      Publication 和 Finalizer 后才能合并 PR #380。
