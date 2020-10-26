#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# No link for this mission, please check the output data of mission 20

import bz2
import zlib


def unpack(content):
    while True:
        try:
            content = zlib.decompress(content)
            print(" ", end="")
            continue
        except zlib.error:
            pass
        try:
            content = bz2.decompress(content)
            print("#", end="")
            continue
        except OSError:
            pass
        content = content[::-1]
        print()
        if content[0] != 120 and content[1] != 156:
            return content


with open("package.pack", "rb") as package:
    print(unpack(package.read()).decode(), "👆")
