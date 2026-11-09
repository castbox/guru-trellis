# Capture And Read A History Preview

Use a persistent Node REPL with top-level `await`. Run the JavaScript blocks in
order, in separate cells. The current AI must first complete the contract's
base validation and current-state review. Keep its actual Discovery public
input in `discoveryInput` and its actual Sync `base_current` transition in
`baseCurrent`. These are existing call-local objects, not example identities.
Set `reviewedRepositoryRoot` to that review's actual repository root before
the first block. The REPL itself can have a different cwd.

The example uses the installed public wrappers and Node standard libraries.
It writes no files. All helpers receive their context explicitly so a later
cell cannot accidentally use a helper's captured older repository cwd.

## Capture Complete Bytes Before Parsing

```js
var historySpawn = (await import('node:child_process')).spawn;
var historyPath = await import('node:path');
var historyContext = {
  cwd: reviewedRepositoryRoot,
  package: '.trellis/guru-team/skills/packages/guru-discover-change-context',
  query: structuredClone(discoveryInput.change_input),
  transition: structuredClone(baseCurrent),
};
var captureHistoryCommand = async function (context, script, args) {
  return await new Promise((resolve, reject) => {
    var child = historySpawn('bash', [
      historyPath.resolve(context.cwd, context.package, 'scripts', script),
      ...args,
    ], { cwd: context.cwd, stdio: ['ignore', 'pipe', 'pipe'] });
    var stdout = [], stderr = [];
    child.stdout.on('data', chunk => stdout.push(chunk));
    child.stderr.on('data', chunk => stderr.push(chunk));
    child.on('error', reject);
    child.on('close', (code, signal) => resolve({
      code, signal,
      stdout: Buffer.concat(stdout),
      stderr: Buffer.concat(stderr),
    }));
  });
};
var captureHistoryPreview = async function (context) {
  return await captureHistoryCommand(context, 'preview-change-context-history.sh', [
    '--root', context.cwd,
    '--query-json', JSON.stringify(context.query),
    '--source-transition', JSON.stringify(context.transition),
  ]);
};
var historyCapture = await captureHistoryPreview(historyContext);
console.log(JSON.stringify({
  exit_code: historyCapture.code, signal: historyCapture.signal,
  stdout_bytes: historyCapture.stdout.length,
  stderr_bytes: historyCapture.stderr.length,
}));
```

Check the actual exit code. On nonzero exit or a signal, retain the captured
failure and read its stdout/stderr in bounded ranges for the original owner's
error handling. Do not parse it as a successful preview or replace it with an
empty result. A spawn error is also a real command failure.

```js
if (historyCapture.code !== 0 || historyCapture.signal !== null) {
  throw new Error('History preview failed; inspect the captured failure and use the original route.');
}
var historyReceipt = JSON.parse(historyCapture.stdout.toString('utf8'));
var historyPreview = historyReceipt.result;
console.log(JSON.stringify({
  schema_version: historyReceipt.schema_version,
  formal_exit: historyReceipt.formal_exit,
  candidates: historyPreview.candidates.length,
  manifest_rows: historyPreview.manifest.length,
}));
```

This direct process capture retains complete `Buffer` chunks until `close`,
then decodes the combined bytes once. Do not decode each chunk independently:
a UTF-8 character can cross chunk boundaries. The intermediate receipt has
`schema_version=1.0` and `formal_exit=false`; only `result` is the preview.

The complete JSON never passes through a shell tool's returned text. If a shell
tool is used instead, both its internal return budget and the outer tool's
model display budget must fit the result. Increasing only the outer budget
cannot recover bytes already removed by the inner tool. A successful capture
still needs bounded model displays below.

## Read Every Candidate In Small Batches

The following helpers keep the preview's order and expose facts only. Lengths
and offsets count Unicode code points in each field's JSON representation,
including JSON quotes and escapes. Use the same representation for subsequent
reads. Every candidate and every field remains available in `historyPreview`.

