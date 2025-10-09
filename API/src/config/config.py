import json
from pathlib import Path
import bcrypt
from authx import AuthX, AuthXConfig
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
config_authx = AuthXConfig()
config_authx.JWT_ACCESS_COOKIE_NAME = "ACCESS_TOKEN"
config_authx.JWT_REFRESH_COOKIE_NAME = "REFRESH_TOKEN"
config_authx.JWT_SECRET_KEY = secret_key
config_authx.JWT_TOKEN_LOCATION = ["cookies"]
config_authx.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
config_authx.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=180)
config_authx.JWT_ACCESS_CSRF_COOKIE_NAME = "CSRF_ACCES_TOKEN"
config_authx.JWT_REFRESH_CSRF_COOKIE_NAME = "CSRF_REFRESH_TOKEN"
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
