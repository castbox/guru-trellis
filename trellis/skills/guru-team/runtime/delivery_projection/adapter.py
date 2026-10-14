"""Use the target's public Delivery API; retain no aggregate or gate authority.

Semantic owners supply scope, candidate and result payloads. The installed
upstream parser/store owns all key validation and legal transitions. Receipts
are private call results; a Skill projects only its next consumer's fields.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from ..task_lifecycle.errors import LifecycleContractError


def upstream_modules(root: Path | str) -> SimpleNamespace:
    """Load only the target installation, with separate namespaces per checkout."""
    directory = Path(root).resolve() / ".trellis/scripts/common"
    init = directory / "__init__.py"
    required = ("delivery_schema", "delivery_operations", "delivery_store", "delivery_session", "runtime_contract")
    if not init.is_file() or any(not (directory / (name + ".py")).is_file() for name in required):
        raise LifecycleContractError("unsupported_delivery_api", "upstream.delivery_api", "Install the reviewed Fixed Fork Delivery API 1.0 candidate before using Guru Delivery profiles.")
    namespace = "guru_delivery_target_" + hashlib.sha256(str(directory).encode()).hexdigest()[:16]
    try:
        if namespace not in sys.modules:
            spec = importlib.util.spec_from_file_location(namespace, init, submodule_search_locations=[str(directory)])
            if spec is None or spec.loader is None:
                raise ImportError("installed public package cannot be loaded")
            module = importlib.util.module_from_spec(spec)
            sys.modules[namespace] = module
            spec.loader.exec_module(module)
        return SimpleNamespace(**{name: importlib.import_module(namespace + "." + name) for name in required})
    except (ImportError, OSError, ValueError) as exc:
        raise LifecycleContractError("unsupported_delivery_api", "upstream.delivery_api", "Reapply the complete reviewed Fixed Fork candidate; no alternative model or source fallback is supported.") from exc


def authority_ref(path: Path | str, root: Path | str) -> dict[str, str]:
    """Bind one actual local file, never a composite approval/acceptance token."""
    file = Path(path).resolve()
    directory = Path(root).resolve()
    try:
        locator = file.relative_to(directory).as_posix()
        content = file.read_bytes()
    except (ValueError, OSError) as exc:
        raise LifecycleContractError("missing_locator", "authority.locator", "Read the exact owner-selected authority file inside this checkout.") from exc
    return {"locator": locator, "revision": "sha256:" + hashlib.sha256(content).hexdigest()}


class DeliveryProjection:
    def __init__(self, root: Path | str, task_ref: str):
        self.root = Path(root).resolve()
        self.task_ref = task_ref
        self.task_dir = self.root / task_ref
        self.api = upstream_modules(self.root)

    def _call(self, function: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except (ValueError, RuntimeError, OSError) as exc:
            if isinstance(exc, LifecycleContractError):
                raise
            raise LifecycleContractError(getattr(exc, "code", "delivery_projection_failed"), "delivery", str(exc)) from exc

    def read_record(self) -> dict:
        try:
            data = json.loads((self.task_dir / "task.json").read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise LifecycleContractError("invalid_record", "task.json", "Read the selected public Task schema-2 record.") from exc
        return self._call(self.api.delivery_schema.parse_task_v2, data)

    def resolve(self, key: dict) -> dict:
        """Use public applicability parsing, including historical relationships."""
        record = self.read_record()
        self._call(self.api.delivery_operations.get_gate_applicability, record, key)
        delivery = next((row for row in record["deliveries"] if row["id"] == key["delivery_id"] and row["lifecycle_generation"] == key["lifecycle_generation"]), None)
        if delivery is None:
            raise LifecycleContractError("delivery_not_found", "delivery_key", "Select the exact Delivery belonging to this Task generation.")
        return delivery

    def planning_directory(self, key: dict) -> Path:
        delivery = self.resolve(key)
        if key["lifecycle_generation"] == self.read_record()["lifecycle_generation"]:
            return self._call(self.api.delivery_session.planning_directory, self.task_dir, self.root, key["delivery_id"])
        # Upstream planning_directory intentionally selects the current generation.
        # History readers instead use the actual validated record's locator.
        return self.task_dir / delivery["planning_root"]

    def declaration(self) -> dict:
        return self._call(self.api.runtime_contract.read_runtime_contract, self.root / ".trellis/workflow.md")

    def has_context(self) -> bool:
        return self._call(self.api.delivery_session.resolve_context_key) is not None

    def _require_explicit_task(self, key: dict) -> None:
        from ..task_lifecycle.active_checkout import resolve_active_task_checkout

        checkout = resolve_active_task_checkout(self.root, self.task_ref)
        if (key["task_id"], key["lifecycle_generation"]) != (
            checkout.artifact.task_id, checkout.artifact.lifecycle_generation,
        ):
            raise LifecycleContractError("stale_lifecycle_generation", "delivery_key", "Use this Task's current generation and registered checkout.")

    def _explicit_current(self, key: dict) -> dict:
        self._require_explicit_task(key)
        delivery = self.resolve(key)
        if delivery["profile"] not in self.declaration()["profiles"]:
            raise LifecycleContractError("unsupported_delivery_profile", "delivery_key", "Use a profile supported by the current workflow.")
        return {"kind": "terminal_delivery" if delivery["phase"] in {"delivered", "stopped"} else "current",
                "key": key, "delivery": delivery, "gate_applicability": self.gate_applicability(key)}

    def current(self, key: dict | None = None) -> dict:
        # An explicit invocation has no session to read. Never use this branch
        # to repair missing/stale selection when a context actually exists.
        if key is not None and not self.has_context():
            return self._explicit_current(key)
        return self._call(self.api.delivery_session.get_current_delivery, self.root)

    def selection_preflight(self, key: dict) -> None:
        """Check existing session facts before creating/selecting another key."""
        if not self.has_context():
            self._require_explicit_task(key)
            return
        current = self.current()
        if current.get("kind") == "error":
            raise LifecycleContractError(current["code"], "session", current["message"])
        selected = current.get("key")
        if selected is not None and (
            {name: selected[name] for name in ("task_id", "lifecycle_generation")}
            != {name: key[name] for name in ("task_id", "lifecycle_generation")}
            or current["kind"] in {"current", "terminal_delivery"} and selected != key
        ):
            raise LifecycleContractError("delivery_selection_conflict", "session", "Resolve the existing explicit current route through its original owner before selecting another Delivery.")

    def apply(self, operation: dict) -> dict:
        return self._call(self.api.delivery_store.apply_to_store, self.task_dir, self.root, operation)

    def select(self, key: dict) -> dict:
        self.resolve(key)
        if not self.has_context():
            current = self._explicit_current(key)
            if current["kind"] == "terminal_delivery":
                raise LifecycleContractError("terminal_delivery", "delivery_key", "Select a nonterminal current Delivery.")
            return current
        return self._call(self.api.delivery_session.select_delivery, self.task_dir, self.root, self.root, key["delivery_id"])

    def release(self, key: dict) -> int:
        self.resolve(key)
        return self._call(self.api.delivery_session.release_delivery, self.root, task_id=key["task_id"], generation=key["lifecycle_generation"], delivery_id=key["delivery_id"])

    def scope(self, authority: dict, *, reopen: bool = False) -> dict:
        record = self.read_record()
        return self.apply({"api_version": "1.0", "operation": "reopen_task" if reopen else "accept_scope",
                           "key": {"task_id": record["id"], "lifecycle_generation": record["lifecycle_generation"]},
                           "owner_role": "task_scope", "owner_id": self.declaration()["owners"]["task_scope"], "authority": authority})

    def begin_check(self, key: dict, candidate: dict) -> dict:
        return self.apply({"api_version": "1.0", "operation": "begin_check", "key": key,
                           "owner_role": "implementation", "owner_id": self.declaration()["owners"]["implementation"],
                           "expected_phase": "implementing", "candidate": candidate})

    def revise_implementation_scope(self, key: dict, scope_ref: dict) -> dict:
        """Project the implementation owner's completed same-slice scope judgment."""
        from .gates import rework
        record = self.read_record()
        if scope_ref["authority"] != record["accepted_scope"]:
            raise LifecycleContractError("stale_scope", "scope_ref", "Consume original Clarify current accepted scope.")
        self._call(self.api.delivery_store.verify_authority, self.root, scope_ref["authority"])
        delivery = self.resolve(key)
        recovered = (delivery["phase"] == "planning" and delivery["scope_ref"] == scope_ref
                     and all(value is None for value in delivery["results"].values()))
        if not recovered:
            if delivery["phase"] != "implementing":
                raise LifecycleContractError("stale_phase", "phase", "Return to the current stage scope owner.")
            rework(self, key, "implementation", "planning", scope_ref["authority"],
                   ["planning", "check", "full_review", "readiness"], scope_ref=scope_ref)
        return key

    def stop_implementation(self, key: dict, result: dict) -> dict:
        """Record the implementation step's already reviewed withdrawal result."""
        owner = self.declaration()["owners"]["implementation"]
        public_result = {name: result[name] for name in ("result_id", "reason", "scope_decision", "evidence")}
        public_result["owner_id"] = owner
        delivery = self.resolve(key)
        if delivery["phase"] == "stopped":
            if delivery["stop_result"] != public_result:
                raise LifecycleContractError("stale_stop_result", "stop_result", "Recover the original implementation withdrawal conclusion.")
        else:
            self.apply({"api_version": "1.0", "operation": "stop", "key": key,
                        "owner_role": "implementation", "owner_id": owner,
                        "expected_phase": "implementing", "result": public_result})
        self.release(key)
        return {"task_id": key["task_id"], "lifecycle_generation": key["lifecycle_generation"]}

    def candidate(self, paths: list[str], *, kind: str = "git", head_ref: str | None = None, base_ref: str | None = None) -> dict:
        return {"kind": kind, "content_ref": self._call(self.api.delivery_store.candidate_content_ref, self.root, paths, kind),
                "paths": paths, "head_ref": head_ref, "base_ref": base_ref}

    def gate_applicability(self, key: dict) -> dict:
        self.resolve(key)
        return self._call(self.api.delivery_operations.get_gate_applicability, self.read_record(), key)

    def require_current_check(self, key: dict, result_id: str, *, head_ref: str, base_ref: str) -> dict:
        """Validate a Review consumer's exact predecessor against public/live facts."""
        delivery = self.resolve(key)
        check = delivery["results"]["check"]
        if (delivery["phase"] != "reviewing" or check is None
                or check["result_id"] != result_id or check["outcome"] != "passed"
                or check["owner_id"] != self.declaration()["owners"]["check"]
                or self.gate_applicability(key)["check"]["kind"] != "applicable"
                or check["candidate"]["kind"] != "git"
                or check["candidate"]["head_ref"] != head_ref
                or check["candidate"]["base_ref"] != base_ref):
            raise LifecycleContractError("stale_check", "check_result_id", "Consume the current candidate-bound public Check after reconciliation.")
        self._call(self.api.delivery_store.verify_candidate, self.root, check["candidate"])
        planning = delivery["results"]["planning"]
        references = [delivery["scope_ref"]["authority"], delivery["plan_ref"]]
        for result in (planning, check):
            references.extend(result["obligations"])
            references.extend(result["evidence"])
        for reference in references:
            self._call(self.api.delivery_store.verify_authority, self.root, reference)
        return check
