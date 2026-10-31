# 需求探索多轮方法试验

此测试工具采集真实 Codex 对话，不属于生产工作流或通用语义评分器。
它位于原 eval adapter 目录，可能随完整安装分发；分发不建立生产调用或正式 Skill 入口。
它只在临时只读 fixture 中提供当前共享交互、Clarify 探索和 Author 来源处理方法、合成仓库事实。
fixture 没有 Guru runtime，不产生正式 context_ready、Approval 或其他生命周期结果。
正式问题记录的形状与 partial 约束由原 recorder/checker 定向测试另行验证。

```bash
python3 trellis/skills/guru-team/adapters/eval/decision_dialogue.py \
  --case lightweight-partial-correction --output /tmp/guru-decision-dialogue-run
```

输出目录必须不存在。使用当前 CLI 配置，不覆盖模型。可用 `--source-root` 指向匹配的旧版
checkout，在相同案例、CLI配置和条件下另跑对照；不是在脚本中预填旧版或新版的预期答复。
`--timeout` 是全部轮次共用预算。第一轮只提供当前请求和事实；后续合成用户回复仅在下一轮
通过真实 thread.started 身份 resume，不使用 --last。review_focus 不提供给被测 Agent。
当前 fixtures 与规则不要求联网；CLI 凭证沿本地既有机制使用，工具不读取或复制凭证。
驱动关闭 hooks、apps、memories，并使用 --no-daemon。运行者须先确认已配置的 MCP 名称，
对每个名称提供 `--disable-mcp NAME`，关闭不相关连接；工具不读取包含凭证的用户配置。
只读 sandbox 防止写入，不宣称它是文件读取隔离；fixture 明确要求不访问外部路径。
全局 Agent 指令或额外工具若影响实际对话，应保留为试验条件及限制，不冒充干净安装行为。

每轮保留实际 prompt、events、stderr、argv、退出码与完成事件。超时、非零退出、身份不匹配、
缺完成事件或无法启动均不算执行完成。`execution_complete=true` 只代表所有轮次运行结束，
不是语义通过；stderr/events 可能含本地路径，分享前按原敏感数据规则核查，不上传原始凭证。

AI reviewer 读取案例 review_focus 和完整实际输出，判断：是否漏问、多问、使用不可行选项、
把推荐当默认、忽略部分回答，或在最终方案中忽略用户修正。还须核对实际文件读取和未答停点，
区分计划、实施与未知。报告逐例结果、失败及限制，不以关键词或问题数量替代判断。
此方法试验证据不证明 Guru 自动路由、原 owner 正式调用、完整安装或生命周期行为。
