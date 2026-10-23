from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

# Used when a username doesn't exist, to reduce
# response-time differences during login.
DUMMY_HASH = password_hash.hash("dummy-not-a-real-password")


def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)


def verify_password(
    plain_password: str,
    stored_hash: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        stored_hash,
    )