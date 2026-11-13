# V1–V3 实际执行观察

## 输入与执行设置

事前材料目录：`/var/folders/01/1zvdy3p137q1kg9ncy4sd9wm0000gn/T/guru826-observation-spmqp0v8/host`。`frozen.json`绑定固定B `f16bb562e4ea844939786cebd5c6c20e686914b2` 的方法正文、初始产品与自然请求。`criteria.md`在首次执行前固定五项人工评价维度：真实入口与可用就绪、独立结果及文件副作用、清理后证据、入口变更维护、诚实边界。准则未传给执行Agent。候选方法从实际canonical Test And Validation Value捕获，摘要见`candidate-capture.json`。

用户指定模型后的当前验收观察使用 `codex-cli 0.167.2`，四次命令均显式 `-m auto/gpt-6.1-sol -c model_reasoning_effort="medium"`，共同参数 `exec --ephemeral --json --skip-git-repo-check --sandbox workspace-write -c approval_policy="never"`。实际argv保留于`sol-*-process.json`。模型缓存明确列出该slug支持medium；实际执行没有模型不支持错误，四次JSONL均含`turn.completed`，外层退出码0。未从模型自述推断配置。

## 实际动作与原始结果

两侧均从相同初始CLI源码和README重新建立干净副本；源码SHA与事前冻结值相等，没有继承早先模型产物。CLI依Python标准库，通过真实`doctor/add/show`入口操作独立临时JSON文件。维护前，host仅将`add --text`改为`add --message`，JSON记录字段仍为`text`，README同步同一变化。

| 观察 | 原始记录 | 工具事实 |
| --- | --- | --- |
| 现行初始 | `host/sol-current-initial.jsonl` | 原生执行完成；产物含可复用验证说明，真实add/show及返回JSON内容检查；独立存储文件观察未证，临时状态清理 |
| 现行维护 | `host/sol-current-maintenance.jsonl` | 原生执行完成；更新说明中的新参数并运行完整读写链；host保留初始产物快照 |
| 候选初始 | `host/sol-candidate-initial.jsonl` | 原生执行完成；真实doctor/add/show、独立文件读取、清理后证据读取；产物含运行证据JSONL |
| 候选维护 | `host/sol-candidate-maintenance.jsonl` | 原生执行完成；更新新参数、保留text字段断言并重跑，旧证据保持历史身份 |

两侧初始调查各有一次合并命令因临时项目没有Git元数据返回128；轨迹保留，后续CLI实际调用继续。它不是目标产品失败。四次原生turn没有环境终止；本观察尚不替代独立语义判读。

## 匿名评价与边界

匿名材料目录：`/var/folders/01/1zvdy3p137q1kg9ncy4sd9wm0000gn/T/guru826-inspection-ljc5489x`。含A/B完整初始/维护轨迹、最终输出、初始与维护产物、同请求与冻结准则。评价副本仅规范化路径，原始记录保留；变体映射留在host，不传评价者。独立评价已由 fresh auto/gpt-6.1-sol / medium 完成，完整结果位于中性包 evaluation.md。评价先匿名读取原始轨迹和产物，未接收变体映射。

此前按当时默认 `wesley/gpt-6-astra` / medium 执行的四次运行保留在同host目录，无`sol-`前缀。它们不计用户最新模型要求下的验收。旧候选首次日志模板问题及重跑、旧现行项目内证据覆写均保留原轨迹与host快照，不将其写成Sol运行事实。

本次仅一个去敏CLI项目、每方法初始和维护各一次。不能据此声明普遍质量、性能、token成本、设备或跨平台改善。V4分发与dogfood检查由原owner另行执行。项目路径与临时材料只是当前直接复核consumer载体，不是公共Skill输出或长期账本。

## 匿名评价与原 owner 综合判读

评价者原结论：A/B均实际完成正常CLI读写及参数维护，未见目标行为失败。A独立读取磁盘JSON，保留两轮独立原始证据并限定旧入口适用边界；B实际多覆盖追加、中文/引号/换行，但独立文件观察未证，维护文档替换旧执行块，后续复用保存步骤较弱。完整评价逐项引用item与产物，不能据用例数或exit0判断。

评价完成后原owner读取既有host/blind-mapping.json：A为候选Sol运行，B为现行Sol运行。综合当前任务与原始动作，本次候选在文件副作用独立观察、清理后可读证据、维护保留历史范围三个方面更完整；现行在追加及特殊字符有更多有效覆盖。没有证据说明候选普遍优于现行，也不推断性能/token改善。

V1/AC1和V2/AC2的候选正常CLI旅程、维护及证据回读已被实际轨迹和独立评价支撑；V3/AC3已按同材料、事前标准隔离、真实原生运行与先匿名评价完成。AC4由原始记录与独立判读支撑，非脚本评分。上述只覆盖这一个正常CLI样本，不能推广设备、异常路径或外部项目。

## V4 分发与安装事实

原tools owner返回tools_upgraded，installed_version=0.7.0-guru.8，unverified=[formal_fork_source_lock]。9项内容投影与canonical一致；Sol medium reviewer直接核对quality正文及Author/Review四份投影，manifest9502 skill文件+3 overlay live hash一致。3181项Task/session before/after相等。实际native/drift/installed公开输出在原tools临时目录 native.publicfact.stdout、drift.publicfact.stdout、installed.publicfact.stdout；Sol medium reviewer已直接回读：native status=ok，drift匹配，installed passed/errors=[]、43包/126命令/9502个skill文件和3个overlay文件，三平台无sidecar或conflict。

## 定向分发测试的实际范围

原始unittest输出保留在实施子会话工具记录。组合运行session 30875为Ran 2 tests in 332.262s，FAILED(failures=8)；PlanningBody对应前导成功点且不在失败列表，8项均为Review清单仍包含历史guru-check-task。仅修正现行consumer清单后，Review单项session 92849 exit0：Ran 1 test in 78.698s，OK。不能把首次组合整轮称为通过；不补造外部日志。使用managed Python、root cwd和显式PYTHONPATH/upstream scripts；其local_candidate不同正式Fork锁，保持未验证边界。
