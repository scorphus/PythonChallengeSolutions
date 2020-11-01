#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/pc/hex/decent.html

from auth import read_riddle
from wand.image import Image
from zipfile import crc32  # NOQA used by _update_crc recompiled in patch_update_crc

import inspect
import zipfile


def extract_source(func):
    """Extracts source of func"""
    source = inspect.getsource(func).splitlines()
    indentation = len(source[0]) - len(source[0].lstrip())
    return "\n".join(line[indentation:] for line in source)


def patch_update_crc():
    """Monkey-patch `ZipExtFile._update_crc` to bypass any bad CRC"""
    update_crc_src = extract_source(zipfile.ZipExtFile._update_crc).replace(
        "raise", "return  #"
    )
    exec(compile(update_crc_src, "<string>", "exec"))
    zipfile.ZipExtFile._update_crc = locals()["_update_crc"]  # defined at runtime above


def reveal_mybroken_gif():
    """Extract a gif from a corrupt zip file and displays it as text"""
    patch_update_crc()
    try:
        with zipfile.ZipFile("mybroken.zip", "r") as zip_file, zip_file.open(
            zip_file.namelist()[0]
        ) as gif_file:
            # Pillow couldn't read the corrupt gif, even with
            # PIL.ImageFile.LOAD_TRUNCATED_IMAGES set to True
            mybroken, text = Image(file=gif_file), ""
            for y in range(0, mybroken.size[1], 2):
                line = ""
                for x in range(0, mybroken.size[0], 2):
                    if not mybroken[x, y].blue:
                        line += " "
                    else:
                        line += "*"
                if "*" in line:
                    text += line + "\n"
            return text
    except FileNotFoundError:
        return "Please run mission 24 and rerun this mission"


print(reveal_mybroken_gif())

for line in read_riddle(
    "http://www.pythonchallenge.com/pc/hex/decent.html"
).splitlines():
    if "<" in line:
        continue
    if not line:
        break
    print(line)
