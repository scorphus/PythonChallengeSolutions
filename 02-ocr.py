#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/ocr.html

from collections import defaultdict
from urllib.request import urlopen


url = "http://www.pythonchallenge.com/pc/def/ocr.html"
page_source = urlopen(url).read().decode().strip()
page_data = page_source.split("<!--")[2].split("-->")[0]

counter = defaultdict(int)
for char in page_data:
    counter[char] += 1

chars = sorted(counter, key=counter.get)
print("".join(iter(lambda: chars.pop(0), "\n")))
