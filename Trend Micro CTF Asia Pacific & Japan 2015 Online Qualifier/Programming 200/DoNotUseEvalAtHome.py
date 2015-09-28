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
