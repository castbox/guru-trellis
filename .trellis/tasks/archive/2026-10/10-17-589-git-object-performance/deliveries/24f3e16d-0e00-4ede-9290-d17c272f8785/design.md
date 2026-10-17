# D4 Cleanup 读取设计

## Authority 与范围

已消费本D4实际candidate_assessment baseline_current/no_architecture_impact。baseline current-main-0.6.17-guru.94与constitution-v1不变，无contribution/ADR/promotion义务。原content_base投影选择B=dc57fc6ed5d1229c50520d74a1f6390a52469604（唯一最大已交付祖先D3 reviewed head），开发初始基线仍3676b9ee；PR目标main。

## 唯一来源承接矩阵

| 来源/原承诺 | 处置与落点 | 理由与边界 |
| --- | --- | --- |
| #589 §3.2/§5.1/§8：仍存同范围热点优化 | retain：原Cleanup manual_targets_current，调用期复用同head树与blob | 原10/100公开dry诊断证明重复，不只盘点 |
| #589 §5.3/§5.4：可变刷新、独立检查 | retain：原每次for-each-ref、ledger/binding和逐资源inspect/remove顺序 | for-each-ref同时取得当前OID；每次函数均重新读取，不缓存ref或业务结论 |
| #589 §5.2/§5.6/§5.8：资源、原owner、兼容 | retain：直接使用现有TaskObjectReader，run内context退出释放spool | 原--name-only树路径输出与regex保持，路径规则不改变；内容逐对象读取；错误出口保留 |
| #589 §6–7：before固定标准、正式链回归 | retain：performance-contract/results与source-private复现工具 | preview/实际删除/恢复分列，真实fixture无业务资源删除 |
| #589 §5.7/§8：canonical/dogfood/installed与前置 | retain：原tools-only/apply/reapply与当前清单；上游前置明确未完成 | 不patch上游，不将#575矩阵或正式发布计本批 |

## 直接替换机制

只修改原Cleanup invoke.py。原manual_targets_current接收当前run持有的reader及head→原路径列表字典；初始总检查及每资源删除前检查共享，run退出即清理。原for-each-ref刷新当前本地ref并取得OID；remote仍使用原expected_cleanup_head和原可用性检查。对每实际head首次按原ls-tree -r --name-only枚举，原regex筛选；用reader.prepare批量准备该head当前全部Task路径，再逐路径read_path/JSON/identity/generation验证。相同blob只请求一次，跨不同路径仍独立解释。原树列表读取错误保留原git CommandError，reader原正常缺失/读取失败兼容保持。

原两个archive commit_path_bytes读取有不同事实consumer且数量固定，不机械替换。normal/machine_handoff与删除/receipt/provider合同不变，无新公共API/schema、持久缓存、后台服务或业务authority。退出旧逐资源树/show路径，不增平行实现或legacy适配。

## 验证与Docs

先按同工具同依赖完成source/installed10/100两轮before，再固定performance-contract；之后生产实施。功能在原public wrapper覆盖真实删除、相同输入恢复、不同head/Task阻断、正常缺失/读取错误、相邻调用ref移动；原Cleanup suite兼容。source/installed同条件after，profile分列hotspot/其他校验，volume分列固定archive与Task内容。原tools/apply/reapply、validator、mode/overlay drift/sidecar定向验证，不做完整Release矩阵。
