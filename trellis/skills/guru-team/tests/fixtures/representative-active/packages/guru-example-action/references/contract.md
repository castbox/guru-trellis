# Contract

This test-only package proves interface 1.3 structured input, per-exit output,
consumer-owned inputs, direct/select/rename/normalize projections, and private
runtime checkpoint and gate evidence classification. The stop exit uses an
empty `select` into explicit `zero_payload`; `exit_id` remains routing identity
and is not forwarded as stop-response payload.
