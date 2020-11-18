#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/bull.html

from auth import read_riddle


def look_and_say(digits):
    """Describes a digit as in a look-and-say manner"""
    desc = [1, digits[0]]
    for digit in digits[1:]:
        if desc[-1] == digit:
            desc[-2] += 1
        else:
            desc.extend([1, digit])
    return desc


def look_and_say_nth(n):
    """Generates the nth element of the look-and-say sequence"""
    digits = [1]
    for _ in range(n):
        digits = look_and_say(digits)
    return digits


url = "http://www.pythonchallenge.com/pc/return/bull.html"
n = int(read_riddle(url).rsplit("[", 1)[1].split("]", 1)[0])
print(len(look_and_say_nth(n)))
