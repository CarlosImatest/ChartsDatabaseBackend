from app.models.chart import CHART_MODEL_REGISTRY, Layer
from app.schemas.chart import ChartCreate
from app.common.enums import ChartType


class ChartService:

    @staticmethod
    async def create_chart(chart: ChartCreate):
        model_cls = CHART_MODEL_REGISTRY[chart.chart_type]

        db_chart = model_cls(
            name=chart.name,
            film_type=chart.film_type,
            layers=[
                Layer(name=layer.name, values=layer.values)
                for layer in chart.layers
            ],
            final_layer=Layer(
                name=chart.final_layer.name,
                values=chart.final_layer.values
            )
        )

        await db_chart.insert()
        return db_chart

    @staticmethod
    async def get_chart(chart_type: ChartType, chart_id: str):
        model_cls = CHART_MODEL_REGISTRY[chart_type]
        return await model_cls.get(chart_id)

    @staticmethod
    async def list_charts(chart_type: ChartType):
        model_cls = CHART_MODEL_REGISTRY[chart_type]
        return await model_cls.find_all().to_list()