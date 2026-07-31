from datetime import datetime

from beanie import Document
from pydantic import EmailStr

from app.common.enums import UserRole, UserStatus


class User(Document):

    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    role: UserRole

    # Defaults to ACTIVE so admin-direct-created users (via POST
    # /auth/register) don't need email verification — only users who
    # sign themselves up through an invite link go through the
    # PENDING_VERIFICATION step.
    status: UserStatus = UserStatus.ACTIVE

    # Only set while status == PENDING_VERIFICATION. Cleared once
    # verified. We store a hash, never the plaintext code, same
    # principle as password storage.
    verification_code_hash: str | None = None
    verification_code_expires_at: datetime | None = None

    class Settings:
        name = "user"