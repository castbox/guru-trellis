def format_metadata_commit_subject(action: str = "固化任务收尾元数据") -> str:
    return f"chore(trellis): {action.strip()}"

def parse_pull_request_number(value: str) -> int | None:
    match = re.search(r"/pull/(\d+)(?:\b|$)", value.strip())
    if match:
        return int(match.group(1))
    match = re.search(r"#(\d+)\b", value.strip())
    if match:
        return int(match.group(1))
    return None

def canonical_json_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def closeout_lexical_path(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))

def reanchor_darwin_system_repo_alias(boundary: Path, target: Path) -> Path | None:
    if sys.platform != "darwin":
        return None
    alias_prefix = Path("/var")
    canonical_prefix = Path("/private/var")
    try:
        alias_mode = os.lstat(alias_prefix).st_mode
        alias_target = Path(os.readlink(alias_prefix))
    except OSError:
        return None
    if not stat.S_ISLNK(alias_mode):
        return None
    if not alias_target.is_absolute():
        alias_target = alias_prefix.parent / alias_target
    if closeout_lexical_path(alias_target) != canonical_prefix:
        return None

    prefix_pairs = [
        (canonical_prefix, alias_prefix),
        (alias_prefix, canonical_prefix),
    ]
    for boundary_prefix, target_prefix in prefix_pairs:
        try:
            repo_suffix = boundary.relative_to(boundary_prefix)
            alias_repo_root = target_prefix / repo_suffix
            path_suffix = target.relative_to(alias_repo_root)
        except ValueError:
            continue
        return boundary / path_suffix
    return None

def reject_closeout_symlink_components(root: Path, path: Path, label: str) -> Path:
    boundary = closeout_lexical_path(root)
    target = closeout_lexical_path(path)
    try:
        relative = target.relative_to(boundary)
    except ValueError:
        mapped = reanchor_darwin_system_repo_alias(boundary, target)
        if mapped is None:
            raise WorkflowError(
                f"finish-work {label} must stay inside the repository root.",
                exit_code=2,
                payload={"path": str(path)},
            )
        target = mapped
        relative = target.relative_to(boundary)

    components = [boundary]
    current = boundary
    for part in relative.parts:
        current = current / part
        components.append(current)
    for component in components:
        try:
            mode = os.lstat(component).st_mode
        except FileNotFoundError:
            break
        except OSError as exc:
            raise WorkflowError(
                f"finish-work could not inspect {label} path components.",
                exit_code=2,
                payload={"path": str(path), "component": str(component)},
            ) from exc
        if stat.S_ISLNK(mode):
            component_label = "." if component == boundary else component.relative_to(boundary).as_posix()
            raise WorkflowError(
                f"finish-work {label} path must not contain symbolic-link components.",
                exit_code=2,
                payload={"path": str(path), "symlink_component": component_label},
            )
    return target

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

def provenance_canonical_github_locator(repo_ref: str) -> str:
    """Return the one credential-free GitHub locator accepted for source fetch."""
    normalized = normalize_github_repository(repo_ref)
    if not normalized:
        return ""
    return f"https://github.com/{normalized}.git"

def provenance_source_binding_errors(
    manifest: Any,
    target_repo: Any,
    reviewed_content_head: str,
) -> tuple[dict[str, str] | None, list[str]]:
    """Resolve the closed self-hosted/installed extension source identity."""
    errors: list[str] = []
    target_repo_ref = normalize_github_repository(target_repo)
    if not target_repo_ref:
        errors.append("provenance_tail_target_repo_invalid")
    if re.fullmatch(r"[0-9a-f]{40}", str(reviewed_content_head or "")) is None:
        errors.append("provenance_tail_reviewed_head_invalid")
    if not isinstance(manifest, dict):
        errors.append("provenance_tail_manifest_invalid")
        return None, sorted(set(errors))
    if manifest.get("schema_version") != "2.0":
        errors.append("provenance_tail_manifest_schema_mismatch")
    extension = manifest.get("extension")
    if not isinstance(extension, dict) or extension.get("extension_id") != "guru-team":
        errors.append("provenance_tail_extension_identity_mismatch")
    source = manifest.get("source")
    if not isinstance(source, dict):
        errors.append("provenance_tail_source_missing")
        return None, sorted(set(errors))

    source_locator = source.get("repo")
    source_repo_ref = parse_github_remote_repository_url(source_locator)
    canonical_locator = provenance_canonical_github_locator(source_repo_ref)
    if (
        not isinstance(source_locator, str)
        or not source_repo_ref
        or source_locator != canonical_locator
    ):
        errors.append("provenance_tail_source_repo_invalid")
    source_ref = source.get("ref")
    source_commit = source.get("commit")
    if re.fullmatch(r"[0-9a-f]{40}", str(source_ref or "")) is None:
        errors.append("provenance_tail_source_ref_invalid")
    if re.fullmatch(r"[0-9a-f]{40}", str(source_commit or "")) is None:
        errors.append("provenance_tail_source_commit_invalid")
    if source_ref != source_commit:
        errors.append("provenance_tail_source_ref_commit_mismatch")
    tree_state = source.get("tree_state")
    mutable_ref = source.get("is_mutable_ref")
    if tree_state not in {"clean", "dirty"}:
        errors.append("provenance_tail_source_tree_state_invalid")
    if not isinstance(mutable_ref, bool):
        errors.append("provenance_tail_source_ref_mutability_invalid")
    if errors:
        return None, sorted(set(errors))

    mode = "self_hosted" if source_repo_ref == target_repo_ref else "installed"
    if mode == "installed" and tree_state != "clean":
        errors.append("provenance_tail_source_not_clean")
    if mode == "installed" and mutable_ref is not False:
        errors.append("provenance_tail_source_ref_mutable")
    if errors:
        return None, sorted(set(errors))
    bound_commit = (
        reviewed_content_head if mode == "self_hosted" else str(source_commit)
    )
    return {
        "mode": mode,
        "target_repo": target_repo_ref,
        "target_reviewed_head": reviewed_content_head,
        "source_repo": source_repo_ref,
        "source_locator": canonical_locator,
        "source_ref": bound_commit,
        "source_commit": bound_commit,
    }, []

