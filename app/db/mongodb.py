from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.user import User
from app.models.invite import Invite
from app.models.chart import (
    ChartCRC, ChartWDR, ChartVISNIR, ChartLDR, ChartUHDR,
    ChartCRC_test, ChartWDR_test,
)


async def init_database():
    client = AsyncIOMotorClient(settings.mongodb_uri)

    users_db = client["Users"]
    charts_db = client["Charts"]

    await init_beanie(
        database=users_db,
        document_models=[User, Invite]  # Invite lives in the Users db alongside User
    )

    await init_beanie(
        database=charts_db,
        document_models=[
            ChartCRC, 
            ChartWDR, 
            ChartVISNIR, 
            ChartLDR, 
            ChartUHDR,
            ChartCRC_test, 
            ChartWDR_test,
        ]
    )