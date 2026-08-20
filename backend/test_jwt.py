from app.auth.jwt_handler import (
    create_access_token,
    verify_access_token
)

token = create_access_token(
    {
        "sub": "learner@test.com",
        "role": "Learner"
    }
)

print("TOKEN:\n")
print(token)

print("\nVERIFY:\n")

payload = verify_access_token(token)

print(payload)