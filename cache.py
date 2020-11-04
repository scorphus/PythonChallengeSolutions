# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/

from functools import wraps

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


def cached(file_path):
    """Decorates a function providing a file-based cache that is read and
    updated on every run"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cache = read_cache(file_path)
            result = f(*(*args, cache), **kwargs)
            write_cache(file_path, cache)
            return result

        return wrapper

    return decorator
