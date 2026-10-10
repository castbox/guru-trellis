# #250 双向 trace

| Requirement / behavior | Design | Test |
| --- | --- | --- |
| R250-01 / BEH250-PROFILE | D250-01/02 | T250-PROFILES, T250-NATIVE |
| R250-02 / BEH250-QUESTION | D250-01/04 | T250-NATIVE |
| R250-03 / BEH250-RETURN | D250-02/03 | T250-PROFILES |
| R250-04 / BEH250-QUALIFY | D250-01/03 | T250-QUALIFIERS |
| R250-05 / BEH250-SOURCE | D250-01/03/04 | T250-RELAY, T250-NATIVE |
| R250-06 / BEH250-RELAY | D250-03/04 | T250-RELAY |
| R250-07 / BEH250-RESUME | D250-02/04 | T250-PROFILES, T250-NATIVE |
| R250-08 / BEH250-ENTRY | D250-04/05 | T250-NATIVE |
| R250-09 / BEH250-DISTRIBUTE | D250-01/05 | T250-DISTRIBUTION |

[requirements](requirements.md)、[design](design.md)、[test](test.md)各拥有本层内容。manifest 绑定 current `.83` 和 Architecture `.82`；未晋升 shared current，后续 promotion diff 重新进入原 gates。
