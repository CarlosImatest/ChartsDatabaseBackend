import asyncio

from app.models.chart import ChartCRC, Layer
from app.db.mongodb import init_database


async def create_chart_test():

    # Start Beanie connection
    await init_database()


    db_chart = ChartCRC(
        name="test insert chart",
        film_type="Fujifilm",
        layers=[
            Layer(name="test 1 layer", values=[1, 2, 3, 4]),
            Layer(name="test 12layer", values=[5, 6, 7, 8])
        ],
        final_layer=Layer(name="final layer", values=[9, 10, 11, 12])
    )


    await db_chart.insert()


    print("Inserted Chart:")
    print(db_chart)



asyncio.run(create_chart_test())