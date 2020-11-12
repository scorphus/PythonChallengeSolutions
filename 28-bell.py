#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/ring/bell.html

from auth import get_last_src_url
from auth import read_url
from io import BytesIO
from itertools import islice
from PIL import Image as Image


img_url = get_last_src_url("http://www.pythonchallenge.com/pc/ring/bell.html")
greens = islice(Image.open(BytesIO(read_url(img_url))).tobytes(), 1, None, 3)
for curr, prev in zip(greens, greens):
    if abs(curr - prev) != 42:  # 😱 the ultimate answer! Boring mission 😒
        print(chr(abs(curr - prev)), end="")
print(" (hint: ‘it’ is Python)")
