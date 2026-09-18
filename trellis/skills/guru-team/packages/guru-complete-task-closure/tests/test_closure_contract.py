import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json


PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]


def write_json(path: Path, value: dict) -> Path:
    path.write_text(json.dumps(value))
    return path


def invocation(tmp_path: Path, disposition: str = "exact_source") -> tuple[list[str], dict, Path]:
    source_issue = {"disposition": disposition}
    if disposition == "exact_source":
        source_issue.update({"repo_ref": "castbox/guru-trellis", "number": 436})
    public = {
        "profile": "completion_approved",
        "source_exit": "completed",
        "mode": "standalone",
        "task_ref": ".trellis/tasks/demo",
        "completion_ref": "completion:v1:demo",
        "source_issue": source_issue,
    }
    semantic = {
        "profile": "completion_approved",
        "mode": "standalone",
        "route": {"typed_exit": "close_issue", "reason": "completed"},
    }
    input_path = write_json(tmp_path / "input.json", public)
    semantic_path = write_json(tmp_path / "semantic.json", semantic)
    command = [
        sys.executable,
        str(PACKAGE / "runtime/invoke.py"),
        "--root",
        str(tmp_path),
        "--input",
        str(input_path),
        "--semantic-result",
        str(semantic_path),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    return command, env, semantic_path


def install_fake_gh(tmp_path: Path, terminal_state: str) -> tuple[dict, Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log_path = tmp_path / "gh.log"
    script = bin_dir / "gh"
    script.write_text(
        "#!/usr/bin/env python3\n"
        "import os, pathlib, sys\n"
        "pathlib.Path(os.environ['GH_LOG']).write_text(' '.join(sys.argv[1:]) + '\\n')\n"
        "if 'close' in sys.argv:\n"
        "    raise SystemExit(99)\n"
        f"print({terminal_state!r})\n"
    )
    script.chmod(0o755)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
    env["GH_LOG"] = str(log_path)
    return env, log_path


def test_contract_assets_and_finish_projection():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    validate_json(interface, ROOT / "schemas/skill-interface-1.4.schema.json", "interface")

    for artifact in interface["artifacts"]:
        assert (PACKAGE / artifact["path"]).is_file()
    for schema in interface["schemas"]:
        assert (PACKAGE / schema["path"]).is_file()

    finish = next(item for item in interface["public_contracts"]["consumer_inputs"] if item["id"] == "finish")
    assert finish["contract"]["kind"] == "skill_input_authoring_seed"
    assert finish["contract"]["interface_path"] == "packages/guru-finish-task/interface.json"
    assert finish["contract"]["seed_fields"] == ["source_exit", "task_ref", "closure_exit", "closure_ref"]

    finish_schema = ROOT / "packages/guru-finish-task/schemas/public-input.schema.json"
    authored = json.loads((PACKAGE / "examples/public-finish-authoring.json").read_text())
    for exit_id, example_name in (
        ("no_mutation", "public-output.json"),
        ("closed", "public-closed-output.json"),
    ):
        output = json.loads((PACKAGE / "examples" / example_name).read_text())
        projection = next(item for item in interface["public_contracts"]["projections"] if item["exit_id"] == exit_id)
        projected = dict(authored)
        projected.update({mapping["target"]: output[mapping["source"]] for mapping in projection["mappings"]})
        validate_json(projected, finish_schema, f"finish_projection.{exit_id}")


def test_no_mutation_and_exact_closed_recovery(tmp_path):
    command, env, semantic_path = invocation(tmp_path, disposition="reference_only")
    semantic = {
        "profile": "completion_approved",
        "mode": "standalone",
        "route": {"typed_exit": "no_mutation", "reason": "reference only"},
    }
    write_json(semantic_path, semantic)
    output = json.loads(subprocess.run(command, text=True, capture_output=True, env=env, check=True).stdout)
    assert output["exit_id"] == "no_mutation"
    assert output["closure_exit"] == "no_mutation"

    command, env, _ = invocation(tmp_path)
    facts_path = write_json(
        tmp_path / "facts.json",
        {"issue": {"repo_ref": "castbox/guru-trellis", "number": 436, "state": "CLOSED"}},
    )
    recovered = json.loads(
        subprocess.run(
            command + ["--confirmed-close", "--facts", str(facts_path)],
            text=True,
            capture_output=True,
            env=env,
            check=True,
        ).stdout
    )
    assert recovered["exit_id"] == "closed"
    assert recovered["closure_exit"] == "closed"
    assert recovered["issue_ref"] == "castbox/guru-trellis#436"


@pytest.mark.parametrize(
    ("issue_patch", "field_path"),
    [
        ({"repo_ref": "castbox/other"}, "facts.issue.repo_ref"),
        ({"number": 435}, "facts.issue.number"),
    ],
)
def test_wrong_issue_recovery_facts_fail_closed(tmp_path, issue_patch, field_path):
    command, env, _ = invocation(tmp_path)
    issue = {"repo_ref": "castbox/guru-trellis", "number": 436, "state": "CLOSED"}
    issue.update(issue_patch)
    facts_path = write_json(tmp_path / "facts.json", {"issue": issue})

    result = subprocess.run(
        command + ["--confirmed-close", "--facts", str(facts_path)],
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )

    assert result.returncode == 3
    error = json.loads(result.stderr)
    assert error["code"] == "stale_identity"
    assert error["field_path"] == field_path


def test_stale_open_recovery_fact_rereads_exact_issue_without_reclosing(tmp_path):
    command, _, _ = invocation(tmp_path)
    facts_path = write_json(
        tmp_path / "facts.json",
        {"issue": {"repo_ref": "castbox/guru-trellis", "number": 436, "state": "OPEN"}},
    )
    env, log_path = install_fake_gh(tmp_path, "CLOSED")

    recovered = json.loads(
        subprocess.run(
            command + ["--confirmed-close", "--facts", str(facts_path)],
            text=True,
            capture_output=True,
            env=env,
            check=True,
        ).stdout
    )

    assert recovered["exit_id"] == "closed"
    assert recovered["closure_exit"] == "closed"
    call = log_path.read_text()
    assert call.startswith("issue view 436 --repo castbox/guru-trellis")
    assert "close" not in call
