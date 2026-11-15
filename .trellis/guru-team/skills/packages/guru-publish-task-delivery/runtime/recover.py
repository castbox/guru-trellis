"""Dispatch the explicit original-owner legacy profiles."""
from legacy_maintenance import run as _legacy_run
from owner import _public_command

run = _public_command(_legacy_run)
