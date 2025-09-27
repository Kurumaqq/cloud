from src.utils import check_password, encode_jwt
from src.schemas.login import * 
from src.errors.login import *
from src.config import Config

config = Config()

async def login(data: LoginRequest):
    try:
        if not check_password(data.password, config.password):
            return InvalidPasswordOrUserHttpError()
        if data.username != config.username:
            return InvalidPasswordOrUserHttpError()
        
        payload = {'sub': data.username}
        token = encode_jwt(payload)
        return LoginResponse(token=token)
    except Exception as e:
        return LoginRequest(massage=str(e))
