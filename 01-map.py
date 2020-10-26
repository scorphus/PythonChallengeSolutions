#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/map.html

original = (
    "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc  dmp. "
    "bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. "
    "sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
)

chr_a = ord("a")
diff_az = ord("z") + 1 - chr_a

translated = ""

for c in original:
    if "a" <= c <= "z":
        c = chr(((ord(c) - chr_a + 2) % diff_az) + chr_a)
    translated += c

print(translated)

transtab = str.maketrans(original, translated)
print("map".translate(transtab))
