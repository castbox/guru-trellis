# Implementation Plan

1. 修改 canonical `.agents/skills/release-guru-trellis-version/references/contract.md`，把三个
   Finalizer 内部分段确认收敛为一个 exact transaction confirmation。
2. 更新 `.agents/skills/release-guru-trellis-version/tests/test_contract.py`，断言新的确认矩阵，
   同时保护 Merge、tag、smoke、Release、closure、cleanup 独立边界。
3. 同步 Codex、Claude、Cursor projection，并核对字节一致性。
4. 运行 focused tests、source/installed validators、projection/ownership/reapply/drift/residue
   checks，根据真实 finding 修正。
5. 完成 Phase 2、受控 commit、完整 diff Branch Review、Publication、Finalizer 和 Merge。
