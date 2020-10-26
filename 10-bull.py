#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/bull.html

from base64 import encodebytes
from urllib.request import Request
from urllib.request import urlopen


def describe(n):
    n_str = f"{n}"
    desc = ""
    curr, count = n_str[0], 0
    for digit in n_str:
        if digit != curr:
            desc = f"{desc}{count}{curr}"
            curr, count = digit, 0
        count += 1
    return int(f"{desc}{count}{curr}")


url = "http://www.pythonchallenge.com/pc/return/sequence.txt"
auth = encodebytes(b"huge:file").decode().rstrip()
headers = {"Authorization": f"Basic {auth}"}
text_data = urlopen(Request(url=url, headers=headers)).read().decode()
a = [int(n.strip()) for n in text_data.split("[")[1].split(",")[:-1]]

for i in range(len(a), 31):
    a.append(describe(a[i - 1]))

print("len(a[30]) =", len(str(a[30])))
