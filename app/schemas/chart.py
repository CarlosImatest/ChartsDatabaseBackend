from pydantic import BaseModel
from app.common.enums import ChartType


class LayerSchema(BaseModel):
    name: str
    values: list


class ChartCreate(BaseModel):
    chart_type: ChartType
    name: str
    film_type: str
    layers: list[LayerSchema]
    final_layer: LayerSchema


class ChartResponse(BaseModel):
    id: str
    name: str
    film_type: str
    layers: list[LayerSchema]
    final_layer: LayerSchema