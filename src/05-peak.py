#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/peak.html
# Source mentions banner.p

from auth import get_last_src_url
from auth import read_url

import pickle


url = "http://www.pythonchallenge.com/pc/def/peak.html"
for row in pickle.loads(read_url(get_last_src_url(url))):
    print("".join(char * times for char, times in row))
