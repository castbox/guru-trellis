# Research: Real native continuation capabilities for #521

- Query: Find supported real-model entry points to prove start, natural same-chat/new-chat, explicit upstream continue caller, and partial-edit automatic/explicit task-free expansion.
- Scope: internal, with local CLI capability probes
- Date: 2026-10-11

## Findings

### Context and boundaries

The injected hook points to business #120, while this dispatch explicitly roots research at Guru #521. This research used the dispatch's isolated checkout and task directory only. Read AGENTS.md, .trellis/workflow.md, task prd/design/implement/task.json, relevant specs and adapters; did not load implement.jsonl/check.jsonl. Installed boundary checker returned status ok immediately before this file write. Other workers' runtime/package changes were not altered. No native model execution, install, fixture creation, Git mutation, binding, commit, push, PR or cleanup was performed.

### Files found and exact evidence

- trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh: source/installed thin CLI wrapper resolving the managed Python runtime and eval runner.
- trellis/skills/guru-team/runtime/eval_runner.py:2130: CLI arguments are --root, --mode source|installed, --skill, --adapter, --case, --run-root, optional --codex-model and grading inputs.
- trellis/skills/guru-team/adapters/eval/native_adapter.py:1029: actual Codex exec argv assembly. All paths currently add --ephemeral. Semantic/qualification runs use --strict-config; ordinary post-owner runs use --ignore-user-config --sandbox workspace-write. No session resume branch exists here.
- trellis/skills/guru-team/adapters/eval/native_adapter.py:1085: Claude noninteractive adapter disables session persistence and restricts allowed tool access to the trace helper.
- trellis/skills/guru-team/adapters/eval/owner_staging.py:250: host constructs selector owner result. At :256-282 host writes completed/partial task-free edits, verifies remaining fixture file unchanged, then constructs semantic owner result.
- trellis/skills/guru-team/adapters/eval/stage0_fixtures.py:524: host chooses task-free typed exit and authors pre-write/AI-review/evolution evidence. This is post-owner transport coverage, not native Agent ownership of edit or expansion judgment.
- trellis/skills/guru-team/packages/guru-execute-task-free-change/evals/evals.json: completed, non-default, location, automatic/explicit expansion and blocked corpus. No semantic_authoring mode or multi-turn caller flow is declared.
- trellis/skills/guru-team/packages/guru-select-workflow-mode/evals/evals.json: selection cases and same-scope retry are independent post-owner cases, not real continuation sessions.
- .agents/skills/trellis-start/SKILL.md: Step 1 exact current-session context; Step 3 no binding invokes workflow initial entry. Upstream-owned.
- .agents/skills/trellis-continue/SKILL.md: Step 1 no binding returns no_current_task and stops its step. Authentic explicit test must show Guru caller consuming this observed upstream outcome and executing its own fresh routing; prompting only a direct owner cannot prove caller behavior.
- trellis/presets/guru-team/scripts/python/verify_native_platform_load.py:245-259: non-OpenCode actual_load is projection_parity. Its passed value is not an actual Codex model session or workflow behavior test.

### Supported invocations and what each proves

Existing source package transport command, for parent execution only once candidate ready:

    trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh --root <source> --mode source --skill guru-execute-task-free-change --adapter codex --case automatic-risk-expansion --run-root <absolute-repo-external-run-root> --json

An installed run uses the installed script with --mode installed and the installed root. run-root must be outside repository/package. Optional --codex-model <available-model> applies only where corpus does not pin model. This proves adapter/model invocation, actual public-wrapper transport and receipt binding; it cannot by itself prove #521 first native write, native semantic expansion, or continuation caller execution because the host stages those results first. Shared adapter is a packaged Python native runtime, not a model, so shared success is not authentic AI evidence.

Existing semantic_authoring and standard_intake flow can exercise their designated owners. Standard Intake flow stops at Readiness ready and is limited to guru-review-change-request. It is not a generic start/continue/task-free multi-chat harness. Do not silently invent a new flow/adapter or change upstream to fill this gap.

Real installed CLI supports direct normal Agent sessions, as verified by local help:

    codex exec --json --sandbox workspace-write --cd <installed-fixture-primary-or-linked-root> --output-last-message <external-evidence>/turn-1-final.txt -
    codex exec resume --json --output-last-message <external-evidence>/turn-2-final.txt <exact-thread-id-from-turn-1> -

Pipe the actual human/request prompt through stdin; capture stdout JSONL and stderr separately outside source. First command must omit --ephemeral so exact-ID resume works. Resume help has no --cd/--sandbox switch; invoke from intended fixture working directory and reread model-observed cwd/topology to prove actual execution location. Avoid --last because concurrent sessions exist. New-chat recovery is a second fresh exec without resume, with an explicit genuine request, target locator and current facts; it must not import a fabricated Task binding or prior owner result. Use requested/configured supported model, not an invented availability claim. Direct CLI session preserves authentic model-generated commands and outputs; external independent transcript review must establish sequence and consumers.

