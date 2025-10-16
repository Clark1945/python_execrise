from datetime import timedelta, datetime

from jose import jwt, JWTError

from fastapi_demo.utility import get_env_value

#####################################################
SECRET_KEY = get_env_value("SECRET_KEY")
ALGORITHM = get_env_value("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = get_env_value("ACCESS_TOKEN_EXPIRE_MINUTES")
#####################################################

# 產生 Token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 驗證 Token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None