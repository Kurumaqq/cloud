import json
from pathlib import Path
import bcrypt
from authx import AuthX, AuthXConfig
from datetime import timedelta


secret_key = "6431c7155c3a5ea9e1ef8d251828a381bbf3d15d7890cf4f714b86de6d735b18524c84e63d1f5fedefa7228976444926799c808a28998b4e5f45c4d66b3fdd04552a42498f4c83c2d6c7409162c76f7afb580cd6af4a850f0f4944395969f81147d3df669db25946cd007c05748b1264b3fca5de038790293dd9fcd7a1dad22d"
config_authx = AuthXConfig()
config_authx.JWT_ACCESS_COOKIE_NAME = "ACCESS_TOKEN"
config_authx.JWT_REFRESH_COOKIE_NAME = "REFRESH_TOKEN"
config_authx.JWT_SECRET_KEY = secret_key
config_authx.JWT_TOKEN_LOCATION = ["cookies"]
config_authx.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
config_authx.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=180)
config_authx.JWT_ACCESS_CSRF_COOKIE_NAME = "csrf_access_token"
config_authx.JWT_COOKIE_CSRF_PROTECT = True

authx = AuthX(config_authx)


class Config():
    def __init__(self, path='src/config/config.json'):
        self.path = path
    
    @property
    def host(self):
        with open(self.path, 'r') as f:
            return json.load(f)['host']

    @property
    def port(self):
        with open(self.path, 'r') as f:
            return json.load(f)['port']
    @property
    def base_dir(self):
        with open(self.path, 'r') as f:
            return json.load(f)['base_dir']

    @property
    def username(self):
        with open(self.path, 'r') as f:
            return json.load(f)['username']

    @property
    def password(self):
        return bcrypt.hashpw('1682'.encode(), bcrypt.gensalt())

    @property
    def secret_key(self):
        key = Path('src/cert/private.pem')
        return key.read_text()
    
    @property
    def public_key(self):
        key = Path('src/cert/public.pem')
        return key.read_text()
