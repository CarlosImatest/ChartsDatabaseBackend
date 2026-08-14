from fastapi import APIRouter, HTTPException, Depends, status

from app.common.enums import ChartType
from app.schemas.chart import ChartCreate, ChartUpdate, ChartResponse, LayerSchema
from app.services.chart_service import ChartService
from app.core.security import require_viewer, require_editor
from app.models.user import User

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
async def create_chart(
    chart: ChartCreate,
    current_user: User = Depends(require_editor)
):
    db_chart = await ChartService.create_chart(chart)
    return _to_response(db_chart)


#had to move get_chart_by_name above get_chart, so that when searching this execute first
#if not the API runs get_chart and gives an error
@router.get("/charts/{chart_type}/search", response_model=ChartResponse)
async def get_chart_by_name(
    chart_type: ChartType,
    name: str,
    current_user: User = Depends(require_viewer),
):
    db_chart = await ChartService.get_chart_by_name(chart_type, name)

    if not db_chart:
        raise HTTPException(status_code=404, detail="Chart not found")

    return _to_response(db_chart)

@router.get("/charts/{chart_type}/{chart_id}", response_model=ChartResponse)
async def get_chart(
    chart_type: ChartType,
    chart_id: str,
    current_user: User = Depends(require_viewer)
):
    db_chart = await ChartService.get_chart(chart_type, chart_id)
    if not db_chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    return _to_response(db_chart)


@router.get("/charts/{chart_type}", response_model=list[ChartResponse])
async def list_charts(
    chart_type: ChartType,
    current_user: User = Depends(require_viewer)
):
    db_charts = await ChartService.list_charts(chart_type)
    return [_to_response(c) for c in db_charts]


@router.patch("/charts/{chart_type}/{chart_id}", response_model=ChartResponse)
async def update_chart(
    chart_type: ChartType,
    chart_id: str,
    update: ChartUpdate,
    current_user: User = Depends(require_editor)
):
    db_chart = await ChartService.update_chart(chart_type, chart_id, update)
    if not db_chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    return _to_response(db_chart)


@router.delete("/charts/{chart_type}/{chart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chart(
    chart_type: ChartType,
    chart_id: str,
    current_user: User = Depends(require_editor)
):
    deleted = await ChartService.delete_chart(chart_type, chart_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chart not found")
