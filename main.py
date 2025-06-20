import requests

a = requests.get('http://localhost:8000/combined/list')

print(a.json()['dirs'])
print(a.json()['files'])
print()
print(a.json()['all'])
