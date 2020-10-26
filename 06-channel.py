#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/def/channel.html
# Source mentions zip

from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import sys


url = "http://www.pythonchallenge.com/pc/def/channel.zip"
zip_content = urlopen(url).read()

with ZipFile(BytesIO(zip_content)) as channel:
    with channel.open("readme.txt") as readme:
        for line in readme.readlines():
            if "start" in line.decode():
                current = line.decode().strip().split(" ")[-1]
                break
        else:
            raise RuntimeError("Could not find start")
    comments = ""
    while True:
        print(".", end="", flush=True)
        comments += channel.getinfo(current + ".txt").comment.decode()
        try:
            with channel.open(current + ".txt") as current_fp:
                riddle = current_fp.read().decode()
                if "Next nothing is" not in riddle:
                    break
                current = riddle.split(" ")[-1]
        except KeyError:
            break
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"Bang! {e} ({current})")
            sys.exit(1)

print(f"{riddle}\nThe comments form:\n\n{comments}")
