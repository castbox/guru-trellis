"""Fact-only task-free fixtures and transport to the existing semantic owner."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

from adapters.eval.fixture_io import public_input_path, run_git

SKILL = "guru-execute-task-free-change"
OWNER_SCHEMA = "schemas/task-free-change-review.schema.json"
QUALIFIERS = ("guru-qualify-normal-scenario", "guru-qualify-solution-mechanism")
ROOT_QUALIFIER = 'guru-qualify-root-cause'
FACTS = ".trellis/task-free-eval/public-authoring-facts.json"
PUBLIC_INPUT = ".trellis/task-free-eval/public-input.json"
PUBLIC_READS = (
    "SKILL.md", "references/contract.md", "interface.json",
    "schemas/task-free-change-review.schema.json", "schemas/public-input.schema.json",
    "schemas/public-selected-route-input.schema.json",
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def observe(repo: Path, argv: list[str]) -> dict:
    """Collect actual process results without classifying their meaning."""
    process = subprocess.run(argv, cwd=repo, capture_output=True, text=True, check=False)
    return {"argv": argv, "returncode": process.returncode,
            "stdout": process.stdout, "stderr": process.stderr}


def stage(request: dict, fixture: Path, package: Path, source_repo: Path) -> None:
    public = json.loads(public_input_path(request).read_text(encoding="utf-8"))
    shared = request["case_id"] == "native-owner-shared-restriction"
    assets = Path(request["workdir"]) / "evals/files/qualification"
    files = {
        "catalog.py": "catalog.py.txt", "test_catalog.py": "test_catalog.py.txt",
        "docs/catalog-contract.md": "contract.md", "docs/display-help.md": "display-help.md",
        "catalog-state.json": "state.json", "qualification.json": "qualification.json",
    }
    if shared:
        files.update({
            "proposal/catalog.py": "candidate-catalog.py.txt",
            "proposal/test_catalog.py": "candidate-test_catalog.py.txt",
            "proposal/design.md": "candidate-design.md",
        })
    for target, source in files.items():
        destination = fixture / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(assets / source, destination)
    # This fixture has no Task or binding. Its actual Git topology supplies the
    # local position facts required by the existing task-free execution owner.
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-qm", "stage catalog authority and task-free operation facts")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", run_git(fixture, "rev-parse", "HEAD"))
    primary = fixture.parent / "task-free-primary"
    fixture.rename(primary)
    run_git(primary, "worktree", "add", "-q", "-b", "task-free-candidate", str(fixture), "HEAD")
    runtime = primary / ".trellis/.runtime"
    if runtime.is_dir():
        shutil.copytree(runtime, fixture / ".trellis/.runtime", dirs_exist_ok=True)
    evidence = fixture / ".trellis/task-free-eval"
    evidence.mkdir(parents=True, exist_ok=True)
    receipts = []
    for implementation in (["catalog.py", "proposal/catalog.py"] if shared else ["catalog.py"]):
        for operation, value in (("rename_display", "Readable title"), ("select_target", "release-2")):
            state = evidence / (implementation.replace("/", "-") + "-" + operation + "-state.json")
            shutil.copy2(fixture / "catalog-state.json", state)
            before = json.loads(state.read_text())
            receipt = observe(fixture, [sys.executable, "-B", implementation,
                "--state", str(state), "--qualification", "qualification.json",
                "--operation", operation, "--value", value])
            receipts.append({"implementation": implementation, "operation": operation,
                "before": before, "after": json.loads(state.read_text()), **receipt})
    write_json(evidence / "operations.json", receipts)
    validation = observe(fixture, [sys.executable, "-B", "-m", "unittest", "-v", "test_catalog"])
    write_json(evidence / "validation.json", validation)
    if shared:
        # A real earlier independent edit in the same bounded continuation.
        # The business target remains untouched for the owner to assess.
        help_path = fixture / "docs/display-help.md"
        help_path.write_text(help_path.read_text() + "\nDisplay titles appear in the catalog list.\n")
        candidate_test = observe(fixture, [sys.executable, "-B", "-m", "unittest", "discover", "-s", "proposal", "-p", "test_catalog.py", "-v"])
        write_json(evidence / "candidate-validation.json", candidate_test)
    write_json(evidence / "local-position.json", {
        "cwd": str(fixture.resolve()), "primary": str(primary.resolve()),
        "branch": run_git(fixture, "branch", "--show-current"),
        "head": run_git(fixture, "rev-parse", "HEAD"),
        "git_common_dir": run_git(fixture, "rev-parse", "--git-common-dir"),
        "worktrees": run_git(fixture, "worktree", "list", "--porcelain"),
        "status": run_git(fixture, "status", "--porcelain"),
        "diff": run_git(fixture, "diff"), "current_task": None,
    })
    write_json(fixture / PUBLIC_INPUT, public)
    reads = [*files, ".trellis/task-free-eval/operations.json",
             ".trellis/task-free-eval/validation.json", ".trellis/task-free-eval/local-position.json"]
    if shared:
        reads.append(".trellis/task-free-eval/candidate-validation.json")
    reads.extend(
        f".trellis/guru-team/skills/packages/{skill}/{relative}"
        for skill in (*QUALIFIERS, ROOT_QUALIFIER) for relative in (
            "SKILL.md", "references/contract.md", "interface.json",
            "schemas/semantic-result.schema.json", "schemas/public-task-free-pre-write-input.schema.json",
            "schemas/public-task-free-evolution-input.schema.json",
        )
    )
    reads.extend(
        f".trellis/guru-team/skills/consumers/workflow/production/{name}-qualification-invocation.schema.json"
        for name in ('normal-scenario', 'solution-mechanism', 'root-cause')
    )
    write_json(fixture / FACTS, {
        "schema_version": "1.0", "public_input_locator": PUBLIC_INPUT,
        "required_reads": reads, "writable_paths": public["target_paths"],
        "qualification_target": {
            "repo_locator": ".", "request_locator": PUBLIC_INPUT,
            "checkout_head": run_git(fixture, "rev-parse", "HEAD"),
            "bounded_paths": public["target_paths"],
        },
        "prior_edited_paths": ["docs/display-help.md"] if shared else [],
        "current_head": run_git(fixture, "rev-parse", "HEAD"),
    })


def context(repository: Path, package: Path, helper_command: str, reads: list[str], input_locator: Path) -> str:
    read = lambda path: f"{helper_command} read --kind owner_file --path {path}"
    return "\n".join([
        "Execute the bounded request using the current task-free Skill and its original semantic gates.",
        "Read every contract and fact locator below before judgment. The fact sheet contains source files and observed process results, not owner conclusions.",
        f"Repository locator: {repository}",
        'This directory is an evidence projection and intentionally has no .git. It is not the execution checkout. The fact-sheet local-position.json was observed in the actual owner checkout. Refresh actual checkout Git facts with the private helper command --skill-id task-free-authoring --command inspect; the host runs read-only Git there and returns its actual process receipts. A missing .git in this evidence projection does not establish a missing owner checkout. Do not run Git in the projection or infer live owner state from it.',
        'For this private test transport, command help lists its syntax. Command write accepts stdin {file_updates:{relative_path:complete_text}} for the bounded targets and applies those exact bytes in the actual checkout. Command run accepts stdin {argv:[explicit executable and arguments]} and returns the actual process output from that checkout. Use write before running the targeted check, then inspect the actual resulting diff. An unsupported command returns its error and leaves the transport available for correction. Original semantic wrapper failures still end the invocation.',
        *[f"{helper_command} read --kind skill_contract --path {package / path}" for path in PUBLIC_READS],
        *[read(repository / path) for path in reads], read(input_locator),
        "Reread live local topology, status and diff before any target write. Use only the selected bounded targets. Do not create a Task, branch, worktree, commit or external side effect.",
        "If the fact sheet lists prior_edited_paths, these are actual earlier writes in this continuation. Inspect their diff and the remaining target files. They do not establish a semantic verdict.",
        "Read each qualifier's original invocation envelope schema in required_reads before calling it. Invoke normal-scenario using helper invoke --stdin --qualifier normal-scenario; invoke solution-mechanism using --qualifier solution-mechanism. Each original qualifier expects {schema_version: '1.0', semantic_result: <your authored semantic result>}, with public_input inside semantic_result. The schema_version value is a JSON string. The task-free {public_input, owner_result} transport envelope is not a qualifier envelope. Use the original task_free_pre_write or task_free_evolution profile selected under the loaded owner contract. qualification_target provides live target facts; candidate refs, decisions and witnesses remain yours. Consume actual qualifier stdout in the task-free owner. Do not write a qualifier result file.",
        'For the original root-cause owner, load its actual Skill/contract, selected input schema, semantic-result schema and shared root-cause-qualification-invocation schema from required_reads. When its original contract applies, invoke it with helper invoke --stdin --qualifier root-cause, using its actual {schema_version:"1.0",semantic_result:<your own result>} envelope. Consume the actual returned disposition. Do not directly execute projected wrappers: the helper forwards each original wrapper to the complete installed owner fixture. No root-cause judgment or result is supplied by host.',
        "Assess the request and candidate under the Skill's current method. Explain your actual judgment in its existing review fields, including applicable source and consumer effects. Apply its existing qualification and evolution routes when required. Do not copy an example owner result.",
        "Perform any suitable bounded edit yourself through command write, then run its actual targeted check through command run and complete the post-write review before authoring a result. Native file edits are allowed only within fact-sheet writable_paths. The final eval-only envelope also accepts file_updates for compatibility, but those deferred writes have no post-write check yet; earlier fixture observations cannot establish checks of changed bytes. This field is not part of public input or owner_result.",
        f"Author your own {{public_input, owner_result}} envelope, with optional file_updates only for actual edits, and invoke {helper_command} invoke --stdin. The helper records your fields unchanged and calls the original recorder, checker and public wrapper. A nonzero wrapper result ends the invocation. The final message must contain only the unchanged public wrapper stdout as one JSON object. Send progress and skill-use announcements before the final message. Do not add Markdown or explanatory text around the JSON.",
    ])


class ObservationCommands:
    """Private bounded writes and actual process observations, without judgment."""

    def __init__(self, repository: Path, receipts_path: Path):
        self.repository = repository
        self.receipts_path = receipts_path
        self.receipts = []

    def record_response(self, payload: dict, result: dict) -> None:
        self.receipts.append({'request': payload, 'response': result})
        write_json(self.receipts_path, self.receipts)

    def forward(self, payload: dict) -> dict:
        command = payload['command']
        if (payload['skill_id'] != 'task-free-authoring' or command not in {'inspect','help','write','run'}
                or payload['arguments'] or (command in {'inspect','help'} and payload.get('stdin'))):
            raise ValueError('Use task-free-authoring inspect/help without stdin, or write/run with JSON stdin.')
        if command == 'write':
            updates = json.loads(payload.get('stdin', ''))['file_updates']
            facts = json.loads((self.repository / FACTS).read_text())
            for relative in updates:
                if relative not in facts['writable_paths']:
                    raise ValueError('task-free authoring write is outside the bounded targets')
            for relative, content in updates.items():
                (self.repository / relative).write_text(content, encoding='utf-8')
            result = {'returncode': 0, 'stdout': json.dumps({'written_paths': list(updates)}) + '\n', 'stderr': ''}
            self.record_response(payload, result)
            return result
        if command == 'run':
            argv = json.loads(payload.get('stdin', ''))['argv']
            if not isinstance(argv, list) or not argv or not all(isinstance(part, str) for part in argv):
                raise ValueError('run requires a nonempty argv array of strings')
            try:
                receipt = observe(self.repository, argv)
            except OSError as error:
                receipt = {'argv': argv, 'returncode': 127, 'stdout': '', 'stderr': str(error)}
            result = {'returncode': 0, 'stdout': json.dumps(receipt) + '\n', 'stderr': ''}
            self.record_response(payload, result)
            return result
        if payload['command'] == 'help':
            result = {'returncode':0, 'stdout':
                'command --skill-id task-free-authoring --command inspect\n'
                'command --skill-id task-free-authoring --command write --stdin\n'
                '  stdin: {"file_updates":{"bounded/relative/path":"complete text"}}\n'
                'command --skill-id task-free-authoring --command run --stdin\n'
                '  stdin: {"argv":["executable","argument"]}\n'
                'Inspect reads Git; write applies bounded bytes; run returns actual process receipts in the owner checkout.\n', 'stderr':''}
            self.record_response(payload, result)
            return result
        receipts = {name: observe(self.repository, ['git', *arguments]) for name, arguments in (
            ('head', ['rev-parse', 'HEAD']), ('branch', ['branch', '--show-current']),
            ('status', ['status', '--porcelain']), ('diff', ['diff']),
            ('worktrees', ['worktree', 'list', '--porcelain']))}
        pointer = self.repository / '.trellis/.runtime/current-task'
        facts = {'cwd': str(self.repository.resolve()), 'git_observations': receipts,
            'task_record_locators': sorted(path.relative_to(self.repository).as_posix()
                for path in self.repository.glob('.trellis/tasks/*/task.json')),
            'current_task_file': pointer.read_text() if pointer.is_file() else None}
        result = {'returncode': 0, 'stdout': json.dumps(facts, ensure_ascii=False) + '\n', 'stderr': ''}
        self.record_response(payload, result)
        return result


def validate_observations(events: list[dict], protocol: dict, request_sha256: str) -> None:
    """Match traced commands to actual host calls; infer no suitability."""
    import hashlib
    from adapters.eval.eval_constants import stdout_digest
    path = Path(protocol['task_free_observation_receipts_path'])
    receipts = json.loads(path.read_text()) if path.is_file() else []
    if len(events) != len(receipts):
        raise ValueError('task-free trace omitted an actual checkout observation')
    for event, receipt in zip(events, receipts):
        request, response = receipt['request'], receipt['response']
        expected = {'kind': 'command', 'skill_id': request['skill_id'], 'command': request['command'],
            'arguments': request['arguments'], 'stdin_sha256': hashlib.sha256(request['stdin'].encode()).hexdigest(),
            'returncode': response['returncode'], 'stdout_sha256': stdout_digest(response['stdout']),
            'stderr_sha256': hashlib.sha256(response['stderr'].encode()).hexdigest(),
            'request_sha256': request_sha256}
        if event != expected or request['skill_id'] != 'task-free-authoring':
            raise ValueError('task-free trace differs from its actual checkout command')


def execute(package: Path, repo: Path, envelope: dict, environment: dict) -> subprocess.CompletedProcess:
    """Apply explicit bounded bytes and transport the AI-authored result unchanged."""
    facts = json.loads((repo / FACTS).read_text())
    updates = envelope.get("file_updates", {})
    for relative, content in updates.items():
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or relative not in facts["writable_paths"]:
            raise ValueError("task-free authoring write is outside the bounded targets")
        (repo / path).write_text(content, encoding="utf-8")
    runtime = repo / ".trellis/.runtime/guru-team/evals"
    public_path, authoring = runtime / "task-free-public-input.json", runtime / "task-free-authoring.json"
    write_json(public_path, envelope["public_input"])
    write_json(authoring, envelope["owner_result"])
    receipts = []
    try:
        for wrapper in ("record-task-free-change.sh", "check-task-free-change.sh", "invoke.sh"):
            argv = [str(package / "scripts" / wrapper), "--input", str(public_path), "--owner-result", str(authoring)]
            result = subprocess.run(argv, cwd=repo, env=environment, capture_output=True, text=True, check=False)
            receipts.append({"argv": argv, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
            if result.returncode:
                return result
        return result
    finally:
        write_json(repo.parent / "task-free-command-receipts.json", receipts)
        authoring.unlink(missing_ok=True)
        public_path.unlink(missing_ok=True)
