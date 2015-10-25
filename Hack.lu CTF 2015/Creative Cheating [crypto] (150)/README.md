# Creative Cheating

## Problem

Mr. Miller suspects that some of his students are cheating in an automated computer test. He [captured some traffic](dump.pcapng) between crypto nerds Alice and Bob. It looks mostly like garbage but maybe you can figure something out.

He knows that Alice's RSA key is (n, e) = (0x53a121a11e36d7a84dde3f5d73cf, 0x10001) (192.168.0.13) and Bob's is (n, e) = (0x99122e61dc7bede74711185598c7, 0x10001) (192.168.0.37)

## Solution

Credit: [@emedvedev](https://github.com/emedvedev)

We're given a PCAP dump, so let's examine it with Wireshark:

![](exchange.png?raw=true)

Alice (`192.168.0.13`) sends Bob (`192.168.0.37`) TCP packets with Base64-encoded data. Let's follow the stream, export all the packets and decode them one by one:

![](stream.png?raw=true)

```
import base64

packets = []
with open('stream.txt') as lines:
  for line in lines:
    decoded = base64.b64decode(line)
    packets.append(decoded)
```

Our decoded packets look like this (notice that `SEQ` is not unique, we'll need it later):

```
SEQ = 13; DATA = 0x3b04b26a0adada2f67326bb0c5d6L; SIG = 0x2e5ab24f9dc21df406a87de0b3b4L;
SEQ = 0; DATA = 0x7492f4ec9001202dcb569df468b4L; SIG = 0xc9107666b1cc040a4fc2e89e3e7L;
SEQ = 5; DATA = 0x94d97e04f52c2d6f42f9aacbf0b5L; SIG = 0x1e3b6d4eaf11582e85ead4bf90a9L;
SEQ = 4; DATA = 0x2c29150f1e311ef09bc9f06735acL; SIG = 0x1665fb2da761c4de89f27ac80cbL;
SEQ = 18; DATA = 0x181901c059de3b0f2d4840ab3aebL; SIG = 0x1b8bdf9468f81ce33a0da2a8bfbeL;
SEQ = 2; DATA = 0x8a03676745df01e16745145dd212L; SIG = 0x1378c25048c19853b6817eb9363aL;
SEQ = 20; DATA = 0x674880905956979ce49af33433L; SIG = 0x198901d5373ea225cc5c0db66987L;
SEQ = 0; DATA = 0x633282273f9cf7e5a44fcbe1787bL; SIG = 0x2b15275412244442d9ee60fc91aeL;
[...]
```

We'll assume that `SEQ` is the sequence order, `DATA` is the content and `SIG` is the signature. The RSA keys we're given are very short, let's query [FactorDB](http://factordb.com) and get `p` and `q` for both Alice and Bob:

- Alice's `p` and `q` are `38456719616722997` and `44106885765559411`.
- Bob's `p` and `q` are `49662237675630289` and `62515288803124247`.

Now, to calculate RSA parameters you would normally use [RSATool](https://github.com/ius/rsatool), but since we're going to need some extra internal logic, let's create a custom RSA class. PyCrypto's `RSA.construct` is going to help us here:

```
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
```

Let's try decrypting the messages now. Since we have Alice sending packets to Bob, we'll have to decode the data with Bob's private key. We'll modify our code to:

1. Order the data entries by `SEQ`.
2. Parse the entries into `SEQ`, `DATA` and `SIG` before storing.
3. Decrypt `DATA` with Bob's key.

```
packets = []
with open('stream.txt') as lines:
    for line in lines:
        decoded = base64.b64decode(line)
        match = regex.match(decoded).groups()
        seq = int(match[0])
        signature = int(match[2], 16)
        data = int(match[1], 16)
        data = bob.decrypt(data)
        data = chr(data)
        packets.append((
            seq,
            data,
            signature
        ))
```

Let's take a look at the output now:

```
(0, '\x0b', 411405985302309658304687940458766L)
(0, '&', 873819575920644857617395222352302L)
(0, '(', 254879289019714299901060498187239L)
(0, 'H', 130444345139656587207775038064682L)
(0, 'f', 525203869657262769956125397333553L)
(0, 'f', 1150325363693092780142319416277197L)
(1, '-', 828076894813745622214013032578722L)
(1, 'Y', 1485043620748068753347713371814689L)
(1, 'j', 1298874456026095076333544275801497L)
(1, 'l', 583679654300144088157196927029953L)
(1, 'u', 1055492309091995510087523902347914L)
(2, '<', 394933299120645953370114156475962L)
(2, 'U', 355616958260007551295456729191093L)
(2, 'a', 355616958260007551295456729191093L)
[...]
```

Clearly, we must only have one character at each position, so we'll have to discard everything else. That's where `SIG` comes into play: since Alice signs every message, we'll add verification and build the string from verified characters only.

```
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
```

Run the script, get the flag:

```
flag{n0th1ng_t0_533_h3r3_m0v3_0n}
```
