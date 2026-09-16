# #418 Requirements Contribution

状态：draft、unpromoted；唯一外部来源为 [Issue #418](https://github.com/castbox/guru-trellis/issues/418)。本贡献不是 current authority，也不证明实现或发布完成。

| ID | 必须交付的行为 |
| --- | --- |
| R418-01 | 正常归档及同一事务恢复后，源/目标task mapping收敛为精确archived locator，不重建未知映射 |
| R418-02 | archived task、worktree、branch、repository与Ready PR唯一绑定 |
| R418-03 | 已知输入、provider、stale失败保留脱敏结构化诊断，未知异常保持generic fallback |
| R418-04 | 缺少当前必要复审时，经独立Branch Review、Publication、Finalizer重新建立Merge handoff；不将旧gate或快照当pass |
| R418-05 | 复审保持task completed、archive/history、PR和远端refs不变，原mutation gates不放宽 |
| R418-06 | 覆盖双端映射、当前复审、A/H/B与title/body快照、失败分支和零mutation |
| R418-07 | canonical、installed、声明平台和preset reapply/drift保持一致 |

现有 REQ-004/005/006/008/010/012/014 与 BEH-015 的 ownership、fail-closed 和独立副作用边界继续有效。新只读能力不把纯metadata问题变为task-content restore，不承接 #398/#419/#421。
