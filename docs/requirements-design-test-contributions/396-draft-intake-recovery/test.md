# #396 唯一测试与证据结果

当前状态：实施中，尚未宣称 complete Task gate、交付或生命周期完成。

| Test identity | 覆盖 |
| --- | --- |
| T396-01 | 实际 producer -> 最小 Readiness -> record.result/check receipt/invoke -> ready。 |
| T396-02 | 五误操作、正确拒绝、原 producer 不变的 consumer 重建。 |
| T396-03 | 正文刷新、旧摘要拒绝、缺真实前序。 |
| T396-04 | native Agent 恢复与缺前序，两次 transcript 由 AI 独立阅读。 |
| T396-05 | canonical/dogfood/installed、selected-platform、clean preset/reapply/drift/hash/mode/sidecar。 |
| T396-06 | 全 Task、Architecture、Branch/Delivery/Completion/Closure/Finish 的实际 gates。 |

## 客观执行结果

使用 canonical `runtime/resolve-python.sh` 的 managed interpreter 执行 unittest；生产 wrapper 再使用其自身 managed launcher。Readiness package `tests/test_contract.py` 22 tests passed；完整 `ReadinessAdapterTests` 9 tests passed（110.657s）。最终 source/producer mismatch 不再被 fixture 重标身份后，5 个 draft/公开recipe/恢复/正文刷新/缺前序 tests passed（55.133s）；不把首轮结果当作最终变更重跑。

T396-01：原 Sync/Discovery/Clarification/Wording 生产命令生成真实 public outputs；canonical Markdown 中公开 Python recipe实际执行最小 authoring，record.false/result → check.false/result.validation_receipt → invoke.ready。fixture semantic shape 仅测试传输与校验，不是 AI review。

T396-02：draft target 带 caller_locator/request_id 时，现有 normalization 接受并归一化忽略；缺真实 draft_id 仍拒绝。body-only authority、自造 draft_id、自包含 linkage 与旧完整 result 局部补算均由真实 recorder 拒绝；从同一 source 和未改 producer 重建最小 consumer 后 ready。未增加 extras 必须拒绝的新限制。

T396-03：正文正常改变后，实际前序重新执行形成新 authority/locator，旧 source digest 与旧 receipt 被拒绝；original context_current/clarity_current 分别支持声明重入，ready 缺 Wording 报 transition.stage 错误，无真实 transition 时停止。

## 真实 native Agent 与 AI transcript review

T396-04：既有 `formal_exit_boundary.py` 新增 readiness-error/readiness-missing 两种事实入口；在完整 installed fixture上使用本机 Codex CLI 0.160.1，各执行一次真实 native continuation。Prompt只给现场 source/public输入/真实producer/error/目标与副作用边界，不给 expected pass、手写receipt或private helper。

恢复运行的初始真实错误为 `stale_identity / target`（body SHA 当 authority digest）。Agent读取 installed Skill/contract、当前业务源、文档和 Git历史，独立写出十个具体维度判断及 scope conclusion，只 author Gate三字段，直接保留实际 Wording transition。record/check/invoke各返回0；整体消费record.result与嵌套checkerreceipt，实际正式出口ready。读取唯一 router及guru-create-issue entry 后停止，没有创建。

缺前序运行的初始真实错误为 `schema_mismatch / transition.stage`，最后实际producer是clear/clarity_current。Agent形成缺Wording finding，首次恢复误写consumer.target，recorder返回 `schema_mismatch / semantic_review.ai_review_gate`；Agent自行读合同修正为consumer.id，重新执行record/check/invoke，实际正式出口review_wording。它读取Wording entry后停止，没有合成ready/producer/receipt。保留首次恢复失败，不记为通过。

父Agent阅读两次实际transcript及完整命令stdout，分别审查以上判断/动作：两次producer文件字节不变、业务源不变、最终fixture Git工作区干净；全过程没有重复确认同范围无副作用修正，没有Issue/Task/branch/worktree或Git publication。此证据限定本机两次真实执行，不推定其它模型/平台的Agent交互效果。runtime实现/schema/interface均未修改，根因闭合在consumer指导与回放。

## 分发与安装结果

T396-05：source ownership validator passed；当前dogfood apply按正常managed升级产生19个.bak，逐一核对与原HEAD相同后移至临时备份，随后reapply.status=ok、installed/activation passed、sidecars=[]。dogfood drift passed，Shared/Claude/Codex/Cursor实际selected projection与canonical一致，hash/mode由installed validator检查。无.new或未知本地冲突。

一个代表性全新preset目标（先装canonical workflow再apply）clean.status=ok、同一目标reapply.status=ok，selected platforms=Claude/Codex/Cursor、installed/activation passed、零sidecar/conflict；安装后复用原fixture helper执行实际context/clarity/wording → readiness.ready，producer不变。TemporaryDirectory最终清理，不创建真实用户测试资源。

Native准备失败单独记录：初次安装尚未放workflow，被installed gate拒绝；调整顺序后fixture未建立clean Git baseline，Sync如实停止；之后seed脚本引用已由fixture省略的body_sha字段导致KeyError。三次都是测试准备/适配错误，均在真实native之前修正，不计native或安装pass，不修改production校验。

T396-06：完整Phase2、current Architecture、TaskCommit/独立BranchReview与后续生命周期仍待各owner实际执行。知识晋升不替代这些门禁。

完整多平台 init/update/upgrade/Release matrix、其他 native host/model、业务仓安装/生产部署及后续 #250/#292/#521 未验证，也不属于本 Task 验收。临时资源不进入公共 package 或 tracked gate。
