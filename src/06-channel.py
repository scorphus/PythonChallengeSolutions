#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/channel.html
# Source mentions zip

from auth import get_nth_comment
from auth import read_url
from io import BytesIO
from zipfile import ZipFile


def read_comments_from_zip(url):
    with ZipFile(BytesIO(read_url(url))) as channel:
        with channel.open(channel.namelist()[-1]) as readme:
            for line in readme.readlines():
                if "start" in line.decode():
                    curr = line.decode().strip().rsplit(maxsplit=1)[-1]
                    break
            else:
                raise RuntimeError("Could not find start")
        comments = ""
        while True:
            try:
                comments += channel.getinfo(f"{curr}.txt").comment.decode()
                with channel.open(f"{curr}.txt") as current_fp:
                    curr = current_fp.read().decode().rsplit(maxsplit=1)[-1]
            except KeyError:
                return comments
            except KeyboardInterrupt:
                exit(0)
            except Exception as e:
                print(f"Bang! {e} ({curr})")
                exit(1)


url = "http://www.pythonchallenge.com/pc/def/channel.html"
zip_url = url.replace("html", get_nth_comment(url, 1).split()[-1])
print(read_comments_from_zip(zip_url))
