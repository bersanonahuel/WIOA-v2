import requests

try:
    r = requests.get('http://wioav2.nserver.space', timeout=5)
    print("HTTP:", r.status_code)
except Exception as e:
    print("HTTP Error:", e)

try:
    r = requests.get('https://wioav2.nserver.space', timeout=5)
    print("HTTPS:", r.status_code)
except Exception as e:
    print("HTTPS Error:", e)
