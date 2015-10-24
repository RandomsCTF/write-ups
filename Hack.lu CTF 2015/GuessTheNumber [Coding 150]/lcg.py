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
