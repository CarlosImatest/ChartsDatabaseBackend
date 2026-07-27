from app.models.user import User
from app.services.user_service import UserService
from app.utils.password import verify_password
from app.core.security import create_access_token


class AuthService:

    @staticmethod
    async def authenticate(email: str, password: str) -> User | None:
        user = await UserService.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def issue_token(user: User) -> str:
        return create_access_token(subject=str(user.id))