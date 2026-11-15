# D1 当前行为诊断事实

本结果供原实施协调、I4判断及后续审核使用。它不提供正式 Check、Branch Review 或整体 Completion 结果。

## 入口、运行与可查依据

当前职责来自 `.trellis/workflow.md` §2.1；其必要引用指向共享 Author 正文／模板、quality-guidelines 的 Test And Validation Value，以及 workflow-contract 的 Phase2／Candidate Applicability And Coverage。静态引用只证明可定位，以下原生事件另外证明实际读取与使用。

外置原始结果根为 `/private/tmp/guru-shared-native.4bItIl`。两例各保留 `prompt.txt`、`native.jsonl`、`native-final.txt`、`collection.json` 和实际 workspace。collector 进程最终退出0；`shared-material` 原生进程退出0，用时111.32秒；`shared-ordinary` 退出0，用时71.78秒。进程结果不代表语义验收通过。

两次实际 argv 都包含 `--model gpt-6.1-sol -c model_reasoning_effort="medium"`，并使用既有 `codex exec --ephemeral --json`。配置由 CLI 参数传递，完整 argv 在各例 collection.json。未以 prompt 或默认继承声明模型绑定。真实 upstream 为安装声明的 `e3793251fad8bd261d0c370d408c7675b9f6a140` scripts；运行前核其 HEAD 相同且工作区干净。

prompt 只给正常 Phase2职责、fixture Task／DeliveryKey／planning_root、事实位置和只读边界。被测 workspace 没有本Task／D1正文、Issue #853或collector／host评估源码。其Task、Git提交和Planning接受仅建立外置测试前置。两个 frozen/run.py 都由宿主实际执行，输出两次PEAR、一次pear后端加载；使用SDK 0.11.1和本地纯Python client，未执行草稿组合、外部服务或生产路径。

## 实际行为与初步诊断依据

| 输入 | 实际读取与判断 | 依据与限制 |
| --- | --- | --- |
| shared-material | 读取选定Task／Delivery三正文、Author正文和模板、Phase2、共享质量及消费者适用性正文，再读当前／草稿源码、生成输入、整合记录和实验。判断为原标量缓存上的适配增量，识别无参构造缺logger、代理fetch_scalar与草稿client仅有fetch_scalars的差额。 | native.jsonl第16–29行是实际工具结果；第33行最终答复。Agent明确没有运行草稿，不将静态不匹配称为本轮已执行失败。 |
| shared-material | 区分七处dirty快照预演和两个已提交dev文档冲突；明确后者不含SDK／生成器／向量草稿，不能证明草稿组合已解决。采用冻结标量局部事实，指出新组合验证缺口。独立字符串工作不必随缓存等待，但具体格式化合同缺失须回原owner补足。 | 场景维护者提供的历史记录是fixture输入，不是本轮业务merge。实际答复保留缓存和字符串整体未完成责任，没有要求另一Issue整项关闭或同步草稿。 |
| shared-ordinary | 读取同一正常入口、Author／模板、质量及消费者适用性正文；检查实际源码、生成链、版本备注、实验断言和观察，并比较五个当前／冻结Python文件及当前app/schema差额。采用宿主已有运行事实，不因标签或阶段变化重跑，不增加全Task／PR／聊天盘点。 | native.jsonl第14–27行是实际工具结果；第28行最终答复。该结论仅覆盖相同本地输入／依赖／环境／调用链；最终自检及独立Review未完成。 |

两例能把方法与实际对象、调用和证据范围连接起来，当前观察没有呈现历史G07的直接偏差。本次未预定或实施规范性修订。是否足以作无需修订结论，以及是否仍需窄诊断，由原I4与审核owner结合完整accepted scope判断；本结果不证明所有未来判断正确。

## I4 原实施协调判断

原实施协调已亲读两例实际prompt、最终答复、关键工具返回及当前collector差额。两例均从Phase2职责读取共享Author、质量与消费者适用性正文，再将方法用于实际源码和工程事实。material没有从路径重叠推导重复实现或整项等待；它将必要后继限定在构造参数、SDK接口、生成物和真实消费者验证，保留独立工作的推进边界。ordinary核对调用链与实验输入一致后采用原运行事实，没有因标签或阶段变化增加验证。

在本Task接受的当前入口和中性材料范围内，这些证据足以支持“已有能力满足目标，无需追加共享依赖规则或入口”的实施诊断结论。没有已确认的消费或具体方法缺口，因此不提出规范性修复，也不为取得同样结论追加原生轮次。该结论不是未来判断永不出错的保证；独立完整Review仍须判断本次装配、证据充分性及全部接受范围。下列收尾路径缺失保留为独立规划外观察，不作为共享依赖方法缺陷的依据。

## 定向工程检查

- `test_behavior_collection.py`：3项通过。执行真实provider／upstream Task及Delivery装配和冻结实验；native进程边界使用运输替身，检查可选参数、旧默认argv、非零退出传播，以及既有v4 followup使用相同设置。测试不判断Agent语义。
- 原内存语法检查通过，覆盖409个Guru Python文件；`git diff --check`通过。
- 首次原计划 `task.py validate <task>` 返回 `delivery_selection_required`。按实际帮助追加本D1精确 `--delivery c00e79b3-2983-42cf-9c3c-1d1ce34b6b28` 后通过。原输出仍提示三份长规范注入会截断，以及collector源码引用警告；读取时已另行补读所需正文。
- 未改规范、workflow、公共接口或受管副本，没有安装／reapply／upgrade证明。完整多平台Release矩阵、业务生产效果与外部采用未验证。

## 规划外观察（仅事实）

- candidate_ref：`fixture-human-artifacts-entry`
- observed_behavior：material Agent在收尾调用 `.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh`，返回127及文件不存在；其最终答复如实保留该缺口。
- locators：外置 `shared-material/native.jsonl` 第32行工具结果和 `native-final.txt` 末段。
- minimal_reproduction_hint：在该例workspace执行原事件中的同路径命令及其实际Task／Delivery参数。

本次没有为该观察编辑、加测试、自修、定severity／分类或选择route。
