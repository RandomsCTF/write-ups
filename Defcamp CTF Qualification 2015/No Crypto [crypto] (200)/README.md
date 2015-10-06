# No Crypto (Crypto 200)

## Problem

The folowing plaintext has been encrypted using an unknown key, with AES-128 CBC:

Original:
```
Pass: sup3r31337. Don't loose it!
```

Encrypted:
```
4f3a0e1791e8c8e5fefe93f50df4d8061fee884bcc5ea90503b6ac1422bda2b2b7e6a975bfc555f44f7dbcc30aa1fd5e
```

IV:
```
19a9d10c3b155b55982a54439cb05dce
```

How would you modify it so that it now decrypts to:
```
Pass: notAs3cre7. Don't loose it!
```

This challenge does not have a specific flag format.

## Solution

Credit: [@emedvedev](https://github.com/emedvedev)

While this challenge doesn't need a particularly long write-up, I'll try to explain in detail how byte-flipping attacks on CBC work. If you only need the challenge, skip right to the [Modifying first block](#modifying-first-block) part.


#### CBC explained

AES is a block cipher, which means that plaintext is split into blocks: every block is encoded with an encryption key of an equal length (128, 192 or 256 bits in case of AES). By itself, a block cipher is only suitable for secure transmission of one block; in order to encode larger amounts of data, various _modes of operation_ were introduced. CBC (Cipher Block Chaining) is one of such modes.

Let's take a look at how CBC works:

![](cbc.png?raw=true)

To encrypt a block in CBC mode each block's plaintext is XORed with the preceding block's ciphertext (or IV for the first block), then encoded with a chosen algorithm (AES in our case). CBC is widely-used, but because of its properties it's vulnerable to byte-flipping attacks: when you change a byte in a block's ciphertext, the byte in the same position of the next block's plaintext gets changed because of the XOR operation. Let's explore that:

```
$ echo "Flip this byte: A" | openssl aes-128-cbc -K AABBAABBAABBAABBAABBAABBAABBAABB -iv AABBAABBAABBAABBAABBAABBAABBAABB > message
$ xxd message
0000000: 9861 cec0 8d8c 476d 0d1d b674 daf1 44c1  .a....Gm...t..D.
0000010: 7a95 aa2b 312a d804 3bf8 92ba 423e bf50  z..+1*..;...B>.P
```

Block size of AES-128 is 16 bytes, which means that the letter "A" that we need to change falls into the first byte of the second block:

```
F  l  i  p     t  h  i  s     b  y  t  e  :
98 61 ce c0 8d 8c 47 6d 0d 1d b6 74 da f1 44 c1

A  \n
7a 95 aa 2b 31 2a d8 04 3b f8 92 ba 42 3e bf 50
```

As described earlier, to flip a byte of a block's plaintext we need to flip the corresponding byte of the preceding block's ciphertext, which means that changing `98` (first byte of the first block) will change `A` in the encoded message. To change `A` to `Z` we'll need to XOR `98` with `A XOR Z`, so let's find out the value with Python:

```
>>> hex(0x98 ^ ord("A") ^ ord("Z"))
'0x83'
```

Let's patch our ciphertext to change `98` to `83`, decode it and see if it worked:

```
$ printf '\x83' | dd of=message bs=1 seek=0 count=1 conv=notrunc &> /dev/null
$ cat message | openssl aes-128-cbc -d -K AABBAABBAABBAABBAABBAABBAABBAABB -iv AABBAABBAABBAABBAABBAABBAABBAABB
???&֖??8?4?qX9?Z
```

Notice that the `A` has changed to `Z` as we intended, so the attack actually succeeded. However, the first block is now garbled since we changed its ciphertext, and this fact makes the attack almost unfeasible outside of the scope of academical curiosity.

Still, there are at least two possible ways this attack can be used to get significant results: changing the first block when the IV is known and can be modified, and bypassing sanitization/validation when AES-CBC is used for secure data storage in certain rare cases.


#### Bypassing validation

Consider the following scenario:

1. A web client for a certain service has fields "username", "about" and "admin" (optional) for every user.
2. Once registered, a user has their data serialized as "username=alice;about=I am alice;admin=true" or "username=mallory;about=I am mallory" and encrypted with AES-CBC.
3. User input is sanitized and escaped, it's not allowed to use any special characters.
4. Encrypted data string is stored on the client side in HTML5 local storage.

Peter the Programmer had some concerns about storing data on the client side: it just feels wrong, and is probably unsafe. He shared the concern, but his CEO said there is simply no time and no resources to implement a proper server-side database in time for the important launch. They go to Wikipedia: the article says that "there are no known practical attacks that would allow anyone to read correctly implemented AES encrypted data," so Peter makes peace with it.

Let's see why Peter is wrong:

```
$ echo -n "username=mallory;about=I am mallory aaaaaaaaaaaaaaaaaaaaaaaaaaa" | openssl aes-128-cbc -K AABBAABBAABBAABBAABBAABBAABBAABB -iv AABBAABBAABBAABBAABBAABBAABBAABB | xxd
0000000: 1076 a770 fddd 9a5b f65f 6de3 3235 a8ff  .v.p...[._m.25..
0000010: c114 617e 43a9 5dc7 e70b 41f6 b2b8 1ed8  ..a~C.]...A.....
0000020: ce8b 424c 759d 34a6 6194 a7fb 7f21 827e  ..BLu.4.a....!.~
0000030: 5ae0 9395 0f4b 1068 3983 bd92 15c9 413a  Z....K.h9.....A:
```

This is exactly the case when scrambling one of the encrypted blocks can be tolerated: if the attack is performed correctly, the "about" field will be scrambled, but the serialization structure will still hold. Mallory just needs to flip one byte to change the underscore preceding "admin" to a semicolon. Let's match the plaintext to blocks:

```
u  s  e  r  n  a  m  e  =  m  a  l  l  o  r  y
10 76 a7 70 fd dd 9a 5b f6 5f 6d e3 32 35 a8 ff

;  a  b  o  u  t  =  I     a  m     m  a  l  l
c1 14 61 7e 43 a9 5d c7 e7 0b 41 f6 b2 b8 1e d8

o  r  y     a  a  a  a  a  a  a  a  a  a  a  a
ce 8b 42 4c 75 9d 34 a6 61 94 a7 fb 7f 21 82 7e

a  a  a  a  a  a  a  a  a  a  a  a  a  a  a
5a e0 93 95 0f 4b 10 68 39 83 bd 92 15 c9 41 3a
```

Now we'll write a Python function that takes the known plaintext of a block, a desired plaintext and the ciphertext of the preceding block, and returns the modified ciphertext:
```
def mod_block(plaintext, mod, prev_block):
    diff = [ord(a) ^ ord(b) for a, b in zip(plaintext[:16], mod[:16])]
    return ''.join(["%0.2x" % (int(prev_block[i*2:i*2+2], 16) ^ diff[i]) for i in range(16)])
```

Let's run it:
```
>>> mod_block(
...   "aaaaaaaaaaaaaaa ",
...   "aaaa;admin=true ",
...   "ce8b424c759d34a66194a7fb7f21827e"
... )
'ce8b424c2f9d31aa699bfbee6c35867e'
```

Now let's see if it worked:
```
username=mallory;about=I am mall? 腳???/???aaaa;admin=true
```

Done: Mallory is admin now.


#### Modifying first block

Modifying the first block of the ciphertext is done similarly to the previous scenario with two important details that are both connected to the fact that there is no preceding block.

1. Instead of preceding block's ciphertext we use IV.
2. Nothing gets scrambled in the plaintext after deciphering.

This means that if you have access to IV and can modify it, you'll be able to change the first block of plaintext with no evidence of tampering. This is exactly how the challenge is solved.

We need to change `Pass: sup3r31337. Don't loose it!` to `Pass: notAs3cre7. Don't loose it!`. We can use the Python function from the previous example and input IV instead of the preceding block, otherwise it's exactly the same:

```
>>> def mod_block(plaintext, mod, prev_block):
...     diff = [ord(a) ^ ord(b) for a, b in zip(plaintext[:16], mod[:16])]
...     return ''.join(["%0.2x" % (int(prev_block[i*2:i*2+2], 16) ^ diff[i]) for i in range(16)])
...
>>> print mod_block(
...     'Pass: sup3r31337',
...     'Pass: notAs3cre7',
...     '19a9d10c3b155b55982a54439cb05dce',
... )
19a9d10c3b15464f9c585543cef10bce
```

`19a9d10c3b15464f9c585543cef10bce` is our new IV and the flag for the challenge.
