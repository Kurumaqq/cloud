import requests

a = requests.post(
    'http://127.0.0.1:8000/dirs/create/',
    params={'path': '..test_dir'},
    )

print(a.json())
