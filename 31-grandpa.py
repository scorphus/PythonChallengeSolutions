#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/rock/grandpa.html

from auth import get_last_attr
from auth import get_last_src_url
from auth import read_url
from cache import autocached
from etc import factorize
from etc import image_to_text
from io import BytesIO
from PIL import Image


def convert_to_number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def read_riddle_numbers(url):
    for el in ["left", "top", "width", "height", "iterations"]:
        yield convert_to_number(get_last_attr(url, el))


def read_riddle_data(url):
    img_url = get_last_src_url(url)
    return (Image.open(BytesIO(read_url(img_url))), *read_riddle_numbers(url))


@autocached
def mandelbrot_set(left, top, width, height, image_size, max_iter):
    """Generates an upside-down section of the Mandelbrot Set as pixel data for
    an image of size `image_size` doing `max_iter` maximum iterations"""
    dx = width / image_size[0]
    dy = height / image_size[1]
    data = []
    for y in range(image_size[1] - 1, -1, -1):  # is mission's image upside down??? 🤷
        for x in range(image_size[0]):
            c0 = complex(left + x * dx, top + y * dy)
            c, i = complex(), 0
            while True:
                c = c * c + c0
                if abs(c) > 2 or i == max_iter - 1:
                    break
                i += 1
            data.append(i)
    return data


def diff_image(data_a, data_b):
    """Generates a 1-bit black and white image by comparing `data_a` and `data_b`"""
    diff = [int(a > b) for a, b in zip(data_a, data_b) if a != b]
    img = Image.new("1", factorize(len(diff)))
    img.putdata(diff)
    return img


url = "http://www.pythonchallenge.com/pc/rock/grandpa.html"
img, left, top, width, height, iterations = read_riddle_data(url)
mandelbrot = mandelbrot_set(left, top, width, height, img.size, iterations)
diff_img = diff_image(img.getdata(), mandelbrot)
print(image_to_text(diff_img, skip=1, white="▓▓"))
