"""Real Architecture candidates and fresh-worker transport; no semantic decisions."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from adapters.eval.eval_constants import ARCHITECTURE_PUBLIC_AUTHORING_FACTS
from adapters.eval.fixture_io import public_input_path, run_git

DELIVERY_CONTEXT = "architecture-delivery-eval"
ARCHITECTURE_PUBLIC_INPUT = ".trellis/tasks/architecture-evidence/public-input.json"


def stage_architecture_facts(request: dict, fixture: Path) -> None:
    fixture = fixture.resolve()
    public = json.loads(public_input_path(request).read_text())
    task = Path(public["task_locator"])
    if task.is_absolute() or ".." in task.parts:
        raise ValueError("Architecture task locator is unsafe")
    if public["profile"].startswith("delivery_"):
        task = stage_delivery_identity(fixture, public).relative_to(fixture)
    case = request["case_id"]
    # These are candidate facts, never pre-authored owner results or pass evidence.
    baseline_source = "def send(payload, protocol='responses', retries=2):\n    if not 0 <= retries <= 8:\n        raise ValueError('retry count out of range')\n    return {'payload': payload, 'protocol': protocol, 'retries': retries}\n"
    candidate_source = baseline_source.replace("{'payload': payload, 'protocol': protocol, 'retries': retries}", "dict(payload=payload, protocol=protocol, retries=retries)")
    design = "transport.send keeps protocol and retry-count parameters. The candidate constructs the returned mapping using dict keyword arguments; explicit retries from 0 to 8 are supported.\n"
    if "business-default" in case:
        candidate_source = (
            "def send(payload, protocol='responses', retries=3, metric_stage=None):\n"
            "    if not 0 <= retries <= 8:\n        raise ValueError('retry count out of range')\n"
            "    stage = metric_stage or ('import_stage1' if protocol == 'chat' else 'import_stage2')\n"
            "    return {'payload': payload, 'protocol': protocol, 'retries': retries, 'metric_stage': stage}\n"
        )
        design = "transport.send gains metric_stage; absent tags use import_stage1 for chat and import_stage2 for responses. Import callers supply a stage; query_summary keeps its existing call.\n"
    if "inherited-business-default" in case:
        baseline_source = baseline_source.replace(
            "return {'payload': payload, 'protocol': protocol, 'retries': retries}",
            "return {'payload': payload, 'protocol': protocol, 'retries': retries, 'metric_stage': 'import_stage1' if protocol == 'chat' else 'import_stage2'}",
        )
        design += "Before this candidate, transport already assigned import_stage1/import_stage2 from protocol. The candidate exposes metric_stage as a new public parameter while retaining that fallback.\n"
    constraint_file = None
    if "constraint-" in case:
        # A task-local endpoint capability is the minimum fact needed for this candidate.
        candidate_source = baseline_source.replace("protocol='responses'", "protocol='wire_v2'")
        design = "The candidate selects wire_v2 as transport.send's default protocol. Existing import and summary callers keep their explicit responses selector. All selectors are forwarded to the registered provider without interpreting business stages.\n"
        constraint_file = str(task / "constraints.md")
        if any(name in case for name in ("constraint-sufficient", "constraint-refresh", "constraint-unchanged")):
            constraint = "# Endpoint capability fact\n\nSource: provider wire-v2 integration specification, revision 1. wire_v2 is a registered technical protocol selector on the same transport/provider integration; it accepts and returns the same payload/response shape as responses. Existing explicit responses and chat callers remain supported. The provider allows either selector as the default; no new storage, state or caller lifecycle is required.\n"
        elif "constraint-refuted" in case:
            constraint = "# Endpoint capability fact\n\nSource: provider wire-v2 integration specification, revision 2. wire_v2 returns an asynchronous job identifier. A separate polling request retrieves the completed response. Existing responses and chat calls return the completed response in the original call. A wire_v2 request therefore needs a different completion lifecycle.\n"
            design += "The accepted design assumes wire_v2 returns the completed response in the original call and therefore retains the existing synchronous caller contract without polling.\n"
        else:
            constraint = "# Endpoint capability fact\n\nSource: integration discovery note. The wire_v2 provider capability and response/lifecycle compatibility specification has not yet been supplied. Its endpoint name alone does not establish compatibility or the meaning of completion.\n"
    if "missing-candidate" in case:
        design = None
        candidate_source = baseline_source
    files = {
        **({} if public["profile"].startswith("delivery_") else {str(task / "task.json"): json.dumps({"id": task.name, "name": task.name, "status": "planning" if public["stage"] == "planning" else "in_progress", "branch": "main", "base_branch": "main"}) + "\n"}),
        public["constitution"]["authority_locator"]: "# Project Constitution\n\nIdentity: constitution-v1. Project rules are read from this current authority. Shared transport owns protocol communication and retry configuration; import semantics belong to import_pipeline. Caller-owned diagnostics must not reject an otherwise legal communication request.\n",
        public["baseline"]["locator"]: "# Project Architecture\n\nIdentity: current-v2. Active. transport.py is shared protocol transport. import_pipeline.py owns import processing; query_summary.py owns summarization. Both call transport.send. Retry configuration supports integers 0 through 8; default and recommended values are not hard invariants. Protocol values chat/responses are technical selectors. legacy_cache.py is a separate existing component.\n",
        public["project_contract"]["change_contract_locator"]: "# Change Contract\n\nIdentity: project-change-contract-v1. Concern set: project-concerns-v1. Examine ownership, state, dependencies, defaults and actual callers. There is no applicable project architecture-check command in this small project; inspect source and callers directly.\n",
        public["requirement_authority"]: "# Transport Requirements\n\nCallers may request protocol chat or responses and any integer retry count from 0 through 8. Query summaries and imports both use Responses. Diagnostic tagging is optional; a missing tag does not invalidate a request.\n",
        public["behavior_authority"]: "# Transport Behavior\n\nTransport sends its payload using the caller's protocol and retry configuration. Import processing and summary generation have separate owners.\n",
        "transport.py": baseline_source,
        "import_pipeline.py": "from transport import send\ndef import_record(record):\n    return send(record, protocol='responses', retries=0)\n",
        "query_summary.py": "from transport import send\ndef summarize(query):\n    return send(query, protocol='responses', retries=6)\n",
        "legacy_cache.py": "# Existing standalone cache debt; neither transport nor its callers depend on it.\nCACHE = {}\n",
    }
    if constraint_file:
        files[constraint_file] = constraint
        files[public["baseline"]["locator"]] += "\nProtocol identifiers are forwarded to the registered provider. Provider capability and response/lifecycle compatibility must be established for a new default selector; no required provider version is inferred from its name.\n"
    if repeated_review(request):
        files['test_transport_selectors.py'] = (
            "import unittest\nfrom transport import send\n"
            "class SelectorTests(unittest.TestCase):\n"
            "    def test_existing_explicit_selectors(self):\n"
            "        for protocol in ('responses', 'chat'):\n"
            "            self.assertEqual(send('x', protocol=protocol)['payload'], 'x')\n"
            "            self.assertEqual(send('x', protocol=protocol)['protocol'], protocol)\n"
        )
    files[public["baseline"]["locator"]] = files[public["baseline"]["locator"]].replace(
        "Identity: current-v2.", f"Identity: {public['baseline']['identity']}.")
    for relative, content in files.items():
        target = fixture / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-qm", "stage transport project authority and actual consumers")
    base = run_git(fixture, "rev-parse", "HEAD")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", base)
    (fixture / "transport.py").write_text(candidate_source)
    candidate_contribution = None
    if "business-default" in case:
        (fixture / "import_pipeline.py").write_text("from transport import send\ndef import_record(record):\n    return send(record, protocol='responses', retries=0, metric_stage='import_stage2')\n")
        (fixture / "test_transport_candidate.py").write_text(
            "import unittest\nfrom transport import send\nfrom import_pipeline import import_record\nfrom query_summary import summarize\n"
            "class TransportCandidateTests(unittest.TestCase):\n"
            "    def test_protocol_defaults_and_optional_tags(self):\n"
            "        self.assertEqual(send('x', protocol='chat')['metric_stage'], 'import_stage1')\n"
            "        self.assertEqual(send('x')['metric_stage'], 'import_stage2')\n"
            "        self.assertEqual(send('x')['retries'], 3)\n"
            "        self.assertEqual(send('x', metric_stage='report')['metric_stage'], 'report')\n"
            "    def test_import_and_unchanged_summary(self):\n"
            "        self.assertEqual(import_record('x')['metric_stage'], 'import_stage2')\n"
            "        self.assertEqual(import_record('x')['retries'], 0)\n"
            "        self.assertEqual(summarize('x')['metric_stage'], 'import_stage2')\n"
            "        self.assertEqual(summarize('x')['retries'], 6)\n"
            "    def test_supported_retry_bounds(self):\n"
            "        for retries in (0, 6, 8):\n"
            "            self.assertEqual(send('x', retries=retries)['retries'], retries)\n"
            "        for retries in (-1, 9):\n"
            "            with self.assertRaises(ValueError): send('x', retries=retries)\n"
        )
        candidate_contribution = "docs/architecture-eval/candidate-contribution.md"
        contribution = fixture / candidate_contribution
        contribution.parent.mkdir(parents=True, exist_ok=True)
        contribution.write_text("# Proposed candidate contribution\n\n" + design + "The proposed retry default is 3; import uses explicit 0 and summary explicit 6. The transport retains its 0..8 validation. The candidate tests assert the protocol-derived defaults, caller results, optional tag forwarding and supported retry bounds.\n")
        argv = [sys.executable, "-B", "-m", "unittest", "-v", "test_transport_candidate"]
        validation = subprocess.run(argv, cwd=fixture, text=True, capture_output=True, check=False)
        (contribution.parent / "candidate-test-result.json").write_text(json.dumps({
            "argv": argv, "returncode": validation.returncode,
            "stdout": validation.stdout, "stderr": validation.stderr,
        }, indent=2) + "\n")
    if design is not None:
        target = fixture / task / "design.md"
        target.write_text("# Candidate Design\n\n" + design)
    if public["stage"] == "branch_review":
        run_git(fixture, "add", ".")
        run_git(fixture, "commit", "-qm", "candidate transport change")
    head = run_git(fixture, "rev-parse", "HEAD")
    evidence = fixture / "docs/architecture-eval"
    evidence.mkdir(parents=True, exist_ok=True)
    diff = run_git(fixture, "diff", base, head) if public["stage"] == "branch_review" else run_git(fixture, "diff", "HEAD")
    (evidence / "candidate.patch").write_text(diff + "\n")
    (evidence / "candidate-inventory.json").write_text(json.dumps({
        "base_ref": "origin/main", "base_head": base, "review_head": head,
        "tracked_diff": "docs/architecture-eval/candidate.patch",
        "untracked_paths": run_git(fixture, "ls-files", "--others", "--exclude-standard").splitlines(),
        "design_locator": str(task / "design.md") if design is not None else None,
    }, indent=2) + "\n")
    (evidence / "before-transport.py.txt").write_text(baseline_source)
    if repeated_review(request):
        argv = [sys.executable, '-B', '-m', 'unittest', '-v', 'test_transport_selectors']
        validation = subprocess.run(argv, cwd=fixture, text=True, capture_output=True, check=False)
        (evidence / 'selector-tests.json').write_text(json.dumps({
            'argv': argv, 'returncode': validation.returncode,
            'stdout': validation.stdout, 'stderr': validation.stderr,
        }, indent=2) + '\n')
    if public["stage"] == "branch_review":
        public["committed_range"] = {"base_ref": "origin/main", "base_head": base, "review_head": head}
    if public.get("planning_purpose") is not None or public.get("schema_version") == "3.0":
        if design is not None:
            public["candidate"] = {"design_locator": str(task / "design.md")}
            current = hashlib.sha256((fixture / task / "design.md").read_bytes()).hexdigest()
        else:
            public["candidate"] = {"design_facts": ["No proposed candidate mechanism was supplied."], "constraint_refs": [public["requirement_authority"]]}
            current = hashlib.sha256(json.dumps(public["candidate"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        public["freshness_identity"] = "sha256:" + current
    if public["stage"] != "planning" and public["profile"] in {"task_impact_sync", "delivery_task_impact_sync"}:
        from runtime.reviewed_content import reviewed_content_identity
        public["schema_version"] = "delivery-3.0" if public["profile"].startswith("delivery_") else "5.0"
        public.pop("planning_purpose", None)
        public["project_contract"]["guru_contract_identity"] = "guru-maintain-architecture-baseline:5.0"
        public["before_authority"] = {"git_revision": base,
            "baseline_locator": public["baseline"]["locator"],
            "constitution_locator": public["constitution"]["authority_locator"],
            "change_contract_locator": public["project_contract"]["change_contract_locator"]}
        public["candidate"] = {"head": head, "content_identity": "sha256:" + reviewed_content_identity(fixture)["sha256"]}
    # The input and its digest facts live outside reviewed content to avoid
    # making a candidate checksum depend on the file that contains that checksum.
    input_target = fixture / ARCHITECTURE_PUBLIC_INPUT
    input_target.parent.mkdir(parents=True, exist_ok=True)
    input_target.write_text(json.dumps(public, ensure_ascii=False, indent=2) + "\n")
    reads = [public["constitution"]["authority_locator"], public["baseline"]["locator"], public["project_contract"]["change_contract_locator"]]
    if design is not None:
        reads.append(str(task / "design.md"))
    if constraint_file:
        reads.append(constraint_file)
    reads.extend(["docs/architecture-eval/candidate.patch", "docs/architecture-eval/candidate-inventory.json", "docs/architecture-eval/before-transport.py.txt", "transport.py", "import_pipeline.py", "query_summary.py", public["requirement_authority"], public["behavior_authority"]])
    if candidate_contribution:
        reads.extend(["test_transport_candidate.py", "docs/architecture-eval/candidate-test-result.json"])
    if repeated_review(request):
        reads.extend(['test_transport_selectors.py', 'docs/architecture-eval/selector-tests.json'])
    (fixture / ARCHITECTURE_PUBLIC_AUTHORING_FACTS).parent.mkdir(parents=True, exist_ok=True)
    (fixture / ARCHITECTURE_PUBLIC_AUTHORING_FACTS).write_text(json.dumps({
        "schema_version": "1.0", "required_reads": reads,
        "public_input_locator": ARCHITECTURE_PUBLIC_INPUT,
        "public_input_sha256": hashlib.sha256(json.dumps(public, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "candidate_inventory": "docs/architecture-eval/candidate-inventory.json",
        **({"candidate_contribution_locator": candidate_contribution} if candidate_contribution else {}),
        **({"followup_locator": "docs/architecture-eval/provider-followup.md"} if repeated_review(request) else {}),
    }, indent=2) + "\n")


def contract_paths(public: dict) -> tuple[str, ...]:
    """Select actual current public contracts without choosing a semantic route."""
    if public.get("schema_version") == "delivery-3.0":
        semantic = "schemas/semantic-result-delivery-3.0.schema.json"
    elif public.get("schema_version") == "5.0":
        semantic = "schemas/semantic-result-5.0.schema.json"
    elif public.get("profile", "").startswith("delivery_"):
        semantic = "schemas/semantic-result-delivery-1.0.schema.json"
    else:
        semantic = "schemas/semantic-result-planning-3.0.schema.json" if public.get("schema_version") == "3.0" else "schemas/semantic-result.schema.json"
    return ("SKILL.md", "references/contract.md", "interface.json", semantic)


def public_contract_reads(package: Path, public: dict | None = None) -> list[Path]:
    """Read the current Interface's input schemas, including local ref closure."""
    from adapters.eval.eval_support import schema_projection_closure
    interface = json.loads((package / "interface.json").read_text())
    inputs = interface["public_contracts"]["input"]
    assets = {Path(path) for path in contract_paths(public or {})}
    assets.add(Path(inputs["aggregate_schema"]["path"]))
    assets.update(Path(row["schema"]["path"]) for row in inputs["profiles"])
    return [package / path for path in sorted(schema_projection_closure(package, assets))]


