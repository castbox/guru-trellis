"""Post-owner structural smoke fixture; causal cognition uses the focused native matrix."""
from pathlib import Path
import json
import subprocess
import os
from adapters.eval.eval_constants import OWNER_INPUT, OWNER_RESULT, OWNER_INVOCATION
from adapters.eval.fixture_io import run_git
from adapters.eval.eval_support import package_tree_sha256


def stage(request: dict, fixture: Path) -> tuple[Path, Path, dict]:
    package = fixture / '.trellis/guru-team/skills/packages/guru-qualify-root-cause'
    if package_tree_sha256(package) != package_tree_sha256(Path(request['package_root'])):
        raise ValueError('root qualification fixture package differs from selected package')
    (fixture / 'README.md').write_text('# Display feature\n\nScope adds labels only, with no incident or protection mechanism.\n')
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'stage root qualification structural smoke')
    head = run_git(fixture, 'rev-parse', 'HEAD')
    result = json.loads((package / 'examples/semantic-result.json').read_text())
    public = json.loads((package / 'examples/public-task-free-pre-write-input.json').read_text())
    public.update(target_locator='request:display-feature', candidate_refs=['display-feature'],
        candidate_locators=[{'candidate_ref':'display-feature','locators':['path:README.md']}])
    public['target'].update(repo_locator='.',request_locator='request:display-feature',checkout_head=head,bounded_paths=['README.md'])
    result['public_input'] = public
    result['candidate_results'][0]['candidate_ref'] = 'display-feature'
    result['ai_review_gate']['reviewed_candidate_refs'] = ['display-feature']
    target = fixture / '.trellis/guru-team/scripts/bash/run-skill-command.sh'
    # Validate fixture transport through the public wrapper, without a causal claim.
    checked = subprocess.run([str(package / 'scripts/invoke.sh'), '--invocation', '-'],
        cwd=fixture, input=json.dumps({'schema_version':'1.0','semantic_result':result}),
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    if checked.returncode:
        raise ValueError('root structural fixture public invocation failed: ' + checked.stderr)
    for relative, value in [(OWNER_INPUT, public), (OWNER_RESULT, result),
                            (OWNER_INVOCATION, {'schema_version':'1.0','semantic_result':result})]:
        path = fixture / relative
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(value)+'\n')
    return package, target, {}
