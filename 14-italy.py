#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/italy.html

from auth import get_last_src_url
from auth import read_riddle
from auth import read_url
from html.parser import HTMLParser
from io import BytesIO
from PIL import Image


def spiral_and_transform(image):
    """Creates a new image from `image`, in a spiral way from inside out"""
    x = y = 0
    dx, dy = 0, -1
    new_image = Image.new(image.mode, (100, 100))
    for pixel in reversed(image.getdata()):
        if -50 < x <= 50 and -50 < y <= 50:
            new_image.putpixel((x + 49, 50 - y), pixel)
        if x == y or x < 0 and x == -y or x > 0 and x == 1 - y:
            dx, dy = -dy, dx
        x, y = x + dx, y + dy
    return new_image


class CatNameSayer(HTMLParser):
    """Parses an HTML and display data for <b> tags"""

    def handle_starttag(self, tag, _):
        self.show = tag == "b"

    def handle_data(self, data):
        if self.show:
            print(data)
        self.show = False


url = "http://www.pythonchallenge.com/pc/return/italy.html"
image_content = read_url(get_last_src_url(url))
image = Image.open(BytesIO(image_content))

spiral_and_transform(image).save("14-italy.png", "PNG")
print("Open 14-italy.png only to see a cat")

cat = read_riddle(url.replace("italy", "cat"))
CatNameSayer().feed(cat)
