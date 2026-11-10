# #775 双向追踪与替代边界

原维护 owner：guru-maintain-requirements-design-test-ssot；authority identity：guru-trellis-rdt。固定适用来源为 Git `313d80215f65777fc70893a90c6d8dce8005d6dd` 的 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`。Architecture authority 为 `docs/architecture/README.md / guru-trellis-architecture / active`。本贡献为 proposed，最终当前性须由原 owner 实际整合给出。

| accepted scope / 观察 | 完整 requirement | 完整 design | 完整 test |
| --- | --- | --- | --- |
| R1 / AC1，范围内规划修复交原 Author | R713-03 / BEH713-RECOVERY 补充 | D713-03 / CON713-DIAGNOSTIC 的路线与薄投影 | T713-03 的实际 stdout→真实 Author 输入 |
| R2 / AC2，同次回退恢复及合法纠正 | R713-03 的原 owner 恢复、真实变化及缺来源边界 | D713-03 的局部绑定、独立恢复前置与原来源转换 | T713-03 的真实回退后恢复/纠正及旧转换 |
| AC3 / 受影响回归与分发 | R713-04/05 原证据层次保留 | D713-04/05 原安装与最终整合职责保留 | T713-03/09 定向回归、matching 及 drift |

只替代 D713-03 中“原非空 scope 引用分支保持”的旧交接规则；原完整6.0消费、11字段authoring、真实需求变化、旧结果、阶段顺序和所有其他职责保持。新的局部绑定由原 Check 恢复直接消费，不增加公共跨层账本。详细接口与 matching 采用由原 package 和 MIGRATION-775 拥有。

三个 proposed-sections 文件分别是原 R713/D713/T713 章节的完整 resulting definition，不是零散插入摘要。候选 Check 同时读取固定来源、完整拟写与真实实现；最终整合替换对应章节，保留同文件其他有效单元，核真实并行差额。本文不记录实现通过、安装、shared-current 晋升、PR 或 Completion 结果。
