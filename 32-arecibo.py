#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/rock/arecibo.html
# http://www.pythonchallenge.com/pc/rock/up.html
# http://www.pythonchallenge.com/pc/rock/python.html


from auth import get_last_href_url
from auth import get_nth_comment
from auth import read_riddle
from cache import autocached
from itertools import chain
from itertools import product
from itertools import zip_longest
from pyeda.boolalg.expr import exprvar
from pyeda.inter import And
from pyeda.inter import Not
from pyeda.inter import Or


# A tuple with 62 different characters to be used in labeling variables
AZ9 = (
    tuple(map(chr, range(ord("A"), ord("Z") + 1)))
    + tuple(map(chr, range(ord("a"), ord("z") + 1)))
    + tuple(map(str, range(10)))
)


def load_puzzle(puzzle):
    """Load puzzle text input into a tuple of proposition lists"""
    horizontal, vertical = [], []
    puzzle_it = iter(puzzle.splitlines())
    for line in puzzle_it:
        if "horizontal" in line.lower():
            break
    for line in puzzle_it:
        if "vertical" in line.lower():
            break
        if line.rstrip():
            horizontal.append(list(map(int, line.split())))
    for line in puzzle_it:
        if line.rstrip():
            vertical.append(list(map(int, line.split())))
    return horizontal, vertical


def expand(combination, size):
    """Expands a possible combination according to the desired size"""
    if len(combination) == size:
        yield combination
    else:
        for i in range((size - len(combination)) // 2 + 1):
            a = [0] * (size - len(combination) - i)
            b = [0] * i
            yield a + combination + b
            if a != b:
                yield b + combination + a


def gen_all_combinations(proposition, size):
    """Generates all possible combinations of 1's and 0's of a given size
    according to a proposition"""
    rem = size - sum(proposition)
    parts = [[1] * i for i in proposition]
    seps = [[0] * i for i in range(1, rem + 1)]
    for sep in product(*([seps] * (len(proposition) - 1))):
        if sum(map(len, sep)) <= rem:
            yield from expand(
                list(
                    chain.from_iterable(
                        list(chain.from_iterable(t))
                        for t in zip_longest(parts, sep, fillvalue=[])
                    )
                ),
                size,
            )


def gen_vars(size):
    """Generates expression variables for every cell in the grid and returns
    them as rows and columns"""
    chars = AZ9[:size]
    rows_vars = tuple(
        tuple(exprvar("".join(p)) for p in product(char, chars)) for char in chars
    )
    return rows_vars, list(zip(*rows_vars))


def satisfy_all(rows_vars, cols_vars, horizontal, vertical):
    """Uses a SAT Solver to satisfy all horizontal and vertical propositions"""
    terms = []
    for i, row_var in enumerate(rows_vars):
        row_terms = []
        for combination in gen_all_combinations(horizontal[i], len(horizontal)):
            row_terms.append(
                And(*list(v if p else Not(v) for v, p in zip(row_var, combination)))
            )
        terms.append(Or(*row_terms))
    for i, col_var in enumerate(cols_vars):
        col_terms = []
        for combination in gen_all_combinations(vertical[i], len(vertical)):
            col_terms.append(
                And(*list(v if p else Not(v) for v, p in zip(col_var, combination)))
            )
        terms.append(Or(*col_terms))
    return And(*terms).tseitin().satisfy_all()


def sat_ip_to_text(sat_point, rows_vars):
    """Converts a satisfying input point into lines of text, one row per line"""
    text = ""
    for row_var in rows_vars:
        for var in row_var:
            if sat_point[var]:
                text += "▓▓"
            else:
                text += "  "
        text += "\n"
    return text.rstrip()


@autocached
def solve_puzzle(puzzle_url):
    """Solves puzzle in `puzzle_url` and return all possible solutions"""
    puzzle = read_riddle(puzzle_url)
    horizontal, vertical = load_puzzle(puzzle)
    assert len(horizontal) == len(vertical)
    rows_vars, cols_vars = gen_vars(len(horizontal))
    return [
        sat_ip_to_text(ip, rows_vars)
        for ip in satisfy_all(rows_vars, cols_vars, horizontal, vertical)
    ]


url = "http://www.pythonchallenge.com/pc/rock/arecibo.html"
puzzle_path = get_nth_comment(url, 2).rsplit(maxsplit=1)[-1]
url_base = url.rsplit("/", 1)[0]
puzzle_url = f"{url_base}/{puzzle_path}"
print("\n".join(solve_puzzle(puzzle_url)))

url = "http://www.pythonchallenge.com/pc/rock/up.html"
puzzle_url = get_last_href_url(url)
print("\n".join(solve_puzzle(puzzle_url)))

url = "http://www.pythonchallenge.com/pc/rock/python.html"
for line in read_riddle(url).splitlines():
    if "<" not in line:
        print(line.strip())
        break
