# #589 D7 公开不可变摘要消费 Architecture contribution

状态：`reviewed_promoted`；change_path：`dedicated_refactor_slice`。原 Architecture owner 按 live expected `current-main-0.6.17-guru.95/active` 晋升 `.96`，完整保留 #599 与 `.95` 的有效 authority。constitution、ADR/GAP lifecycle、原 owners 与软件四轴不变；无新 ADR。

TaskId：589-git-object-performance，generation0；Delivery：533a4e7a-9173-47db-b810-f26de5db74f3。首次独立完整 committed Review 范围为 `865f4a9576eabc85cb3b91e74ecd856785095510..f168092b2783d8c09ee416fb850ecaa1c694d65c`。该 Git HEAD 中的 Task-local `architecture-contribution.md` 保留晋升前不可变正文。晋升新增差额仍须 fresh Phase2、TaskCommit 与独立完整 Branch Review。

## 责任与局部收敛

manual recovery/history 原 snapshot→filesystem 摘要路径改为直接调用上游公开 `GitCandidateContent`。上游继续拥有摘要算法、mode/删除/编码/排序与对象读取；Guru 保留候选身份、expected 比较、PR/祖先/cutoff、历史准备及恢复判断。原 `CandidateObjects` 与无生产 consumer 的专属测试退出，其他实际 consumer 使用的共享 reader 保留。

context 仅在一次操作的实际仓库中复用不可变事实。history 准备切换 actual root 前关闭并重建，返回或异常退出时释放。相同 exact OID 的 terminal endpoint 准备与同 root 已重建候选的重复存在性检查收敛，不删除独立输入检查。没有新持久 store、公共 DTO、业务 owner 或摘要双路 fallback。

current source/安装能力诊断与原维护入口目标成套一致，旧稳定发布保留原来源。后继原 tools owner 从 clean source 正式采用；本 slice 的代表 candidate 安装不等于 Task/installed 已升级。

## 证据与剩余

[唯一 Test](../../requirements-design-test-contributions/589-git-object-performance/test.md)拥有定向公开链、读取/hash 消除、耗时和资源观测、历史失败及未验证边界。本贡献不复制样本。正式两目标采用、native/live 受影响链、最终库存与整体 Completion 尚未完成；完整 Release 矩阵与业务采用归其原 owner。知识晋升不证明这些步骤通过。
