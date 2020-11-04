#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/equality.html

from auth import get_nth_comment

import re


riddle = get_nth_comment("http://www.pythonchallenge.com/pc/def/equality.html", 1)
content = "".join(riddle.splitlines())
pattern = re.compile(r"[a-z][A-Z]{3}([a-z])[A-Z]{3}[a-z]")
print("".join(pattern.findall(content)))
