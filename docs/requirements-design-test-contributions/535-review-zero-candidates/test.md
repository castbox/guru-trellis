# #535 验证策略与实际结果

来源与贡献状态见 [manifest](manifest.yaml)，需求和设计分别由 [requirements](requirements.md)、[design](design.md)拥有。

| Test identity | 入口与观察 | 实际结果 |
| --- | --- | --- |
| T535-01 | Branch 原 schema/validator/wrappers，current初始/最终、bounded continuity、archived各 consumer | passed：Branch package 39 tests；真实 []、非空 rejected、有 finding、缺必需 evidence、孤立 refs 与正常 stale 均覆盖。 |
| T535-02 | Delivery 原 schema/runtime/public wrapper 与原非 ready routes | passed：Delivery package 21 tests；真实 [] ready、非空 rejected、qualified finding/proposal、缺维度/conclusion 与正常 drift 均覆盖。 |
| T535-03 | 完整实际独立零候选 Branch recorder→checker→invoke 及 Delivery public invocation | 尚未执行；package fixture 不是独立 semantic 或当前 task 的正式结果。 |
| T535-04 | 实际非空 rejected 与正常 qualified finding 的 qualification 和原 route | 尚未执行实际 semantic 链；T535-01/02只证明定向 wrapper/runtime 消费。 |
| T535-05 | canonical/dogfood/apply/reapply、mode、投影/sidecar/drift | passed：正规 reapply/installed activation 与 drift成功；首次51份.bak逐个等于HEAD旧内容，处理后无未解决 sidecar。 |
| T535-06 | 一个完整 clean Codex installed 的原公开链与 reapply | passed（安装与确定性 wrapper 层）：锁定 Fork 0.7.0-castbox.3 marketplace init、完整 preset apply/reapply installed/activation 均成功，sidecar为零。Branch9项原record/check/invoke定向测试及Delivery14项原runtime/invoke测试通过；两个package共124份installed文件字节/可执行mode匹配canonical。独立实际语义链见T535-03，不能由这些fixture推定。 |
| T535-07 | JSON/Python/shell、task context、candidate commit-message、diff checks | JSON/Python/shell/task context/diff passed；commit-message需原 TaskCommit候选，尚未执行候选检查。 |

首次失败：#292正常正式 TaskCommit 后完整独立 Review无真实候选，原 Branch recorder 在 candidate_classifications schema validation阶段拒绝 []；没有取得正式 passed，不修改该历史现场。

共享 reviewed-content identity integration 两项错误：读取 intermediate receipt 时缺 status/algorithm。HEAD原测试代码在当前runtime下同样复现两项错误；本次仅移除其虚构 no-defect fixture，未改变 receipt 实现。不以此声称该 suite通过，也不扩大修复范围。

安装 setup曾误将 init cwd 设为临时父目录；生成文件已保留隔离，正确目标重新 init。这次 setup不计验收。安装测试 harness首次遗漏 installed runtime导入路径、随后将receipt schema根定位错误；原wrapper执行成功但harness解析失败，纠正为真实installed位置后定向tests通过，无产品机制修改。canonical/source与dogfood/installed registry检查均通过；pinned Branch5/6字节保持。#292恢复、正式版本、业务部署和完整 Release矩阵保持各自外部 owner，不能由本Task结果推定。
