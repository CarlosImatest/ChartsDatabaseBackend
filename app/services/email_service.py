import resend

from app.core.config import settings

resend.api_key = settings.resend_api_key


class EmailService:
    """
    Thin wrapper around Resend. Keeping this as its own service (rather
    than calling resend.Emails.send directly from AuthService/InviteService)
    if we change providers, only this file changes.
    """

    @staticmethod
    def send_verification_code(to_email: str, code: str, first_name: str) -> None:
        resend.Emails.send({
            "from": settings.email_from,
            "to": [to_email],
            "subject": "Verify your email",
            "html": f"""
                <p>Hi {first_name},</p>
                <p>Your verification code is:</p>
                <h2>{code}</h2>
                <p>This code expires in {settings.verification_code_expire_minutes} minutes.</p>
            """
        })

    @staticmethod
    def send_invite(to_email: str, invite_url: str, role: str) -> None:
        resend.Emails.send({
            "from": settings.email_from,
            "to": [to_email],
            "subject": "You've been invited",
            "html": f"""
                <p>You've been invited to join as a <strong>{role}</strong>.</p>
                <p><a href="{invite_url}">Click here to create your account</a></p>
                <p>This link expires in {settings.invite_expire_hours} hours.</p>
            """
        })