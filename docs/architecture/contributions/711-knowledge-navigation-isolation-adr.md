# ADR-KNOWLEDGE-NAVIGATION-ISOLATION（候选）

状态 proposed；来源#711；前驱ADR-031的完整知识与ADR-KNOWLEDGE-FINAL-INTEGRATION的晋升时机继续适用。本ADR仅在原owner最终晋升后成为适用架构决定。

## 背景与决定

不同知识单元的正常Task在最终晋升时仍向共享根/current README逐项登记，导致独立正文也竞争同一文件。将登记移到下层或生成需提交的manifest不能消除该原因。

根入口保存体系稳定身份、scope/status、真实版本/历史、迁移边界与限定发现方法。日常新增或修改独立主题只维护自身完整单元及真实受影响的关系；不向任何共享文件逐项登记，不追加无关全局版本或合并历史。单元拥有稳定身份/alias、原owner晋升来源、状态与完整定义；目录和检索只定位，不能决定authority。原RDT/Architecture owner及候选/最终质量门禁保持。

## 代价与替代

读取端需限定搜索并核晋升/适用状态及必要关系，单元修改者须同步真实受影响引用。无需外部服务、registry或运行协议。拒绝共享生成索引及强制全部Task串行；它们分别保留共同写入或牺牲正常变化隔离。真实相同能力/关系不拆散复制，仍由原owner比较并整合双方有效条件。

## 兼容、迁移与重审

MIGRATION-711明确旧authority、未迁移范围、切换前置与失败恢复；未达保持原authority，达条件新写停止旧索引登记。旧Task可读原阶段版本，但final integration触及迁移单元须重读真实目标并写当前完整单元。历史快照和原证据不改。根身份/scope/状态/位置/发现合同或真实跨体系关系变化仍由原owner维护入口。

若目录发现无法定位完整适用知识、单元current判定缺来源、引用语义丢失或新的真实共享关系出现，由原owner重审当前边界；不以搜索排序、日期或更大版本替代。验证要求、完整样本及证据限制见本Delivery design第8节；Planning不证明实际行为或采用。


## 完整拟写定位

最终目标是 `docs/architecture/adr/knowledge-navigation-isolation.md`；完整拟写正文位于 [隔离 proposed ADR](./711-knowledge-navigation-isolation-proposed/docs/architecture/adr/knowledge-navigation-isolation.md)。该副本的 accepted 状态描述晋升后的目标，不使当前候选生效。原独立评估、候选 Check 和原 final_integration 仍须实际完成；本候选文件保留 Planning 来源，不代替目标正文或正式结果。
