import urllib.request, urllib.parse, re
try:
    req1 = urllib.request.Request('http://127.0.0.1:5000/')
    resp1 = urllib.request.urlopen(req1)
    html = resp1.read().decode('utf-8')
    cookie = resp1.headers.get('Set-Cookie').split(';')[0]
    token = re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)
    print(f"Token: {token}")
    print(f"Cookie: {cookie}")
    data = urllib.parse.urlencode({'rut': 'pasajero', 'password': '123', 'csrf_token': token}).encode('utf-8')
    req2 = urllib.request.Request('http://127.0.0.1:5000/', data=data, headers={'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded'})
    resp2 = urllib.request.urlopen(req2)
    print("Success:", resp2.status)
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Response body:", e.read().decode('utf-8'))
