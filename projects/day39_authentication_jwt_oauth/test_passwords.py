from security import hash_password, verify_password

password = "MySecureDemo#2026"

hashed = hash_password(password)

print("Original password:", password)
print("Stored hash:", hashed)

print(
    "Correct password:",
    verify_password(password, hashed),
)

print(
    "Incorrect password:",
    verify_password("wrong-password", hashed),
)

assert verify_password(password, hashed)
assert not verify_password("wrong-password", hashed)

print("PASSWORD HASHING TEST: PASS")