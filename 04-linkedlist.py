#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/linkedlist.html

from auth import read_riddle

import pickle


def read_cache(file_path):
    try:
        with open(file_path, "rb") as fd:
            return pickle.load(fd)
    except IOError:
        return {}


def write_cache(file_path, cache):
    try:
        with open(file_path, "wb") as fd:
            pickle.dump(cache, fd)
    except IOError:
        pass


def unravel_riddle(url, cache):
    """Follows the riddle leads until the end to ultimately unravel it"""
    curr = 12345
    while True:
        try:
            if curr not in cache:
                cache[curr] = read_riddle(f"{url}?nothing={curr}")
            riddle = cache[curr]
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            print(f"Bang! {e} ({curr})")
            exit(1)
        try:
            next_ = int(riddle.rsplit(maxsplit=1)[-1])
        except ValueError:
            if riddle == "Yes. Divide by two and keep going.":
                next_ = curr // 2
            else:
                return riddle
        curr = next_


url = "http://www.pythonchallenge.com/pc/def/linkedlist.html"
url_base = url.rsplit("/", 1)[0]
new_path = read_riddle(url).rstrip()

cache_file = "04-linkedlist-cache.p"
cache = read_cache(cache_file)
cache_len = len(cache)

print(unravel_riddle(f"{url_base}/{new_path}", cache))

if len(cache) > cache_len:
    write_cache(cache_file, cache)