def provenance_source_binding(
    manifest: Any,
    target_repo: Any,
    reviewed_content_head: str,
) -> dict[str, str]:
    binding, errors = provenance_source_binding_errors(
        manifest,
        target_repo,
        reviewed_content_head,
    )
    if binding is None or errors:
        raise WorkflowError(
            "Installed extension source provenance is invalid for Finalizer preparation.",
            exit_code=2,
            payload={
                "reason_code": "provenance_source_binding_invalid",
                "errors": errors,
            },
        )
    return binding

def _provenance_platform_inventory(manifest: Any) -> tuple[str, ...]:
    extension = manifest.get("extension") if isinstance(manifest, dict) else None
    public_api = extension.get("public_api") if isinstance(extension, dict) else None
    capabilities = (
        public_api.get("platform_capabilities")
        if isinstance(public_api, dict)
        else None
    )
    if not isinstance(capabilities, dict):
        raise WorkflowError(
            "Installed platform inventory is missing from Finalizer provenance.",
            exit_code=2,
            payload={"reason_code": "provenance_platform_inventory_missing"},
        )

    upstream = capabilities.get("upstream_platforms")
    descriptors = capabilities.get("projection_descriptors")
    if not isinstance(upstream, list) or not upstream:
        raise WorkflowError(
            "Installed upstream platform inventory is invalid.",
            exit_code=2,
            payload={"reason_code": "provenance_platform_inventory_invalid"},
        )
    if not isinstance(descriptors, list) or not descriptors:
        raise WorkflowError(
            "Installed platform projection descriptors are invalid.",
            exit_code=2,
            payload={"reason_code": "provenance_platform_descriptors_invalid"},
        )

    def rows_by_id(rows: list[Any], label: str) -> dict[str, str]:
        result: dict[str, str] = {}
        flags: set[str] = set()
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                raise WorkflowError(
                    "Installed platform inventory row is invalid.",
                    exit_code=2,
                    payload={
                        "reason_code": "provenance_platform_inventory_invalid",
                        "row": f"{label}[{index}]",
                    },
                )
            platform_id = row.get("id")
            cli_flag = row.get("cli_flag")
            if (
                not isinstance(platform_id, str)
                or not platform_id
                or not isinstance(cli_flag, str)
                or not cli_flag
                or platform_id in result
                or cli_flag in flags
            ):
                raise WorkflowError(
                    "Installed platform inventory has duplicate or invalid identity.",
                    exit_code=2,
                    payload={
                        "reason_code": "provenance_platform_inventory_invalid",
                        "row": f"{label}[{index}]",
                    },
                )
            result[platform_id] = cli_flag
            flags.add(cli_flag)
        return result

    upstream_by_id = rows_by_id(upstream, "upstream_platforms")
    descriptor_by_id = rows_by_id(descriptors, "projection_descriptors")
    if upstream_by_id != descriptor_by_id:
        raise WorkflowError(
            "Installed platform inventory and projection descriptors disagree.",
            exit_code=2,
            payload={"reason_code": "provenance_platform_inventory_mismatch"},
        )
    return tuple(sorted(upstream_by_id.values()))


def provenance_apply_platform_args(manifest: Any) -> list[str]:
    """Project one reviewed installed platform identity into preset apply argv."""
    errors: list[str] = []
    try:
        available_platforms = set(_provenance_platform_inventory(manifest))
    except WorkflowError:
        raise
    selected_by_locator: dict[str, list[str]] = {}
    for object_name in ("install", "skill_packages", "overlays"):
        container = manifest.get(object_name) if isinstance(manifest, dict) else None
        if not isinstance(container, dict):
            errors.append(f"provenance_platform_selection_{object_name}_missing")
            continue
        selected = container.get("selected_platforms")
        if not isinstance(selected, list):
            errors.append(
                f"provenance_platform_selection_{object_name}_type_invalid"
            )
            continue
        if not selected:
            errors.append(f"provenance_platform_selection_{object_name}_empty")
            continue
        if any(not isinstance(platform, str) for platform in selected):
            errors.append(
                f"provenance_platform_selection_{object_name}_member_invalid"
            )
            continue
        if len(selected) != len(set(selected)):
            errors.append(
                f"provenance_platform_selection_{object_name}_duplicate"
            )
        if selected != sorted(selected):
            errors.append(
                f"provenance_platform_selection_{object_name}_not_sorted"
            )
        if any(platform not in available_platforms for platform in selected):
            errors.append(
                f"provenance_platform_selection_{object_name}_unknown"
            )
        selected_by_locator[object_name] = selected

    if len(selected_by_locator) == 3:
        selections = list(selected_by_locator.values())
        if selections[1:] != selections[:-1]:
            errors.append("provenance_platform_selection_mismatch")

    if errors:
        raise WorkflowError(
            "Installed platform selection is invalid for Finalizer preparation.",
            exit_code=2,
            payload={
                "reason_code": "provenance_platform_selection_invalid",
                "errors": sorted(set(errors)),
            },
        )

    selected = selected_by_locator["install"]
    return [item for platform in selected for item in ("--platform", platform)]

def provenance_tail_manifest_errors(
    before: Any,
    after: Any,
    reviewed_content_head: str,
    target_repo: Any,
) -> list[str]:
    """Validate the only manifest mutation allowed after reviewed content."""
    errors: list[str] = []
    if not isinstance(before, dict) or not isinstance(after, dict):
        return ["provenance_tail_manifest_invalid"]
    binding, binding_errors = provenance_source_binding_errors(
        before,
        target_repo,
        reviewed_content_head,
    )
    errors.extend(binding_errors)
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
    elif binding is not None:
        if source.get("repo") != binding["source_locator"]:
            errors.append("provenance_tail_source_repo_mismatch")
        if source.get("ref") != binding["source_ref"]:
            errors.append("provenance_tail_source_ref_mismatch")
        if source.get("commit") != binding["source_commit"]:
            errors.append("provenance_tail_source_commit_mismatch")
        if source.get("tree_state") != "clean":
            errors.append("provenance_tail_source_not_clean")
        if source.get("is_mutable_ref") is not False:
            errors.append("provenance_tail_source_ref_mutable")
    if "installed_at" in after and not isinstance(after["installed_at"], str):
        errors.append("provenance_tail_installed_at_invalid")
    return sorted(set(errors))

