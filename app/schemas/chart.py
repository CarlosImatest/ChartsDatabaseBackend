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

class ChartUpdate(BaseModel):
    """
    All fields optional — a PATCH should only touch what's provided.
    chart_type is deliberately NOT included: you can't move a chart
    between collections via update, only edit its contents in place.
    """
    name: str | None = None
    film_type: str | None = None
    layers: list[LayerSchema] | None = None
    final_layer: LayerSchema | None = None