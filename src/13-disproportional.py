#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/disproportional.html

from auth import get_last_href_url
from cache import autocached
from xmlrpc.client import ServerProxy


@autocached
def get_evil():
    """Reads part of last mission's riddle; did you miss that???"""
    evil = __import__("12-evil")
    return next(evil.get_next_jpg_images(evil.jpg_url, (4, 5))).split()[0]


@autocached
def proxy_phone(proxy_url, callee):
    with ServerProxy(proxy_url) as proxy:
        return proxy.phone(callee)


url = "http://www.pythonchallenge.com/pc/return/disproportional.html"
proxy_url = get_last_href_url(url)

if __name__ == "__main__":
    callee = get_evil()
    print(proxy_phone(proxy_url, callee))