def provenance_tail_git_status_paths(root: Path) -> list[str]:
    proc = run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not inspect provenance metadata-tail checkout status.",
            exit_code=2,
        )
    paths: list[str] = []
    for record in proc.stdout.split("\0"):
        if not record:
            continue
        path = record[3:] if len(record) >= 3 else ""
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[-1]
        if path:
            paths.append(path)
    return sorted(set(paths), key=lambda item: item.encode("utf-8"))

def read_json_from_git(root: Path, revision_path: str) -> Any:
    proc = run(["git", "show", revision_path], cwd=root, check=False)
    if proc.returncode != 0:
        raise WorkflowError(
            "Could not read the provenance manifest from the reviewed Git commit.",
            exit_code=2,
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise WorkflowError(
            "The provenance manifest in the reviewed Git commit is invalid JSON.",
            exit_code=2,
        ) from exc

def provenance_tail_checkout_errors(
    root: Path,
    reviewed_content_head: str,
) -> list[str]:
    """Check one detached clean target checkout before apply or commit."""
    errors: list[str] = []
    try:
        head = current_head(root)
    except WorkflowError:
        head = ""
    if head != reviewed_content_head:
        errors.append("provenance_tail_checkout_head_mismatch")
    branch = current_branch(root)
    if branch != "HEAD":
        errors.append("provenance_tail_checkout_not_detached")
    if provenance_tail_git_status_paths(root):
        errors.append("provenance_tail_checkout_not_clean")
    return sorted(set(errors))

def provenance_extension_source_checkout_errors(
    root: Path,
    binding: dict[str, str],
) -> list[str]:
    """Validate extension source identity independently from the target checkout."""
    errors: list[str] = []
    try:
        head = current_head(root)
    except WorkflowError:
        head = ""
    if head != binding["source_commit"]:
        errors.append("provenance_tail_extension_source_head_mismatch")
    if current_branch(root) != "HEAD":
        errors.append("provenance_tail_extension_source_not_detached")
    if provenance_tail_git_status_paths(root):
        errors.append("provenance_tail_extension_source_not_clean")
    origin = run(
        ["git", "remote", "get-url", "--all", "origin"],
        cwd=root,
        check=False,
    )
    urls = origin.stdout.splitlines() if origin.returncode == 0 else []
    if (
        not urls
        or any(
            parse_github_remote_repository_url(value) != binding["source_repo"]
            for value in urls
        )
    ):
        errors.append("provenance_tail_extension_source_repo_mismatch")
    if binding["mode"] == "installed" and urls != [binding["source_locator"]]:
        errors.append("provenance_tail_extension_source_origin_not_canonical")
    return sorted(set(errors))

def provenance_tail_manifest_postimage(
    parent: dict[str, Any],
    binding: dict[str, str],
) -> dict[str, Any]:
    """Build the Finalizer-only provenance tail without reinstalling the preset."""
    postimage = copy.deepcopy(parent)
    source = postimage.get("source")
    if not isinstance(source, dict):
        raise WorkflowError(
            "Provenance tail manifest source is missing.",
            exit_code=2,
            payload={"reason_code": "provenance_tail_source_missing"},
        )
    source.update(
        {
            "repo": binding["source_locator"],
            "ref": binding["source_ref"],
            "commit": binding["source_commit"],
            "tree_state": "clean",
            "is_mutable_ref": False,
        }
    )
    postimage["source"] = source
    return postimage

def prepare_provenance_extension_source_checkout(
    target_root: Path,
    source_root: Path,
    binding: dict[str, str],
) -> None:
    """Create the package-local detached source checkout for one binding mode."""
    if binding["mode"] == "self_hosted":
        proc = run(
            [
                "git",
                "worktree",
                "add",
                "--detach",
                str(source_root),
                binding["source_commit"],
            ],
            cwd=target_root,
            check=False,
        )
        if proc.returncode != 0:
            raise WorkflowError(
                "Could not create the self-hosted extension source checkout.",
                exit_code=2,
                payload={"reason_code": "provenance_source_checkout_create_failed"},
            )
    else:
        init = run(
            ["git", "init", "--quiet", str(source_root)],
            check=False,
        )
        if init.returncode != 0:
            raise WorkflowError(
                "Could not initialize the installed extension source checkout.",
                exit_code=2,
                payload={"reason_code": "provenance_source_checkout_init_failed"},
            )
        origin = run(
            ["git", "remote", "add", "origin", binding["source_locator"]],
            cwd=source_root,
            check=False,
        )
        if origin.returncode != 0:
            raise WorkflowError(
                "Could not configure the canonical extension source origin.",
                exit_code=2,
                payload={"reason_code": "provenance_source_origin_failed"},
            )
        fetch = run(
            [
                "git",
                "fetch",
                "--depth=1",
                "origin",
                binding["source_commit"],
            ],
            cwd=source_root,
            check=False,
        )
        if fetch.returncode != 0 and "not our ref" in fetch.stderr.lower():
            fetch = run(
                ["git", "fetch", "--depth=1", "origin", "HEAD"],
                cwd=source_root,
                check=False,
            )
        if fetch.returncode != 0:
            raise WorkflowError(
                "Could not fetch the immutable extension source commit.",
                exit_code=2,
                payload={"reason_code": "provenance_source_fetch_failed"},
            )
        resolved = run(
            ["git", "rev-parse", "--verify", "FETCH_HEAD^{commit}"],
            cwd=source_root,
            check=False,
        )
        if (
            resolved.returncode != 0
            or resolved.stdout.strip() != binding["source_commit"]
        ):
            raise WorkflowError(
                "Fetched extension source does not match the immutable manifest commit.",
                exit_code=2,
                payload={"reason_code": "provenance_source_fetch_mismatch"},
            )
        checkout = run(
            ["git", "checkout", "--detach", binding["source_commit"]],
            cwd=source_root,
            check=False,
        )
        if checkout.returncode != 0:
            raise WorkflowError(
                "Could not detach the immutable extension source checkout.",
                exit_code=2,
                payload={"reason_code": "provenance_source_checkout_failed"},
            )
    errors = provenance_extension_source_checkout_errors(source_root, binding)
    if errors:
        raise WorkflowError(
            "Extension source checkout failed its immutable clean-source contract.",
            exit_code=2,
            payload={"reason_code": "provenance_source_checkout_invalid", "errors": errors},
        )

def provenance_tail_commit_errors(
    root: Path,
    reviewed_content_head: str,
    publication_head: str,
    *,
    target_repo: Any,
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
                provenance_tail_manifest_errors(
                    before,
                    after,
                    reviewed_content_head,
                    target_repo,
                )
            )
    return sorted(set(errors))

def validate_provenance_metadata_tail(
    root: Path,
    reviewed_content_head: str,
    publication_head: str,
    *,
    target_repo: Any,
) -> dict[str, Any]:
    errors = provenance_tail_commit_errors(
        root,
        reviewed_content_head,
        publication_head,
        target_repo=target_repo,
    )
    if errors:
        raise WorkflowError(
            "Provenance metadata-tail failed its clean-source contract.",
            exit_code=2,
            payload={"errors": errors},
        )
    return {
        "status": "passed",
        "reviewed_content_head": reviewed_content_head,
        "publication_head": publication_head,
        "changed_paths": [PROVENANCE_TAIL_MANIFEST_PATH],
        "changed_fields": sorted(PROVENANCE_TAIL_ALLOWED_FIELDS),
    }

def commit_provenance_metadata_tail(
    root: Path,
    reviewed_content_head: str,
    *,
    target_repo: Any,
    message: str = "chore(trellis): 更新 Guru Team provenance 元数据",
) -> dict[str, Any]:
    """Commit an already-applied manifest tail; no preset/apply is performed here."""
    if current_head(root) != reviewed_content_head:
        raise WorkflowError("Provenance tail commit requires reviewed HEAD as parent.", exit_code=2)
    dirty = provenance_tail_git_status_paths(root)
    if dirty != [PROVENANCE_TAIL_MANIFEST_PATH]:
        raise WorkflowError(
            "Provenance tail commit requires exactly one manifest-only dirty path.",
            exit_code=2,
            payload={"dirty_paths": dirty},
        )
    parent = read_json_from_git(root, f"{reviewed_content_head}:{PROVENANCE_TAIL_MANIFEST_PATH}")
    manifest = read_json(root / PROVENANCE_TAIL_MANIFEST_PATH)
    errors = provenance_tail_manifest_errors(
        parent,
        manifest,
        reviewed_content_head,
        target_repo,
    )
    if errors:
        raise WorkflowError("Provenance tail manifest is outside the allowlist.", exit_code=2, payload={"errors": errors})
    run_stdout(["git", "add", "--", PROVENANCE_TAIL_MANIFEST_PATH], cwd=root)
    run_stdout(["git", "commit", "--no-verify", "-m", message], cwd=root)
    publication_head = current_head(root)
    return validate_provenance_metadata_tail(
        root,
        reviewed_content_head,
        publication_head,
        target_repo=target_repo,
    )

def finalizer_publication_identity(
    root: Path,
    reviewed_content_head: str,
    target_repo: Any,
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
    errors = provenance_tail_commit_errors(
        root,
        reviewed_content_head,
        publication_head,
        target_repo=target_repo,
    )
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

def finalizer_pre_pr_provenance_tail_required(
    root: Path,
    plan: dict[str, Any],
) -> bool:
    """Return whether the current pre-PR plan still carries stale provenance."""
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    reviewed = str(git.get("branch_review_commit") or "")
    target_repo = git.get("repo")
    if re.fullmatch(r"[0-9a-f]{40}", reviewed) is None:
        raise WorkflowError("Finalizer reviewed content identity is invalid.", exit_code=2)
    payload = read_json_from_git(
        root,
        f"{reviewed}:{PROVENANCE_TAIL_MANIFEST_PATH}",
    )
    binding = provenance_source_binding(payload, target_repo, reviewed)
    publication = finalizer_publication_identity(root, reviewed, target_repo)
    if publication["metadata_tail"] is not None:
        return False
    source = payload["source"]
    return not (
        source.get("repo") == binding["source_locator"]
        and source.get("ref") == binding["source_ref"]
        and source.get("commit") == binding["source_commit"]
        and source.get("tree_state") == "clean"
        and source.get("is_mutable_ref") is False
    )

def prepare_provenance_metadata_tail(
    root: Path,
    reviewed_content_head: str,
    target_repo: Any,
) -> dict[str, Any]:
    """Apply source-owned preset bytes to one isolated target reviewed checkout."""
    if current_head(root) != reviewed_content_head:
        raise WorkflowError(
            "Provenance tail preparation requires the reviewed content HEAD.",
            exit_code=2,
        )
    with tempfile.TemporaryDirectory(prefix="guru-provenance-source-") as tmp:
        target_reviewed_checkout = Path(tmp) / "target-reviewed"
        extension_source_checkout = Path(tmp) / "extension-source"
        run_stdout(
            [
                "git",
                "worktree",
                "add",
                "--detach",
                str(target_reviewed_checkout),
                reviewed_content_head,
            ],
            cwd=root,
        )
        binding: dict[str, str] | None = None
        try:
            pre_errors = provenance_tail_checkout_errors(
                target_reviewed_checkout,
                reviewed_content_head,
            )
            if pre_errors:
                raise WorkflowError(
                    "Provenance target checkout is not a clean reviewed checkout.",
                    exit_code=2,
                    payload={"errors": pre_errors},
                )
            parent = read_json_from_git(
                target_reviewed_checkout,
                f"{reviewed_content_head}:{PROVENANCE_TAIL_MANIFEST_PATH}",
            )
            binding = provenance_source_binding(
                parent,
                target_repo,
                reviewed_content_head,
            )
            # Keep the installed platform matrix fail-closed without invoking
            # the full preset installer or changing managed files.
            provenance_apply_platform_args(parent)
            prepare_provenance_extension_source_checkout(
                root,
                extension_source_checkout,
                binding,
            )
            source_errors = provenance_extension_source_checkout_errors(
                extension_source_checkout,
                binding,
            )
            if source_errors:
                raise WorkflowError(
                    "Provenance source checkout is not clean or canonical.",
                    exit_code=2,
                    payload={"errors": source_errors},
                )
            postimage = provenance_tail_manifest_postimage(parent, binding)
            write_json(
                target_reviewed_checkout / PROVENANCE_TAIL_MANIFEST_PATH,
                postimage,
            )
            dirty = provenance_tail_git_status_paths(target_reviewed_checkout)
            if dirty != [PROVENANCE_TAIL_MANIFEST_PATH]:
                raise WorkflowError(
                    "Provenance tail producer produced changes outside the provenance manifest.",
                    exit_code=2,
                    payload={"dirty_paths": dirty},
                )
            manifest = read_json(
                target_reviewed_checkout / PROVENANCE_TAIL_MANIFEST_PATH
            )
            errors = provenance_tail_manifest_errors(
                parent,
                manifest,
                reviewed_content_head,
                target_repo,
            )
            if errors:
                raise WorkflowError(
                    "Provenance tail producer produced invalid metadata.",
                    exit_code=2,
                    payload={"errors": errors},
                )
            result = commit_provenance_metadata_tail(
                target_reviewed_checkout,
                reviewed_content_head,
                target_repo=target_repo,
            )
            publication_head = str(result["publication_head"])
        finally:
            if binding is not None and binding["mode"] == "self_hosted":
                run(
                    [
                        "git",
                        "worktree",
                        "remove",
                        "--force",
                        str(extension_source_checkout),
                    ],
                    cwd=root,
                    check=False,
                )
            run(
                [
                    "git",
                    "worktree",
                    "remove",
                    "--force",
                    str(target_reviewed_checkout),
                ],
                cwd=root,
                check=False,
            )
    run_stdout(["git", "merge", "--ff-only", publication_head], cwd=root)
    return {
        "reviewed_content_head": reviewed_content_head,
        "publication_head": publication_head,
        "metadata_tail": {
            "commit": publication_head,
            "parent": reviewed_content_head,
            "path": PROVENANCE_TAIL_MANIFEST_PATH,
        },
    }

def finalizer_current_transaction_provenance_reprepare_preflight(
    root: Path,
    task_dir: Path,
    transaction: dict[str, Any],
    current_plan: dict[str, Any],
) -> dict[str, Any]:
    """Validate an unbound ordinary transaction before rebuilding its current plan."""
    current_git = current_plan.get("git") if isinstance(current_plan.get("git"), dict) else {}
    task_ref = repo_relative(root, task_dir)
    previous_publication = str(transaction.get("publication_head") or "")
    current_reviewed = str(
        current_git.get("reviewed_content_head")
        or current_git.get("branch_review_commit")
        or ""
    )
    if (
        transaction.get("mode") != "ordinary_publication"
        or transaction.get("next_transition") != "push_content"
        or transaction.get("pr") is not None
        or transaction.get("adopted_pr") is not None
        or transaction.get("task_ref") != task_ref
        or transaction.get("repo_ref") != current_git.get("repo")
        or transaction.get("base_branch") != current_git.get("base_branch")
        or transaction.get("branch") != current_git.get("head_branch")
        or transaction.get("branch_review_commit") != previous_publication
        or not re.fullmatch(r"[0-9a-f]{40}", previous_publication)
        or not re.fullmatch(r"[0-9a-f]{40}", current_reviewed)
        or not is_ancestor(root, previous_publication, current_reviewed)
        or not provenance_tail_transaction_reprepare_eligible(
            root,
            current_plan,
            transaction,
        )
    ):
        raise WorkflowError(
            "Ordinary Finalizer transaction is not an eligible provenance reprepare predecessor.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_base_evolution_mismatch"},
        )
    remote_head = closeout_remote_branch_head(root, current_plan)
    if remote_head != previous_publication:
        raise WorkflowError(
            "Provenance reprepare requires the remote at the predecessor Publication HEAD.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_remote_not_reviewed_head",
                "reviewed_content_head": current_reviewed,
                "remote_head": remote_head,
                "fast_forwardable": bool(
                    remote_head and is_ancestor(root, remote_head, current_reviewed)
                ),
            },
        )
    return {
        "reviewed_content_head": current_reviewed,
        "local_head": current_head(root),
        "remote_head": remote_head,
        "head_branch": current_git.get("head_branch"),
        "pull_request": None,
        "parallel_publication_consumers": [],
        "tracked_task_artifacts": [],
        "base_evolution": None,
    }

