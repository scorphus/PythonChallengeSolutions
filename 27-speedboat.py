#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/speedboat.html

from auth import get_last_src_url
from auth import read_url
from io import BytesIO
from itertools import islice
from PIL import Image as PILImage
from wand.image import Image as WandImage

import bz2
import keyword


def get_pixel_values(url):
    """Gets pixel values using PIL and Wand — does PIL get them wrong? 🤔"""
    img_url = get_last_src_url(url).replace("jpg", "gif")
    img_content = BytesIO(read_url(img_url))
    pil_pixels = PILImage.open(img_content).tobytes()
    img_content.seek(0)
    return pil_pixels, WandImage(file=img_content).export_pixels()[::4]


def filter_different_pixels(pil_pixels, wand_pixels):
    """Returns a generator of items of `pil_pixels` that are different from
    `wand_pixels` — with `pil_pixels` offset 1 🔞"""
    return (p for p, w in zip(islice(pil_pixels, 1, None), wand_pixels) if p != w)


def extract_solution(data):
    """Decompress data and yields words that aren't “Pythonic”"""
    for word in sorted(set(bz2.decompress(bytes(data)).decode().split())):
        if not keyword.iskeyword(word) and not hasattr(__builtins__, word):
            yield word


url = "http://www.pythonchallenge.com/pc/hex/speedboat.html"
pil_pixels, wand_pixels = get_pixel_values(url)
data = filter_different_pixels(pil_pixels, wand_pixels)
print("url : {}\nuser: {}\npass: {}".format(*extract_solution(data)))
