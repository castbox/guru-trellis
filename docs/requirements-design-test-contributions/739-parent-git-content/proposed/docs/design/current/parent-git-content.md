# 父仓 Git 内容设计

Identity：RDT-DES-PARENT-GIT-CONTENT；aliases：parent Git、gitlink、submodule。Owner：RDT。Status：proposed。适用来源与晋升：RDT-REQ-PARENT-GIT-CONTENT；Architecture guru-trellis-architecture及parent-git-content领域/ADR拟写；完整candidate Check后由原RDT owner晋升/readback。

D739-01（R739-01）：共享runtime.parent_git读取父index/head entries及父状态投影。worktree忽略child，cached父差异仍保留；stage0 mode/OID/absence与普通worktree bytes分开。shared reviewed_content和Check按父原子entry捕获。删除取父absence，即使child目录仍在；replacement按父新类型。committed-tree算法保持。局部算法及payload归canonical runtime和preset spec/workflow/data-contracts.md单写。

D739-02（R739-01/03）：原TaskCommit snapshot以index_blob/mode表示父gitlink，isolated index写被审OID或删除条目；普通文件保持原staging/hook/exact-tree事务。private delivery-3.0替代旧child字段；旧未执行候选不进入新执行，已有receipt先核原commit恢复。公共Delivery authority仍归上游API，Guru不能排除路径或伪造身份绕过regular-only缺口。

D739-03（R739-02/03）：Check验证真实public Task/Delivery/Planning后精确识别当前task.json，Reconcile同边界保留bytes/index并独占exact tree/parents/message提交。Review/Reconcile及真实快照consumer复用父事实，保留ordinary unstaged/unmerged/stale。canonical合同与受管投影沿原upgrade-tools更新，不热改业务或生成脚本。

当前定义不表示所有上游调用者已具备gitlink能力。父/child边界及权衡由Architecture原单元拥有；本单元消费而不复制其算法。要求：../../requirements/current/parent-git-content.md；测试：../../test/current/parent-git-content.md。
