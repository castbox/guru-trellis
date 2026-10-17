# Research: Three bounded installation observations

- Query: Give original coordinator causal/normal-path evidence for three #599 implementation observations, without expanding scope.
- Scope: internal
- Date: 2026-10-17

## Findings

| Candidate | Live and exact-base evidence | Normal reproduction | #599 necessity |
| --- | --- | --- | --- |
| `platform-cli-mock-python-keyword` | Exact GitHub contents at `ea9998c36`: `test_guru_platform_inventory.py` byte-identical to current; lambda at line 171 takes only four positional args. Base installer main line 2883 and current line 2888 both call `install_assets(..., python=args.python)`. | Actual current `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=trellis/presets/guru-team/scripts/python python3 -m unittest test_guru_platform_inventory.InstallerPlatformCliTest -v`: default platforms and repeated platforms both error `unexpected keyword argument python`; unknown-platform parser test passes. No target mutation. | Existing test-double signature defect, not introduced by #599. A narrow mock update is necessary to execute this relevant platform suite for AC7 without changing production behavior. Do not classify it as a new writing-rule runtime defect. |
| `dogfood-legacy-inventory-apply` | `delivery_installation.py` exact-base/current byte-identical. `diagnose_delivery_installation():92-134` scans all `**/task.json`, treats missing/non-2.0 schema as legacy and blocks `upstream_delivery_migration_required`. Current read-only snapshot has 228 legacy-schema records, including `.trellis/tasks/archive/2026-07/07-03-1-enhance-guru-team-workflow-middle/task.json` with no schema_version. | `install_assets():2411-2416` ordinary path invokes `require_delivery_installation()` before installing. Existing old archives are sufficient to reach this preflight without any forged inputs. This research did not rerun full apply. | Environment/adoption prerequisite for dogfood AC6, not a new requirement to migrate Task data or weaken ordinary installation. Existing `guru-upgrade-tools` explicit tools-only path is the bounded owner. |
| `apply-cwd-runtime-location` | Exact base/current `_guru_temporary_directory():122-136` identical; `apply.sh` entirely identical. Function checks only `Path.cwd()/.trellis/guru-team/runtime` and `Path.cwd()/trellis/skills/guru-team/runtime`. Script path does not change cwd. | Coordinator reports a complete new target invoking an absolute source apply script fails but source-cwd invocation succeeds. This research independently executed the exact extracted function from a cwd without either runtime: same `RuntimeError: Guru temporary lifecycle runtime is unavailable`, before entering any context or writing files. This is mechanism confirmation, not another full-install result. | Pre-existing cwd dependency. Root README:127 explicitly documents `(cd "$GURU_SOURCE" && bash ... --repo "$TARGET_REPO")`, so AC6 has a supported working path. Not necessary to expand #599 into cwd-independent installer resolution. |

### Tools-only evidence for candidate 2

`guru-upgrade-tools/references/contract.md:13-18` supports isolated development `local_candidate`; lines 29-33 preview old tools without parsing old Tasks; lines 53-58 exclude Task/planning/archive/workspace/session/private-control writes and do not require a valid old Task parser. `delivery_installation.py:143-164` requires a genuinely applied public tools operation and current capability APIs, then reports `task_inventory=preserved_unparsed`. `tools_owner.py:365-367` calls the existing installer with `checkout_local=True, tools_only=True` plus original operation context. No old Task migration, inventory editing or fake manifest is needed. The main coordinator is executing this owner; research makes no claim it completed.

### Recommended coordinator disposition

1. Qualify the test-mock observation as pre-existing, normal and narrowly relevant to current AC7 validation; permit test-only repair if the original owner accepts it.
2. Treat legacy inventory as the existing tools-only maintenance boundary and recover the original supported operation; preserve archives unchanged.
3. Use documented source-cwd apply for AC6. Record the pre-existing unsupported/undocumented invocation limitation; do not make cwd-generalization a current blocking finding or required follow-up.

## Caveats / Not Found

The original qualification owner must select the formal classification; this research is evidence only. No production file, Task identity, archive, Git state or lifecycle state was changed. Remote base was read through exact-ref GitHub contents API, not assumed from current main. The only file written is this role-required concise research note.
