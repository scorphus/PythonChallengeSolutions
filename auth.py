# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/

from base64 import encodebytes
from cache import autocached
from urllib.request import Request
from urllib.request import urlopen


credentials = {
    "http://www.pythonchallenge.com/pc/def": b"",
    "http://www.pythonchallenge.com/pc/return": b"huge:file",
    "http://www.pythonchallenge.com/pc/hex": b"butter:fly",
    "http://www.pythonchallenge.com/pc/ring": b"repeat:switch",
}


def get_credentials(url):
    base_url = url.rsplit("/", 1)[0]
    return credentials[base_url]


def open_url(url):
    auth = encodebytes(get_credentials(url)).decode().rstrip()
    headers = {"Authorization": f"Basic {auth}"} if auth else {}
    return urlopen(Request(url=url, headers=headers))


@autocached("read_url.cache")
def read_url(url):
    return open_url(url).read()


def read_riddle(url):
    """Reads and returns the content of the mission at `url`"""
    return read_url(url).decode()


def get_last_attr_url(url, attr):
    """Extracts the URL of the last `attr` attribute in the mission at `url`"""
    img_src = read_riddle(url).split(f'{attr}="')[-1].split('"')[0]
    return "{}/{}".format(url.rsplit("/", 1)[0], img_src)


def get_last_src_url(url):
    """Extracts the URL of the last `src` attribute in the mission at `url`"""
    return get_last_attr_url(url, "src")


def get_last_href_url(url):
    """Extracts the URL of the last `href` attribute in the mission at `url`"""
    return get_last_attr_url(url, "href")


def get_longest_line(url):
    return max(read_riddle(url).splitlines(), key=len)


def get_nth_comment(url, n):
    return read_riddle(url).split("<!--", n)[n].split("-->", 1)[0]
