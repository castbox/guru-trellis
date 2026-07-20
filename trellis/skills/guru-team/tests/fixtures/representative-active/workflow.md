# Fixture Workflow

<!-- guru-skill-invoke: {"skill":"guru-example-legacy","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-example-legacy","exit":"completed","consumer":{"kind":"workflow","id":"fixture-legacy-next"}} -->
<!-- guru-skill-exit: {"skill":"guru-example-legacy","exit":"blocked","consumer":{"kind":"stop","id":"fixture-legacy-stop"}} -->
<!-- guru-workflow-target: {"id":"fixture-legacy-next"} -->
<!-- guru-stop-target: {"id":"fixture-legacy-stop"} -->

<!-- guru-skill-invoke: {"skill":"guru-example-action","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-example-action","exit":"forwarded","consumer":{"kind":"skill","id":"guru-example-sync"}} -->
<!-- guru-skill-exit: {"skill":"guru-example-action","exit":"repeat","consumer":{"kind":"skill","id":"guru-example-action"}} -->
<!-- guru-skill-exit: {"skill":"guru-example-action","exit":"completed","consumer":{"kind":"workflow","id":"fixture-next"}} -->
<!-- guru-skill-exit: {"skill":"guru-example-action","exit":"blocked","consumer":{"kind":"stop","id":"fixture-stop"}} -->
<!-- guru-workflow-target: {"id":"fixture-next"} -->
<!-- guru-stop-target: {"id":"fixture-stop"} -->

<!-- guru-skill-invoke: {"skill":"guru-example-sync","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-example-sync","exit":"synced","consumer":{"kind":"workflow","id":"fixture-sync-next"}} -->
<!-- guru-workflow-target: {"id":"fixture-sync-next"} -->
