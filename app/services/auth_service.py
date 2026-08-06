import resend
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

        # Same reasoning as invite_service.create_invite: the account
        # itself is already fully created at this point. If email
        # delivery fails (e.g. unverified sending domain), we don't
        # want to crash the whole signup — the account still exists,
        # the user just needs the code delivered another way (resend
        # endpoint once domain is fixed, or read from server logs
        # during local development).
        try:
            EmailService.send_verification_code(user.email, code, user.first_name)
        except resend.exceptions.ResendError as e:
            print(f"[DEV] Verification code for {user.email}: {code}")
            print(f"[DEV] Email send failed: {e}")

        return user

    @staticmethod
    async def verify_email(user: User, code: str) -> bool:
        if user.status == UserStatus.ACTIVE:
            return True

        if not user.verification_code_hash or not user.verification_code_expires_at:
            return False

        now_naive_utc = datetime.now(timezone.utc).replace(tzinfo=None)

        if now_naive_utc > user.verification_code_expires_at:
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

        try:
            EmailService.send_verification_code(user.email, code, user.first_name)
        except resend.exceptions.ResendError as e:
            print(f"[DEV] Verification code for {user.email}: {code}")
            print(f"[DEV] Email send failed: {e}")

    @staticmethod
    async def change_password(user: User, current_password: str, new_password: str) -> bool:
        """
        Returns False if current_password doesn't match what's on file —
        the route turns that into a 400 rather than silently succeeding.
        """
        if not verify_password(current_password, user.hashed_password):
            return False

        user.hashed_password = hash_password(new_password)
        await user.save()
        return True