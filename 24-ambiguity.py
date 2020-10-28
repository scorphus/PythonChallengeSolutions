#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/ambiguity.html

from base64 import encodebytes
from io import BytesIO
from PIL import Image
from urllib.request import Request
from urllib.request import urlopen
from zipfile import ZipFile


turns_set = {(1, 0), (0, 1), (-1, 0), (0, -1)}

turns_map = {
    (1, 0): turns_set - {((-1, 0))},
    (-1, 0): turns_set - {((1, 0))},
    (0, 1): turns_set - {((0, -1))},
    (0, -1): turns_set - {((0, 1))},
}


def load_maze():
    """Fetches and loads maze.png then returns its pixels and size"""
    url = "http://www.pythonchallenge.com/pc/hex/ambiguity.html"
    auth = encodebytes(b"butter:fly").decode().rstrip()
    headers = {"Authorization": f"Basic {auth}"}
    riddle_source = urlopen(Request(url=url, headers=headers)).read().decode()
    url = url.replace("ambiguity.html", riddle_source.split('src="')[-1].split('"')[0])
    maze = Image.open(urlopen(Request(url=url, headers=headers)))
    return maze.load(), maze.size


def find_black_square(maze, size, row):
    width, _ = size
    for x in range(width):
        if maze[x, row][0] == 0:
            return x, row


def explore(curr_dir, curr_square, maze):
    """Explores the possible vicinities of a current square"""
    x, y = curr_square
    for dx, dy in turns_map[curr_dir]:
        if maze[x + dx, y + dy][2] == 0:
            yield (x + dx, y + dy), (dx, dy)


def tumble_down(maze, start, finish):
    """Tumbles down the maze in a DFS fashion"""
    data = []
    visited, next_squares = {start}, [(start, 0, (0, 1))]
    while next_squares:
        curr_square, steps, curr_dir = next_squares.pop()
        if curr_square == finish:
            break
        # Deadend? Remove all steps in wrong direction
        del data[steps:]
        visited.add(curr_square)
        for square, direction in explore(curr_dir, curr_square, maze):
            if square not in visited:
                next_squares.append((square, steps + 1, direction))
        data.append(maze[curr_square][0])
    # Skip every even-indexed pixel 🤷🏻‍♂️
    return bytes(data[1::2])


maze, size = load_maze()
start = find_black_square(maze, size, 0)
finish = find_black_square(maze, size, size[1] - 1)
data = tumble_down(maze, start, finish)
with ZipFile(BytesIO(data), "r") as zip_file:
    print("Check", zip_file.extract(zip_file.namelist()[0]))
