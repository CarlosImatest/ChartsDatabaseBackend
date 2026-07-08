from pydantic import BaseModel


class Layer(BaseModel):
    name: str
    values: list


class Chart(BaseModel):
    name: str
    film_type: str
    layers: list[Layer]
    final_layer: Layer