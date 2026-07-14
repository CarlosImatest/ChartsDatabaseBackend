from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.password import hash_password


class UserService:

    @staticmethod
    async def create_user(user: UserCreate) -> User:

        db_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=user.role
        )

        await db_user.insert()

        return db_user