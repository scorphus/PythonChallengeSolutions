#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/evil.html
# Source includes evil1.jpg
# Try evil2.jpg which then mentions evil2.gfx

from base64 import encodebytes
from urllib.request import Request
from urllib.request import urlopen


def identify(image, header_size=10):
    known_formats = [("FIF", "jpg"), ("GIF", "gif"), ("PNG", "png")]
    header = image[:header_size]
    for fmt, ext in known_formats:
        if fmt in f"{header}":
            return ext


url = "http://www.pythonchallenge.com/pc/return/evil2.gfx"
auth = encodebytes(b"huge:file").decode().rstrip()
headers = {"Authorization": f"Basic {auth}"}
req = urlopen(Request(url=url, headers=headers))
gfx = req.read()

images = [b""] * 5
for i, n in enumerate(gfx):
    images[i % 5] += bytes([n])

for i, image in enumerate(images):
    ext = identify(image)
    with open(f"12-evil2-{i+1}.{ext}", "wb") as image_file:
        image_file.write(image)

print("Open 12-evil2-*")
