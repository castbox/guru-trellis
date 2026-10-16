"""Create benchmark history through the existing public operation/Check wrappers.

Semantic and provider values remain the original integration fixture, not native
AI-owner or remote publication proof. No pre-existing Task history is rewritten.
"""
import hashlib
import json
import sys
import uuid
from pathlib import Path
from runtime.delivery_projection.adapter import DeliveryProjection

def prepare_history(case, assets, count):
    original_candidate = DeliveryProjection.candidate
    responses = json.loads((case.bin / 'responses.json').read_text())
    responses['checks:9'] = responses.pop('checks')
    (case.bin / 'gh').write_text('#!' + sys.executable + '\nimport json,sys\nfrom pathlib import Path\na=sys.argv[1:]\nif a[:2]==["auth","status"]:sys.exit(0)\nv=json.loads(Path(' + repr(str(case.bin / 'responses.json')) + ').read_text())\nk=next(x for x in a if x.startswith("repos/")) if a[0]=="api" else "checks:"+a[2]\nprint(json.dumps(v[k]))\n')
    (case.bin / 'gh').chmod(493)

    def update_responses(number):
        pr = {'number': number, 'state': 'CLOSED', 'merged_at': '2026-10-15T01:00:00Z', 'merge_commit_sha': case.merge, 'base': {'ref': 'main', 'repo': {'full_name': 'example/repo'}}, 'head': {'sha': case.actual, 'repo': {'full_name': 'example/repo'}}}
        responses.update({'repos/example/repo/pulls/' + str(number): pr, 'repos/example/repo/commits/' + case.merge + '/pulls': [pr], 'repos/example/repo/git/commits/' + case.merge: {'sha': case.merge, 'message': 'Merge pull request #' + str(number), 'parents': [{'sha': case.base}, {'sha': case.actual}]}, 'repos/example/repo/git/ref/heads/main': {'object': {'sha': case.merge}}, 'checks:' + str(number): {'number': number, 'state': 'MERGED', 'url': 'https://github.com/example/repo/pull/' + str(number), 'body': 'Refs #9', 'headRefOid': case.actual, 'baseRefName': 'main', 'mergeCommit': {'oid': case.merge}, 'statusCheckRollup': case.checks, 'reviewDecision': ''}})
        (case.bin / 'responses.json').write_text(json.dumps(responses))

    def deliver(number):
        review = case.review()
        review['publication_result_id'] = case.publication['result_id']
        review['reviewed_pr']['pr_number'] = number
        return case.invoke(review=review)
    (case.bin / 'responses.json').write_text(json.dumps(responses))
    assert deliver(9)['exit_id'] == 'delivered'
    flow = case.flow
    projection = case.projection
    owners = projection.declaration()['owners']
    for ordinal in range(1, count):
        number = 9 + ordinal
        flow.key = {**flow.key, 'delivery_id': str(uuid.uuid4())}
        scope_ref = projection.resolve(case.public['delivery_key'])['scope_ref']
        projection.apply({'api_version': '1.0', 'operation': 'create_delivery', 'key': flow.key, 'owner_role': 'creation', 'owner_id': owners['creation'], 'scope_ref': scope_ref, 'profile': 'pull_request'})
        directory = projection.planning_directory(flow.key)
        directory.mkdir(parents=True, exist_ok=True)
        from runtime.delivery_projection.adapter import authority_ref
        for name in ['prd.md', 'design.md', 'implement.md']:
            (directory / name).write_text('R1: current reviewed plan.\n')
        for name in ['implement.jsonl', 'check.jsonl']:
            (directory / name).write_text('')
        result = {'result_id': 'planning:' + str(number), 'owner_role': 'planning', 'owner_id': owners['planning'], 'outcome': 'accepted', 'scope_ref': scope_ref, 'plan_ref': authority_ref(directory / 'implement.md', flow.repo), 'candidate': None, 'predecessor_result_id': None, 'obligations': [], 'evidence': [scope_ref['authority']]}
        projection.apply({'api_version': '1.0', 'operation': 'record_gate', 'key': flow.key, 'owner_role': 'planning', 'owner_id': owners['planning'], 'expected_phase': 'planning', 'result': result})
        (flow.repo / 'app.txt').write_text('feature-' + str(number) + '\n')
        flow.git('add', '.')
        flow.git('commit', '-qm', 'next legitimate delivery')
        flow.head = flow.git('rev-parse', 'HEAD').strip()
        projection.begin_check(flow.key, original_candidate(projection, ['app.txt', *assets], head_ref=flow.head, base_ref=projection.content_base(flow.key)))
        original_wrapper = flow.wrapper

        def check_wrapper(skill, name, *args, success=True):
            if skill == 'guru-check-task' and name == 'invoke.sh':
                path = Path(args[1])
                value = json.loads(path.read_text())
                value['planning_accepted_result_id'] = result['result_id']
                path.write_text(json.dumps(value))
            return original_wrapper(skill, name, *args, success=success)
        flow.wrapper = check_wrapper
        checked = flow.check()
        flow.wrapper = original_wrapper
        flow.readiness(flow.full_review(checked))
        d = projection.resolve(flow.key)
        case.publication = {'result_id': 'publication:' + str(number), 'owner_id': owners['publication'], 'evidence': [scope_ref['authority']], 'profile': 'pull_request', 'candidate': d['candidate'], 'repo_ref': 'example/repo', 'pr_number': number, 'reviewed_head': flow.head, 'target_ref': 'main', 'publication_ref': {'locator': 'https://github.com/example/repo/pull/' + str(number), 'revision': 'sha256:' + hashlib.sha256(b'Refs #9').hexdigest()}}
        case.base = flow.git('rev-parse', 'main').strip()
        case.actual = flow.head
        case.make_merge()
        update_responses(number)
        projection.apply({'api_version': '1.0', 'operation': 'record_publication', 'key': flow.key, 'owner_role': 'publication', 'owner_id': owners['publication'], 'expected_phase': 'publishing', 'historical_success': True, 'result': case.publication})
        case.public = {**case.public, 'delivery_key': flow.key, 'pr_number': number}
        assert deliver(number)['exit_id'] == 'delivered'
