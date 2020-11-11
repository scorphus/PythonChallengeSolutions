#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/integrity.html

from auth import get_last_href_url
from auth import read_url

import bz2


url = "http://www.pythonchallenge.com/pc/def/integrity.html"
page_source = read_url(url).decode("unicode_escape").encode("latin1")
page_data = page_source.split(b"<!--", 1)[1].split(b"-->", 1)[0]

_, un, _, pw, _ = page_data.split(b"'")
print(f"next: {get_last_href_url(url)}")
print(f"user: {bz2.decompress(un).decode()}")
print(f"pass: {bz2.decompress(pw).decode()}")
