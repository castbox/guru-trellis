# 独立审查的执行条件与正式结果

Identity：guru-review-execution-boundary。状态：拟晋升完整定义，当前不生效。Owner：原Architecture维护方；公共执行方法由原Architecture/Review/Bind packages拥有。

## 责任与顺序

独立review的实际执行者先在最小工程规则下核actual prelude、对象定位与职责所需读写能力，再按原authority-first顺序作语义判断。Task/Delivery和实际design_facts是待审对象，不是实施者先前pass；不预载本Task PRD/验收/实现总结/先前通过或scope defense。其他Task历史authority只保其原范围，不替代当前判断，也不一律表示污染。

能力查询只报告当前对象读取与所需目录的唯一临时create/write/rename/delete事实。它不建立Task/Delivery选择，不写正式session/Task记录，不产生semantic pass、发布资格或未来权限承诺。临时对象用后清理，已有文件保持；失败保实际操作、脱敏位置、异常类别及可取得errno，无法取得不猜测。没有读过证明、能力ledger或授权持久化。

## 最小写集与单写

原Bind/Selection使用Git common-dir/trellis/sessions；正式Review使用原Task的task.json和JSON writer同目录临时项，以及本checkout原owner-checkpoints/<task-dir>/<Delivery>/review-gate.json。必要call-local carrier使用后清理。源码、测试、文档与其他Task不属于reviewer写入职责，固定候选需保持。启动者按实际载体配置必要范围，不以全盘访问替代最小范围判断。

这些写集按原实际职责适用：candidate_assessment有context时保原绑定/选择职责，confirmed no-context保原显式对象路径；branch_review保完整正式写集。final_plan遵从ADR-EXPLICIT-REVIEW-OBJECT，完整显式对象可只读校验，合法已有选择复用；无绑定/选择不恢复、不写选择、不探测上述写能力，即使session目录不可写也不能据此阻塞。不同选择、损坏绑定和真实冲突仍回原owner；例外不扩展到Author/Approval/Activation或其他stage。

目录probe不等于正式写入成功。实际需要绑定/选择的原入口仍由Identity/Ensure/Bind/Selection完成状态校验；原reviewer独立判断，原recorder/checker/invoke顺序记录check与full_review及其真实predecessor。不同合法选择、真实身份/阶段/内容错误由原owner处理，不借环境身份或绕过public API。

## 失败与恢复

原Bind对projection读取、既有session读取、写入及读回保真实分层。稳定official_session_write_failed不专指写权限；最小技术诊断供当次caller定位，不能泄露payload/context/原异常敏感文本。底层官方API已丢失errno时明确未知，不编造故障原因。

同candidate部分结果写入后，原同owner checkpoint承接未完步骤，恢复采用真实已写公共槽只补缺步。checkpoint退休后原public results承接lost stdout。没有完整语义覆盖时必须补真实审查；不得空写pass、重复gate或无因全套工程命令。合规同reviewer优先续审，覆盖丢失或影响无法界定时按原合同补足。

generic/CLI已承担审查职责则直接完成，不递归派发同职责。无反馈核本次原句柄、事件和阻塞/结果缺失，存活不能证明完成；沿原blocked/re-entry，不无变化循环等待/新开。actual prelude不合规时不能假装遗忘恢复独立性，应选择可满足原条件的干净受支持设施。

## 知识与证据边界

完整当前authority与必要关系由current-knowledge发现与读取；根入口不逐Task追记历史。历史按影响追溯，不能用摘要缓存、路径剪枝或父read marker替代实际全文。未迁移业务仓由其原owner按匹配知识采用，Guru修复不直接改业务私有文档。

能力、正式Bind、完整独立Review、恢复与安装/采用各自记录真实观察，任何一项不能替代其他项。平台注入环节或worker无反馈底因未定位时保持未知，不将源码/fixture绿色或后续一次成功写为普遍root_cause_fixed。本单元候选来自Issue929与其隔离贡献，正式生效及证据范围由原maintenance/committed Review确定。
