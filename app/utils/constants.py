"""
This file contains constants used in the application.
"""

from enum import Enum


class UserStatus(Enum):
    """
    An enumeration of possible user statuses.

    This enumeration defines a set of constants that represent different
    statuses that a user can have. The values defined in this enumeration
    can be used to indicate the current status of a user.
    """

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"


class RoutePrefix(Enum):
    """
    An enumeration of route prefixes used in the application.

    This enumeration defines a set of constants that represent different
    route prefixes used in the application.
    """

    AUTH = "/auth"
    USER = "/user"
    ROLE = "/role"


class RouteTag(Enum):
    """
    An enumeration of route tags used in the application.

    This enumeration defines a set of constants that represent different
    route tags used in the application. The values defined in this enumeration
    can be used to categorize routes and provide additional metadata.
    """

    AUTH = "Authentication"
    USER = "Users"
    ROLE = "Roles"
