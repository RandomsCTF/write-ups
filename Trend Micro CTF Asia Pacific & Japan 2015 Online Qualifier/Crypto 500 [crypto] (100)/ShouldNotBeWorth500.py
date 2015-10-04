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
