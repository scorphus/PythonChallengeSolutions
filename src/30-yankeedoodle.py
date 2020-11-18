#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/ring/yankeedoodle.html

from auth import get_last_src_url
from auth import read_riddle
from etc import factorize
from itertools import chain
from itertools import product


def read_csv_cells(url):
    """Reads the cells of the CSV mentioned in the riddle"""
    csv_url = get_last_src_url(url).replace("jpg", "csv")
    rows = (line.rstrip(",").split(", ") for line in read_riddle(csv_url).splitlines())
    return list(chain.from_iterable(rows))


def extract_formula(cells, width, height):
    """Extracts the formula hidden in the CSV"""
    it = iter(cells)
    formula = [[" "] * width for _ in range(height)]
    for x, y in product(range(width), range(height)):
        if float(next(it)) < round(1 - height / width, 1):
            formula[y][x] = "#"
    return formula


def apply_formula(cells):
    """Applies the hidden formula on cells"""
    it = iter(cells)
    for _ in range(len(cells) // 3):
        yield int(next(it)[5] + next(it)[5] + next(it)[6])


url = "http://www.pythonchallenge.com/pc/ring/yankeedoodle.html"
cells = read_csv_cells(url)
factors = factorize(len(cells))
print("\n".join("".join(row) for row in extract_formula(cells, *factors[::-1])))
print(bytes(apply_formula(cells)).decode())
