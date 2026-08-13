# Semantic Retrieval Contract 1.0

This is the single Guru Team contract for semantic retrieval across current
repository facts, durable documentation, Git and GitHub history, and local
conversation history. Semantic owners reference this file; they do not copy
its rules into workflows, launchers, public DTOs, or search scripts.

## Concept Family

Before searching, the AI derives the smallest concept family that adequately
covers the current question from live authority and repository evidence. It
must include every applicable category below and omit inapplicable variants:

- the user's original Chinese or English wording;
- Chinese formal names, colloquial names, abbreviations, and historical names;
- English terms, synonyms, abbreviations, and historical names;
- exact code symbols, configuration keys, CLI tokens, schema fields, error
  text, and path literals;
- legacy aliases that actually occur in current or historical evidence.

This is semantic expansion, not a requirement to run every query in two
languages. Add a language variant only when it can retrieve relevant evidence
that the other applicable terms may miss. Exact errors and literals such as
`OBJECT_ACCESS_DENIED`, `reviewed_content_sha256`, and `workspace_ref` must
always retain an original exact lookup; do not translate or paraphrase that
lookup. An additional semantic term is allowed only when evidence shows it has
separate recall value.

## Evidence Coverage

The AI selects queries and judges whether their combined results cover the
applicable concept family. It records in the current semantic gate only the
concept scope, its authority/evidence sources, the key evidence used, and any
remaining coverage boundary. Query count and raw hit count do not prove
sufficiency.

A negative conclusion about an existing implementation, entry, test, fixture,
external validation, historical decision, former contract, duplicate Issue or
PR, field, helper, schema/config consumer, Docs authority, or prior problem is
permitted only after the applicable Chinese concepts, English terms, exact
literals, and evidenced legacy aliases have been covered. A zero-result search
in one language cannot independently support "not found" or "does not exist."

Examples of one concept spanning evidence surfaces include:

- `发布门禁` in Chinese Docs and `release_gate` in English code;
- `stale context` in an English Issue and `上下文过期` in Chinese commits or
  sessions;
- current `workspace mapping`, legacy `handoff map`, and exact `workspace_ref`.

## Ownership Boundary

The AI owns concept-family construction, query selection, evidence-coverage
judgment, and conclusion sufficiency. Python and shell can only execute queries
supplied by the AI, read facts, and validate objective structure. They must not
generate synonyms, translate queries, count hits as a gate, or decide semantic
pass or route.

The retrieval owners are `guru-discover-change-context`,
`guru-clarify-requirements`, `trellis-research`, `trellis-session-insight`,
`trellis-implement`, `trellis-check`, `guru-check-task`, and
`guru-review-branch`. Other workflow Skills and deterministic executors do not
gain broad retrieval ownership from this contract.

## Artifact Boundary

Do not persist a raw search report, per-query transcript, long-lived keyword
list, query approval, query digest, reviewer metadata, or authorization state.
Do not add search-process fields to public inputs or typed outputs. Promote a
term mapping into durable Docs only when it is itself a lasting domain or
workflow contract with a direct future consumer.
