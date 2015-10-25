import base64
import re
import gmpy
from Crypto.PublicKey import RSA


class RSAPerson(object):

    def __init__(self, e, p, q):
        self.n = p * q
        self.e = e
        self.p = p
        self.q = q
        self.d = long(gmpy.invert(e, (p-1)*(q-1)))
        self.key = RSA.construct((long(self.n), long(self.e), self.d))

    def sign(self, message):
        return self.key.sign(message, '')

    def verify(self, message, signature):
        return self.key.publickey().verify(message, [signature])

    def encrypt(self, message):
        return self.key.publickey().encrypt(message)

    def decrypt(self, message):
        return self.key.decrypt(message)


alice = RSAPerson(
    0x10001,
    38456719616722997,
    44106885765559411
)
bob = RSAPerson(
    0x10001,
    49662237675630289,
    62515288803124247
)

regex = re.compile(r'SEQ = (\d+); DATA = 0x(.*?)L; SIG = 0x(.*?)L;')

packets = []
with open('stream.txt') as lines:
    for line in lines:
        decoded = base64.b64decode(line)
        match = regex.match(decoded).groups()
        seq = int(match[0])
        signature = int(match[2], 16)
        data = int(match[1], 16)
        data = bob.decrypt(data)
        if alice.verify(data, signature):
            data = chr(data)
            packets.append((
                seq,
                data,
                signature
            ))

print ''.join([packet[1] for packet in sorted(packets)])
