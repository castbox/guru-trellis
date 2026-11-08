# Public Documentation

## Audience and Language

Write top-level user documentation primarily in Chinese. Keep commands, paths,
config keys, public API identifiers and marketplace ids literal. Lower-level
source comments and technical contracts may retain their existing English or
bilingual form. Apply the complete
[clear technical writing specification](../workflow/clear-technical-writing.md).
Business repositories default to Chinese durable specifications, requirements,
designs, tasks and human-readable workflow content.

## Document Responsibilities

| Document | Responsibility |
| --- | --- |
| Root `README.md` | Product introduction, quick start, version/source choice, upgrade entry selection, daily use and links to detailed owners. |
| `trellis/presets/guru-team/README.md` | Executable build/install instructions, installed assets, platform selection and technical installation validation. |
| `trellis/workflows/guru-team/README.md` | Workflow usage and navigation to the current global workflow and Skills. |
| Canonical Skill `SKILL.md` and owned references | Complete step-local prerequisites, behavior, review, recovery and typed exits. |
| Registry, Interfaces and global workflow | Current package graph, public contracts and cross-Skill invocation/routing. |

The root README is a user entry, not another workflow or Skill contract.
Describe capabilities briefly and link their actual owners. Do not require all
three READMEs to repeat private schemas, DTO fields, complete profile/exit
lists, registry counts, internal algorithms or historical Issue narratives.
Keep shared principles in their existing SSOT and provide a direct locator.
Retired Publication/Finalizer graphs and historical validation belong to their
original versioned sources and Test evidence, not current quick-start prose.

Canonical workflow Skills live under `trellis/skills/guru-team/`. The marketplace
installs `.trellis/workflow.md`; the complete preset installs the compatible
packages, runtime and selected platform projections. A copied Skill directory
is not a standalone installation. Platform entries load and route to owners;
they do not reproduce their internal steps. AI owns semantic judgment; scripts
execute, validate or record deterministic facts under the existing contracts.

## Install and Upgrade Entries

Provide both a copyable AI request and a non-interactive new-project command
path. Use `init -y` with the explicit `guru-team` workflow and matching source;
interactive spec selection is opt-in. Link the detailed Fork build recipe
instead of copying it into every README. State the real Git, Bash, Python,
Node/package-manager and authenticated `gh` requirements without depending on
hidden machine-local setup. GitHub operations use repo-bound `gh`/`gh api`;
Git transport uses `git`.

Before installation, the AI checks existing development frameworks, local
customizations and selected platforms. New bootstrap work is a separate
explicit choice: explain `00-bootstrap-guidelines` and the proposed project
specification writes before doing them. Do not infer Git publishing permission
from installation. Preserve current-dialogue authorization boundaries; never
persist authorization or its process in repository or runtime artifacts.

Upgrade navigation selects the existing owner from the actual goal:

- One checkout's tools/workflow/Skills with Task/session preservation:
  `guru-upgrade-tools`.
- Complete installation upgrade including required Task/schema migration:
  `guru-upgrade-installation`.
- Independently selected legacy Task conversion or historical maintenance:
  `guru-maintain-legacy-task`.

These Skills own old-operation disposition, exact source pairing, target/write
scope, recovery, rollback and installed verification. README links them rather
than copying those procedures. A diagnostic or missing prerequisite does not
choose another route. Updating source files does not establish target adoption.
Ordinary update/apply does not replace a required migration. Where workflow
replacement applies, `--create-new` previews and explicit `--force` applies the
same provider. Resolve `.new`/`.bak` through the original owner and validate
actual installed assets before reporting success.

## Version and Evidence Sources

Distinguish a published immutable Guru tag from an explicitly selected
unpublished candidate. Workflow marketplace and preset use the same selected
Guru ref; candidate trials resolve to a real remote-addressable full SHA.
Unpublished `main` is not the default stable release. Guru extension revision,
release tag and Fork source/CLI version are separate identities.

The selected checkout's
`trellis/presets/guru-team/source/trellis-source.json` is the sole current Fork
source record. Read its repository, commit, package manager and CI identity;
build the matching CLI/Core with the normal dependency layout and original
modes. Do not keep a second current Fork SHA/CI table in README or this writing
specification. Equal versions, an old tarball, a global CLI or mutable latest
cannot substitute for that build. Build-origin markers follow the existing
successful-build contract; validation alone does not create one.

Read current Requirements/Design/Test and Architecture through
`docs/{requirements,design,test,architecture}/README.md`. The original owners
control definitions and promotion. Preserve historical test observations with
their original sources and cutoff. Static validation, local candidates,
installed samples, native Agent behavior, business recovery and Release gates
establish different claims. Report only the layer actually exercised.

## Validation and Safety

Review changed prose against its real audience, current owners and unchanged
consumers. Preserve public anchors with direct consumers, including the
extension manifest's `README.md#guru-team-extension-version`. Check changed
relative links/anchors, commands and shell-block syntax, plus `git diff --check`.
Use relevant existing package/installed/drift checks when Skill projections
change. Documentation edits do not require a new self-proving text test or a
full installation/upgrade/Release matrix; use
[validation scope ownership](../workflow/quality-guidelines.md#validation-scope-ownership).

Never publish credentials, sensitive raw logs, `.env` content, database URLs or
signed URLs. Public packages contain reusable contracts and sanitized examples;
business requirements and private runtime state remain in business repositories.
