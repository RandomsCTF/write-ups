# Crypto 500

## Problem

Think about two different alphabetical strings with the same lengths.
After you encode the strings with Base64 respectively, if you find characters located in the same position between the two strings, then you may want to extract them.
You may find examples where the final strings are ‘2015’ and ‘Japan’ if you place the extracted characters from left to right in order.

Example:
CaEkMbVnD→(Base64)→Q_2_FFa_01_iVm_5_E
GePoMjXNW→(Base64)→R_2_VQb_01_qWE_5_X

aBckjTiRgbpS→(Base64)→YU_J_j_a_2_p_U_a_VJnY_n_BT
URehZQjLyvwk→(Base64)→VV_J_l_a_F_p_R_a_kx5d_n_dr

Character 'a' may appear in the extracted string like the example above, character `f` will never appear.
Please find a list of characters that would not appear in the extracted string, even if you specify any alphabetical characters in the input.
Once you come up with a list of characters, please sort the characters in the order of ASCII table and generate a SHA1 hash value in lower case.
This is the flag you are looking for.

Please submit the flag in the format of 'TMCTF{<flag>}'.

## Solution

Commendation: [@emedvedev](https://github.com/emedvedev)

I don't get why this challenge was worth 500 points. I also don't get why is it a _crypto_ challenge. It's ridiculously easy once you learn how base64 is formed.

Let's refresh the memory: when you want to encode a string in Base64, it's split into groups of 6 bits (because 6 bits have a maximum of exactly 64 values) and each group is converted into a number, which is in turn converted into a character using Base64 index table. Wikipedia has a good article explaining everything in more detail.

What's important for this challenge is that we're only encoding _alphabetical strings_, so naturally there will be unused characters in Base64: [a-zA-Z] combinations can't make up every possible 6-bit group.

Something else worth mentioning: to solve this challenge, you only need initial strings up to three letters in length, because 8*3 is evenly divisible by 6, so a three-letter string will be enough to comprise every possible Base64 character position, as asked in the challenge description. If the string being encoded is not evenly divisible by three, a padding is applied, so we can try 1 and 2 as well.

That's how this challenge can be solved:
0. Get a reference list of every Base64 character in the order of ASCII table (symbols, uppercase, lowercase).
1. Base64-encode every alphabetical string of lengths 1, 2 and 3.
2. Given an encoded string, store a number of occurrences of every character in a certain position.
3. Remove every character with a number of occurrences of more than 2 from the reference list.
4. Get a sha1 checksum of whatever's left in a reference list. This is your flag.

Code speaks louder than words:
```
import string
import itertools
from base64 import b64encode
from hashlib import sha1

b64chars = "+/"+string.digits+string.uppercase+string.lowercase
charset = string.uppercase+string.lowercase
combinations = [
    itertools.product(charset, repeat=1),
    itertools.product(charset, repeat=2),
    itertools.product(charset, repeat=3)
]
mappings = {}

for comb in xrange(len(combinations)):
    for block in combinations[comb]:
        base = b64encode(''.join(block))
        for index in xrange(len(base)):
            if comb not in mappings:
                mappings[comb] = {}
            if index not in mappings[comb]:
                mappings[comb][index] = {}
            if base[index] not in mappings[comb][index]:
                mappings[comb][index][base[index]] = 0
            mappings[comb][index][base[index]] += 1

print mappings

nonmatching = [a for a in "+/"+string.digits+string.uppercase+string.lowercase]
for comb in mappings.keys():
    for pos in mappings[comb].keys():
        for key in mappings[comb][pos].keys():
            if mappings[comb][pos][key] > 0 and key in nonmatching:
                nonmatching.remove(key)

print ''.join(nonmatching)
print "TMCTF{%s}" % sha1(''.join(nonmatching)).hexdigest()
```

Done.
