from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    ENGINEER = "engineer"
    VIEWER = "viewer"

#define the chart type database we have
class ChartType(str, Enum):
    CRC = "CRC"
    WDR = "WDR"
    VISNIR = "VISNIR"
    LDR = "LDR"
    UHDR = "UHDR"
