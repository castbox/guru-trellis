def publish_config(config: dict[str, Any]) -> dict[str, Any]:
    value = config.get("publish")
    return value if isinstance(value, dict) else dict(DEFAULTS["publish"])

def is_strict_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

def task_dir_is_archived(root: Path, task_dir: Path) -> bool:
    try:
        task_dir.resolve().relative_to((tasks_root(root) / "archive").resolve())
        return True
    except ValueError:
        return False

def contract_wording_read_input(root: Path, value: str | None, label: str) -> dict[str, Any]:
    if isinstance(value, dict):
        return copy.deepcopy(value)
    if not value:
        raise WorkflowError(f"{label} requires an input JSON file.", exit_code=2)
    if value == "-":
        raw = sys.stdin.read()
    else:
        path = Path(value)
        if not path.is_absolute():
            path = root / path
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise WorkflowError(f"{label} input is unreadable.", exit_code=2) from exc
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"{label} input is invalid JSON.", exit_code=2) from exc
    if not isinstance(payload, dict):
        raise WorkflowError(f"{label} input root must be an object.", exit_code=2)
    return payload

def repo_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)

def finalizer_unreviewed_dirty_paths(
    root: Path,
    task_dir: Path,
) -> list[str]:
    del task_dir
    return [
        path
        for path in git_status_paths(root, fail_closed=True)
        if not reviewed_content_metadata_path(path)
    ]

def review_branch_content_continuity_errors(
    root: Path,
    task_dir: Path,
    review_commit: str,
    reviewed_content_sha256: str,
    current: str | None = None,
) -> list[str]:
    del task_dir
    current_head_value = current or current_head(root)
    if not re.fullmatch(r"[0-9a-f]{40}", review_commit):
        return ["Branch Review review_commit is invalid."]
    if not re.fullmatch(r"[0-9a-f]{64}", reviewed_content_sha256):
        return ["Branch Review reviewed_content_sha256 is invalid."]
    if not is_ancestor(root, review_commit, current_head_value):
        return [
            "Branch Review review_commit is not an ancestor of the current HEAD."
        ]
    try:
        anchor_identity = reviewed_content_identity(
            root,
            review_commit,
            include_worktree=False,
        )["sha256"]
        current_identity = reviewed_content_identity(
            root,
            current_head_value,
            include_worktree=True,
        )["sha256"]
    except WorkflowError:
        return ["Branch Review could not calculate reviewed-content continuity."]
    if anchor_identity != reviewed_content_sha256:
        return ["Branch Review gate identity does not match review_commit."]
    if current_identity != reviewed_content_sha256:
        return [BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX + "identity mismatch"]
    return []

def base_branch_from_sources(args: argparse.Namespace, task: dict[str, Any], task_context: dict[str, Any]) -> str:
    for value in [
        getattr(args, "base_branch", None),
        task_context.get("base_branch"),
        task.get("base_branch"),
    ]:
        if value:
            return str(value)
    raise WorkflowError("Could not resolve base_branch from args, task runtime identity, or task.json.")

def markdown_section_ranges(body: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^(#{2,6})\s+(.+?)\s*$", body))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[title] = body[start:end].strip()
    return sections

def find_pr_body_sections(body: str) -> dict[str, str]:
    raw_sections = markdown_section_ranges(body)
    found: dict[str, str] = {}
    for required, aliases in PR_BODY_SECTION_ALIASES.items():
        for title, content in raw_sections.items():
            normalized_title = re.sub(r"\s+", " ", title).strip()
            if any(alias.lower() in normalized_title.lower() for alias in aliases):
                found[required] = content
                break
    return found

def normalized_body_line(line: str) -> str:
    return line.strip().lstrip("-*•").strip()

def section_has_specific_bullet(section: str) -> bool:
    for line in section.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("-") or stripped.startswith("*") or stripped.startswith("•")):
            continue
        normalized = normalized_body_line(stripped).lower()
        if normalized in PR_BODY_PLACEHOLDER_VALUES:
            continue
        if "详见" in normalized:
            continue
        if len(normalized) < 8:
            continue
        return True
    return False

def section_has_substantive_text(section: str) -> bool:
    lines = [normalized_body_line(line) for line in section.splitlines()]
    meaningful = [line for line in lines if line and line.lower() not in PR_BODY_PLACEHOLDER_VALUES]
    if not meaningful:
        return False
    return any("详见" not in line for line in meaningful)

def missing_docs_ssot_keys(section: str) -> list[str]:
    lowered = section.lower()
    missing: list[str] = []
    for key, aliases in PR_BODY_DOCS_SSOT_KEY_ALIASES.items():
        if not any(alias.lower() in lowered for alias in aliases):
            missing.append(key)
    return missing

def close_keyword_pattern() -> re.Pattern[str]:
    return re.compile(r"(?i)\b(" + "|".join(re.escape(keyword) for keyword in PR_CLOSE_KEYWORDS) + r")\s+#(\d+)\b")

def canonical_json_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def validate_pr_body_quality(body: str, draft: bool) -> list[str]:
    errors: list[str] = []
    sections = find_pr_body_sections(body)
    for section in PR_BODY_REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(f"PR body 缺少 `{section}` section。")

    if not draft:
        for phrase in PR_BODY_LOW_INFORMATION_PHRASES:
            if phrase in body:
                errors.append(f"PR body 包含低信息量摘要或占位短语：{phrase}")

    summary = sections.get("变更摘要", "")
    if summary and not section_has_specific_bullet(summary):
        errors.append("PR body `变更摘要` 缺少具体 bullet。")
    for section in ["影响范围", "验证结果", "安全说明"]:
        value = sections.get(section, "")
        if value and not section_has_substantive_text(value):
            errors.append(f"PR body `{section}` 缺少具体内容。")
    docs_ssot = sections.get("Docs SSOT", "")
    if docs_ssot:
        missing = missing_docs_ssot_keys(docs_ssot)
        if missing:
            errors.append("PR body `Docs SSOT` section 缺少客观键：{}。".format(", ".join(missing)))

    return errors

TASK_PUBLICATION_DIMENSIONS = (
    "diff_outcome_consistency",
    "external_work_item_effect",
    "pr_body_quality",
    "validation_claims",
    "branch_review_summary",
    "docs_ssot_reconciliation",
    "safety_deployment_impact",
    "finish_summary_semantics",
    "metadata_tail_integrity",
    "artifact_binding_freshness",
)

TASK_PUBLICATION_CONSUMERS = {
    "ready": {"kind": "skill", "id": "guru-finalize-task"},
    "return_to_task_work": {
        "kind": "workflow",
        "id": "guru-task-publication-work-router",
    },
    "blocked": {"kind": "stop", "id": "task-publication-review-blocked"},
}


class TaskPublicationInvocationContext:
    """Invocation-local Publication facts and validation receipt.

    This context never crosses a process boundary. It allows the Happy Path
    invocation to reuse one objective snapshot between record and check while
    the package-private commands continue to rebuild live facts independently.
    """

    def __init__(
        self,
        root: Path,
        config: dict[str, Any],
        task_dir: Path,
        task_context: dict[str, Any],
    ) -> None:
        self.root = root
        self.config = config
        self.task_dir = task_dir
        self.task_context = task_context
        self.entry_cache: dict[
            str,
            tuple[
                dict[str, dict[str, str]],
                list[str],
                dict[str, Any],
                dict[str, Any],
            ],
        ] = {}
        self.checked_owner_result: dict[str, Any] | None = None
        self.operation_counts: dict[str, int] = {}

    @classmethod
    def create(cls, root: Path, task_ref: str | None) -> "TaskPublicationInvocationContext":
        config = load_config(root)
        task_dir = resolve_task_dir(root, task_ref)
        task_context = load_task_runtime_identity(task_dir, config)
        assert_workspace_boundary(root, config, task_context, task_dir)
        context = cls(
            root=root,
            config=config,
            task_dir=task_dir,
            task_context=task_context,
        )
        context.count("task_workspace.read")
        return context

    def count(self, operation: str) -> None:
        self.operation_counts[operation] = self.operation_counts.get(operation, 0) + 1

    def assert_call(self, root_value: str | None, task_ref: str | None) -> None:
        requested_root = repo_root(Path(root_value or self.root))
        requested_task = resolve_task_dir(requested_root, task_ref)
        if requested_root != self.root or requested_task != self.task_dir:
            raise WorkflowError(
                "Publication invocation context does not match the requested task.",
                exit_code=2,
                payload={
                    "error_code": "publication_input_invalid",
                    "field_path": "input.task_ref",
                    "recovery": "Use one public invocation for the exact current task and repository.",
                },
            )

    def entry_bindings(
        self,
        invocation: dict[str, Any],
    ) -> tuple[dict[str, dict[str, str]], list[str], dict[str, Any], dict[str, Any]]:
        cache_value = {
            "task_ref": invocation.get("task_ref"),
            "branch_review_commit": invocation.get("branch_review_commit"),
            "pr_payload": invocation.get("pr_payload"),
        }
        cache_key = context_digest(cache_value)
        if cache_key not in self.entry_cache:
            self.entry_cache[cache_key] = task_publication_entry_precondition_bindings(
                self.root,
                self.task_dir,
                self.config,
                invocation,
            )
            self.count("publication.snapshot")
        return self.entry_cache[cache_key]

def task_publication_schema(root: Path) -> dict[str, Any]:
    candidates = (
        root
        / "trellis/skills/guru-team/packages/guru-review-task-publication/schemas/pr-readiness.schema.json",
        root
        / ".trellis/guru-team/skills/packages/guru-review-task-publication/schemas/pr-readiness.schema.json",
    )
    for path in candidates:
        if path.is_file() and not path.is_symlink():
            errors: list[str] = []
            schema = skill_read_schema(path, "task publication readiness schema", errors)
            if isinstance(schema, dict) and not errors:
                return schema
    raise WorkflowError(
        "guru-review-task-publication readiness schema is unavailable.",
        exit_code=2,
    )

def task_publication_path(
    root: Path,
    task_dir: Path,
) -> Path:
    return ai_first_owner_checkpoint_path(root, task_dir, PR_READINESS_ARTIFACT)

def task_publication_repository_binding(
    root: Path,
    task_dir: Path,
) -> dict[str, Any]:
    task = task_json(task_dir)
    base_branch = str(task.get("base_branch") or "")
    base_ref = diff_base_ref(root, base_branch) if base_branch else ""
    diff_process = run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=root,
        check=False,
    )
    if diff_process.returncode != 0:
        raise WorkflowError(
            "Task publication review could not rebuild the current diff.",
            exit_code=2,
        )
    readiness_relative = repo_relative(root, task_dir / PR_READINESS_ARTIFACT)
    return {
        "head": current_head(root),
        "branch": current_branch(root),
        "base_ref": base_ref,
        "diff_paths": sorted(
            line.strip()
            for line in diff_process.stdout.splitlines()
            if line.strip()
        ),
        "status_paths": sorted(
            path
            for path in git_status_paths(root, fail_closed=True)
            if path != readiness_relative
        ),
    }

