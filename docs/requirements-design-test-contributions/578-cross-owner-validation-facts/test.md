# #578 验证
状态：implementation evidence，尚未宣称整体Check、committed Review、promotion或Delivery完成。本文件单写实际结果与未验证边界。

## T578-01：新reviewer文档对齐
R578-01/02/05→D578-01/03。fresh generic reviewer先独立读fixture需求、设计、实现、消费者、检查定义，确定A/B完整集合，再核对原执行者日志。唯一增量notes.md描述既有语义，A/B计数1/1→1/1，未运行run A/B；实际查验解释器3.15.0一致，源文件/检查/依赖与初始HEAD无差异。明确采用父会话原结果，不假称本人执行。

## T578-02：变化与新义务
R578-03/05→D578-02/03。同一fixture、同一原始日志，逐次重新判断：
| 场景 | 实跑 | A/B/C计数 |
| --- | --- | --- |
| factor=3，C正式纳入scope | B/C | 1/1/0→1/2/1 |
| 文档新增B负小数舍入义务并承接check_b | B | →1/3/1 |
| B_DECIMALS=0 | B | →1/4/1 |
| check-version新增负整数断言 | B | →1/5/1 |
| Python3.15.0→3.14.8 | A/B/C | →2/6/2 |

所有实际命令由现有local-revision-facts.py run执行，returncode=0，stdout/stderr为空。未受影响事实保留。原日志前两行字节前缀保持，仅追加真实结果。

一次以“声明B来源不可用”构造缺失分支时，reviewer实际仍知道可访问来源，额外执行B→2/7/2；该调用保留但不计缺失来源证明。随后在独立fixture只生成A原始结果，B没有可定位原始来源，另一个fresh reviewer采用A并补B，1/0/0→1/1/0。后一个观察初次批量读取提前显示了日志，不证明严格读取顺序；只计真实缺失来源命令选择，读序正向证明由T578-01承担。不改写失败尝试或原始日志。

## T578-03：身份与当前绑定
R578-02/04/05→D578-01/03。fixture仅精确stage notes.md并提交真实文档对齐，得到ffd6f31880e599b331e108c82b6a5a64de603190，保留其余dirty，A/B/C计数2/7/2→2/7/2。新判断采用日志第8/11/10行，说明原执行来源及适用理由，不copy旧pass/token。
正式当前结果绑定：独立Architecture owner在matching installed root经官方Task2/Delivery API创建真实fixture并正式执行delivery_task_impact_sync(stage=planning, final_plan)，exit0/baseline_current/target_native/reviewed_candidate。TaskId=fixture-578-installed-architecture，DeliveryId=3e997c78-097e-4bb9-80bd-0728b636f9ef；design、贡献与project-check freshness均绑定本fixture真实文件，owner先独立确定集合再作者当前九concern语义结果，无旧pass/token复制。当前安装拒绝旧task级planning3.0 development输入，error=schema_mismatch/exit2；复制Task文档没有建立合法Delivery，本次未放宽schema。正向验证使用官方Task2/Delivery真实对象。

## T578-04：package和安装投影
R578-05→D578-03。
- source package validation通过：40active/124commands/106package tests inventory。
- Architecture contract32/32、BranchReview contract25/25通过；Architecture使用干净本地Trellis b0d87f952043058e21001a002b661bf2db56b1fa完整dist scripts/API1.0，CLI0.7.0-castbox.3。
- Check contract11/12：既有interface包含legacy_controls_retired，测试仍仅列7项；interface/测试本次未改，不标全绿。
- platform inventory9/11：既有mock lambda未接收installer传入python kwarg，2项TypeError；installer/该测试未改。实际完整三平台安装补足本任务投影验证，未修改无关红测。
- native platform load5/5通过；runtime AST对照仅remediation字符串变化，freshness/descriptor/route原逻辑不变；py_compile/diff-check通过。

独立clean source dogfood使用完整官方local CLI init、完整matching preset apply/reapply、installed package validation和dogfood drift。Claude/Codex/Cursor、shared/spec/workflow/runtime投影一致；installed status=passed、124commands、0sidecar/0private test projection；reapply status=ok，new/backups/removals均0；无.new/.bak。
最初继承旧安装的临时试样产生.new/provenance冲突，未冒充成功；正式正向结果来自另一个clean样本。source ownership bootstrap要求源仓extension manifest，补齐源仓完整manifest后由原installer完成安装；不是业务仓手工补manifest或热补丁升级路径。当前开发Task保持原完整安装。

## 可复现入口与证据边界
现有executor位于trellis/skills/guru-team/packages/guru-check-task/evals/files/local-revision-facts.py。stage空临时目录；run A/B产生真实原始结果；新reviewer读当前canonical合同后自行判断，inspect观察计数。后续使用现有change dependency/c/check-version、真实文档/测试修订、环境精度和解释器切换。没有自动semantic classifier、预填owner pass、DTO绿色自证或长期测试ledger。
package验证使用对应tests/test_contract.py；平台使用test_verify_native_platform_load.py。完整安装从官方CLI init后运行原apply.sh --repo .，再原check-dogfood-overlay-drift.sh。当前binding验证由合法Delivery及真实Architecture owner正式invoke承接，不用测试模型替代。
完整多平台Release/Upgrade矩阵、source-lock精确Fork安装、remote marketplace、业务项目采用和生产效果未验证，不扩为普通#578验收。

## 独立Check补充执行
reviewer本人Architecture配置完整API后32/32通过；Branch全suite44项，43通过/1既有skip。Check默认环境54项=33通过/1既有exit断言失败/20缺API环境skip。补齐GURU_UPSTREAM_DELIVERY_SCRIPTS与TRELLIS_DELIVERY_API_COMMON后，suite停在test_delivery_flow.py的test_bounded_continuity_does_not_fabricate_full_review_for_new_candidate，Branch common.py tree_identity调用git cat-file --batch等待超过160秒；该测试、Check runtime及Branch common.py与HEAD逐字相同，本次未触及。只终止本轮测试及其专属child，记录incomplete，不计通过，不调整fixture/timeout。必要验证层由三owner定向合同、AST不变、真实Agent选择、matching合法Delivery公开绑定、installed与drift覆盖；无关历史失败/skip/不完整未隐藏。
