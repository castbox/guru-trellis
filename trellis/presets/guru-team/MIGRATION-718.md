# #718：共享环境选择与Git只读来源迁移

适用前驱为main `610a810d45bb30173906d55c77709389adf1cf31`。新行为须成套采用本文件所在完整matching workflow/preset/packages/runtime；不单独把新DTO交给旧consumer。原完整旧安装可以固定原合同继续，来源代码、共享环境和目标安装分别验证。这里不改变Task schema2/Delivery API1、软件版本或Release资格。

## 环境owner与公开入口

原 `runtime/bootstrap.py` 独占identity/cache/选择，`resolve-python.sh REPO ASSETS COMMAND...` 保持原ABI。独立 `manage-python.sh REPO ASSETS OPERATION` 使用可用CPython3或cache seed运行当前assets标准库维护，不依赖目标dispatcher。

| 操作 | 精确参数 | 副作用与结果 |
| --- | --- | --- |
| 检查 | `--check --json` | 只读检查实际选择/兼容cache，不装依赖、不迁移hint |
| 日常解析 | `--resolve-active --json` 或原 `--exec-active -- COMMAND...` | 验证当前需求；只缓存成功解析，不安装；最终命令执行当前目标assets |
| 修复 | `--repair --python /path/to/python3 --json` | 原锁定bootstrap/probe/真实wrapper验证后成功切换，失败保护原环境/合法选择 |
| writer位置 | `--print-active-pointer` | 返回当前checkout的selection-v3.json；不表示旧v2 reader位置或当前实际解释器 |

无操作flag仍为原初始化。`--python` 表达显式兼容类别；安装器未收到用户解释器时取当时PATH python3并以 `--automatic-selection` 转交原bootstrap，保存自动模式。显式失效不fallback。原 `--print-identity`、`--resolve-runtime ID`、`--no-activate`、`--checkout-local` 仍保留其对应合同；当前writer始终只写明确目标checkout。

当前格式3.0位于 `.trellis/.runtime/guru-team/python/selection-v3.json`，内容为schema_version、cache_scope=user、selection_mode=automatic|explicit及按工具需求指纹保存的hints。仅explicit包含interpreter_class。类别包含Python implementation/major/minor及OS/architecture/ABI；patch/path不进入环境identity。需求指纹由runtime API/layout、lock及声明Python要求构成。

日常先验证当前需求hint；自动hint不可用时按24位runtime identity字典序验证已有cache，选首个匹配者。显式类别只在自身类别查找，缺少时拒绝并指向repair。有效hint不因PATH或新增cache变化；不同依赖切回复用各自hint。不新增venv复制、时间排序、全局偏好authority或cache GC。

缺seed返回interpreter_unavailable；缺manifest/lock返回runtime_assets_missing，其dependency分别为runtime-manifest/runtime-lock；当前选择无效返回runtime_selection_invalid，显式类别缺cache返回explicit_runtime_unavailable；缺可用环境、损坏或显式失配由原owner给出具体dependency/runtime诊断和恢复。普通调用不因缺cache自动安装，也不回退global site-packages。实际缺口不能以源码环境成功冒充目标恢复。

## v2旧reader与原维护回退

旧local/gitdir/common `active.json` schema2.0原文保持。由于其不记录选择来源，不能推断曾为用户显式意图。仅在新selection-v3.json不存在时，当前owner按原有效位置顺序读取旧来源一次：有效且兼容时保同物理环境，失效时按自动hint查兼容cache。新文件成立后不继续以旧v2覆盖当前选择；新文件存在但无效时拒绝，不能fallback丢失显式约束。需要持久显式类别时使用当前公开--python重表达。

旧完整安装继续按旧reader读取原v2；同位置新canonical与旧installed可以正常共存。当前writer不覆写或双写旧载体，也不把旧pointer升级成第二authority。旧来源支持在该checkout形成当前选择后退出当前读路径；历史旧工具只在其完整固定版本或原rollback窗口内继续消费原v2。

