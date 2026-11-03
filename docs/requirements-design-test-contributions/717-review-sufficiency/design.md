# #717 Design 隔离贡献

状态：proposed。完整拟写见 [D717](proposed/docs/design/current/review-sufficiency.md)，职责分别为共同规则依赖、provider/target、真实观察和分发。来源设计唯一处置仍在本批 design 第3节；RDT 不另作处置或复制专业规则。

Architecture 继承 `guru-trellis-architecture` / `docs/architecture/README.md`，独立候选/最终规划评估选择 target_native，实际 shared owner 单元/ADR 仍由原 Architecture owner 晋升。RDT 原 owner 在 candidate Check 后 final_integration 写入 manifest 的完整三层 targets 与必要导航，再读回、重绑实际候选并完成最终质量。
