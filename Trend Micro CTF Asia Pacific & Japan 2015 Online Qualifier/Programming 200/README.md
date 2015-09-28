# Programming 200

## Problem

Solve all tasks

nc ctfquest.trendmicro.co.jp 51740

## Solution

Commendation: [@emedvedev](https://github.com/emedvedev)

When you connect to the server, it gives you a range of arithmetic problems and expects answers.

```
3 * 4 =
```

Sounds simple, right? We can use Python's `eval` and pray that one of the equations wouldn't suddenly appear to be `shutil.rmtree('/')`. Trend Micro guys could have a lot of fun with this one. Anyways, here's a basic example of the calculating loop:

```
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ctfquest.trendmicro.co.jp', 51740))

while True:
    recv = s.recv(1000)
    print 'Received: ' + recv
    try:
        answer = str(eval(recv[:-2]))
        print 'Sent: ' + str(answer)
        s.send(answer)
    except:
        print s.recv(1000)
        print s.recv(1000)
        print s.recv(1000)
        break
```

It works at first, but after a while large numbers start to use `,` as a separator, which Python doesn't like. We can strip commas, no problem:

```
recv = recv.replace(',', '').replace('.', '')
```

Then, after a few more problems, Roman numerals start to appear, like this:

```
IX * VIII =
```

You'd think that Trend Micro has advanced with the rest of humanity since the fall of the Roman Empire, but apparently they still have some, um, legacy problems. Not to worry, there's a Python lib for that and it's called `romanclass`. We're gonna catch every Roman numeral with a regex, make it an instance of `romanclass.Roman` and cast to integer.

```
from romanclass import Roman

def roman_to_int_repl(match):
    return str(int(Roman(match.group(0))))

roman_regex = re.compile(r'\b(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b')

[...]
recv = roman_regex.sub(roman_to_int_repl, recv)
[...]
```

Some people don't know that Python's `re.sub` can accept a function as a replacement argument, but it's a really cool feature you should by all means use.

After Roman numerals you get plain English:

```
five + seven =
```

Let's just use some random method from Stack Overflow. It's simple and it works:

```
def text_to_int(textnum, numwords={}):
    if not numwords:
        units = [
          "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
          "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
          "sixteen", "seventeen", "eighteen", "nineteen",
        ]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)
    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)
        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
    return result + current


def english_to_int_repl(match):
    return str(text_to_int(match.group(1)))

english_regex = re.compile(r'((?:[a-z]+\s?)+)(?=\W{3,})')

[...]
recv = english_regex.sub(english_to_int_repl, recv)
[...]
```

Here's what the problems look like closer to the end:

```
eight hundred ninety nine million, one hundred sixty eight thousand eleven - 556226 * ( 576 - 21101236 ) * 948 - ( 29565441 + thirty six ) * 182,745 - 6,124,792 + CMLXXVI - 647 =
```

Fortunately, our code is fine with that: we just replace every weird monstrosity with an integer and `eval` the final string.

Let's take a look at the final version:

```
import socket
import re
from romanclass import Roman


def text_to_int(textnum, numwords={}):
    if not numwords:
        units = [
          "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
          "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
          "sixteen", "seventeen", "eighteen", "nineteen",
        ]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)
    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)
        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
    return result + current


def english_to_int_repl(match):
    return str(text_to_int(match.group(1)))


def roman_to_int_repl(match):
    return str(int(Roman(match.group(0))))


roman_regex = re.compile(r'\b(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b')
english_regex = re.compile(r'((?:[a-z]+\s?)+)(?=\W{3,})')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ctfquest.trendmicro.co.jp', 51740))

while True:
    recv = s.recv(1000)
    print 'Received: ' + recv
    recv = recv.replace(',', '').replace('.', '')
    recv = roman_regex.sub(roman_to_int_repl, recv)
    recv = english_regex.sub(english_to_int_repl, recv)
    print 'Converted: ' + recv
    try:
        answer = str(eval(recv[:-2]))
        print 'Sent: ' + str(answer)
        s.send(answer)
    except:
        print s.recv(1000)
        print s.recv(1000)
        print s.recv(1000)
        break
```

Not the best piece of code in the world, but it works.

```
Congratulations!
The flag is TMCTF{U D1D 17!}
```
