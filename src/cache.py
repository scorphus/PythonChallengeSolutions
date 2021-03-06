# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/

from collections import Hashable
from functools import wraps

import hashlib
import inspect
import logging
import pickle


def _read_cache(file_path):
    try:
        with open(file_path, "rb") as fd:
            return pickle.load(fd)
    except IOError:
        return {}


def _write_cache(file_path, cache):
    try:
        with open(file_path, "wb") as fd:
            pickle.dump(cache, fd)
    except IOError:
        logging.exception("error writing cache")


def _file_cacher(cacher):
    """Decorates other decorators defined below providing them with a file path
    regardless of how they're used"""

    @wraps(cacher)
    def wrapper(file_path=None, *args, **kwargs):
        if inspect.isfunction(file_path):
            func_file_path = f"{inspect.getfile(file_path).rsplit('.', 1)[0]}.cache"
            return cacher(func_file_path)(file_path, *args, **kwargs)
        if file_path is None:
            file_path = f"{inspect.stack()[-1].filename.rsplit('.', 1)[0]}.cache"
        return cacher(file_path, *args, **kwargs)

    return wrapper


@_file_cacher
def cached(file_path):
    """Decorates a function providing a file-based cache that is read and
    updated on every run"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cache = _read_cache(file_path)
            result = f(*(*args, cache), **kwargs)
            _write_cache(file_path, cache)
            return result

        return wrapper

    return decorator


def _get_cache_key(*args, **kwargs):
    if not args and not kwargs:
        return None
    if args and not kwargs and len(args) == 1 and isinstance(args[0], Hashable):
        return args[0]
    return hashlib.sha1(pickle.dumps((args, kwargs))).hexdigest()


@_file_cacher
def autocached(file_path, reset=False):
    """Decorates a function providing a file-based cache that is read and
    updated on every run. The function result is automatically cached and
    returned"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cache = _read_cache(file_path)
            key = _get_cache_key(*args, **kwargs) or f.__name__
            if key not in cache or reset:
                cache[key] = f(*args, **kwargs)
            _write_cache(file_path, cache)
            return cache[key]

        return wrapper

    return decorator
