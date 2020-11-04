#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/oxygen.html

from auth import get_last_src_url
from auth import read_url
from io import BytesIO
from itertools import islice
from itertools import takewhile

import png


url = "http://www.pythonchallenge.com/pc/def/oxygen.html"
png_content = read_url(get_last_src_url(url))
png_reader = png.Reader(BytesIO(png_content))
_, height, content, *_ = png_reader.read()
middle_row = next(islice(content, height // 2, height // 2 + 1))

message = "".join(
    chr(n) for n in takewhile(lambda n: n != ord("]"), islice(middle_row, 5, None, 28))
)
print("".join(chr(int(d)) for d in message.split("[", 1)[-1].split(", ")))
