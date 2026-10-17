# D6 正式工具采用设计

## 固定来源与范围

开发基线main@3676b9e不变。原content_base选择最大已delivered祖先：B=f70b64b026725b27d59fed17ed710cc2f831439f（D5实际head），PR目标main；不默认追赶。D5 PR597 mergeff238f67已实际交付clean canonical来源。本批不改canonical源码，source_locked选择该真实Guru HEAD及Forkc7bd746b42d75f73534c85e263cd6b51fe0e5287/mainCI38994652194的source-built完整CLI/Core0.7.0-castbox.3，pnpm10.32.1。发布包两个Python模板mode与sourcebuild不同，选择source-built roots，不chmod伪造匹配。

## 唯一source-design处置矩阵

|来源及原承诺|处置、落点与影响|
|---|---|
|#589 §5.7/AC13/15、原tools-only source_locked合同|retain：完整clean source执行原preview/prepare/invoke，匹配真实CLI/Core bytes/modes/maintenance1.0；只更新所选checkout工具，不转换Task或跨peer写入|
|原tools owner workflow/custom provider与file decision|retain：canonical workflow内容、template guru-team、ownership custom，provider gh:castbox/guru-trellis/trellis#f70b64b026725b27d59fed17ed710cc2f831439f；真实optional config冲突preserve，required runtime从正式模板更新|
|D5来源准备/原普通apply archive前置|retain：本Task完整工具及Guru投影由原tools-only安装，不重跑普通apply迁移archive、不手工patch；原installer生成receipt，原同operation恢复/rollback保持|
|D5 performance-contract、#589 §6/AC01..11|retain：同373GuruPython、冻结工具/exactpool、14组before与预先门槛；新Fork after分列完整链/writer/ensure/recovery、Git命令/正文与RSS；保留失败，网络及fixture/native/live证明分开|
|#589 AC06公开摘要owner|retain：snapshot残余仍上游；不导入private observation、不复制hash算法或以inode作业务authority；整体Completion仍须其实际交付复验|
|#575完整Release矩阵|retain：本批tools/source/installed/native/定向drift，完整矩阵不承接、不声称通过|

## 原安装路径与保留

只读source_locked preview已通过真实formal Guru/Fork来源与package匹配。本Task实际required更新是common/git_objects.py、task_store.py、delivery_store.py；.trellis/config.yaml为optional用户配置冲突，原公开file_decision采用preserve。原Guru managed相对旧receipt无localdelta，当前source投影需从2a6更新到c7；config.yml用户配置保持。没有新installer映射或当前canonical改动。

原source runtime逐一为本Task checkout和原代表installed生成各自独立tools operation；同一target只prepare一次，actual frozen plan提交AI gate后原invoke执行，失败按原recovery_ref恢复，不分配替代operation。当前声明平台claude/codex/cursor保持，不因本批扩张平台矩阵。原tools owner对真实preimage作preserve/replace，若出现未知变更或sidecar则停在同owner核对，不静默覆盖。

public maintenance单写upstream工具/workflow，原Guru installer单写Guru投影和checkout-local Python pointer。Task/planning/archive/workspace/session、peer工具与common/peer pointer不在write set；前后用原owner及独立bytes核对。源与本Task目标可同checkout，canonical trellis在D5已clean committed且本批不改它。原Task/session/current Delivery保持。

## 验证与交付

每个目标使用自身resolver、installed validator与真实native current/continuation；本Task仍返回同Task/D6及实际next owner。对原代表installed不得为通过而转换/伪造其Task：合法旧Task保持原maintenance_required，current reader与source证明分别报告。原普通apply/reapply在本Task的archive阻塞保留；tools owner的真实重复同operation恢复和目标受管drift/mode/sidecar按原合同验证，benchmark installed由原fixture安装生成。

after执行冻结tools/run_after.py指向新Fork，不改timed函数/样本/输入或门槛。source/installed10档完整链≥5%、100档≥25%；source writer profile wall10≥30%、100≥60%；ensure/recovery≤max(before×1.30,before+.10s)，wrapper64MiB/Git32MiB单进程RSS。对象量按原不同consumer分列，原逐输入检查保留。

本批按实际Check/Commit/fullReview/Publish/Merge验证正式Guru PR链，计数追踪完整原入口但不把网络等待当成本地收益。merge后实际链与D1–D5事实再交整体Completion；原AC06残余未解决前不返回completed。
