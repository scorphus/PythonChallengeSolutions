#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/copper.html

from base64 import encodebytes
from PIL import Image
from PIL import ImageSequence
from urllib.request import Request
from urllib.request import urlopen


url = "http://www.pythonchallenge.com/pc/hex/copper.html"
auth = encodebytes(b"butter:fly").decode().rstrip()
headers = {"Authorization": f"Basic {auth}"}

riddle_source = urlopen(Request(url=url, headers=headers)).read().decode()
riddle_data = riddle_source.split("<!--", 1)[-1].split("-->", 1)[0].strip()
print(riddle_data)

replacement = [s for s in riddle_data.split() if "." in s][0]
url_parts = url.split("/")
url_parts[-1] = replacement
url = "/".join(url_parts)

image = Image.open(urlopen(Request(url=url, headers=headers)))
width, height = image.size
assert width == height

white_pixels = [frame.getbbox()[:2] for frame in ImageSequence.Iterator(image)]
min_w = min(p[0] for p in white_pixels)
diff_w = max(p[0] for p in white_pixels) - min_w

word = {}
char_count = char_width = x = y = 0
x_limits = y_limits = (0, 0)
for dx, dy in white_pixels:
    dx = (dx - min_w - diff_w // 2) // 2
    dy = (dy - min_w - diff_w // 2) // 2
    if dx == 0 and dy == 0:
        if char_width == 0:
            char_width = x_limits[1] * 2
        x, y = char_count * char_width, 0
        char_count += 1
    x += dx
    y += dy
    word[(x, y)] = "#"
    x_limits = (min(x_limits[0], x), max(x_limits[1], x + 1))
    y_limits = (min(y_limits[0], y), max(y_limits[1], y + 1))

print(
    "\n".join(
        "".join(word.get((x, y), " ") for x in range(*x_limits))
        for y in range(*y_limits)
    )
)
