import asyncio

from app.schemas.user import UserCreate
from app.models.user import User
from app.common.enums import UserRole
from app.utils.password import hash_password
from app.db.mongodb import init_database


async def create_user_test():

    # Start Beanie connection
    await init_database()


    user_request = UserCreate(
        name="Carlos",
        email="carlos@test.com",
        password="SuperSecret123",
        role=UserRole.ENGINEER
    )


    print(user_request)


    db_user = User(
        name=user_request.name,
        email=user_request.email,
        hashed_password=hash_password(
            user_request.password
        ),
        role=user_request.role
    )


    await db_user.insert()


    print("Inserted User:")
    print(db_user)



asyncio.run(create_user_test())