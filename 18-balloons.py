#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/balloons.html
# http://www.pythonchallenge.com/pc/return/brightness.html
# Source mentions deltas.gz

import gzip

from base64 import encodebytes
from contextlib import ExitStack
from difflib import Differ
from urllib.request import Request, urlopen

url = "http://www.pythonchallenge.com/pc/return/deltas.gz"
auth = encodebytes(b"huge:file").decode().rstrip()
headers = {"Authorization": f"Basic {auth}"}

delta_l, delta_r = [], []

with gzip.open(urlopen(Request(url=url, headers=headers))) as deltas:
    for line in deltas:
        line = line.strip().decode()
        delta_l.append(line[:53])
        delta_r.append(line[56:])

differ = Differ()

with ExitStack() as stack:
    left = stack.enter_context(open("18-left.png", "wb"))
    right = stack.enter_context(open("18-right.png", "wb"))
    equal = stack.enter_context(open("18-equal.png", "wb"))
    for diff in differ.compare(delta_l, delta_r):
        try:
            chunk = bytes([int(b, 16) for b in diff[2:].split(" ")])
        except ValueError:
            chunk = bytes(len(chunk))
        if diff[0] is "-":
            left.write(chunk)
        elif diff[0] is "+":
            right.write(chunk)
        else:
            equal.write(chunk)

print("Open 18-left.png, 18-right.png and 18-equal.png")
