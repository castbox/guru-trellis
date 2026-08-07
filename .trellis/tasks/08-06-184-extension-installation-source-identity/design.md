# #184 技术设计：目标仓库与扩展源双身份验证

## 1. Design Decision

采用一个 semantic owner、一个 deterministic runtime、两个隔离 checkout。Public input
继续描述 target invocation；extension source 由 target installed manifest 解析。Taskless
standalone 的 locator fallback 是 source selection 的受限分支，不是第二套验证标准。

Private/execution evidence 使用新的 current-only schema identity。Public inputs、四个 exit
id 与 consumer DTO 保持兼容；不为旧 private schema 增加 reader、alias 或 migration branch。

## 2. Identity Model

```text
public invocation
  -> target_repository(repo, remote, ref, resolved_head)
       -> target_checkout
       -> branch review continuity
       -> reviewed-content identity
  -> installed extension manifest
       -> extension_source(repo, locator, ref, direct_oid, commit)
       -> extension_source_checkout
       -> installer + canonical assets + ownership + sidecars
  -> isolated install/project
       -> installed asset inventory and update/reapply facts
```

`repo_ref` remains the target repository public identity. Source provenance never rewrites it.
Every source-dependent command and asset fact names `extension_source_checkout`; every target
content fact names `target_checkout` or the current active task root.

## 3. Source Resolver

Introduce one structured resolver shared by execute/check freshness paths:

```text
resolve_extension_source(target_root, public_input, task_bearing) ->
  selection: manifest | standalone_fallback
  manifest_provenance: available | not_available
  repo: owner/repo
  locator: https://github.com/owner/repo.git
  requested_ref: manifest/public value
  resolved_ref: 40-hex commit | refs/heads/* | refs/tags/*
  direct_oid: 40-hex
  commit: 40-hex direct-or-peeled commit
  tree_state: clean | dirty
  is_mutable_ref: bool
  ref_matches_commit: bool
```

Resolution rules:

1. Task-bearing paths require a regular current installed manifest in target root.
2. Canonicalize manifest source to a credential-free GitHub repo and HTTPS clone locator.
3. When `requested_ref` is a full 40-hex commit OID, initialize the isolated source checkout,
   configure the canonical locator as `origin`, and fetch exactly that OID through `origin`.
   Resolve `FETCH_HEAD^{commit}` and require it to equal both `requested_ref` and manifest
   `source.commit` before reading source assets. Preserving `origin` is required so source-owned
   nested preset/throwaway installs can record complete `source.repo` provenance.
4. For branch and tag refs, resolve direct and optional peeled rows with one explicit
   `git ls-remote` request. Annotated tag selects peeled commit; branch/lightweight tag selects
   direct commit.
5. Compare every selected commit with manifest `source.commit`; no ancestor or branch-tip
   substitution is accepted.
6. A malformed manifest blocks. Only taskless standalone with an absent manifest may select the
   public locator fallback and record `manifest_provenance=not_available`.

Preset installation from a Git worktree records the current full source commit as both
`source.ref` and `source.commit`, with `is_mutable_ref=false`. The manifest explicitly describes
the source bytes observed before the manifest-bearing target commit; it does not self-reference
that later target commit. Archive installation without Git provenance retains its existing
non-verifiable archive shape and cannot satisfy a task-bearing manifest path.

## 4. Executor Flow

The temporary work root contains three disjoint roots:

```text
<tmp>/target-checkout
<tmp>/extension-source-checkout
<tmp>/install/project
```

### 4.1 Target checkout

- Resolve and clone target remote/ref, checkout the exact target commit, and compare live HEAD.
- Compute remote target reviewed-content identity from target checkout.
- For task-bearing calls, compute local target identity from the active task worktree and compare
  it with `branch_review_commit`/remote target identity.
- Do not locate installer, canonical package bytes, ownership, or sidecars here.

### 4.2 Extension source checkout

- For a commit OID ref, initialize the isolated checkout, configure its canonical `origin`, fetch
  exactly that OID through the remote, detach at the fetched commit and compare live HEAD with
  source provenance. For branch/tag refs, retain the resolve-then-clone path and detach at the
  selected commit.
- Locate `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` only here.
- Derive workflow source, canonical asset expectations, ownership inventory and source package
  bytes only from this checkout.
- Execute installer into the isolated install root and inspect installed assets from
  `<tmp>/install/project`.

### 4.3 Result rule

Machine execution is passed only when target continuity, source provenance, both checkout HEADs,
throwaway lifecycle, installed inventory, ownership and zero-sidecar facts pass. Semantic
`verified` additionally requires the existing AI adequacy/finding gate.

## 5. Evidence Contract

Execution facts and `marketplace-verification.json` require two explicit objects:

- `target_repository`: `repo_ref`, `remote`, `ref`, `resolved_head`, local/remote reviewed-content
  identity and target checkout facts.
- `extension_source`: selection, manifest provenance, repo, safe locator, requested/resolved ref,
  direct oid, selected commit, tree state, mutability and commit-match facts.

Command records use a closed checkout owner label. Source-dependent asset expectations and
ownership rows must reference source facts. The checker re-resolves both identities and rejects
cross-owned or stale evidence.

Public outputs remain unchanged and minimal. No source locator inventory, direct tag object,
command transcript, asset list, machine-local path or credential material crosses the Skill DTO.

## 6. Distribution Strategy

Canonical edits occur in:

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` and its tests;
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/**`;
- preset manifest/installer tests and durable specs/README surfaces.

Then run the canonical preset installer to update `.trellis/guru-team` and selected platform
copies. Handle every generated `.new`/`.bak`, verify byte equality, and leave no recursive
sidecars. Direct manual editing of installed/platform copies is not an implementation path.

## 7. Compatibility And Failure Boundary

- Breaking change is limited to private/execution current-only schema. Public API ids and DTO
  consumers remain stable.
- Missing/invalid manifest, unsafe locator, unresolved source ref, direct/peeled mismatch,
  fetched OID mismatch, manifest commit drift, either checkout HEAD mismatch, target content drift,
  source installer absence, incomplete inventory, ownership drift or sidecars fail closed at their
  owning boundary.
- Runtime continues to use Python standard library plus explicit `git` subprocesses.
- Error artifacts and public errors expose stable reason codes/remediation without echoing a
  sensitive locator.

## 8. Docs SSOT Plan

Strategy: `ssot_first`.

| SSOT | Required change |
| --- | --- |
| `.trellis/spec/workflow/data-contracts.md` | target/source private evidence shape and bindings |
| `.trellis/spec/workflow/companion-scripts.md` | resolver, dual checkout and command ownership |
| `.trellis/spec/workflow/skill-package-contract.md` | current-only schema upgrade and public DTO boundary |
| `.trellis/spec/preset/installer.md` | manifest provenance and source-root install contract |
| `.trellis/spec/workflow/quality-guidelines.md` | separation/tag/fallback/redaction/stale test matrix |
| `.trellis/spec/docs/public-docs.md` | public explanation and evidence limits |
| workflow/preset README | operator-visible source/target behavior and validation |

Workflow phase routing is unchanged, so canonical `.trellis/workflow.md` semantics are checked
for consistency but need no new route.
