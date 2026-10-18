# 正式来源采用验证

本文件是本增量实际结果的唯一长期来源。以下是本地准备工程证明，不是最终 main exact-candidate、远端 provider 或 tag smoke。完整候选的 canonical 变更在隔离 Git source 形成 clean 本地验证提交，保留66d31cd33父提交；没有提前提交正式Task分支。R4增补后的实际验证source包含本轮11个canonical变更文件，逐路径bytes/modes相等。

## T575-SA-01：来源与构建 / AC1–2

生产 `verify_trellis_compatibility_matrix.py validate-source` 实际通过：PR52 merge `7bcbeaad31380e7a29c97898cb947c6120a61775`、tree `c2129a4e600f37b40b08ecec7347fe16a5642d3a`、ordered parents `fda3e12181b72d7aa33cdad54066d33d3386b621` 与 `28fcf4c611d197903b64b818fe9bd4fea7040b3e`，main CI39043542548成功，212 templates。干净Fork正常install/build及成功后marker匹配；该workspace cwd的实际pnpm为10.32.1，不声称host全局pnpm版本。

实际CLI package manifest.main公开入口返回maintenance_api1.0、CLI/Core0.7.0-castbox.4，operation_kinds包含tools_install/task_conversion/legacy_closeout/task_resume。后续source_locked两个原owner均使用该正常workspace匹配Core与dist，未改mode、上游或node_modules。历史tarball与#577 local_candidate证明保持历史归属。

## T575-SA-02：Plan2 包定位 / AC3

`python -B -m unittest discover -s trellis/skills/guru-team/packages/guru-upgrade-installation/tests -p test_delivery_upstream_packages.py -v`：5项通过。真实Node覆盖workspace/pnpm依赖symlink、npm sibling、缺Core、错版本与不可读Core manifest。首次4通过、1失败：MigrationError继承ValueError，缺依赖诊断被同try的manifest catch重新包装。按Node执行、解析结果和manifest读取分段后，同测试全通过；未放宽匹配条件。

现有`test_delivery_upgrade.py`以本次实际Fork CLI和真实`.3` predecessor CLI执行，20项全部通过。它证明相应真实Plan2数据、preview、保留、部分恢复与rollback集成；其preset/native acceptance仍与本节集成分开，不扩称真实业务恢复。

## T575-SA-03：前驱与分发 / AC4

实际从immutable `v0.7.0-guru.3`读取extension manifest和source lock，两者CLI均为0.7.0-castbox.3，Fork为5c760463680ffc10a3f26957b330c57a4b0c3ff8；当前lock仍独立为castbox.4。四份私有release contract逐字节一致，`--before-cli`使用推导的predecessor_cli_version；六输入保持。最终远端existing cell由Stage2执行，这里不以文案/parity冒充该升级证明。

## T575-SA-04：真实 source_locked 采用 / AC2–3/5

原失败现场是66d31cd33发布候选的Plan2只读preview：固定相邻Core路径导致缺失packages/trellis-core/package.json。保持原候选不写，在独立Git副本保留其完整234个历史归档；没有activeTask/common或local session，也不制造指针或Task状态。

新clean验证source经原`guru-upgrade-installation` public preview取得完整inventory；AI按全归档事实选择history_only，生成新的完整Plan2，非复用旧冻结plan。source_locked带计划dry-run无conflicts，原invoke实际返回upgraded、unverified=[]。234归档及artifact共2561文件逐项bytes/modes保持。原public迁移实际产生自己的receipt/checkpoint；未手写回执或绕过旧档案guard。

随后正常三平台preset reapply通过。首次默认PATH Python3.15因锁定依赖安装不可用而失败；显式选择正常Python3.12重跑status=ok。前次失败保留，3.12成功不说明3.15环境问题已修复。

同一代表目标又经原`guru-upgrade-tools`完整preview→prepare→invoke，严格source_locked返回tools_upgraded、unverified=[]。保留用户.trellis/config.yaml。工具原rollback实际返回rolled_back，恢复本次tools操作前的Plan2已采用来源（同为Guru.4），不扩称`.3`版本回退。输入修订保留：首次prepare误用了upstream平台名claude-code，改为现有manifest的Guru CLI flags；source_locked provider改为准确绑定clean验证source commit。均是调用输入修复，未增加产品别名或放宽合同。

目标自身get_context.py的continuation与runtime-contract入口实际成功。因该副本没有activeTask/session，此结果只证明native入口可读。对真实旧archive调用current-only Identity实际为blocked/unsupported_legacy_task；这不是maintenance_required或旧activeTask进入下一owner的证明。这是R4增补前归档样本的边界，不将它提升为旧活动Task证明；T575-SA-06另记录正常predecessor原生创建的真实活动样本。

正式Task工作树另经同clean来源、原tools owner实际source_locked同步必要受管投影，返回tools_upgraded、unverified=[]。2568个Task/local-session文件bytes/modes保持；原owner检查peer/common指针保持，未切换分支或提交正式Task。

