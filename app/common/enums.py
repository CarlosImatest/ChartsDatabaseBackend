from enum import Enum


class UserRole(str, Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    ADMIN = "admin"


class UserStatus(str, Enum):
    """
    Tracks whether a user has completed email verification.
    PENDING_VERIFICATION: account exists, but can't access anything
        except the verify-email/resend-code endpoints.
    ACTIVE: fully verified, normal access per their role.
    """
    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"


class ChartType(str, Enum):
    CRC = "CRC"
    WDR = "WDR"
    VISNIR = "VISNIR"
    LDR = "LDR"
    UHDR = "UHDR"