from datetime import datetime, timedelta, timezone

from app.models.user import User
from app.services.user_service import UserService
from app.services.invite_service import InviteService
from app.services.email_service import EmailService
from app.utils.password import hash_password, verify_password
from app.utils.verification import generate_verification_code, hash_code, verify_code
from app.core.security import create_access_token
from app.core.config import settings
from app.common.enums import UserStatus
from app.schemas.auth import RegisterWithInviteRequest


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

    @staticmethod
    async def register_with_invite(payload: RegisterWithInviteRequest) -> User:
        """
        Redeems an invite: validates it, creates a PENDING_VERIFICATION
        user with the invite's preset role/email, marks the invite used,
        and emails a verification code. The invite is consumed even if
        the user never finishes verifying — they'd need a new invite.
        """
        invite = await InviteService.get_valid_invite(payload.invite_token)

        code = generate_verification_code()

        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=invite.email,
            hashed_password=hash_password(payload.password),
            role=invite.role,
            status=UserStatus.PENDING_VERIFICATION,
            verification_code_hash=hash_code(code),
            verification_code_expires_at=datetime.now(timezone.utc)
                + timedelta(minutes=settings.verification_code_expire_minutes)
        )
        await user.insert()

        await InviteService.mark_used(invite)

        EmailService.send_verification_code(user.email, code, user.first_name)

        return user

    @staticmethod
    async def verify_email(user: User, code: str) -> bool:
        if user.status == UserStatus.ACTIVE:
            return True  # already verified, nothing to do

        if not user.verification_code_hash or not user.verification_code_expires_at:
            return False

        if datetime.now(timezone.utc) > user.verification_code_expires_at:
            return False

        if not verify_code(code, user.verification_code_hash):
            return False

        user.status = UserStatus.ACTIVE
        user.verification_code_hash = None
        user.verification_code_expires_at = None
        await user.save()

        return True

    @staticmethod
    async def resend_verification_code(user: User) -> None:
        code = generate_verification_code()
        user.verification_code_hash = hash_code(code)
        user.verification_code_expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.verification_code_expire_minutes
        )
        await user.save()
        EmailService.send_verification_code(user.email, code, user.first_name)