def stage_delivery_identity(fixture: Path, public: dict, *, scope_content=None, scope_anchor="R1. Architecture eval") -> Path:
    """Create the selected identity through the fixed installed API, never a model."""
    from adapters.eval.delivery_production import installed_task
    from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
    from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
    task = installed_task(fixture, "architecture-eval")
    (task / "prd.md").write_text(scope_content or "# Whole Task\n\n## R1. Architecture eval\nCurrent accepted scope.\n")
    projection = DeliveryProjection(fixture, task.relative_to(fixture).as_posix())
    scope = authority_ref(task / "prd.md", fixture)
    projection.scope(scope)
    import uuid
    key = {"task_id": "current", "lifecycle_generation": 0, "delivery_id": str(uuid.uuid4())}
    projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": key,
                      "owner_role": "creation", "owner_id": projection.declaration()["owners"]["creation"],
                      "scope_ref": {"authority": scope, "anchors": [scope_anchor]}, "profile": "pull_request"})
    BranchBindingStore(inspect_repository(fixture)).establish(
        TaskLifecycleKey("current", 0), run_git(fixture, "branch", "--show-current")
    )
    previous_context = os.environ.get("TRELLIS_CONTEXT_ID")
    os.environ["TRELLIS_CONTEXT_ID"] = previous_context or DELIVERY_CONTEXT
    try:
        projection.select(key)
    finally:
        if previous_context is None:
            os.environ.pop("TRELLIS_CONTEXT_ID", None)
        else:
            os.environ["TRELLIS_CONTEXT_ID"] = previous_context
    record = projection.resolve(key)
    public.update(task_locator=task.relative_to(fixture).as_posix(), delivery_key=key,
                  planning_root=record["planning_root"])
    return projection.planning_directory(key)


