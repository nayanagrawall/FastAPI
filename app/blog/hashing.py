from passlib.context import CryptContext  # to encrypt the password

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated='auto')


class Hash():
    def bcrypt(password: str):
        hasedPassword = pwd_cxt.hash(password)
        return hasedPassword

    def verify(hashed_password, clean_password):
        return pwd_cxt.verify(clean_password, hashed_password)
