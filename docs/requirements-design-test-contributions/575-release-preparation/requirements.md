# #575 S2/S3/S4/S5：来源、工具采用与完整准备需求

本贡献以 RDT `.100` 为前驱，继承 Architecture `.93/active`；[S1](../575-source-adoption/requirements.md)保留正式来源采用与历史公开映射。依据为 #575 Stage 1、Task 整体 R575-01..07 及当前同 Delivery 的来源准备规划。软件发布目标与知识版本独立；实际结果仅由 test.md 拥有。

| Requirement / Behavior | 必须满足的行为 | Design / Test |
| --- | --- | --- |
| R575-S2-01 / BEH575-S2-01 | canonical extension、原 maintenance target、生产结果、schema/example/stop consumers 同步 `.4`；保留合法旧族、predecessor 和原 source 检查，正常 preset resume 使用 managed interpreter | D575-S2-01 / T575-S2-01 |
| R575-S2-02 / BEH575-S2-02 | M 已采用的 installed `.3` 基础图及固定 Fork Task2/session3 与自身 receipt 一致，历史身份、配置和原生资产保持；不声明 `.4` parity | D575-S2-02、03 / T575-S2-02、04 |
| R575-S2-03 / BEH575-S2-03 | 四份当前源码公开映射准确表达 `.4` 未发布、CLI/Core `0.7.0-castbox.3` 和固定 Fork；稳定 `.3` tag、旧锁与历史证据保持原归属 | D575-S2-01 / T575-S2-01、02 |
| R575-S2-04 / BEH575-S2-04 | 最小证明覆盖 source/graph、现存 `.3` receipt、固定 Fork native、版本消费者及模块恢复、ownership/平台入口/卫生/secret scan；source/installed/fixture/外部层次不混用 | D575-S2-02、03 / T575-S2-01、02、04、05 |
| R575-S2-05 / BEH575-S2-05 | 原 RDT owner 在独立 draft 贡献完成当前切片 reconciliation 与双向 trace；完整贡献与 shared promotion 留给 S3，晋升前后分别执行原 committed Review 门禁 | D575-S2-04 / T575-S2-06 |
| R575-S2-06 / BEH575-S2-06 | S2 经 Check/TaskCommit/独立完整 Review、Refs-only Delivery 形成真实 clean committed `.4` source；S3 消费该来源后，Whole Completion 才判断全部准备责任，Closure/Finish 与软件发布独立 | D575-S2-03、04 / T575-S2-03、06 |

## 后继范围与历史边界

旧草案将完整 `.4` 投影与正式维护证明放入 S2；当前规划用 S2 来源→S3 正式消费替换其来源循环，既有身份保留但不将旧草案作为当前验收。原 S3 已按实际来源依赖分为当前来源修复与后续完整安装 Delivery；后者承接全 `.4` packages/runtime/schema/四平台投影、三平台 reapply/drift、focused Codex clean/local-workflow、真实 stable `.3` predecessor 维护、native/下一 owner、同操作 resume、不兼容单侧 tools rollback 和最终 contribution/promotion。其设计与测试定位见 D575-S2-03/04、T575-S2-03/06；这些义务继续归同 Task R575-03..07，不能由 S2 合并消除。

不新增 API/owner/兼容 reader/恢复框架，不纳入 #577/#46 产品实现，不升级真实业务仓或执行累计多平台/native-host 矩阵。最终 main exact candidate、远端 immutable provider、tag smoke、Release 与 Issue 关闭仍归 #575 Stage 2。

## 当前来源修复增量

本轮贡献以 RDT `current-main-0.6.17-guru.101/active` 与 Architecture `.94/active` 为适用 authority；上述 S2 来源、结果及其当时 `.100/.93` 身份保留历史归属。当前 S3 的独立交付不删除同 Task 后续完整安装责任。

| Requirement / Behavior | 必须满足的行为 | Design / Test |
| --- | --- | --- |
| R575-S3-01 / BEH575-S3-01 | `validate_installed=False` 只验证 canonical 来源，不读取 target installed manifest；default/True 继续要求并验证原安装证据 | D575-S3-01 / T575-S3-01 |
| R575-S3-02 / BEH575-S3-02 | 在原 validator 与 preset source-only 调用边界证明同失败点修复，并保留 default/True 对照；模块证据不冒充正式工具安装 | D575-S3-01 / T575-S3-01、02 |
| R575-S3-03 / BEH575-S3-03 | 先经原 Check/TaskCommit/完整独立 Review 交付可消费的真实 source；后续完整安装使用新的 source_locked 操作，不变更旧 recovery/source/preimages | D575-S3-02 / T575-S3-02、03 |
| R575-S3-04 / BEH575-S3-04 | 当前只收敛既有 draft contribution 与双向 trace；完整安装、最终 RDT promotion 前后门禁、Completion/Closure/Finish 留同 Task 原 owners | D575-S3-02 / T575-S3-03 |

