#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/map.html

from auth import get_longest_line


def translate(phrase, rot):
    """Translates `phrase` by shifting each character `rot` positions forward"""
    ord_a = ord("a")
    diff_az = ord("z") + 1 - ord_a
    translated = ""
    for char in phrase:
        if "a" <= char <= "z":
            char = chr(((ord(char) - ord_a + rot) % diff_az) + ord_a)
        translated += char
    return translated


original = get_longest_line("http://www.pythonchallenge.com/pc/def/map.html")
translated = translate(original, 2)
print(original)
print(translated)
print("map ->", "map".translate(str.maketrans(original, translated)))
