# ADR-024：公共 Delivery authority 与 Guru 语义 owner

状态：`accepted`；来源：#531已独立审查的[贡献](../contributions/531-task-delivery-lifecycle.md)；expected `.86` 晋升至 `.87`。

Task首次Planning与后继resume曾由Task开发status路由，导致首个/后继Delivery不对称，旧clean候选接续与私有事务恢复需要零散阶段关联。

公共Task2/API1/Plan2由上游唯一拥有。Task只有身份、Direct Source、整体scope、交付关系与完成责任；所有Delivery含D1拥有稳定identity、独立Planning及可返工生命周期。Guru每阶段原语义owner完成判断后调用公共转换，薄projection不重建store/状态机。整体scope写作和Clarify审查与Delivery方案Planning分开，Author仍唯一。Check、dirty精确提交、clean同HEAD接续、首次完整Review和Readiness各自独立。

Publish/Merge保留Guru中文Refs-only、CI、expected-head/trailers与私有事务。已经发生的成功由原owner恢复后记录公共事实，历史事实不补造当前门禁。Completion重新判断整个accepted scope及未分配义务，Closure/Finish/Cleanup/Reactivate保持各自职责，无Delivery证据或收尾不造空切片。

不采用Guru私有Delivery模型、原生/Guru竞争gate、Task首次激活分叉、永久双写或人工dirty/重复提交。旧完整安装在公共Plan2与Guru私有转换成套验证前固定原包；正常defer/副本合法性归上游，Guru透传真实binding/session资源。最后直接consumer退出后删除旧reader。当前主148注册根未执行成套切换，不由受控验证推出原业务恢复。

本决定仅替代ADR-022的Task方案Planning与activate/resume片段，以及ADR-015/016里依赖Task开发status的阶段路由；其独立Architecture方法、identity/generation、scope/完成及终态owners保持。constitution无例外、现有GAP状态和软件四轴不变。promotion新diff必须fresh Phase2、TaskCommit与不同reviewer完整BranchReview；本ADR不证明发布、部署或Release矩阵。