## 工具采用、平台证据与正常捕获修复增量

当前 S4 沿 RDT `.101/active`、Architecture `.94/active` 承接根 R575-01..07；S2/S3 上述来源、失败、回滚和未完成描述保留原观察时间。下列要求与设计/测试定位只定义本切片责任，不提前宣称整体完成。

| Requirement / Behavior | 必须满足的行为 | Design / Test |
| --- | --- | --- |
| R575-S4-01 / BEH575-S4-01 | 从真实已提交修复源建立新的正式 source_locked tools 操作，当前 checkout 完整 `.4` 投影可由自身 resolver/native 及下一实际 owner 消费；保留 Task/session/历史/配置与 peer/common | D575-S4-01 / T575-S4-01 |
| R575-S4-02 / BEH575-S4-02 | A含旧归档只走 tools-only；同源无旧归档B证明普通三平台apply/reapply/drift，Shared/Codex/Claude/Cursor source及私有release Skill投影一致，ownership/权限/退休项/sidecar/卫生真实可核实 | D575-S4-02 / T575-S4-02 |
| R575-S4-03 / BEH575-S4-03 | 正常CLI两流分别strict UTF8消费，stdout数据不混入stderr；日志/错误保留完整诊断和真实exit/timeout，定向回归与同Fork init证明原解码阶段；禁止quiet/filter/替换解码/放宽timeout | D575-S4-05 / T575-S4-05 |
| R575-S4-04 / BEH575-S4-04 | 本切片唯一Test/trace收敛，保留完整clean、真实predecessor最终证据判断和最终RDT/晋升义务，WholeCompletion路由后继而不预造key；Refs-only不充当整体完成 | D575-S4-04 / T575-S4-04 |

当前R575-S4-03的捕获修复替代原S4方案的执行顺序，不删除根R575-04/A575-05的完整focused与真实predecessor要求。保留的整体责任由D575-S4-02/03、T575-S4-02/03定位；原首次focused失败与真实predecessor结果分别记录，当前捕获回归不能改称完整clean通过。最终promotion仍遵守根R575-05/06与私有release合同。


## 完整 clean 与最终准备收敛增量

S5沿当前RDT `.101/active` 与Architecture `.94/active` 承接根A575-01..08。S2/S3/S4的原要求与历史层次保持；当前行为只补齐完整样本和最终Docs责任。来源为 live #575 Stage1及既有staged plan，实际执行结果只读test.md，不从本表推定通过。

| Requirement / Behavior | 必须满足的行为 | Design / Test |
| --- | --- | --- |
| R575-S5-01 / BEH575-S5-01 | 从包含捕获修复的真实clean committed source及其同一完整SHA的真实远端provider、正式Fork执行原完整Codex focused；init/preset、两轮update/reapply、native load和session binding全部观察，保留真实退出/首失败；原local-sample失败不改称修复，准备SHA不充当Stage2最终main | D575-S5-01 / T575-S5-01 |
| R575-S5-02 / BEH575-S5-02 | 对根定向来源/工具/平台/真实stable predecessor证据按当前依赖独立终审；可核实且未受影响的原事实注明来源采用，缺失/变化/不确定补受影响验证；不把旧安装重命名为新source执行 | D575-S5-02 / T575-S5-02 |
| R575-S5-03 / BEH575-S5-03 | 既有唯一五文件及Test/双向trace完整收敛，首次完整committed Review后原owners按expected-current串行晋升，shared差额重新Check/TaskCommit/不同reviewer完整Review | D575-S5-03 / T575-S5-03 |
| R575-S5-04 / BEH575-S5-04 | 当前Refs-only交付及WholeCompletion、reference_only Closure、Finish保持原owner；Stage2最终main/provider/tag/smoke/Release独立，未验证层次不提升为完成声明 | D575-S5-03 / T575-S5-03 |

上述承接根R575-04/A575-05及R575-05/A575-06，S4的有界捕获回归不替代R575-S5-01。完整累计多平台/native-host、真实业务安装升级/原始在途/生产仍为未验证边界；不扩张其它Open Issue或新增产品机制。
