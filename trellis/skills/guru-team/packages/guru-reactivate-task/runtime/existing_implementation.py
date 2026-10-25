"""Call-local implementation facts and same-owner recovery comparisons."""
from pathlib import Path

from runtime.task_lifecycle.checkout_resolution import canonical_head_ref
from runtime.task_lifecycle.errors import LifecycleContractError
from runtime.task_lifecycle.git_facts import capture_implementation_state, inspect_repository, local_branch_head
from runtime.task_lifecycle.identity import origin_matches
from runtime.task_lifecycle.source import normalize_repo_ref
import shared_finish

PROFILE = "delivery_reactivate_existing_implementation"


def require_match(condition, field):
    if not condition:
        raise LifecycleContractError("implementation_state_changed", field,
                                     "Reread the selected implementation, base and Draft PR before continuing.")


def read_implementation_pr(public, state, selected_base_ref):
    locator = public["implementation_pr"]
    repo = normalize_repo_ref(locator["repo_ref"])
    require_match(repo == normalize_repo_ref(public["archive_anchor"]["repo_ref"])
                  and origin_matches(Path(state["path"]), repo), "implementation_pr.repo_ref")
    row = shared_finish.github_json(repo, "pulls/" + str(locator["number"]))
    require_match(isinstance(row, dict) and row.get("number") == locator["number"]
                  and row.get("state") == "open" and row.get("draft") is True, "implementation_pr.state")
    for side in ("base", "head"):
        require_match(isinstance(row.get(side), dict)
                      and isinstance(row[side].get("repo"), dict)
                      and str(row[side]["repo"].get("full_name", "")).casefold() == repo.casefold(),
                      "implementation_pr." + side + ".repo")
    base = canonical_head_ref(selected_base_ref)
    require_match(canonical_head_ref(row["base"].get("ref", "")) == base
                  and canonical_head_ref(public["archive_anchor"]["target_ref"]) == base, "implementation_pr.base")
    require_match(canonical_head_ref(row["head"].get("ref", "")) == state["branch_ref"]
                  and row["head"].get("sha") == state["head"], "implementation_pr.head")
    return {"repo_ref": repo, "number": row["number"], "state": row["state"], "draft": row["draft"],
            "base_ref": base, "head_ref": state["branch_ref"], "head": state["head"]}


def observe(root, public):
    state = capture_implementation_state(root)
    base_ref = canonical_head_ref(public["archive_anchor"]["target_ref"])
    base_head = local_branch_head(inspect_repository(root), base_ref)
    require_match(base_head is not None, "selected_base_ref")
    return {"implementation_state": state, "selected_base_ref": base_ref, "reviewed_base_head": base_head,
            "implementation_pr_facts": read_implementation_pr(public, state, base_ref)}


def pending_file_paths(root, public_plan):
    """Derive exact file names from the original writer's frozen plan."""
    checkout = Path(root).resolve()
    return tuple(sorted({action["path"] for action in public_plan["actions"]
                         if action.get("kind", "file") == "file"
                         and Path(action["root"]).resolve() == checkout}))


def validate_current(root, public, semantic, stored=None):
    """Use the after-state only after this operation's own public Task writes."""
    expected = stored["implementation_state"] if stored is not None else semantic["implementation_state"]
    public_files = pending_file_paths(root, stored["public_plan"]) if stored is not None and stored["stage"] == "public_prepared" else ()
    actual = capture_implementation_state(root, public_write_paths=public_files)
    require_match(actual == expected, "implementation_state")
    base_ref = canonical_head_ref(semantic["selected_base_ref"])
    repository = inspect_repository(root)
    require_match(local_branch_head(repository, base_ref) == semantic["reviewed_base_head"], "reviewed_base_head")
    if stored is not None:
        require_match(stored["implementation_pr"] == public["implementation_pr"]
                      and stored["base_ref"] == base_ref and stored["base_head"] == semantic["reviewed_base_head"], "transaction")
    read_implementation_pr(public, actual, base_ref)
    return actual
