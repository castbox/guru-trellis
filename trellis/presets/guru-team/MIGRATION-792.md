# #792：当前出口查询与按步骤加载迁移

## 采用单位与公共调用

完整 matching 单位包括 marketplace `workflow.md`、`references/routing.md`、
`references/legacy.md`、原 Skill packages/Interfaces、查询及图校验 runtime、
preset 受管资产清单，以及实际受影响的平台入口/spec。Skill id、schema、typed exit、
consumer id、Task/Delivery API 和原语义门禁保持。

原 `discover-skill-contract` 新增 `--exit <id>`。`--root`、`--mode source|installed`
和 `--skill <producer>` 继续定位实际 provider 与 Skill；`--json` 保持原输出入口。
省略 exit 时，保留原 public contract discovery。提供 exit 时，一次查询投影唯一
consumer、该出口的 output/input/projection 合同，以及消费者入口和前置。
响应由当前 AI 直接消费，不是新 Skill DTO、语义 pass、授权或长期恢复记录。

正常新 runtime 直接采用 reference-only，不读取旧 inline graph，不在缺失引用时
fallback。完整图、router/stop 条件仍由 workflow-owned Markdown 单写；Interface
仍拥有各 Skill 合同。原始类型的 unknown、multiple、unmapped、缺引用和
mismatch 均非零停止，不能返回成功空 consumer 或猜测下一步。

## 已有 checkout 与在途工作

已有 checkout 沿原 `guru-upgrade-tools` 的完整目标来源合同更新，保留当前 Task、
Delivery、scope、plan、selection、固定 development baseline 和原副作用事实。
需要整套旧安装升级时，进入原 `guru-upgrade-installation`；真实 legacy Task
转换、手工 archive resume 或历史保留由原 `guru-maintain-legacy-task` 承接。
这些 owner 的 entry、profile、source pin、支持家族和回退条件保持，不能按版本号
一刀切，也不批量转换无关 Task 或改写历史归档。

工具更新前，旧安装继续使用自己的完整 matching provider。新 workflow 与旧
runtime/缺失 reference 混装时，停止依赖调用，回原 tools owner 补齐完整采用后再试。
不手工覆盖受管副本，不借普通 apply 阻塞扩大为历史迁移。丢失语义结果仍回原
producer；同对象恢复不从 phase 或文件存在制造 Planning、Check 或 Review pass。

marketplace workflow 更新保留官方预览/应用顺序：先用同 provider 的
`--create-new` 生成 `.trellis/workflow.md.new`，由原 owner 核字节、live identity、
sidecar 和用户修改，再显式 `--force` 应用，最后按原安装 owner 同步完整 preset。
预览本身不代表应用确认或匹配安装成功。`.new`/`.bak` 通过原 owner 逐项处理，
保留用户内容；不修改上游 extractor、hook、全局 npm 包或 node_modules。

## 正常加载与维护加载

Phase Index 紧邻 Phase 1，只提供全局约束和当前入口。唯一 continuation 继续从
实际当前会话和公共 Task/Delivery 事实定位原 owner；完整接收会话/phase/recovery
矩阵保留在同一 workflow 的按需章节。原 `get_context.py` phase/step/continuation
接口和声明不变，当前 phase 仍不代表任何语义通过。

正常路径只识别旧状态并转交原维护 owner。实际维护入口加载 managed legacy
reference 和原 package references，保留 family、conversion、control-retirement、
manual archive resume、historical closeout 的完整合同及准确历史来源；不复制迁移算法。

## Verifier 历史观察边界

compatibility verifier 的原 before-snapshot 可以继续只读观察明确的旧 inline 样本。
这是该 verifier 既有历史输入覆盖，不赋予正常新 runtime 或 installed validation
接受 inline 的资格。新 candidate preview 显式读取其 matching source reference；
installed snapshot 读取 matching installed reference，二者不能混用。
由 verifier owner 维护这条观察分支；当其受支持 before 样本不再包含 inline 时，
删除原观察分支及对应定向用例。不因本项 reader 改动执行完整矩阵。

## 验证与结论边界

验证公开 source/installed 查询的合法 consumer、普通错误停止与合法权威演进；
验证原生 phase/step/唯一 continuation 的实际提取、原 legacy 合同可达、source/installed/
preview 对同一图的消费、受影响平台和 dogfood drift，以及实际 AI 查询/加载消费。
分别报告 source 静态、installed 投影和实际 Agent 行为，不以行数、关键词数量、
模板或安装一致代替语义判断，不承诺固定成本降幅。

本迁移说明不声明实现、安装或实际平台行为已验证。当前 Task 的最终证据由原
Check/Review owner 消费；本项不承担完整多平台安装、升级或 Release 矩阵。
