# ADR-CONDITIONAL-QUALIFICATION：按原 owner 条件加载和调用

状态：current。来源为[Issue #793](https://github.com/castbox/guru-trellis/issues/793)，适用before=`e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`。原 Architecture 维护方从 #793 隔离完整拟写晋升本决定；固定 before 保留前驱含义。

## 决定与窄替代

normal、solution、root继续分别独占场景、authority placement和因果候选准入。每个原包以可单独读取的短reference拥有适用条件；原caller在全文加载前按当前authority、真实行为和材料变化判断是否触发，不能在短条件里复制完整资格verdict。条件触发且无仍适用结论时，显式加载原stable Skill并执行原semantic闭环。

未触发不加载全文、不装配空调用、不产生替代typed exit。root接收当前caller场景/authority-placement判断，并在normal/solution实际触发时消费其真实结果，不强求正确未触发的两次调用。新建或实质改变的诊断、缓解、修复、保护仍进入root；ordinary feature无这些机制时不填incident问卷。

阶段/caller改变不重做同结论，实质authority、机制、条件、支持入口/consumer或因果证据变化刷新受影响判断。丢失必要结论回原owner恢复/重判；新正式invocation仍绑定当前facts，不重放旧envelope。原阶段完整判断、非通过出口和唯一consumer保持，资格不是阶段完成。

本决定窄替代ADR-008及原normal/solution调用方的固定非空候选调用要求、ADR-020和root合同的两上游结果一律前置及相关普遍重跑表述。禁止OS等原语承载业务authority、普通I/O允许、诚实正常路径边界和保护提出方因果责任继续成立。实际条件由各原qualifier reference独占，ADR不另写第二套判据。

## 选择与兼容

拒绝仅删global mandatory：原caller和root前置仍会强制调用。拒绝新统一wrapper、classifier或固定问卷：会复制原owner并增加无必要consumer。采用三个原包短条件及原caller落点，完整判定仍留原Skill，runtime只校确定性facts。

原id/profile/输入/输出/consumer保持。MIGRATION-793要求完整matching provider采用；旧完整安装在切换前保原合同，同Task/key/实际阶段合法恢复。旧适用结论可采用，不新增资格账本、授权存储、skipped exit或兼容双写层。

## 验证与生效

本决定经完整候选 Architecture 与 candidate Check 后，由原 final_integration 写入并读回。实际 V1—V5 观察与首次失败边界见 [唯一 Test](../../requirements-design-test-contributions/793-conditional-qualifiers/test.md)；有界原生观察、确定性验证及 dogfood 同步分别陈述。实际 after 仍须最终 Check、Task Commit 和独立完整 committed Review，阶段结果以各原公共输出为准。源码发布、dogfood 安装、目标业务采用和实际费用效果保持区别。
