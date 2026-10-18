"""Native causal stage judgments, then unchanged installed owner wrappers.

Only facts, public inputs and installed contracts reach Codex. Expected decisions
stay with the host. One installed throwaway is reused; fixture commits are local
test setup. Outputs remain outside the source checkout.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
sys.path.insert(0, str(SKILLS))
from adapters.eval.fixture_io import stage_clean_installed_owner_repo, run_git
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository

OWNERS = {"check": "guru-check-task", "branch": "guru-review-branch",
          "delivery": "guru-review-task-delivery", "completion": "guru-review-task-completion",
          "refresh": "guru-review-task-completion", "reactivation": "guru-review-task-completion",
          "reactivation_pending": "guru-review-task-completion", "closure": "guru-complete-task-closure",
          "second_delivery": "guru-review-task-delivery", "second_completion": "guru-review-task-completion"}
TASK = ".trellis/tasks/causal-eval"
SPEC = ".trellis/spec/workflow/causal-completion-semantics.md"


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def command(repo, argv):
    process = subprocess.run(argv, cwd=repo, text=True, capture_output=True,
                             env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    if process.returncode:
        raise ValueError(json.dumps({"argv": argv, "returncode": process.returncode,
                                     "stdout": process.stdout, "stderr": process.stderr}))
    return json.loads(process.stdout)


def setup(source, output):
    target = source / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
    fixture, _ = stage_clean_installed_owner_repo(output, target, PACKAGE)
    (fixture / ".trellis/guru-team/config.yml").write_text("workspace_mode: current\n")
    task = {
        "id": "causal-eval", "name": "causal-eval", "lifecycle_generation": 0,
        "status": "in_progress", "title": "Causal stage fixture",
        "description": "One bounded factual stage observation",
        "scope": "Current factual record R1", "base_branch": "main",
        "source": {"kind": "issue", "repo_ref": "castbox/guru-trellis",
                   "number": 383, "disposition": "reference_only"},
        "dev_type": None, "package": None, "priority": "P2",
        "createdAt": "2026-10-10", "completedAt": None, "worktree_path": None,
        "commit": None, "pr_url": None, "children": [], "parent": None,
        "relatedFiles": [], "notes": "", "meta": {},
    }
    write(fixture / TASK / "task.json", task)
    for name in ("prd.md", "design.md", "implement.md"):
        (fixture / TASK / name).write_text("# Fixture R1\n\nRead src/production-eval.txt for the current factual scope and candidate.\n")
    (fixture / "src").mkdir()
    (fixture / "src/production-eval.txt").write_text("Original supported failure observations.\n")
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-qm", "fixture baseline")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", run_git(fixture, "rev-parse", "HEAD"))
    run_git(fixture, "remote", "add", "origin", "https://github.com/castbox/guru-trellis.git")
    run_git(fixture, "switch", "-qc", "codex/causal-eval")
    BranchBindingStore(inspect_repository(fixture)).establish(TaskLifecycleKey("causal-eval", 0), "codex/causal-eval")
    return fixture


def public_input(fixture, output, stage):
    installed = fixture / ".trellis/guru-team/skills/packages"
    head = run_git(fixture, "rev-parse", "HEAD")
    if stage == "check":
        return {"profile": "initial_check", "mode": "workflow", "task_ref": TASK,
                "source_exit": "implementation_complete"}
    if stage == "branch":
        return {"profile": "branch_review", "mode": "workflow", "task_ref": TASK,
                "base_ref": "origin/main", "branch_review_commit": head, "review_intent": "initial_review"}
    if stage in ("delivery", "second_delivery"):
        return {"profile": "delivery_review", "mode": "workflow", "task_ref": TASK, "branch_review_commit": head}
    if stage == "refresh":
        value = json.loads((output / "completion.public-input.json").read_text())
        pending = json.loads((output / "C14-completion.wrapper.json").read_text())
        value.update(profile="evidence_refresh", source_exit=pending["exit_id"], reason=pending["reason"])
        value["evidence_slots"]["delivery_publication"] = "publication:current-with-new-production-observation"
        return value
    if stage == "reactivation":
        value = json.loads((output / "reactivation_pending.public-input.json").read_text())
        pending = json.loads((output / "C16-pending.wrapper.json").read_text())
        value.update(profile="evidence_refresh", source_exit=pending["exit_id"], reason=pending["reason"])
        value["evidence_slots"]["validation"] = "validation:current-generation-production-observed"
        return value
    if stage == "closure":
        completion = json.loads((output / "C20-completion.wrapper.json").read_text())["result_ref"]
        value = json.loads((installed / "guru-complete-task-closure/examples/public-input.json").read_text())
        value.update(completion_result=completion, source=json.loads((fixture / TASK / "task.json").read_text())["source"],
                     binding_ref={"task_id": "causal-eval", "lifecycle_generation": 0, "binding_revision": 0},
                     content_head=head, evidence_slots={"completion": completion["result_id"]},
                     action_set=[{"issue_ref": {"repo_ref": "castbox/guru-trellis", "issue_number": 383},
                                  "disposition": "no_close_authority"}])
        return value
    name = "public-reactivation-validation-input.json" if stage == "reactivation_pending" else "public-input.json"
    value = json.loads((installed / "guru-review-task-completion/examples" / name).read_text())
    value["task_artifact"].update(task_id="causal-eval", task_ref=TASK)
    if "merge_result" in value:
        value["merge_result"].update(task_id="causal-eval", task_ref=TASK, reviewed_head=head,
                                     merge_commit_sha=head)
    else:
        value["reactivation_anchor"]["task_id"] = "causal-eval"
        value["reactivation_anchor"].update(archive_ref=".trellis/tasks/archive/2026-10/causal-eval",
                                           archive_head=run_git(fixture, "rev-parse", "HEAD^"))
    if stage == "second_completion":
        ready = json.loads((output / "C21-delivery.wrapper.json").read_text())
        previous = json.loads((output / "completion.public-input.json").read_text())
        observed = json.loads((output / "second-delivery.git.json").read_text())
        value["merge_result"].update(delivery_cycle_ref=ready["delivery_cycle_ref"], pr_number=2,
                                     reviewed_head=ready["reviewed_head"], merge_commit_sha=observed["merge_head"],
                                     result_id="merge:second-local-fixture")
        value["evidence_slots"].update(delivery_review=ready["delivery_cycle_ref"],
                                       delivery_publication="publication:second-local-fixture")
        write(output / "second-delivery.observations.json", {"first_merge": previous["merge_result"],
              "second_review": ready, "second_merge": value["merge_result"],
              "transport_boundary": "Local fixture merge; no remote Publication or business production."})
    return value


def native_batch(fixture, output, stage, rows, batch_name):
    package = fixture / ".trellis/guru-team/skills/packages" / OWNERS[stage]
    model_root = output / ("native-" + batch_name)
    model_root.mkdir()
    for relative in ("SKILL.md", "references/contract.md"):
        if (package / relative).is_file():
            target = model_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(package / relative, target)
    schema_name = {"check": "phase2-check.schema.json", "branch": "review-gate-7.0.schema.json"}.get(stage, "semantic-result.schema.json")
    shutil.copytree(package / "schemas", model_root / "schemas")
    for relative in (SPEC, ".trellis/spec/workflow/quality-guidelines.md",
                     ".trellis/spec/workflow/subtraction-first-compatibility.md",
                     ".trellis/spec/workflow/semantic-retrieval.md"):
        target = model_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fixture / relative, target)
    public = public_input(fixture, output, stage)
    write(output / (batch_name + ".public-input.json"), public)
    metadata = json.loads((fixture / TASK / "task.json").read_text())
    facts = [{"id": row["id"], "facts": row["facts"], "public_input": public,
              "task_source": metadata["source"],
              "git_facts": {"head": run_git(fixture, "rev-parse", "HEAD"),
                            "base_ref": "origin/main",
                            "base_head": run_git(fixture, "rev-parse", "origin/main")}}
             for row in rows]
    if stage in ("second_delivery", "second_completion"):
        transport = json.loads((output / "first-delivery.git.json").read_text())
        if stage == "second_completion":
            transport = {"first_delivery": transport, "second_delivery": json.loads(
                (output / "second-delivery.observations.json").read_text())}
        for record in facts:
            record["transport_facts"] = transport
    write(model_root / "facts.json", facts)
    authoring = {
        "check": "Author exactly mode, reviewed_paths, delivery_policy, validation, docs_ssot, candidate_classifications, semantic_review, typed_exit, route, reason, consumer. Omit recorder-derived fields. reviewed_paths is ['src/production-eval.txt'].",
        "branch": "Author exactly candidate_classifications, semantic_review, verification_evidence, delivery_review. Choose the exit in semantic_review.ai_review_gate.status. Use the actual public branch_review_commit for introduced_head, null fix/closure heads for open findings. reviewer is native-causal-reviewer and review_source is independent-agent.",
    }.get(stage, "Author the complete existing semantic-result schema without adding production DTO fields.")
    prompt = (
        "Execute this installed Skill's current semantic review on each separate factual record. "
        "Read SKILL.md, any references/contract.md, the common causal spec, schemas/" + schema_name + " and facts.json. "
        "For auxiliary quality-guidelines.md, read the applicable Test And Validation Value and "
        "Validation Scope Ownership sections; its historical release/Finalizer/install matrices are "
        "outside this bounded stage experiment. Read other auxiliary policies only where this stage applies. "
        "These are bounded workflow judgment fixtures, not evidence of real business production repair. "
        "Prerequisite normal/solution qualification and current Architecture eligibility are factual fixture inputs; "
        "this experiment tests stage judgment, not re-execution of unrelated prerequisite owners. "
        "Unchanged mechanism qualification remains applicable; independently judge all current evidence. "
        "No expected answers, owner results or semantic decisions have been supplied. Do not inspect outside this directory. "
        "All noncausal entry facts, current base/HEAD and source reference-only relation are available; "
        "the actual stage-specific deficiencies and evidence requirements are in each record. "
        "Path for witnessed candidate behavior is src/production-eval.txt; requirement ref is R1. "
        "Use each record's exact public input identities. " + authoring +
        " Return only a JSON array with one object per input id: id, semantic (your original owner authoring), "
        "assessment (goal: feature|diagnosis|mitigation|repair|protection, dispositions: string array, "
        "close_root_parent: boolean, wait_for_new_evidence: boolean, rationale: concrete judgment). "
        "Assessment is test-only explanation, not a production DTO. The host will execute the original installed "
        "record/check/invoke sequence without altering your semantic judgment. Keep adequate summaries concise."
    )
    argv = ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only",
            "--cd", str(model_root), "--output-last-message", str(output / (batch_name + ".native.json")), "-"]
    try:
        with (output / (batch_name + ".native.log")).open("w") as trace:
            process = subprocess.run(argv, input=prompt, text=True, stdout=trace,
                                     stderr=subprocess.STDOUT, timeout=600)
    except subprocess.TimeoutExpired as error:
        write(output / (batch_name + ".execution.json"), {"argv": argv, "timed_out": True})
        raise ValueError("native execution timed out; partial log retained") from error
    write(output / (batch_name + ".execution.json"), {"argv": argv, "returncode": process.returncode})
    if process.returncode:
        raise ValueError("native execution failed; inspect " + batch_name + ".native.log")
    raw = (output / (batch_name + ".native.json")).read_text().strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    values = json.loads(raw)
    if sorted(row["id"] for row in values) != sorted(row["id"] for row in rows):
        raise ValueError("native case coverage differs")
    return {row["id"]: row for row in values}, public


def wrapper(fixture, output, stage, row, public, semantic):
    package = fixture / ".trellis/guru-team/skills/packages" / OWNERS[stage]
    private = fixture / ".trellis/.runtime/causal-eval"
    input_path, semantic_path = private / "input.json", private / "semantic.json"
    write(input_path, public)
    write(semantic_path, semantic)
    prefix = [str(package / "scripts")]
    if stage == "check":
        receipt = command(fixture, [prefix[0] + "/record-phase2-check.sh", "--root", str(fixture),
                  "--task", TASK, "--input", str(semantic_path)])
        command(fixture, [prefix[0] + "/check-phase2-check.sh", "--root", str(fixture), "--task", TASK])
        actual = command(fixture, [prefix[0] + "/invoke.sh", "--root", str(fixture),
                         "--input", str(input_path), "--owner-result", receipt["artifact_path"]])
    elif stage == "branch":
        exit_id = semantic["semantic_review"]["ai_review_gate"]["status"]
        command(fixture, [prefix[0] + "/review-branch.sh", "--root", str(fixture), "--task", TASK,
                          "--skill-input", str(input_path), "--semantic-review-file", str(semantic_path),
                          "--typed-exit", exit_id])
        command(fixture, [prefix[0] + "/check-review-gate.sh", "--root", str(fixture),
                          "--task", TASK, "--expected-exit", exit_id])
        actual = command(fixture, [prefix[0] + "/invoke.sh", "--root", str(fixture), "--input", str(input_path)])
    else:
        actual = command(fixture, [prefix[0] + "/invoke.sh", "--root", str(fixture),
                                  "--input", str(input_path), "--semantic-result", str(semantic_path)])
    write(output / (row["id"] + ".wrapper.json"), actual)
    return actual


def run(source, output, stages, reuse=False, case_ids=None):
    if not reuse:
        output.mkdir(parents=True, exist_ok=False)
    rows = json.loads((PACKAGE / "tests/causal_cases.json").read_text())
    fixture = output / "owner-repo" if reuse else setup(source, output)
    if not fixture.is_dir():
        raise ValueError("reuse requires the original installed fixture")
    results_path = output / "results.json"
    results = json.loads(results_path.read_text()) if reuse and results_path.exists() else []
    for stage in stages:
        current = [row for row in rows if row["stage"] == stage]
        if case_ids:
            current = [row for row in current if row["id"] in case_ids]
        if not current:
            raise ValueError("unknown stage")
        batch_name = stage + ("-" + "-".join(row["id"] for row in current) if case_ids else "")
        if (output / (batch_name + ".native.json")).exists():
            raise ValueError("retain first execution; choose a new native attempt directory")
        if stage == "second_delivery":
            first = json.loads((output / "completion.public-input.json").read_text())["merge_result"]
            continuation = json.loads((output / "C21-completion.wrapper.json").read_text())
            run_git(fixture, "switch", "main")
            run_git(fixture, "merge", "--ff-only", first["merge_commit_sha"])
            first_head = run_git(fixture, "rev-parse", "HEAD")
            run_git(fixture, "switch", "codex/causal-eval")
            write(output / "first-delivery.git.json", {"merge_result": first,
                  "actual_main_head": first_head, "continuation": continuation,
                  "transport_boundary": "Local fast-forward merge; no remote Publication."})
        # Implementation stages change a real Git candidate; later observations stay evidence.
        observation_path = fixture / (".trellis/.runtime/causal-eval/observations.json"
                                      if stage in ("refresh", "closure", "second_completion", "reactivation_pending", "reactivation")
                                      else "src/production-eval.txt")
        observation_path.parent.mkdir(parents=True, exist_ok=True)
        observation_path.write_text(
            json.dumps([{"id": row["id"], "facts": row["facts"]} for row in current], indent=2) + "\n")
        if stage in ("branch", "delivery", "completion", "second_delivery"):
            if run_git(fixture, "status", "--porcelain", "--", "src/production-eval.txt"):
                run_git(fixture, "add", "src/production-eval.txt")
                run_git(fixture, "commit", "-qm", "current " + stage + " observations")
        if stage == "second_completion":
            reviewed = run_git(fixture, "rev-parse", "HEAD")
            run_git(fixture, "switch", "main")
            run_git(fixture, "merge", "--no-ff", "-m", "second Delivery local fixture", "codex/causal-eval")
            run_git(fixture, "switch", "codex/causal-eval")
            run_git(fixture, "merge", "--ff-only", "main")
            write(output / "second-delivery.git.json", {"reviewed_head": reviewed,
                  "merge_head": run_git(fixture, "rev-parse", "HEAD"), "task_id": "causal-eval", "generation": 0})
        if stage == "reactivation_pending":
            metadata = json.loads((fixture / TASK / "task.json").read_text())
            archive = fixture / ".trellis/tasks/archive/2026-10/causal-eval"
            write(archive / "task.json", {**metadata, "status": "completed"})
            run_git(fixture, "add", str(archive.relative_to(fixture)))
            run_git(fixture, "commit", "-qm", "preceding terminal archive fixture")
            write(fixture / TASK / "task.json", {**metadata, "lifecycle_generation": 1})
            run_git(fixture, "add", TASK)
            run_git(fixture, "commit", "-qm", "reactivated generation fixture")
        judgments, public = native_batch(fixture, output, stage, current, batch_name)
        for row in current:
            judgment = judgments[row["id"]]
            result = {"id": row["id"], "native_stage": stage, "assessment": judgment["assessment"]}
            try:
                actual = wrapper(fixture, output, stage, row, public, judgment["semantic"])
                expected, assessment = row["expected"], judgment["assessment"]
                matched = (actual["exit_id"] == expected["exit"] and assessment["goal"] == expected["goal"]
                           and not assessment["close_root_parent"])
                # Unknown diagnosis/mitigation, production equivalence and truthful layer distinctions.
                if expected["disposition"] in ("diagnosis_incomplete", "mitigation_applied",
                                               "production_effect_unverified", "root_cause_fixed"):
                    matched = matched and expected["disposition"] in assessment["dispositions"]
                if expected["exit"] == "evidence_pending":
                    matched = matched and assessment["wait_for_new_evidence"]
                if expected["disposition"] != "root_cause_fixed":
                    matched = matched and "root_cause_fixed" not in assessment["dispositions"]
                result.update(status="passed" if matched else "failed", wrapper_stdout=actual)
            except (ValueError, KeyError) as error:
                result.update(status="failed", detail=str(error))
            results.append(result)
            write(output / "results.json", results)
            print(json.dumps(result, ensure_ascii=False), flush=True)
        # Passed Check / reentry Branch checkpoints are retained by their production consumers.
        # This fixture ends those isolated checks without claiming Task Commit or branch acceptance.
        checkpoints = fixture / ".trellis/.runtime/guru-team/owner-checkpoints"
        if checkpoints.exists():
            shutil.rmtree(checkpoints)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stage", action="append")
    parser.add_argument("--reuse", action="store_true")
    parser.add_argument("--case", action="append", help="Explicit affected-case re-entry; preserve earlier attempt files first.")
    args = parser.parse_args()
    results = run(args.root.resolve(), args.output.resolve(),
                  args.stage or ["check", "branch", "delivery", "completion", "refresh", "closure",
                                 "second_delivery", "second_completion", "reactivation_pending", "reactivation"], args.reuse, args.case)
    current_results = {row["id"]: row for row in results}
    raise SystemExit(0 if current_results and all(row["status"] == "passed" for row in current_results.values()) else 1)
