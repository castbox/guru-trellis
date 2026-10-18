"""Task-wide Completion: review current authority and all recorded facts.

No current Delivery is required. The caller owns semantic completeness; the
public operation only verifies the recorded conclusion's exact applicability.
"""
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.task_lifecycle import LifecycleContractError


def invoke(root, package, public, semantic):
    validate_json(public, package / ('schemas/public-' + public['profile'].replace('_', '-') + '-input-1.0.schema.json'), 'input')
    validate_json(semantic, package / 'schemas/semantic-delivery-result-1.0.schema.json', 'semantic_result')
    projection = DeliveryProjection(root, public['task_ref'])
    try:
        record = projection.read_record()
        key = {'task_id': record['id'], 'lifecycle_generation': record['lifecycle_generation']}
        scope = record['accepted_scope']
        results = [row['delivery_result']['result_id'] for row in record['deliveries'] if row['delivery_result']]
        if public['task_key'] != key or semantic['reviewed_task_key'] != key:
            raise CommandError('stale_identity', 'task_key', 'Review the exact current Task generation.', 3)
        if scope is None:
            raise CommandError('stale_identity', 'accepted_scope', 'Refresh the Task scope owner before Completion.', 3)
        projection._call(projection.api.delivery_store.verify_authority, root, scope)
        if ((public['profile'], public['mode']) != (semantic['profile'], semantic['mode'])
                or semantic['reviewed_scope'] != scope
                or sorted(semantic['reviewed_delivery_result_ids']) != sorted(results)):
            raise CommandError('stale_identity', 'semantic_result', 'Review current scope and every actual Delivery fact, including history.', 3)
        if public['profile'] == 'delivery_reactivation_validation':
            anchor = public['reactivation_anchor']
            if anchor.get('task_id') != key['task_id'] or anchor.get('archived_generation') != key['lifecycle_generation'] - 1:
                raise CommandError('stale_identity', 'reactivation_anchor', 'Review the preceding archived generation.', 3)
        exit_id = semantic['route']['typed_exit']
        if exit_id == 'completed':
            if semantic['remaining_work_refs']:
                raise CommandError('stale_identity', 'remaining_work_refs', 'Accepted work remains; select its actual continuation.', 3)
            owner = projection.declaration()['owners']['completion']
            result = {'result_id': semantic['result_id'], 'owner_id': owner, 'evidence': semantic['evidence'],
                      'lifecycle_generation': key['lifecycle_generation'], 'accepted_scope': scope,
                      'delivery_result_ids': results, 'outcome': 'completed'}
            existing = next((r for r in record['completion_results'] if r['result_id'] == result['result_id']), None)
            if existing is not None and existing != result:
                raise CommandError('stale_identity', 'result_id', 'Recover the exact recorded Completion conclusion.', 3)
            if existing is None:
                projection.apply({'api_version': '1.0', 'operation': 'complete_task', 'key': key,
                                  'owner_role': 'completion', 'owner_id': owner, 'result': result})
            output = {'exit_id': 'completed', 'result_ref': {**key, 'result_id': result['result_id']}}
        elif exit_id == 'blocked':
            output = {'exit_id': exit_id, 'reason': semantic['route']['reason']}
        else:
            output = {'exit_id': exit_id, 'task_ref': public['task_ref'], 'task_key': key, 'reason': semantic['route']['reason']}
        validate_json(output, package / ('schemas/public-output-delivery-' + exit_id.replace('_', '-') + '-1.0.schema.json'), 'stdout')
        return output
    except LifecycleContractError as exc:
        raise CommandError('stale_identity', exc.field_path, exc.remediation, 3) from exc
