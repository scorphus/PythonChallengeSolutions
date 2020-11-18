#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/rock/beer.html


from auth import get_last_src_url
from auth import read_url
from collections import Counter
from etc import image_to_text
from io import BytesIO
from itertools import islice
from itertools import product
from math import sqrt
from PIL import Image


def read_image(url):
    img_url = get_last_src_url(url).replace("1", "2").replace("jpg", "png")
    img = Image.open(BytesIO(read_url(img_url)))
    return img.mode, img.getdata()


def gen_images(mode, data, pixel_values):
    """Generates images out of `data`, removing the brightest pixels according
    to the order in `pixel_values` — as hinted by the mission"""
    images = []
    while pixel_values:
        *pixel_values, second_brightest, _ = pixel_values
        data = [d for d in data if d < second_brightest]
        size = int(sqrt(len(data)))  # that's also one of the hints
        img = Image.new(mode, (size, size))
        for (y, x), pixel in zip(product(range(size), repeat=2), data):
            img.putpixel((x, y), (pixel == pixel_values[-1]) * 255)
        img = img.crop(img.getbbox())
        if 0 not in islice(img.getdata(), img.width):  # is there a top white border?
            img = img.crop((1, 1, img.width - 1, img.height - 1))
            img = img.crop(img.getbbox())
            images.append(img.resize((img.width // 2, img.height // 2)))
    return images


def combine(images):
    width = sum(img.width for img in images) + len(images)
    height = max(img.height for img in images)
    image = Image.new(img_mode, (width, height))
    x_offset = 0
    for img in images:
        image.paste(img, (x_offset, height - img.height))
        x_offset += img.width + 1
    return image


url = "http://www.pythonchallenge.com/pc/rock/beer.html"
img_mode, img_data = read_image(url)
pixel_values = sorted(Counter(img_data))
images = gen_images(img_mode, img_data, pixel_values)
image = combine(images)
print(image_to_text(image, skip=1))
