#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/ocr.html

from auth import get_nth_comment
from collections import Counter


riddle = get_nth_comment("http://www.pythonchallenge.com/pc/def/ocr.html", 2)
counter = Counter(riddle)
print("".join(filter(lambda key: counter[key] == 1, counter)))
