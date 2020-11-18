#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/idiot.html

from auth import get_last_href_url
from auth import get_last_src_url
from auth import read_riddle
from auth import read_url
from auth import read_url_and_headers
from cache import autocached
from io import BytesIO
from urllib.error import HTTPError
from zipfile import ZipFile


def range_header(start):
    return {"Range": f"bytes={start}-"}


@autocached
def get_pwd_and_size(img_url):
    """Loops through the responses, varying the Range header until it fails. By
    then returns part of the last seen message as password and the last seen
    range size — if it ever changes during the process, we don't care"""
    start = size = 0
    while True:
        try:
            msg, headers = read_url_and_headers(img_url, range_header(start))
            msg = msg.decode().strip()
        except UnicodeDecodeError:
            pass
        except HTTPError:
            return msg.split(maxsplit=2)[1].rstrip(".")[::-1], int(size)
        content_range = headers["Content-Range"].split(maxsplit=1)[1]
        start_end, size = content_range.split("/", 1)
        start = int(start_end.rsplit("-", 1)[-1]) + 1


def advance_rewind_and_extract(img_url, pwd, size):
    """Finds the correct range start and use the password to ultimately extract
    and display next mission's content"""
    msg = read_riddle(img_url, range_header(size)).strip()
    msg = read_riddle(img_url, range_header(size - len(msg) - 2)).strip()
    start = msg.rstrip(".").rsplit(maxsplit=1)[-1]
    zip_content = read_url(img_url, range_header(start)).strip()
    with ZipFile(BytesIO(zip_content), "r") as zip_file:
        readme, package = zip_file.namelist()
        print(zip_file.read(readme, pwd=pwd.encode()).decode())
        print(zip_file.extract(package, pwd=pwd.encode()))


url = "http://www.pythonchallenge.com/pc/hex/idiot.html"
next_url = get_last_href_url(url)
img_url = get_last_src_url(next_url)
pwd, size = get_pwd_and_size(img_url)
advance_rewind_and_extract(img_url, pwd, size)