```js
var historyFieldText = function (candidate, path) {
  var value = path.reduce((part, key) => part[key], candidate);
  return Array.from(JSON.stringify(value));
};
var showHistoryCandidates = function (preview, start, count = 1, width = 120) {
  var rows = preview.candidates.slice(start, start + count).map(candidate => {
    var fields = [
      ['matched_clues'],
      ...Object.keys(candidate.index_projection).map(key => ['index_projection', key]),
    ].map(path => {
      var text = historyFieldText(candidate, path);
      return { path, length: text.length, offset: 0,
        text: text.slice(0, width).join(''), next_offset: Math.min(width, text.length) };
    });
    return { candidate_id: candidate.candidate_id,
      finish_summary_path: candidate.finish_summary_path, fields };
  });
  console.log(JSON.stringify({ start, next: start + rows.length,
    total: preview.candidates.length, rows }));
};
var readHistoryField = function (preview, id, path, offset = 0, count = 600) {
  var candidate = preview.candidates.find(row => row.candidate_id === id);
  if (!candidate) throw new Error('Use an ID from this complete preview.');
  var text = historyFieldText(candidate, path);
  console.log(JSON.stringify({ candidate_id: id, path, offset,
    length: text.length, next_offset: Math.min(offset + count, text.length),
    text: text.slice(offset, offset + count).join('') }));
};
showHistoryCandidates(historyPreview, 0);
```

Repeat the last call in separate cells with starts `1`, `2`, and so on until
`next` equals `total`. A zero-candidate result needs no candidate reads and
retains the contract's empty selection and `not_needed` mem handling. Batch
sizes and widths are display choices, not candidate limits or sufficiency
rules. Inspect what actually reaches the model. If a display is truncated,
reduce `count` or `width` and reread that batch from the same in-memory result.
Do not treat a truncated display as an exclusion or a reason to stop Discovery.

For each returned candidate, the AI judges what information it needs to select
or exclude it. Read missing matched clues, problem, outcome or other fields
before that judgment. These example calls use the first actual candidate; set
the ID, path and offset to the candidate and missing range under review.

```js
var historyCandidateId = historyPreview.candidates[0]?.candidate_id;
if (historyCandidateId) {
  readHistoryField(historyPreview, historyCandidateId, ['index_projection', 'problem'], 0, 600);
}
```

Continue with the returned `next_offset` until the needed field is complete;
use smaller counts if necessary. The same helper accepts `['matched_clues']`,
`['index_projection', 'outcome']` or any actual candidate field path. Short
snippets alone do not establish complete reading or sufficient evidence. Review
all returned candidates and author each selection or exclusion yourself. The
helpers do not rank again, filter the returned set or decide relevance.

## Deep Read Selected Evidence And Continue

After selecting one to three candidates under the original contract, use its
public source reader to deep-read the selected archive and explicit supporting
files. For example, set the path to an actual selected candidate's summary:

```js
// Set historySelectedId to the current AI's actual selection before this cell.
var historySelectedPath = historyPreview.candidates.find(
  row => row.candidate_id === historySelectedId)?.finish_summary_path;
if (historySelectedPath) {
  var historySourceCapture = await captureHistoryCommand(historyContext,
    'read-change-context-source.sh', [
      '--source-transition', JSON.stringify(historyContext.transition),
      '--path', historySelectedPath,
    ]);
  if (historySourceCapture.code !== 0 || historySourceCapture.signal !== null) {
    throw new Error('Source read failed; retain the failure and use the original route.');
  }
  var historySource = JSON.parse(historySourceCapture.stdout.toString('utf8')).result;
  console.log(JSON.stringify({ path: historySource.path, blob: historySource.blob,
    content_length: Array.from(historySource.content).length }));
}
```

Read `historySource.content` in consecutive bounded ranges through its end,
then read other selected evidence required by the question. Capture success,
field lengths and candidate coverage are facts, not an AI Gate pass. Complete
the original semantic review, Gate, record/check/invoke and consume the actual
typed exit. The recorder receipt's `result` replaces only the envelope's
`owner_result`; the checker receipt does not replace it.

If only display was shortened, reuse the complete in-memory result and read the
missing ranges automatically. If the result is lost, restore the original
query and actual source transition from this call's existing inputs, rerun
`captureHistoryPreview` with that same context, check success and parse again.
This recovery continues the same fixed baseline and investigation; it does not
start a new broad search or silently adopt a newer commit. Real source gaps,
command failures and stale/mismatch facts retain their original routes. Do not
ask the user to continue solely because of display truncation. Add no preview
cache, checkpoint, tracked evidence or authorization state.
