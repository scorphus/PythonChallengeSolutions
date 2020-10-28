#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/bonus.html

from base64 import encodebytes
from urllib.request import Request
from urllib.request import urlopen

import this


url = "http://www.pythonchallenge.com/pc/hex/bonus.html"
auth = encodebytes(b"butter:fly").decode().rstrip()
headers = {"Authorization": f"Basic {auth}"}

riddle_source = urlopen(Request(url=url, headers=headers)).read().decode()
riddle_data = riddle_source.split("<!--")[-1].split("-->")[0].strip("\n'")
print(riddle_data)
print("Translated:", "".join(this.d.get(c, c) for c in riddle_data))

search = " ".join(riddle_data.split()[:-1])
for guiding_principle in this.s.split("\n"):
    if search in guiding_principle.lower():
        print(guiding_principle)
        print("Translated:", "".join(this.d.get(c, c) for c in guiding_principle))
        break
