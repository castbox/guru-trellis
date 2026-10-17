# D6 正式工具采用结果

D5 clean canonical Guru source f70b64b026725b27d59fed17ed710cc2f831439f，Fork c7bd746b42d75f73534c85e263cd6b51fe0e5287/mainCI38994652194；CLI/Core0.7.0-castbox.3、pnpm10.32.1。完整干净Fork正常source build；发布assets checksum通过，Core272文件一致，CLI736文件仅两个Python模板mode差异（发布644/source755、bytes同）。采用source-built roots，未chmod包伪造一致。

原guru-upgrade-tools使用source_locked完整匹配来源，分别操作本Task和原代表installed。custom workflow为canonical guru-team，provider gh:castbox/guru-trellis/trellis#f70b64b026725b27d59fed17ed710cc2f831439f；optional .trellis/config.yaml经原file_decision preserve，Guru config.yml保留。canonical trellis无修改。三个common模块、template hashes与source/extension receipts均由原安装器生成，非手工patch；receipt如实记录Task规划dirty，不混淆canonical来源clean。

|目标|原operation|结果与同operation恢复|受管动作bytes/mode|保留验证|
|---|---|---|---|---|
|当前Task|6eb1ac5d-ce30-4d73-8d89-f71dcb84512c|tools_upgraded，unverified=[]，同ref恢复相同结果|212项零mismatch|Task/workspace/config/planning2516项、common/peer指针305项零变化|
|代表installed|bc407d43-d327-40f7-9db1-6640f9936891|tools_upgraded，unverified=[]，同ref恢复相同结果|102项零mismatch|Task/config7项、common/peer指针1项零变化|

两目标自身resolver/installed validator/continuation通过。本Task native current/Delivery current仍为原Task/gen0/D6 implementing；代表installed当前会话无binding，current exit1正常none、Delivery no_current_task，未造binding。其唯一原bootstrap Task为schema2.0且task.py list识别，不伪造legacy Task或maintenance通过。

source/installed packages、40 active skills/124 commands ownership、Claude/Codex/Cursor drift及执行mode通过；零.new/.bak。代表installed三个.codex/hooks/*.py由原upstream writer固定mode644→755、bytes同，未改hook行为或patch preview；原正常场景qualification判rejected_not_reproduced，未引入修复或新测试。

普通apply的历史archive前置upstream_delivery_migration_required保留，写前零变更。本批通过原tools-only完整投影与同operation重入，不为apply通过迁移历史Task。无新overlay/canonical改动需再apply。实际命令与两目标工程摘要存于本会话原安装工程目录供适用性核对；本文件仅保留Completion需要的长期结果。

工具交付不是正式Guru版本发布，未升级业务仓；完整多平台Release/upgrade矩阵仍由#575负责。after见performance-results.md；本Task真实Check/TaskCommit/fullReview/Publish/Merge沿原owner执行，事实发生后交Completion，不预写成功。AC06上游残余仍阻塞整体，不Closure/Finish。
