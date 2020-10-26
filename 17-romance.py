#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/linkedlist.php
# http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=12345

import bz2
import sys

from contextlib import suppress
from http.cookiejar import CookieJar
from urllib.parse import unquote_to_bytes
from urllib.request import HTTPCookieProcessor, Request, build_opener, urlopen
from xmlrpc.client import ServerProxy

url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing={}"
curr = 12345

msg = ""
cookie_jar = CookieJar()
url_opener = build_opener(HTTPCookieProcessor(cookie_jar))

try:
    with open("17-cookie-cache.txt", "r") as msg_file:
        msg = msg_file.read()
except IOError:
    for _ in range(400):
        print(".", end="", flush=True)
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
    with suppress(IOError):
        with open("17-cookie-cache.txt", "w") as msg_file:
            msg_file.write(msg)

dec_msg = bz2.decompress(unquote_to_bytes(msg.replace("+", " "))).decode()
print(dec_msg)

url = "http://www.pythonchallenge.com/pc/phonebook.php"
with ServerProxy(url) as proxy:
    print("phone('Leopold'): {}".format(proxy.phone("Leopold")))

url = "http://www.pythonchallenge.com/pc/stuff/violin.php"
info = dec_msg.split('"')[-2].replace(" ", "+")
print(urlopen(Request(url, headers={"Cookie": f"info={info}"})).read().decode())
