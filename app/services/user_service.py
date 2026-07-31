from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.password import hash_password


class UserService:

    @staticmethod
    async def create_user(user: UserCreate) -> User:
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=user.role
            # status defaults to ACTIVE — this is the admin-direct-create
            # path, which stays exempt from email verification.
        )
        await db_user.insert()
        return db_user

    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        return await User.find_one(User.email == email)