#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/good.html

from auth import get_nth_comment
from PIL import Image
from PIL import ImageDraw


def extract_lines(riddle):
    """Extracts the first and second lines from the riddle"""
    _, *lines, _ = riddle.split("\n\n")
    lines = [line.rsplit(":", 1)[1] for line in lines]
    return [[int(n) for n in line.split(",")] for line in lines]


def gen_image(first, second, fraction):
    """Generates an image with the lines and returns a fraction of it"""
    size = max(first + second) + fraction + 1
    image = Image.new("L", (size, size))
    draw = ImageDraw.Draw(image)
    draw.line(list(zip(first[::2], first[1::2])), 255)
    draw.line(list(zip(second[::2], second[1::2])), 255)
    return image.resize((size // fraction, size // fraction))


def image_to_text(image, threshold):
    """Converts an image to text, lighting pixel greater than a threshold"""
    text = ""
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if image.getpixel((x, y)) > threshold:
                text += "^^"
            else:
                text += "  "
        text += "\n"
    return text.rstrip()


url = "http://www.pythonchallenge.com/pc/return/good.html"
first, second = extract_lines(get_nth_comment(url, 2))
image = gen_image(first, second, 6)
text = image_to_text(image, 15)
print("\n".join(filter(str.strip, text.splitlines())))