def reviewer_context(repository: Path, package: Path, helper_command: str, reads: list[str], input_locator: Path, *, upstream: bool) -> str:
    """Build operational locators only. Outcomes remain entirely reviewer-owned."""
    read = lambda path, kind="owner_file": f"{helper_command} read --kind {kind} --path {path}"
    return "\n".join([
        "You are a fresh independent Architecture reviewer for this repository candidate.",
        "This fresh ephemeral worker has no candidate-author history. Inspect the actual native prelude before proceeding. If it preloads task PRD, acceptance, implementation summaries or pass narratives, stop with the existing blocked/re-entry contract; do not retroactively claim independence.",
        "Load the Architecture Skill and contract below for the reviewer method and current authoring/wrapper contracts. Execute every listed contract read command, including all Interface input-profile schemas and their referenced schemas, before authoring or invoking. This complete public-contract read is an execution prerequisite; the current public input still selects only its own profile. Review source; do not edit product code, promote authority, or read task PRD/implement/acceptance/contribution narratives in the first round.",
        "Finish this independent Architecture assessment through its original formal invocation before reading Task PRD, implement, task.json or acceptance narratives. Completing the initial source reads or forming an internal judgment does not end this invocation boundary. Necessary candidate design explanations remain subject to the original contract.",
        "The trace protocol requires one SKILL.md read as its first event. Execute that listed read once and retain its complete text for this session; do not repeat that helper read during a later review round. Complete the other required reads before the corresponding wrapper invocation.",
        f"Repository locator: {repository}",
        f"Public input locator: {input_locator}",
        *[read(path, "owner_file" if upstream else "skill_contract") for path in public_contract_reads(package, json.loads(input_locator.read_text()))],
        "First read current Constitution, Baseline and project change contract, then actual candidate design/full diff, changed responsibilities/defaults/state/dependencies, unchanged production callers and comparable capabilities/constraints. The ordered evidence locators follow:",
        *[read(repository / path) for path in reads],
        read(input_locator, "owner_file"),
        "Form your independent architecture judgment before checking explanations. Apply task necessity only after establishing actual before/after responsibility and causality; do not suppress an architecture defect for absent functional failure. Do not turn unrelated legacy debt into current work. Legal nondefault configuration remains legal; diagnostics do not invent business rejection.",
        "If the fact sheet provides a candidate contribution locator, inspect it only after forming that independent judgment, to check attribution rather than establish Architecture authority.",
        f"After forming judgment, read the selected exit's output schema and projection declared by Interface using: {helper_command} read --kind " + ("owner_file" if upstream else "skill_contract") + f" --path <absolute-schema-path-under-{package}>. Supply every field required by that selected public output projection in your owner_result; properties optional across the semantic union may still be mandatory on the selected branch. Preserve existing identities and current stage. Do not add fields from other branches.",
        "Existing recorder fact: ai_review_gate.status is blocked only for typed_exit=blocked; all other declared exits, including incomplete/conflict routes, require passed for the completed semantic classification round. This does not assert candidate suitability or completion. Follow the actual selected exit and findings; do not force baseline_current.",
        "Execute applicable checks; missing candidate/constraints or unavailable worker uses existing incomplete/blocked exits. Public-input digest is available in the fact sheet; author your own smallest semantic owner_result and mapped consumer under the schema. Do not copy examples or seek expected outcomes.",
        f"{helper_command} invoke --stdin" + (" --upstream-architecture" if upstream else "") + " <<'GURU_INVOCATION_JSON'\n<your {public_input, owner_result} envelope>\nGURU_INVOCATION_JSON",
        "Invoke the formal wrapper yourself. Return its actual complete single typed-exit JSON, without relabeling or narrative. A nonzero wrapper error ends this invocation; never synthesize a pass.",
    ])


