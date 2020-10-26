#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/italy.html

from base64 import encodebytes
from PIL import Image  # pip install pillow
from urllib.request import Request
from urllib.request import urlopen


url = "http://www.pythonchallenge.com/pc/return/wire.png"
auth = encodebytes(b"huge:file").decode().rstrip()
headers = {"Authorization": f"Basic {auth}"}

image = Image.open(urlopen(Request(url=url, headers=headers)))
new_image = Image.new(image.mode, (100, 100))

x = y = 0
dx, dy = 0, -1
for pixel in reversed(image.getdata()):
    if -50 < x <= 50 and -50 < y <= 50:
        new_image.putpixel((x + 49, 50 - y), pixel)
    if x == y or x < 0 and x == -y or x > 0 and x == 1 - y:
        dx, dy = -dy, dx
    x, y = x + dx, y + dy

new_image.save("14-italy.png", "PNG")
print("Open 14-italy.png")
