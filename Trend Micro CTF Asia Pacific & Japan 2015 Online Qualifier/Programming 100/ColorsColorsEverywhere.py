import operator
import re
import requests
from PIL import Image
from StringIO import StringIO

host = "http://ctfquest.trendmicro.co.jp:43210"
ctf = "click_on_the_different_color"


def play(url):
    content = requests.get("%s/%s" % (host, url)).content
    image_name = get_file_name(content)
    if not image_name:
        print content
    else:
        print "Image: %s " % str(image_name)
        img = StringIO(requests.get('%s/img/%s.png' % (host, image_name)).content)
        coords = find_coords(img)
        play("%s?x=%s&y=%s" % (
            image_name, coords[0], coords[1]
        ))


def find_coords(image):
    image = Image.open(image)
    pixels = image.load()

    count = {}
    coords = {}

    for x in xrange(image.size[0]):
        for y in xrange(image.size[1]):
            color = pixels[x, y]
            if color != (255, 255, 255):
                if color not in count:
                    count[color] = 1
                else:
                    count[color] += 1
                if color not in coords:
                    coords[color] = (x, y)

    smallest_square = sorted(count.items(), key=operator.itemgetter(1))[0][0]
    return coords[smallest_square]


def get_file_name(content):
    findall = re.findall(r"href='/(.*?)\?", content)
    if findall:
        return findall[0]
    else:
        return None

play(ctf)