原 `guru-upgrade-tools`、`guru-upgrade-installation` 及其rollback owners同时覆盖目标新旧载体真实preimage和mode。新文件原先不存在则rollback移除，原先存在则恢复原文；公共tools/data兼容先核，再恢复工具与载体。非目标工具/Task/session/用户配置、peer/common选择bytes及其自身入口实际选择保持。共享cache不随位置、branch或Task生命周期删除。原source-loaded维护从明确完整matching来源执行，成功后跑目标自身resolver、installed/native入口。

## Git来源与成套consumer

原Sync public invoke envelope新增 `operation=read|sync`，省略仍为sync。read明确operation与repo。`base_ref`给定时解析该ref或commit；省略时复用原base_branch/config scalar/已有ordered candidates/remote default选择合同，选定ref后固定commit。可选 `base_commit` 断言选择时解析的40位commit。错选或不存在对象按原诊断纠正；read不fetch/ff、不要求所读分支检出或无关checkout干净。

read返回 `baseline_ready`（`guru-stage0-sync-base-output-baseline-ready-1.0`），其transition为2.0，base=`{kind:git_object,source,selected_ref,commit,identity_sha256}`。明确Git对象不是synced；不伪填HEAD/local/remote三个角色。其固定commit不因后续ref前进静默更换。实际sync保持原clean/ff/identity、synced2.0及guru-base-sync-result-1.0。

| 当前生产者/出口 | 当前合同与原consumer |
| --- | --- |
| 五阶段transition | base-current-2.0；context/clarity/wording/readiness-current-3.0，支持明确来源variant |
| Discovery输入 | pre_task4.0/context_request2.0，aggregate4.0；可选candidate_file独立绑定草案真实字节 |
| Discovery结果 | context_ready5.0；Git对象owner4.0分离repository/observation，原同步owner3.0保留原义 |
| Clarify | clear4.0/needs_context3.0；原Delivery非Intake输出保其独立合同 |
| Wording | change_request pass4.0（当前文件public-pass-output-3.0）；原Planning/显式路径pass仍保固定profile |
| Readiness | ready6.0（当前文件public-ready-output-5.0）、review_wording/clarify_requirements3.0 |
| 回程 | refresh_base/refresh_context/retarget_context2.0携handoff_operation=read及固定commit，回原明确读取，不隐式Sync |
| 创建 | CreateIssue只消费与ready目标闭合的reviewed_target；Task创建仍核selected_base_ref/reviewed_base_head及原身份/checkout |

以上仅标示实际选择的当前合同；精确字段由各Interface/schema单写，旧业务DTO字节保留为固定旧安装验证资产，不代表当前来源能交旧consumer。Interface1.8的transition descriptor只作兼容语法扩展，以表达当前versioned path/id，原合法描述仍可验证。

Discovery通过公开 `read-change-context-source --source-transition JSON --path PATH` 读取固定tree，receipt.result含commit/path/blob/content；history preview同样接受 `--source-transition JSON`。AI须真正阅读源正文、先current后history并完成语义gate。候选文件不冒充Git authority；普通草案变化使其下游结果失效。原prepare-task在固定B没有实际runtime consumer，不为历史声明复活退役入口。

## 采用与验证边界

canonical workflow、公共packages、managed specs、registry/manifest与声明平台投影须经原完整安装owner同步。活跃Task/session的工具维护选择原source-loaded guru-upgrade-tools，普通apply仍保current-only数据前置；不绕过旧数据门禁或手抄dogfood。sidecar按原owner处理，再核mode、drift及目标自身入口。

本项要求本仓A1—A8的真实before/after、必要拒绝、原维护/rollback、代表性Agent及至多一个clean样本。实际结果只由[唯一Test](../../../docs/test/current/runtime-location.md)拥有。local_candidate证据不声明formal_fork_source_lock、完整多平台升级/Release矩阵、远端marketplace或业务采用通过；这些边界不代替本项内部义务。