def execute_reviewer(argv: list[str], output_path: Path, context: str, *, cwd: Path, environment: dict) -> subprocess.CompletedProcess:
    """A separate fresh native exec, never resume/fork or inherited task context."""
    command = list(argv)
    if "--ephemeral" not in command or "resume" in command or "fork" in command:
        raise ValueError("Architecture requires a fresh ephemeral native worker")
    command[command.index("--output-last-message") + 1] = str(output_path)
    command[-1] = context
    # The native worker may read this visible artifact in addition to argv.
    # Project the current worker's input before launch; the caller restores the
    # overall owner context only after receiving the actual Architecture output.
    (cwd / "native-context.txt").write_text(context, encoding="utf-8")
    return subprocess.run(command, cwd=cwd, env=environment, input="", text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def validate_phase2_predecessor(process: subprocess.CompletedProcess, output: str, events: list[dict]) -> None:
    """Check the existing upstream receipt and fixed Check entry prerequisite."""
    invokes = [event for event in events if event.get("kind") == "invoke"]
    if (process.returncode or len(invokes) != 1 or invokes[0]["returncode"] != 0
            or invokes[0]["stdout_sha256"] != hashlib.sha256(output.encode()).hexdigest()):
        raise ValueError("fresh Architecture worker did not return its actual wrapper output")
    if json.loads(output).get("exit_id") != "baseline_current":
        raise ValueError("Phase2 Check requires actual upstream Architecture baseline_current; retain the upstream result for its existing consumer")


def validate_reviewer_reads(events: list[dict], repository: Path, reads: list[str], *, phase2: bool) -> None:
    """Check observed ordering/coverage only, never judge architecture suitability."""
    first_invoke = next((index for index, event in enumerate(events) if event.get("kind") == "invoke"), len(events))
    observed = [event["path"] for event in events[:first_invoke] if event.get("kind") == "read"]
    required = [str(repository / path) for path in reads]
    if not all(path in observed for path in required):
        raise ValueError("independent reviewer omitted candidate or consumer reads before Architecture invocation")
    if len(required) < 3 or not observed.index(required[0]) < observed.index(required[1]) < observed.index(required[2]):
        raise ValueError("independent reviewer must read Constitution, Baseline and project change contract in authority order")
    if any(observed.index(path) < observed.index(required[2]) for path in required[3:]):
        raise ValueError("independent reviewer must read authority before candidate and consumers")
    if phase2 and any(Path(path).name in {"prd.md", "implement.md", "task.json"} for path in observed):
        raise ValueError("independent reviewer read task narrative before Architecture invocation")


def repeated_review(request: dict) -> bool:
    return request.get("case_id") in {"planning-constraint-refresh-native", "planning-constraint-unchanged-native"}


def stage_followup(request: dict, repository: Path, projection: Path, private_root: Path):
    """Reveal original provider evidence only after the first actual owner call."""
    if not repeated_review(request):
        return None
    changed = request['case_id'] == 'planning-constraint-refresh-native'
    content = ('# Provider integration observation, revision 2\n\n'
        + ('wire_v2 returns an asynchronous job identifier. Completed output requires a later polling call. '
           'responses and chat still return completed output in their original call.\n' if changed else
           'wire_v2, responses and chat still return completed output in their original call with the same payload and response shape. '
           'No provider lifecycle or supported caller behavior has changed.\n'))
    calls = []
    def reveal(process):
        calls.append({'returncode':process.returncode,'stdout':process.stdout,'stderr':process.stderr})
        private_root.mkdir(parents=True, exist_ok=True)
        (private_root / 'review-rounds.json').write_text(json.dumps(calls, indent=2) + '\n')
        if len(calls) != 1 or process.returncode:
            return
        relative = 'docs/architecture-eval/provider-followup.md'
        for root in (repository, projection):
            (root / relative).write_text(content)
    reveal.calls = calls
    return reveal


def validate_followup_reads(events: list[dict], repository: Path) -> None:
    invokes = [index for index,event in enumerate(events) if event.get('kind') == 'invoke']
    later = str(repository / 'docs/architecture-eval/provider-followup.md')
    reads = [index for index,event in enumerate(events) if event.get('kind') == 'read' and event.get('path') == later]
    if len(invokes) != 2 or not reads or not all(invokes[0] < index < invokes[1] for index in reads):
        raise ValueError('same-reviewer followup must read newly arrived evidence between the actual wrapper calls')
