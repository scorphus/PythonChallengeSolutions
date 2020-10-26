#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/5808.html

from PIL import Image  # pip install pillow
from base64 import encodebytes
from urllib.request import Request, urlopen

url = "http://www.pythonchallenge.com/pc/return/cave.jpg"
auth = encodebytes(b"huge:file").decode().rstrip()
headers = {"Authorization": f"Basic {auth}"}

image = Image.open(urlopen(Request(url=url, headers=headers)))
hidden = Image.new(image.mode, [d // 2 for d in image.size])

for x in range(image.width):
    for y in range(image.height):
        if (x + y) % 2 == 0:
            pixel = image.getpixel((x, y))
            hidden.putpixel((x // 2, y // 2), pixel)

hidden.save("11-hidden.jpg", "JPEG")
print("Open 11-hidden.jpg")
