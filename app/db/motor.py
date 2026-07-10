from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


class MongoConnection:

    def __init__(self, database_name=None):
        self.client = AsyncIOMotorClient(settings.mongodb_uri)

        if database_name is None:
            database_name = settings.database_name

        self.database = self.client[database_name]

    def get_collection(self, collection_name: str):
        return self.database[collection_name]

    def get_database(self):
        return self.database

    def close(self):
        self.client.close()