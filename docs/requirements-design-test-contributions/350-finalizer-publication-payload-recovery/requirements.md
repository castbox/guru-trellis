# #350 Requirements Contribution

`R350-01`: 在合法 base evolution 加单一 provenance metadata tail 的 Finalizer
recovery 中，fresh Publication Review 的 title/body 演进必须作为 existing-PR
metadata convergence 输入处理；旧 rebind predicate 不得将其误判为身份漂移。

`R350-02`: task、repository、base/head branch、close-Issue scope、PR/remote HEAD
与 Git topology 仍须精确成立；title/body mismatch 仅在 exact base evolution 加
单一合法 provenance tail 的组合拓扑中放行，pure base evolution 与 direct tail
继续要求 predecessor Publication payload 精确一致。

`R350-03`: 保持现有 public I/O、typed exit、transaction stage/schema、PR
#337 与 #333 transaction 不变；existing-PR recovery 必须继续复用既有
strict-ancestor、metadata、Ready/Draft、transaction-before-mutation 与 retry
语义。
