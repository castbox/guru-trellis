# 验证仓变更合同

版本：531-validation-change-contract-1。状态：active。
required_concern_set_identity：531-validation-concerns-1。
引用 Architecture Baseline 531-validation-foundation-1 与 DEC-531-OWNER-1、GAP-531-LIVE-1。

## 边界和 owner
本仓只允许远端恢复样本与必要规划/foundation 变化。公共 Task/Delivery 状态的唯一 writer 是安装上游 public store；Guru 仅由对应原语义 owner 调用。Publish/Merge 私有事务分别由原 owner 写入，短生命周期用于同结果恢复；不得记录授权。Markdown 负责语义门禁，脚本只执行和校验。
允许并行读取产品仓和旧样本；禁止修改其工作树、scope、Task、ref 或远端对象。本仓仅专用 base；保持现有行为和 schema2 五 trailers。不存在业务 SDK、DB、API server 或 business provider，相关业务 concerns 不适用，不因此声称安装/Release兼容性通过。

## 项目检查协议
正常 candidate 仅新增验证文本及规划/foundation，不新增本仓运行架构或项目专用可执行检查；project-check descriptor 集为零，当前无另一个本仓 check command。
原 Check、Branch Review、Readiness、Publish、Merge 与 Completion 的现有检查仍须各自执行，不由本合同替代。只要候选扩张到 owner、状态、安装依赖或 provider，原 Architecture owner 必须先重判 applicability，并在必要时引入真实项目 descriptor/result contract；零 descriptor 不免除适用检查。

## ADR 与退出
当前遵循 DEC-531-OWNER-1 不创建 ADR。若改变架构决策、owner/writer 或兼容退出，先由原 Architecture owner 选择必要 contribution/ADR，再经原审查与 promotion，不扩张当前样本。
无法证明恢复时保留 GAP-531-LIVE-1；证据不足回原 owner。历史事实由原 discovery 读取，不补当前 gate。完成后 archive/cleanup 由原 owners 单独处理。
