#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/uzi.html

from datetime import datetime

start = 1996  # Last leap year of the second millennium

probable_dates = ""
for year in range(start, 1000, -20):
    day = f"{year}-01-27"
    date = datetime.strptime(day, "%Y-%m-%d")
    if date.weekday() == 1:
        probable_dates += f"\n * {day}"

print(f"Probable dates are:{probable_dates}\nCheck what happened on them!")
