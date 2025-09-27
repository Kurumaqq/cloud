import json
from pathlib import Path
import bcrypt

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
        return hash_password('1682')

    @property
    def secret_key(self):
        key = Path('src/cert/private.pem')
        return key.read_text()
    
    @property
    def public_key(self):
        key = Path('src/cert/public.pem')
        return key.read_text()
