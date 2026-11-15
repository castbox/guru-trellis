"""Content identity shared by adjacent change-request consumers."""

from __future__ import annotations

import hashlib
import json


def title_body_identity(title: str, body: str) -> str:
    """Return the existing title/body identity without semantic normalization."""
    fields = {
        "title_sha256": hashlib.sha256(title.encode("utf-8")).hexdigest(),
        "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    }
    encoded = json.dumps(fields, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
