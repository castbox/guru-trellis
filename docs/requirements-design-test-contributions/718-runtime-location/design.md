# #718 design贡献

状态：promoted；固定来源为main `610a810d45bb30173906d55c77709389adf1cf31`，authority=`guru-trellis-rdt`。完整当前定义见[当前单元](../../design/current/runtime-location.md)，固定拟写保留于[proposed](proposed/docs/design/current/runtime-location.md)。拟写内相对链接按其最终target解析。

原RDT owner在实际candidate Check之后，通过final_integration将manifest中的六个目标整合到完整当前单元及必要导航，并逐项读回。仅替代自动pointer作为启动必要前置及只读来源继承Sync前置的组合解释；#219/#231/#556/#566其余有效条件、旧来源与未迁移范围保持。稳定关系由[traceability](traceability.md)定位。

实际工程、安装和Agent观察由Test当前单元单写，保留早期失败、单样本复用及各次覆盖边界。晋升不证明最终Check、完整committed Review、交付或Release；后续结果由原公共Task/Delivery结果和Git/PR事实承接。
