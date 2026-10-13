"""Project an owner's completed scope withdrawal judgment, with a fixed role.

The caller owns the stop decision and legal role. This projection neither
selects an owner from phase nor infers withdrawal from a changed scope.
"""
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle import LifecycleContractError
from .adapter import DeliveryProjection


def stop(root, package, public, semantic, *, owner_role, expected_phase):
    validate_json(public, package / 'schemas/public-delivery-scope-withdrawal-input-1.0.schema.json', 'input')
    validate_json(semantic, package / 'schemas/delivery-scope-withdrawal-review-1.0.schema.json', 'semantic_result')
    projection = DeliveryProjection(root, public['task_ref'])
    try:
        delivery = projection.resolve(public['delivery_key'])
        owner = projection.declaration()['owners'][owner_role]
        if semantic['reviewed_delivery_key'] != public['delivery_key']:
            raise CommandError('stale_identity', 'reviewed_delivery_key', 'Review the selected withdrawn Delivery.', 3)
        result = {name: semantic[name] for name in ('result_id', 'evidence', 'reason', 'scope_decision')}
        result['owner_id'] = owner
        if delivery['phase'] == 'stopped':
            if delivery['stop_result'] != result:
                raise CommandError('stale_identity', 'stop_result', 'Recover the original stop conclusion.', 3)
        else:
            if delivery['phase'] != expected_phase:
                raise CommandError('stale_identity', 'phase', 'Return to the actual current stage owner for scope withdrawal.', 3)
            projection.apply({'api_version': '1.0', 'operation': 'stop', 'key': public['delivery_key'],
                              'owner_role': owner_role, 'owner_id': owner,
                              'expected_phase': expected_phase, 'result': result})
        projection.release(public['delivery_key'])
        key = {name: public['delivery_key'][name] for name in ('task_id', 'lifecycle_generation')}
        output = {'exit_id': 'delivery_stopped', 'task_ref': public['task_ref'], 'task_key': key}
        validate_json(output, package / 'schemas/public-delivery-stopped-output-1.0.schema.json', 'stdout')
        return output
    except LifecycleContractError as exc:
        raise CommandError('stale_identity', exc.field_path, exc.remediation, 3) from exc
