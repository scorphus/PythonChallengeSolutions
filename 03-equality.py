#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/equality.html

import re

from urllib.request import urlopen

url = "http://www.pythonchallenge.com/pc/def/equality.html"
page_source = urlopen(url).read().decode().strip()
page_data = page_source.split("<!--")[1].split("-->")[0]
content = "".join(page_data.split("\n"))
pattern = re.compile(r"[a-z][A-Z]{3}([a-z])[A-Z]{3}[a-z]")
print("".join(pattern.findall(content)))
