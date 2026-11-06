# #713 追踪与晋升边界

| Source | Requirement/behavior | Design/contract | Test |
| --- | --- | --- | --- |
| S1 / AC1/2 | R713-01 / BEH713-CONTRACT | D713-01 / CON713-CONTRACT | T713-01/07 |
| S2 / AC3 | R713-02 / BEH713-EXECUTION | D713-02 / CON713-CANDIDATE | T713-02/03/06 |
| S3 / AC4、缩减 AC6 | R713-03 / BEH713-RECOVERY | D713-03 / CON713-DIAGNOSTIC | T713-03/05/06 |
| S4 / 缩减 AC6/7/8 | R713-04/05 / BEH713-EVIDENCE/DISTRIBUTION | D713-04 / CON713-EVAL | T713-05..08 |
| S5 / AC9 | R713-05 / BEH713-DISTRIBUTION | D713-05 / CON713-ADOPTION | T713-09 |

| 取消的本项验收 | 定义与结果边界 |
| --- | --- |
| C1 / AC5：新增首次正确 preTask→Finish 完整 native 链 | R713-04、D713-04、T713-04；保留原首失败和实际后续结果，不记全链通过 |
| C2 / AC6：新增独立 N3 public-only 恢复链、旧 fixture 接续 | R713-04、D713-04、T713-06；已有 stale/恢复按实际层级采用，原不充分保留 |
| C3 / AC7：F10 与其余非等价 family/profile/caller/goal 追加 native 代表 | R713-05、D713-04/05、T713-07；43/127/180 声明、导航与 consumer 核对保持，未验证行为保留 |
| C4 / AC8：R5 完整方法加载、同 fixture Planning→Activation/resume、Drift 新模型补证 | R713-05、D713-04、T713-08；职责与模块回归保持，方法不足、execution_error、fitness_regression 保留 |
| C5 / AC9：为追加 native 重复环境准备、损坏 clean 恢复与再次安装 | R713-05、D713-05、T713-09；采用仍匹配的已有安装/投影事实，仅刷新真实变更依赖 |

上述取消不撤销生产职责、公开支持域、已知正确性修复或全部最终质量门禁，不形成隐藏 D2 或必需补证支线。原失败、部分成功、污染、未知退出码和当前 H2 终态保留，不清理、续跑或改记 passed。根 PRD 与 D1 PRD 拥有当前要求，D1 design 拥有规范性来源设计处置，implement 拥有 Policy 与 Docs Plan；本表只定位 R/D/T 承接。

三个完整 proposed 单元逐字保留 B 前缀，仅增加本项定义；稳定 identity 不变，shared navigation 无需新版本或逐 Issue 摘要。Completion/Closure/knowledge-maintenance 当前单元无新语义差额，原引用和原责任继续有效。本批不改布局/索引。当前 status=proposed，共享 authority 尚未写入；原 RDT 在候选 Check 之后 final_integration 核 live expected-current、写完整单元并 readback。implementation 重绑实际 after 后进入最终 Check、TaskCommit、完整 committed Review、Delivery Review/readiness、发布/交付及 Completion/Closure/Finish，合并前保留 fresh merge gate。
