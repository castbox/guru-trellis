def skill_json_schema_validation_errors(
    instance: Any,
    schema: dict[str, Any],
    label: str,
) -> list[str]:
    errors = skill_json_schema_subset_errors(schema, label)
    if errors:
        return errors
    nonfinite_paths = skill_json_nonfinite_paths(instance)
    if nonfinite_paths:
        return [
            f"{label} contains a non-finite number at {path}"
            for path in nonfinite_paths
        ]
    active_references: set[str] = set()

    def resolve_ref(reference: Any, output: list[str], path: str) -> dict[str, Any] | None:
        if not isinstance(reference, str) or not reference.startswith("#/"):
            output.append(f"{label} schema has an unsupported reference at {path}")
            return None
        target: Any = schema
        for encoded_part in reference[2:].split("/"):
            part = encoded_part.replace("~1", "/").replace("~0", "~")
            if not isinstance(target, dict) or part not in target:
                output.append(f"{label} schema has an unresolved reference at {path}")
                return None
            target = target[part]
        if not isinstance(target, dict):
            output.append(f"{label} schema reference does not resolve to an object at {path}")
            return None
        return target

    def type_matches(value: Any, expected: str) -> bool:
        if expected == "object":
            return isinstance(value, dict)
        if expected == "array":
            return isinstance(value, list)
        if expected == "string":
            return isinstance(value, str)
        if expected == "boolean":
            return isinstance(value, bool)
        if expected == "null":
            return value is None
        if expected == "integer":
            return (
                isinstance(value, int) and not isinstance(value, bool)
            ) or (
                isinstance(value, float) and math.isfinite(value) and value.is_integer()
            )
        if expected == "number":
            return (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and (not isinstance(value, float) or math.isfinite(value))
            )
        return False

    def validate(value: Any, node: Any, path: str, output: list[str]) -> None:
        if not isinstance(node, dict):
            output.append(f"{label} schema node is not an object at {path}")
            return
        if "$ref" in node:
            reference = node.get("$ref")
            target = resolve_ref(reference, output, path)
            if target is not None and isinstance(reference, str):
                if reference in active_references:
                    output.append(f"{label} schema has a recursive reference at {path}")
                else:
                    active_references.add(reference)
                    try:
                        validate(value, target, path, output)
                    finally:
                        active_references.remove(reference)
        all_options = node.get("allOf")
        if all_options is not None:
            if not isinstance(all_options, list) or not all_options:
                output.append(f"{label} schema has an invalid allOf at {path}")
            else:
                for option in all_options:
                    validate(value, option, path, output)
        any_options = node.get("anyOf")
        if any_options is not None:
            if not isinstance(any_options, list) or not any_options:
                output.append(f"{label} schema has an invalid anyOf at {path}")
            else:
                branch_results: list[list[str]] = []
                for option in any_options:
                    branch_errors: list[str] = []
                    validate(value, option, path, branch_errors)
                    branch_results.append(branch_errors)
                if not any(not branch_errors for branch_errors in branch_results):
                    output.append(f"{label} violates anyOf at {path}")
        options = node.get("oneOf")
        if options is not None:
            if not isinstance(options, list) or not options:
                output.append(f"{label} schema has an invalid oneOf at {path}")
                return
            matches = 0
            for option in options:
                branch_errors: list[str] = []
                validate(value, option, path, branch_errors)
                if not branch_errors:
                    matches += 1
            if matches != 1:
                output.append(f"{label} violates oneOf at {path}")

        negated = node.get("not")
        if negated is not None:
            negated_errors: list[str] = []
            validate(value, negated, path, negated_errors)
            if not negated_errors:
                output.append(f"{label} violates not at {path}")

        condition = node.get("if")
        if condition is not None:
            condition_errors: list[str] = []
            validate(value, condition, path, condition_errors)
            branch = node.get("then") if not condition_errors else node.get("else")
            if branch is not None:
                validate(value, branch, path, output)

        expected_type = node.get("type")
        if expected_type is not None:
            expected_types = (
                [expected_type]
                if isinstance(expected_type, str)
                else expected_type
                if isinstance(expected_type, list)
                else []
            )
            if (
                not expected_types
                or any(not isinstance(item, str) for item in expected_types)
                or not any(type_matches(value, item) for item in expected_types)
            ):
                output.append(f"{label} has wrong type at {path}")
                return
        if "const" in node and not skill_json_equal(value, node.get("const")):
            output.append(f"{label} violates const at {path}")
        enum = node.get("enum")
        if enum is not None:
            if not isinstance(enum, list) or not any(skill_json_equal(value, item) for item in enum):
                output.append(f"{label} violates enum at {path}")

        if isinstance(value, str):
            minimum = node.get("minLength")
            if isinstance(minimum, int) and len(value) < minimum:
                output.append(f"{label} is shorter than minLength at {path}")
            maximum = node.get("maxLength")
            if isinstance(maximum, int) and len(value) > maximum:
                output.append(f"{label} is longer than maxLength at {path}")
            pattern = node.get("pattern")
            if isinstance(pattern, str):
                try:
                    pattern_matches = skill_compile_portable_pattern(pattern).search(value) is not None
                except SkillPortablePatternError:
                    pattern_matches = False
                if not pattern_matches:
                    output.append(f"{label} violates pattern at {path}")
            expected_format = node.get("format")
            if isinstance(expected_format, str) and not skill_format_matches(value, expected_format):
                output.append(f"{label} violates format at {path}")

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            minimum = node.get("minimum")
            maximum = node.get("maximum")
            if isinstance(minimum, (int, float)) and value < minimum:
                output.append(f"{label} is less than minimum at {path}")
            if isinstance(maximum, (int, float)) and value > maximum:
                output.append(f"{label} is greater than maximum at {path}")

        if isinstance(value, list):
            minimum = node.get("minItems")
            if isinstance(minimum, int) and len(value) < minimum:
                output.append(f"{label} has fewer than minItems at {path}")
            maximum = node.get("maxItems")
            if isinstance(maximum, int) and len(value) > maximum:
                output.append(f"{label} has more than maxItems at {path}")
            if node.get("uniqueItems") is True:
                for index, item in enumerate(value):
                    if any(skill_json_equal(item, previous) for previous in value[:index]):
                        output.append(f"{label} violates uniqueItems at {path}")
                        break
            item_schema = node.get("items")
            if item_schema is not None:
                for index, item in enumerate(value):
                    validate(item, item_schema, f"{path}[{index}]", output)
            contains_schema = node.get("contains")
            if contains_schema is not None:
                contains_match = False
                for index, item in enumerate(value):
                    branch_errors: list[str] = []
                    validate(item, contains_schema, f"{path}[{index}]", branch_errors)
                    if not branch_errors:
                        contains_match = True
                        break
                if not contains_match:
                    output.append(f"{label} violates contains at {path}")

        if isinstance(value, dict):
            minimum = node.get("minProperties")
            if isinstance(minimum, int) and len(value) < minimum:
                output.append(f"{label} has fewer than minProperties at {path}")
            required = node.get("required")
            if isinstance(required, list):
                for key in required:
                    if isinstance(key, str) and key not in value:
                        output.append(f"{label} is missing required property at {path}.{key}")
            properties = node.get("properties")
            declared_properties = properties if isinstance(properties, dict) else {}
            additional = node.get("additionalProperties")
            for key in value:
                if key not in declared_properties:
                    if additional is False:
                        output.append(f"{label} has an additional property at {path}.{key}")
                    elif isinstance(additional, dict):
                        validate(value[key], additional, f"{path}.{key}", output)
            if isinstance(properties, dict):
                for key, child_schema in properties.items():
                    if key in value:
                        validate(value[key], child_schema, f"{path}.{key}", output)

    try:
        validate(instance, schema, "$", errors)
    except Exception:
        errors.append(f"{label} schema validation failed safely on malformed input")
    return errors

def stage0_invocation_error(code: str, field_path: str, remediation: str, message: str) -> WorkflowError:
    return WorkflowError(
        message,
        exit_code=2,
        payload={"code": code, "field_path": field_path, "remediation": remediation},
    )

def stage0_output_contract(
    skill_id: str,
    package: Path,
    interface: dict[str, Any],
    exit_id: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    declared_exits = {
        str(item.get("id") or "")
        for item in interface.get("external_exits", []) if isinstance(item, dict)
    }
    if exit_id not in declared_exits:
        raise stage0_invocation_error(
            "unknown_typed_exit",
            "owner_result.typed_exit",
            f"Rerun the owner step so it returns one declared typed exit for {skill_id}: {', '.join(sorted(declared_exits))}.",
            "Stage 0 owner result selected an unknown typed exit.",
        )
    contracts = interface["public_contracts"]
    outputs = [
        item for item in contracts.get("outputs", [])
        if isinstance(item, dict) and item.get("exit_id") == exit_id
    ]
    projections = [
        item for item in contracts.get("projections", [])
        if isinstance(item, dict) and item.get("exit_id") == exit_id
    ]
    if len(outputs) != 1 or len(projections) != 1:
        raise stage0_invocation_error(
            "invalid_public_contract",
            f"public_contracts.outputs.{exit_id}",
            "Restore one output and one projection for every declared typed exit.",
            "Stage 0 typed output contract is missing or ambiguous.",
        )
    output = outputs[0]
    projection = projections[0]
    schema_ref = output.get("schema")
    errors: list[str] = []
    schema = skill_read_schema(
        package / str(schema_ref.get("path") if isinstance(schema_ref, dict) else ""),
        "Stage 0 typed output schema",
        errors,
    )
    if errors or not isinstance(schema, dict):
        raise stage0_invocation_error(
            "invalid_public_contract",
            f"public_contracts.outputs.{exit_id}",
            "Restore the declared output schema and rerun package validation.",
            "Stage 0 typed output contract is invalid.",
        )
    return schema, projection

def stage0_owner_path(root: Path, value: str | None, field: str) -> Path:
    raw = str(value or "").strip()
    relative = skill_safe_relative(raw)
    if relative is None:
        raise stage0_invocation_error(
            "invalid_owner_result",
            field,
            "Provide the repo-relative locator emitted by the completed owner step.",
            "Stage 0 owner result locator is invalid.",
        )
    path = root / relative
    errors: list[str] = []
    if skill_lstat_path(root, path, "Stage 0 owner result", errors, kind="file") is None:
        raise stage0_invocation_error(
            "invalid_owner_result",
            field,
            "Restore the regular repo-local owner result and rerun its checker.",
            "Stage 0 owner result is missing or unsafe.",
        )
    return path

def parse_canonical_pull_request_url(repo: str, url: Any) -> tuple[str, int]:
    expected_repo = normalize_github_repository(repo)
    if not expected_repo or not isinstance(url, str) or not git_remote_config_value_is_safe(url):
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        ) from exc
    parts = parsed.path.split("/")
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or parsed.query
        or parsed.fragment
        or len(parts) != 5
        or parts[0] != ""
        or parts[3] != "pull"
        or not re.fullmatch(r"[1-9][0-9]*", parts[4])
        or normalize_github_repository(f"{parts[1]}/{parts[2]}") != expected_repo
    ):
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    try:
        number = int(parts[4])
    except ValueError as exc:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        ) from exc
    return url, number

