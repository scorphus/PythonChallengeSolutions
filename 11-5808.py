#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/5808.html

from auth import get_last_src_url
from auth import read_url
from io import BytesIO
from PIL import Image


img_url = get_last_src_url("http://www.pythonchallenge.com/pc/return/5808.html")
img = Image.open(BytesIO(read_url(img_url))).convert("L")
for y in range(0, 2 * img.height // 5, 4):
    for x in range(img.width // 2, img.width, 4):
        if (x + y) % 2 == 0:
            if img.getpixel((x, y)) > 14:
                print("##", end="")
            else:
                print("  ", end="")
    print()
