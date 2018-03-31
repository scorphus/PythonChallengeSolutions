#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/mozart.html

from PIL import Image  # pip install pillow
from base64 import encodebytes
from urllib.request import Request, urlopen

url = 'http://www.pythonchallenge.com/pc/return/mozart.gif'
auth = encodebytes(b'huge:file').decode().rstrip()
headers = {'Authorization': f'Basic {auth}'}

image = Image.open(urlopen(Request(url=url, headers=headers))).convert('RGB')
new_image = Image.new(image.mode, (2 * image.width, image.height))

for y in range(image.height):
    X = iter(range(image.width))
    row = list()
    for x in X:
        row.append(image.getpixel((x, y)))
        if row[-1][0] == row[-1][2] == 255 and row[-1][1] == 0:
            threshold = image.width - x
            break
    for x, pixel in enumerate(row):
        new_image.putpixel((threshold + x, y), pixel)
    for x in X:
        new_image.putpixel((threshold + x, y), image.getpixel((x, y)))

new_image.save('16-mozart.png', 'PNG')
print('Open 16-mozart.png')
