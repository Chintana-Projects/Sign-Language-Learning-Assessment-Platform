from app.auth.hashing import hash_password, verify_password

password = "Rohan@123"

hashed = hash_password(password)

print("Hashed Password:")
print(hashed)

print()

print(
    verify_password(
        "Rohan@123",
        hashed
    )
)