def finalizer_pre_pr_provenance_reprepare_preflight(
    root: Path,
    task_dir: Path,
    plan: dict[str, Any],
    *,
    previous_transaction: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Prove the pre-PR recovery window before any producer or cleanup mutation."""
    git = plan.get("git") if isinstance(plan.get("git"), dict) else {}
    task = plan.get("task") if isinstance(plan.get("task"), dict) else {}
    reviewed_content_head = str(
        git.get("reviewed_content_head") or git.get("branch_review_commit") or ""
    )
    if re.fullmatch(r"[0-9a-f]{40}", reviewed_content_head) is None:
        raise WorkflowError(
            "Provenance reprepare reviewed content identity is invalid.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_reviewed_head_invalid"},
        )
    local_head = current_head(root)
    existing_tail_errors = (
        []
        if local_head == reviewed_content_head
        else provenance_tail_commit_errors(
            root,
            reviewed_content_head,
            local_head,
            target_repo=git.get("repo"),
        )
    )
    if existing_tail_errors:
        raise WorkflowError(
            "Provenance reprepare requires reviewed content HEAD or its valid existing tail.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_local_head_changed",
                "errors": existing_tail_errors,
            },
        )

    active_locator = str(task.get("active_locator") or "")
    archive_locator = str(task.get("archive_locator") or "")
    if (
        not active_locator
        or repo_relative(root, task_dir) != active_locator
        or (archive_locator and (root / archive_locator).exists())
    ):
        raise WorkflowError(
            "Provenance reprepare is unavailable after archive publication starts.",
            exit_code=2,
            payload={"reason_code": "provenance_reprepare_archive_started"},
        )

    head_branch = str(git.get("head_branch") or "")
    branch_ref = f"refs/heads/{head_branch}"
    branch_worktrees = [
        record
        for record in worktree_records(root)
        if record.get("branch") == branch_ref
    ]
    current_branch_worktrees = [
        record
        for record in branch_worktrees
        if Path(record.get("worktree") or "").resolve() == root.resolve()
    ]
    parallel_consumers = sorted(
        str(record.get("worktree") or "")
        for record in branch_worktrees
        if Path(record.get("worktree") or "").resolve() != root.resolve()
    )
    if not head_branch or len(current_branch_worktrees) != 1 or parallel_consumers:
        raise WorkflowError(
            "Provenance reprepare requires one exclusive publication worktree.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_parallel_publication_consumer",
                "worktrees": parallel_consumers,
            },
        )

    existing_pr = resolve_closeout_pull_request(
        root,
        str(git.get("repo") or ""),
        head_branch,
        str(git.get("base_branch") or ""),
        str(git.get("remote") or "origin"),
    )
    if existing_pr is not None:
        raise WorkflowError(
            "Provenance reprepare is unavailable after pull request creation.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_pull_request_exists",
                "pull_request": existing_pr.get("number"),
            },
        )

    remote_head = closeout_remote_branch_head(root, plan)
    if previous_transaction is not None:
        base_evolution = finalizer_current_transaction_provenance_reprepare_preflight(
            root,
            task_dir,
            previous_transaction,
            plan,
        )
    else:
        base_evolution = None
    if (
        previous_transaction is None
        and remote_head
        and remote_head != reviewed_content_head
    ):
        raise WorkflowError(
            "Provenance reprepare requires no remote branch or the remote branch at reviewed content HEAD.",
            exit_code=2,
            payload={
                "reason_code": "provenance_reprepare_remote_not_reviewed_head",
                "reviewed_content_head": reviewed_content_head,
                "remote_head": remote_head,
                "fast_forwardable": bool(
                    remote_head
                    and is_ancestor(root, remote_head, reviewed_content_head)
                ),
            },
        )
    return {
        "reviewed_content_head": reviewed_content_head,
        "local_head": local_head,
        "remote_head": remote_head,
        "head_branch": head_branch,
        "pull_request": None,
        "parallel_publication_consumers": [],
        "tracked_task_artifacts": [],
        "base_evolution": base_evolution,
    }

def finalizer_supersede_pre_pr_state(root: Path, task_dir: Path) -> list[str]:
    """Retire only owner-private Finalizer state before a fresh plan is reviewed."""
    retired: list[str] = []
    transaction = finalization_transaction_path(root, task_dir)
    for gate in (
        task_finalization_path(root, task_dir),
        task_finalization_transition_path(root, task_dir),
    ):
        if gate.is_file() and not gate.is_symlink():
            gate.unlink()
            retired.append(repo_relative(root, gate))
    if transaction.is_file() and not transaction.is_symlink():
        transaction.unlink()
        retired.append(repo_relative(root, transaction))
    retired.extend(
        ai_first_retire_owner_checkpoints(
            root,
            task_dir,
            (
                TASK_FINALIZATION_GATE_ARTIFACT,
                TASK_FINALIZATION_TRANSITION_GATE_ARTIFACT,
            ),
        )
    )
    return retired

SKILL_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"

TASK_PUBLICATION_SKILL_ID = "guru-review-task-publication"

FINALIZE_TASK_SKILL_ID = "guru-finalize-task"

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

def skill_compile_portable_pattern(pattern: str) -> SkillPortablePattern:
    """Compile the closed ASCII-source pattern subset with ECMA-262 semantics."""

    def fail(reason: str, position: int) -> None:
        raise SkillPortablePatternError(f"{reason} at offset {position}")

    for position, character in enumerate(pattern):
        if ord(character) > 0x7F:
            fail("uses a non-ASCII pattern character", position)
        if ord(character) < 0x20 or ord(character) == 0x7F:
            fail("uses a raw control character", position)

    control_escapes = {
        "t": (r"\t", 0x09),
        "n": (r"\n", 0x0A),
        "v": (r"\v", 0x0B),
        "f": (r"\f", 0x0C),
        "r": (r"\r", 0x0D),
    }
    syntax_escapes = set(r"^$\.*+?()[]{}|/")

    def parse_escape(
        position: int,
        *,
        in_class: bool,
    ) -> tuple[str, int | None, int]:
        if position + 1 >= len(pattern):
            fail("ends with an incomplete escape", position)
        marker = pattern[position + 1]
        if marker in control_escapes:
            rendered, codepoint = control_escapes[marker]
            return rendered, codepoint, position + 2
        if marker == "u":
            digits = pattern[position + 2:position + 6]
            if len(digits) != 4 or re.fullmatch(r"[0-9A-Fa-f]{4}", digits) is None:
                fail("has an invalid Unicode escape", position)
            codepoint = int(digits, 16)
            if codepoint > 0x7F:
                fail("uses a non-ASCII Unicode escape", position)
            return f"\\u{digits}", codepoint, position + 6
        if marker == "s":
            if in_class:
                return SKILL_ECMA_WHITESPACE_CLASS, None, position + 2
            return f"[{SKILL_ECMA_WHITESPACE_CLASS}]", None, position + 2
        if marker == "S":
            if in_class:
                fail("uses \\S inside a character class", position)
            return (
                skill_ecma_code_point_complement(SKILL_ECMA_WHITESPACE_CLASS),
                None,
                position + 2,
            )
        allowed_syntax = syntax_escapes | ({"-"} if in_class else set())
        if marker in allowed_syntax:
            return re.escape(marker), ord(marker), position + 2
        fail(f"uses unsupported escape \\{marker}", position)

    def parse_class(position: int) -> tuple[str, int]:
        cursor = position + 1
        negated = cursor < len(pattern) and pattern[cursor] == "^"
        if negated:
            cursor += 1
        parts: list[str] = []
        saw_item = False

        def parse_atom(atom_position: int) -> tuple[str, int | None, int]:
            character = pattern[atom_position]
            if character == "\\":
                return parse_escape(atom_position, in_class=True)
            if character == "[":
                fail("uses a nested character class", atom_position)
            if character == "-":
                return r"\-", ord("-"), atom_position + 1
            if character == "^":
                return r"\^", ord("^"), atom_position + 1
            return re.escape(character), ord(character), atom_position + 1

        while cursor < len(pattern):
            if pattern[cursor] == "]":
                if not saw_item:
                    fail("uses an empty character class", position)
                class_body = "".join(parts)
                if negated:
                    return skill_ecma_code_point_complement(class_body), cursor + 1
                return f"[{class_body}]", cursor + 1
            if pattern[cursor] == "-":
                parts.append(r"\-")
                saw_item = True
                cursor += 1
                continue

            rendered, codepoint, next_cursor = parse_atom(cursor)
            if (
                next_cursor < len(pattern)
                and pattern[next_cursor] == "-"
                and next_cursor + 1 < len(pattern)
                and pattern[next_cursor + 1] != "]"
            ):
                if codepoint is None:
                    fail("uses a character-set escape as a range endpoint", cursor)
                endpoint_rendered, endpoint_codepoint, endpoint_cursor = parse_atom(next_cursor + 1)
                if endpoint_codepoint is None:
                    fail("uses a character-set escape as a range endpoint", next_cursor + 1)
                if codepoint > endpoint_codepoint:
                    fail("uses a descending character range", cursor)
                parts.append(f"{rendered}-{endpoint_rendered}")
                cursor = endpoint_cursor
            else:
                parts.append(rendered)
                cursor = next_cursor
            saw_item = True

        fail("has an unterminated character class", position)

    translated: list[str] = []
    group_kinds: list[str] = []
    cursor = 0
    can_quantify = False
    while cursor < len(pattern):
        character = pattern[cursor]
        if character == "\\":
            rendered, _, cursor = parse_escape(cursor, in_class=False)
            translated.append(rendered)
            can_quantify = True
            continue
        if character == "[":
            rendered, cursor = parse_class(cursor)
            translated.append(rendered)
            can_quantify = True
            continue
        if character == "(":
            if pattern.startswith("(?:", cursor):
                translated.append("(?:")
                group_kinds.append("group")
                cursor += 3
            elif pattern.startswith("(?!", cursor):
                translated.append("(?!")
                group_kinds.append("negative_lookahead")
                cursor += 3
            elif pattern.startswith("(?", cursor):
                fail("uses an unsupported group or assertion", cursor)
            else:
                # Captures are deliberately erased because backreferences are outside the subset.
                translated.append("(?:")
                group_kinds.append("group")
                cursor += 1
            can_quantify = False
            continue
        if character == ")":
            if not group_kinds:
                fail("has an unmatched closing parenthesis", cursor)
            group_kind = group_kinds.pop()
            translated.append(")")
            cursor += 1
            can_quantify = group_kind == "group"
            continue
        if character == "|":
            translated.append("|")
            cursor += 1
            can_quantify = False
            continue
        if character == "^":
            translated.append("^")
            cursor += 1
            can_quantify = False
            continue
        if character == "$":
            translated.append(r"\Z")
            cursor += 1
            can_quantify = False
            continue
        if character == ".":
            translated.append(SKILL_ECMA_DOT_PATTERN)
            cursor += 1
            can_quantify = True
            continue
        if character in "*+?":
            if not can_quantify:
                fail("uses a misplaced or repeated quantifier", cursor)
            translated.append(character)
            cursor += 1
            can_quantify = False
            continue
        if character == "{":
            if not can_quantify:
                fail("uses a misplaced or repeated quantifier", cursor)
            closing = pattern.find("}", cursor + 1)
            if closing < 0:
                fail("has an unterminated bounded quantifier", cursor)
            body = pattern[cursor + 1:closing]
            match = re.fullmatch(r"([0-9]+)(?:,([0-9]*))?", body)
            if match is None:
                fail("has an invalid bounded quantifier", cursor)
            lower_text = match.group(1)
            upper_text = match.group(2)
            if len(lower_text) > 6 or upper_text is not None and len(upper_text) > 6:
                fail("uses a bounded quantifier outside the portable range", cursor)
            lower = int(lower_text)
            if upper_text not in (None, "") and lower > int(upper_text):
                fail("has a descending bounded quantifier", cursor)
            translated.append(pattern[cursor:closing + 1])
            cursor = closing + 1
            can_quantify = False
            continue
        if character in "}]":
            fail(f"has an unmatched {character}", cursor)

        translated.append(re.escape(character))
        cursor += 1
        can_quantify = True

    if group_kinds:
        fail("has an unterminated group", len(pattern))
    try:
        return SkillPortablePattern(re.compile("".join(translated)))
    except re.error as error:
        raise SkillPortablePatternError("cannot be represented by the portable pattern subset") from error

def skill_json_schema_subset_errors(
    schema: Any,
    label: str,
    *,
    relative_root: Path | None = None,
    boundary: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    local_ref_targets: dict[int, dict[str, Any]] = {}
    allowed_keywords = {
        "$schema", "$id", "$defs", "$ref", "title", "description",
        "type", "const", "enum", "allOf", "anyOf", "oneOf", "not",
        "if", "then", "else", "minLength", "maxLength", "pattern", "format",
        "minimum", "maximum", "minItems", "maxItems", "uniqueItems", "items",
        "contains", "properties", "required", "minProperties", "additionalProperties",
    }
    json_types = {"object", "array", "string", "boolean", "null", "integer", "number"}
    supported_formats = {"date-time", "uri"}

    def add(path: str, reason: str) -> None:
        errors.append(f"[schema_subset] {label} schema {reason} at {path}")

    for nonfinite_path in skill_json_nonfinite_paths(schema):
        add(nonfinite_path, "contains a non-finite number")

    def resolve_ref(reference: Any, path: str, node: dict[str, Any]) -> None:
        if not isinstance(reference, str):
            add(path, "has a non-string $ref")
            return
        if reference.startswith("#/"):
            target: Any = schema
            for encoded_part in reference[2:].split("/"):
                part = encoded_part.replace("~1", "/").replace("~0", "~")
                if not isinstance(target, dict) or part not in target:
                    add(path, "has an unresolved $ref")
                    return
                target = target[part]
            if not isinstance(target, dict):
                add(path, "has a $ref that does not resolve to an object schema")
            else:
                local_ref_targets[id(node)] = target
            return
        relative = skill_safe_relative(reference)
        if relative is None or relative_root is None or boundary is None:
            add(path, "has a non-local or invalid $ref")
            return
        target_path = relative_root / relative
        reference_errors: list[str] = []
        if skill_lstat_path(
            boundary,
            target_path,
            f"schema reference {reference}",
            reference_errors,
            kind="file",
        ) is None:
            add(path, "has an unsafe or unresolved package-local $ref")
            return
        try:
            target = skill_json_loads(target_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            add(path, "has an unreadable package-local $ref")
            return
        if not isinstance(target, dict):
            add(path, "has a package-local $ref that does not resolve to an object schema")

    def validate_nonnegative_integer(value: Any, path: str, keyword: str) -> None:
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            add(path, f"has an invalid {keyword}")

    def validate_node(node: Any, path: str) -> None:
        if not isinstance(node, dict):
            add(path, "uses a boolean or non-object schema node")
            return

        for keyword in sorted(set(node) - allowed_keywords):
            add(path, f"uses unsupported keyword {keyword}")

        if "$schema" in node and node.get("$schema") != SKILL_SCHEMA_DIALECT:
            add(path, "declares an unsupported $schema dialect")
        for keyword in ("$id", "title", "description"):
            if keyword in node and not isinstance(node.get(keyword), str):
                add(path, f"has a non-string {keyword}")
        if "$id" in node and path != "$":
            add(path, "uses a non-root $id resource boundary")
        if "$ref" in node:
            resolve_ref(node.get("$ref"), path, node)

        definitions = node.get("$defs")
        if definitions is not None:
            if not isinstance(definitions, dict):
                add(path, "has a non-object $defs")
            else:
                for name, child in definitions.items():
                    validate_node(child, f"{path}.$defs.{name}")

        expected_type = node.get("type")
        if expected_type is not None:
            if isinstance(expected_type, str):
                expected_types = [expected_type]
            elif isinstance(expected_type, list):
                expected_types = expected_type
            else:
                expected_types = []
            if (
                not expected_types
                or any(not isinstance(item, str) or item not in json_types for item in expected_types)
                or len(expected_types) != len(set(expected_types))
            ):
                add(path, "has an invalid type")

        enum = node.get("enum")
        if enum is not None:
            if not isinstance(enum, list) or not enum:
                add(path, "has an invalid enum")
            elif any(
                skill_json_equal(item, previous)
                for index, item in enumerate(enum)
                for previous in enum[:index]
            ):
                add(path, "has duplicate enum values")

        for keyword in ("allOf", "anyOf", "oneOf"):
            branches = node.get(keyword)
            if branches is not None:
                if not isinstance(branches, list) or not branches:
                    add(path, f"has an invalid {keyword}")
                else:
                    for index, branch in enumerate(branches):
                        validate_node(branch, f"{path}.{keyword}[{index}]")
        for keyword in ("not", "if", "then", "else", "items", "contains"):
            if keyword in node:
                validate_node(node.get(keyword), f"{path}.{keyword}")

        for keyword in ("minLength", "maxLength", "minItems", "maxItems", "minProperties"):
            if keyword in node:
                validate_nonnegative_integer(node.get(keyword), path, keyword)
        if (
            isinstance(node.get("minLength"), int)
            and not isinstance(node.get("minLength"), bool)
            and isinstance(node.get("maxLength"), int)
            and not isinstance(node.get("maxLength"), bool)
            and node["minLength"] > node["maxLength"]
        ):
            add(path, "has minLength greater than maxLength")
        if (
            isinstance(node.get("minItems"), int)
            and not isinstance(node.get("minItems"), bool)
            and isinstance(node.get("maxItems"), int)
            and not isinstance(node.get("maxItems"), bool)
            and node["minItems"] > node["maxItems"]
        ):
            add(path, "has minItems greater than maxItems")

        pattern = node.get("pattern")
        if pattern is not None:
            if not isinstance(pattern, str):
                add(path, "has a non-string pattern")
            else:
                try:
                    skill_compile_portable_pattern(pattern)
                except SkillPortablePatternError as error:
                    add(path, f"has an invalid portable pattern ({error})")
        expected_format = node.get("format")
        if expected_format is not None:
            if not isinstance(expected_format, str):
                add(path, "has a non-string format")
            elif expected_format not in supported_formats:
                add(path, "has an unsupported format")

        for keyword in ("minimum", "maximum"):
            value = node.get(keyword)
            if keyword in node and (
                not isinstance(value, (int, float)) or isinstance(value, bool)
                or isinstance(value, float) and not math.isfinite(value)
            ):
                add(path, f"has an invalid {keyword}")
        if (
            isinstance(node.get("minimum"), (int, float))
            and not isinstance(node.get("minimum"), bool)
            and isinstance(node.get("maximum"), (int, float))
            and not isinstance(node.get("maximum"), bool)
            and node["minimum"] > node["maximum"]
        ):
            add(path, "has minimum greater than maximum")

        if "uniqueItems" in node and not isinstance(node.get("uniqueItems"), bool):
            add(path, "has a non-boolean uniqueItems")
        properties = node.get("properties")
        if properties is not None:
            if not isinstance(properties, dict):
                add(path, "has non-object properties")
            else:
                for name, child in properties.items():
                    validate_node(child, f"{path}.properties.{name}")
        required = node.get("required")
        if required is not None and (
            not isinstance(required, list)
            or any(not isinstance(item, str) for item in required)
            or len(required) != len(set(required))
        ):
            add(path, "has an invalid required")
        if "additionalProperties" in node:
            additional = node.get("additionalProperties")
            if isinstance(additional, dict):
                validate_node(additional, f"{path}.additionalProperties")
            elif not isinstance(additional, bool):
                add(path, "has an invalid additionalProperties")

    def schema_children(node: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
        children: list[tuple[str, dict[str, Any]]] = []
        for keyword in ("$defs", "properties"):
            values = node.get(keyword)
            if isinstance(values, dict):
                children.extend(
                    (f"{keyword}.{name}", child)
                    for name, child in values.items()
                    if isinstance(child, dict)
                )
        for keyword in ("allOf", "anyOf", "oneOf"):
            values = node.get(keyword)
            if isinstance(values, list):
                children.extend(
                    (f"{keyword}[{index}]", child)
                    for index, child in enumerate(values)
                    if isinstance(child, dict)
                )
        for keyword in ("not", "if", "then", "else", "items", "contains"):
            child = node.get(keyword)
            if isinstance(child, dict):
                children.append((keyword, child))
        additional = node.get("additionalProperties")
        if isinstance(additional, dict):
            children.append(("additionalProperties", additional))
        return children

    def detect_recursive_refs(
        node: dict[str, Any],
        path: str,
        active: set[int],
        complete: set[int],
    ) -> None:
        node_id = id(node)
        if node_id in active:
            add(path, "has a recursive $ref")
            return
        if node_id in complete:
            return
        active.add(node_id)
        for child_label, child in schema_children(node):
            detect_recursive_refs(child, f"{path}.{child_label}", active, complete)
        target = local_ref_targets.get(node_id)
        if target is not None:
            detect_recursive_refs(target, f"{path}.$ref", active, complete)
        active.remove(node_id)
        complete.add(node_id)

    validate_node(schema, "$")
    if isinstance(schema, dict):
        detect_recursive_refs(schema, "$", set(), set())
    return errors
