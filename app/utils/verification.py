import hashlib
import secrets


def generate_verification_code() -> str:
    """
    Generates a random 6-digit numeric code as a string (e.g. '042917'),
    zero-padded so it's always exactly 6 characters.
    """
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_code(code: str) -> str:
    """
    SHA-256 is sufficient here (unlike passwords, which need a slow,
    salted hash like bcrypt/argon2) because verification codes are
    short-lived and low-value — even a fast hash makes offline brute
    forcing impractical within the code's expiry window.
    """
    return hashlib.sha256(code.encode()).hexdigest()


def verify_code(code: str, hashed: str) -> bool:
    return hash_code(code) == hashed