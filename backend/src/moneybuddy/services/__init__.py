"""Business logic services.

This module contains service classes that encapsulate business logic,
keeping it separate from API endpoints and database models.
"""

from moneybuddy.services.auth_service import AuthService

__all__ = ["AuthService"]
