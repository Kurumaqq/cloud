from fastapi import Response
from src.schemas.request.other import *
from src.schemas.response.login import *
from uuid import uuid1
from src.errors.login import *
from src.config import Config, authx, config_authx
from src.utils.validators import validate_user

config = Config()


async def login(data: UserRequest, response: Response):
    uid = str(uuid1())
    username = data.username
    password = data.password
    validate_user(username, password)

    data = {"username": username}
    token = authx.create_access_token(uid=uid, data=data)
    refresh_token = authx.create_refresh_token(uid=uid, data=data)

    authx.set_access_cookies(
        token, response, int(config_authx.JWT_ACCESS_TOKEN_EXPIRES.total_seconds())
    )
    authx.set_refresh_cookies(
        refresh_token,
        response,
        int(config_authx.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()),
    )

    return LoginResponse(message="Login successful", uuid=uid, username=username)
