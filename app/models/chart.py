from beanie import Document
from pydantic import BaseModel


class Layer(BaseModel):
    name: str
    values: list


class ChartBase(BaseModel):
    name: str
    film_type: str
    layers: list[Layer]
    final_layer: Layer


class ChartCRC_test(Document, ChartBase):
    class Settings:
        name = "CRC_test"


class ChartWDR_test(Document, ChartBase):
    class Settings:
        name = "UHDR_test"

class ChartWDR(Document, ChartBase):
    class Settings:
        name = "WDR"

class ChartCRC(Document, ChartBase):
    class Settings:
        name = "CRC"

class ChartVISNIR(Document, ChartBase):
    class Settings:
        name = "VISNIR"

class ChartLDR(Document, ChartBase):
    class Settings:
        name = "LDR"

class ChartUHDR(Document, ChartBase):
    class Settings:
        name = "UHDR"