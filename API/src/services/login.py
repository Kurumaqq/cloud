from fastapi import Response, Request
from fastapi.exceptions import HTTPException
from authx.exceptions import AuthXException
from uuid import uuid1
from src.config import Config, authx, config_authx
from src.utils import check_password


config = Config()


async def login_endpoint(username: str, pasw: str, response: Response):
    uid = str(uuid1())
    if username == config.username and check_password(pasw, config.password):
        token = authx.create_access_token(uid=uid)
        refresh_token = authx.create_refresh_token(uid=uid)

        authx.set_access_cookies(
            token, 
            response, 
            int(config_authx.JWT_ACCESS_TOKEN_EXPIRES.total_seconds())
            )
        authx.set_refresh_cookies(
            refresh_token, 
            response,
            int(config_authx.JWT_REFRESH_TOKEN_EXPIRES.total_seconds())
            )

        return {"token": token}


async def auto_refresh_access_token(request: Request, response: Response):
    access_token = request.cookies.get(config_authx.JWT_ACCESS_COOKIE_NAME)
    refresh_token = request.cookies.get(config_authx.JWT_REFRESH_COOKIE_NAME)

    if access_token:
        try:
            await authx.access_token_required(request)
            return
        except AuthXException:
            pass

    if refresh_token:
        try:
            payload = await authx.refresh_token_required(request)
            uid = payload.sub

            new_access_token = authx.create_access_token(uid=uid)
            response.set_cookie(
                config_authx.JWT_ACCESS_COOKIE_NAME,
                new_access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=int(config_authx.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
            )

            new_refresh_token = authx.create_refresh_token(uid=uid)
            response.set_cookie(
                config_authx.JWT_REFRESH_COOKIE_NAME,
                new_refresh_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=int(config_authx.JWT_REFRESH_TOKEN_EXPIRES.total_seconds()),
            )
            return
        except AuthXException:
            raise HTTPException(status_code=401, detail="Session expired")

    raise HTTPException(status_code=401, detail="Not authenticated")
