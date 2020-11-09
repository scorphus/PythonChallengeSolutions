#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/return/romance.html

from auth import read_riddle
from cache import autocached
from cache import cached
from http.cookiejar import CookieJar
from urllib.parse import unquote_to_bytes
from urllib.request import build_opener
from urllib.request import HTTPCookieProcessor

import bz2
import sys


@autocached
def discover_url():
    """Retrieves the query string param name from the first cookie set by
    mission 04's URL and returns a formatting string with URL and the param"""
    cookie_jar = CookieJar()
    linkedlist = __import__("04-linkedlist")
    url = f"{linkedlist.url_base}/{linkedlist.new_path}"
    build_opener(HTTPCookieProcessor(cookie_jar)).open(url)
    the_one_cookie = list(cookie_jar)[0].value
    qs_param = the_one_cookie.rstrip(".").rsplit("+", 1)[-1]
    return f"{url}?{qs_param}={{}}"


@cached
def unravel_message(url, cache):
    """Follows the riddle until the end — as in mission 04 — but this time
    looking at the first cookie. Then returns the message decompressed."""
    curr = 12345
    cookie_jar = CookieJar()
    url_opener = build_opener(HTTPCookieProcessor(cookie_jar))
    msg = cache.get("msg", "")
    if not msg:
        while True:
            try:
                resp = url_opener.open(url.format(curr), timeout=3)
                riddle = resp.read().decode()
                cookie = list(cookie_jar)[0]
                msg += cookie.value
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                print(f"\nBang! {e} ({curr})")
                sys.exit(1)
            try:
                next_ = int(riddle.split(" ")[-1])
            except ValueError:
                break
            curr = next_
        cache["msg"] = msg
    return bz2.decompress(unquote_to_bytes(msg.replace("+", " "))).decode()


@autocached
def proxy_phone(callee):
    """Uses mission 13's capabilities to phone"""
    disproportional = __import__("13-disproportional")
    resp = disproportional.proxy_phone(disproportional.proxy_url, callee)
    return resp.rsplit("-", 1)[-1].lower()


@autocached
def discover_next_url(url):
    """Retrieves the riddle URL sitting at `url` — 🤷"""
    url_base = url.rsplit("/", 1)[0]
    new_path = read_riddle(url).rstrip("\n.").rsplit(maxsplit=1)[-1]
    return f"{url_base}/{new_path}"


@autocached
def unravel_riddle(msg, new_url):
    """Uses `message` as cookie to finally unravel the riddle at `new_url`"""
    cookie = f"""info={msg.split('"', 2)[1].replace(" ", "+")}"""
    riddle = read_riddle(new_url, headers={"Cookie": cookie})
    for line in (line.lstrip() for line in riddle.splitlines()):
        if not line.startswith("<"):
            return line.rsplit(maxsplit=1)[-1].split(".", 1)[0]


url = "http://www.pythonchallenge.com/pc/return/romance.html"
msg = unravel_message(discover_url())
response = proxy_phone("Leopold")  # duh... Mozart's father
new_url = discover_next_url(url.replace("romance", response))
print(unravel_riddle(msg, new_url))
