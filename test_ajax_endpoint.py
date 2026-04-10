import urllib.request
import urllib.parse
import http.cookiejar
import re
import json

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

# Get login page to get CSRF token
resp = opener.open('https://wioav2.nserver.space/accounts/login/')
html = resp.read().decode()

csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
csrf_token = csrf_match.group(1) if csrf_match else ''
print('CSRF:', csrf_token[:20] if csrf_token else 'NOT FOUND')

# Login
login_data = urllib.parse.urlencode({
    'username': 'admin',
    'password': 'admin123',
    'csrfmiddlewaretoken': csrf_token
}).encode()
req = urllib.request.Request(
    'https://wioav2.nserver.space/accounts/login/',
    data=login_data,
    headers={'Referer': 'https://wioav2.nserver.space/accounts/login/'}
)
resp2 = opener.open(req)
print('After login URL:', resp2.url)

# Test with proyectoId
for pid in [1, 2, 3, 4, 5]:
    try:
        url = 'https://wioav2.nserver.space/registros/listarRegistro?action=getAlumnosDelProyecto&proyectoId=' + str(pid)
        req3 = urllib.request.Request(url, headers={'X-Requested-With': 'XMLHttpRequest'})
        resp3 = opener.open(req3)
        raw = resp3.read().decode()
        data = json.loads(raw)
        keys = list(data.keys())
        if 'alumnos' in data:
            n = len(data['alumnos'])
            first = data['alumnos'][0] if n > 0 else 'none'
            print(f'proyectoId={pid} -> {n} alumnos. First: {first}')
        elif 'error' in data:
            print(f'proyectoId={pid} -> ERROR: {data["error"]}')
        else:
            print(f'proyectoId={pid} -> Keys: {keys}')
    except Exception as e:
        print(f'proyectoId={pid} -> EXCEPTION: {e}')
