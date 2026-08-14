# #222 修复发布验证受管 Python wrapper 漏洞

## 背景

`v0.6.5-guru.6` 的第一次正式 pre-tag `guru-verify-extension-installation`
在 fresh-install source package validation 处失败。隔离目标仓已经安装可用的受管
Python runtime 和 `jsonschema 4.25.1`，但共享 validator/eval/compat shell wrapper
仍直接调用 PATH `python3`。当系统 Python 没有 `jsonschema` 时，安装链路错误地退回
外部运行时并以 `runtime_dependency_missing` 终止。

## 需求

- 所有需要 Guru Team Python runtime 的共享 validator/eval/compat wrapper 必须通过
  repo-local `resolve-python.sh` 执行，不得依赖系统 Python 的第三方包。
- source checkout 与 installed checkout 必须解析各自仓库的 active managed runtime，
  且缺失、损坏或身份不匹配时 fail closed 并给出 preset reapply remediation。
- canonical workflow scripts、preset 安装结果、dogfood 副本和平台入口必须保持一致。
- 回归必须覆盖 PATH Python 无 `jsonschema`、受管 runtime 有依赖的 fresh-install source
  validation 与 eval discovery。
- 修复后的 candidate bytes 不得继续使用 `0.6.5-guru.28`；extension revision 前进到
  `0.6.5-guru.29`。尚未创建的 repo tag 仍为 `v0.6.5-guru.6`。
- #223、#208、#164、#220 仍不属于本次范围；本修复 PR 不关闭 #222。

## 验收标准

- [ ] PATH Python 缺少 `jsonschema` 时，shared source/installed validator 与 eval/compat
  wrapper 均使用对应 checkout 的受管 Python 并通过。
- [ ] `guru-verify-extension-installation` 从 fresh clean candidate 正式完整通过一次。
- [ ] clean workflow install、existing preview/switch、preset apply、official update、reapply、
  platform equality、ownership inventory、dogfood drift和零 sidecar 均通过。
- [ ] Branch Review、Finalizer/Merge 生命周期、隔离业务仓 pinned upgrade 和 2130 路径
  Publication/Finalizer preflight 在新的 exact candidate 上通过。
- [ ] manifest、README、release notes 与 stable source 映射一致为 repo tag `.6`、extension
  revision `.29`、official Trellis CLI `0.6.5`。
- [ ] 所有 pre-tag gate 通过前不创建 tag、Release，不评论或关闭 #222。

## 边界

- 不修改 Trellis upstream、全局 npm、系统 Python、真实业务 checkout或生产状态。
- 不通过安装系统 `jsonschema` 掩盖 wrapper 漏洞。
- 诊断日志只保留在隔离临时目录，不进入 release artifact。