def task_publication_unexpected_status_paths(
    status_paths: list[str],
) -> list[str]:
    return sorted(
        path for path in status_paths if not reviewed_content_metadata_path(path)
    )

def task_publication_binding(
    value: Any,
    *,
    status: str = "passed",
) -> dict[str, str]:
    return {
        "status": status,
        "facts_sha256": context_digest(value),
    }

def task_publication_entry_precondition_bindings(
    root: Path,
    task_dir: Path,
    config: dict[str, Any],
    invocation: dict[str, Any],
) -> tuple[dict[str, dict[str, str]], list[str], dict[str, Any], dict[str, Any]]:
    """Rebuild the objective publication-entry preconditions.

    The function records only deterministic facts after the semantic owner has
    authored its review. It never selects a finding route, dimension status, or
    typed exit.
    """
    bindings: dict[str, dict[str, str]] = {}
    errors: list[str] = []

    step_errors: list[str] = []
    try:
        readiness_schema = task_publication_schema(root)
        package_candidates = (
            root / "trellis/skills/guru-team/packages/guru-review-task-publication",
            root / ".trellis/guru-team/skills/packages/guru-review-task-publication",
        )
        package = next(
            (
                candidate
                for candidate in package_candidates
                if (candidate / "interface.json").is_file()
                and (candidate / "schemas/public-input.schema.json").is_file()
            ),
            None,
        )
        if package is None:
            raise WorkflowError(
                "guru-review-task-publication package is unavailable.",
                exit_code=2,
            )
        runtime_facts = {
            "schema": readiness_schema,
            "interface_sha256": hashlib.sha256(
                (package / "interface.json").read_bytes()
            ).hexdigest(),
            "public_input_schema_sha256": hashlib.sha256(
                (package / "schemas/public-input.schema.json").read_bytes()
            ).hexdigest(),
        }
    except (OSError, WorkflowError) as exc:
        step_errors.append(f"runtime_dependency:{exc}")
    if step_errors:
        errors.extend(step_errors)
    else:
        bindings["runtime_dependency"] = task_publication_binding(runtime_facts)

    task_context: dict[str, Any] = {}
    task: dict[str, Any] = {}
    step_errors = []
    try:
        task_context = load_task_runtime_identity(task_dir, config)
        assert_workspace_boundary(root, config, task_context, task_dir)
        task = task_json(task_dir)
    except WorkflowError as exc:
        step_errors.append(f"task_workspace:{exc}")
    if step_errors:
        errors.extend(step_errors)
    else:
        bindings["task_workspace"] = task_publication_binding({
            "task_artifact_dir": task_context.get("task_artifact_dir"),
            "task_workspace_id": task_context.get("task_workspace_id"),
            "workspace_mode": config.get("workspace_mode"),
            "repo_root": str(root.resolve()),
        })

    step_errors = []
    expected_task = repo_relative(root, task_dir)
    expected_branch = str(
        task_context.get("branch_name") or task.get("branch") or ""
    )
    expected_base = str(
        task_context.get("base_branch") or task.get("base_branch") or ""
    )
    if (
        not task
        or task.get("status") != "in_progress"
        or not expected_branch
        or current_branch(root) != expected_branch
        or not expected_base
        or invocation.get("task_ref", expected_task) != expected_task
    ):
        step_errors.append("task_identity:current task, branch, base, or status mismatch")
    if step_errors:
        errors.extend(step_errors)
    else:
        bindings["task_identity"] = task_publication_binding({
            "task_ref": expected_task,
            "task_id": task.get("id"),
            "status": task.get("status"),
            "branch": expected_branch,
            "base_branch": expected_base,
        })

    branch_review_commit = str(invocation.get("branch_review_commit") or "")
    review_handoff: dict[str, Any] = {
        "typed_exit": "passed",
        "branch_review_commit": branch_review_commit,
    }
    review_errors: list[str] = []
    if not re.fullmatch(r"[0-9a-f]{40}", branch_review_commit):
        review_errors.append("Branch Review DTO branch_review_commit is invalid.")
    else:
        try:
            reviewed_content_sha256 = reviewed_content_identity(
                root,
                branch_review_commit,
                include_worktree=False,
            )["sha256"]
            review_errors.extend(
                review_branch_content_continuity_errors(
                    root,
                    task_dir,
                    branch_review_commit,
                    reviewed_content_sha256,
                    current_head(root),
                )
            )
        except WorkflowError as exc:
            review_errors.append(
                f"Branch Review DTO content continuity is unavailable: {exc}"
            )
    if review_errors:
        errors.extend(
            f"branch_review_handoff:{item}" for item in sorted(set(review_errors))
        )
    else:
        bindings["branch_review_handoff"] = task_publication_binding(
            review_handoff
        )

    try:
        repository = task_publication_repository_binding(root, task_dir)
    except WorkflowError as exc:
        repository = {}
        errors.append(f"review_range_and_working_tree:{exc}")

    publication_content_errors: list[str] = []
    pr_payload = invocation.get("pr_payload")
    if not isinstance(pr_payload, dict) or set(pr_payload) != {"title", "body"}:
        publication_content_errors.append("PR payload must contain exactly title and body")
        pr_payload = {}
    title = pr_payload.get("title")
    body = pr_payload.get("body")
    if not isinstance(title, str) or not title.strip():
        publication_content_errors.append("PR title is empty")
    if not isinstance(body, str) or not body.strip():
        publication_content_errors.append("PR body is empty")
    else:
        publication_content_errors.extend(validate_pr_body_quality(body, False))
    if publication_content_errors:
        errors.extend(
            f"publication_content:{item}"
            for item in sorted(set(publication_content_errors))
        )
    else:
        bindings["publication_content"] = task_publication_binding({
            "pr_title": title,
            "pr_body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        })

    if repository:
        unexpected_status_paths = task_publication_unexpected_status_paths(
            repository["status_paths"],
        )
        if unexpected_status_paths:
            errors.append(
                "review_range_and_working_tree:working tree has paths outside "
                "the reviewed-content boundary: "
                + ", ".join(unexpected_status_paths[:20])
                + "."
            )
        else:
            bindings["review_range_and_working_tree"] = task_publication_binding(
                repository
            )

    bindings["invocation_freshness"] = task_publication_binding({
        "task_ref": expected_task,
        "branch_review_commit": branch_review_commit,
    })

    expected_ids = {
        "runtime_dependency",
        "task_workspace",
        "task_identity",
        "branch_review_handoff",
        "publication_content",
        "review_range_and_working_tree",
        "invocation_freshness",
    }
    for entry_id in sorted(expected_ids - set(bindings)):
        entry_errors = [
            item
            for item in errors
            if item.startswith(entry_id + ":")
        ]
        bindings[entry_id] = task_publication_binding(
            {
                "entry_precondition_id": entry_id,
                "errors": entry_errors or ["objective evidence unavailable"],
            },
            status="failed",
        )
    return bindings, sorted(set(errors)), review_handoff, repository

def task_publication_semantic_errors(
    authored: dict[str, Any],
    *,
    branch_review_commit: str,
) -> list[str]:
    errors: list[str] = []
    pr_payload = authored.get("pr_payload")
    if not isinstance(pr_payload, dict) or set(pr_payload) != {"title", "body"}:
        errors.append("publication pr_payload must contain exactly title and body")
    elif (
        not isinstance(pr_payload.get("title"), str)
        or not pr_payload["title"].strip()
        or not isinstance(pr_payload.get("body"), str)
        or not pr_payload["body"].strip()
    ):
        errors.append("publication pr_payload title and body must be non-empty")
    candidate_commit = str(
        authored.get("branch_review_commit") or branch_review_commit
    )
    if candidate_commit != branch_review_commit:
        errors.append(
            "publication branch_review_commit does not match current Branch Review"
        )
    dimensions = authored.get("dimensions")
    if not isinstance(dimensions, list):
        errors.append("publication dimensions must be a list")
        dimensions = []
    ids = [item.get("id") for item in dimensions if isinstance(item, dict)]
    if ids != list(TASK_PUBLICATION_DIMENSIONS):
        errors.append("publication dimensions must contain the exact ordered ten ids")
    for item in dimensions:
        if (
            not isinstance(item, dict)
            or set(item) != {"id", "status", "summary", "evidence_refs"}
            or item.get("status") not in {"passed", "finding", "blocked"}
            or not isinstance(item.get("summary"), str)
            or not str(item.get("summary") or "").strip()
            or not isinstance(item.get("evidence_refs"), list)
            or not item.get("evidence_refs")
            or any(
                not isinstance(value, str) or not value.strip()
                for value in item.get("evidence_refs", [])
            )
        ):
            errors.append("publication dimension evidence is incomplete")
            break

    findings = authored.get("findings")
    if not isinstance(findings, list):
        errors.append("publication findings must be a list")
        findings = []
    refs: list[str] = []
    for finding in findings:
        if not isinstance(finding, dict):
            errors.append("publication finding must be an object")
            continue
        required = {
            "finding_ref",
            "candidate_ref",
            "dimension",
            "summary",
            "scope_basis",
            "evidence_refs",
            "affected_artifacts",
            "route_class",
            "status",
            "closure_evidence",
        }
        if set(finding) != required:
            errors.append("publication finding fields are incomplete or unknown")
            continue
        refs.append(str(finding.get("finding_ref") or ""))
        if (
            finding.get("dimension") not in TASK_PUBLICATION_DIMENSIONS
            or finding.get("route_class")
            not in {"metadata_revision", "task_work", "external_blocker"}
            or finding.get("status") not in {"open", "closed"}
        ):
            errors.append("publication finding enum is invalid")
        textual_fields = ("summary", "scope_basis")
        list_fields = ("evidence_refs", "affected_artifacts")
        if any(
            not isinstance(finding.get(field), str)
            or not str(finding.get(field) or "").strip()
            for field in textual_fields
        ) or any(
            not isinstance(finding.get(field), list)
            or not finding.get(field)
            or any(
                not isinstance(value, str) or not value.strip()
                for value in finding.get(field, [])
            )
            for field in list_fields
        ):
            errors.append("publication finding evidence must be non-empty")
        closure = finding.get("closure_evidence")
        if (
            not isinstance(closure, list)
            or any(not isinstance(value, str) or not value.strip() for value in closure)
            or (finding.get("status") == "closed" and not closure)
            or (finding.get("status") == "open" and bool(closure))
        ):
            errors.append("publication finding closure evidence does not match status")
    if len(refs) != len(set(refs)) or any(not value for value in refs):
        errors.append("publication finding refs must be unique and non-empty")

    conclusions = authored.get("conclusions")
    if not isinstance(conclusions, dict) or set(conclusions) != {
        "issue_scope",
        "docs_ssot",
        "safety_deployment",
    }:
        errors.append("publication conclusions are incomplete")
        conclusions = {}
    for conclusion in conclusions.values():
        if (
            not isinstance(conclusion, dict)
            or set(conclusion) != {"status", "summary", "evidence_refs"}
            or conclusion.get("status") not in {"passed", "finding", "blocked"}
            or not isinstance(conclusion.get("summary"), str)
            or not str(conclusion.get("summary") or "").strip()
            or not isinstance(conclusion.get("evidence_refs"), list)
            or not conclusion.get("evidence_refs")
        ):
            errors.append("publication conclusion evidence is incomplete")
            break

    route = authored.get("route")
    typed_exit = route.get("typed_exit") if isinstance(route, dict) else None
    if typed_exit not in TASK_PUBLICATION_CONSUMERS:
        errors.append("publication route is invalid")
        return sorted(set(errors))
    expected_route_fields = (
        {"typed_exit", "reason_code", "remediation"}
        if typed_exit == "blocked"
        else {"typed_exit"}
    )
    if set(route) != expected_route_fields:
        errors.append("publication route fields are incomplete or unknown")

    dimension_statuses = {
        str(item.get("id")): str(item.get("status"))
        for item in dimensions
        if isinstance(item, dict)
    }
    open_findings = [
        item
        for item in findings
        if isinstance(item, dict) and item.get("status") == "open"
    ]
    for finding in open_findings:
        if dimension_statuses.get(str(finding.get("dimension") or "")) == "passed":
            errors.append(
                "open publication finding must reference a non-passed dimension"
            )
    open_finding_dimensions = {
        str(item.get("dimension") or "") for item in open_findings
    }
    if any(
        status != "passed" and dimension not in open_finding_dimensions
        for dimension, status in dimension_statuses.items()
    ):
        errors.append(
            "every non-passed publication dimension requires open finding evidence"
        )

    if typed_exit == "ready":
        if any(status != "passed" for status in dimension_statuses.values()):
            errors.append("ready requires every publication dimension to pass")
        if any(item.get("status") != "closed" for item in findings):
            errors.append("ready requires every publication finding to close")
        if any(item.get("status") != "passed" for item in conclusions.values()):
            errors.append("ready requires every publication conclusion to pass")
    elif typed_exit == "return_to_task_work":
        if not any(status == "finding" for status in dimension_statuses.values()):
            errors.append("return_to_task_work requires a finding publication dimension")
        if any(status == "blocked" for status in dimension_statuses.values()):
            errors.append("return_to_task_work cannot carry a blocked publication dimension")
        if not any(item.get("route_class") == "task_work" for item in open_findings):
            errors.append("return_to_task_work requires an open task_work finding")
        if any(
            item.get("route_class") != "task_work"
            or dimension_statuses.get(str(item.get("dimension") or "")) != "finding"
            for item in open_findings
        ):
            errors.append(
                "return_to_task_work open findings must reference finding dimensions"
            )
        if any(item.get("status") == "blocked" for item in conclusions.values()):
            errors.append(
                "return_to_task_work cannot carry a blocked publication conclusion"
            )
    else:
        if (
            not isinstance(route.get("reason_code"), str)
            or not str(route.get("reason_code") or "").strip()
            or not isinstance(route.get("remediation"), str)
            or not str(route.get("remediation") or "").strip()
        ):
            errors.append("blocked requires non-empty reason_code and remediation")
        if not any(status == "blocked" for status in dimension_statuses.values()):
            errors.append("blocked requires a blocked publication dimension")
        if not any(
            item.get("route_class") == "external_blocker"
            for item in open_findings
        ):
            errors.append("blocked requires an open external_blocker finding")
        if any(
            item.get("route_class") != "external_blocker"
            or dimension_statuses.get(str(item.get("dimension") or "")) != "blocked"
            for item in open_findings
        ):
            errors.append("blocked open findings must reference blocked dimensions")
        if not any(item.get("status") == "blocked" for item in conclusions.values()):
            errors.append("blocked requires a blocked publication conclusion")
    return sorted(set(errors))

def task_publication_closeout_preflight(
    root: Path,
    task_dir: Path,
    branch_review_commit: str,
    pr_payload: dict[str, Any],
) -> dict[str, Any]:
    """Run the exact side-effect-free Finalizer producer preflight."""
    config = load_config(root)
    task_context = load_task_runtime_identity(task_dir, config)
    assert_workspace_boundary(root, config, task_context, task_dir)
    args = argparse.Namespace(
        repo=None,
        remote=None,
        base_branch=None,
        title=None,
        include_finalization_gate=True,
    )
    return prepare_closeout(
        root,
        args,
        config,
        task_dir,
        task_context,
        publication_ready={
            "profile": "publication_ready",
            "mode": "workflow",
            "task_ref": repo_relative(root, task_dir),
            "branch_review_commit": branch_review_commit,
            "pr_title": pr_payload["title"],
            "pr_body": pr_payload["body"],
        },
        current_finalizer=True,
    )

def task_publication_check_errors(
    root: Path,
    task_dir: Path,
    payload: dict[str, Any],
    invocation_context: TaskPublicationInvocationContext | None = None,
) -> list[str]:
    errors = skill_json_schema_validation_errors(
        payload,
        task_publication_schema(root),
        "task publication readiness",
    )
    if payload.get("task_ref") != repo_relative(root, task_dir):
        errors.append("task publication task identity mismatch")
    route = payload.get("route") if isinstance(payload.get("route"), dict) else {}
    typed_exit = route.get("typed_exit")
    classifications = payload.get("candidate_classifications")
    classification_refs = [
        item.get("candidate_ref")
        for item in classifications
        if isinstance(item, dict)
    ] if isinstance(classifications, list) else []
    if (
        not classification_refs
        or len(classification_refs) != len(classifications)
        or len(set(classification_refs)) != len(classification_refs)
    ):
        errors.append("publication candidate classifications must be non-empty and unique")
    known_candidates = set(classification_refs)
    if any(
        not item.get("candidate_ref")
        or item.get("candidate_ref") not in known_candidates
        for item in payload.get("findings", [])
        if isinstance(item, dict)
    ):
        errors.append("publication findings must bind current classified candidates")
    branch_review_commit = str(payload.get("branch_review_commit") or "")
    reviewed_content_sha256 = str(payload.get("reviewed_content_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", branch_review_commit):
        errors.append("task publication branch_review_commit is invalid")
    else:
        continuity_errors = review_branch_content_continuity_errors(
            root,
            task_dir,
            branch_review_commit,
            reviewed_content_sha256,
            current_head(root),
        )
        errors.extend(
            "task publication reviewed content is stale: " + item
            for item in continuity_errors
            if not (
                typed_exit == "return_to_task_work"
                and item.startswith(BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX)
                and len(item) > len(BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX)
            )
        )
    if (
        typed_exit != "return_to_task_work"
        and payload.get("reviewed_content_sha256")
        != reviewed_content_identity(root)["sha256"]
    ):
        errors.append("task publication reviewed content identity is stale")
    invocation = {
        "task_ref": payload.get("task_ref"),
        "branch_review_commit": branch_review_commit,
        "pr_payload": copy.deepcopy(payload.get("pr_payload")),
    }
    if invocation_context is None:
        _, entry_errors, _, _ = task_publication_entry_precondition_bindings(
            root,
            task_dir,
            load_config(root),
            invocation,
        )
    else:
        _, entry_errors, _, _ = invocation_context.entry_bindings(invocation)
    if typed_exit == "ready":
        errors.extend(entry_errors)
        try:
            task_publication_closeout_preflight(
                root,
                task_dir,
                branch_review_commit,
                payload.get("pr_payload") or {},
            )
        except WorkflowError as exc:
            errors.append(f"finalizer_preflight:{exc}")
            errors.extend(
                f"finalizer_preflight:{item}"
                for item in exc.payload.get("errors", [])
                if isinstance(item, str)
            )
    errors.extend(
        task_publication_semantic_errors(
            payload,
            branch_review_commit=str(payload.get("branch_review_commit") or ""),
        )
    )
    return sorted(set(errors))

def cmd_record_task_publication_review(
    args: argparse.Namespace,
    invocation_context: TaskPublicationInvocationContext | None = None,
) -> dict[str, Any]:
    if invocation_context is None:
        root = repo_root(Path(args.root or os.getcwd()))
        config = load_config(root)
        task_dir = resolve_task_dir(root, args.task)
        task_context = load_task_runtime_identity(task_dir, config)
        assert_workspace_boundary(root, config, task_context, task_dir)
    else:
        invocation_context.assert_call(args.root, args.task)
        root = invocation_context.root
        config = invocation_context.config
        task_dir = invocation_context.task_dir
    authored = contract_wording_read_input(
        root,
        args.input,
        "guru-review-task-publication recorder",
    )
    path = task_publication_path(root, task_dir)
    profile = authored.get("profile")
    mode = authored.get("mode")
    review_intent = authored.get("review_intent")
    authoring_fields = {
        "profile",
        "mode",
        "review_intent",
        "pr_payload",
        "candidate_classifications",
        "dimensions",
        "findings",
        "conclusions",
        "route",
    }
    if profile == "publication_review_stale":
        authoring_fields.add("stale_reason")
    authoring_errors: list[str] = []
    if set(authored) != authoring_fields:
        authoring_errors.append(
            "publication authoring fields are incomplete or unknown"
        )
    if profile not in {"publication_review", "publication_review_stale"}:
        authoring_errors.append("publication profile is invalid")
    if mode not in {"workflow", "standalone"}:
        authoring_errors.append("publication mode is invalid")
    if review_intent not in {
        "initial_review",
        "metadata_revision_review",
        "stale_reentry_review",
    }:
        authoring_errors.append("publication review_intent is invalid")
    if profile == "publication_review_stale":
        if review_intent != "stale_reentry_review":
            authoring_errors.append(
                "stale publication requires stale_reentry_review intent"
            )
        if not isinstance(authored.get("stale_reason"), str) or not str(
            authored.get("stale_reason") or ""
        ).strip():
            authoring_errors.append(
                "stale publication requires non-empty stale_reason"
            )
    if authoring_errors:
        raise WorkflowError(
            "AI-authored task publication review is structurally invalid.",
            exit_code=2,
            payload={"error_codes": sorted(set(authoring_errors))},
        )
    invocation = {
        "profile": profile,
        "mode": mode,
        "review_intent": review_intent,
        "stale_reason": authored.get("stale_reason"),
        "task_ref": repo_relative(root, task_dir),
        "branch_review_commit": str(
            getattr(args, "branch_review_commit", "") or ""
        ),
        "pr_payload": copy.deepcopy(authored.get("pr_payload")),
    }
    if invocation_context is None:
        entry_bindings, entry_errors, review_gate, repository = (
            task_publication_entry_precondition_bindings(
                root,
                task_dir,
                config,
                invocation,
            )
        )
    else:
        entry_bindings, entry_errors, review_gate, repository = (
            invocation_context.entry_bindings(invocation)
        )
    route = authored.get("route") if isinstance(authored.get("route"), dict) else {}
    typed_exit = route.get("typed_exit")
    if entry_errors and typed_exit == "ready":
        raise WorkflowError(
            "Ready task publication entry preconditions are missing, stale, or incomplete.",
            exit_code=2,
            payload={
                "task_ref": repo_relative(root, task_dir),
                "error_codes": entry_errors,
            },
        )
    branch_review_commit = str(invocation["branch_review_commit"])
    reviewed_content_sha256 = reviewed_content_identity(root)["sha256"]
    if typed_exit == "return_to_task_work":
        reviewed_content_sha256 = reviewed_content_identity(
            root,
            branch_review_commit,
            include_worktree=False,
        )["sha256"]
    payload: dict[str, Any] = {
        "schema_version": "5.0",
        "skill_id": TASK_PUBLICATION_SKILL_ID,
        "task_ref": repo_relative(root, task_dir),
        "branch_review_commit": branch_review_commit,
        "reviewed_content_sha256": reviewed_content_sha256,
        "pr_payload": copy.deepcopy(authored.get("pr_payload")),
        "candidate_classifications": copy.deepcopy(authored.get("candidate_classifications")),
        "dimensions": copy.deepcopy(authored.get("dimensions")),
        "findings": copy.deepcopy(authored.get("findings")),
        "conclusions": copy.deepcopy(authored.get("conclusions")),
        "route": copy.deepcopy(route),
    }
    errors = task_publication_check_errors(
        root,
        task_dir,
        payload,
        invocation_context,
    )
    if errors:
        raise WorkflowError(
            "Task publication readiness materialization failed validation.",
            exit_code=2,
            payload={"error_codes": errors},
        )
    if not args.dry_run:
        write_json(path, payload)
    if invocation_context is not None:
        invocation_context.checked_owner_result = copy.deepcopy(payload)
        invocation_context.count("semantic.record")
        invocation_context.count("objective.check")
    return {
        **payload,
        "artifact_path": str(path),
        "dry_run": bool(args.dry_run),
    }

def cmd_check_task_publication_review(
    args: argparse.Namespace,
    invocation_context: TaskPublicationInvocationContext | None = None,
) -> dict[str, Any]:
    if invocation_context is None:
        root = repo_root(Path(args.root or os.getcwd()))
        config = load_config(root)
        task_dir = resolve_task_dir(root, args.task)
        task_context = load_task_runtime_identity(task_dir, config)
        assert_workspace_boundary(root, config, task_context, task_dir)
    else:
        invocation_context.assert_call(args.root, args.task)
        root = invocation_context.root
        task_dir = invocation_context.task_dir
    path = task_publication_path(root, task_dir)
    if not path.is_file() or path.is_symlink():
        raise WorkflowError(
            "Task publication readiness artifact is missing or unsafe.",
            exit_code=2,
        )
    payload = read_json(path)
    if (
        invocation_context is not None
        and invocation_context.checked_owner_result == payload
    ):
        errors: list[str] = []
        invocation_context.count("checkpoint.verify")
    else:
        errors = task_publication_check_errors(
            root,
            task_dir,
            payload,
            invocation_context,
        )
    expected_exit = str(getattr(args, "expected_exit", "") or "")
    typed_exit = (payload.get("route") or {}).get("typed_exit")
    if expected_exit and typed_exit != expected_exit:
        errors.append("task publication expected exit mismatch")
    if errors:
        raise WorkflowError(
            "Task publication readiness is missing, stale, or incomplete.",
            exit_code=2,
            payload={"artifact_path": str(path), "errors": sorted(set(errors))},
        )
    return {
        "status": "ok",
        "artifact_path": str(path),
        "task_dir": str(task_dir),
        "task_ref": payload["task_ref"],
        "branch_review_commit": payload["branch_review_commit"],
        "typed_exit": typed_exit,
        "owner_result": payload,
    }

def task_commit_index_identity(
    root: Path, path: str, git_env: dict[str, str] | None = None
) -> tuple[str | None, str | None]:
    proc = subprocess.run(
        ["git", "--literal-pathspecs", "ls-files", "-s", "-z", "--", path],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=None if git_env is None else {**os.environ, **git_env},
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not read the literal task commit index identity.",
            exit_code=2,
            payload={"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    records = [record for record in proc.stdout.split(b"\0") if record]
    if not records:
        return None, None
    if len(records) != 1:
        raise WorkflowError("Task commit index identity is ambiguous for a literal path.", exit_code=2)
    metadata_raw, separator, record_path = records[0].partition(b"\t")
    if not separator or record_path.decode("utf-8", "strict") != path:
        raise WorkflowError("Task commit index identity did not return the exact literal path.", exit_code=2)
    metadata = metadata_raw.decode("ascii", "strict").split()
    if len(metadata) != 3 or metadata[2] != "0":
        raise WorkflowError("Task commit index identity has an invalid or unmerged record.", exit_code=2)
    return metadata[1], metadata[0]

def task_commit_gitlink_worktree_identity(root: Path, path: str) -> dict[str, Any]:
    target = root / path
    try:
        metadata = target.lstat()
    except FileNotFoundError as exc:
        raise WorkflowError(
            "Task commit gitlink worktree is not initialized.", exit_code=2
        ) from exc
    if not stat.S_ISDIR(metadata.st_mode):
        raise WorkflowError(
            "Task commit gitlink worktree is not an exact directory.", exit_code=2
        )

    top_proc = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "--show-toplevel"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    top_value = top_proc.stdout.decode("utf-8", "strict").rstrip("\n") if top_proc.returncode == 0 else ""
    try:
        exact_root = target.resolve(strict=True)
        reported_root = Path(top_value).resolve(strict=True) if top_value else None
    except (OSError, RuntimeError) as exc:
        raise WorkflowError(
            "Task commit gitlink worktree root is ambiguous.", exit_code=2
        ) from exc
    if top_proc.returncode != 0 or reported_root != exact_root:
        raise WorkflowError(
            "Task commit gitlink worktree is uninitialized or root-mismatched.", exit_code=2
        )

    head_proc = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "--verify", "HEAD^{commit}"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    head = head_proc.stdout.decode("ascii", "strict").strip() if head_proc.returncode == 0 else ""
    if head_proc.returncode != 0 or re.fullmatch(r"[0-9a-f]{40,64}", head) is None:
        raise WorkflowError(
            "Task commit gitlink worktree HEAD is missing or ambiguous.", exit_code=2
        )

    status_proc = subprocess.run(
        [
            "git", "-C", str(target), "status", "--porcelain=v1", "-z",
            "--untracked-files=all", "--ignore-submodules=none",
        ],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if status_proc.returncode != 0:
        raise WorkflowError(
            "Could not inspect the task commit gitlink worktree state.", exit_code=2
        )
    if status_proc.stdout:
        raise WorkflowError(
            "Task commit gitlink worktree must be clean before candidate capture.", exit_code=2
        )
    return {
        "gitlink_head": head,
        "gitlink_initialized": True,
        "gitlink_dirty": False,
    }

def task_commit_worktree_content(
    root: Path, path: str
) -> tuple[bytes | None, str | None, str | None]:
    target = root / path
    try:
        metadata = target.lstat()
    except FileNotFoundError:
        return None, None, None
    if stat.S_ISLNK(metadata.st_mode):
        content = os.fsencode(os.readlink(target))
        return content, hashlib.sha256(content).hexdigest(), "120000"
    if not stat.S_ISREG(metadata.st_mode):
        return None, None, None
    mode = "100755" if metadata.st_mode & stat.S_IXUSR else "100644"
    content = target.read_bytes()
    return content, hashlib.sha256(content).hexdigest(), mode

def task_commit_worktree_identity(root: Path, path: str) -> tuple[str | None, str | None]:
    _, content_sha256, mode = task_commit_worktree_content(root, path)
    return content_sha256, mode

def task_commit_porcelain_status_records(root: Path) -> list[dict[str, Any]]:
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not capture the task commit Git snapshot.",
            exit_code=2,
            payload={"stderr": proc.stderr.decode("utf-8", "replace")},
        )
    fields = proc.stdout.split(b"\0")
    records: list[dict[str, Any]] = []
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if not field:
            continue
        if len(field) < 4:
            raise WorkflowError("Git returned an invalid porcelain status record.", exit_code=2)
        status_text = field[:2].decode("ascii", "strict")
        if status_text in {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}:
            raise WorkflowError(
                "Reviewed Git state contains an unresolved merge entry.",
                exit_code=2,
            )
        path = field[3:].decode("utf-8", "strict")
        renamed_from: str | None = None
        copied_from: str | None = None
        relation_kinds = {item for item in status_text if item in {"R", "C"}}
        if len(relation_kinds) > 1:
            raise WorkflowError(
                "Git returned an ambiguous rename/copy status record.", exit_code=2
            )
        if relation_kinds:
            if index >= len(fields) or not fields[index]:
                raise WorkflowError(
                    "Git returned an incomplete rename/copy status record.", exit_code=2
                )
            relation_source = fields[index].decode("utf-8", "strict")
            index += 1
            if relation_kinds == {"R"}:
                renamed_from = relation_source
            else:
                copied_from = relation_source
        records.append({
            "status_text": status_text,
            "path": path,
            "renamed_from": renamed_from,
            "copied_from": copied_from,
        })
    return records

def task_commit_snapshot_entry(
    root: Path,
    record: dict[str, Any],
) -> dict[str, Any]:
    status_text = str(record["status_text"])
    path = str(record["path"])
    index_status = "" if status_text[0] == " " else status_text[0]
    worktree_status = "" if status_text[1] == " " else status_text[1]
    untracked = status_text == "??"
    index_blob, index_mode = task_commit_index_identity(root, path)
    worktree_sha256, worktree_mode = task_commit_worktree_identity(root, path)
    deleted = "D" in status_text
    entry = {
        "path": path,
        "index_status": index_status,
        "worktree_status": worktree_status,
        "untracked": untracked,
        "deleted": deleted,
        "renamed_from": record.get("renamed_from"),
        "copied_from": record.get("copied_from"),
        "index_blob": index_blob,
        "worktree_sha256": worktree_sha256,
        "mode": worktree_mode or index_mode,
    }
    if index_mode == "160000":
        if deleted and not (root / path).exists():
            entry.update(
                {
                    "gitlink_head": None,
                    "gitlink_initialized": False,
                    "gitlink_dirty": None,
                }
            )
        else:
            entry.update(task_commit_gitlink_worktree_identity(root, path))
    return entry

def closeout_reviewed_change_facts(
    root: Path,
    task_context: dict[str, Any],
    branch_review_commit: str,
) -> dict[str, Any]:
    """Rebuild one reviewed-path fact set for closeout and its projections."""
    base_head = str(task_context.get("base_head_sha") or "").strip()
    if re.fullmatch(r"[0-9a-f]{40}", base_head) is None:
        raise WorkflowError(
            "Closeout reviewed paths require the pinned task base commit.",
            exit_code=2,
        )
    proc = run(
        ["git", "diff", "--name-only", f"{base_head}...{branch_review_commit}"],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not rebuild closeout reviewed paths from the pinned task base.",
            exit_code=2,
            payload={
                "base_head": base_head,
                "branch_review_commit": branch_review_commit,
                "stderr": proc.stderr.strip(),
            },
        )
    changed_paths = sorted(
        {
            path.strip()
            for path in proc.stdout.splitlines()
            if path.strip()
        }
    )
    return {"changed_paths": changed_paths}

def provenance_tail_flatten_manifest(value: Any, prefix: str = "") -> dict[str, Any]:
    """Return deterministic dotted paths for the manifest field-diff contract."""
    if isinstance(value, dict):
        flattened: dict[str, Any] = (
            {prefix: PROVENANCE_TAIL_OBJECT_PRESENCE}
            if prefix
            else {}
        )
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else str(key)
            flattened.update(provenance_tail_flatten_manifest(value[key], child))
        return flattened
    return {prefix: value}

def provenance_tail_manifest_field_diff(
    before: Any,
    after: Any,
) -> list[str]:
    before_flat = provenance_tail_flatten_manifest(before)
    after_flat = provenance_tail_flatten_manifest(after)
    return sorted(
        [
            path
            for path in set(before_flat) | set(after_flat)
            if (
                path not in before_flat
                or path not in after_flat
                or before_flat[path] != after_flat[path]
            )
        ],
        key=lambda item: item.encode("utf-8"),
    )

def provenance_tail_safe_file_action_transition(
    before: Any,
    after: Any,
    container: str,
) -> bool:
    """Accept only an ordered installed-to-unchanged files transition."""
    if container not in PROVENANCE_TAIL_FILE_ACTION_CONTAINERS:
        return False
    if not isinstance(before, dict) or not isinstance(after, dict):
        return False
    section_name, field_name = container.split(".", 1)
    before_section = before.get(section_name)
    after_section = after.get(section_name)
    if not isinstance(before_section, dict) or not isinstance(after_section, dict):
        return False
    before_files = before_section.get(field_name)
    after_files = after_section.get(field_name)
    if not isinstance(before_files, list) or not isinstance(after_files, list):
        return False
    if len(before_files) != len(after_files):
        return False
    for before_item, after_item in zip(before_files, after_files):
        if not isinstance(before_item, dict) or not isinstance(after_item, dict):
            return False
        if before_item.get("action") != "installed":
            return False
        if after_item.get("action") != "unchanged":
            return False
        before_identity = dict(before_item)
        after_identity = dict(after_item)
        before_identity.pop("action", None)
        after_identity.pop("action", None)
        try:
            before_bytes = json.dumps(
                before_identity,
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            after_bytes = json.dumps(
                after_identity,
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        except (TypeError, ValueError):
            return False
        if before_bytes != after_bytes:
            return False
    return True

def provenance_tail_manifest_errors(
    before: Any,
    after: Any,
    reviewed_content_head: str,
) -> list[str]:
    """Validate the only manifest mutation allowed after reviewed content."""
    errors: list[str] = []
    if not isinstance(before, dict) or not isinstance(after, dict):
        return ["provenance_tail_manifest_invalid"]
    if re.fullmatch(r"[0-9a-f]{40}", str(reviewed_content_head or "")) is None:
        errors.append("provenance_tail_reviewed_head_invalid")
    changed = provenance_tail_manifest_field_diff(before, after)
    unexpected = set(changed) - PROVENANCE_TAIL_ALLOWED_FIELDS
    for container in PROVENANCE_TAIL_FILE_ACTION_CONTAINERS:
        if (
            container in unexpected
            and provenance_tail_safe_file_action_transition(
                before,
                after,
                container,
            )
        ):
            unexpected.remove(container)
    unexpected = sorted(unexpected, key=lambda item: item.encode("utf-8"))
    if unexpected:
        errors.append("provenance_tail_manifest_fields_outside_allowlist")
    source = after.get("source")
    if not isinstance(source, dict):
        errors.append("provenance_tail_source_missing")
    else:
        if source.get("ref") != reviewed_content_head:
            errors.append("provenance_tail_source_ref_mismatch")
        if source.get("commit") != reviewed_content_head:
            errors.append("provenance_tail_source_commit_mismatch")
        if source.get("tree_state") != "clean":
            errors.append("provenance_tail_source_not_clean")
        if source.get("is_mutable_ref") is not False:
            errors.append("provenance_tail_source_ref_mutable")
    if "installed_at" in after and not isinstance(after["installed_at"], str):
        errors.append("provenance_tail_installed_at_invalid")
    return sorted(set(errors))

def provenance_tail_commit_errors(
    root: Path,
    reviewed_content_head: str,
    publication_head: str,
    *,
    require_current: bool = True,
) -> list[str]:
    """Validate one committed provenance tail and its reviewed/publication identities."""
    errors: list[str] = []
    if re.fullmatch(r"[0-9a-f]{40}", str(publication_head or "")) is None:
        errors.append("provenance_tail_publication_head_invalid")
        return sorted(set(errors))
    if require_current and publication_head != current_head(root):
        errors.append("provenance_tail_publication_head_not_current")
    parent_proc = run(
        ["git", "show", "-s", "--format=%P", publication_head],
        cwd=root,
        check=False,
    )
    parents = parent_proc.stdout.split() if parent_proc.returncode == 0 else []
    if parents != [reviewed_content_head]:
        errors.append("provenance_tail_parent_mismatch")
    changed_proc = run(
        [
            "git",
            "diff-tree",
            "--root",
            "--no-commit-id",
            "--name-only",
            "--no-renames",
            "-r",
            "-z",
            publication_head,
        ],
        cwd=root,
        check=False,
    )
    changed = {
        item for item in changed_proc.stdout.split("\0") if item
    } if changed_proc.returncode == 0 else set()
    if changed != {PROVENANCE_TAIL_MANIFEST_PATH}:
        errors.append("provenance_tail_changed_paths_invalid")
    if not errors:
        before_proc = run(
            ["git", "show", f"{publication_head}^:{PROVENANCE_TAIL_MANIFEST_PATH}"],
            cwd=root,
            check=False,
        )
        after_proc = run(
            ["git", "show", f"{publication_head}:{PROVENANCE_TAIL_MANIFEST_PATH}"],
            cwd=root,
            check=False,
        )
        try:
            before = json.loads(before_proc.stdout)
            after = json.loads(after_proc.stdout)
        except (json.JSONDecodeError, TypeError):
            errors.append("provenance_tail_manifest_unreadable")
        else:
            errors.extend(
                provenance_tail_manifest_errors(before, after, reviewed_content_head)
            )
    return sorted(set(errors))

def finalizer_publication_identity(
    root: Path,
    reviewed_content_head: str,
) -> dict[str, Any]:
    """Project the reviewed head and the optional single provenance tail."""
    if re.fullmatch(r"[0-9a-f]{40}", str(reviewed_content_head or "")) is None:
        raise WorkflowError("Finalizer reviewed_content_head is invalid.", exit_code=2)
    publication_head = current_head(root)
    if publication_head == reviewed_content_head:
        return {
            "reviewed_content_head": reviewed_content_head,
            "publication_head": publication_head,
            "metadata_tail": None,
        }
    if not is_ancestor(root, reviewed_content_head, publication_head):
        raise WorkflowError(
            "Finalizer publication head is not a descendant of reviewed content.",
            exit_code=2,
        )
    errors = provenance_tail_commit_errors(root, reviewed_content_head, publication_head)
    if errors == ["provenance_tail_changed_paths_invalid"]:
        # Existing task/archive metadata commits are excluded from reviewed
        # content and are not provenance tails; keep their historical behavior.
        paths_proc = run(
            [
                "git", "diff-tree", "--no-commit-id", "--name-only", "--no-renames",
                "-r", "-z", publication_head,
            ],
            cwd=root,
            check=False,
        )
        paths = {item for item in paths_proc.stdout.split("\0") if item}
        if (
            paths
            and PROVENANCE_TAIL_MANIFEST_PATH not in paths
            and all(reviewed_content_metadata_path(path) for path in paths)
        ):
            return {
                "reviewed_content_head": reviewed_content_head,
                "publication_head": publication_head,
                "metadata_tail": None,
            }
    if errors:
        raise WorkflowError(
            "Finalizer publication head contains an invalid provenance tail.",
            exit_code=2,
            payload={"errors": errors},
        )
    return {
        "reviewed_content_head": reviewed_content_head,
        "publication_head": publication_head,
        "metadata_tail": {
            "commit": publication_head,
            "parent": reviewed_content_head,
            "path": PROVENANCE_TAIL_MANIFEST_PATH,
        },
    }

def skill_safe_relative(value: Any) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    path = Path(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    return path

def skill_lexical_relative(boundary: Path, path: Path) -> Path | None:
    boundary_abs = Path(os.path.abspath(boundary))
    path_abs = Path(os.path.abspath(path))
    try:
        relative = path_abs.relative_to(boundary_abs)
    except ValueError:
        return None
    if not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        return None
    return relative

def skill_lstat_path(
    boundary: Path,
    path: Path,
    label: str,
    errors: list[str],
    *,
    kind: str,
    required: bool = True,
) -> os.stat_result | None:
    boundary_abs = Path(os.path.abspath(boundary))
    path_abs = Path(os.path.abspath(path))
    if path_abs == boundary_abs:
        try:
            current_stat = boundary_abs.lstat()
        except FileNotFoundError:
            if required:
                errors.append(f"missing {label}")
            return None
        except OSError:
            errors.append(f"{label} cannot be inspected")
            return None
        if stat.S_ISLNK(current_stat.st_mode):
            errors.append(f"{label} contains a symlink component")
            return None
        if kind == "file" and not stat.S_ISREG(current_stat.st_mode):
            errors.append(f"{label} is not a regular file")
            return None
        if kind == "directory" and not stat.S_ISDIR(current_stat.st_mode):
            errors.append(f"{label} is not a directory")
            return None
        return current_stat
    relative = skill_lexical_relative(boundary, path)
    if relative is None:
        errors.append(f"{label} is outside its lexical boundary")
        return None
    current = Path(os.path.abspath(boundary))
    for index, part in enumerate(relative.parts):
        current /= part
        try:
            current_stat = current.lstat()
        except FileNotFoundError:
            if required:
                errors.append(f"missing {label}")
            return None
        except OSError:
            errors.append(f"{label} cannot be inspected")
            return None
        if stat.S_ISLNK(current_stat.st_mode):
            errors.append(f"{label} contains a symlink component")
            return None
        if index < len(relative.parts) - 1 and not stat.S_ISDIR(current_stat.st_mode):
            errors.append(f"{label} has a non-directory ancestor")
            return None
    if kind == "file" and not stat.S_ISREG(current_stat.st_mode):
        errors.append(f"{label} is not a regular file")
        return None
    if kind == "directory" and not stat.S_ISDIR(current_stat.st_mode):
        errors.append(f"{label} is not a directory")
        return None
    return current_stat

def skill_read_schema(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    payload = skill_read_json(path, label, errors)
    if payload is None:
        return None
    if not isinstance(payload.get("type"), str) and not any(
        key in payload for key in ("$ref", "oneOf", "anyOf", "allOf")
    ):
        errors.append(f"{label} is not a recognizable JSON schema")
    schema_uri = payload.get("$schema")
    if schema_uri is not None and schema_uri not in {
        "https://json-schema.org/draft/2020-12/schema",
        "http://json-schema.org/draft-07/schema#",
    }:
        errors.append(f"{label} declares an unsupported JSON schema dialect")
    return payload

def skill_json_loads(value: str) -> Any:
    def reject_constant(constant: str) -> Any:
        raise ValueError(f"non-standard JSON constant: {constant}")

    def parse_finite_float(number: str) -> float:
        parsed = float(number)
        if not math.isfinite(parsed):
            raise ValueError("JSON number is outside the finite runtime range")
        return parsed

    return json.loads(
        value,
        parse_constant=reject_constant,
        parse_float=parse_finite_float,
    )

def skill_json_nonfinite_paths(value: Any, path: str = "$") -> list[str]:
    if isinstance(value, float) and not math.isfinite(value):
        return [path]
    if isinstance(value, list):
        return [
            child_path
            for index, item in enumerate(value)
            for child_path in skill_json_nonfinite_paths(item, f"{path}[{index}]")
        ]
    if isinstance(value, dict):
        return [
            child_path
            for key, item in value.items()
            for child_path in skill_json_nonfinite_paths(item, f"{path}.{key}")
        ]
    return []

def skill_rfc3339_date_time_matches(value: str) -> bool:
    matched = re.fullmatch(
        r"(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
        r"[Tt](?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"
        r"(?:\.[0-9]+)?(?P<zone>[Zz]|[+-][0-9]{2}:[0-9]{2})",
        value,
    )
    if matched is None:
        return False
    values = {key: int(matched.group(key)) for key in (
        "year", "month", "day", "hour", "minute", "second",
    )}
    zone = matched.group("zone")
    if (
        values["hour"] > 23
        or values["minute"] > 59
        or values["second"] > 60
    ):
        return False

    def leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    month_lengths = [
        31,
        29 if leap_year(values["year"]) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    if (
        values["month"] < 1
        or values["month"] > 12
        or values["day"] < 1
        or values["day"] > month_lengths[values["month"] - 1]
    ):
        return False

    if zone.lower() == "z":
        offset_minutes = 0
    else:
        offset_hour = int(zone[1:3])
        offset_minute = int(zone[4:6])
        if offset_hour > 23 or offset_minute > 59:
            return False
        sign = 1 if zone[0] == "+" else -1
        offset_minutes = sign * (offset_hour * 60 + offset_minute)
    if values["second"] != 60:
        return True

    def days_before_year(year: int) -> int:
        # RFC 3339 includes year 0000; count proleptic Gregorian years [0, year).
        return (
            365 * year
            + (year + 3) // 4
            - (year + 99) // 100
            + (year + 399) // 400
        )

    def day_ordinal(year: int, month: int, day: int) -> int:
        lengths = [
            31,
            29 if leap_year(year) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ]
        return days_before_year(year) + sum(lengths[:month - 1]) + day - 1

    local_day = day_ordinal(values["year"], values["month"], values["day"])
    utc_minutes = (
        local_day * 24 * 60
        + values["hour"] * 60
        + values["minute"]
        - offset_minutes
    )
    utc_day, utc_minute = divmod(utc_minutes, 24 * 60)
    if utc_minute != 23 * 60 + 59:
        return False
    return any(
        utc_day == day_ordinal(year, month, day)
        for year in range(max(0, values["year"] - 1), min(9999, values["year"] + 1) + 1)
        for month, day in ((6, 30), (12, 31))
    )

def skill_uri_matches(value: str) -> bool:
    if not value or any(ord(character) < 0x21 or ord(character) > 0x7E for character in value):
        return False
    matched = re.match(r"(?P<scheme>[A-Za-z][A-Za-z0-9+.-]*):", value)
    if matched is None:
        return False
    remainder = value[matched.end():]

    unreserved = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")
    sub_delimiters = set("!$&'()*+,;=")

    def component_matches(component: str, extra: str = "") -> bool:
        allowed = unreserved | sub_delimiters | set(extra)
        index = 0
        while index < len(component):
            character = component[index]
            if character == "%":
                if (
                    index + 2 >= len(component)
                    or re.fullmatch(r"[0-9A-Fa-f]{2}", component[index + 1:index + 3]) is None
                ):
                    return False
                index += 3
                continue
            if character not in allowed:
                return False
            index += 1
        return True

    if remainder.count("#") > 1:
        return False
    hierarchy_and_query, separator, fragment = remainder.partition("#")
    if separator and not component_matches(fragment, ":@/?"):
        return False
    hierarchy, query_separator, query = hierarchy_and_query.partition("?")
    if query_separator and not component_matches(query, ":@/?"):
        return False

    authority: str | None = None
    path = hierarchy
    if hierarchy.startswith("//"):
        authority_and_path = hierarchy[2:]
        authority, path_separator, path_tail = authority_and_path.partition("/")
        path = f"/{path_tail}" if path_separator else ""
    if not component_matches(path, ":@/"):
        return False
    if authority is None:
        return True

    if authority.count("@") > 1:
        return False
    userinfo, at, host_and_port = authority.rpartition("@")
    if not at:
        host_and_port = authority
    elif not component_matches(userinfo, ":"):
        return False

    if host_and_port.startswith("["):
        closing = host_and_port.find("]")
        if closing < 0:
            return False
        literal = host_and_port[1:closing]
        suffix = host_and_port[closing + 1:]
        if suffix and (
            not suffix.startswith(":")
            or suffix[1:] and not suffix[1:].isdigit()
        ):
            return False
        if re.fullmatch(r"[Vv][0-9A-Fa-f]+\.[A-Za-z0-9._~!$&'()*+,;=:-]+", literal) is None:
            if "%" in literal:
                return False
            try:
                ipaddress.IPv6Address(literal)
            except ValueError:
                return False
        return True

    if host_and_port.count(":") > 1:
        return False
    host, colon, port = host_and_port.rpartition(":")
    if not colon:
        host = host_and_port
    elif port and not port.isdigit():
        return False
    return component_matches(host)

def skill_format_matches(value: str, expected: str) -> bool:
    if expected == "date-time":
        return skill_rfc3339_date_time_matches(value)
    if expected == "uri":
        return skill_uri_matches(value)
    return False

def skill_read_json(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = skill_json_loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing {label}")
        return None
    except OSError:
        errors.append(f"unreadable {label}")
        return None
    except (UnicodeDecodeError, ValueError):
        errors.append(f"invalid JSON in {label}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{label} root must be an object")
        return None
    return payload

def skill_json_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right
    if type(left) is not type(right):
        return False
    if isinstance(left, list):
        return len(left) == len(right) and all(
            skill_json_equal(left_item, right_item)
            for left_item, right_item in zip(left, right)
        )
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            skill_json_equal(left[key], right[key]) for key in left
        )
    return left == right

SKILL_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"

TASK_PUBLICATION_SKILL_ID = "guru-review-task-publication"

SKILL_ECMA_WHITESPACE_CLASS = (
    r"\u0009-\u000d\u0020\u00a0\u1680\u2000-\u200a"
    r"\u2028\u2029\u202f\u205f\u3000\ufeff"
)

SKILL_UTF16_HIGH_SURROGATE = r"[\ud800-\udbff]"

SKILL_UTF16_LOW_SURROGATE = r"[\udc00-\udfff]"

SKILL_UTF16_SURROGATE_PAIR = r"[\ud800-\udbff][\udc00-\udfff]"

def skill_ecma_code_point_complement(excluded_class: str) -> str:
    """Match one ECMA Unicode code point outside a BMP-only character class."""

    return (
        rf"(?:{SKILL_UTF16_SURROGATE_PAIR}|"
        rf"(?!{SKILL_UTF16_SURROGATE_PAIR})"
        rf"(?:(?<!{SKILL_UTF16_HIGH_SURROGATE})(?={SKILL_UTF16_LOW_SURROGATE})|"
        rf"(?!{SKILL_UTF16_LOW_SURROGATE}))[^{excluded_class}])"
    )

SKILL_ECMA_DOT_PATTERN = skill_ecma_code_point_complement(r"\n\r\u2028\u2029")

class SkillPortablePatternError(ValueError):
    pass

def skill_utf16_code_units(value: str) -> str:
    """Project a Python Unicode string onto JavaScript UTF-16 code units."""

    encoded = value.encode("utf-16-le", errors="surrogatepass")
    return "".join(
        chr(encoded[position] | encoded[position + 1] << 8)
        for position in range(0, len(encoded), 2)
    )

class SkillPortablePattern:
    def __init__(self, compiled: re.Pattern[str]):
        self._compiled = compiled

    @property
    def pattern(self) -> str:
        return self._compiled.pattern

    def search(self, value: str) -> re.Match[str] | None:
        return self._compiled.search(skill_utf16_code_units(value))
