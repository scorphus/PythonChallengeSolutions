#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/ring/yankeedoodle.html

from auth import get_img_url
from auth import read_riddle
from itertools import chain
from math import sqrt


def read_csv_cells(url):
    """Read the cells of the CSV mentioned in the riddle"""
    csv_url = get_img_url(url).replace("jpg", "csv")
    rows = (line.rstrip(",").split(", ") for line in read_riddle(csv_url).splitlines())
    return list(chain.from_iterable(rows))


def obtain_factors(n):
    """Obtain the factors of the length of the list of cells"""
    size, factors = n, []
    for n in range(2, int(sqrt(size))):
        if size % n == 0:
            factors.extend([n, size // n])
    return factors


def extract_formula(cells, width, height):
    """Extract the formula hidden in the CSV"""
    it = iter(cells)
    formula = [[" "] * width for _ in range(height)]
    for x in range(width):
        for y in range(height):
            if float(next(it)) < round(1 - height / width, 1):
                formula[y][x] = "#"
    return formula


def apply_formula(cells):
    """Apply the hidden formula on cells"""
    it = iter(cells)
    while True:
        try:
            yield int(next(it)[5] + next(it)[5] + next(it)[6])
        except StopIteration:
            break


url = "http://www.pythonchallenge.com/pc/ring/yankeedoodle.html"
cells = read_csv_cells(url)
factors = obtain_factors(len(cells))
print("\n".join("".join(row) for row in extract_formula(cells, *factors[::-1])))
print(bytes(apply_formula(cells)).decode())
