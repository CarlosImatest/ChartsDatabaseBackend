from fastapi import APIRouter, HTTPException

from app.common.enums import ChartType
from app.schemas.chart import ChartCreate, ChartResponse, LayerSchema
from app.services.chart_service import ChartService

router = APIRouter()


def _to_response(db_chart) -> ChartResponse:
    return ChartResponse(
        id=str(db_chart.id),
        name=db_chart.name,
        film_type=db_chart.film_type,
        layers=[
            LayerSchema(name=layer.name, values=layer.values)
            for layer in db_chart.layers
        ],
        final_layer=LayerSchema(
            name=db_chart.final_layer.name,
            values=db_chart.final_layer.values
        )
    )


@router.post("/charts", response_model=ChartResponse)
async def create_chart(chart: ChartCreate):
    db_chart = await ChartService.create_chart(chart)
    return _to_response(db_chart)


@router.get("/charts/{chart_type}/{chart_id}", response_model=ChartResponse)
async def get_chart(chart_type: ChartType, chart_id: str):
    db_chart = await ChartService.get_chart(chart_type, chart_id)

    if not db_chart:
        raise HTTPException(status_code=404, detail="Chart not found")

    return _to_response(db_chart)


@router.get("/charts/{chart_type}", response_model=list[ChartResponse])
async def list_charts(chart_type: ChartType):
    db_charts = await ChartService.list_charts(chart_type)
    return [_to_response(c) for c in db_charts]