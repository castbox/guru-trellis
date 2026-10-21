# Catalog operation contract

The catalog has an active runtime target and a display title. Selecting a different active target makes that target eligible to serve production work. A target must have current qualification evidence before it can become active. The qualification service owns the target evidence; the target-selection handler consumes it before changing active_target. Existing active targets remain active when the qualification service is unavailable. A display-title change only affects the catalog list and must remain available without qualification evidence. It does not select, requalify or start a runtime target. The display caller passes only a title and must not acquire target-qualification responsibilities.

catalog.py owns the two operations. qualification.json is the current qualification-service observation. No qualification service or runtime deployment is contacted in this fixture. Only local catalog-state.json copies are operated on.
