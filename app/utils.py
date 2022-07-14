from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Hashing algorithm


def hash_pwd(pwd: str):
    return pwd_context.hash(pwd)


def verify_pass(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)
