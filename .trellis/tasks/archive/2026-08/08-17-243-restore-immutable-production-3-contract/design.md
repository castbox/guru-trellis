# Design

## Root Cause

#237 的提交 `cef73ece` 将 versioned immutable legacy asset 的 EOF 空行当作普通格式问题删除，同时刷新了 installed copy 与 extension manifest，从而把错误字节合法化为当前 managed inventory。既有回归测试仍保存正确的历史摘要，因此稳定失败。

## Change Design

1. 从 `cef73ece^` 恢复 canonical `production-current-3.0.json` 的完整字节，不重排或重新序列化 JSON。
2. 运行 preset apply 使 installed copy 与 managed manifest 由 canonical source 收敛。
3. 检查实际 diff 只包含：canonical asset、installed asset、extension manifest，以及 task-local artifacts。
4. 用固定 SHA、byte equality、targeted unittest、preset/package tests、source/installed validator、ownership、overlay drift、sidecar 与 bytecode snapshot 验证。

## Boundaries

- 不改变 current v4 contract、schema、runtime route 或 public API。
- 不更新 expected digest 来接受新的历史字节。
- 不执行 throwaway 安装和 live model matrix。
- 不修改 release task #242 的 metadata；合并后由 #242 重新冻结 candidate。
