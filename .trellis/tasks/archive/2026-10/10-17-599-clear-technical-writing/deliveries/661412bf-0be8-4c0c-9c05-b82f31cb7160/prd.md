# Delivery D1：清晰技术写作规范

## 切片与来源

本 Delivery 完整承担 [整体需求](../../prd.md) 的 R1-R5 和 AC1-AC8。唯一来源为 https://github.com/castbox/guru-trellis/issues/599。无独立剩余切片。

## 行为要求

- 一份 canonical managed-spec 正文，覆盖全部新写或修改的自然语言；保留业务语义及字面例外。
- 首次实质输出前读取完整规范；加载期间提示和缺失诊断受简短入口规则约束。
- 无 Task、正式 Task、task-free、独立 Git/GitHub、恢复和子 Agent 使用同一正文。
- 写作 owner 自检；审核 owner 保持原范围。建议不阻塞，正确性及适用强制规则违规要求修订。
- AC5 必须在实际支持平台验证；源码、投影和实际行为分开记录。

## 验收

AC1–AC8 的逐项通过条件完整引用整体 PRD，不缩减。正式来源、双语逐例语义检查、实际 Codex 加载/recovery/child、匹配完整安装/reapply/用户指令保护、22 平台定向投影和 dogfood drift 都属于本切片。完整升级/Release 矩阵为明确未验证边界。
