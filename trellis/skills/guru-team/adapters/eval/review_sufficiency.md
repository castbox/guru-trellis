# 当前审核充分性行为采集

此工具在隔离目标中通过完整匹配 provider 的原生产 owner 采集真实 Agent 行为。
它不是新 Skill、充分性判定器或正式 Task gate。`execution_complete` 只表示 native
调用实际结束；AI 验收方必须独立读取原始工具轨迹和最终报告，判断审查是否充分。

```bash
python3 trellis/skills/guru-team/adapters/eval/review_sufficiency.py \
  --source-root /absolute/frozen-source \
  --output /tmp/review-observation-B --case B --python /path/to/python3
```

输出目录必须不存在，且应位于仓库外。运行前从确切 Git commit 冻结旧完整源；新侧使用
明确固定的完整候选源。不要把同步修改中的源码作为旧侧。工具保留原安装命令、stdout、
stderr 与返回码，然后从该源的匹配 Core 文件建立无 Task 的 fixture，调用原 preset installer。
这只建立评测前置，不证明完整安装或 Release 矩阵。安装错误保留原诊断，不降级成方法片段。

案例 A 通过 Clarify 原需求审核入口处理本地 Issue 草稿，并保留其真实 Discovery 等前置；
C 通过 Wording `explicit_paths` 审核明确选定的设计与实施文本，不冒充正式 Planning
Approval。B、D、E 走独立 `guru-review-change`，保留三名实际独立子 Agent 和架构先读要求。
B 在相同真实 thread 上接续两个用户请求：宿主更新候选后复审，再在无变化条件下结束。
所有 fixture 都只有原始对象与来源约束；具体预期 findings、合法对照和必要缺口由验收侧在
首次执行前持有，不进入被测 Agent 输入，也不由采集器计算结论。

CLI 保留现有模型、provider 和推理配置，不指定模型。单次调用关闭 hooks、apps、memories，
通过 `mcp_servers={}` 排除无关连接，使用 `--no-daemon`。默认采用 read-only sandbox；
若系统 sandbox 阻止原 managed runtime 正常执行，可明确选择 `--sandbox danger-full-access`，
并在旧新两侧保留相同条件。原审查请求仍为只读；每轮比较对象文件字节，记录实际改动。
工具不读取凭证。read-only 不等同文件读取隔离，提示明确限定目标 provider 与当前对象。记录实际
环境差异；不要将受全局 Agent 指令影响的结果称为通用行为保证。

每轮保留实际 prompt、argv、events、stderr、返回码和真实 thread 身份。超时、非零返回、
缺少完成事件或身份冲突不算执行完成。首次失败不能覆盖；恢复使用新输出目录并说明原因。
原始轨迹留仓库外，分享前按原敏感数据规则核查；任务内只保留本次所需的最小观察摘要。
运行机械测试：`python3 trellis/skills/guru-team/adapters/eval/review_sufficiency_test.py`。
机械测试只验证 thread 接续及原始失败保留，不验证审查语义。
