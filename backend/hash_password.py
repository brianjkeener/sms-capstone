# New self-contained content for backend/hash_password.py

from passlib.context import CryptContext

# This context is copied from your auth.py file to make this script independent
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# The password you want to use for all users
plain_password = "password123"

# Generate the hash
hashed_password = get_password_hash(plain_password)

print("Password:", plain_password)
print("Generated Hash:", hashed_password)