# v0.7.0-guru.3 发布准备需求

## 来源与交付边界
需求来源为 https://github.com/castbox/guru-trellis/issues/500 。本 task 的 source disposition 是 reference_only，独立交付 Stage 1 准备内容；终态归档由 Completion/Closure 后的 Finish owner 承接。Stage 2 exact-candidate、tag、tag-pinned smoke、GitHub Release 和 Issue closure 由同一 Release Issue 在准备 Delivery/Finish 合并后继续承接，不属于本 task Completion。

## R500-01 版本身份
根 README、workflow README、preset README 与 public-docs spec 明确 repository 目标 tag v0.7.0-guru.3、extension 0.7.0-guru.3、Fork CLI/core 0.7.0-castbox.3、source castbox/Trellis@cc5f9a30652be29cffee9acc7e14d5dc5daaf04c、pnpm@10.32.1、CI 37647767799、已发布 predecessor v0.7.0-guru.1。版本轴独立，不发布中间 .2，不递增 extension，不改 source lock。

## R500-02 来源与升级文档
未发布候选的 marketplace/preset 指向同一完整远端 SHA；只有目标 tag 已发布且远端核验匹配后，使用同一 immutable tag。公开文字不得提前宣称 candidate gate 或 Release 成功。安装入口继续使用官方 workflow marketplace/preset；旧安装走 guru-upgrade-installation，覆盖已接受的 0.6.x/0.7.0 系列，按实际 receipt/ownership/core/task 区分正常来源，保留业务定制、dirty/untracked 和当前任务状态。普通 update/reapply 不替代迁移；legacy nonterminal pinned-old/deferred 与实际来源 rollback 边界保持原合同。

## R500-03 Docs authority
以 docs/requirements/README.md、docs/design/README.md、docs/test/README.md、docs/architecture/README.md 的 active .75 为事实来源；修正 public-docs 与 architecture usage 中的版本/来源投影漂移。Architecture/RDT owner 判定 no-op 或真实贡献；仅真实 requirement/design/test 或 Architecture 增量形成隔离 contribution，并在独立 pre-promotion Branch Review 后串行 promotion。历史 authority、tag、manifest、归档和首次失败证据不溯源改写。

## R500-04 独立准备交付
完整准备 diff 完成 scoped Phase 2、精确 task commit 和独立 origin/main...HEAD Branch Review。若 promotion 改变 delivery bytes，再执行 fresh Phase 2、commit、完整独立 Branch Review。Delivery PR 为中文 Refs #500；Completion 仅覆盖上述完整准备范围，Closure 为 no_mutation。Finish 与资源 cleanup 按各 owner 合同执行。

## 验收
A1：四个公开文档的目标版本/来源一致，manifest 与 source lock 固定值不变，候选与已发布状态不混写。
A2：公开安装/升级入口保持 canonical Skill 和 marketplace/preset 合同，不新增 alias、fallback、双读或自动迁移。
A3：Architecture/RDT projection 与唯一 active authority 一致；owner 输出不存在未处理的 sync/conflict/incomplete；需要的贡献晋升完成。
A4：source/installed package validator、四平台 source parity、私有 release Skill 四份字节 parity、ownership 与 dogfood drift 通过；git diff --check 无输出。
A5：无 task-local release notes、PR/Release body handoff、动态发布 checklist 或 tracked gate/progress/authorization。
A6：准备 Delivery 完整交付构成 task Completion 的验收范围；#500 保持 OPEN，Stage 2 尚未执行的门禁被明确保留。Finish bookkeeping 是后续终态动作，不是 Completion 的前置条件。

## 排除
不修复 inventory/runtime 产品逻辑，不修改公共 API/schema/Skill owner，不部署或升级真实业务仓，不发布 Fork/npm，不执行完整多平台/native-host 累计矩阵，不把早期 SHA 验收当作最终 candidate 证据。
