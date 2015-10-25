# GuessTheNumber

## Problem

The teacher of your programming class gave you a tiny little task: just write a guess-my-number script that beats his script.

He also gave you some hard facts:
- he uses some LCG with standard glibc LCG parameters
- the LCG is seeded with server time using number format YmdHMS (python strftime syntax)
- numbers are from 0 up to (including) 99
- numbers should be sent as ascii string

You can find the service on school.fluxfingers.net:1523

## Solution

Credit: [@emedvedev](https://github.com/emedvedev)

Communicating with the service opens a guess-the-number game, which uses a PRNG to generate numbers and exposes the right number on a failed try:

```
> Welcome to the awesome guess-my-number game!
> It's 24.10.2015 today and we have 23:34:22 on the server right now. Today's goal is easy:
> just guess my 100 numbers on the first try within at least 30 seconds from now on.
> Ain't difficult, right?
> Now, try the first one:
< 0
> Wrong! You lost the game. The right answer would have been '62'. Quitting.
```

Let's take a look at the hints we're given: LCG (linear congruental generator) is a pseudorandom number generator which is defined by the following relation:

```
X(n+1) = (a * X(n) + c) mod m
```

Here, `X` is the sequence, where `X(0)` is the seed (start value), and the rest of the numbers are pre-defined. [Wikipedia](https://en.wikipedia.org/wiki/Linear_congruential_generator) gives a lot more information as well as `glibc` parameters, which we'll need in our challenge. With the parameters from `glibc` our sequence will be defined as:

```
X(n+1) = (1103515245 * X(n) + 12345) mod 2^31
```

The seed is server time formatted as `YmdHMS`: for `24.10.2015 23:34:22` the seed would be `20152410233422`.

Let's start by writing a simple Python script with an LCG taking a `time` object as a seed and returning `number % 100` (since we'll need 0-99 as an answer), as well as a wrapper class for communicating with a socket (unnecessary, but I'm used to it):

```
import socket
import time


class LCG():

    def __init__(self, timeseed):
        self.a = 1103515245
        self.c = 12345
        self.m = 2**31
        self.state = int(time.strftime('%Y%m%d%H%M%S', timeseed))

    def round(self):
        self.state = (((self.state * self.a) + self.c) % self.m)
        return self.state % 100


class CTFSocket():

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def read(self):
        return self.socket.recv(4096)

    def send(self, message):
        return self.socket.send(str(message))


conn = CTFSocket("school.fluxfingers.net", 1523)
read = conn.read()
server_time = time.strptime(read[50:87],
                            "%d.%m.%Y today and we have %H:%M:%S")
lcg = LCG(server_time)
rnd = lcg.round()

print rnd
conn.send(rnd)
print conn.read()
```

Checking the output, the number we get proves to be incorrect:
```
48
Wrong! You lost the game. The right answer would have been '47'. Quitting.
```

Time for some long and tiresome trial and error. The breakthrough happens after checking whether the number we get from the server appears at some other place in a sequence rather than the beginning. We modify the code to open the connection 10 times and compare the correct answer with the first 200 elements from our LCG sequence with the same seed:

```
for sample in xrange(1, 10):
    print 'Sample #%i' % sample

    conn = CTFSocket("school.fluxfingers.net", 1523)
    read = conn.read()
    server_time = time.strptime(read[50:87],
                                "%d.%m.%Y today and we have %H:%M:%S")
    lcg = LCG(server_time)
    rnd = lcg.round()
    conn.send("101")
    num = int(conn.read().split("'")[1])

    print ' The answer should be %i' % num

    sequence = []
    for pos in xrange(1, 200):
        if rnd == num:
            print ' Answer found in the LCG sequence at pos %i' % pos
        rnd = lcg.round()

    time.sleep(1)
```

Let's run it:

```
Sample #1
 The answer should be 2
 [...]
 Answer found in the LCG sequence at pos 100
Sample #2
 The answer should be 95
 [...]
 Answer found in the LCG sequence at pos 100
 [...]
Sample #3
 The answer should be 40
 [...]
 Answer found in the LCG sequence at pos 100
 [...]
Sample #4
 The answer should be 26
 [...]
 Answer found in the LCG sequence at pos 100
 [...]
Sample #5
 The answer should be 71
 Answer found in the LCG sequence at pos 100
 [...]
```

Apparently, sequence element #100 is always our answer #1. When we try to go forward, it turns out that the element #101 is not the answer #2, but the element #99 is. That is enough to guess what the server algorithm is: take the first 100 numbers from the LCG and run them backwards.

Here's the code to replicate the whole sequence:

```
seeds = []

conn = CTFSocket("school.fluxfingers.net", 1523)
read = conn.read()
server_time = time.strptime(read[50:87],
                            "%d.%m.%Y today and we have %H:%M:%S")
lcg = LCG(server_time)
rnd = lcg.round()
seeds.append(rnd)

for i in xrange(99):
    rnd = lcg.round()
    seeds.append(rnd)

for num in reversed(seeds):
    conn.send(str(num))
    print conn.read()
```

Run it and get the flag:

```
Congrats! You won the game! Here's your present:
flag{don't_use_LCGs_for_any_guessing_competition}
```

## Another take

There's another take on this problem that's just too creative not to mention here: some teams solved the challenge by opening 101 connections at the same second (to have the same seed), then used each connection as an oracle for getting subsequent numbers.

The method works like this:
- open 101 connections in one second so that they all have the same seed;
- use conn #1 to get the first number from the server;
- input the number you got from conn #1 into conn #2, get the second number #2;
- input the first two numbers into conn #3, get the third number;
- ...
- consecutively get 100 numbers with 100 connections, input them using connection #101;
- get the flag!

Pretty neat.