## T575-SA-05：工程检查与未验证边界 / AC5–6

source与installed package validators通过；Shared/Codex/Claude/Cursor各source投影校验通过；ownership与三平台dogfood drift通过。首次ownership读取与tools写入并行，读到暂时缺manifest而失败，不作为通过证据；待安装完成后重跑status=ok。末轮git diff --check通过。递归检查发现四个普通Python缓存目录，精确清除这些可重建缓存后，bytecode/.new/.bak残留为零。R4增补前gitleaks曾扫描27个适用变更文件（含Task规划）约4.10MB，无告警；该历史结果不证明新增写集，当前完整写集另执行末轮扫描。

工程证据保存在本机调用期临时目录，不写入public handoff：source-validator、完整Plan2 inventory/plan/preview/output、tools input/prepare/plan/output/rollback、保留对比、native输出和复用driver。正式Task的完整Check、提交、独立Review、Delivery、Completion/Closure/Finish仍由原owners完成。真实业务、生产、累计多平台/native-host、最终main/provider/predecessor cell/tag smoke与软件发布均未由本准备样本证明；#575保持OPEN。

## T575-SA-06：共享 AGENTS 与真实 `.3` 恢复 / AC2/5

保留首次实际失败：正常`.3`工具升级成功后，Core公开AGENTS target与Guru installer合法更新后的live不同，原public rollback返回later_work_conflict。原失败target/checkpoint未修改；只读重叠检查表明唯一不一致为AGENTS，managed block外相同，Guru自己的完成基线与live一致。R4经原需求/机制/Architecture owner重新接受后实施限定修复，不把公开字段可改等同于权限依据。

新等价样本通过原`.3` CLI init、原生task create、原binding和start产生，非伪造Task/session。与首次样本8个原保护文件bytes/modes相同，另将正常新增session/binding纳入12文件基线。新clean工程验证source通过原tools public preview→prepare→invoke实际source_locked返回tools_upgraded/unverified=[]；首次apply前投影AGENTS唯一target与canonical Guru block，之后public target与live相等、block外字节不变，12个原文件保持。没有在回退前恢复Guru block或修改checkpoint。

目标自身get_context --json、task.py current --json、get_context --mode continuation均exit1并实际给出maintenance_required；这是旧活动Task要求独立数据维护的预期诊断。随后公开inspectTaskTarget实际exit0/classification=schema1，原Guru legacy maintenance preview也exit0，确实进入下一只读consumer；未执行数据转换或宣称业务恢复完成。调用期Node探针首次因脚本括号错误未启动，修正探针后取得上述实际inspect，不作为产品缺陷或通过声明。

同一原source/recovery_ref的tools rollback实际返回rolled_back/installed_version=0.7.0-guru.3。回退后目标自身旧get_context和task.py current均exit0，context实际从session解析到原Task；Core恢复0.7.0-castbox.3、Guru恢复0.7.0-guru.3/source commit7d20a930341dae3e7dd2d214660ce3b99e28d863，12个原文件bytes/modes保持，AGENTS完整原bytes/mode恢复。新成功证明不覆盖或修写旧失败样本。

两项新增真实SDK回归通过：实际prepare→投影→public apply→原Guru ensure保持unchanged→public rollback恢复；去掉投影的原正常双writer路径自然复现later_work_conflict。原renderer四项通过。tools package本轮12项中11通过、1项因其独立旧native fixture变量未配置而SKIP；本节真实`.3`样本单独完成，未把SKIP计为通过。原Check还独立重跑SDK2、renderer4、tools recovery4及AST，结果由其原owner消费。

正式Task工作树经新clean验证source的原tools操作同步受管代码/合同/平台投影，tools_upgraded/unverified=[]，2568个Task/local-session文件保持，peer/common指针由原owner检查。第一次原preview因旧本地验证source对象未在repo common objectdb而阻塞；正常从该已知精确clean source获取objects/FETCH_HEAD后继续，未移动branch/ref、未改receipt或回执。新的实际验证source对象同样获取供来源恢复，不宣称远端已发布。

新增范围稳定后，source、installed、Shared/Codex/Claude/Cursor各source projection、ownership、dogfood drift均通过；未重复无变化的旧Plan2全套。当前完整变更集43个适用文件已由gitleaks实际扫描，无告警；git diff --check通过。首次末轮residue发现一个普通.trellis/scripts/common/__pycache__目录及其缓存，保留非空记录，精确清除此可重建目录后再用禁用bytecode的环境复扫为空；没有把首次非空结果写为通过。Test结果更新后再扫描同一完整文件集。最终main远端provider、tag smoke、软件发布和完整多平台/native-host/真实业务仍由原Stage2负责；本节不以本地验证source替代正式Task commit或远端candidate。
