#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/ambiguity.html

from auth import get_last_src_url
from auth import read_url
from cache import autocached
from cache import cached
from etc import image_to_text
from io import BytesIO
from itertools import product
from PIL import Image
from PIL import UnidentifiedImageError
from zipfile import ZipFile

import logging


turns_set = {(1, 0), (0, 1), (-1, 0), (0, -1)}

turns_map = {
    (1, 0): turns_set - {(-1, 0)},
    (-1, 0): turns_set - {(1, 0)},
    (0, 1): turns_set - {(0, -1)},
    (0, -1): turns_set - {(0, 1)},
}


def load_maze(url):
    """Fetches and loads maze.png then returns its pixels and size"""
    maze_url = get_last_src_url(url)
    maze = Image.open(BytesIO(read_url(maze_url)))
    return maze.load(), maze.size


def find_black_square(maze, size, row):
    for x in range(size[0]):
        if maze[x, row][0] == 0:
            return x, row


def explore(curr_dir, curr_square, maze):
    """Explores the possible vicinities of a current square"""
    x, y = curr_square
    for dx, dy in turns_map[curr_dir]:
        if maze[x + dx, y + dy][2] == 0:
            yield (x + dx, y + dy), (dx, dy)


@cached
def tumble_down(maze, start, finish, cache):
    """Tumbles down the maze in a DFS fashion"""
    if "result_data" in cache:
        return cache["result_data"]
    data, visited, next_squares = [], {start}, [(start, 0, (0, 1))]
    while next_squares:
        curr_square, steps, curr_dir = next_squares.pop()
        if curr_square == finish:
            break
        del data[steps:]  # Deadend? Remove all steps in wrong direction
        visited.add(curr_square)
        for square, direction in explore(curr_dir, curr_square, maze):
            if square not in visited:
                next_squares.append((square, steps + 1, direction))
        data.append(maze[curr_square][0])
    cache["result_data"] = bytes(data[1::2])  # Skip every even-indexed pixel 🤷
    return cache["result_data"]


def extract_image(data):
    """Tries and extracts the image inside data (which is a zipfile)"""
    with ZipFile(BytesIO(data)) as zip_file:
        for name in zip_file.namelist()[::-1]:
            try:
                return Image.open(BytesIO(zip_file.read(name)))
            except UnidentifiedImageError:
                logging.warning("%s does not seem to be an image", name)


@autocached
def crop_blue_only(image):
    """Returns a cropped image with `image`'s bluest pixels"""
    img = Image.new("L", (image.width, image.height))
    for xy in product(range(image.width), range(image.height)):
        r, g, b = image.getpixel(xy)
        if b > 1.2 * r and b > 1.2 * g:
            img.putpixel(xy, b)
    return img.crop((0, img.height // 2, img.width, img.height))


maze, size = load_maze("http://www.pythonchallenge.com/pc/hex/ambiguity.html")
start = find_black_square(maze, size, 0)
finish = find_black_square(maze, size, size[1] - 1)
data = tumble_down(maze, start, finish)

if __name__ == "__main__":
    image = extract_image(data)
    new_image = crop_blue_only(image)
    print(image_to_text(new_image))
