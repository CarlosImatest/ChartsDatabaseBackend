from enum import Enum


class UserRole(str, Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    ADMIN = "admin"


class ChartType(str, Enum):
    CRC = "CRC"
    WDR = "WDR"
    VISNIR = "VISNIR"
    LDR = "LDR"
    UHDR = "UHDR"