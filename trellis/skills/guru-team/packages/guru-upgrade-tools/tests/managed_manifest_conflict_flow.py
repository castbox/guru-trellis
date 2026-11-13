"""Build a real manifest-conflict fixture, then verify its owner-led resolution.

The default action stops at the actual Git conflict. An Agent reads the current
Reconcile/tools contracts and performs the original preview/prepare/invoke flow.
``--verify`` observes the final installation and resolved merge; it supplies no
semantic decision. All repositories and retained command output stay below the
explicit external --output directory. No remote operation is performed.

Task/Planning setup is pre-boundary fixture state. It does not prove Planning,
independent Review, live PR behavior, or formal source-locked adoption.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


MANIFEST = ".trellis/guru-team/extension.json"
CHANGES = {
    "guru-reconcile-task-base": "The fixture retains the exact prior task HEAD.\n",
    "guru-upgrade-tools": "The fixture retains the original frozen tools plan.\n",
}


def snapshot(directory: Path) -> dict:
    return {
        p.relative_to(directory).as_posix(): [p.stat().st_mode & 0o777,
                                             hashlib.sha256(p.read_bytes()).hexdigest()]
        for p in directory.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(directory).parts
        and "__pycache__" not in p.parts
    }


class Flow:
    def __init__(self, source: Path, fork: Path, output: Path):
        self.source, self.fork, self.output = source, fork, output
        self.repo = output / "repo"
        self.env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
                    "TRELLIS_CONTEXT_ID": "codex_manifest_fixture815"}
        self.sequence = len(list(output.glob("command-*.json")))

    def run(self, argv, *, cwd=None, expected=0):
        result = subprocess.run(list(map(str, argv)), cwd=cwd or self.repo,
                                env=self.env, capture_output=True, text=True)
        (self.output / f"command-{self.sequence:03d}.json").write_text(json.dumps({
            "argv": list(map(str, argv)), "returncode": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}, indent=2) + "\n")
        self.sequence += 1
        if expected is not None and result.returncode != expected:
            raise RuntimeError(f"Command failed ({result.returncode}): {argv}\n"
                               + result.stderr[-1500:] + result.stdout[-1500:])
        return result

    def git(self, *args):
        return self.run(["git", *args]).stdout.strip()

    def install(self):
        argv = ["bash", self.repo / "trellis/presets/guru-team/scripts/bash/apply.sh",
                "--repo", self.repo, "--platform", "claude", "--platform", "codex",
                "--platform", "cursor", "--json"]
        result = self.run(argv, expected=None)
        value = json.loads(result.stdout)
        if result.returncode:
            # Initial branch generation uses the installer's ordinary known
            # upgrade backup path. Resolve only its declared exact old bytes,
            # then let the original installer regenerate its own final result.
            manifest = json.loads((self.repo / MANIFEST).read_text())
            sidecars = []
            for domain in ("skill_packages", "overlays"):
                part = manifest.get(domain, {})
                if part.get("conflicts"):
                    raise RuntimeError(f"Unexpected fixture install conflict: {part['conflicts']}")
                sidecars.extend(part.get("sidecars", []))
            if not sidecars:
                raise RuntimeError(f"Installer failed before a known backup result: {value}")
            for relative in sidecars:
                path = self.repo / relative
                if not relative.endswith(".bak") or not path.is_file():
                    raise RuntimeError(f"Unexpected sidecar in fixture: {relative}")
                original = self.run(["git", "show", f"HEAD:{relative[:-4]}"]).stdout.encode()
                if path.read_bytes() != original:
                    raise RuntimeError(f"Backup differs from actual old fixture bytes: {relative}")
                path.unlink()
            result = self.run(argv)
            value = json.loads(result.stdout)
        return value

    def seed_task(self):
        self.run([sys.executable, ".trellis/scripts/task.py", "create", "Manifest fixture",
                  "--slug", "manifest-fixture", "--task-id", "manifest-fixture",
                  "--description", "Pre-boundary manifest conflict fixture", "--no-start"])
        records = [p for p in (self.repo / ".trellis/tasks").glob("*/task.json")
                   if json.loads(p.read_text())["id"] == "manifest-fixture"]
        if len(records) != 1:
            raise RuntimeError("Original Task writer did not create one exact fixture Task")
        task_ref = records[0].parent.relative_to(self.repo).as_posix()
        from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
        from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
        BranchBindingStore(inspect_repository(self.repo)).establish(
            TaskLifecycleKey("manifest-fixture", 0), "fixture/task")
        self.run([sys.executable, ".trellis/scripts/task.py", "start", task_ref])
        projection = DeliveryProjection(self.repo, task_ref)
        authority = self.repo / task_ref / "prd.md"
        authority.write_text("R1: retain both installed canonical changes and the same fixture identity.\n")
        projection.scope(authority_ref(authority, self.repo))
        key = {"task_id": "manifest-fixture", "lifecycle_generation": 0,
               "delivery_id": "50191581-5815-4815-8815-000000000815"}
        owners = projection.declaration()["owners"]
        projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": key,
            "owner_role": "creation", "owner_id": owners["creation"],
            "scope_ref": {"authority": projection.read_record()["accepted_scope"], "anchors": ["R1"]},
            "profile": "pull_request"})
        plan = projection.planning_directory(key)
        for name in ("prd.md", "design.md", "implement.md"):
            (plan / name).write_text("Pre-boundary fixture planning for R1.\n")
        for name in ("implement.jsonl", "check.jsonl"):
            (plan / name).write_text("")
        projection.apply({"api_version": "1.0", "operation": "record_gate", "key": key,
            "owner_role": "planning", "owner_id": owners["planning"], "expected_phase": "planning",
            "result": {"result_id": "planning:manifest-fixture", "owner_role": "planning",
                "owner_id": owners["planning"], "outcome": "accepted",
                "scope_ref": projection.resolve(key)["scope_ref"],
                "plan_ref": authority_ref(plan / "design.md", self.repo), "candidate": None,
                "predecessor_result_id": None, "obligations": [],
                "evidence": [authority_ref(plan / name, self.repo)
                             for name in ("prd.md", "design.md", "implement.md")]}})
        projection.select(key)
        return task_ref, key

    def build(self):
        if self.repo.exists():
            raise RuntimeError("Fixture already exists; retain it for its original continuation")
        lock = json.loads((self.source / "trellis/presets/guru-team/source/trellis-source.json").read_text())
        actual = self.run(["git", "rev-parse", "HEAD"], cwd=self.fork).stdout.strip()
        marker = (self.fork / "packages/cli/dist/.guru-source-commit").read_text().strip()
        if actual != lock["commit"] or marker != actual:
            raise RuntimeError("Fork source/build marker differs from this Guru source lock")
        self.repo.mkdir()
        self.git("init", "-q", "-b", "fixture/task")
        self.git("config", "user.name", "Manifest Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("remote", "add", "origin", "https://github.com/castbox/guru-trellis.git")
        shutil.copytree(self.source / "trellis", self.repo / "trellis",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for name in ("README.md", ".gitattributes", ".gitignore"):
            shutil.copy2(self.source / name, self.repo / name)
        self.run(["node", self.fork / "packages/cli/bin/trellis.js", "init", "--yes",
                  "--claude", "--codex", "--cursor"])
        # Assembly before the tested boundary uses exact canonical workflow
        # bytes; this is not evidence of remote marketplace installation.
        shutil.copy2(self.repo / "trellis/workflows/guru-team/workflow.md",
                     self.repo / ".trellis/workflow.md")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture: initialize canonical and native tools")
        self.install()
        task_ref, key = self.seed_task()
        self.git("add", ".")
        self.git("commit", "-qm", "fixture: establish pre-boundary installation and task")
        base = self.git("rev-parse", "HEAD")
        peer = self.output / "peer"
        self.git("worktree", "add", "-qb", "fixture/peer", str(peer))
        self.git("switch", "-qc", "fixture/base")
        self.change("guru-upgrade-tools")
        new_base = self.git("rev-parse", "HEAD")
        self.git("switch", "fixture/task")
        self.change("guru-reconcile-task-base")
        return self.conflict(task_ref, key, base, new_base, peer)

    def conflict(self, task_ref, key, base, new_base, peer):
        """Enter the tested boundary after the actual fixture writers finish."""
        prior = self.git("rev-parse", "HEAD")
        from runtime.delivery_projection.adapter import DeliveryProjection
        projection = DeliveryProjection(self.repo, task_ref)
        paths = self.git("diff", "--name-only", base, prior).splitlines()
        projection.begin_check(key, projection.candidate(paths, head_ref=prior, base_ref=base))
        metadata = (self.repo / task_ref / "task.json").read_bytes()
        merged = self.run(["git", "merge", "--no-commit", "--no-ff", new_base], expected=None)
        if merged.returncode == 0 or MANIFEST not in self.git("diff", "--name-only", "--diff-filter=U").splitlines():
            raise RuntimeError("Normal installer outputs did not produce the required manifest conflict")
        if (self.repo / task_ref / "task.json").read_bytes() != metadata:
            raise RuntimeError("Merge changed unrelated natural Task metadata")
        facts = {"repo": str(self.repo), "peer": str(peer), "task_ref": task_ref, "delivery_key": key,
                 "base": base, "prior_head": prior, "new_base": new_base,
                 "branch": "fixture/task", "manifest": MANIFEST,
                 "peer_before": snapshot(peer), "metadata_sha256": hashlib.sha256(metadata).hexdigest(),
                 "boundary": "Real Git/installer fixture; Agent continuation and final verification pending"}
        (self.output / "fixture.json").write_text(json.dumps(facts, indent=2) + "\n")
        return {k: v for k, v in facts.items() if k != "peer_before"}

    def change(self, skill):
        path = self.repo / "trellis/skills/guru-team/packages" / skill / "references/contract.md"
        path.write_text(path.read_text() + "\n## Fixture branch observation\n\n" + CHANGES[skill])
        self.install()
        self.git("add", ".")
        self.git("commit", "-qm", "fixture: regenerate " + skill + " installation")

    def verify(self):
        facts = json.loads((self.output / "fixture.json").read_text())
        if self.git("ls-files", "-u"):
            raise RuntimeError("Final fixture index still has unmerged entries")
        for skill, text in CHANGES.items():
            canonical = self.repo / "trellis/skills/guru-team/packages" / skill / "references/contract.md"
            for prefix in (".trellis/guru-team/skills/packages", ".agents/skills", ".claude/skills", ".cursor/skills"):
                installed = self.repo / prefix / skill / "references/contract.md"
                if installed.read_bytes() != canonical.read_bytes() or text not in installed.read_text():
                    raise RuntimeError(f"Combined canonical change missing from {installed}")
        manifest = json.loads((self.repo / MANIFEST).read_text())
        if manifest.get("skill_packages", {}).get("status") != "ok":
            raise RuntimeError("Final installer inventory is not valid")
        if self.git("show", "-s", "--format=%P").split() != [facts["prior_head"], facts["new_base"]]:
            raise RuntimeError("Resolved executor did not preserve exact merge parents")
        if snapshot(Path(facts["peer"])) != facts["peer_before"]:
            raise RuntimeError("Peer checkout changed")
        if hashlib.sha256((self.repo / facts["task_ref"] / "task.json").read_bytes()).hexdigest() != facts["metadata_sha256"]:
            raise RuntimeError("Natural dirty Task metadata changed")
        return {"verified": True, "head": self.git("rev-parse", "HEAD"),
                "boundary": "Installation/merge facts only; native Agent and live remote claims remain separate"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--fork", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    source, fork, output = (p.resolve() for p in (args.source, args.fork, args.output))
    if output == source or source in output.parents or output == fork or fork in output.parents:
        parser.error("--output must be outside the source and Fork checkouts")
    output.mkdir(parents=True, exist_ok=True)
    os.environ["TRELLIS_CONTEXT_ID"] = "codex_manifest_fixture815"
    sys.path.insert(0, str(source / "trellis/skills/guru-team"))
    flow = Flow(source, fork, output)
    print(json.dumps(flow.verify() if args.verify else flow.build(), indent=2))


if __name__ == "__main__":
    main()
