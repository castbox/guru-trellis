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

def closeout_json_artifact_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

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
    return sorted(set(move_paths) & set(CLOSEOUT_ARCHIVE_CORE_ARTIFACTS))

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
    existing_plan: dict[str, Any] = {}
    plan_schema_version = FINALIZATION_PLAN_SCHEMA_VERSION
    existing_task = existing_plan.get("task") if isinstance(existing_plan.get("task"), dict) else {}
    existing_projection = (
        existing_plan.get("projection")
        if isinstance(existing_plan.get("projection"), dict)
        else {}
    )
    archive_month_now = current_archive_month()
    existing_archive_month = (
        closeout_archive_month(existing_plan) if existing_plan else None
    )
    same_archive_month = existing_archive_month == archive_month_now
    archive_locator = str(existing_task.get("archive_locator") or "")
    if archive_locator and not same_archive_month:
        archive_locator = f".trellis/tasks/archive/{archive_month_now}/{task_dir.name}"
    if not archive_locator:
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
    if existing_projection:
        task_files = set(existing_projection.get("move_paths", []))
        unexpected_task_files = sorted(observed_task_files - task_files)
        if unexpected_task_files:
            raise WorkflowError(
                "Persisted finalization plan does not own newly added task artifacts.",
                exit_code=2,
                payload={"unexpected_task_files": unexpected_task_files},
            )
    else:
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
    existing_summary_template = (
        existing_projection.get("summary_template")
        if isinstance(existing_projection.get("summary_template"), dict)
        else {}
    )
    generated_at = str(
        existing_summary_template.get("generated_at")
        or ""
    )
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", generated_at):
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
    existing_plan: dict[str, Any] | None,
    allow_base_evolution_supersession: bool = False,
) -> str:
    if existing_plan is not None and not allow_base_evolution_supersession:
        plan_task_ref = str(existing_plan.get("task", {}).get("active_locator") or "")
        branch_review_commit = str(
            existing_plan.get("git", {}).get("branch_review_commit") or ""
        )
        if plan_task_ref != task_ref:
            raise WorkflowError(
                "Persisted finalization plan does not match the current task.",
                exit_code=2,
            )
    else:
        if publication_ready is None:
            raise WorkflowError(
                "Initial closeout requires a Publication ready DTO or immutable plan.",
                exit_code=2,
            )
        branch_review_commit = str(
            publication_ready.get("branch_review_commit") or ""
        )

    publication_mismatch = publication_ready is not None and (
        publication_ready.get("profile") != "publication_ready"
        or publication_ready.get("task_ref") != task_ref
        or publication_ready.get("branch_review_commit") != branch_review_commit
    )
    if (
        publication_ready is not None
        and existing_plan is not None
        and not allow_base_evolution_supersession
    ):
        publish = existing_plan.get("publish", {})
        payload_title = publication_ready.get("pr_title")
        payload_body = publication_ready.get("pr_body")
        publication_mismatch = publication_mismatch or (
            payload_title != publish.get("title")
            or payload_body != publish.get("body")
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
    allowed_current_gate: dict[str, Any] | None = None,
    current_finalizer: bool = False,
) -> dict[str, Any]:
    official_after_archive_hook_state(root)
    existing_plan = None
    expected_task_ref = repo_relative(root, task_dir)
    branch_review_commit = resolve_closeout_branch_review_commit(
        expected_task_ref,
        publication_ready=publication_ready,
        existing_plan=existing_plan,
        allow_base_evolution_supersession=False,
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

def closeout_commit_tree_entry(root: Path, commit: str, path: str) -> tuple[str, str, str]:
    proc = run(["git", "ls-tree", commit, "--", path], cwd=root, check=False)
    rows = [line for line in proc.stdout.splitlines() if line]
    if proc.returncode != 0 or len(rows) != 1:
        raise WorkflowError(
            "Closeout transaction parent is missing one exact tracked move path.",
            exit_code=2,
            payload={"commit": commit, "path": path, "stage": "pre-archive-continuity"},
        )
    metadata, separator, actual_path = rows[0].partition("\t")
    fields = metadata.split()
    if separator != "\t" or actual_path != path or len(fields) != 3:
        raise WorkflowError(
            "Closeout evidence tree entry is ambiguous.",
            exit_code=2,
            payload={"commit": commit, "path": path, "stage": "pre-archive-continuity"},
        )
    return fields[0], fields[1], fields[2]

def closeout_commit_blob_bytes(root: Path, commit: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(
            "Closeout could not read an immutable Git blob.",
            exit_code=2,
            payload={"commit": commit, "path": path},
        )
    return proc.stdout

def context_canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def context_digest(value: Any) -> str:
    return hashlib.sha256(context_canonical_bytes(value)).hexdigest()

def context_sort(values: set[str] | list[str]) -> list[str]:
    return sorted(set(values), key=lambda item: item.encode("utf-8"))
