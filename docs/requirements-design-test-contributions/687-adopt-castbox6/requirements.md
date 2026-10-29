# #687 固定 .6 来源采用：需求差额

状态：proposed。来源为 [Issue #687](https://github.com/castbox/guru-trellis/issues/687) 及本 Task 已接受的整体 AC1–AC5；适用完整前驱为 Git `7718d129bcb2055d77c7f43d0e4edca9aee313ea:docs/requirements/current/native-compatibility.md`。本贡献只修改当前来源采用关系，不替代 #630 的三系统脚本要求或原历史观察。

完整拟生效正文由 [proposed Requirements](./proposed/docs/requirements/current/native-compatibility.md) 单写。其中 R630-05 保留 canonical、所有权与分层身份校验；R687-01..03 / BEH687-SOURCE/TOOLS/STOP 承接固定来源、严格 tools-only 与旧 profile 停止。原 R657-03 的生命周期原则保持，未支持 profile 的创建不因此获准。

源锁从 .5 切至 .6 不证明已安装。严格 source_locked、source/build、字节/mode 及维护恢复继续由原公开维护 owner 的完整合同定义；不另造协议。完整累计矩阵、新 Guru 软件 Release、真实业务安装和原 Backend 收尾保持范围外。

设计与测试关系由 [traceability](./traceability.md) 定位。未改变的 R630-01..04/06、旧历史版本和其它 current 单元保持原义。共享 current 尚未写入；实际采用观察只在本贡献 [Test](./test.md) 记录。
