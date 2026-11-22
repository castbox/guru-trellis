# #908 追踪与整合边界

原完整来源为 Git `2acab7fadebf57c2f2560451b9ff2a050d8811f5` 的 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`。原 owner 为 `guru-maintain-requirements-design-test-ssot`，authority identity 为 `guru-trellis-rdt`，状态 active。完整 proposed after 保留 RDT-REQ/DES/TST-LIFECYCLE 身份，只更新当前 Publication readiness 表述，不创建第二 current，不改共享入口或全局版本。

| 当前行为 | 要求 | 设计责任 | 验证 |
| --- | --- | --- | --- |
| Publication preparation 链 | R531-05、R636-04/05、R794-05、R900-01/02 | D531-05、D636-04/05、D794-02、D900-01/02 | T531、T636-05、T794-01/02、T900-01/02 |
| 子切片成果与 readiness | R649-03、R657-04、R713-05 | D649-02、D679、D713-05 | T649-02、T657-06、T713-03 |
| 旧 Draft、same-PR 和已合并恢复 | R636、R635-03、R637-06、R794-06 | D636-02、D635-03、D637、D794-04 | T636-02/07、T635-03、T637-06、T794-04 |

R856 的错误边界、R899 的续接读取和 R900 的完整发布入口保持 current。Architecture candidate/final 判断为 `no_architecture_impact`，本贡献不创建 Architecture contribution、ADR 或 project-check burden。

Planning 批准且工程验证完成后，原 RDT owner 重读 live current、本贡献完整 proposed、实际实施结果和必要关系，将 proposed after 写入 current、逐文件 readback，并记录 `integrated_pending_review`。当前 private release regression 11/11、upgrade installation contract 35/35、source/platform validators 和 focused Codex 来源样本均通过。随后 TaskCommit 纳入实际 after，固定 committed candidate 的独立 Review 审核真实 before/after。本文不预先声明 Review 或发布通过。
