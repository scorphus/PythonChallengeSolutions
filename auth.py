# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/

from base64 import encodebytes
from urllib.request import Request
from urllib.request import urlopen


def open_url(url):
    auth = encodebytes(b"butter:fly").decode().rstrip()
    headers = {"Authorization": f"Basic {auth}"}
    return urlopen(Request(url=url, headers=headers))


def read_url(url):
    return open_url(url).read()


def read_riddle(url):
    """Reads and returns the content of the mission at `url`"""
    return read_url(url).decode()


def get_img_url(url):
    """Extracts the URL of the only image in the mission at `url`"""
    img_src = read_riddle(url).split('src="')[-1].split('"')[0]
    return "{}/{}".format(url.rsplit("/", 1)[0], img_src)
