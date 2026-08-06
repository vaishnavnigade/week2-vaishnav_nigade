from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password (same as training practice)."""
    return password_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored hash."""
    return password_hasher.verify(plain_password, hashed_password)