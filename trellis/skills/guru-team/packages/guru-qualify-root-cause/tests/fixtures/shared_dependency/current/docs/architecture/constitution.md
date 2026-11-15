# Cache Fixture Constitution

Identity: behavior-fixture-constitution-v1. Status: current. Use current Python owners for required behavior. Keep cache values, caller parameters, generated interfaces and observed outcomes distinct. Shared code has one owner in app/; consumers call it through actual interfaces. Add complexity only for current callers. Remove obsolete consumers when replacing a supported path. No new persistence or external service is required by this fixture.
