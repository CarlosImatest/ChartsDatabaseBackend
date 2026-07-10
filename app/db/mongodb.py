from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.user import User


async def init_database():
    client = AsyncIOMotorClient(
        settings.mongodb_uri
    )

    database = client[settings.database_name]

    await init_beanie(
        database=database,
        document_models=[
            User
        ]
    )