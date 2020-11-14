#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/evil.html

from auth import get_last_src_url
from auth import read_url
from etc import image_to_text
from io import BytesIO
from PIL import Image
from PIL import ImageFile
from PIL import UnidentifiedImageError


ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_next_jpg_images(jpg_url, from_to):
    """Gets next images by changing the number in the URL"""
    for i in range(*from_to):
        jpg_content = read_url(jpg_url.replace("1", f"{i}"))
        try:
            jpg = Image.open(BytesIO(jpg_content))
            yield image_to_text(jpg, 10, 8)
        except UnidentifiedImageError:
            yield jpg_content.decode()


def get_images_in_gfx(jpg_url):
    """Gets the 5 images, distributed in noncontiguous 5*n indexes"""
    gfx_url = jpg_url.replace("1", "2").replace("jpg", "gfx")
    gfx = read_url(gfx_url)
    for i in range(5):
        img = Image.open(BytesIO(bytes(gfx[i::5])))
        yield image_to_text(img)


url = "http://www.pythonchallenge.com/pc/return/evil.html"
jpg_url = get_last_src_url(url)

if __name__ == "__main__":
    print("\n".join(get_next_jpg_images(jpg_url, (2, 5))))
    print("\n".join(get_images_in_gfx(jpg_url)))
