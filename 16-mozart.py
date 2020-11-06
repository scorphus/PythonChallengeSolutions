#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/mozart.html

from auth import get_last_src_url
from auth import read_url
from cache import cached
from image import image_to_text
from io import BytesIO
from PIL import Image


@cached("16-mozart.cache")
def generate_aligned_image(image, pivot, cache):
    """Generates a new image by aligning the rows of the original using
    the pivot pixel as reference"""
    if cache.get("new_image"):
        return Image.frombytes(image.mode, image.size, cache["new_image"])
    new_image = Image.new(image.mode, image.size)
    for y in range(image.height):
        width_iter = iter(range(image.width))
        pixels = list()
        threshold = 0
        for x in width_iter:
            pixels.append(image.getpixel((x, y)))
            if pixels[-1] == pivot:
                threshold = image.width - x
                break
        for x, pixel in enumerate(pixels):
            new_image.putpixel(((threshold + x) % image.width, y), pixel)
        for x in width_iter:
            new_image.putpixel((threshold + x - image.width, y), image.getpixel((x, y)))
    cache["new_image"] = new_image.tobytes()
    return new_image


def find_pivot(image, color):
    for i, c in enumerate(zip(*([iter(image.getpalette())] * 3))):
        if c == color:
            return i


url = "http://www.pythonchallenge.com/pc/return/mozart.html"
image_content = read_url(get_last_src_url(url))
image = Image.open(BytesIO(image_content))
pivot = find_pivot(image, (255, 0, 255))
new_image = (
    generate_aligned_image(image, pivot)
    .convert("RGB")
    .crop((50, 50, *[n - 50 for n in image.size]))
    .resize([n // 4 for n in image.size])
)
print(image_to_text(new_image, 95, 3))
