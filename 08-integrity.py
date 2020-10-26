#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/integrity.html

from urllib.request import urlopen

import bz2


url = "http://www.pythonchallenge.com/pc/def/integrity.html"
page_source = urlopen(url).read().decode("unicode_escape").encode("latin1")
page_data = page_source.split(b"<!--")[1].split(b"-->")[0]

_, un, _, pw, _ = page_data.split(b"'")

dec_un = bz2.decompress(un)
dec_pw = bz2.decompress(pw)

print(f"user: {dec_un.decode()}")
print(f"pass: {dec_pw.decode()}")
