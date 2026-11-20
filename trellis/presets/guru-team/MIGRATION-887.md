# #887 Issue 创建和独立审核入口

## 当前调用

| 请求 | 当前入口 | 结果 |
| --- | --- | --- |
| 只创建 Issue | `guru-create-issue` 的直接入口 | 确认准确的待写内容后创建并回读 Issue 和审核评论 |
| 审核 Issue 需求 | `guru-clarify-requirements:standalone_issue_requirements` | 向用户返回审核范围、结论和待确认事项 |
| 审核能否开工 | `guru-review-change-request:standalone_issue_readiness` | 向用户返回当前交付单位和前置依赖的判断 |
| 正式开始工作 | Sync 后的 `existing_issue_intake` | 按原就绪审核和 Task 创建分流处理 |

先加载所选 Skill 的安装正文。其直接调用示例和证据要求在该 Skill 包中。审核者从实际 Issue 和有效讨论出发，判断还需要哪些依据。复审核对正文、讨论和有关依据的变化。当前仍适用的调查结果可继续使用。

## 旧调用和在途恢复

已进入完整链的草稿继续使用该链产生的实际 Readiness 结果。旧独立审核调用继续按进入时的 profile 完成。计划内运行期仍支持这些已声明的业务入口。固定旧 provider 已尝试的建单写入，先使用同一 provider 和确切输入恢复 Issue 与评论。

新直接入口返回 `direct_review_refresh` 时，Create owner 根据实际原因处理尚未写入的同一草稿。若只有查重过期，重新查重并核对拟写内容。若实质内容变化，沿原责任刷新受影响审查。若写入结果未知，保留原尝试身份并走原恢复入口。

## 采用

通过原 marketplace 和 preset 安装完整匹配的 workflow、Skills 和 runtime。已有 checkout 使用 `guru-upgrade-tools` 保留 Task、Delivery、session 和用户文件。运行安装包和路由验证，并处理受管文件冲突与残留 sidecar。这个入口变更随完整匹配版本分发。
