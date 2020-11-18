# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/

from itertools import product
from math import sqrt


def factorize(number):
    """Obtains the factors of `number`"""
    factors = set()
    for factor in range(2, int(sqrt(number)) + 1):
        if number % factor == 0:
            factors.update({factor, number // factor})
    return sorted(factors)


def image_to_text(image, threshold=10, skip=6, white="##", black="  "):
    """Converts an image to text, lighting pixel greater than a threshold and
    skiping some rows/cols"""
    image = image.crop(image.getbbox()).convert("L")
    cols, rows = -(-image.width // skip), -(-image.height // skip)  # ceiling
    lines = [[black] * cols for _ in range(rows)]
    for (x, y) in product(range(0, image.width, skip), range(0, image.height, skip)):
        if image.getpixel((x, y)) > threshold:
            lines[y // skip][x // skip] = white
    return "\n".join(filter(str.strip, map("".join, lines)))
