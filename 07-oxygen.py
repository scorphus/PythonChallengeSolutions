#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/oxygen.html
# Source mentions oxygen.png

from itertools import islice
from itertools import takewhile
from urllib.request import urlopen

import png


url = "http://www.pythonchallenge.com/pc/def/oxygen.png"
png_reader = png.Reader(urlopen(url))
height, content = png_reader.read()[1:3]
middle_row = next(islice(content, height // 2, height // 2 + 1))

message = "".join(
    chr(n) for n in takewhile(lambda n: n != ord("]"), islice(middle_row, 5, None, 28))
)
print(f"Message is: {message}...")

next_level = "".join(chr(int(d)) for d in message.split("[", 1)[-1].split(", "))
print(f"Next level: {next_level}")
