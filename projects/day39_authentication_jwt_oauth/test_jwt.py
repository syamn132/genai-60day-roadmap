from jwt_utils import (
    create_access_token,
    verify_access_token,
)


print("=" * 55)
print("DAY 39 — PART 2: JWT TESTING")
print("=" * 55)


# TEST 1: Create a token

token = create_access_token(
    subject="12"
)

print("\nTEST 1 — TOKEN CREATION")

print(
    "JWT structure valid:",
    len(token.split(".")) == 3
)


# TEST 2: Verify a valid token

print("\nTEST 2 — VALID TOKEN")

subject = verify_access_token(token)

print("Authenticated subject:", subject)


# TEST 3: Detect tampering

print("\nTEST 3 — TAMPERED TOKEN")

parts = token.split(".")

signature = parts[2]

replacement = (
    "A" if signature[0] != "A" else "B"
)

parts[2] = replacement + signature[1:]

tampered_token = ".".join(parts)

try:
    verify_access_token(tampered_token)

    print("FAIL: Tampered token accepted")

except ValueError:
    print("PASS: Tampered token rejected")


# TEST 4: Reject expired token

print("\nTEST 4 — EXPIRED TOKEN")

expired_token = create_access_token(
    subject="12",
    expires_minutes=-1,
)

try:
    verify_access_token(expired_token)

    print("FAIL: Expired token accepted")

except ValueError:
    print("PASS: Expired token rejected")


print("\nJWT TESTING COMPLETE")