# Analysis - Offensive 100

## Problem

You're given a link to the website, "Strange Auth System". It has register and login forms, and a list recent of logins with timestamps and UIDs.

## Solution

Commendation @emedvedev

You're not given a hint or any indication about what to do, but usually low-point web challenges just want you to login as admin. Not in this case though: somebody just created an "admin" account which isn't any different from others.

There are two peculiar things you notice after a while:
1. There's a user with a UID 1 who logs in every minute.
2. Sometimes you log in as one user, but have another username appear after the login page.

This means you can intercept someone else's session, and since sometimes it happens automatically without any effort, a good assumption would be that you're intercepting a user that logs in at the same time with you.

Let's try to intercept the mysterious "UID 1" login by logging in repeatedly and watching the logins that appear:

```
import requests
import re

while True:
    data = { "username": "admin", "password": "admin" }
    post = requests.post("http://ctfquest.trendmicro.co.jp:8888/95f20bb7856574e91db4402435a87427/signin", data).text
    findall = re.findall(r'<h2>Welcome (.*?)\s+<', post)
    if findall:
        print findall[0]
    else:
        print post
        break
```

After a couple minutes you log in as UID 1; its username is the flag.
