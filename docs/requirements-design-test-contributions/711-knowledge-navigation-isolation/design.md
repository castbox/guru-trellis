# #711 设计差额与完整拟写

完整方案为所选 D1 design，唯一来源处置在其第3节；本贡献承接原 RDT owner 的完整候选，不建立第二规划 authority。

D711-01/02 修改 canonical 共同 current-knowledge、原 RDT/Architecture Skill/contract 和 managed RDT spec，稳定入口保目录/身份查找，不再登记所有单元。RDT 仍用原 current/<stable-capability>.md；Architecture 原职责目录由原 Architecture contribution 独立承接。原 public profile、I/O、schema、runtime、workflow bytes 及 quality owner 不变。

D711-03 保同能力/关系的原 owner 语义整合与全量 after 质量链。D711-04/MIGRATION-711 分开 matching 安装与项目切换；先完整 proposed，后原 candidate Check/final integration/readback，implementation 绑定实际 after，再最终 Check/Review。D711-05 复用原 tools owner 安装与 sidecar/mode/drift，不手工同步受管文件。

manifest 中 proposed/<target> 是对应真实目标的完整 after 正文。三层根/current 入口保历史与未迁移区；旧列表 aliases 逐项核对，仅缺失者补原单元的定位元信息，其原正文保持。知识维护三单元拥有新行为/设计/测试，项目 docs usage projection 改为限定目录发现；实际 .trellis/spec 未提前写。源 Git 固定 f75f0f5dd078a0c2c4c9a54ac861383774162806，最终集成仍必须重读真实目标。Architecture baseline-usage/proposed 根/治理归原 Architecture owner，不在本 manifest 冒领。
