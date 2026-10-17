# D8 实施与验证计划

## 唯一Delivery Policy

policy=full。本批完成D7留下的两目标正式采用和受影响链证据，承接原已交付的AC04/05等事实并最终核对整体全部AC。本批PR仍Refs-only。手动merge后的首次recovery/query2属于真实后merge证据，在其完成前不能整体Completion/Closure/Finish；不能把后merge证据前置成发布循环条件。若实际出现同范围缺口，回原owner处理，不删验收。

## Docs SSOT Plan

strategy=delta_first。D7来源锁和算法说明不重复维护。当前Delivery validation.md及workflow-inventory.md仅拥有工程执行摘要和全步骤盘点；原RDT owner把实际结果收敛到现有#589唯一Test，并判断是否需版本晋升。原Architecture当前.96适用性由独立owner实际判断，不因调用方变化制造新晋升。

## 执行顺序

1. 原Author solution_planning→Wording→同独立Architecture final_plan→八维Approval→Activation。明确B1cee、当前两目标及来源，不写生产工具再补Planning。
2. 从canonical H1cee运行原guru-upgrade-tools：读preview，核对两份config冲突保留与准确平台；prepare各一次。AI审查精确public/Guru/pointer写集后串行invoke，原Task与代表installed各自的同operation恢复和目标native验证不得省略。读取Task/session/archive/workspace/peer/common保持事实。
3. 两目标实际CLI/Core.4/source/receipt/API、脚本可执行mode和原native入口可用；声明平台、workflow/guru投影、drift、适用reapply/sidecar按实际变化定向核验。复用D7已证明的相同production bytes/package行为，不能用源端进程代替target native。保留失败/SKIP和真实mode归一化边界。
4. 核对D1–D7工程事实的源码、依赖与当前consumer适用；完成当前全步骤优化/保留清单、原RDT收敛和Architecture Phase2。完整Check、精确TaskCommit、committed fresh Check及不同reviewer完整B..H Review后，原Delivery Review/Publish中文Refs-only PR。
5. 对已发布但尚未记录Delivery的本批PR，执行实际普通两父手动merge；原Merge owner先完整终态归属/内容/CI review，再以delivery_merged_recovery首次运行新candidate入口，记录historical_success并验证同结果恢复。query2对实际Task全部Delivery执行固定cutoff历史查询，保留真实网络/本地耗时、全部Git计数和读取行为。
6. 收敛最终受影响链/全步骤事实与唯一Test，原Architecture acceptance_finish；原Completion核对全部AC和实际交付。完成后原Closure/Finish/适用Cleanup；未发生步骤不能预写通过。

## 最小可靠验证集

原tools自身target validators和native；两目标平台/mode/受管字节/drift/sidecar/保留检查；当前manual recovery与query2真实GitHub链及同结果恢复。D7的41consumer、16cell/32fresh plain/64资源summary和全部失败按实际适用承接，不无条件重跑；#575完整Release矩阵不执行。任何新问题先正常场景资格，不加攻击/故障注入范围。
