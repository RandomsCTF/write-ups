# Programming 100

## Problem

You have to play a game of "choose a square with a different color". The problem is inspired by color vision test games such as this one: http://106.186.25.143/kuku-kube/en-3/

## Solution

Commendation: [@emedvedev](https://github.com/emedvedev)

After you try to play by hand a little bit, you see that the difference between colors gets really small and—very soon—just indistinguishable to the human eye, and the squares get smaller up to 1x1 in the end, too. Up to a certain point you can actually use color range select in Photoshop to find the odd square and then click it, but let's not dig into that: after all, we have a programming challenge.

Here's what we'll do, step by step:

1. Connect to the server, fetch the image.
2. Load it into PIL (Python Image Library) and read the pixels.
3. Get an amount of pixels with each individual color (we'll only have two colors: the common and the odd).
4. Get the coordinates for at least one pixel of every color.
5. Find the color that has the least pixels painted with it.
6. Imitate a click on that color's location.

It's all pretty straightforward, so I'll just present the full code:

```
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
```

Congratulations.

```
TMCTF{U must have R0807 3Y3s!}
```
