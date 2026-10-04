# #489 发布准备设计

## 唯一修改路径

现有公开文本是发布身份说明的 owner。直接更新根 README、canonical workflow/preset README 与 `.trellis/spec/docs/public-docs.md` 的 tag/predecessor 和 immutable安装引用；不添加 runtime adapter、状态文件、writer、兼容 fallback 或新 package。

canonical `trellis/guru-team-extension.json` 与 `trellis/presets/guru-team/source/trellis-source.json` 是版本/source权威。本任务读取并核验它们，已符合 #489/#490 的值不为标记进度再次修改。公开 README 的已构建源码使用同一 canonical pin；本次发布流程只读使用现有产物。

## Docs SSOT Plan

strategy：`ssot_first`。durable_paths：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/docs/public-docs.md`。依序读取三个 RDT current入口与 Architecture baseline/constitution/change-contract，以既有 release-axis 契约约束当前值；owner正式审查无新增需求或架构语义时保持当前知识版本，并仅同步上述项目使用投影。确需 shared-current promotion 的变化走既有串行 owner，不写平行 SSOT。

## Subtraction 与兼容

code_subtraction：只改 Markdown 当前值，不产生新代码或退出待清理资产。docs_ssot_subtraction：用目标身份替换过时当前值，历史 predecessor与版本正文保持字节；不复制完整历史合同。旧安装拒绝语义沿用 current Fork，Stage 2验证真实拒绝及数据不变，绝不声称升级成功。

## Owner 与阶段

独立 pre-promotion Branch Review仅审查准备 diff；需promotion时后续完整review重新开始。Delivery使用中文 Refs #489，Publish/Merge既有owner执行。Completion确认全部准备scope后，reference-only Closure返回no_mutation，Finish独立持久化终态归档并合并bookkeeping。最终发布候选仅在这两次merge之后冻结。

## 可验证性与风险

source/installed validators、四个平台 source投影、ownership、dogfood overlay drift与diff hygiene证明准备字节一致。每项Stage 2 gate绑定fresh exact候选；本任务不把旧日志、本地workflow样本或projection parity描述为最终remote/native proof。无部署、DB、CI或秘密配置变化。
