"""Stateless projections onto the installed upstream Delivery API."""

from .adapter import DeliveryProjection, authority_ref, upstream_modules

__all__ = ["DeliveryProjection", "authority_ref", "upstream_modules"]
