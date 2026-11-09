"""Factual cross-repository scenes for the real native orchestration runner.

This source-only carrier reuses the existing Codex process, MCP, operation and
trace implementation. It never parses child messages or chooses coordinator
routes. Host-only observations live in forward-cases.md, outside model context.
"""
from pathlib import Path
import time

from run_native_orchestration import Carrier, WORKFLOW


class CrossCarrier(Carrier):
    def __init__(self, scene: str, output: Path, model_root: Path):
        super().__init__("dag", output, model_root)
        self.scene = scene
        self.merge_service_ready_at = None
        self.coordinator_started = False
        repositories = ("fixture/api", "fixture/web")
        if scene == "initiative":
            repositories += ("fixture/product",)
        elif scene == "environment-user":
            repositories += ("fixture/cms", "fixture/product")
        projects = {}
        for index, repository in enumerate(repositories):
            name = repository.split("/")[1]
            base = "dev" if name == "api" else ("stable" if name == "web" else "main")
            projects[repository] = {
                "repository": repository, "path": str(model_root / name),
                "project_id": f"project-{name}", "primary_folder": str(model_root / name),
                "primary_repository": repository, "remote": f"https://github.com/{repository}.git",
                "default_branch": "main", "selected_base": base,
                "local_base_oid": f"{name}-{base}", "tracking_oid": f"{name}-{base}",
                "remote_base_oid": f"{name}-{base}", "checkout_clean": True,
                "checkout_exists": True, "saved_project": True, "trust": "ready",
                "setup_prerequisites": [], "setup_configured": False,
                "creation_entry": "establish_environment", "creation_permission": True,
            }
        if scene in ("environment-create", "environment-user"):
            projects["fixture/web"].update(checkout_exists=False, saved_project=False)
        if scene == "environment-user":
            projects["fixture/web"]["creation_permission"] = False
            projects["fixture/cms"].update(saved_project=False, creation_entry=None)
            projects["fixture/product"]["trust"] = "user_review_required"
        nodes = {}
        pairs = [("fixture/api", 7), ("fixture/web", 7)]
        if scene == "cross-repo":
            pairs += [("fixture/web", 8)]
        elif scene == "initiative":
            pairs += [("fixture/product", 4), ("fixture/product", 99)]
        elif scene == "environment-user":
            pairs += [("fixture/cms", 7), ("fixture/product", 7), ("fixture/api", 8)]
        for repository, issue in pairs:
            key = f"{repository}#{issue}"
            binding = projects[repository]
            path = f"inputs/{repository}/{issue}/current.json"
            dependencies = []
            if scene == "cross-repo" and key == "fixture/web#7":
                dependencies = ["fixture/api#7"]
            if scene == "environment-user" and key == "fixture/api#8":
                dependencies = ["fixture/web#7"]
            if scene == "initiative" and key == "fixture/product#4":
                dependencies = ["fixture/api#7", "fixture/web#7"]
            nodes[key] = {
                "node_key": key, "repository": repository, "issue": issue, "state": "open",
                "scope": "Deliver the scoped fixture output and complete its Task.",
                "depends_on": dependencies, "default_branch": binding["default_branch"],
                "task_id": f"task-{key}", "generation": 0, "delivery_id": f"delivery-{key}",
                "branch": f"issue-{issue}", "worktree": binding["path"] + f"/issue-{issue}",
                "input_path": path, "input_catalog": {path: {"exists": True, "value": issue}},
                "operations": {}, "output": None, "verification": None, "gates": {},
                "pr": {"repository": repository, "number": issue + 1000,
                       "base": binding["selected_base"], "head": f"candidate-{key}",
                       "merged": False, "merge_result": None, "required_checks": []},
                "task_archived": False, "resources": "retained; nonblocking by repository policy",
            }
        if scene == "initiative":
            nodes["fixture/product#4"]["scope"] = "Finalize product acceptance of the two formally bound engineering deliveries; requirements are already ready."
            for key in ("fixture/api#7", "fixture/web#7"):
                nodes[key]["requirement_source"] = {"issue": "fixture/product#4", "requirements_status": "ready", "role": "accepted product requirements, not completed final acceptance"}
        self.state = {
            "coordinator_repository": "fixture/coordination", "provider_repository": "fixture/provider",
            "repositories": projects, "workflow": WORKFLOW,
            "nodes": nodes, "children": {}, "heartbeat": None,
            "competing_owners": [], "unresolved_operations": {}, "tick": 0,
            "capabilities": {
                "environment_read": "inspect_environment(repository)",
                "environment_creation": "establish_environment(repository, path, remote, primary_folder)",
                "project_list": "list_projects", "trust_mutation": None,
                "heartbeat_update": "automation_update(mode=update, id, status=ACTIVE|PAUSED, prompt, interval_minutes, target); preserve existing fields, then heartbeat_read",
                "user_ui": "Codex Projects: add/edit local project and choose primary folder; review App-displayed trust prompt; local environment setup only when actual prerequisites exist",
                "operation_read": "read_operation(operation_id); child recover_operation(operation_id) reads its original transaction",
                "child_creation": "create_child(repository, issue, project_id, source_branch, target_branch, model, effort, message)",
            },
        }
        if scene == "initiative":
            self.state["initiative"] = {
                "locator": "https://github.com/fixture/product/issues/42", "state": "open",
                "formal_members": [
                    {"issue": "fixture/product#4", "role": "product final acceptance", "requirements_status": "ready"},
                    {"issue": "fixture/api#7", "role": "API engineering delivery"},
                    {"issue": "fixture/web#7", "role": "Web engineering delivery"}],
                "related_links": [{"issue": "fixture/product#99", "role": "historical research, information only"}],
            }

    def prime_pending_merge(self, model: str, effort: str, limit: int) -> None:
        """Create genuine existing readiness and one unknown merge before resume."""
        for key, node in self.state["nodes"].items():
            project = self.state["repositories"][node["repository"]]
            self.coordinator_call("create_child", {
                "repository": node["repository"], "issue": node["issue"],
                "project_id": project["project_id"], "source_branch": project["selected_base"],
                "target_branch": project["selected_base"], "model": model, "effort": effort,
                "message": "Read current Issue facts and original workflow. Own this Issue’s implementation, required verification, semantic Check, full-range Review and readiness. Stop before merge and report actual results and exact next operation.",
            })
        self.wait_for_children(limit)
        for node in self.state["nodes"].values():
            if any(node["gates"].get(stage, {}).get("status") != "passed"
                   for stage in ("check", "review", "readiness")):
                raise RuntimeError("Original real child readiness was not established; inspect preserved traces.")
        self.launch("child-fixture-api-7", "合并PR fixture/api#1007, exact candidate candidate-fixture/api#7 into dev. Recheck its current merge prerequisites, perform the original merge once and report its actual operation result. This segment stops after that result; do not repeat an unknown operation or perform Closure/Finish.")
        self.wait_for_children(limit)
        if not self.state["nodes"]["fixture/api#7"].get("merge_operation"):
            raise RuntimeError("Original real child did not execute the pending merge boundary.")
        self.coordinator_started = True

    def wait_for_children(self, limit: int) -> None:
        deadline = time.monotonic() + min(limit, 600)
        while self.running and time.monotonic() < deadline:
            time.sleep(1)
            self.refresh()
        if self.running:
            raise RuntimeError("Priming original child did not settle; preserve process logs.")

    def resolve_merge_service(self) -> None:
        if self.scene != "merge-pending" or not self.coordinator_started:
            return
        if self.merge_service_ready_at is None:
            self.merge_service_ready_at = time.monotonic() + 120
        node = self.state["nodes"]["fixture/api#7"]
        operation = node.get("merge_operation")
        if operation and operation["status"] == "pending" and time.monotonic() >= self.merge_service_ready_at:
            node["pr"].update(merged=True, merge_result="merge-fixture/api#7",
                              reachable_from_base="dev", reachable_from_default=False)
            operation.update(status="succeeded", result=dict(node["pr"]))
            self.trace("external-merge-service", "operation_completed", {"operation_id": operation["id"]}, operation)

    def child_call(self, child: str, op: str, a: dict) -> object:
        self.resolve_merge_service()
        row = self.state["children"][child]
        node = self.state["nodes"][row["node_key"]]
        if op == "inspect" and ("node_ref" in a or "repository" in a):
            key = self.key(a)
            return self.state["nodes"][key] if key else {"error": "repository_qualified_identity_required"}
        if self.scene == "merge-pending" and node["node_key"] == "fixture/api#7":
            if op == "merge":
                if node.get("merge_operation"):
                    return {"error": "existing_merge_operation", "operation": node["merge_operation"]}
                missing = [stage for stage in ("check", "review", "readiness")
                           if node["gates"].get(stage, {}).get("status") != "passed"]
                if missing or not (node["verification"] or {}).get("passed"):
                    return {"error": "merge_prerequisites_missing", "missing": missing}
                operation = {"id": "merge-operation-fixture-api-7", "repository": "fixture/api",
                             "issue": 7, "status": "pending", "candidate": node["pr"]["head"],
                             "base": "dev", "owner": child, "result": None,
                             "recheck": "bounded merge service completion"}
                node["merge_operation"] = operation
                node["operations"][operation["id"]] = operation
                return {"status": "unknown", "operation_id": operation["id"],
                        "result_available": False}
        return super().child_call(child, op, a)

    def selection(self) -> str:
        if self.scene == "initiative":
            import json
            bindings = {repo: {"project_path": row["path"], "base_branch": row["selected_base"]}
                        for repo, row in self.state["repositories"].items()}
            return "initiative=https://github.com/fixture/product/issues/42; repositories=" + json.dumps(bindings) + "; max_parallel=2; failure_policy=continue_independent"
        refs = [key for key in self.state["nodes"]]
        nodes = [{"repository": self.state["nodes"][key]["repository"], "issue": self.state["nodes"][key]["issue"],
                  "depends_on": self.state["nodes"][key]["depends_on"]} for key in refs]
        bindings = {repo: {"project_path": row["path"], "base_branch": row["selected_base"]}
                    for repo, row in self.state["repositories"].items()}
        import json
        return "repositories=" + json.dumps(bindings) + "; nodes=" + json.dumps(nodes) + "; max_parallel=2; failure_policy=continue_independent"

    def key(self, a: dict) -> str | None:
        if a.get("node_ref") in self.state["nodes"]:
            return a["node_ref"]
        if a.get("repository") is not None and a.get("issue") is not None:
            key = f"{a['repository']}#{a['issue']}"
            return key if key in self.state["nodes"] else None
        matches = [key for key, node in self.state["nodes"].items() if node["issue"] == a.get("issue")]
        return matches[0] if len(matches) == 1 else None

    def coordinator_call(self, op: str, a: dict) -> object:
        self.resolve_merge_service()
        s = self.state
        if op == "read_operation" and self.scene == "merge-pending":
            return s["nodes"]["fixture/api#7"]["operations"].get(a["operation_id"], {"error": "unknown_operation"})
        if op == "inspect":
            if "issue" in a or "node_ref" in a:
                key = self.key(a)
                return s["nodes"][key] if key else {"error": "repository_qualified_identity_required"}
            return s
        if op == "inspect_environment":
            return s["repositories"].get(a["repository"], {"error": "unknown_repository"})
        if op == "list_projects":
            return [row for row in s["repositories"].values() if row["saved_project"]]
        if op == "inspect_capabilities":
            return s["capabilities"]
        if op == "read_initiative":
            return s.get("initiative", {"error": "unknown_initiative"})
        if op == "establish_environment":
            row = s["repositories"][a["repository"]]
            if row["creation_entry"] is None:
                return {"error": "unsupported_entry", "repository": a["repository"]}
            if not row["creation_permission"]:
                return {"error": "permission_denied", "repository": a["repository"]}
            expected = {"path": row["path"], "remote": row["remote"], "primary_folder": row["primary_folder"]}
            if any(a.get(k) != v for k, v in expected.items()):
                return {"error": "environment_arguments_mismatch", "expected": expected}
            row.update(checkout_exists=True, saved_project=True)
            return {"operation": "created_checkout_and_saved_project", "repository": row["repository"], "project_id": row["project_id"]}
        if op == "automation_update":
            heartbeat = s["heartbeat"]
            if not heartbeat or a.get("id") != heartbeat["id"] or a.get("mode") != "update":
                return {"error": "unknown_heartbeat_or_update_mode"}
            if a.get("status") not in ("ACTIVE", "PAUSED"):
                return {"error": "unsupported_status"}
            fields = ("prompt", "interval_minutes", "target")
            if any(a.get(field) != heartbeat[field] for field in fields):
                return {"error": "existing_heartbeat_fields_required", "heartbeat": heartbeat}
            heartbeat["active"] = a["status"] == "ACTIVE"
            return heartbeat
        if op == "create_child":
            key = self.key(a)
            if not key:
                return {"error": "repository_qualified_identity_required"}
            node = s["nodes"][key]
            row = s["repositories"][node["repository"]]
            if not row["checkout_exists"] or not row["saved_project"] or row["trust"] != "ready":
                return {"error": "environment_not_ready", "repository": row["repository"]}
            expected = {"project_id": row["project_id"], "source_branch": row["selected_base"], "target_branch": row["selected_base"]}
            if any(a.get(k) != v for k, v in expected.items()):
                return {"error": "child_binding_mismatch", "expected": expected}
            if any(child.get("node_key") == key for child in s["children"].values()):
                return {"error": "existing_child", "node_ref": key}
            identity = "child-" + key.replace("/", "-").replace("#", "-")
            s["children"][identity] = {
                "node_key": key, "repository": node["repository"], "issue": node["issue"],
                "thread_id": identity, "host_id": "fixture-host", "active": False, "safe": True,
                "project_id": row["project_id"], "source_branch": a["source_branch"],
                "model": a["model"], "effort": a["effort"], "messages": [],
            }
            result = self.launch(identity, a["message"])
            result.update(thread_id=identity, host_id="fixture-host")
            return result
        if op == "observe_external":
            return None
        return super().coordinator_call(op, a)

    def user_environment_update(self) -> str:
        # This host event is a completed user action between genuine coordinator
        # turns. It supplies facts only; no Agent message is interpreted as consent.
        for row in self.state["repositories"].values():
            row.update(checkout_exists=True, saved_project=True, trust="ready")
        result = "I created/registered fixture/web and fixture/cms at their listed paths, selected their correct primary folders, and completed the App trust review for fixture/product. Please reread the current facts and continue this same run."
        self.trace("external-user", "environment_update", {}, {"repositories": self.state["repositories"], "message": result})
        return result
