# #481 Task Personnel Retirement Design

State: implementation candidate; reviewed promotion to shared current remains pending.

- `D481-01`: Use the official Fork task schema and `task.py create` without personnel flags. Guru create-task public input no longer accepts `creator` or `assignee`; the executor does not write `task.json.delivery_target`. Reviewed delivery target remains call-local for its existing direct consumer.
- `D481-02`: Current task enumeration validates supported official task shape. Legacy archive scanning extracts only an `id` for uniqueness, then optionally applies strict exact-source matching for a rejection diagnostic; no legacy record becomes a current lifecycle candidate.
- `D481-03`: Reactivate and Finish recovery reject an old personnel-bearing archive before lifecycle mutation. Current schema-valid archives continue through #454 validation and generation transition.
- `D481-04`: Preserve the existing session, branch and resource stores and their single writers. No personnel-derived lookup or second identity store is introduced.
- `D481-05`: Source lock uses `castbox/Trellis@64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`, CLI/core `0.7.0-castbox.1`, successful CI `36755826713`; extension candidate is `0.7.0-guru.1`. These are candidate identities, not published release facts.
- `D481-06`: Canonical preset and workflow feed dogfood and installed projections through the existing installer. Old public task input and personnel-bearing task files have no compatibility executor, alias or automatic writer.

The predecessor `v0.6.17-guru.2` target tag is a separate release axis. This contribution neither publishes it nor changes #292's Phase 1 owner.
