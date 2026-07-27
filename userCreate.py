import asyncio

from app.models.user import User
from app.common.enums import UserRole
from app.utils.password import hash_password
from app.db.mongodb import init_database


async def create_first_admin():
    await init_database()

    admin = User(
        first_name="Carlos",
        last_name="Sanchez",
        email="carlos@imatest.com",
        hashed_password=hash_password("carlosimatest1"),
        role=UserRole.ADMIN
    )

    await admin.insert()
    print("Created bootstrap admin:", admin)


asyncio.run(create_first_admin())