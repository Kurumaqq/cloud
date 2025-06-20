import json

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
    def token(self):
        with open(self.path, 'r') as f:
            return f'Bearer {json.load(f)['token']}'