Do not pass --worktree here to bypass the owner being tested: pre-acquiring an execution worktree is fine for a reuse case, while first-acquisition tests must let the Guru owner display and perform only its separately authorized precise acquisition. A CLI-level automatic worktree would prove the CLI feature rather than Guru ownership.

Start: prompt explicitly invokes the installed upstream trellis-start entry and gives bounded work. Natural same-chat: exact-ID resume with ordinary continuation wording. New-chat: fresh exec plus explicit candidate/worktree context and live facts. Explicit continue: invoke installed upstream entry inside the Guru workflow caller; trace must visibly read original upstream Skill, observe no exact Task, return no_current_task, then show caller fresh-check and legal task-free owner. If native host treats upstream stop as whole-turn stop, record unexercised caller dependency rather than patching upstream or claiming static prose success.

Expansion: give the Agent a genuine two-target bounded request; first native edit must be followed by an actual newly observed scope/public-contract impact before the second write. The model must choose automatic reselect_mode -> selector or explicit_choice_required -> original execution owner, preserve first partial diff, and leave remaining target unchanged. Fixture setup may arrange deterministic source facts, but must not pre-write the candidate, preselect the exit, preauthor owner result, or force a semantic pass. Follow-on narrow/intake choice must be real dialogue; no task-free binding/new store and no silently created Task to satisfy continuation.

### Live capabilities and prerequisites

- /opt/homebrew/bin/codex: codex-cli 0.160.1; codex login status reports Logged in using ChatGPT. Supports exec --json, exec resume exact ID and persistent session unless --ephemeral. Actual selected model/provider execution remains untested.
- /Users/wumengye/.local/bin/claude: Claude Code 2.1.220; claude auth status reports loggedIn false. Claude native runs are unavailable until authenticated.
- /Users/wumengye/.local/bin/cursor-agent exists; status reports Not logged in. Do not count it as runnable model capability.
- /opt/homebrew/bin/gh is authenticated; /usr/bin/git is present. Read-only authenticated git ls-remote origin refs/heads/main succeeded with 44a8b9c1f8495e2f811f892f248a1f2693a8bc80. This verifies current origin access only, not write permission or mutation authorization.
- Qualification-only eval identity path pins Codex 0.147.0 (eval_runner.py:290-330); current PATH CLI 0.160.1 does not satisfy that special pin. Do not generalize that pin to ordinary direct native sessions; separately check if invoking qualification cases.
- CLI presence/login is capability evidence, not successful model call. Missing model, sandbox execution, network/provider, install/runtime capability must remain SKIP/blocked, not pass.
- Probe credential status only; never read/copy/emit auth.json, keychain secrets, token-bearing environment or full config. Evidence should contain model commands/results and safe identity, no credential material or persisted authorization.

### Fixture/setup ownership and evidence layers

Parent owns exact fixture/acquisition/install side-effect scope after candidate is ready. Keep ordinary no-Task installed fixture separate from this formally Task-bound #521 checkout; do not clear/rebind current source Task. Use existing preset installer and supported upstream core install with exact source identity. Fixture branch/worktree creation and install are real local mutations, not performed in this research. Parent should determine approved location for generated runtime/eval evidence; no new persistent checkout registry/store.

Capture before/after primary symbolic ref/HEAD, live worktree registration/common-dir, exact current-chat no-Task result, all dirty/untracked fixture contents, candidate diff, remaining-target bytes and model JSONL. Show zero Task creation/activation/binding/lifecycle writes separately from model's final claim. Keep untouched primary/unrelated contents provable through exact snapshots. Same-chat model context and fresh new-chat location recovery are separate observations.

Report four layers separately: objective topology/runtime tests; existing eval wrapper/receipt transport; direct real installed Agent caller/edit/continuation behavior; install/upstream-byte parity. None implies full multi-platform Release matrix or business #120 adoption.

### Related specs and external references

- .trellis/spec/workflow/companion-scripts.md:1083-1216: runner invocation, post_owner versus semantic_authoring, public projection, trace receipts and constrained Intake flow.
- .trellis/spec/workflow/quality-guidelines.md:322-352: normal Agent transcript and eval assertions are separate; fake native and host-prewritten results cannot prove native authoring.
- .trellis/spec/preset/upstream-ownership.md: official platform/runtime ownership.
- task prd.md R521-04, R521-07, R521-09 and T521-03/T521-06/T521-07; design.md caller dependency and no upstream patch; implement.md actual native evidence requirements.
- Current local codex exec --help and codex exec resume --help (0.160.1), codex login status, claude auth status, cursor-agent status were capability references. No web documentation or external native run used.

## Caveats / Not Found

No existing generic real-model same-chat/new-chat/explicit-continue task-free harness was found. Existing eval transport's ephemeral execution and host-owned task-free staging are precise limitations, not production native results. No new adapter, test, upstream patch or severity/route was proposed. Implementation is concurrently changing canonical/dogfood contracts; parent must reread final installed candidate before native runs. Source fixture/eval DTOs and projection parity cannot be reported as #521 continuation success.