def canonical_pull_request_url(repo: str, number: int, url: Any) -> str:
    value, parsed_number = parse_canonical_pull_request_url(repo, url)
    if isinstance(number, bool) or not isinstance(number, int) or parsed_number != number:
        raise WorkflowError(
            "Publish recovery open PR lacks a canonical URL for the current repository.",
            exit_code=2,
        )
    return value

def create_pull_request(
    root: Path,
    repo: str,
    base_branch: str,
    branch: str,
    title: str,
    body: str,
    draft: bool,
) -> str:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(body)
        body_file = tmp.name
    try:
        command = [
            "pr", "create", "--repo", repo, "--base", base_branch,
            "--head", branch, "--title", title, "--body-file", body_file,
        ]
        if draft:
            command.append("--draft")
        proc = run_gh_command(command, root, repo=repo, operation="pull_request_create")
        pr_url = proc.stdout.strip()
        try:
            canonical_url, _ = parse_canonical_pull_request_url(repo, pr_url)
        except WorkflowError as exc:
            raise github_response_incomplete(
                operation="pull_request_create",
                repo=repo,
                detail="gh pr create did not return a canonical PR URL for the current repository.",
            ) from exc
        return canonical_url
    finally:
        Path(body_file).unlink(missing_ok=True)

def update_pull_request_metadata(
    root: Path,
    repo: str,
    number: int,
    title: str,
    body: str,
) -> None:
    if normalize_github_repository(repo) != repo.casefold():
        raise WorkflowError("Closeout pull request repository is invalid.", exit_code=2)
    if isinstance(number, bool) or not isinstance(number, int) or number <= 0:
        raise WorkflowError("Closeout pull request number is invalid.", exit_code=2)
    try:
        body_bytes = body.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise WorkflowError("Closeout pull request body is not valid UTF-8.", exit_code=2) from exc
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        tmp.write(body_bytes)
        body_file = tmp.name
    try:
        run_gh_command(
            [
                "pr",
                "edit",
                str(number),
                "--repo",
                repo,
                "--title",
                title,
                "--body-file",
                body_file,
            ],
            root,
            repo=repo,
            operation="pull_request_edit",
        )
    finally:
        Path(body_file).unlink(missing_ok=True)

def validate_publish_identity_and_remote_head(
    root: Path,
    task: dict[str, Any],
    task_context: dict[str, Any],
    repo: str,
    base_branch: str,
    branch: str,
    remote: str,
) -> dict[str, str]:
    errors: list[str] = []
    expected_repo = str(
        task_context.get("source_repo", {}).get("repo")
        if isinstance(task_context.get("source_repo"), dict)
        else ""
    ).strip()
    if expected_repo and expected_repo.casefold() != repo.casefold():
        errors.append("publish repo does not match current task runtime repository identity")
    expected_branch = str(task_context.get("branch_name") or "").strip()
    if expected_branch and expected_branch != branch:
        errors.append("current head branch does not match current task runtime branch")
    normalized_base = normalize_ref(base_branch).removeprefix("origin/")
    for label, value in [
        ("task runtime identity", task_context.get("base_branch")),
        ("task.json", task.get("base_branch")),
    ]:
        if value and normalize_ref(str(value)).removeprefix("origin/") != normalized_base:
            errors.append(f"publish base branch does not match {label} base_branch")
    if errors:
        raise WorkflowError(
            "Publish branch/base/repository identity validation failed.",
            exit_code=2,
            payload={"errors": errors},
        )
    head = current_head(root)
    remote_proc = run(["git", "ls-remote", "--heads", remote, branch], cwd=root, check=False)
    remote_lines = [line.split() for line in remote_proc.stdout.splitlines() if line.strip()]
    remote_head = remote_lines[0][0] if len(remote_lines) == 1 and remote_lines[0] else ""
    if remote_proc.returncode != 0 or remote_head != head:
        raise WorkflowError(
            "Publish remote branch HEAD does not match the current local HEAD.",
            exit_code=2,
            payload={"head": head, "remote_head": remote_head},
        )
    return {
        "repo": repo,
        "base_branch": normalized_base,
        "head_branch": branch,
        "head": head,
        "remote_head": remote_head,
    }

def task_finalization_path(
    root: Path,
    task_dir: Path,
) -> Path:
    return ai_first_owner_checkpoint_path(
        root,
        task_dir,
        TASK_FINALIZATION_GATE_ARTIFACT,
    )

def task_finalization_transition_path(
    root: Path,
    task_dir: Path,
) -> Path:
    return ai_first_owner_checkpoint_path(
        root,
        task_dir,
        TASK_FINALIZATION_TRANSITION_GATE_ARTIFACT,
    )

def closeout_input_record(root: Path, path: Path, *, payload: dict[str, Any] | None = None) -> dict[str, str]:
    if not path.is_file() and payload is None:
        raise WorkflowError("Closeout protected input is missing.", exit_code=2, payload={"path": str(path)})
    digest = canonical_json_sha256(payload) if payload is not None else hashlib.sha256(path.read_bytes()).hexdigest()
    return {"path": repo_relative(root, path), "sha256": digest}

def current_archive_month() -> str:
    """Return the month used by the unmodified official task archive command."""
    return datetime.now().strftime("%Y-%m")

def closeout_archive_month(plan: dict[str, Any]) -> str:
    parts = Path(str(plan.get("task", {}).get("archive_locator") or "")).parts
    if len(parts) != 5 or parts[:3] != (".trellis", "tasks", "archive"):
        raise WorkflowError("Closeout archive locator does not contain one canonical month.", exit_code=2)
    month = parts[3]
    if not re.fullmatch(r"\d{4}-\d{2}", month):
        raise WorkflowError("Closeout archive locator month is invalid.", exit_code=2)
    return month

def assert_closeout_archive_month_current(plan: dict[str, Any]) -> None:
    planned = closeout_archive_month(plan)
    actual = current_archive_month()
    if planned != actual:
        raise WorkflowError(
            "Closeout archive month no longer matches the official task.py archive month; the task remains active.",
            exit_code=2,
            payload={
                "stage": "archive-month-preflight",
                "planned_month": planned,
                "official_month": actual,
                "next_action": "rerun trellis-finish-work dry-run and review a new digest before formal closeout",
            },
        )

def assert_closeout_archive_path_preflight(root: Path, archive_locator: str) -> None:
    """Inspect archive ancestors lexically without following symlink components."""
    parts = Path(archive_locator).parts
    if (
        len(parts) != 5
        or parts[:3] != (".trellis", "tasks", "archive")
        or not re.fullmatch(r"\d{4}-\d{2}", parts[3])
        or not parts[4]
    ):
        raise WorkflowError("Closeout archive locator is not canonical.", exit_code=2)
    components = (
        ("archive-root", root.joinpath(*parts[:3])),
        ("archive-month", root.joinpath(*parts[:4])),
        ("archive-destination", root.joinpath(*parts)),
    )
    for component, path in components:
        try:
            mode = os.lstat(path).st_mode
        except FileNotFoundError:
            break
        except OSError as exc:
            raise WorkflowError(
                "Closeout archive path component could not be inspected lexically.",
                exit_code=2,
                payload={
                    "stage": "archive-path-preflight",
                    "component": component,
                    "path": path.relative_to(root).as_posix(),
                },
            ) from exc
        if stat.S_ISLNK(mode):
            raise WorkflowError(
                "Closeout archive path contains a symlink component; the task remains active.",
                exit_code=2,
                payload={
                    "stage": "archive-path-preflight",
                    "component": component,
                    "path": path.relative_to(root).as_posix(),
                },
            )
        if component != "archive-destination" and not stat.S_ISDIR(mode):
            raise WorkflowError(
                "Closeout archive path ancestor is not a directory; the task remains active.",
                exit_code=2,
                payload={
                    "stage": "archive-path-preflight",
                    "component": component,
                    "path": path.relative_to(root).as_posix(),
                },
            )
        if component == "archive-destination":
            raise WorkflowError(
                "Finalization planned archive locator already exists; the task remains active.",
                exit_code=2,
                payload={
                    "stage": "archive-locator-preflight",
                    "archive_locator": archive_locator,
                },
            )

def official_active_task_match(tasks_dir: Path, task_name: str) -> Path | None:
    """Mirror official task_utils.find_task_by_name active-directory lookup."""
    if not task_name or not tasks_dir.is_dir():
        return None
    exact_match = tasks_dir / task_name
    if exact_match.is_dir():
        return exact_match
    for candidate in tasks_dir.iterdir():
        if candidate.is_dir() and candidate.name.endswith(f"-{task_name}"):
            return candidate
    return None

