from app.models.chart import CHART_MODEL_REGISTRY, Layer
from app.schemas.chart import ChartCreate, ChartUpdate
from app.common.enums import ChartType


class ChartService:

    @staticmethod
    async def create_chart(chart: ChartCreate):
        model_cls = CHART_MODEL_REGISTRY[chart.chart_type]

        db_chart = model_cls(
            name=chart.name,
            film_type=chart.film_type,
            layers=[Layer(name=l.name, values=l.values) for l in chart.layers],
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

    @staticmethod
    async def update_chart(chart_type: ChartType, chart_id: str, update: ChartUpdate):
        """
        Returns None if the chart doesn't exist — the route turns that
        into a 404. Only fields actually present in `update` (not None)
        get overwritten, so a partial edit (e.g. just renaming) doesn't
        wipe out layers/final_layer that weren't sent.
        """
        db_chart = await ChartService.get_chart(chart_type, chart_id)
        if not db_chart:
            return None

        if update.name is not None:
            db_chart.name = update.name
        if update.film_type is not None:
            db_chart.film_type = update.film_type
        if update.layers is not None:
            db_chart.layers = [Layer(name=l.name, values=l.values) for l in update.layers]
        if update.final_layer is not None:
            db_chart.final_layer = Layer(
                name=update.final_layer.name,
                values=update.final_layer.values
            )

        await db_chart.save()
        return db_chart

    @staticmethod
    async def delete_chart(chart_type: ChartType, chart_id: str) -> bool:
        """Returns False if nothing was there to delete — lets the route 404 correctly."""
        db_chart = await ChartService.get_chart(chart_type, chart_id)
        if not db_chart:
            return False

        await db_chart.delete()
        return True

    @staticmethod
    async def get_chart_by_name(chart_type: ChartType, chart_name: str):
        model_cls = CHART_MODEL_REGISTRY[chart_type]
        return await model_cls.find_one(model_cls.name == chart_name)

    # @staticmethod
    # async def query(chart_type: ChartType, search: Query):
    #     ChartService.get_chart_by_name()
    #     return