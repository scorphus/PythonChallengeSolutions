#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# No link for this mission, please check the output data of mission 20

from cache import autocached

import bz2
import zlib


@autocached
def unpack(package):
    """Unpacks package, reversing its content, and alternating between the
    different formats, while “logging” as it goes along"""
    with open(package, "rb") as fd:
        content = fd.read()
    log = ""
    while True:
        try:
            content = zlib.decompress(content)
            log += " "
            continue
        except zlib.error:
            pass
        try:
            content = bz2.decompress(content)
            log += "#"
            continue
        except OSError:
            pass
        content = content[::-1]
        log += "\n"
        if content[0] != 120:
            return log.rstrip()


print(unpack("package.pack"))
