# 本地 slice 验收与远端边界

版本：`current-main-0.6.17-guru.74`；状态：`active`；predecessor：`current-main-0.6.17-guru.73`。薄继承[不可变前驱](../current-main-0.6.17-guru.73/test-plan.md)；仅本版明确的来源系列、迁移和证据增量取代前驱限制，其余合同及历史边界继续有效。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.74` / `active`。知识版本不表示软件发布。

本地 family、定制、current task/control、部分恢复与真实来源回退由[唯一 Test](../../../requirements-design-test-contributions/495-upgrade-version-families/test.md)维护：26 package、2 helper，Skill/overlay canonical-only 与暂停新增工作四格实际运行、companion组合，installed/drift 均有证据。三个历史回退 finding 已修复并独立关闭；`11ef591c...6cd766dd` 完整分支复审及正式 public Branch Review passed。本版晋升 diff 仍须 fresh Phase2、TaskCommit、不同 reviewer 完整复审，不复用晋升前 pass。REMOTE 同一可寻址 Guru source 的 public/source_locked/provider/deferred 验收待候选发布，#495 保持未完成。历史 preset/Fork full-suite 首次失败不改称全套通过；Release、真实业务安装、累计多平台矩阵未执行。
