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