def official_archive_would_handle_child_metadata(child_json: Path) -> bool:
    """Match official read_json plus the truthy child_data mutation guard."""
    try:
        payload = json.loads(child_json.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False
    return bool(payload)

def validate_closeout_task_children(task_dir: Path, task: dict[str, Any]) -> None:
    children = task.get("children", [])
    if not isinstance(children, list) or any(not isinstance(child, str) for child in children):
        raise WorkflowError(
            "Closeout task children must be a list of strings.",
            exit_code=2,
            payload={"stage": "task-children-preflight"},
        )
    tasks_dir = task_dir.parent
    active_children: list[str] = []
    for child_name in children:
        child_dir = official_active_task_match(tasks_dir, child_name)
        if child_dir is not None and official_archive_would_handle_child_metadata(
            child_dir / "task.json"
        ):
            active_children.append(child_dir.name)
    if active_children:
        raise WorkflowError(
            "Closeout archive transaction would modify active child task metadata.",
            exit_code=2,
            payload={
                "stage": "task-children-preflight",
                "active_children": active_children,
            },
        )

def closeout_transaction_parent_head(plan: dict[str, Any]) -> str:
    git = plan.get("git", {}) if isinstance(plan.get("git"), dict) else {}
    return str(git.get("publication_head") or git.get("branch_review_commit") or "")

def validate_closeout_reviewed_content(
    root: Path,
    plan: dict[str, Any],
    commit: str,
    *,
    include_worktree: bool,
) -> str:
    branch_review_commit = closeout_transaction_parent_head(plan)
    if (
        re.fullmatch(r"[0-9a-f]{40}", branch_review_commit) is None
        or re.fullmatch(r"[0-9a-f]{40}", commit) is None
        or not is_ancestor(root, branch_review_commit, commit)
    ):
        raise WorkflowError(
            "Closeout commit is not a descendant of branch_review_commit.",
            exit_code=2,
        )
    anchor_identity = reviewed_content_identity(
        root,
        branch_review_commit,
        include_worktree=False,
    )["sha256"]
    current_identity = reviewed_content_identity(
        root,
        commit,
        include_worktree=include_worktree,
    )["sha256"]
    if current_identity != anchor_identity:
        raise WorkflowError(
            "Closeout reviewed content changed after Branch Review.",
            exit_code=2,
        )
    return anchor_identity

def normalize_closeout_archive_identity(value: Any, archive_locator: str) -> Any:
    if isinstance(value, dict):
        return {
            key: normalize_closeout_archive_identity(item, archive_locator)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [normalize_closeout_archive_identity(item, archive_locator) for item in value]
    if isinstance(value, str):
        if value == archive_locator:
            return "<archive-locator>"
        prefix = f"{archive_locator}/"
        if value.startswith(prefix):
            return f"<archive-locator>/{value.removeprefix(prefix)}"
    return value

def closeout_month_supersession_errors(
    previous: dict[str, Any],
    current: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        previous_month = closeout_archive_month(previous)
        current_month = closeout_archive_month(current)
    except WorkflowError as exc:
        return [str(exc)]
    if previous_month == current_month:
        errors.append("closeout archive month supersession requires a changed month.")
    normalized: list[dict[str, Any]] = []
    for plan, locator in (
        (previous, previous["task"]["archive_locator"]),
        (current, current["task"]["archive_locator"]),
    ):
        candidate = copy.deepcopy(plan)
        candidate.pop("plan_digest", None)
        candidate["projection"]["summary_template_sha256"] = "<archive-template-digest>"
        normalized.append(normalize_closeout_archive_identity(candidate, locator))
    if normalized[0] != normalized[1]:
        errors.append("archive month supersession changed facts beyond archive identity.")
    return errors

def official_after_archive_hook_state(root: Path) -> dict[str, Any]:
    """Reject official after_archive hooks before the archive command can run them."""
    config_path = root / ".trellis/config.yaml"
    try:
        mode = os.lstat(config_path).st_mode
    except FileNotFoundError:
        return {"commands": []}
    except OSError as exc:
        raise WorkflowError("Could not inspect official Trellis config for after_archive hooks.", exit_code=2) from exc
    if not stat.S_ISREG(mode):
        raise WorkflowError(
            "Official Trellis config must be a regular file before finish-work archive.",
            exit_code=2,
            payload={"path": ".trellis/config.yaml", "stage": "after-archive-hook-preflight"},
        )
    try:
        raw = config_path.read_bytes()
        content = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise WorkflowError(
            "Official Trellis config is unreadable for after_archive hook preflight.",
            exit_code=2,
            payload={"path": ".trellis/config.yaml", "stage": "after-archive-hook-preflight"},
        ) from exc
    if b"\x00" in raw:
        raise WorkflowError(
            "Official Trellis config contains an invalid NUL byte.",
            exit_code=2,
            payload={"path": ".trellis/config.yaml", "stage": "after-archive-hook-preflight"},
        )

    parser_path = root / ".trellis/scripts/common/config.py"
    if not parser_path.is_file() or parser_path.is_symlink():
        raise WorkflowError(
            "Official Trellis config parser is unavailable for after_archive hook preflight.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    parser = (
        "import json,sys; "
        "from common.config import parse_simple_yaml; "
        "print(json.dumps(parse_simple_yaml(open(sys.argv[1], encoding='utf-8').read())))"
    )
    proc = run(
        [sys.executable, "-c", parser, str(config_path)],
        cwd=root / ".trellis/scripts",
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Official Trellis config could not be parsed for after_archive hook preflight.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    try:
        parsed = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise WorkflowError(
            "Official Trellis config parser returned invalid hook state.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        ) from exc
    if not isinstance(parsed, dict):
        raise WorkflowError("Official Trellis config root must be a mapping.", exit_code=2)
    hooks = parsed.get("hooks")
    declarations = len(re.findall(r"(?m)^[ \t]*after_archive[ \t]*:", content))
    if hooks is None:
        if declarations:
            raise WorkflowError(
                "Official after_archive hook declaration is outside a parseable hooks mapping.",
                exit_code=2,
                payload={"stage": "after-archive-hook-preflight"},
            )
        return {"commands": []}
    if not isinstance(hooks, dict) or declarations > 1:
        raise WorkflowError(
            "Official after_archive hook configuration is ambiguous or unparsable.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    configured_present = "after_archive" in hooks
    if declarations != (1 if configured_present else 0):
        raise WorkflowError(
            "Official after_archive hook declaration is outside the parsed hooks mapping.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    configured = hooks.get("after_archive", [])
    if configured in ({}, None):
        configured = []
    if not isinstance(configured, list) or any(not isinstance(item, str) for item in configured):
        raise WorkflowError(
            "Official after_archive hook configuration must be an empty command list for finish-work.",
            exit_code=2,
            payload={"stage": "after-archive-hook-preflight"},
        )
    if configured:
        raise WorkflowError(
            "Guru Team finish-work does not support non-empty official after_archive hooks because they run after the task move.",
            exit_code=2,
            payload={
                "stage": "after-archive-hook-preflight",
                "configured_command_count": len(configured),
                "hook_executed": False,
            },
        )
    return {"commands": []}

def closeout_pr_placeholder(repo: str) -> dict[str, Any]:
    number = CLOSEOUT_PR_PLACEHOLDER_NUMBER
    return {
        "number": number,
        "url": f"https://github.com/{repo}/pull/{number}",
        "ref": f"PR #{number}",
    }

def render_closeout_summary_for_pr(plan: dict[str, Any], pr: dict[str, Any]) -> dict[str, Any]:
    number = pr.get("number")
    if (
        not isinstance(number, int)
        or isinstance(number, bool)
        or number < 1
        or number > CLOSEOUT_PR_PLACEHOLDER_NUMBER
    ):
        raise WorkflowError("Final projection PR number is invalid.", exit_code=2)
    expected_url = canonical_pull_request_url(plan["git"]["repo"], number, pr.get("url"))
    summary = copy.deepcopy(plan["projection"]["summary_template"])
    summary["github"]["pr_url"] = expected_url
    summary["index"]["search_terms"]["pr_refs"] = [f"PR #{number}"]
    summary["index"]["retrieval_text"] = current_finish_summary_retrieval_text(
        str(summary["task"]["title"]), summary["index"]
    )
    return summary

def closeout_summary_for_pr(plan: dict[str, Any], pr: dict[str, Any]) -> dict[str, Any]:
    summary = render_closeout_summary_for_pr(plan, pr)
    validate_finish_summary(summary)
    return summary

def closeout_json_artifact_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def closeout_summary_runtime_pr_facts_from_bytes(
    plan: dict[str, Any], content: bytes, *, expected_pr: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Bind runtime PR facts without invoking the general local summary validator."""
    try:
        summary = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowError("Committed final summary is not deterministic UTF-8 JSON.", exit_code=2) from exc
    if not isinstance(summary, dict):
        raise WorkflowError("Committed final summary JSON root must be an object.", exit_code=2)
    github = summary.get("github")
    index = summary.get("index")
    search_terms = index.get("search_terms") if isinstance(index, dict) else None
    pr_url = github.get("pr_url") if isinstance(github, dict) else None
    try:
        pr_url, number = parse_canonical_pull_request_url(plan["git"]["repo"], pr_url)
    except WorkflowError as exc:
        raise WorkflowError(
            "Committed final summary PR URL is not canonical for the immutable repo.", exit_code=2
        ) from exc
    if not isinstance(search_terms, dict) or search_terms.get("pr_refs") != [f"PR #{number}"]:
        raise WorkflowError("Committed final summary PR ref does not match its canonical URL.", exit_code=2)
    runtime_pr = {"number": number, "url": pr_url}
    if expected_pr is not None:
        expected_number = expected_pr.get("number")
        if not isinstance(expected_number, int) or isinstance(expected_number, bool):
            raise WorkflowError("Expected final summary PR number is invalid.", exit_code=2)
        expected_url = canonical_pull_request_url(
            plan["git"]["repo"], expected_number, expected_pr.get("url")
        )
        if number != expected_number or pr_url != expected_url:
            raise WorkflowError(
                "Final summary runtime PR facts differ from the bound pull request.",
                exit_code=2,
            )
        runtime_pr = {"number": expected_number, "url": expected_url}
    expected_summary = render_closeout_summary_for_pr(plan, runtime_pr)
    expected_bytes = closeout_json_artifact_bytes(expected_summary)
    actual_digest = hashlib.sha256(content).hexdigest()
    expected_digest = hashlib.sha256(expected_bytes).hexdigest()
    if content != expected_bytes:
        raise WorkflowError(
            "Final summary bytes do not match the deterministic runtime PR projection.",
            exit_code=2,
            payload={
                "expected_summary_sha256": expected_digest,
                "actual_summary_sha256": actual_digest,
            },
        )
    return {
        "number": number,
        "url": str(pr_url),
        "summary_sha256": actual_digest,
    }

def closeout_summary_template_digest(plan: dict[str, Any], summary: dict[str, Any]) -> str:
    normalized = copy.deepcopy(summary)
    placeholder = plan["projection"]["summary_placeholder"]
    normalized["github"]["pr_url"] = placeholder["url"]
    normalized["index"]["search_terms"]["pr_refs"] = [placeholder["ref"]]
    normalized["index"]["retrieval_text"] = current_finish_summary_retrieval_text(
        str(normalized["task"]["title"]), normalized["index"]
    )
    return closeout_json_artifact_sha256(normalized)

def validate_closeout_final_summary(plan: dict[str, Any], summary: dict[str, Any]) -> None:
    validate_finish_summary(summary)
    pr_url = summary.get("github", {}).get("pr_url")
    try:
        _canonical_url, number = parse_canonical_pull_request_url(plan["git"]["repo"], pr_url)
    except WorkflowError as exc:
        raise WorkflowError(
            "Final summary PR URL does not match closeout repo identity.", exit_code=2
        ) from exc
    expected_ref = [f"PR #{number}"]
    if summary.get("index", {}).get("search_terms", {}).get("pr_refs") != expected_ref:
        raise WorkflowError("Final summary PR ref does not match canonical PR identity.", exit_code=2)
    actual = closeout_summary_template_digest(plan, summary)
    expected = plan["projection"]["summary_template_sha256"]
    if actual != expected:
        raise WorkflowError(
            "Final summary differs from the prevalidated closeout template.",
            exit_code=2,
            payload={"expected_template_sha256": expected, "actual_template_sha256": actual},
        )

def read_and_validate_closeout_final_summary(path: Path, plan: dict[str, Any]) -> dict[str, Any]:
    summary = read_json(path)
    expected_file_sha = closeout_json_artifact_sha256(summary)
    actual_file_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_file_sha != expected_file_sha:
        raise WorkflowError(
            "Final summary bytes are not the exact deterministic JSON artifact encoding.",
            exit_code=2,
            payload={"expected_file_sha256": expected_file_sha, "actual_file_sha256": actual_file_sha},
        )
    validate_closeout_final_summary(plan, summary)
    return summary

def finalization_plan_digest(plan: dict[str, Any]) -> str:
    payload = copy.deepcopy(plan)
    payload.pop("plan_digest", None)
    return canonical_json_sha256(payload)

def closeout_archive_retained_paths(plan: dict[str, Any]) -> list[str]:
    move_paths = plan.get("projection", {}).get("move_paths", [])
    if not isinstance(move_paths, list):
        return []
    if plan.get("schema_version") != FINALIZATION_PLAN_SCHEMA_VERSION:
        return []
    retained = sorted(set(move_paths) & set(CLOSEOUT_ARCHIVE_CORE_ARTIFACTS))
    return retained

def closeout_archive_pruned_paths(plan: dict[str, Any]) -> list[str]:
    move_paths = plan.get("projection", {}).get("move_paths", [])
    if not isinstance(move_paths, list):
        return []
    return sorted(set(move_paths) - set(closeout_archive_retained_paths(plan)))

def closeout_json_artifact_sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(closeout_json_artifact_bytes(payload)).hexdigest()

def finalization_plan_errors(plan: Any) -> list[str]:
    if not isinstance(plan, dict):
        return ["finalization plan must be an object."]
    expected = {
        "schema_version", "task", "git", "inputs", "review", "publish",
        "projection", "transitions", "plan_digest",
    }
    errors: list[str] = []
    if set(plan) != expected:
        errors.append("finalization plan top-level keys do not match a supported schema.")
    if plan.get("schema_version") != FINALIZATION_PLAN_SCHEMA_VERSION:
        errors.append("finalization plan schema_version must match the current contract.")
    digest = str(plan.get("plan_digest") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != finalization_plan_digest(plan):
        errors.append("finalization plan digest does not match canonical content.")
    if plan.get("transitions") != CLOSEOUT_TRANSITIONS:
        errors.append("finalization plan transitions are invalid.")
    task = plan.get("task") if isinstance(plan.get("task"), dict) else {}
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    review = plan.get("review") if isinstance(plan.get("review"), dict) else {}
    publish = plan.get("publish") if isinstance(plan.get("publish"), dict) else {}
    projection = plan.get("projection") if isinstance(plan.get("projection"), dict) else {}
    projection_keys = {
        "active_locator", "archive_locator", "finish_summary_locator",
        "move_paths", "tracked_move_paths", "untracked_archive_outputs",
        "reviewed_tracked_bindings",
        "summary_placeholder",
        "summary_template_sha256", "summary_template", "runtime_fact_fields",
    }
    nested_keys = {
        "task": (task, {"id", "title", "active_locator", "archive_locator"}),
        "review": (review, {"branch_review_commit", "changed_paths"}),
        "publish": (
            publish,
            {
                "title",
                "body",
                "draft",
                "draft_to_ready",
                "match",
            },
        ),
        "projection": (
            projection,
            projection_keys,
        ),
    }
    for label, (value, keys) in nested_keys.items():
        if set(value) != keys:
            errors.append(f"finalization plan {label} keys are invalid.")
    git_keys = {
        "repo", "remote", "base_branch", "head_branch", "branch_review_commit",
        "reviewed_content_head", "publication_head",
    }
    if set(git) != git_keys:
        errors.append("finalization plan git keys are invalid.")
    for label, value in [
        ("task.active_locator", task.get("active_locator")),
        ("task.archive_locator", task.get("archive_locator")),
        ("projection.finish_summary_locator", projection.get("finish_summary_locator")),
    ]:
        errors.extend(finish_summary_path_errors(value, label))
    if not str(task.get("active_locator") or "").startswith(".trellis/tasks/"):
        errors.append("closeout task active locator is invalid.")
    if not str(task.get("archive_locator") or "").startswith(".trellis/tasks/archive/"):
        errors.append("closeout task archive locator is invalid.")
    for key in ["repo", "remote", "base_branch", "head_branch"]:
        if not isinstance(git.get(key), str) or not str(git[key]).strip():
            errors.append(f"closeout git.{key} is invalid.")
    if normalize_github_repository(git.get("repo")) != git.get("repo"):
        errors.append("closeout git.repo must be a normalized GitHub owner/repository identity.")
    if not re.fullmatch(r"[0-9a-f]{40}", str(git.get("branch_review_commit") or "")):
        errors.append("closeout branch_review_commit is invalid.")
    reviewed_head = str(git.get("reviewed_content_head") or git.get("branch_review_commit") or "")
    publication_head = str(git.get("publication_head") or git.get("branch_review_commit") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", reviewed_head):
        errors.append("closeout reviewed_content_head is invalid.")
    if not re.fullmatch(r"[0-9a-f]{40}", publication_head):
        errors.append("closeout publication_head is invalid.")
    if reviewed_head != str(git.get("branch_review_commit") or ""):
        errors.append("closeout reviewed_content_head does not match branch_review_commit.")
    if review.get("branch_review_commit") != git.get("branch_review_commit"):
        errors.append("closeout review commit does not match git identity.")
    changed = review.get("changed_paths")
    if not isinstance(changed, list) or any(not isinstance(path, str) for path in changed) or changed != sorted(set(changed)):
        errors.append("closeout review changed paths must be sorted and unique.")
    if publish.get("draft") is not True or publish.get("draft_to_ready") is not True:
        errors.append("closeout publish must use draft then ready.")
    if not isinstance(publish.get("title"), str) or not publish["title"].strip():
        errors.append("closeout publish title is invalid.")
    if not isinstance(publish.get("body"), str) or not publish["body"].strip():
        errors.append("closeout publish body is invalid.")
    expected_match = {"repo": git.get("repo"), "head": git.get("head_branch"), "base": git.get("base_branch")}
    if publish.get("match") != expected_match:
        errors.append("closeout publish match identity does not match git identity.")
    if projection.get("active_locator") != task.get("active_locator") or projection.get("archive_locator") != task.get("archive_locator"):
        errors.append("closeout projection task locators do not match task identity.")
    if projection.get("finish_summary_locator") != f"{task.get('archive_locator')}/{FINISH_SUMMARY_ARTIFACT}":
        errors.append("closeout projection finish-summary locator is invalid.")
    move_paths = projection.get("move_paths")
    if (
        not isinstance(move_paths, list)
        or not move_paths
        or any(
            not isinstance(path, str)
            or bool(finish_summary_path_errors(path, "projection.move_paths[]"))
            for path in move_paths
        )
        or move_paths != sorted(set(move_paths))
    ):
        errors.append("closeout move paths must be a sorted unique task-relative file set.")
        move_paths = []
    tracked_move_paths = projection.get("tracked_move_paths")
    if (
        not isinstance(tracked_move_paths, list)
        or tracked_move_paths != sorted(set(tracked_move_paths))
        or any(path not in move_paths for path in tracked_move_paths)
    ):
        errors.append("closeout tracked move paths must be a sorted subset of move paths.")
        tracked_move_paths = []
    untracked_archive_outputs = projection.get("untracked_archive_outputs")
    if (
        not isinstance(untracked_archive_outputs, list)
        or not untracked_archive_outputs
        or untracked_archive_outputs != sorted(set(untracked_archive_outputs))
        or any(path not in move_paths for path in untracked_archive_outputs)
    ):
        errors.append("closeout untracked archive outputs must be a sorted non-empty subset of move paths.")
        untracked_archive_outputs = []
    if (
        set(tracked_move_paths) & set(untracked_archive_outputs)
        or sorted(set(tracked_move_paths) | set(untracked_archive_outputs)) != move_paths
    ):
        errors.append("closeout tracked/untracked move classes must be disjoint and cover every move path.")
    if FINISH_SUMMARY_ARTIFACT not in untracked_archive_outputs:
        errors.append("closeout final summary must be classified as an untracked archive output.")
    reviewed_bindings = projection.get("reviewed_tracked_bindings")
    if not isinstance(reviewed_bindings, list):
        errors.append("closeout reviewed tracked bindings must be an array.")
        reviewed_bindings = []
    else:
        binding_paths: list[str] = []
        for index, binding in enumerate(reviewed_bindings):
            if not isinstance(binding, dict) or set(binding) != {"path", "mode", "sha256"}:
                errors.append(f"closeout reviewed tracked binding {index} is invalid.")
                continue
            path = binding.get("path")
            mode = binding.get("mode")
            digest_value = binding.get("sha256")
            if (
                not isinstance(path, str)
                or path not in tracked_move_paths
                or finish_summary_path_errors(path, f"projection.reviewed_tracked_bindings[{index}].path")
            ):
                errors.append(f"closeout reviewed tracked binding {index} path is invalid.")
            else:
                binding_paths.append(path)
            if mode not in {"100644", "100755"}:
                errors.append(f"closeout reviewed tracked binding {index} mode is invalid.")
            if re.fullmatch(r"[0-9a-f]{64}", str(digest_value or "")) is None:
                errors.append(f"closeout reviewed tracked binding {index} digest is invalid.")
        if binding_paths != sorted(set(binding_paths)):
            errors.append("closeout reviewed tracked binding paths must be sorted and unique.")
    forbidden_finalizer_artifacts = {
        PR_READINESS_ARTIFACT,
        TASK_FINALIZATION_GATE_ARTIFACT,
    }
    if forbidden_finalizer_artifacts & set(move_paths):
        errors.append(
            "finalization plan must not move owner-private publication or finalization gates."
        )
    retained_paths = closeout_archive_retained_paths(plan)
    required_retained = {FINISH_SUMMARY_ARTIFACT}
    if not required_retained.issubset(retained_paths):
        errors.append("closeout archive is missing required recovery artifacts.")
    archive_limit = CLOSEOUT_ARCHIVE_MAX_ARTIFACTS
    if len(retained_paths) > archive_limit:
        errors.append("closeout archive exceeds the long-term artifact budget.")
    placeholder = projection.get("summary_placeholder")
    expected_placeholder = closeout_pr_placeholder(str(git.get("repo") or "invalid/invalid"))
    if placeholder != expected_placeholder:
        errors.append("closeout summary PR placeholder is invalid.")
    if projection.get("runtime_fact_fields") != CLOSEOUT_SUMMARY_RUNTIME_FACT_FIELDS:
        errors.append("closeout summary runtime fact fields are invalid.")
    template = projection.get("summary_template")
    template_digest = str(projection.get("summary_template_sha256") or "")
    if not isinstance(template, dict):
        errors.append("closeout summary template must be an object.")
    else:
        template_errors = finish_summary_errors(template)
        if template_errors:
            errors.extend(f"closeout summary template: {error}" for error in template_errors)
        if template.get("github", {}).get("pr_url") != expected_placeholder["url"]:
            errors.append("closeout summary template PR URL must equal the deterministic placeholder.")
        if template.get("index", {}).get("search_terms", {}).get("pr_refs") != [expected_placeholder["ref"]]:
            errors.append("closeout summary template PR ref must equal the deterministic placeholder.")
        if template.get("task", {}).get("archive_dir") != task.get("archive_locator"):
            errors.append("closeout summary template archive locator is invalid.")
        template_artifacts = set(template.get("artifacts", {}).values()) if isinstance(template.get("artifacts"), dict) else set()
        if not template_artifacts.issubset(set(retained_paths)):
            errors.append("closeout summary template artifacts are outside the retained archive set.")
        if not re.fullmatch(r"[0-9a-f]{64}", template_digest) or template_digest != closeout_json_artifact_sha256(template):
            errors.append("closeout summary template digest does not match canonical content.")
    inputs = plan.get("inputs")
    if not isinstance(inputs, dict) or not inputs:
        errors.append("closeout inputs must be a non-empty object.")
    else:
        required_inputs = {
            "task",
            "official_after_archive_hooks",
        }
        if not required_inputs.issubset(inputs):
            errors.append("closeout inputs are missing required direct-consumer facts.")
        if "task_context" in inputs or "review_gate" in inputs:
            errors.append("finalization plan must not persist producer-private runtime identity.")
        for key, item in inputs.items():
            if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
                errors.append(f"closeout input {key} is invalid.")
            elif not re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256") or "")):
                errors.append(f"closeout input {key} digest is invalid.")
            else:
                errors.extend(finish_summary_path_errors(item.get("path"), f"inputs.{key}.path"))
    return errors

def validate_finalization_plan(plan: Any) -> dict[str, Any]:
    errors = finalization_plan_errors(plan)
    if errors:
        raise WorkflowError("finalization plan validation failed.", exit_code=2, payload={"errors": errors})
    return plan

def closeout_live_move_classes(
    root: Path,
    active_locator: str,
    move_paths: list[str],
) -> tuple[list[str], list[str]]:
    tracked: list[str] = []
    for relative in move_paths:
        repo_path = f"{active_locator}/{relative}"
        _blob, mode = task_commit_index_identity(root, repo_path)
        if mode is None:
            continue
        if mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Closeout tracked move paths must be regular Git index entries.",
                exit_code=2,
                payload={"path": relative, "mode": mode},
            )
        tracked.append(relative)
    tracked_move_paths = sorted(tracked)
    untracked_archive_outputs = sorted(set(move_paths) - set(tracked_move_paths))
    return tracked_move_paths, untracked_archive_outputs

def closeout_reviewed_tracked_binding_map(
    plan: dict[str, Any],
) -> dict[str, dict[str, str]]:
    bindings = plan.get("projection", {}).get("reviewed_tracked_bindings", [])
    if not isinstance(bindings, list):
        return {}
    return {
        str(binding["path"]): binding
        for binding in bindings
        if isinstance(binding, dict)
        and set(binding) == {"path", "mode", "sha256"}
        and isinstance(binding.get("path"), str)
    }

def build_closeout_reviewed_tracked_bindings(
    root: Path,
    active_locator: str,
    tracked_move_paths: list[str],
    transaction_parent: str,
) -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    for relative in tracked_move_paths:
        repo_path = f"{active_locator}/{relative}"
        parent_mode, object_type, _object_id = closeout_commit_tree_entry(
            root,
            transaction_parent,
            repo_path,
        )
        if object_type != "blob" or parent_mode not in {"100644", "100755"}:
            raise WorkflowError(
                "Closeout tracked move paths must resolve to regular transaction-parent blobs.",
                exit_code=2,
                payload={"path": relative, "mode": parent_mode, "type": object_type},
            )
        content, content_sha256, working_mode = task_commit_worktree_content(
            root,
            repo_path,
        )
        if (
            content is None
            or content_sha256 is None
            or working_mode not in {"100644", "100755"}
        ):
            raise WorkflowError(
                "Closeout tracked move path is not a readable regular working-tree file.",
                exit_code=2,
                payload={"path": relative},
            )
        parent_content = closeout_commit_blob_bytes(
            root,
            transaction_parent,
            repo_path,
        )
        if working_mode != parent_mode or content != parent_content:
            bindings.append(
                {
                    "path": relative,
                    "mode": working_mode,
                    "sha256": content_sha256,
                }
            )
    return bindings

def build_finalization_plan(
    root: Path,
    task_dir: Path,
    task_context: dict[str, Any],
    task: dict[str, Any],
    *,
    repo: str,
    remote: str,
    base_branch: str,
    head_branch: str,
    branch_review_commit: str,
    title: str,
    body: str,
    review_facts: dict[str, Any] | None = None,
    allow_existing_summary: bool = False,
) -> dict[str, Any]:
    if not isinstance(review_facts, dict):
        raise WorkflowError(
            "Current closeout requires reviewed Publication facts.",
            exit_code=2,
        )
    reviewed_paths = list(review_facts["changed_paths"])
    active_locator = repo_relative(root, task_dir)
    plan_schema_version = FINALIZATION_PLAN_SCHEMA_VERSION
    archive_month_now = current_archive_month()
    archive_locator = f".trellis/tasks/archive/{archive_month_now}/{task_dir.name}"
    assert_closeout_archive_path_preflight(root, archive_locator)
    observed_task_files = {
        path.relative_to(task_dir).as_posix()
        for path in task_dir.rglob("*")
        if path.is_file()
    }
    active_prefix = f"{active_locator}/"
    observed_task_files.update(
        path.removeprefix(active_prefix)
        for path in git_status_paths(root)
        if path.startswith(active_prefix)
    )
    if (
        (task_dir / FINISH_SUMMARY_ARTIFACT).exists()
        and not allow_existing_summary
    ):
        raise WorkflowError(
            "Initial closeout prepare found a stale final summary before the immutable plan existed.",
            exit_code=2,
        )
    task_files = set(observed_task_files)
    task_files.add(FINISH_SUMMARY_ARTIFACT)
    move_paths = sorted(task_files)
    tracked_move_paths, untracked_archive_outputs = closeout_live_move_classes(
        root,
        active_locator,
        move_paths,
    )
    binding_paths = list(tracked_move_paths)
    reviewed_tracked_bindings = build_closeout_reviewed_tracked_bindings(
        root,
        active_locator,
        binding_paths,
        branch_review_commit,
    )
    retained_names = set(CLOSEOUT_ARCHIVE_CORE_ARTIFACTS)
    retained_archive_paths = sorted(set(move_paths) & retained_names)
    transaction_paths = sorted(
        {f"{active_locator}/{name}" for name in tracked_move_paths}
        | {f"{archive_locator}/{name}" for name in retained_archive_paths}
    )
    inputs = {
        "task": closeout_input_record(root, task_dir / "task.json"),
        "official_after_archive_hooks": closeout_input_record(
            root,
            root / ".trellis/config.yaml",
            payload=official_after_archive_hook_state(root),
        ),
    }
    config_path = root / ".trellis/guru-team/config.yml"
    if config_path.is_file():
        inputs["guru_team_config"] = closeout_input_record(root, config_path)
    placeholder = closeout_pr_placeholder(repo)
    commit_time = run_stdout(
        ["git", "show", "-s", "--format=%cI", branch_review_commit],
        cwd=root,
    )
    try:
        generated_at = (
            datetime.fromisoformat(commit_time)
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )
    except ValueError as exc:
        raise WorkflowError(
            "Reviewed content commit time is invalid for the deterministic final-summary projection.",
            exit_code=2,
        ) from exc
    projected_artifacts = {
        key: filename
        for key, filename in CURRENT_FINISH_SUMMARY_ARTIFACT_FILES.items()
        if filename in retained_archive_paths
    }
    summary_template = build_finish_summary(
        root,
        task_dir,
        task_context,
        body,
        branch_review_commit,
        pr_url=placeholder["url"],
        changed_paths=sorted(set(reviewed_paths) | set(transaction_paths)),
        archive_dir_override=archive_locator,
        generated_at_override=generated_at,
        artifacts_override=projected_artifacts,
    )
    try:
        publication_head = current_head(root)
    except WorkflowError:
        publication_head = branch_review_commit
    if re.fullmatch(r"[0-9a-f]{40}", publication_head) is None:
        publication_head = branch_review_commit
    plan: dict[str, Any] = {
        "schema_version": plan_schema_version,
        "task": {
            "id": str(task.get("id") or task.get("name") or task_dir.name),
            "title": str(task.get("title") or task.get("name") or task_dir.name),
            "active_locator": active_locator,
            "archive_locator": archive_locator,
        },
        "git": {
            "repo": repo,
            "remote": remote,
            "base_branch": normalize_ref(base_branch).removeprefix("origin/"),
            "head_branch": head_branch,
            "branch_review_commit": branch_review_commit,
            "reviewed_content_head": branch_review_commit,
            "publication_head": publication_head,
        },
        "inputs": inputs,
        "review": {
            "branch_review_commit": branch_review_commit,
            "changed_paths": reviewed_paths,
        },
        "publish": {
            "title": title,
            "body": body,
            "draft": True,
            "draft_to_ready": True,
            "match": {"repo": repo, "head": head_branch, "base": normalize_ref(base_branch).removeprefix("origin/")},
        },
        "projection": {
            "active_locator": active_locator,
            "archive_locator": archive_locator,
            "finish_summary_locator": f"{archive_locator}/{FINISH_SUMMARY_ARTIFACT}",
            "move_paths": move_paths,
            "tracked_move_paths": tracked_move_paths,
            "untracked_archive_outputs": untracked_archive_outputs,
            "reviewed_tracked_bindings": reviewed_tracked_bindings,
            "summary_placeholder": placeholder,
            "summary_template_sha256": closeout_json_artifact_sha256(summary_template),
            "summary_template": summary_template,
            "runtime_fact_fields": list(CLOSEOUT_SUMMARY_RUNTIME_FACT_FIELDS),
        },
        "transitions": list(CLOSEOUT_TRANSITIONS),
        "plan_digest": "",
    }
    plan["plan_digest"] = finalization_plan_digest(plan)
    return validate_finalization_plan(plan)

def resolve_closeout_branch_review_commit(
    task_ref: str,
    *,
    publication_ready: dict[str, Any] | None,
) -> str:
    if publication_ready is None:
        raise WorkflowError(
            "Initial closeout requires a Publication ready DTO.",
            exit_code=2,
        )
    branch_review_commit = str(publication_ready.get("branch_review_commit") or "")

    publication_mismatch = publication_ready is not None and (
        publication_ready.get("profile") != "publication_ready"
        or publication_ready.get("task_ref") != task_ref
        or publication_ready.get("branch_review_commit") != branch_review_commit
    )
    if publication_mismatch:
        raise WorkflowError(
            "Finalizer Publication ready DTO does not match the current task or immutable plan.",
            exit_code=2,
        )
    if re.fullmatch(r"[0-9a-f]{40}", branch_review_commit) is None:
        raise WorkflowError(
            "Finalizer branch_review_commit is invalid.",
            exit_code=2,
        )
    return branch_review_commit

def prepare_closeout(
    root: Path,
    args: argparse.Namespace,
    config: dict[str, Any],
    task_dir: Path,
    task_context: dict[str, Any],
    *,
    publication_ready: dict[str, Any] | None = None,
    current_finalizer: bool = False,
) -> dict[str, Any]:
    official_after_archive_hook_state(root)
    expected_task_ref = repo_relative(root, task_dir)
    target_repo = normalize_github_repository(
        str(args.repo or config.get("github_repo") or "").strip()
        or infer_github_repo(root)
    )
    branch_review_commit = resolve_closeout_branch_review_commit(
        expected_task_ref,
        publication_ready=publication_ready,
    )
    validate_closeout_reviewed_content(
        root,
        {"git": {"branch_review_commit": branch_review_commit}},
        current_head(root),
        include_worktree=True,
    )
    publication_identity = finalizer_publication_identity(
        root,
        branch_review_commit,
        target_repo,
    )
    review_facts = closeout_reviewed_change_facts(
        root,
        task_context,
        branch_review_commit,
    )
    dirty_paths = finalizer_unreviewed_dirty_paths(
        root,
        task_dir,
    )
    if dirty_paths:
        raise WorkflowError(
            "Working tree has uncommitted reviewed content. Commit reviewed task work before finish-work.",
            exit_code=2,
            payload={"dirty_paths": dirty_paths},
        )
    if publication_ready is not None:
        title = str(publication_ready.get("pr_title") or "")
        body = str(publication_ready.get("pr_body") or "")
    else:
        raise WorkflowError(
            "Initial closeout requires the Publication 4.0 exact PR payload.",
            exit_code=2,
        )
    body_errors = validate_pr_body_quality(body, False)
    if not title.strip():
        body_errors.append("PR title is empty.")
    if body_errors:
        raise WorkflowError(
            "finish-work blocked because PR readiness evidence is incomplete.",
            exit_code=2,
            payload={"errors": body_errors},
        )
    task = task_json(task_dir)
    if task.get("status") != "in_progress":
        raise WorkflowError(
            "Initial or resumed closeout preparation requires task status=in_progress.",
            exit_code=2,
        )
    validate_closeout_task_children(task_dir, task)
    repo = normalize_github_repository(
        str(args.repo or config.get("github_repo") or "").strip() or infer_github_repo(root)
    )
    if not repo:
        raise WorkflowError("Could not resolve GitHub repo for finalization plan.", exit_code=2)
    base = base_branch_from_sources(args, task, task_context)
    branch = current_branch(root)
    remote = str(args.remote or publish_config(config).get("remote") or "origin")
    validate_github_remote_repository(root, remote, repo)
    plan = build_finalization_plan(
        root, task_dir, task_context, task,
        repo=repo, remote=remote, base_branch=base, head_branch=branch,
        branch_review_commit=branch_review_commit, title=title, body=body,
        review_facts=review_facts,
        allow_existing_summary=current_finalizer,
    )
    month_supersession: dict[str, Any] | None = None
    pre_pr_reprepare: dict[str, Any] | None = None
    return {
        "plan": plan,
        "plan_digest": plan["plan_digest"],
        "task": task,
        "task_context": task_context,
        "body": body,
        "month_supersession": month_supersession,
        "pre_pr_reprepare": pre_pr_reprepare,
        "reviewed_content_head": publication_identity["reviewed_content_head"],
        "publication_head": publication_identity["publication_head"],
        "metadata_tail": publication_identity["metadata_tail"],
    }

def resolve_closeout_pre_draft_state(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
) -> str:
    branch_review_commit = str(plan["git"]["branch_review_commit"])
    anchor_identity = reviewed_content_identity(
        root,
        branch_review_commit,
        include_worktree=False,
    )["sha256"]
    continuity_errors = review_branch_content_continuity_errors(
        root,
        task_dir,
        branch_review_commit,
        anchor_identity,
        current_head(root),
    )
    if continuity_errors:
        raise WorkflowError(
            "Closeout reviewed content is stale.",
            exit_code=2,
            payload={"errors": continuity_errors},
        )
    publication_head = str(
        plan["git"].get("publication_head")
        or plan["git"]["branch_review_commit"]
    )
    remote_head = closeout_remote_branch_head(root, plan)
    if remote_head != publication_head:
        return "prepared"
    return "content_pushed"

def closeout_remote_branch_head(root: Path, plan: dict[str, Any]) -> str:
    proc = run(
        ["git", "ls-remote", "--heads", plan["git"]["remote"], plan["git"]["head_branch"]],
        cwd=root,
        check=False,
    )
    rows = [line.split() for line in proc.stdout.splitlines() if line.strip()]
    if proc.returncode != 0 or len(rows) > 1:
        raise WorkflowError("Could not resolve the unique closeout remote branch HEAD.", exit_code=2)
    return rows[0][0] if rows else ""

def push_closeout_branch_if_needed(root: Path, plan: dict[str, Any]) -> bool:
    local_head = current_head(root)
    if closeout_remote_branch_head(root, plan) == local_head:
        return False
    command = ["git", "push", plan["git"]["remote"], plan["git"]["head_branch"]]
    run_stdout(command, cwd=root)
    return True

def closeout_pull_request_head_repository(
    item: dict[str, Any], expected_repo: str
) -> tuple[str, bool]:
    expected = normalize_github_repository(expected_repo)
    repository = item.get("headRepository")
    owner = item.get("headRepositoryOwner")
    cross_repository = item.get("isCrossRepository")
    if (
        not expected
        or not isinstance(repository, dict)
        or not isinstance(owner, dict)
        or not isinstance(cross_repository, bool)
    ):
        raise WorkflowError("Closeout pull request head repository identity is missing or invalid.", exit_code=2)
    actual = normalize_github_repository(repository.get("nameWithOwner"))
    owner_login = str(owner.get("login") or "").strip().casefold()
    if not actual or owner_login != actual.split("/", 1)[0]:
        raise WorkflowError("Closeout pull request head repository fields are inconsistent.", exit_code=2)
    is_target = actual == expected
    if cross_repository != (not is_target):
        raise WorkflowError("Closeout pull request cross-repository identity is inconsistent.", exit_code=2)
    return actual, is_target

def resolve_closeout_pull_request(
    root: Path, repo: str, branch: str, base_branch: str, remote: str = "origin"
) -> dict[str, Any] | None:
    expected_repo = validate_github_remote_repository(root, remote, repo)
    values = gh_json(
        [
            "pr", "list", "--repo", repo, "--head", branch,
            "--base", base_branch, "--state", "open", "--limit", "100",
            "--json", (
                "number,url,title,body,headRefName,baseRefName,headRefOid,isDraft,"
                "headRepository,headRepositoryOwner,isCrossRepository"
            ),
        ],
        cwd=root,
        required_fields=(
            "number", "url", "title", "body", "headRefName", "baseRefName",
            "headRefOid", "isDraft", "headRepository", "headRepositoryOwner",
            "isCrossRepository",
        ),
        operation="pull_request_read",
    )
    if not isinstance(values, list):
        raise github_response_incomplete(
            operation="pull_request_read", repo=repo, detail="Pull request list is not an array."
        )
    exact: list[dict[str, Any]] = []
    cross_repository: list[dict[str, Any]] = []
    for item in values:
        if not isinstance(item, dict):
            raise WorkflowError("Closeout pull request identity is invalid.", exit_code=2)
        number = item.get("number")
        if (
            not isinstance(number, int)
            or item.get("headRefName") != branch
            or item.get("baseRefName") != base_branch
        ):
            raise WorkflowError("Closeout pull request repo/head/base identity is invalid.", exit_code=2)
        actual_repo, is_target = closeout_pull_request_head_repository(item, expected_repo)
        if not is_target:
            cross_repository.append({"number": number, "head_repository": actual_repo})
            continue
        item["url"] = canonical_pull_request_url(expected_repo, number, item.get("url"))
        if not re.fullmatch(r"[0-9a-f]{40}", str(item.get("headRefOid") or "")):
            raise WorkflowError("Closeout pull request headRefOid is invalid.", exit_code=2)
        if not isinstance(item.get("isDraft"), bool):
            raise WorkflowError("Closeout pull request draft state is invalid.", exit_code=2)
        if not isinstance(item.get("title"), str) or not isinstance(item.get("body"), str):
            raise WorkflowError("Closeout pull request title/body identity is invalid.", exit_code=2)
        exact.append(item)
    if cross_repository:
        raise WorkflowError(
            "Closeout found cross-repository pull request candidates for the immutable head branch.",
            exit_code=2,
            payload={"candidates": cross_repository},
        )
    if len(exact) > 1:
        raise WorkflowError(
            "Closeout requires zero or one exact open pull request.",
            exit_code=2,
            payload={"open_pr_count": len(exact)},
        )
    return exact[0] if exact else None


def resolve_closeout_terminal_pull_requests(
    root: Path, repo: str, branch: str, base_branch: str, remote: str = "origin"
) -> list[dict[str, Any]]:
    """Return exact same-repository Closed or Merged PRs for the target branch."""
    expected_repo = validate_github_remote_repository(root, remote, repo)
    values = gh_json(
        [
            "pr", "list", "--repo", repo, "--head", branch,
            "--base", base_branch, "--state", "closed", "--limit", "100",
            "--json", (
                "number,url,state,headRefName,baseRefName,headRepository,"
                "headRepositoryOwner,isCrossRepository"
            ),
        ],
        cwd=root,
        required_fields=(
            "number", "url", "state", "headRefName", "baseRefName",
            "headRepository", "headRepositoryOwner", "isCrossRepository",
        ),
        operation="pull_request_read",
    )
    if not isinstance(values, list):
        raise github_response_incomplete(
            operation="pull_request_read",
            repo=repo,
            detail="Terminal pull request list is not an array.",
        )
    exact: list[dict[str, Any]] = []
    for item in values:
        if not isinstance(item, dict):
            raise WorkflowError("Terminal closeout pull request identity is invalid.", exit_code=2)
        number = item.get("number")
        state = item.get("state")
        if (
            not isinstance(number, int)
            or state not in {"CLOSED", "MERGED"}
            or item.get("headRefName") != branch
            or item.get("baseRefName") != base_branch
        ):
            raise WorkflowError(
                "Terminal closeout pull request repo/head/base/state identity is invalid.",
                exit_code=2,
            )
        _actual_repo, is_target = closeout_pull_request_head_repository(item, expected_repo)
        if not is_target:
            continue
        exact.append(
            {
                "number": number,
                "url": canonical_pull_request_url(expected_repo, number, item.get("url")),
                "state": state,
            }
        )
    return exact

def classify_existing_pr_recovery(
    root: Path,
    plan: dict[str, Any],
    existing_pr: dict[str, Any] | None = None,
    remote_head: str | None = None,
    *,
    allow_equal: bool = False,
) -> dict[str, Any] | None:
    """Build the exact side-effect-free adoption facts for one current PR."""
    git = plan["git"]
    pr = existing_pr if existing_pr is not None else resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    if pr is None:
        return None
    remote = remote_head if remote_head is not None else closeout_remote_branch_head(root, plan)
    pr_head = str(pr.get("headRefOid") or "")
    publication_head = str(git.get("publication_head") or git.get("branch_review_commit") or "")
    if remote != pr_head:
        raise WorkflowError(
            "Existing PR recovery requires identical remote branch and PR HEADs.",
            exit_code=2,
            payload={
                "reason_code": "existing_pr_remote_head_mismatch",
                "remote_head": remote,
                "pr_head": pr_head,
            },
        )
    if remote == publication_head:
        if not allow_equal:
            raise WorkflowError(
                "Fresh existing PR recovery cannot adopt an already-pushed publication HEAD without an owner transaction.",
                exit_code=2,
                payload={
                    "reason_code": "existing_pr_unbound_equal_head",
                    "remote_head": remote,
                    "publication_head": publication_head,
                },
            )
        ancestry = "equal"
    elif remote and is_ancestor(root, remote, publication_head):
        ancestry = "strict_ancestor"
    else:
        raise WorkflowError(
            "Fresh existing PR recovery requires a strict publication HEAD ancestor; equality is valid only for a transaction-bound resume.",
            exit_code=2,
            payload={
                "reason_code": "existing_pr_head_not_ancestor",
                "remote_head": remote,
                "publication_head": publication_head,
            },
        )
    metadata_comparison = {
        "live_title": pr.get("title"),
        "live_body": pr.get("body"),
        "title_matches": pr.get("title") == plan["publish"]["title"],
        "body_matches": pr.get("body") == plan["publish"]["body"],
    }
    return {
        "mode": "existing_pr_recovery",
        "pr": {"number": pr["number"], "url": pr["url"]},
        "initial_state": "draft" if pr["isDraft"] else "ready",
        "initial_is_draft": bool(pr["isDraft"]),
        "pre_push_remote_head": remote,
        "publication_head": publication_head,
        "ancestry": ancestry,
        "push_required": ancestry == "strict_ancestor",
        "metadata_update_required": not (
            metadata_comparison["title_matches"]
            and metadata_comparison["body_matches"]
        ),
        "metadata_comparison": metadata_comparison,
        "ready_action": "mark_ready" if pr["isDraft"] else "preserve_ready",
    }

def provenance_tail_transaction_rebind_errors(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
) -> list[str]:
    """Validate the one supported predecessor-to-current provenance identity step."""
    git = plan["git"]
    active_task_dir = root / str(plan["task"]["active_locator"])
    current_publication_head = str(
        git.get("publication_head") or git.get("branch_review_commit") or ""
    )
    errors = [
        field
        for field, matches in (
            ("task_ref", transaction.get("task_ref") == plan["task"]["active_locator"]),
            ("repo_ref", transaction.get("repo_ref") == git.get("repo")),
            ("base_branch", transaction.get("base_branch") == git.get("base_branch")),
            ("branch", transaction.get("branch") == git.get("head_branch")),
            (
                "publication",
                transaction.get("publication")
                == {
                    "title": plan["publish"]["title"],
                    "body": plan["publish"]["body"],
                },
            ),
            (
                "current_reviewed_publication_head",
                git.get("branch_review_commit") == current_publication_head,
            ),
            (
                "archive_state",
                not (active_task_dir / FINISH_SUMMARY_ARTIFACT).exists(),
            ),
        )
        if not matches
    ]
    predecessor_reviewed_head = str(transaction.get("branch_review_commit") or "")
    predecessor_publication_head = str(transaction.get("publication_head") or "")
    if predecessor_reviewed_head != predecessor_publication_head:
        errors.extend(
            provenance_tail_commit_errors(
                root,
                predecessor_reviewed_head,
                predecessor_publication_head,
                target_repo=git.get("repo"),
                require_current=False,
            )
        )
    errors.extend(
        provenance_tail_commit_errors(
            root,
            predecessor_publication_head,
            current_publication_head,
            target_repo=git.get("repo"),
        )
    )
    return sorted(set(errors))

def provenance_tail_transaction_rebind_is_base_evolution(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
    *,
    comparison_head: str | None = None,
) -> bool:
    """Identify a current base descendant without treating business drift as a tail."""
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    base_branch = str(git.get("base_branch") or "")
    current_publication_head = str(
        comparison_head
        or git.get("publication_head")
        or git.get("branch_review_commit")
        or ""
    )
    predecessor_publication_head = str(transaction.get("publication_head") or "")
    if not base_branch or not re.fullmatch(
        r"[0-9a-f]{40}", current_publication_head
    ) or not re.fullmatch(r"[0-9a-f]{40}", predecessor_publication_head):
        return False
    base_ref = diff_base_ref(root, base_branch)
    base_proc = run(
        ["git", "rev-parse", "--verify", base_ref],
        cwd=root,
        check=False,
    )
    base_head = base_proc.stdout.strip() if base_proc.returncode == 0 else ""
    if not (
        re.fullmatch(r"[0-9a-f]{40}", base_head) is not None
        and base_head != predecessor_publication_head
        and is_ancestor(root, base_head, current_publication_head)
        and not is_ancestor(root, base_head, predecessor_publication_head)
    ):
        return False
    merge_base_proc = run(
        ["git", "merge-base", predecessor_publication_head, base_head],
        cwd=root,
        check=False,
    )
    if merge_base_proc.returncode != 0:
        return False
    merge_base = merge_base_proc.stdout.strip()
    current_delta = run(
        [
            "git", "diff", "--no-ext-diff", "--binary",
            f"{predecessor_publication_head}..{current_publication_head}",
        ],
        cwd=root,
        check=False,
    )
    base_delta = run(
        [
            "git", "diff", "--no-ext-diff", "--binary",
            f"{merge_base}..{base_head}",
        ],
        cwd=root,
        check=False,
    )
    return (
        current_delta.returncode == 0
        and base_delta.returncode == 0
        and current_delta.stdout == base_delta.stdout
    )

def provenance_tail_transaction_rebind_base_evolution_tail_parent(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
) -> str | None:
    """Return the current tail parent only when the full tail and evolution are legal."""
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    current_publication_head = str(
        git.get("publication_head") or git.get("branch_review_commit") or ""
    )
    parent_proc = run(
        ["git", "show", "-s", "--format=%P", current_publication_head],
        cwd=root,
        check=False,
    )
    parents = parent_proc.stdout.split() if parent_proc.returncode == 0 else []
    if len(parents) != 1:
        return None
    tail_parent = parents[0]
    if provenance_tail_commit_errors(
        root,
        tail_parent,
        current_publication_head,
        target_repo=git.get("repo"),
    ):
        return None
    if provenance_tail_transaction_rebind_is_base_evolution(
        root,
        plan,
        transaction,
        comparison_head=tail_parent,
    ):
        return tail_parent
    reviewed_content_head = str(git.get("branch_review_commit") or "")
    if tail_parent != reviewed_content_head:
        return None
    if not provenance_tail_transaction_rebind_is_reviewed_base_descendant(
        root,
        plan,
        transaction,
        comparison_head=tail_parent,
    ):
        return None
    return tail_parent


def provenance_tail_transaction_rebind_is_reviewed_base_descendant(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
    *,
    comparison_head: str,
) -> bool:
    """Allow reviewed task commits after base evolution, with or without a tail."""
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    base_branch = str(git.get("base_branch") or "")
    predecessor_publication_head = str(transaction.get("publication_head") or "")
    reviewed_content_head = str(git.get("branch_review_commit") or "")
    current_publication_head = str(
        git.get("publication_head") or git.get("branch_review_commit") or ""
    )
    if not base_branch or not all(
        re.fullmatch(r"[0-9a-f]{40}", value)
        for value in (
            predecessor_publication_head,
            comparison_head,
            reviewed_content_head,
            current_publication_head,
        )
    ):
        return False
    base_ref = diff_base_ref(root, base_branch)
    base_proc = run(
        ["git", "rev-parse", "--verify", base_ref],
        cwd=root,
        check=False,
    )
    base_head = base_proc.stdout.strip() if base_proc.returncode == 0 else ""
    return bool(
        re.fullmatch(r"[0-9a-f]{40}", base_head)
        and base_head != predecessor_publication_head
        and comparison_head == reviewed_content_head
        and is_ancestor(root, predecessor_publication_head, comparison_head)
        and is_ancestor(root, base_head, comparison_head)
        and not is_ancestor(root, base_head, predecessor_publication_head)
        and is_ancestor(root, comparison_head, current_publication_head)
    )

def provenance_tail_transaction_reprepare_eligible(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
    errors: list[str] | None = None,
) -> bool:
    """Allow only Publication metadata drift to enter the existing reprepare route."""
    errors = (
        errors
        if errors is not None
        else provenance_tail_transaction_rebind_errors(root, plan, transaction)
    )
    error_set = set(errors)
    if "publication" not in error_set or not (
        error_set & PROVENANCE_TAIL_INAPPLICABLE_ERRORS
    ):
        return False
    if error_set - (
        PROVENANCE_TAIL_INAPPLICABLE_ERRORS
        | {"publication", "current_reviewed_publication_head"}
    ):
        return False
    return (
        provenance_tail_transaction_rebind_base_evolution_tail_parent(
            root,
            plan,
            transaction,
        )
        is not None
    )

def classify_provenance_tail_transaction_rebind(
    root: Path,
    plan: dict[str, Any],
    transaction: dict[str, Any],
) -> dict[str, Any] | None:
    """Classify one old unbound publication transaction against a legal new tail."""
    if (
        transaction.get("mode") != "ordinary_publication"
        or transaction.get("next_transition") != "push_content"
        or transaction.get("pr") is not None
        or transaction.get("adopted_pr") is not None
    ):
        return None
    errors = provenance_tail_transaction_rebind_errors(root, plan, transaction)
    base_evolution = False
    reviewed_base_descendant = False
    if errors:
        error_set = set(errors)
        allowed_topology_errors = PROVENANCE_TAIL_INAPPLICABLE_ERRORS | {
            "current_reviewed_publication_head"
        }
        if error_set <= allowed_topology_errors:
            base_evolution = provenance_tail_transaction_rebind_is_base_evolution(
                root, plan, transaction
            )
            if not base_evolution:
                base_evolution = (
                    provenance_tail_transaction_rebind_base_evolution_tail_parent(
                        root, plan, transaction
                    )
                    is not None
                )
            if not base_evolution:
                current_publication_head = str(
                    plan.get("git", {}).get("publication_head")
                    or plan.get("git", {}).get("branch_review_commit")
                    or ""
                )
                reviewed_base_descendant = (
                    provenance_tail_transaction_rebind_is_reviewed_base_descendant(
                        root,
                        plan,
                        transaction,
                        comparison_head=current_publication_head,
                    )
                )
        elif (
            "publication" in error_set
            and error_set - {"publication"} <= allowed_topology_errors
        ):
            base_evolution = (
                provenance_tail_transaction_rebind_base_evolution_tail_parent(
                    root, plan, transaction
                )
                is not None
            )
            pure_base_evolution = False
            if not base_evolution:
                pure_base_evolution = (
                    provenance_tail_transaction_rebind_is_base_evolution(
                        root, plan, transaction
                    )
                )
            if not pure_base_evolution and not base_evolution:
                current_publication_head = str(
                    plan.get("git", {}).get("publication_head")
                    or plan.get("git", {}).get("branch_review_commit")
                    or ""
                )
                reviewed_base_descendant = (
                    provenance_tail_transaction_rebind_is_reviewed_base_descendant(
                        root,
                        plan,
                        transaction,
                        comparison_head=current_publication_head,
                    )
                )
    reprepare_eligible = provenance_tail_transaction_reprepare_eligible(
        root,
        plan,
        transaction,
        errors,
    )
    if (
        errors
        and not base_evolution
        and not reviewed_base_descendant
        and not reprepare_eligible
    ):
        raise WorkflowError(
            "Task finalization transaction cannot rebind across the current provenance tail.",
            exit_code=2,
            payload={
                "reason_code": "provenance_tail_transaction_rebind_invalid",
                "errors": errors,
            },
        )
    git = plan["git"]
    candidate = resolve_closeout_pull_request(
        root,
        git["repo"],
        git["head_branch"],
        git["base_branch"],
        git["remote"],
    )
    if candidate is None:
        terminal_prs = resolve_closeout_terminal_pull_requests(
            root,
            git["repo"],
            git["head_branch"],
            git["base_branch"],
            git["remote"],
        )
        if terminal_prs:
            raise WorkflowError(
                "Provenance-tail transaction rebind found a Closed or Merged pull request for the immutable head/base.",
                exit_code=2,
                payload={
                    "reason_code": "pre_finalizer_terminal_pr_exists",
                    "pull_requests": terminal_prs,
                },
            )
        return None
    remote_head = closeout_remote_branch_head(root, plan)
    predecessor_publication_head = str(transaction["publication_head"])
    if remote_head != predecessor_publication_head and (
        not reviewed_base_descendant
        or not is_ancestor(root, predecessor_publication_head, remote_head)
    ):
        raise WorkflowError(
            "Provenance-tail transaction rebind requires the remote and PR at the predecessor Publication HEAD.",
            exit_code=2,
            payload={
                "reason_code": "provenance_tail_transaction_rebind_remote_head_mismatch",
                "remote_head": remote_head,
                "predecessor_publication_head": predecessor_publication_head,
            },
        )
    recovery = classify_existing_pr_recovery(
        root,
        plan,
        candidate,
        remote_head,
    )
    if (
        recovery.get("ancestry") != "strict_ancestor"
        or recovery.get("push_required") is not True
        or recovery.get("pre_push_remote_head") != remote_head
    ):
        raise WorkflowError(
            "Provenance-tail transaction rebind no longer matches strict-ancestor recovery.",
            exit_code=2,
            payload={"reason_code": "existing_pr_recovery_drift"},
        )
    return recovery
