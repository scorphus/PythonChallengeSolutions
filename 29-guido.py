#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/ring/guido.html

from auth import read_riddle

import bz2


riddle = read_riddle("http://www.pythonchallenge.com/pc/ring/guido.html")
data = (len(line) for line in riddle.splitlines() if "<" not in line)
print(bz2.decompress(bytes(data)).decode())
