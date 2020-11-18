#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/copper.html

from auth import get_nth_comment
from auth import read_url
from cache import autocached
from io import BytesIO
from PIL import Image
from PIL import ImageSequence


@autocached
def load_pixels(img_url):
    """Returns a list of (x, y) coordinates of all pixels from all frames of the
    GIT at `img_url`"""
    image = Image.open(BytesIO(read_url(img_url)))
    pixels = [frame.getbbox()[:2] for frame in ImageSequence.Iterator(image)]
    min_x, min_y = min(p[0] for p in pixels), min(p[1] for p in pixels)
    max_x, max_y = max(p[0] for p in pixels), max(p[1] for p in pixels)
    assert image.width == image.height and min_x == min_y and max_x == max_y
    return pixels, min_x, max(p[0] for p in pixels) - min_x


def draw_word(pixels, min_pos, max_diff):
    """Follows each pixel coordinate as direction and registers each new
    position in the returned dict that is later displayed as a word"""
    word, offset = {}, min_pos + max_diff // 2
    char_width = char_count = x = y = 0
    x_lim = y_lim = (0, 0)
    for dx, dy in pixels:
        dx = (dx - offset) // 2
        dy = (dy - offset) // 2
        if dx == dy == 0:
            if char_width == 0:
                char_width = x_lim[1] * 2
            x, y = char_count * char_width, 0
            char_count += 1
        x += dx
        y += dy
        word[(x, y)] = True
        x_lim = min(x_lim[0], x), max(x_lim[1], x + 1)
        y_lim = min(y_lim[0], y), max(y_lim[1], y + 1)
    return word, x_lim, y_lim


url = "http://www.pythonchallenge.com/pc/hex/copper.html"
riddle_data = get_nth_comment(url, 1)

url_base = url.rsplit("/", 1)[0]
img_name = next(s for s in riddle_data.split() if "." in s)
pixels, min_pos, max_diff = load_pixels("/".join((url_base, img_name)))
word, x_lim, y_lim = draw_word(pixels, min_pos, max_diff)
print(
    "\n".join(
        "".join("#" if (x, y) in word else " " for x in range(*x_lim))
        for y in range(*y_lim)
    )
)
