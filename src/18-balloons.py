#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/balloons.html
# Or is it http://www.pythonchallenge.com/pc/return/brightness.html?

from auth import get_nth_comment
from auth import read_url
from difflib import Differ
from etc import image_to_text
from io import BytesIO
from PIL import Image

import gzip


def split_deltas(deltas_url):
    """Opens and decompress a gzipped text file and splits each line into two
    deltas"""
    left, right = [], []
    with gzip.open(BytesIO(read_url(deltas_url))) as deltas:
        for line in deltas:
            line = line.decode().rsplit("   ", 1)
            left.append(line[0].strip())
            right.append(line[1].strip())
    return left, right


def compare_deltas(delta_left, delta_right):
    """Compares the deltas with difflib and returns, as bytes, the lines that
    are equal, only on the right and on the left delta"""
    equal, right, left = BytesIO(), BytesIO(), BytesIO()
    for diff in Differ().compare(delta_left, delta_right):
        try:
            chunk = bytes(int(b, 16) for b in diff[2:].split())
        except ValueError:
            continue
        if diff[0] == " ":
            equal.write(chunk)
        elif diff[0] == "+":
            right.write(chunk)
        else:
            left.write(chunk)
    return equal, right, left


url = "http://www.pythonchallenge.com/pc/return/brightness.html"
url_base = url.rsplit("/", 1)[0]
new_path = get_nth_comment(url, 1).rstrip().rsplit(maxsplit=1)[-1]
deltas_url = f"{url_base}/{new_path}"
delta_left, delta_right = split_deltas(deltas_url)
diffs = compare_deltas(delta_left, delta_right)
print("\n".join(image_to_text(Image.open(diff)) for diff in diffs))
