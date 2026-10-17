# D1 实施与验证计划

## Delivery Policy

类型：full。整体责任为 R1-R5/AC1-AC8，本切片完整承担这些责任。remaining_work：无独立剩余切片。独立交付条件：源码、完整安装投影、AC5 最低行为验证和原 gates 均通过。Task Completion 检查全部 AC，而不是从 PR 合并推定完成。剩余问题由同一 Task 保留，不能用 full 标记隐藏。

## Docs SSOT Plan

策略：delta_first。唯一规则正文定位见 design.md D3；业务文字和示例不复制到 docs。
原 owner 为 guru-maintain-requirements-design-test-ssot，直接 consumer 为本次 Check/Review/Completion。贡献根 docs/requirements-design-test-contributions/599-clear-technical-writing；Architecture 贡献 docs/architecture/contributions/599-clear-technical-writing.md。在最终 Phase2 前完成 contribution 与双向 trace。共享晋升在首次完整 committed Review 后进行，再对晋升差额执行 fresh Check/commit/Review。

## 实施顺序

1. 编写并自检 canonical 规则：正式来源/采用边界、稳定规则表、术语、双语正反例、语义例外。
2. 增加现有 managed-spec 映射和 AGENTS 有界加载定位；更新 workflow Phase Index/continuation、公共 Guru Skills 与22个平台 Guru finish entries 的短引用。保持全部公共 I/O、原审核范围和官方文件不变。
3. 更新三个公开 README、原 spec 导航和任务隔离的 RDT/Architecture contribution。修订本次冲突写作指令；不追溯历史文本。
4. 扩展现有 installer/platform 定向验证。通过 actual apply 同步 dogfood；逐项核对 sidecar，再运行 drift 和 source/installed checks。
5. 复用一个代表完整 throwaway 做安装/reapply与用户指令保护；其22个平台仅声明投影通过。
6. 在实际 Codex CLI/原生 child 执行 AC5，审查读取顺序和输出语义。记录 actual session/ref 与最小结果；不把原生投影检查写成行为通过。
7. 完成独立 Phase2 Architecture、正式 Check、TaskCommit、完整独立 BranchReview；处理实际 findings。晋升贡献后按原路刷新差额 gates。发布 PR 到 dev、合并、Completion、Closure、Finish 与精确 Cleanup。

## 验证映射

| ID/AC | 入口和可观察结果 |
| --- | --- |
| V1/AC1 | 读取 ASD 官方主页/About/FAQ/downloads；规范记录 Issue9/日期、已核对公开段落与未取得条款，所有 GTW 规则的强度/内容/例外齐全 |
| V2/AC3/AC4 | AI 逐例核对中英指令、条件、术语、强度、未验证结论；对照源前提检查义务/否定/例外/顺序/literal/授权功能修改/脱敏边界 |
| V3/AC2/AC7 | 正式 installer 将唯一正文投影到完整目标；解析全部22个平台入口格式并检查引用；source/installed package 与 workflow graph 定向验证 |
| V4/AC5 主会话 | 实际 Codex 无Task与绑定本次真实Task会话：首次实质输出前完整读取正文；加载提示短句且无未验证断言 |
| V5/AC5 恢复 | 以真实初始 session UUID 执行 native resume，再生成原用途文本；确认当前正文可用，丢失时重新读 |
| V6/AC5 child | 独立 child 不继承规范全文；检查实际完整原生注入或自读发生在首个实质输出前，记录实际使用路径 |
| V7/AC5 缺失/恢复 | 专用测试环境的普通缺失依赖状态：只报告具体缺口并暂停正文；通过原支持路径恢复规则后继续同一请求，不新增审批 |
| V8/AC6 | 一个代表完整安装与 reapply；目标 AGENTS 用户区块字节不变、重复应用稳定、managed-spec 正常冲突按原机制处理，零未解决 .new/.bak；dogfood drift 通过 |
| V9/AC7/AC8 | shell/Python语法、task validate、whitespace、受影响测试；分别列源码、投影与实际行为通过/失败/未验证 |

AC5 最低行为缺失就不能宣布 #599 验收通过。实际行为只声明实测 Codex，不由它推定其他平台。完整多平台 clean/existing/update/reapply/release-candidate 矩阵不在本次验证范围；软件发布和业务仓库自动升级不执行。

## 上下文

implement.jsonl/check.jsonl 通过官方 task.py add-context --delivery 写入。只列实际需要的当前 specs、规范正文和研究文件。规范尚未生成时不加入不存在的路径；生成后在原 Author/context owner 补入同路径。

## 来源语义

仅 design.md D2 拥有来源承诺处置矩阵；本文件不复制该矩阵。
