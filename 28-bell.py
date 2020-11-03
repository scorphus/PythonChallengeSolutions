#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/ring/bell.html

from auth import get_img_url
from auth import open_url
from itertools import islice
from PIL import Image as Image


img_url = get_img_url("http://www.pythonchallenge.com/pc/ring/bell.html")
greens = islice(Image.open(open_url(img_url)).tobytes(), 1, None, 3)
for curr, prev in zip(greens, greens):
    if abs(curr - prev) != 42:  # the ultimate answer, oh!!! Boring mission 😒
        print(chr(abs(curr - prev)), end="")
