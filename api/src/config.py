import json

class Config():
    def __init__(self, path='config.json'):
        self.path = path
    
    @property
    def host(self):
        with open('config.json', 'r') as f:
            return json.load(f)['host']

    @property
    def port(self):
        with open('config.json', 'r') as f:
            return json.load(f)['port']
    @property
    def base_dir(self):
        with open('config.json', 'r') as f:
            return json.load(f)['base_dir']
