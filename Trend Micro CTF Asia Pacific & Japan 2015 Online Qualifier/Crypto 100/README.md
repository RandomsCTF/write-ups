# Crypto 100

## Problem

You're given an RSA public key and an encrypted message which contains a flag. Get the flag.

There's also a hint about "1bit" being wrong in the public key.

## Solution

Commendation: @emedvedev

First of all, let's get the information about the public key:

```
$ openssl rsa -pubin -in PublicKey.pem -noout -text -modulus
Modulus (256 bit):
    00:b6:2d:ce:9f:25:81:63:57:23:db:6b:18:8f:12:
    f0:46:9c:be:e0:cb:c5:da:cb:36:c3:6e:0c:96:b6:
    ea:7b:fc
Exponent: 65537 (0x10001)
Modulus=B62DCE9F2581635723DB6B188F12F0469CBEE0CBC5DACB36C36E0C96B6EA7BFC
```

It's 256 bit RSA that's easily crackable even here in 2015 (are you proud of me, grandson? granddaughter? grand... um... person?). Let's take a look at the prime factors of our modulus:

```
$ python -c 'print int(0xB62DCE9F2581635723DB6B188F12F0469CBEE0CBC5DACB36C36E0C96B6EA7BFC)'
82401872610398250859431855480217685317486932934710222647212042489320711027708
```

Here's what FactorDB says: `8240187261...08<77> = 2^2 · 3^2 · 11 · 19 · 307 · 180728237 · 2478211847<10> · 7964994460...79<53>`.

Clearly, something's wrong with the key, so let's take a look at the hint we're given: "1bit". What the hell is that? First bit? One bit? `1`—as opposed to `0`—bit? If I were a smarter person, I'd just flip the last bit, make our modulus an odd number and see that it can be factorized into two primes, but I'm an aspiring retard with an attention span of two and a half seconds, so thinking is definitely not something I'd do. Let's just flip all the bits instead and see what happens. After all, "do a stupid thing, see what happens" is pretty much a story of my life, why change now.

So, FLIP ALL THE BITS!

```
import requests
import re

bits = "1011011000101101110011101001111100100101100000010110001101010111001000111101101101101011000110001000111100010010111100000100011010011100101111101110000011001011110001011101101011001011001101101100001101101110000011001001011010110110111010100111101111111100"
regex = re.compile(r'</tr><tr><td>(.*?)</td>.*</td>\s*<td>(.*)\s*More information.*?</td>\s*</tr>\s*</table>', re.DOTALL)
strings = {}


def get_factors(query):
    req = requests.get("http://factordb.com/index.php?query=%s" % query)
    table = regex.findall(req.text)[0]
    result = re.sub(r'<.*?>', ' ', table[1])
    result = re.sub(r'  &middot;  ', 'x', result)
    result = re.sub(r'&gt;', '> ', result)
    result = re.sub(r'  &lt;', '<', result)
    return table[0] + " " + result


def flip(str, pos):
    return str[:pos]+("1" if str[pos]=="0" else "0")+str[pos+1:]


for pos in xrange(len(bits)):
    strings[int(flip(bits, pos), 2)] = 1


for number in strings.keys():
    print "Number: %s" % number
    print get_factors(number)
```

Pay attention: this script queries FactorDB 256 times—without permission—which is indecent and not what the cool kids should do. If this is something that deeply hurts your feelings, close this page, take a deep breath, pet a cute furry animal of your choice, smell a flower, kiss a girl. Calm down.

For the ones who are not disturbed that easily, let's keep on, we're almost done.

Going through the output, there's only one number that's easily factorized into two primes:

```
8240187261...09<77> = 279125332373073513017147096164124452877<39> · 295214597363242917440342570226980714417<39>
```

It's our number with the last bit flipped from `0` to `1`, which is consistent with what the hint says. Let's use `rsatool` to generate the private key.

```
$ python rsatool.py -p 279125332373073513017147096164124452877 -q 295214597363242917440342570226980714417 -o private.key
Using (p, q) to initialise RSA instance

n =
b62dce9f2581635723db6b188f12f0469cbee0cbc5dacb36c36e0c96b6ea7bfd

e = 65537 (0x10001)

d =
6615bd16c8f97c25345e9be0a32bc59f99ce0e404f21bebbe97ce3bd6dc78d01

p = 279125332373073513017147096164124452877 (0xd1fd9565dae264f5fd57953dbfb9e80d)

q = 295214597363242917440342570226980714417 (0xde1843682ab2b482ccff506f02cf77b1)

Saving PEM as private.key
```

And now for decryption:

```
$ cat message.txt | base64 -D | openssl rsautl -decrypt -inkey private.key
TMCTF{$@!zbo4+qt9=5}
```

Isn't that what you always wanted? Your whole life? I know it is.

Congratulations.
