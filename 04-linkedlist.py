#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/linkedlist.php
# http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=12345

import pickle
import sys

from urllib.request import urlopen

cache_file = "04-linkedlist-cache.p"

try:
    with open(cache_file, "rb") as cache_file:
        cache = pickle.load(cache_file)
except IOError:
    cache = dict()

cache_len = len(cache)

url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing={}"
curr = 12345

for _ in range(400):
    sys.stderr.write(".")
    sys.stderr.flush()
    try:
        if curr in cache:
            riddle = cache[curr]
        else:
            riddle = cache[curr] = urlopen(url.format(curr)).read().decode()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"\nBang! {e} ({curr})")
        sys.exit(1)
    try:
        next_ = int(riddle.split(" ")[-1])
    except ValueError:
        if riddle == "Yes. Divide by two and keep going.":
            next_ = curr // 2
        else:
            break
    curr = next_

if len(cache) > cache_len:
    try:
        with open(cache_file, "wb") as cache_file:
            pickle.dump(cache, cache_file)
    except IOError:
        pass

sys.stderr.write(f"{riddle}\n")
